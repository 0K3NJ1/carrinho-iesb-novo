# O que falta para os Marcos 1 e 2

Comparação com `materiais_do_professor/enunciado/Projeto_Academico_IA_20262.pdf` e com o gabarito da Aula 10. O código atual é um protótipo do agente de rotas; estes itens ainda precisam de dados, implementação ou resultados reais.

## Antes dos dois Marcos: medida do mapa

**Custo de rota é comprimento em metros (m), não área em metros quadrados (m²).** A planta informa algumas dimensões gerais, mas não a distância de cada uma das 69 ligações do grafo. Hoje todas custam `1 trecho`. Para afirmar que uma rota é a mais curta em metros, é preciso medir os segmentos percorridos e substituir esses custos.

O grafo atual tem 70 nós e 69 ligações: é uma árvore, com um único caminho entre cada par de locais. Assim, mudar os custos não muda a sequência de nós. Para demonstrar que um obstáculo ou custo previsto muda a rota, o grupo precisa confirmar pelo menos um percurso alternativo real no campus e acrescentá-lo ao grafo.

## Marco 1 — busca

- [x] Nós, ligações e função de A* simples.
- [ ] Modelagem escrita do espaço de estados: estado, origem, ações, transição, teste de objetivo e custo em metros.
- [ ] Medidas em metros para cada ligação ou uma regra de medição reproduzível.
- [ ] Uma busca não informada (por exemplo, custo uniforme) para comparar com A*.
- [ ] Heurística própria com justificativa de admissibilidade. A heurística atual é `0`: segura, mas não informa a direção e se comporta como custo uniforme.
- [ ] Experimento em pelo menos três tamanhos de mapa com nós expandidos, custo e tempo; tabela e gráfico.
- [ ] Relatório de 2 a 4 páginas com modelagem, resultados e divisão do trio.

## Marco 2 — agente final

- [x] Qwen, descrição da ferramenta, leitura de `<tool_call>` e ciclo do agente adaptados do gabarito.
- [x] Ferramenta do trio chama o A* do mapa do IESB.
- [ ] Dados por trecho com características e tempo observado, reais ou sintéticos declarados como tal; pré-processamento documentado.
- [ ] Treinar e comparar pelo menos dois modelos de previsão de tempo, com validação cruzada e métricas de erro.
- [ ] Integrar o tempo previsto como custo do A* e demonstrar um caso em que a rota muda, após confirmar um caminho alternativo.
- [ ] Bateria de pelo menos 15 pedidos com resultado esperado antes da execução; medir ferramenta, argumentos e validade/fidelidade da rota. Há somente seis casos iniciais de escolha da ferramenta.
- [ ] Executar o Qwen no Colab, registrar acertos e falhas e testar o notebook inteiro em uma sessão nova.
- [ ] Relatório de 4 a 8 páginas com avaliação, limites, IA responsável, LGPD e declaração do uso de IA generativa.
- [ ] Preencher o arquivo AUTORES com nomes e divisão de trabalho. O enunciado também pede link do Colab com leitura para o professor e relatório em PDF.

## O que o professor e o nosso código fazem

O gabarito da Aula 10 ensina o Qwen a escolher uma ferramenta, o Python a executar a ferramenta e o A* a devolver a rota. Nosso notebook segue esse fluxo e troca o mapa da Romênia pelo mapa do IESB. O gabarito da Aula 10 **não implementa** por si só o modelo aprendido da Fase 2 nem o experimento completo do Marco 1; esses requisitos vêm do enunciado geral.
