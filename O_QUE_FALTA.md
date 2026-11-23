# O que falta para os Marcos 1 e 2

**Atualização: 23/11/2026. Versão atual: v3, com base fixa de 15 km/h, interpretação validada e resposta direta da ferramenta.** Este arquivo reúne o relatório de situação, a estimativa de conclusão e o plano dos próximos passos solicitado pelo grupo.

Referência acadêmica: `Projeto_Academico_IA_20262.pdf`, seções 3, 5, 7 e 8, disponível localmente em `materiais_do_professor/enunciado/`. O código atual é um protótipo acadêmico funcional; os Marcos ainda não estão encerrados. O relatório de pendências abaixo não substitui os relatórios acadêmicos em PDF.

## Quanto falta: aproximadamente 30%

**Estimativa de acompanhamento: 70% concluído e 30% restante para fechar código, validação, documentação e preparação da entrega/apresentação.** Não é previsão de nota, medição de horas nem taxa de acerto do agente. É uma avaliação de prontidão com pesos definidos para este acompanhamento, não os pesos de avaliação do professor. As tarefas históricas do checklist não entram como unidades iguais, pois várias descrevem versões sucessivas da mesma funcionalidade.

| Frente de trabalho | Peso no projeto | Concluído estimado | Restante | Evidência e limite atual |
|---|---:|---:|---:|---|
| Mapa e modelagem do protótipo sintético | 15 | 15 | 0 | 90 nós/90 ligações, decisões e estimativas documentadas; não equivale a validação física. |
| Busca, heurística e experimento do Marco 1 | 15 | 12 | 3 | Custo uniforme/A*, testes e gráficos; falta resolver a aceitação dos três recortes. |
| Dados, dois modelos e custo aprendido | 20 | 20 | 0 | 2.160 linhas, validação por trecho, teste reservado e integração; reproduzidos no Colab v2. |
| Agente e tratamento da linguagem | 15 | 12 | 3 | V3 implementada e testada de forma controlada; falta validar comportamento real e adequação da explicação final. |
| Avaliação final e reprodutibilidade | 15 | 6 | 9 | Duas execuções históricas preservadas; faltam v3 em sessão nova, perguntas inéditas e revisão humana. |
| Relatórios acadêmicos | 10 | 3 | 7 | Rascunho do Marco 1 e análises técnicas disponíveis; faltam os dois PDFs finais e a consolidação de IA responsável. |
| Organização da entrega | 5 | 2 | 3 | Notebook e documentação organizados para o GitHub/Colab; faltam autores reais, conferência de acesso e comprovação de envio. |
| Demonstração e arguição | 5 | 0 | 5 | Há exemplos executáveis, mas não há evidência de ensaio do trio nem preparação individual concluída. |
| **Total** | **100** | **70** | **30** | **Percentual sujeito a revisão conforme surgirem evidências.** |

Os itens de código não devem ser marcados como finalizados academicamente só porque passam em testes simulados. Se a execução real revelar uma falha, a estimativa da frente correspondente deve diminuir até a correção ser validada. Chegar a 100% exige satisfazer os critérios de encerramento abaixo, não apenas aumentar o número de caixas marcadas.

## Relatório do estado atual

- **Busca e aprendizado:** A* integrado ao custo previsto, base fixa em 15 km/h, regressão linear comparada à árvore e dados explicitamente sintéticos. No exemplo de cadeiras no pátio, a alternativa de 46 m/23,7 s previstos supera a de 42 m/35,7 s previstos.
- **Agente v2, já executado:** escolha de ferramenta e argumentos corretos em 23/23 casos, incluindo três sem ferramenta. Houve omissões de percurso e erro de conversão na redação final. Isso não foi 100% de respostas fiéis.
- **Agente v3, implementado:** apresentação direta em Python, sem reescrita de rota pelo Qwen; nomes alternativos, grafias próximas, validação e esclarecimento com continuidade. Os 39 casos têm referências e testes controlados. **Ainda não há resultado real da v3 no Colab.**
- **Entrega:** existem análise das duas execuções anteriores, rascunho do Marco 1 e documentação técnica. Não foram encontrados os dois relatórios finais em PDF nem os nomes reais preenchidos em AUTORES.

Detalhes: [avaliação da v2](AVALIACAO_COLAB_15KMH.md), [interpretação na v3](INTERPRETACAO_DO_AGENTE.md), [dados e modelos](PROPOSTA_DADOS_FASE_2.md) e [rascunho do Marco 1](RELATORIO_MARCO_1_RASCUNHO.md).

