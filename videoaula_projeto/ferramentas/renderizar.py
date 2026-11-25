"""Renderiza os quadros de um capítulo no Chrome (Playwright) e monta o MP4 com FFmpeg.

Só quadros diferentes são capturados: durante a fala o quadro fica parado, então cada
imagem recebe a duração certa no arquivo de lista do FFmpeg (timeline determinística).
Quadros de blocos que não mudaram são reaproveitados do cache.

Uso: python ferramentas/renderizar.py 3            (capítulo 3)
     python ferramentas/renderizar.py 3 --ate 5    (só os 5 primeiros blocos, para teste)
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parents[1]
FPS = 30


def dados_motor():
    tr = json.loads((RAIZ / 'dados' / 'tracos.json').read_text(encoding='utf-8'))
    return dict(codigo=json.loads((RAIZ / 'dados' / 'codigo.json').read_text(encoding='utf-8')),
                layout=json.loads((RAIZ / 'dados' / 'layout.json').read_text(encoding='utf-8')),
                ligacoes=tr['ligacoes'])


def chave_bloco(linha, i):
    b = linha['blocos'][i]
    ant = linha['blocos'][i - 1]['visual'] if i > 0 else None
    texto = json.dumps([b['visual'], ant, [f['legenda'] for f in b['frases']], b['transicao'], i,
                        len(linha['blocos']), linha['titulo'], (RAIZ / 'motor' / 'motor.js').stat().st_mtime,
                        (RAIZ / 'motor' / 'estilo.css').stat().st_mtime], ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(texto.encode()).hexdigest()[:14]


def renderizar(numero, ate=None, qualidade=92):
    linha = json.loads((RAIZ / 'cache' / f'linha_cap{numero:02d}.json').read_text(encoding='utf-8'))
    blocos = linha['blocos'][:ate] if ate else linha['blocos']
    pasta = RAIZ / 'cache' / 'quadros' / f'cap{numero:02d}'
    pasta.mkdir(parents=True, exist_ok=True)
    lista, capturados = [], 0
    with sync_playwright() as pw:
        nav = pw.chromium.launch(channel='chrome', headless=True)
        pagina = nav.new_page(viewport=dict(width=1920, height=1080), device_scale_factor=1)
        pagina.goto((RAIZ / 'motor' / 'index.html').as_uri())
        pagina.evaluate('([t, d]) => iniciar(t, d)', [linha, dados_motor()])
        for i, b in enumerate(blocos):
            chave = chave_bloco(linha, i)
            dir_b = pasta / f'{i:03d}_{chave}'
            quadros = []                       # (arquivo, duração em quadros)
            trans = b['transicao']
            for f in range(1, trans + 1):
                quadros.append((dir_b / f't{f:02d}.jpg', i, f / trans, 0, 1))
            q0 = b['frases'][0]['quadros'] - trans
            quadros[-1] = (quadros[-1][0], i, 1.0, 0, 1 + q0)
            for k, fr in enumerate(b['frases'][1:], start=1):
                quadros.append((dir_b / f'f{k:02d}.jpg', i, 1.0, k, fr['quadros']))
            if not all(q[0].exists() for q in quadros):
                dir_b.mkdir(exist_ok=True)
                for arq, bi, p, k, _ in quadros:
                    pagina.evaluate('([i, p, k]) => desenhar(i, p, k)', [bi, p, k])
                    pagina.screenshot(path=str(arq), type='jpeg', quality=qualidade)
                    capturados += 1
            for arq, *_, dur in quadros:
                lista.append((arq, dur))
            print(f'\r  bloco {i + 1}/{len(blocos)}', end='', flush=True)
        nav.close()
    print(f'\n  {capturados} quadros capturados, {len(lista)} imagens na lista')
    total = sum(d for _, d in lista)
    arq_lista = RAIZ / 'cache' / f'lista_cap{numero:02d}.txt'
    with open(arq_lista, 'w', encoding='utf-8') as fl:
        fl.write('ffconcat version 1.0\n')
        for arq, dur in lista:
            fl.write(f"file '{arq.as_posix()}'\nduration {dur / FPS:.6f}\n")
        fl.write(f"file '{lista[-1][0].as_posix()}'\n")   # o último quadro precisa ser repetido
    saida = RAIZ / 'capitulos' / f'cap{numero:02d}.mp4'
    if ate:
        saida = RAIZ / 'testes' / f'teste_cap{numero:02d}_{ate}blocos.mp4'
    saida.parent.mkdir(exist_ok=True)
    audio = RAIZ / 'audio' / f'cap{numero:02d}.wav'
    cmd = ['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(arq_lista), '-i', str(audio),
           '-vf', f'fps={FPS},scale=in_range=full:out_range=limited:in_color_matrix=bt601:out_color_matrix=bt709,format=yuv420p',
           '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
           '-profile:v', 'high', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-ac', '2',
           '-t', f'{total / FPS:.3f}', '-movflags', '+faststart', str(saida)]
    subprocess.run(cmd, check=True)
    print(f'  gravado {saida.name}: {total / FPS:.1f} s')
    return saida


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('capitulos', type=int, nargs='+')
    ap.add_argument('--ate', type=int)
    a = ap.parse_args()
    for n in a.capitulos:
        renderizar(n, a.ate)
