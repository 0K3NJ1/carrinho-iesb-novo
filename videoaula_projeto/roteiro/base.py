"""Funções curtas para escrever o roteiro: cada bloco = narração + visual."""


def bloco(fala, visual=None, anim=None):
    return dict(fala=fala, visual=visual, anim=anim)


def titulo(t, sub=None, rotulo=None):
    return dict(tipo='titulo', titulo=t, subtitulo=sub, rotulo=rotulo)


def topicos(titulo, itens, mostrar=None, ativo=None, fonte=None, realce=True):
    return dict(tipo='topicos', titulo=titulo, itens=itens, mostrar=mostrar, ativo=ativo, fonte=fonte, realce=realce)


def codigo(celula, linhas=None, janela=None, notas=None):
    """Mostra a célula do notebook com as linhas (a, b) destacadas (numeração da célula)."""
    if isinstance(linhas, int):
        linhas = (linhas, linhas)
    return dict(tipo='codigo', celula=celula, linhas=list(linhas) if linhas else None,
                janela=list(janela) if janela else None,
                notas=[dict(linha=l, texto=t) for l, t in (notas or [])])


def livre(texto, titulo='exemplo.py', linhas=None, notas=None):
    """Código de exemplo que NÃO é do projeto (o painel avisa isso)."""
    if isinstance(linhas, int):
        linhas = (linhas, linhas)
    return dict(tipo='codigo', livre_fonte=texto, titulo=titulo, linhas=list(linhas) if linhas else None,
                notas=[dict(linha=l, texto=t) for l, t in (notas or [])])


def tabela(titulo, colunas, linhas, destaque=None, estilos=None, rodape=None, fonte=None):
    return dict(tipo='tabela', titulo=titulo, colunas=colunas, linhas=linhas, destaque=destaque or [],
                estilos=estilos, rodape=rodape, fonte=fonte)


def cartoes(titulo, itens):
    return dict(tipo='cartoes', titulo=titulo, itens=[list(i) for i in itens])


def formula(partes, linhas=None, titulo=None, realce=None):
    partes = [(p,) if isinstance(p, str) else p for p in partes]     # ('=') é só uma string, não uma tupla
    return dict(tipo='formula', partes=[dict(t=p[0], cor=p[1] if len(p) > 1 else None) for p in partes],
                linhas=linhas or [], titulo=titulo, realce=realce)


def transf(titulo, etapas, mostrar=None, nota=None):
    return dict(tipo='transformacao', titulo=titulo, mostrar=mostrar, nota=nota,
                etapas=[dict(op=e[3:]) if e.startswith('-> ') else dict(valor=e) for e in etapas])


def terminal(titulo, texto, destaque=None, estilos=None, fonte=None):
    if isinstance(texto, str):
        texto = texto.split('\n')
    return dict(tipo='terminal', titulo=titulo, texto=texto, destaque=destaque or [], estilos=estilos, fonte=fonte)


def pergunta(numero, pergunta, resposta, mostrar=None):
    return dict(tipo='pergunta', numero=numero, pergunta=pergunta, resposta=resposta, mostrar=mostrar)


def imagem(src, titulo):
    return dict(tipo='imagem', src=src, titulo=titulo)


def fluxo(titulo, nos, setas, ativo=None):
    return dict(tipo='fluxo', titulo=titulo, nos=nos, setas=setas, ativo=ativo or [])


def no(id, texto, x, y, w=260, h=90, cor=None):
    return dict(id=id, texto=texto, x=x, y=y, w=w, h=h, cor=cor)


def grafo(**kw):
    kw['tipo'] = 'grafo'
    return kw


def dividido(esq, dir, proporcao=.56):
    return dict(tipo='dividido', esquerda=esq, direita=dir, proporcao=proporcao)


def vertical(cima, baixo, proporcao=.5):
    return dict(tipo='vertical', cima=cima, baixo=baixo, proporcao=proporcao)


# Câmeras do grafo (x, y, largura, altura no viewBox 1600 x 900)
CAMPUS = [-60, 10, 1720, 850]          # campus inteiro, tela cheia
PATIO_LARGO = [-40, 10, 960, 425]      # pátio, tela cheia
PATIO_LADO = [10, 15, 620, 510]        # pátio + Eixo Norte, painel dividido (lado do grafo)
EIXO = [-40, 330, 1640, 520]           # eixo principal, cinema e corredor I/J