## Próximos passos, na ordem recomendada

| Prioridade | O que fazer | Responsável proposto | Evidência para encerrar |
|---|---|---|---|
| 1 | Executar o notebook v3 inteiro no Colab, após reiniciar a sessão, com os 39 casos. Baixar notebook executado e ZIP de resultados. | Integrante de LLM, com apoio do grupo | Execução completa, sem dependência de variáveis antigas, versões/limites registrados e arquivos preservados. |
| 2 | Revisar intenção, origem/destino, ferramenta, resultado e esclarecimentos. Preencher `revisao_manual.json` com justificativa e revisor; corrigir falhas e repetir os casos afetados. | Grupo, com revisão por outro integrante | Relatório de falhas e decisões; respostas conferidas por pessoa. Igualdade com a ferramenta não basta se os argumentos estiverem errados. |
| 3 | Testar frases que não estão no notebook: abreviações novas, erros de escrita, ordem invertida, origem ausente, “não quero X”, nomes genéricos e locais desconhecidos. Testar também responder ao esclarecimento e cancelar. Sugestão de trabalho: pelo menos 10 perguntas novas, não uma exigência adicional do enunciado. | Dois integrantes que não ajustaram os exemplos | Perguntas, expectativas e resultados registrados; não alterar a expectativa para fazer uma resposta errada passar. |
| 4 | Fechar as dúvidas de adequação acadêmica descritas abaixo. Pode ocorrer em paralelo aos testes. | Grupo/professor | Confirmação registrada ou implementação/experimento ajustado com justificativa. |
| 5 | Finalizar relatório do Marco 1, de 2–4 páginas, com modelagem, buscas, heurística, tabela/gráficos, limitações e divisão do trio. | Integrante de busca + revisão do grupo | PDF final, consistente com o notebook e com a decisão sobre os três mapas. |
| 6 | Preparar relatório final, de 4–8 páginas, com dados, pré-processamento, dois modelos, métricas/erros, integração, testes reais da v3, latência, limites e IA responsável. Incluir viés sintético, ausência de dados pessoais na base, LGPD quando aplicável e declaração do uso de IA generativa. | Integrantes de dados/LLM + revisão do grupo | PDF final com resultados reais identificados por versão; sem usar testes controlados como acerto do Qwen. |
| 7 | Preencher AUTORES com os três nomes e contribuições; conferir o link do Colab e o acesso de leitura; reunir PDFs e notebook da versão validada. | Grupo | Pacote revisado, acesso conferido e envio pelo canal definido pelo professor. Publicação no GitHub não comprova entrega no Google Sala de Aula. |
| 8 | Ensaiar demonstração ao vivo de cerca de 9 minutos e arguição cruzada de cerca de 9 minutos. Todos devem explicar as três fases. | Todos os integrantes | Ensaio cronometrado: busca por distância, mudança por tempo aprendido, pergunta livre e esclarecimento; cada integrante explica uma fase do colega. |

**Próxima ação concreta:** executar a v3 no Colab e enviar o notebook executado e `resultados_agente.zip`. É esse resultado que permitirá fechar a parte de interpretação antes de escrever as conclusões do relatório final.

### Dúvidas acadêmicas a resolver sem ocultar limitações

1. **Três mapas:** hoje são recortes de 20, 40 e 70 nós da mesma planta. Confirmar se isso atende ao requisito; se não, preparar três topologias sintéticas documentadas. Não afirmar que são três plantas independentes.
2. **Explicação da decisão:** o enunciado descreve o LLM traduzindo/explicando a rota, inclusive motivos do desvio e economia. Na v3, o Python apresenta o retorno fiel da ferramenta; a resposta padrão informa percurso, distância, tempo e cenário, mas não compara automaticamente alternativas nem explica gargalos. Confirmar a adequação dessa apresentação. Se necessário, acrescentar justificativa baseada em cálculos da ferramenta, mantendo caminhos e números protegidos de reescrita incorreta.
3. **Escopo da consulta:** o protótipo resolve um par origem–destino e três cenários. O enunciado também exemplifica vários endereços e restrições. Confirmar o escopo exigido na avaliação; não declarar suporte a múltiplas entregas, bloqueios arbitrários ou horários reais que não foram implementados.
4. **Calendário e situação da entrega:** o PDF original informa datas anteriores a esta atualização e duas datas de apresentação. Conferir com o professor a situação específica do grupo; não presumir nova data ou prorrogação.

