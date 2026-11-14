# Carrinho IESB — Marcos 1 e 2 no mesmo notebook

Use **[carrinho_iesb_unificado.ipynb](carrinho_iesb_unificado.ipynb)**. Ele reúne o grafo, o A*, as ferramentas e o agente Qwen, com distâncias aproximadas em metros e tempo de deslocamento a velocidade constante.

[Abrir o notebook único no Google Colab](https://colab.research.google.com/github/0K3NJ1/carrinho-iesb-novo/blob/main/carrinho_iesb_unificado.ipynb)

## Uso

1. Na primeira célula de código, escolha `ORIGEM`, `DESTINO` e `VELOCIDADE_KMH` (padrão: 10.0; pode trocar para 15.0).
2. Execute de cima para baixo. A seção 5 já mostra caminho, metros, segundos, minutos e comparação entre 10 e 15 km/h, sem carregar o LLM.
3. Para executar o agente Qwen, continue a partir da seção 6; ela instala transformers e baixa o modelo público. No Colab, selecione GPU T4 se disponível.
4. Depois de mudar as variáveis, execute novamente as células seguintes, pois as funções usam essa configuração como padrão.

As 69 ligações têm estimativas explícitas baseadas nas dimensões gerais da planta e em hipóteses declaradas. Veja [MAPA_DO_GRAFO.md](MAPA_DO_GRAFO.md). O tempo usa `distância_m * 3.6 / velocidade_kmh`, sem paradas ou aceleração. Não é tempo observado nem modelo treinado.

Exemplo: Entrada Principal → Eixo - Norte → Pátio/Direito → Mesa 4: **107,5 m**, **38,7 s a 10 km/h**, **25,8 s a 15 km/h**.

## Situação da entrega

O código atual foi unificado, mas os requisitos acadêmicos ainda não estão completos: veja [O_QUE_FALTA.md](O_QUE_FALTA.md). O grafo é uma árvore com 70 nós; não contém rotas alternativas. A heurística continua zero, como na adaptação anterior.

Verificação local em 14/11/2026: sintaxe das células Python, 4.900 pares de origem/destino comparados com Floyd-Warshall, unidades, velocidades inválidas e argumentos repassados às ferramentas. Todos passaram. O Qwen e a execução integral deste notebook novo no Colab ainda não foram verificados. O sucesso anterior do Marco 1 no Colab se refere à versão antiga em trechos.

`Marco_1/` e `Marco_2/` guardam a versão anterior em trechos para consulta histórica; use o notebook unificado para o trabalho atual. `AUTORES_PREENCHER.md` contém os dados a preencher pelo grupo. A planta está em `referencias/planta_terreo_iesb.png`.
