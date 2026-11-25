from base import *

ROTA = ['Biblioteca', 'Eixo - Norte', 'Pátio/Direito', 'Pátio - D', 'Mesa 3']
CAM = [-60, 10, 1080, 640]

CHAMADAS = [
    no('ag', '`agente(pergunta)`', 40, 60, 330, 80),
    no('cv', '`conversar` · Qwen\n<tool_call> rota_tempo_previsto', 450, 40, 520, 110, cor='proc'),
    no('lp', '`ler_pedido_de_ferramenta`\n`extrair_json`', 1060, 40, 420, 110),
    no('pp', '`preparar_pedido`\nresolver_local · local_na_pergunta', 1060, 210, 520, 110, cor='alerta'),
    no('ex', '`executar`\n`rota_tempo_previsto(**args)`', 450, 210, 520, 110),
    no('pg', '`prever_grafo_tempo`\nMODELO_TEMPO.predict', 40, 210, 360, 110),
    no('bu', '`buscar` (A*)\ncusto em segundos', 40, 390, 360, 110, cor='caminho'),
    no('ob', 'resultado → mensagem `tool`\nQwen explica', 450, 390, 520, 110, cor='proc'),
    no('nf', '`numeros_fora_da_ferramenta`\nverifica números', 1060, 390, 520, 110),
    no('rs', 'resposta final', 450, 560, 520, 90, cor='caminho'),
]
SETAS = [['ag', 'cv'], ['cv', 'lp'], ['lp', 'pp'], ['pp', 'ex'], ['ex', 'pg'], ['pg', 'bu'], ['bu', 'ob'], ['ob', 'nf'], ['nf', 'rs']]


def passo(ativos, setas_ativas):
    return fluxo('Uma pergunta atravessando o código', CHAMADAS,
                 [s + ([None, True] if [s[0], s[1]] in setas_ativas else []) for s in SETAS], ativo=ativos)