### Critérios para considerar o projeto completo

- [ ] V3 executada integralmente em sessão nova, com resultados e ambiente preservados.
- [ ] Bateria revisada por pessoa e testes inéditos documentados; falhas relevantes corrigidas ou limitações justificadas conforme o escopo aceito.
- [ ] Dúvidas sobre mapas, explicação e escopo resolvidas e registradas.
- [ ] Relatórios de 2–4 e 4–8 páginas finalizados em PDF, com IA responsável e declaração do uso de IA.
- [ ] AUTORES preenchido; notebook validado acessível; entrega formal conferida.
- [ ] Trio preparado para demonstração ao vivo e arguição cruzada.

As medições de campo e testes com carrinho físico são uma frente futura de validação do campus. O enunciado permite mapas/dados sintéticos: não são bloqueios obrigatórios para esta entrega acadêmica, desde que as hipóteses e limitações sejam declaradas. O percentual acima não representa prontidão para operação física.

## Checklist técnico e histórico das decisões

## Antes dos dois Marcos: medida do mapa

**No Marco 1, o custo é comprimento em metros (m), não área em metros quadrados (m²); no agente final, é tempo previsto em segundos.** Após a revisão dos corredores, há 90 ligações com metros aproximados. A autorização anterior para estimativas continua aplicada, com as novas hipóteses descritas em `MAPA_DO_GRAFO.md`. Falta conferir os comprimentos no campus para avaliar a precisão física, fora do fechamento do protótipo sintético.

O grafo atual tem 90 nós e 90 ligações, com um ciclo no pátio. O usuário confirmou circulação pelo chão, com muitas cadeiras e mesas: os percursos representam possibilidades condicionais, não garantia de passagem física.

## Marco 1 — busca

- [x] Nós, ligações e função de A* simples.
- [x] Subdividir os corredores confirmados de Design, C, B e I/J; rotas entre portas próximas verificadas sem retorno obrigatório à entrada. Total atual: 90 nós e 90 ligações.
- [x] Incorporar Easy Smart e Café Mania, retirar Gastro a pedido do usuário e representar os quatro lados do pátio como circulação condicionada à disposição de móveis. Distâncias e posições das mesas são hipóteses documentadas.
- [ ] Validação física futura: conferir largura disponível, posições das mesas e bloqueios por cadeiras. O programa não faz detecção física nem desvio local; não é requisito de coleta para a base sintética.
- [x] Modelagem escrita do espaço de estados: estado, origem, ações, transição, teste de objetivo e custo em metros. Incluída na seção 1.1 do notebook e no rascunho do relatório em 22/11/2026.
- [x] Distâncias aproximadas explícitas em metros e método de estimativa documentado.
- [ ] Validação física futura: conferir as aproximações com medições de campo.
- [x] Custo uniforme e A* no mesmo laço simples, com a heurística desativada/ativada.
- [x] Heurística pela diferença absoluta de distâncias até a Entrada Principal, justificada pela desigualdade triangular e verificada em todos os pares.
- [x] Experimento em recortes conectados de 20, 40 e 70 nós da mesma planta, com custo uniforme e A*, expansões, custo, tempo mediano de 30 consultas, tabela e gráficos. Uma consulta por recorte; não são três plantas independentes.
- [ ] Confirmar com o professor se três recortes da mesma planta atendem ao requisito de “três mapas de tamanhos diferentes”; se não atenderem, preparar três topologias documentadas sem alegar que são três plantas reais do campus.
- [x] Discutir no relatório os limites da amostra, os empates da heurística e o custo de preparação; não houve redução de expansões com A* nesses casos. Análise incluída no notebook e em `RELATORIO_MARCO_1_RASCUNHO.md`.
- [ ] Relatório de 2 a 4 páginas com modelagem, resultados e divisão do trio.

## Marco 2 — agente final

Em 22/11/2026, o usuário autorizou fixar a base da simulação em 15 km/h e usar uma única ferramenta de rota no agente. O custo é o tempo previsto com atrasos sintéticos; a distância da rota escolhida é informada separadamente. A fórmula `distância_m * 3.6 / 15`, sem atrasos, permanece apenas como referência do Marco 1. O aprendizado de custos continua necessário e foi treinado novamente.

