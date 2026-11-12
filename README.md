# Carrinho IESB — pacote para revisão do grupo

Este pacote reúne o código atual dos Marcos 1 e 2. **Ainda não é uma entrega completa para avaliação.** Leia `O_QUE_FALTA.md` antes de apresentar os notebooks como prontos.

## Arquivos

- `Marco_1/busca_iesb.ipynb`: mapa, A* e três consultas de rota. Roda sem carregar o LLM.
- `Marco_2/agente_iesb.ipynb`: mapa, A*, Qwen, ferramentas e seis perguntas de avaliação inicial.
- `MAPA_DO_GRAFO.md`: convenções e dúvidas da leitura da planta.
- `referencias/planta_terreo_iesb.png`: planta usada para montar o grafo.
- `AUTORES_PREENCHER.md`: modelo para o grupo registrar os responsáveis.

## Testar no Google Colab

1. Abra o notebook desejado pelo GitHub ou faça upload do arquivo `.ipynb` no Colab.
2. No Marco 2, escolha uma GPU T4 se estiver disponível. A primeira célula de código instala `transformers`; o download do Qwen ocorre ao executar a célula do modelo.
3. Execute **Ambiente de execução → Reiniciar sessão e executar tudo**. Guarde a saída e anote erros. Uma execução em sessão nova é exigida pelo enunciado.
4. Não coloque tokens nem chaves de API nas células. Este notebook usa um modelo público e não contém token.

O custo atual de cada ligação é **1 trecho**. Uma rota em três trechos não significa três metros. A planta não fornece a distância de cada ligação nem observações de tempo para treinar o modelo de custo do Marco 2.
