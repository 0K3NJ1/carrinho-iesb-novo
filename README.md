# Carrinho IESB

Implementação atual: [carrinho_iesb_unificado.ipynb](carrinho_iesb_unificado.ipynb). Execute de cima para baixo no Jupyter ou [Colab](https://colab.research.google.com/github/0K3NJ1/carrinho-iesb-novo/blob/main/carrinho_iesb_unificado.ipynb). A parte do Qwen baixa o modelo e recomenda GPU T4.

- `materiais_do_professor/`: acervo completo disponível, com laboratórios, gabarito, slides, enunciado e variantes de backup. Consulte o inventário `LEIA_ME.md`; variantes têm autoria não verificada.
- `MAPA_DO_GRAFO.md` e `referencias/planta_terreo_iesb.png`: mapa atual e decisões do grafo.
- `INTERPRETACAO_DO_AGENTE.md`: funcionamento e limites do agente.
- `AUTORES_PREENCHER.md`: identificação do grupo.

## Próxima análise

Comparar o código do grupo com os laboratórios e o gabarito do professor para aproximar seu nível de complexidade do ensinado em aula. Priorizar funções pequenas, variáveis claras e fluxo sequencial explicável, preservando os requisitos do enunciado. O gabarito da Aula 10 é a principal referência do agente; o laboratório de busca orienta os algoritmos.

O LLM interpreta pedidos e seleciona ferramentas; o A* calcula rotas; a regressão estima tempos com dados sintéticos. A velocidade base de 15 km/h é uma hipótese. Não há detecção física de obstáculos. O grafo tem 90 nós e 90 ligações. A bateria v3 tem 39 casos e ainda precisa de validação real no Colab; testes controlados não medem compreensão real do Qwen.

## Organização de 24/11/2026

O projeto usa um notebook, sem pastas separadas por marcos. Versões antigas, rascunhos, evidências anteriores e arquivos temporários de `work/` foram retirados da árvore atual e continuam recuperáveis no histórico Git. O código do notebook foi preservado nesta limpeza. Todo o acervo disponível do professor foi incluído; apenas o texto final do inventário foi atualizado.