- [x] Qwen, descrição da ferramenta, leitura de `<tool_call>` e ciclo do agente adaptados do gabarito.
- [x] Ferramenta do trio chama o A* do mapa do IESB.
- [x] Prompt principal (`REGRAS`) e saída estruturada de ferramenta estão versionados no notebook; não há chave de API escrita no código.
- [x] Dados sintéticos autorizados pelo grupo: 2.160 observações, regra pública, semente 42, proveniência explícita e pré-processamento na seção 5.3. CSV atual regenerado a 15 km/h em `work/resultados_fase2_15kmh/tempos_sinteticos.csv`; dados anteriores preservados.
- [x] Escolha por dados sintéticos e método adotado registrados em `PROPOSTA_DADOS_FASE_2.md`.
- [x] Regressão linear e árvore treinadas novamente a 15 km/h e comparadas em validação cruzada de 5 folds por trecho; seleção pelo MAE e teste reservado em 18 trechos. Evidência atual em `work/resultados_fase2_15kmh/resumo.json` e `previsoes_teste.csv`. Regressão escolhida; MAE de teste 0,8376 s sintéticos.
- [x] Integração do tempo previsto ao mesmo A*, com heurística em segundos. A ferramenta agora informa também os metros da rota escolhida. Verificação local atual de 24.300 pares nos três cenários contra Floyd-Warshall em `work/resultados_fase2_15kmh/verificacao.txt`.
- [x] Fixar base em 15 km/h e expor apenas `rota_tempo_previsto` para rotas, além de `listar_vizinhos`. Remover velocidade das consultas, exemplos e argumentos do agente; rejeitar parâmetros extras. Na execução real `20261122T220438_334631Z`, escolha de ferramenta e argumentos corretos em 23/23 casos, incluindo três sem ferramenta. Fidelidade final ainda não aprovada; ver `AVALIACAO_COLAB_15KMH.md`.
- [x] Demonstrar a mudança de rota no ciclo do pátio sob atraso SINTÉTICO por cadeiras no trecho A–B: rota de 42 m/42,9 s previstos substituída por 46 m/30,9 s previstos. Evidência local: `work/resultados_fase2/demonstracao_patio.json`. Reproduzida no Colab em 22/11/2026; ver `AVALIACAO_COLAB.md`. Não é resultado de campo.
- [x] Recalcular a demonstração com base fixa de 15 km/h: 42 m/35,7 s previstos contra 46 m/23,7 s previstos. Evidência local em `work/resultados_fase2_15kmh/demonstracao_patio.json`, reproduzida no novo notebook executado no Colab. Os valores do item anterior são históricos da base de 10 km/h.
- [x] Ampliar a bateria para 23 casos: os 15 anteriores, sete pedidos de tempo aprendido (incluindo cadeiras, padrão e origem=destino) e um contraste com velocidade constante. Referências preparadas antes da inferência; ferramenta, argumentos, chamadas, resultados e conteúdo mínimo avaliados separadamente.
- [x] Adaptar a bateria para `v2_base_fixa_15`: todos os pedidos de rota usam previsão, sem velocidade, e o caso 23 consulta Café Mania → Biblioteca. Preparadas e verificadas 23 referências; não comparar a taxa agregada diretamente com a bateria histórica acima.
- [x] Testar o avaliador com respostas controladas, incluindo chamadas inválidas e respostas incompletas. Evidência em `work/verificacao_avaliacao.txt`. Isso não mede o Qwen.
- [x] Executar os 23 casos com o Qwen no Colab, incluindo `rota_tempo_previsto`; preservar as evidências e analisar cada falha. Execução `20261122T172315_085694Z`, recebida em 22/11/2026, preservada em `evidencias/colab_20261122T172315_085694Z/`. Ferramenta correta em 15/23 e argumentos em 14/23; análise assistida dos 23 casos em `AVALIACAO_COLAB.md`. Isso não comprova fidelidade final.
- [x] Executar e revisar os 23 casos da versão `v2_base_fixa_15`: arquivos preservados em `evidencias/colab_20261122T220438_334631Z/`; código idêntico ao projeto na revisão, 17 células consecutivas de 1 a 17, sem erros registrados. Escolha/argumentos corretos em 23/23; conteúdo automático em 12/20; mediana de 5,57 s. Revisão assistida por caso em `AVALIACAO_COLAB_15KMH.md`. Não equivale a 100% de respostas fiéis.
- [ ] Revisar manualmente a fidelidade das respostas em `revisao_manual.json`, com justificativa e revisor. A triagem automática não comprova ausência de alucinações e não conta como fidelidade final.
- [x] Discutir os erros de interpretação, vizinhos inventados, a pergunta geral aceita fora do campus, duração e limites da medição de custo em `AVALIACAO_COLAB.md`. Mediana de 6,05 s por caso; GPU e memória não foram quantificadas. Incorporar essa análise ao relatório final.
- [x] Receber o notebook completo executado no Colab: 17 células de código consecutivas sem erros registrados, com código igual ao do projeto. Auditoria em `evidencias/colab_20261122T172315_085694Z/auditoria_arquivos.json`.
- [ ] Confirmar reinício da sessão antes da execução integral. A nova execução apresenta contagens de 1 a 17, compatíveis com sessão nova, mas sem confirmação independente do reinício.
- [x] Avaliar com Qwen real a versão que remove a escolha entre tempo constante e aprendido. Não houve erro de escolha/argumentos nesta bateria; perguntas e contrato mudaram, portanto não é comparação controlada nem prova de generalização.
- [x] Corrigir a apresentação final: a v3 devolve diretamente o texto formatado pela ferramenta, sem segunda geração do Qwen nem conversão de unidades pelo LLM. Testes controlados confirmam caminho e valores preservados; não comprova que os argumentos escolhidos correspondem à intenção.
- [x] Implementar recuperação de JSON inválido, validação de parâmetros e registro de tokens/motivo de término. Até três tentativas antes de recusar a interpretação; uma ferramenta só é executada após validação. Testado com saídas controladas; recuperação e registro real ainda precisam do Colab.
- [x] Normalizar nomes, acentos, códigos, apelidos e grafias próximas inequívocas; pedir esclarecimento para nomes genéricos, inexistentes ou ausentes. Não corrigir números por semelhança. A interface retém o pedido pendente e permite cancelar. Ver `INTERPRETACAO_DO_AGENTE.md`.
- [x] Preparar bateria v3 de 39 casos, mantendo os 23 da v2 e acrescentando 16 de interpretação/esclarecimento. Testes controlados em `work/verificar_interpretacao.py`; evidência em `work/verificacao_interpretacao_v3.txt`.
- [ ] Executar a v3 com Qwen real no Colab, revisar os 39 casos e testar perguntas independentes criadas pelo grupo, incluindo erros de escrita, omissões, negação e ordem diferente das informações. Não apresentar os testes controlados como taxa de compreensão do modelo.
- [x] Ajustar a triagem de conteúdo: aceitar “fictício” e dispensar caminho completo nos casos 20/21, que pedem apenas tempo. Mantidas verificações numéricas e de percurso nos demais casos; resultados originais preservados. Testes controlados passaram, sem substituir revisão humana.
- [ ] Reexecutar a bateria após as correções e acrescentar perguntas inéditas; registrar versões completas das dependências e revisão do modelo. Os resultados atuais não devem ser apresentados como agente final aprovado.
- [ ] Relatório de 4 a 8 páginas com avaliação, limites, IA responsável, LGPD e declaração do uso de IA generativa.
- [ ] Preencher o arquivo AUTORES com nomes e divisão de trabalho. O enunciado também pede link do Colab com leitura para o professor e relatório em PDF.