CAPITULO = dict(numero=15, titulo='Simulação completa: do “Executar tudo” à resposta', blocos=[
    bloco('Capítulo quinze. Vamos juntar tudo e acompanhar o programa inteiro, do “Executar tudo” até a resposta de uma pergunta. Todos os valores são de execuções reais.',
          titulo('Simulação completa', 'Inicialização, construção do grafo, treino, carregamento do Qwen e uma pergunta de ponta a ponta', 'Capítulo 15')),
    bloco('Ao clicar em executar tudo, a seção 1 cria as constantes: origem Entrada Principal, destino Mesa 4 e velocidade base 15.',
          cartoes('Memória da sessão', [('ORIGEM', '"Entrada Principal"'), ('DESTINO', '"Mesa 4"'), ('VELOCIDADE_BASE_KMH', '15.0')])),
    bloco('A seção 2 constrói o grafo: `LOCAIS`, `LIGACOES` e `VIZINHOS`, e imprime 90 nós e 90 ligações.',
          cartoes('Memória da sessão', [('ORIGEM', '"Entrada Principal"'), ('DESTINO', '"Mesa 4"'), ('VELOCIDADE_BASE_KMH', '15.0'),
                                        ('LOCAIS', 'lista com 90 nomes', 'dest'), ('LIGACOES', 'lista com 90 tuplas', 'dest'), ('VIZINHOS', 'dicionário com 90 chaves', 'dest')])),
    bloco('A seção 3 define `buscar` e calcula `DISTANCIA_ENTRADA` para os 90 locais, em cerca de 3 milissegundos. As seções 4 e 5 criam as ferramentas e rodam o experimento.',
          cartoes('Memória da sessão', [('ORIGEM', '"Entrada Principal"'), ('DESTINO', '"Mesa 4"'), ('VELOCIDADE_BASE_KMH', '15.0'),
                                        ('LOCAIS', 'lista com 90 nomes'), ('LIGACOES', 'lista com 90 tuplas'), ('VIZINHOS', 'dicionário com 90 chaves'),
                                        ('DISTANCIA_ENTRADA', '{"Mesa 4": 89.5, ...}', 'dest'), ('RESULTADOS', '6 linhas do experimento', 'dest')])),
    bloco('A seção 5.3 gera 2160 linhas sintéticas, valida os dois modelos, escolhe a regressão linear e treina `MODELO_TEMPO`. No fim, cria a lista `FERRAMENTAS`.',
          cartoes('Memória da sessão', [('VIZINHOS', 'dicionário com 90 chaves'), ('DISTANCIA_ENTRADA', '{"Mesa 4": 89.5, ...}'),
                                        ('DADOS_TEMPO', 'DataFrame 2160 × 13', 'dest'), ('MELHOR_MODELO', '"regressao_linear"', 'dest'),
                                        ('MODELO_TEMPO', 'Pipeline treinado', 'dest'), ('FERRAMENTAS', '[rota_tempo_previsto, listar_vizinhos]', 'dest')])),
    bloco('A seção 6 detecta a GPU e carrega o Qwen. A seção 7 define as regras e o agente. A partir daqui, o notebook pode responder perguntas.',
          cartoes('Memória da sessão', [('MODELO_TEMPO', 'Pipeline treinado'), ('FERRAMENTAS', '[rota_tempo_previsto, listar_vizinhos]'),
                                        ('dispositivo', '"cuda"', 'dest'), ('qwen', 'Qwen2.5-1.5B-Instruct', 'dest'),
                                        ('REGRAS', 'prompt v5', 'dest'), ('agente', 'função', 'dest')])),
    bloco('Agora a pergunta da célula 8.2: “Como vou da Biblioteca até a Mesa 3?”. A função `agente` monta as mensagens e chama `conversar`.',
          passo(['ag', 'cv'], [['ag', 'cv']])),
    bloco('O Qwen responde com um pedido de ferramenta: `rota_tempo_previsto`, origem Biblioteca, destino Mesa 3. `ler_pedido_de_ferramenta` e `extrair_json` transformam o texto num dicionário.',
          passo(['cv', 'lp'], [['cv', 'lp']])),
    bloco('`preparar_pedido` confere: Biblioteca e Mesa 3 existem e aparecem na pergunta, não há parâmetro extra, e o cenário vazio vira tranquilo. Status ok.',
          passo(['pp'], [['lp', 'pp']])),
    bloco('`executar` chama `rota_tempo_previsto`, que chama `prever_grafo_tempo`: o modelo da Fase 2 prevê o tempo dos 90 trechos no cenário tranquilo.',
          passo(['ex', 'pg'], [['pp', 'ex'], ['ex', 'pg']])),
    bloco('Com o grafo de segundos e a referência recalculada, a mesma `buscar` da Fase 1 roda o A estrela.',
          passo(['bu'], [['pg', 'bu']])),
    bloco('O caminho encontrado: Biblioteca, Eixo Norte, Pátio Direito, Pátio D, Mesa 3. São 113,5 metros e 43 segundos previstos.',
          grafo(camera=CAM, rotulos='todos', caminho=ROTA, estados={x: 'caminho' for x in ROTA}, carrinho=dict(caminho=ROTA), zoomTexto=1.1), 4),
    bloco('O texto da ferramenta volta ao Qwen como mensagem tool. Ele escreve a explicação em português. Depois, `numeros_fora_da_ferramenta` compara os números: 113.5 e 43 estão no resultado. Nada sinalizado.',
          passo(['ob', 'nf'], [['bu', 'ob'], ['ob', 'nf']])),
    bloco('E a resposta final é impressa. Em resumo: o LLM entendeu e explicou, o modelo de custo deu os tempos, e a busca A estrela encontrou o caminho. As três fases numa só pergunta.',
          passo(['rs'], [['nf', 'rs']])),
    bloco('Na GPU, essa pergunta inteira levou alguns segundos. O mapa e o treino rodam uma vez só; o Qwen é a parte cara de cada pedido.',
          topicos('Onde o tempo vai', ['Grafo, tabela da heurística e treino: **uma vez**, em segundos',
                                       'Cada pergunta: 1 a 3 gerações do Qwen + uma busca A*',
                                       'A busca leva centésimos de milissegundo',
                                       'O Qwen leva segundos na GPU e minutos na CPU'], mostrar=4)),
])
