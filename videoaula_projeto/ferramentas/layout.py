"""Posições DIDÁTICAS dos 90 nós para desenhar o grafo no vídeo.

Atenção: o projeto NÃO tem coordenadas. Estas posições servem só para desenhar,
imitando a disposição da planta; a busca usa apenas LIGACOES (metros estimados).
Uso: python ferramentas/layout.py  (lê dados/tracos.json, grava dados/layout.json)
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def posicoes():
    p = {}
    # Eixo principal, da esquerda para a direita (viewBox 1600 x 900)
    eixo_y = 470
    for nome, x in [('Entrada Principal', 60), ('Eixo - Norte', 330), ('Eixo - Design', 760),
                    ('Eixo - Bloco C', 1040), ('Eixo - Bloco B', 1320), ('Eixo - Fundo', 1520)]:
        p[nome] = (x, eixo_y)
    # Pátio (ciclo A-B-Direito-D) acima do Eixo - Norte
    p.update({'Pátio - A': (200, 140), 'Pátio - B': (420, 140), 'Pátio/Direito': (420, 330), 'Pátio - D': (200, 330),
              'Mesa 1': (130, 90), 'Mesa 2': (420, 60), 'Mesa 3': (120, 380), 'Mesa 4': (470, 380),
              'Easy Smart': (530, 95), 'Café Mania': (530, 175),
              'Sala dos Professores': (535, 265), 'WC Acessível Pátio': (90, 230), 'WC Feminino Pátio': (310, 235)})
    # Cinema e Biblioteca abaixo do Eixo - Norte
    p.update({'Cinema': (250, 590), 'WC Cinema': (140, 670), 'Anexo Creche': (320, 690), 'Biblioteca': (80, 580)})
    # Corredores verticais acima do eixo: Design, Bloco C, Bloco B
    for prefixo, corredor, bloco, banheiro, x in [('D', 'Corredor Design', 'Design', 'Design', 760),
                                                  ('C', 'Corredor Bloco C', 'Bloco C', 'C', 1040),
                                                  ('B', 'Corredor Bloco B', 'Bloco B', 'B', 1320)]:
        p[corredor] = (x, 390)
        p[bloco] = (x - 105, 415)
        p['WC Masculino ' + banheiro] = (x + 90, 395)
        p['WC Feminino ' + banheiro] = (x + 90, 440)
        for i, (a, b) in enumerate([('03', '06'), ('02', '05'), ('01', '04')]):
            y = 300 - i * 95
            p[f'{corredor} - {a}/{b}'] = (x, y)
            p[f'{prefixo}-{a}'] = (x - 80, y)
            p[f'{prefixo}-{b}'] = (x + 80, y)
    # Acesso lateral e corredor I/J abaixo do Eixo - Bloco C
    p['Acesso Lateral I/J'] = (1040, 560)
    for nome, pos, destinos in [('Corredor I/J - I-01/04', -35, ['I-01', 'I-04']),
                                ('Corredor I/J - I-02/05', -25, ['I-02', 'I-05']),
                                ('Corredor I/J - I-03/06', -15, ['I-03', 'I-06']),
                                ('Corredor I/J - WC I', -5, ['WC Masculino I', 'WC Feminino I']),
                                ('Corredor I/J', 0, []),
                                ('Corredor I/J - J-01/04', 10, ['J-01', 'J-04']),
                                ('Corredor I/J - J-02/05', 20, ['J-02', 'J-05']),
                                ('Corredor I/J - J-03/06', 30, ['J-03', 'J-06']),
                                ('Corredor I/J - WC J', 35, ['WC Masculino J', 'WC Feminino J'])]:
        x = 1040 + pos * 14
        p[nome] = (x, 680)
        if destinos:
            p[destinos[0]] = (x, 610)
            p[destinos[1]] = (x, 760)
    p['Bloco I'] = (1000, 820)
    p['Bloco J'] = (1085, 820)
    return p


def rotulo_curto(nome):
    trocas = {'Entrada Principal': 'Entrada', 'Corredor Design': 'Corr. Design', 'Corredor Bloco C': 'Corr. C',
              'Corredor Bloco B': 'Corr. B', 'Sala dos Professores': 'Sala Prof.', 'WC Acessível Pátio': 'WC Acess.',
              'WC Feminino Pátio': 'WC Fem.', 'Acesso Lateral I/J': 'Acesso I/J', 'Pátio/Direito': 'Pátio/Direito',
              'Corredor I/J': 'Corr. I/J'}
    if nome in trocas:
        return trocas[nome]
    nome = nome.replace('Corredor I/J - ', '').replace('Corredor Design - ', '').replace('Corredor Bloco C - ', '')
    nome = nome.replace('Corredor Bloco B - ', '').replace('WC Masculino ', 'WC M ').replace('WC Feminino ', 'WC F ')
    return nome.replace('Eixo - ', 'Eixo ')


def main():
    tracos = json.loads((RAIZ / 'dados' / 'tracos.json').read_text(encoding='utf-8'))
    p = posicoes()
    faltando = [l for l in tracos['locais'] if l not in p]
    sobrando = [l for l in p if l not in tracos['locais']]
    assert not faltando and not sobrando, (faltando, sobrando)
    def lado(nome):
        if nome.startswith('WC ') and nome.split()[-1] in ('Design', 'C', 'B'):
            return 'dir'
        if nome in ('Design', 'Bloco C', 'Bloco B'):
            return 'esq'
        return 'cima'
    saida = {l: dict(x=p[l][0], y=p[l][1], rotulo=rotulo_curto(l), lado=lado(l)) for l in tracos['locais']}
    (RAIZ / 'dados' / 'layout.json').write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding='utf-8')
    print(len(saida), 'posições gravadas')


if __name__ == '__main__':
    main()