## O que o professor e o nosso código fazem

O gabarito da Aula 10 ensina o Qwen a escolher uma ferramenta, o Python a executar a ferramenta e o A* a devolver a rota. Nosso notebook segue esse fluxo e troca o mapa da Romênia pelo mapa do IESB. O gabarito da Aula 10 **não implementa** por si só o modelo aprendido da Fase 2 nem o experimento completo do Marco 1; esses requisitos vêm do enunciado geral.

## Pendências levantadas no chat de dúvidas

Registro iniciado em 22/11/2026 e consolidado em 23/11/2026. O plano e a estimativa no início deste arquivo distinguem implementação, validação real, exigências acadêmicas e validação física futura. A revisão de status usou os arquivos e as duas execuções recebidas; não realizou nova inferência do Qwen.

- [x] **Melhoria opcional — entrada interativa de perguntas:** adicionada a função `conversa_interativa()` na seção 8.1 em 22/11/2026. Ela usa `input()` e só inicia quando chamada manualmente, para não bloquear a execução integral do notebook. É bônus, não requisito obrigatório.
- [x] **Relatório das pendências e próximos passos:** consolidado neste `O_QUE_FALTA.md` em 23/11/2026, com prioridades, responsáveis propostos, critérios de encerramento e estimativa ponderada de 70% concluído/30% restante. Não substitui os PDFs acadêmicos.
