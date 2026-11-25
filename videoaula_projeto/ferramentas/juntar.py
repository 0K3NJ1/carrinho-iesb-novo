"""Junta os capítulos no vídeo final e gera capitulos.txt, legendas.srt, roteiro_completo.md e matriz_de_cobertura.md.

Uso: python ferramentas/juntar.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
FPS = 30


def duracao(arq):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(arq)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def hms(s, srt=False):
    h, resto = divmod(s, 3600)
    m, seg = divmod(resto, 60)
    if srt:
        return f'{int(h):02d}:{int(m):02d}:{int(seg):02d},{int(round((seg - int(seg)) * 1000)) % 1000:03d}'
    return f'{int(h):02d}:{int(m):02d}:{int(seg):02d}'


def limpar(texto):
    return re.sub(r'\*\*([^*]+)\*\*', r'\1', texto.replace('<br>', ' — '))


def resumo_visual(v):
    t = v['tipo']
    if t == 'dividido':
        return resumo_visual(v['esquerda']) + ' | ' + resumo_visual(v['direita'])
    if t == 'vertical':
        return resumo_visual(v['cima']) + ' / ' + resumo_visual(v['baixo'])
    if t == 'codigo':
        if 'livre' in v:
            return f"código de exemplo ({v.get('titulo')})"
        lin = v.get('linhas')
        return f"código: célula {v['celula']}" + (f", linhas {lin[0]}–{lin[1]}" if lin else '')
    if t == 'grafo':
        extra = []
        if v.get('caminho'):
            extra.append('caminho ' + ' → '.join(v['caminho']))
        if v.get('carrinho'):
            extra.append('carrinho animado')
        return 'grafo do campus' + (' (' + '; '.join(extra) + ')' if extra else '')
    return f"{t}: {limpar(str(v.get('titulo') or v.get('pergunta') or ''))}"


def refs_codigo(v):
    t = v['tipo']
    if t == 'dividido':
        return refs_codigo(v['esquerda']) + refs_codigo(v['direita'])
    if t == 'vertical':
        return refs_codigo(v['cima']) + refs_codigo(v['baixo'])
    if t == 'codigo' and 'livre' not in v and v.get('linhas'):
        return [(int(v['celula']), v['linhas'][0], v['linhas'][1])]
    return []


def pico_db(arq):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(arq), '-map', '0:a', '-af', 'volumedetect', '-f', 'null', '-'],
                       capture_output=True, text=True)
    m = re.search(r'max_volume: (-?[\d.]+) dB', r.stderr)
    return float(m.group(1)) if m else 0.0


def normalizar_audio(mp4):
    """Capítulos com pico acima de -1 dB recebem loudnorm (o vídeo é copiado, sem recompressão)."""
    if pico_db(mp4) <= -1.0:
        return
    tmp = mp4.with_suffix('.tmp.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(mp4), '-c:v', 'copy', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11',
                    '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-ac', '2', '-movflags', '+faststart', str(tmp)], check=True)
    tmp.replace(mp4)


def main():
    linhas_tl = sorted((RAIZ / 'cache').glob('linha_cap*.json'))
    for arq in linhas_tl:
        normalizar_audio(RAIZ / 'capitulos' / (arq.stem.replace('linha_', '') + '.mp4'))
    capitulos = []
    for arq in linhas_tl:
        tl = json.loads(arq.read_text(encoding='utf-8'))
        mp4 = RAIZ / 'capitulos' / f"cap{tl['numero']:02d}.mp4"
        assert mp4.exists(), mp4
        capitulos.append((tl, mp4, duracao(mp4)))

    # 1) vídeo final por concatenação sem recompressão + marcadores de capítulo
    lista = RAIZ / 'cache' / 'lista_final.txt'
    lista.write_text(''.join(f"file '{m.as_posix()}'\n" for _, m, _ in capitulos), encoding='utf-8')
    meta = [';FFMETADATA1']
    t = 0.0
    for tl, _, d in capitulos:
        meta += ['[CHAPTER]', 'TIMEBASE=1/1000', f'START={int(t * 1000)}', f'END={int((t + d) * 1000)}',
                 f"title=Capítulo {tl['numero']} - {tl['titulo']}"]
        t += d
    arq_meta = RAIZ / 'cache' / 'capitulos.ffmeta'
    arq_meta.write_text('\n'.join(meta) + '\n', encoding='utf-8')
    final = RAIZ / 'Videoaula_Projeto_IESB.mp4'
    # Áudio a 48 kHz: com 44,1 kHz a trilha de capítulos do MP4 estoura a escala de tempo e os capítulos saem embaralhados.
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(lista), '-i', str(arq_meta),
                    '-map', '0:v', '-map', '0:a', '-map_metadata', '1', '-map_chapters', '1', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-ac', '2', '-movflags', '+faststart', str(final)], check=True)

    # 2) capitulos.txt, legendas.srt e roteiro completo, com tempos reais
    cap_txt, srt, roteiro, usos = [], [], ['# Roteiro completo da videoaula', ''], []
    t0, n_leg = 0.0, 0
    for tl, mp4, d in capitulos:
        cap_txt.append(f"{hms(t0)}  Capítulo {tl['numero']} — {tl['titulo']}")
        roteiro += [f"## Capítulo {tl['numero']} — {tl['titulo']}  (início {hms(t0)}, duração {hms(d)})", '']
        q = 0
        for i, b in enumerate(tl['blocos']):
            ini_b = t0 + q / FPS
            roteiro.append(f"**[{hms(ini_b)}] Bloco {i + 1}** · _{resumo_visual(b['visual'])}_  ")
            roteiro.append(' '.join(limpar(f['legenda']) for f in b['frases']))
            roteiro.append('')
            for ref in refs_codigo(b['visual']):
                usos.append(dict(cap=tl['numero'], tempo=ini_b, celula=ref[0], ini=ref[1], fim=ref[2]))
            for f in b['frases']:
                ini, fim = t0 + q / FPS, t0 + q / FPS + min(f['dur'] + 0.15, f['quadros'] / FPS)
                n_leg += 1
                srt += [str(n_leg), f'{hms(ini, True)} --> {hms(fim, True)}', limpar(f['legenda']).replace('`', ''), '']
                q += f['quadros']
        t0 += d
    (RAIZ / 'capitulos.txt').write_text('\n'.join(cap_txt) + f'\n{hms(t0)}  Fim\n', encoding='utf-8')
    (RAIZ / 'legendas.srt').write_text('\n'.join(srt), encoding='utf-8')
    (RAIZ / 'roteiro_completo.md').write_text('\n'.join(roteiro), encoding='utf-8')

    # 3) matriz de cobertura: cada função e cada célula de código × momentos do vídeo
    inv = json.loads((RAIZ / 'dados' / 'inventario.json').read_text(encoding='utf-8'))
    cod = json.loads((RAIZ / 'dados' / 'codigo.json').read_text(encoding='utf-8'))
    m = ['# Matriz de cobertura', '',
         'Gerada automaticamente: cada destaque de código no vídeo foi comparado com as linhas de cada função e célula.', '',
         '## Funções', '', '| função | célula · linhas | onde é explicada (capítulo · tempo) |', '|---|---|---|']
    sem = []
    for f in inv['funcoes']:
        hits = [u for u in usos if u['celula'] == f['celula'] and u['ini'] <= f['linha_fim'] and u['fim'] >= f['linha_inicio']]
        vistos, txt = set(), []
        for u in hits:
            k = (u['cap'], hms(u['tempo']))
            if k not in vistos:
                vistos.add(k)
                txt.append(f'cap. {u["cap"]} · {hms(u["tempo"])}')
        if not txt:
            sem.append(f['nome'])
        m.append(f"| `{f['nome']}` | {f['celula']} · {f['linha_inicio']}–{f['linha_fim']} | {', '.join(txt[:8]) + (' …' if len(txt) > 8 else '') or '**não destacada**'} |")
    m += ['', '## Células de código', '', '| célula | seção | linhas com código | linhas destacadas no vídeo | cobertura |', '|---|---|---|---|---|']
    for cel, dados in cod.items():
        uteis = [i + 1 for i, l in enumerate(dados['texto']) if l.strip() and not l.strip().startswith('#')]
        cobertas = {n for u in usos if u['celula'] == int(cel) for n in range(u['ini'], u['fim'] + 1)}
        c = [n for n in uteis if n in cobertas]
        pct = 100 * len(c) / len(uteis) if uteis else 100
        m.append(f"| {cel} | {dados['titulo']} | {len(uteis)} | {len(c)} | {pct:.0f}% |")
    m += ['', '## Bibliotecas', '', '| módulo | nome importado | célula |', '|---|---|---|']
    for imp in inv['importacoes']:
        m.append(f"| `{imp['modulo']}` | `{imp['nome']}` | {imp['celula']} |")
    m += ['', '## Funções sem destaque de código', '', ', '.join(f'`{s}`' for s in sem) if sem else 'Nenhuma: todas as funções aparecem no vídeo.']
    (RAIZ / 'matriz_de_cobertura.md').write_text('\n'.join(m) + '\n', encoding='utf-8')
    print(f'vídeo final: {final.name}, {hms(t0)}; {n_leg} legendas; funções sem destaque: {sem}')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
