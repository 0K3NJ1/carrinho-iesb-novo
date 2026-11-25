import json
from base import *
from dados import RAIZ

EX = json.loads((RAIZ / 'dados' / 'exemplos_agente.json').read_text(encoding='utf-8'))
PADR = ['"Sala B04"', '-> .lower()', '"sala b04"', '-> tira pontuação', '"sala b04"', '-> separa b|4', '"sala b 4"', '-> TROCAS / int', '"b 4"']

RESOLVER = [
    no('e', 'texto do pedido\n`resolver_local(texto)`', 40, 330, 360, 110),
    no('n', 'está em `NOMES`?\nnome ou apelido', 520, 90, 380, 100, cor='caminho'),
    no('g', 'está em `GENERICOS`?\n“banheiro”, “lanchonete”', 520, 260, 380, 100, cor='alerta'),
    no('d', 'tem número ou vazio?\nnunca “corrige” sala', 520, 430, 380, 100, cor='erro'),
    no('p', '`get_close_matches`\nerro de digitação', 520, 600, 380, 100, cor='proc'),
    no('r1', 'devolve o local\n(local, [])', 1040, 90, 340, 100), no('r2', 'pergunta ao usuário\n(None, opções)', 1040, 260, 340, 100),
    no('r3', 'pergunta ao usuário\n(None, [])', 1040, 430, 340, 100), no('r4', '1 parecido: o local\nsenão: pergunta', 1040, 600, 340, 100),
]
SETAS_R = [['e', 'n'], ['n', 'g', 'não'], ['g', 'd', 'não'], ['d', 'p', 'não'], ['n', 'r1', 'sim'], ['g', 'r2', 'sim'], ['d', 'r3', 'sim'], ['p', 'r4']]


def ex_pedido(i):
    r = EX['preparar_pedido'][i]
    linhas = ['pergunta: ' + r['pergunta'], 'pedido do Qwen: ' + json.dumps(r['pedido']['arguments'], ensure_ascii=False), '']
    res = r['resultado']
    linhas.append('status: ' + res['status'])
    if 'pedido' in res:
        linhas.append('argumentos limpos: ' + json.dumps(res['pedido']['arguments'], ensure_ascii=False))
    if 'mensagem' in res:
        msg = res['mensagem']
        linhas.append('mensagem: ' + (msg[:95] + '...' if len(msg) > 98 else msg))
    estilo = {'ok': 'dest', 'erro': 'erro', 'esclarecimento': 'alerta'}[res['status']]
    return terminal('preparar_pedido · exemplo real', linhas, estilos=['', '', '', estilo, estilo], fonte=22)


