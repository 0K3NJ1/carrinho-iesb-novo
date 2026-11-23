# Comparação com o gabarito da Aula 10

Referência: `laboratorio_9_aula10_agente_com_ferramenta_gabarito.ipynb`. Comparação das funções em 14/11/2026 por árvore sintática (AST), ignorando comentários e formatação. Não é uma porcentagem de similaridade do notebook inteiro.

| Parte | Relação com o gabarito |
| --- | --- |
| `agente` | A v3 mantém funções e um laço de até três tentativas, mas acrescenta validação, normalização e esclarecimento. Após uma chamada válida, devolve diretamente seu retorno; não pede ao Qwen uma segunda redação. Os detalhes preservam tentativas brutas e chamadas executadas. |
| `ler_pedido_de_ferramenta` | A v3 exige exatamente um bloco tool_call completo e JSON válido. |
| `conversar` | Mesmo Qwen2.5-1.5B-Instruct; limite de 200 tokens em vez de 150. A v3 também registra quantidade de tokens e motivo de término. |
| `extrair_json` | A v3 decodifica o conteúdo inteiro do bloco e exige objeto, sem recuperar silenciosamente um pedaço entre chaves. |
| `executar` | Mesmo despacho por nome com if; valida pedido e argumentos. Em 22/11/2026 passou a expor apenas `rota_tempo_previsto` para rotas e `listar_vizinhos` para ligações diretas. Parâmetros de velocidade são rejeitados: a base fixa é 15 km/h. |
| Busca A* | Mesmo laço com lista de fronteira, min, visitados e custo acumulado. Agora em `buscar`, com parâmetros para o grafo, opção de custo uniforme e contador de expansões; `a_estrela` chama essa função. |
| Heurística | Professor: tabela em linha reta até Bucareste, ou zero para outro destino. Nosso: diferença absoluta de distâncias até uma referência fixa (Entrada Principal), com prova por desigualdade triangular. É uma adaptação nova. |
| Mapa | Romênia substituída por 90 locais e 90 ligações do IESB, em metros estimados. |
| Tempo | Base fixa de 15 km/h, acrescida de atrasos sintéticos para treinar o custo do agente. A conta ideal distância × 3,6 / 15 permanece apenas como referência didática do Marco 1. |
| Aprendizado de tempos | Acréscimo da Fase 2: dados sintéticos, regressão linear e árvore, validação cruzada por trecho, teste reservado e ferramenta `rota_tempo_previsto`. O mesmo laço de busca aceita tabela de referência em segundos. Não existem classes próprias; Pipeline e estimadores são componentes da biblioteca scikit-learn. |
| Experimentos/gráficos | Acréscimo para atender à comparação pedida no enunciado geral do projeto. O gabarito da Aula 10 não traz matplotlib nem esse experimento completo. |
| Avaliação com 39 casos | A v3 preserva os 23 casos anteriores e acrescenta 16 de linguagem/esclarecimento. Referências antes da inferência, argumentos normalizados, tentativas brutas, resultado, apresentação direta e revisão humana separada. Os resultados reais da v3 ainda dependem do Colab. |
| Interface por texto | Acréscimo opcional: `conversa_interativa()` usa `input()` quando chamada manualmente e não bloqueia a execução automática do notebook. |

O estilo continua com funções, listas, dicionários, if e for/while. Não foram introduzidas classes ou construtores próprios. Matplotlib desenha os gráficos; não altera as buscas. A biblioteca tem sua própria implementação interna.

O gabarito é uma base de laboratório para o agente com ferramenta. Segui-lo não basta para cumprir todos os requisitos dos dois Marcos; as pendências permanecem em O_QUE_FALTA.md. O professor original não foi alterado.
