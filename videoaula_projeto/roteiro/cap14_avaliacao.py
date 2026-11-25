from base import *
from dados import avaliacao_colab, resumo_colab, ambiente_colab, brutos_colab

AV = avaliacao_colab()
RS = resumo_colab()['fase3']
GRUPOS = [('Nomes exatos', 0, 8), ('Vizinhos', 8, 12), ('Sem ferramenta', 12, 15), ('Cenários', 15, 23),
          ('Escrita informal', 23, 33), ('Esclarecimento', 33, 39)]


def certo(l):
    return l['argumentos_ok'] == 'True' and l['numeros_inventados'] in ('[]', '')


LIN_GR = [[g, f'{sum(certo(l) for l in AV[a:b])} de {b - a}'] for g, a, b in GRUPOS]
ERRADOS = [l for l in AV if not certo(l)]
BR = {b['pergunta']: b for b in brutos_colab()}


def bruto(p):
    return [r[:70].replace('\n', ' ') for r in BR[p]['respostas_do_qwen']]


CAPITULO = dict(numero=14, titulo='Avaliação real do agente', blocos=[
    bloco('Capítulo catorze: a avaliação. O enunciado pede pelo menos 15 pedidos de teste, com o resultado esperado, medindo em quantos o agente acerta, e uma análise das falhas. O projeto tem 39.',
          titulo('Avaliação real do agente', '39 pedidos, resultados da execução no Colab e na GPU local', 'Capítulo 14')),
    bloco('Cada caso é uma tupla com três valores: a pergunta, o que o agente deve fazer, e os argumentos esperados. O que fazer pode ser o nome da ferramenta, `None` ou esclarecer.',
          codigo(33, (1, 5))),
    bloco('A lista é organizada por grupos, com comentários: rotas com nomes exatos, vizinhos, perguntas sem ferramenta e os três cenários.',
          codigo(33, (6, 23), janela=(5, 24))),
    bloco('Depois vêm os testes difíceis: escrita informal, abreviações, erros de digitação, ordem invertida, e pedidos em que falta informação ou o local não existe. Nesses, o esperado é esclarecer.',
          codigo(33, (24, 51), janela=(24, 52))),
    bloco('Antes de chamar o Qwen, a célula confere os próprios casos: todo caso de ferramenta precisa executar sem erro. Isso evita testar o agente contra uma resposta esperada errada.',
          codigo(33, (55, 59), janela=(40, 60))),
    bloco('A função `o_que_o_agente_fez` traduz os detalhes devolvidos pelo agente para o mesmo formato do caso: esclarecer com o campo, o nome e os argumentos da ferramenta, ou nada.',
          codigo(35, (2, 11))),
    bloco('O laço mede o tempo de cada pedido com `perf_counter`, compara a escolha e os argumentos, e verifica números inventados. Um caso só é certo se tudo estiver certo.',
          codigo(35, (14, 30))),
    bloco('Cada caso imprime uma linha com certo ou ERRADO, a escolha esperada e a feita, os números inventados e o tempo. E o dicionário do caso entra na lista `AVALIACAO`.',
          codigo(35, (27, 37), janela=(12, 38))),
    bloco('A linha 22 tem um detalhe: `dict` com dois asteriscos junta o cenário padrão tranquilo com os argumentos esperados, porque o agente sempre preenche o cenário.',
          codigo(35, 22, notas=[(22, 'cenário padrão incluído')])),
    bloco('No fim, o pandas monta a tabela, calcula os totais e salva um CSV com a versão das regras no nome.',
          codigo(35, (39, 57), janela=(36, 58))),
    bloco('Resultado real, com o Qwen dois ponto cinco: 31 de 39 casos certos. Em 30 casos que pediam uma ferramenta, 24 tiveram ferramenta e argumentos certos. E 4 explicações tiveram números sinalizados.',
          tabela('Resultado da avaliação (regras v5, execução real)', ['métrica', 'valor'],
                 [['escolheu o que fazer certo', f"{RS['escolha_certa']} de {RS['casos']}"],
                  ['argumentos certos', f"{RS['argumentos_certos']} de {RS['casos']}"],
                  ['rotas ou vizinhos válidos', f"{RS['rotas_validas']} de {RS['total_rotas']}"],
                  ['explicações com número sinalizado', f"{RS['com_numero_inventado']} de {RS['total_rotas']}"]], fonte=30)),
    bloco('Por grupo, o ponto fraco é claro: escrita informal, com 3 de 10. Saudações e perguntas fora do mapa acertaram todas.',
          tabela('Acertos por grupo de casos', ['grupo', 'certos'], LIN_GR, estilos=['', '', 'ok', '', 'erro', ''], fonte=30)),
    bloco('Vamos ver as falhas de verdade, com o texto bruto que o Qwen escreveu. Em “cafe manai para easy smrt”, nas três tentativas, ele escreveu a mesma frase, sem chamar a ferramenta.',
          terminal('cafe manai para easy smrt · respostas brutas do Qwen', bruto('cafe manai para easy smrt') + ['', 'resposta final: Não consegui consultar o mapa em 3 passos.'],
                   estilos=['erro', 'erro', 'erro', '', 'dest'], fonte=23)),
    bloco('Repare que “caminha 203” não existe no mapa. Sem a proteção da versão 5, isso seria mostrado ao usuário como se fosse verdade. Com ela, o agente admite que não conseguiu.',
          terminal('cafe manai para easy smrt · respostas brutas do Qwen', bruto('cafe manai para easy smrt') + ['', 'resposta final: Não consegui consultar o mapa em 3 passos.'],
                   estilos=['erro', 'erro', 'erro', '', 'dest'], fonte=23)),
    bloco('Em “mesa um pra mesa quatro, ta lotado”, o Qwen entendeu outra coisa: que a mesa estava ocupada. Depois escreveu algo parecido com argumentos, mas fora do formato de ferramenta.',
          terminal('mesa um pra mesa quatro, ta lotado · respostas brutas', bruto('mesa um pra mesa quatro, ta lotado'), estilos=['erro', 'alerta', 'alerta'], fonte=23)),
    bloco('E em “O que há ao lado do Corredor Design?”, ele primeiro inventou salas 203, 204 e 205, e na segunda tentativa chamou a ferramenta de rota sem destino, quando o certo era listar vizinhos.',
          terminal('O que há ao lado do Corredor Design? · respostas brutas', bruto('O que há ao lado do Corredor Design?'), estilos=['erro', 'alerta'], fonte=23)),
    bloco('As quatro explicações sinalizadas arredondaram números: 74,2 segundos virou 74, 51,8 virou 51, 22,2 virou 22 e 17,8 virou 17. A verificação pegou todas e mostrou o resultado exato.',
          topicos('Números sinalizados (todos arredondamentos)', ['74,2 s → “74 segundos”', '51,8 s → “51 segundos”',
                                                                  '22,2 s → “22 segundos”', '17,8 s → “cerca de 17 segundos”'], mostrar=4)),
    bloco('A comparação entre versões mostra o efeito das correções. Na versão 4, eram 24 certos, e 15 pedidos com rotas inventadas. Na versão 5, 31 certos e nenhuma rota inventada chegou ao usuário.',
          tabela('Versões das regras (execuções reais)', ['versão', 'certos', 'rotas válidas', 'números sinalizados'],
                 [['v4', '24 de 39', '21 de 30', '6 de 30'], ['v5', '31 de 39', '24 de 30', '4 de 30']], estilos=['erro', 'ok'], fonte=30)),
    bloco('Agora o custo. O Qwen roda dentro da sessão, sem API paga e sem chave no código. Mas não é de graça: cada pedido consome tempo de processamento e memória.',
          tabela('Tempo por pedido (mesmo resultado nos dois)', ['ambiente', 'mediana', 'máximo', 'avaliação inteira'],
                 [['GPU RTX 4050 (local)', '3,8 s', '9,5 s', '≈ 3 min'], [f"Colab sem GPU ({ambiente_colab()['dispositivo'].upper()})", '135 s', '234 s', '88 min']],
                 estilos=['ok', 'erro'], fonte=28)),
    bloco('Na CPU, cada pedido levou cerca de 35 vezes mais. Por isso, na apresentação, é obrigatório escolher a GPU T4 no Colab. E pedidos com falha custam mais, porque o agente chama o Qwen até três vezes.',
          topicos('Limites para o relatório', ['O Qwen 1.5B falha em escrita informal e erros de digitação',
                                               'Pode arredondar números e reescrever o caminho com palavras',
                                               'Inferência local: sem custo por chamada, mas lenta sem GPU',
                                               'Testes controlados: 39 casos, não cobrem tudo o que um usuário pode escrever'], mostrar=4)),
])
