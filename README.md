# Carrinho IESB — Marcos 1 e 2 no mesmo notebook

Use **[carrinho_iesb_unificado.ipynb](carrinho_iesb_unificado.ipynb)**. Ele reúne o grafo, o A*, o treinamento com dados sintéticos e o agente Qwen. A base é fixa em 15 km/h e o custo do agente é o tempo previsto em segundos, incluindo atrasos. A distância da rota escolhida é informada em metros.

**Versão atual: v3.** O Qwen interpreta o pedido; o Python normaliza e valida os nomes, pede esclarecimento quando necessário e apresenta diretamente o retorno da ferramenta. A rota não é reescrita por uma segunda geração do modelo. Veja [INTERPRETACAO_DO_AGENTE.md](INTERPRETACAO_DO_AGENTE.md) para exemplos, limites e testes. A v3 ainda precisa de execução real no Colab.

**Para testar:** [abra o notebook do repositório no Colab](https://colab.research.google.com/github/0K3NJ1/carrinho-iesb-novo/blob/main/carrinho_iesb_unificado.ipynb), ou faça upload do arquivo local acima. Confira que a seção 9 informa **v3 — 39 casos** antes de executar.

**Situação em 23/11/2026:** estimativa de **70% concluído e 30% restante**, incluindo validação, relatórios e preparação da apresentação. O [O_QUE_FALTA.md](O_QUE_FALTA.md) reúne o critério da estimativa, o relatório de situação e os próximos passos em ordem. Não é previsão de nota nem prontidão para operação física.

## Uso

1. Na primeira célula de código, escolha apenas `ORIGEM` e `DESTINO`. `VELOCIDADE_BASE_KMH = 15.0` é a hipótese fixa da simulação, não uma entrada da consulta.
2. Execute de cima para baixo. A seção 5 mostra a referência ideal por distância, sem atrasos; a seção 5.3 treina os modelos e mostra a rota por tempo previsto, sem carregar o LLM.
3. Para executar o agente Qwen, continue a partir da seção 6; ela instala transformers e baixa o modelo público. No Colab, selecione GPU T4 se disponível.
4. Depois de mudar as variáveis, execute novamente as células seguintes, pois as funções usam essa configuração como padrão.
5. A seção 8.1 oferece a interface opcional `conversa_interativa()`. Chame-a manualmente depois de carregar o Qwen; ela não inicia sozinha. Quando pedir esclarecimento, responda somente o nome que faltou. Use `cancelar` para limpar o pedido pendente ou `sair` para encerrar.

As 90 ligações têm estimativas explícitas baseadas nas dimensões gerais da planta e em hipóteses declaradas. Veja [MAPA_DO_GRAFO.md](MAPA_DO_GRAFO.md). A base dos dados sintéticos usa `distância_m * 3.6 / 15`, acrescida de penalidades por fluxo, piso, porta e obstáculo, e ruído. Não são tempos observados no campus. Não se somam metros com segundos no custo.

Exemplo no cenário sintético de cadeiras: Mesa 1 → A → D → Pátio/Direito → Mesa 4 tem **46 m e 23,7 s previstos**, contra **42 m e 35,7 s previstos** pelo lado A–B. A rota mais curta pode ter mais atraso.

## Situação da entrega

A seção 5.3 implementa a Fase 2 com dados sintéticos autorizados pelo grupo: 2.160 observações, regressão linear versus árvore de decisão, validação cruzada por trecho e teste reservado. Os CSVs e métricas atuais são salvos em `resultados_fase2_15kmh/`. `rota_tempo_previsto(origem, destino, cenario)` é a única ferramenta de rota do Qwen e usa o modelo escolhido e o mesmo A* com custos em segundos. Cenários aceitos: `tranquilo` (padrão), `movimentado` e `cadeiras_no_patio` (atraso hipotético no trecho A–B). `listar_vizinhos` continua disponível para consultar ligações diretas.

Exemplo direto: `rota_tempo_previsto("Entrada Principal", "Mesa 4")`. No chat: “Como vou da Entrada Principal até a Mesa 4?”. Não é necessário informar velocidade ou cenário. A referência ideal do Marco 1 permanece fora das ferramentas do Qwen. O programa não detecta cadeiras nem garante que a largura esteja livre.

O código atual foi unificado, mas os requisitos acadêmicos ainda não estão completos: veja [O_QUE_FALTA.md](O_QUE_FALTA.md). O grafo tem 90 nós e um ciclo no pátio, com passagens condicionadas à disposição dos móveis. A heurística agora usa a diferença entre as distâncias dos dois locais até a Entrada Principal; a justificativa de admissibilidade está na seção 3.

Busca e aprendizado a 15 km/h foram verificados em 8.100 pares em metros e 24.300 pares em segundos contra Floyd-Warshall, com geração reproduzível, heurística e separação por trecho. A v3 mantém esse mapa e esses custos e passou pelos testes controlados das 39 referências, apresentação direta, normalização, esclarecimento e recuperação de formato. Ainda não há taxa de compreensão do Qwen na v3. Na execução real anterior (v2), ferramenta/argumentos foram corretos em 23/23, mas restaram erros na redação final: veja [AVALIACAO_COLAB_15KMH.md](AVALIACAO_COLAB_15KMH.md). Os originais estão preservados em `evidencias/`; a primeira avaliação está em [AVALIACAO_COLAB.md](AVALIACAO_COLAB.md).

A seção 9 define a bateria `v3_interpretacao_resposta_direta`, com os 23 pedidos da v2 e 16 novos: abreviações, erros de grafia, inversão na ordem da frase, ambiguidade, local ausente ou não cadastrado. Total: 39 casos, incluindo seis que devem solicitar esclarecimento sem rota. Argumentos são avaliados após normalização; os brutos ficam no registro. `apresentacao_fiel` verifica fidelidade ao retorno da ferramenta, não compreensão da intenção. Testar também frases inéditas criadas pelo grupo e revisar as respostas manualmente.

Após a execução real da seção 9.1 no Colab, baixe a pasta `resultados_agente/<execucao>/`: ela contém `metadados.json`, `casos_esperados.json`, `resultados.json`, `resumo.json` e `revisao_manual.json`. As chamadas, respostas e erros ficam preservados; cada caso é salvo antes de iniciar o próximo. Preencha a revisão em arquivo separado, sem substituir os resultados brutos. Os testes locais com respostas controladas não geram taxas de acerto do Qwen.

`Marco_1/` e `Marco_2/` guardam a versão anterior em trechos para consulta histórica; use o notebook unificado para o trabalho atual. `AUTORES_PREENCHER.md` contém os dados a preencher pelo grupo. A planta está em `referencias/planta_terreo_iesb.png`.

## Gráficos e comparação com o gabarito

As seções 5.1 e 5.2 geram tabela e quatro gráficos: nós expandidos, custo em metros, tempo de execução das buscas e referência ideal de deslocamento a 15 km/h sem atrasos. O experimento do Marco 1 usa custo uniforme e A* em recortes conectados da mesma planta com 20, 40 e 70 nós. Os tempos de execução são medidos em cada execução; a preparação da heurística é contabilizada separadamente. Os PNGs são salvos na pasta de execução.

Verificação local: quatro PNGs gerados, resultados de custo iguais entre buscas nos três recortes, e admissibilidade e consistência da heurística verificadas nos 8.100 pares do mapa. A* e custo uniforme expandiram 19, 39 e 69 nós; esta amostra não mostrou redução de expansões com A*. Isso decorre dos empates da heurística e da consulta escolhida; não se deve afirmar que o A* sempre será mais rápido.

Veja [COMPARACAO_COM_PROFESSOR.md](COMPARACAO_COM_PROFESSOR.md) para saber exatamente o que foi mantido e acrescentado.