CAPITULO = dict(numero=12, titulo='Fase 3: o código confere o pedido do modelo', blocos=[
    bloco('Capítulo doze. O Qwen escreve um pedido de ferramenta. Mas um modelo pequeno erra: troca nomes, inventa locais, usa cenários errados. Por isso, antes de executar, o código confere tudo.',
          titulo('O código confere o pedido', '`padronizar`, `resolver_local`, `preparar_pedido` e `executar`', 'Capítulo 12')),
    bloco('A seção 7 importa `json`, `re`, `unicodedata` e `get_close_matches`, todos nativos do Python. Depois cria a tabela `TROCAS`, um dicionário de palavras a trocar ou ignorar.',
          codigo(24, (2, 9), janela=(1, 26), notas=[(8, "'' = palavra ignorada")])),
    bloco('A primeira peça é `padronizar`. Ela transforma qualquer texto numa forma simples e comparável, para que “Sala B04”, “b4” e “B-04” virem a mesma coisa.',
          codigo(24, (12, 25), janela=(1, 26))),
    bloco('Passo um: `lower()` deixa tudo minúsculo. `unicodedata.normalize` com a forma NFD separa cada letra do seu acento, e a linha 15 descarta os acentos, que têm a categoria Mn.',
          codigo(24, (14, 15), janela=(1, 26), notas=[(15, 'remove acentos (categoria Mn)')])),
    bloco('Passo dois, com expressões regulares: `re.sub` troca tudo o que não é letra ou número por espaço. E a linha 17 coloca um espaço entre letra e número: b4 vira b espaço 4.',
          codigo(24, (16, 17), janela=(1, 26), notas=[(17, '`b4` → `b 4`')])),
    bloco('Passo três: para cada palavra, a tabela `TROCAS` substitui ou apaga. Banheiro vira wc, fem vira feminino, e palavras como sala, bloco, do e da somem. Números perdem zeros à esquerda com `int`.',
          codigo(24, (18, 25), janela=(1, 26), notas=[(20, 'troca pela tabela'), (22, '`04` → `4`')])),
    bloco('Veja a transformação real de “Sala B04”, passo a passo, até chegar em “b 4”.',
          transf('`padronizar("Sala B04")`', PADR, mostrar=3, nota='saída real: `"b 4"`')),
    bloco('A sala some, porque está na tabela de palavras ignoradas, e o zero de 04 também. É por isso que “B-04” e “Sala B04” chegam ao mesmo nome padronizado.',
          transf('`padronizar("Sala B04")`', PADR, nota='saída real: `"b 4"` · também `padronizar("B-04")` → `"b 4"`')),
    bloco('Mais dois exemplos reais: “banheiro fem do Design” vira “wc feminino design”, igual ao nome padronizado de “WC Feminino Design”. E “Pátio/Direito” vira “patio direito”.',
          tabela('padronizar: exemplos reais', ['entrada', 'saída'], [[f'`{k}`', f'`{v}`'] for k, v in EX['padronizar'].items()], fonte=26)),
    bloco('Com isso, o código monta o dicionário `NOMES`: a chave é o nome padronizado, e o valor é o nome oficial do mapa. O `assert` garante que dois locais nunca fiquem com o mesmo nome padronizado.',
          codigo(24, (39, 45), janela=(26, 50), notas=[(42, 'sem colisão de nomes')])),
    bloco('Os apelidos também entram em `NOMES`: biblio leva à Biblioteca, mesa um leva à Mesa 1. Já os genéricos, como banheiro e lanchonete, ficam em outro dicionário, porque apontam para vários locais.',
          codigo(24, (28, 37), janela=(26, 50))),
    bloco('E o dicionário `CENARIOS` lista, para cada cenário, as palavras que o usuário pode usar: lotado e cheio indicam movimentado; calmo e normal indicam tranquilo.',
          codigo(24, (47, 49), janela=(26, 50))),
    bloco('Agora `resolver_local`, que decide qual local o texto significa. Ela devolve uma tupla: o local, ou `None`, e uma lista de opções.',
          fluxo('resolver_local: a ordem das perguntas', RESOLVER, SETAS_R)),
    bloco('Primeiro, procura o texto padronizado em `NOMES`. Se achar, é um nome do mapa ou um apelido, e devolve o local.',
          fluxo('resolver_local: a ordem das perguntas', RESOLVER, SETAS_R, ativo=['n', 'r1'])),
    bloco('Se for genérico, devolve `None` com a lista de opções, para o programa perguntar qual. Para banheiro, são 13 opções; para lanchonete, Easy Smart e Café Mania.',
          fluxo('resolver_local: a ordem das perguntas', RESOLVER, SETAS_R, ativo=['g', 'r2'])),
    bloco('Se o texto tiver número ou estiver vazio, devolve `None` sem opções. Uma decisão de segurança: “B-07” não existe, e o código nunca “corrige” para uma sala parecida, como B-01.',
          fluxo('resolver_local: a ordem das perguntas', RESOLVER, SETAS_R, ativo=['d', 'r3'])),
    bloco('Só então tenta erro de digitação com `get_close_matches`, que compara a semelhança entre textos. O corte de 0,85 exige muita semelhança, e o resultado só é aceito se houver um único candidato.',
          fluxo('resolver_local: a ordem das perguntas', RESOLVER, SETAS_R, ativo=['p', 'r4'])),
    bloco('No código, são poucas linhas, na mesma ordem do diagrama.',
          codigo(24, (52, 64), janela=(47, 70))),
    bloco('Exemplos reais: “b4” e “biblio” são resolvidos direto; “bibliotca” e “cafe manai” por semelhança; banheiro e lanchonete pedem escolha; sala 02, B-07 e auditório pedem um nome do mapa.',
          tabela('resolver_local: exemplos reais', ['texto', 'local', 'opções'],
                 [[f'`{k}`' if k else '(vazio)', v[0] or '`None`', (str(len(v[1])) + ' opções') if v[1] else '—'] for k, v in EX['resolver_local'].items()],
                 fonte=22, estilos=['ok', 'ok', 'ok', 'ok', 'ok', 'alerta', 'alerta', 'erro', 'erro', 'erro', 'erro'])),
    bloco('`resolver_cenario` faz o mesmo com os cenários. Lotado vira movimentado, e até grafias erradas como “tranqulho” e “tranq” viram tranquilo, por causa do corte menor, de 0,7.',
          dividido(codigo(24, (67, 73), janela=(47, 74)),
                   tabela('resolver_cenario (real)', ['texto', 'cenário'], [[f'`{k}`', v or '`None`'] for k, v in EX['resolver_cenario'].items()], fonte=24), .6)),
    bloco('Duas funções conferem se o modelo não inventou nada. `aparece_na_pergunta` testa se alguma das palavras aparece no texto padronizado da pergunta.',
          codigo(24, (76, 78), janela=(74, 98))),
    bloco('E `local_na_pergunta` percorre todos os trechos de 1 a 4 palavras da pergunta e resolve cada um. Se algum trecho leva ao mesmo local que o modelo pediu, o local veio mesmo do usuário.',
          codigo(24, (81, 90), janela=(74, 98), notas=[(85, 'trechos de 1 a 4 palavras')])),
    bloco('Exemplo real: na pergunta “cafe manai para easy smrt”, o trecho “cafe manai” resolve para Café Mania, então o pedido é aceito. Já Mesa 3 não aparece em “da biblioteca para o banheiro”.',
          tabela('local_na_pergunta (real)', ['teste', 'resultado'], [[k, str(v)] for k, v in EX['local_na_pergunta'].items()],
                 estilos=['ok', 'erro'], fonte=26)),
    bloco('`pergunta_ao_usuario` monta o texto de esclarecimento. Se houver opções, lista as opções; senão, pede um nome do mapa com o exemplo B-04. A f-string coloca o nome do campo na pergunta.',
          codigo(24, (93, 97), janela=(80, 101))),
    bloco('`CAMPOS` diz quais argumentos de local cada ferramenta tem: origem e destino para a rota, e local para os vizinhos.',
          codigo(24, 100, janela=(80, 101))),
    bloco('Tudo isso é reunido em `preparar_pedido`. Ela devolve um dicionário com um status: ok, se pode executar; erro, que volta para o modelo corrigir; ou esclarecimento, que vira uma pergunta ao usuário.',
          codigo(24, (103, 105), janela=(99, 131))),
    bloco('Primeiro, confere se o pedido é um dicionário com uma ferramenta conhecida. `pedido.get("name")` busca a chave sem dar erro se ela não existir.',
          codigo(24, (106, 108), janela=(99, 131))),
    bloco('Depois, parâmetros extras: a diferença entre conjuntos com o sinal de menos mostra o que sobrou. Se o modelo mandar velocidade, o pedido é recusado, porque a base é fixa.',
          codigo(24, (109, 110), janela=(99, 131), notas=[(109, 'diferença de conjuntos')])),
    bloco('Para cada campo de local, resolve o texto. Se não houver local, devolve esclarecimento. Se houver, mas não estiver na pergunta, devolve erro: o modelo inventou.',
          codigo(24, (111, 120), janela=(99, 131))),
    bloco('Para a rota, resolve o cenário. Se for diferente de tranquilo e não aparecer na pergunta, devolve erro com uma dica do cenário que o usuário citou.',
          codigo(24, (121, 130), janela=(99, 131))),
    bloco('Exemplos reais. “biblio para b4”: o pedido vira Biblioteca até B-04, cenário tranquilo, status ok.',
          ex_pedido(0)),
    bloco('“da biblioteca para o banheiro”: status esclarecimento, com a pergunta “Qual é o local de destino?” e as 13 opções de banheiro.',
          ex_pedido(1)),
    bloco('Um pedido com velocidade 10 é recusado por parâmetro extra.',
          ex_pedido(3)),
    bloco('E este caso aconteceu de verdade no teste: o usuário pediu cadeiras no pátio, e o Qwen mandou movimentado. O código recusa e devolve a dica: use cadeiras no pátio.',
          ex_pedido(4)),
    bloco('Por fim, `executar` chama `preparar_pedido` e, se estiver tudo certo, chama a função Python da ferramenta, desempacotando os argumentos com dois asteriscos.',
          codigo(24, (133, 141), janela=(116, 142), notas=[(140, '`**argumentos`: vira origem=..., destino=...')])),
    bloco('Dois asteriscos transformam um dicionário em argumentos nomeados: origem igual a Biblioteca, destino igual a B-04, cenário igual a tranquilo. No próximo capítulo, o ciclo completo do agente.',
          codigo(24, 140, janela=(116, 142))),
])
