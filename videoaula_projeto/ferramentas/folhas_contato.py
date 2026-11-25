"""Monta folhas de contato (um quadro final de cada cena) para inspeção visual. Saída: testes/contato_NN.jpg"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from renderizar import chave_bloco  # noqa: E402

COL, LIN, W, H = 3, 3, 640, 360
amostras = []
for arq in sorted((RAIZ / 'cache').glob('linha_cap*.json')):
    tl = json.loads(arq.read_text(encoding='utf-8'))
    cena_ant = None
    for i, b in enumerate(tl['blocos']):
        if b['visual']['cena'] == cena_ant:
            continue
        cena_ant = b['visual']['cena']
        pasta = RAIZ / 'cache' / 'quadros' / f"cap{tl['numero']:02d}" / f'{i:03d}_{chave_bloco(tl, i)}'
        quadro = sorted(pasta.glob('t*.jpg'))[-1]
        amostras.append((f"cap {tl['numero']} · bloco {i + 1}", quadro))
saida = RAIZ / 'testes'
saida.mkdir(exist_ok=True)
for n in range(0, len(amostras), COL * LIN):
    folha = Image.new('RGB', (COL * W, LIN * H), '#000')
    d = ImageDraw.Draw(folha)
    for k, (rot, q) in enumerate(amostras[n:n + COL * LIN]):
        x, y = (k % COL) * W, (k // COL) * H
        folha.paste(Image.open(q).resize((W, H)), (x, y))
        d.rectangle([x, y, x + 210, y + 22], fill='#000')
        d.text((x + 4, y + 4), rot, fill='#ff0')
    folha.save(saida / f'contato_{n // (COL * LIN):02d}.jpg', quality=88)
print(len(amostras), 'cenas em', (len(amostras) + COL * LIN - 1) // (COL * LIN), 'folhas')
