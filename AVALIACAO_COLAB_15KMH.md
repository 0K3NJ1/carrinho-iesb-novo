# Avaliação do Colab — base fixa de 15 km/h

**Histórico da v2:** a v3 foi implementada depois desta revisão, com apresentação direta e normalização/esclarecimento de nomes. A afirmação de código idêntico e as pendências abaixo se referem ao momento da análise. Estas métricas não avaliam a v3.

Execução `20261122T220438_334631Z`, recebida em 22/11/2026. A versão `v2_base_fixa_15` fez corretamente as 20 chamadas de ferramenta e não chamou ferramentas nos três casos restantes. A redação final ainda apresenta omissões, frases incompletas e um erro de conversão de unidade. Isso não é uma aprovação integral do agente.

## Evidências

Arquivos originais preservados em [evidencias/colab_20261122T220438_334631Z](evidencias/colab_20261122T220438_334631Z/), junto dos JSON extraídos e de `auditoria_arquivos.json`. Os arquivos recebidos com sufixo “(1)” foram copiados com nomes simples; os bytes foram mantidos e registrados por SHA-256. O código coincide com o notebook atual do projeto no momento desta revisão.

As 17 células de código têm contagens consecutivas de 1 a 17, sem saídas de erro. Isso é compatível com execução desde o início em sessão nova, mas não comprova isoladamente o reinício do ambiente. A inspeção não executou novamente o notebook nem o Qwen.

Metadados: Qwen2.5-1.5B-Instruct, CUDA, transformers 5.22.1, torch 2.14.1+cu130, scikit-learn 1.6.1, numpy 2.4.6 e pandas 2.2.3. Base 15 km/h, custo `tempo_previsto_s`, regressão linear, semente 42, geração determinística, até 200 novos tokens e três passos. A revisão exata do modelo continua nula; tipo de GPU e pico de memória não foram registrados.

## Contagens conferidas

| Critério | Resultado |
|---|---:|
| Escolha da ferramenta ou ausência correta de chamada | 23/23 |
| Argumentos | 23/23 |
| Quantidade esperada de chamadas | 23/23 |
| Fluxo e retorno da ferramenta (`resultado_valido`) | 23/23 |
| Conteúdo mínimo automático, nos casos com ferramenta | 12/20 |

Todas as contagens foram recalculadas a partir dos resultados individuais. Os retornos das 20 chamadas coincidem com as referências salvas. Há 16 pedidos de rota, quatro de vizinhos e três sem ferramenta. Nenhuma exceção foi registrada pelo avaliador.

`resultado_valido` não significa texto fiel: verifica a chamada e seu retorno, não todas as afirmações da resposta em português. A triagem de conteúdo também não comprova fidelidade; por exemplo, aprovou o caso 2 mesmo com a última frase interrompida.

Latência mediana: 5,57 s; mínimo: 0,54 s; máximo: 13,18 s; soma dos casos: 134,11 s. Esses tempos não incluem todo o carregamento e treinamento. Não houve medição de custo financeiro ou memória.

Na execução anterior, a escolha de ferramenta foi correta em 15/23 e os argumentos em 14/23. Na atual, não ocorreu falha nesses critérios. É evidência favorável à interface simplificada nesta bateria, mas não uma comparação controlada: mudaram perguntas, contrato, instruções e dados. Não atribuir o resultado somente ao número 15 nem generalizar 100% para perguntas inéditas.

## Revisão assistida dos 23 casos

Esta leitura foi feita pelo Codex e serve de apoio ao grupo. `revisao_manual.json` permanece intacto, com fidelidade humana pendente. Não foi calculada uma taxa de fidelidade manual.

| Caso | Triagem | Observação sobre a resposta final |
|---:|:---:|---|
| 1 | Não | Caminho e 41,4 s corretos; omite 107,5 m. Refere-se a simulação, mas troca móveis por “máquinas”, sem apoio no retorno. |
| 2 | Sim | Caminho, 120 m, 51,8 s e origem sintética corretos; termina em “dados sintéticos e”, deixando a frase incompleta. |
| 3 | Não | Caminho, 174 m e 63,5 s corretos; termina em “Este modelo foi calcul”, antes de explicar a origem sintética. |
| 4 | Sim | Caminho, 39 m, 17,8 s, base fixa e ressalva de dados sintéticos sem validação conferem. |
| 5 | Não | Altera nomes de nós para “Corrida I/J”, usa expressão sem sentido (“Subscrever-se”) e omite a origem sintética. Distância e tempo conferem. |
| 6 | Não | Caminho coerente; arredonda 22,3 para 22 s, o que pode ser aceitável como aproximação, mas omite distância e origem sintética e acrescenta “máquinas”. |
| 7 | Sim | Caminho, 45 m, 17,3 s e cenário sintético corretos. |
| 8 | Sim | Todos os nós aparecem na ordem e os valores conferem. A lista de segmentos deixa implícitas as ligações Corredor I/J → Acesso Lateral e Eixo - Norte → Pátio/Direito. “Mais próxima” também não explica que o objetivo é menor tempo. Revisar clareza. |
| 9 | Sim | Vizinhos diretos do pátio corretos. |
| 10 | Sim | Vizinhos diretos de Corredor Design corretos; não repetiu a lista inventada da primeira execução. |
| 11 | Sim | Vizinhos diretos de Cinema corretos. |
| 12 | Sim | Vizinhos diretos de Corredor I/J corretos. |
| 13 | — | Saudação sem ferramenta, como esperado. |
| 14 | — | Agradecimento sem ferramenta, como esperado. |
| 15 | — | Brasília, sem ferramenta. O teste aceita resposta geral; não testa restrição de assuntos ao campus. |
| 16 | Não | Caminho e 22,3 s corretos, mas afirma “cerca de 3 minutos”. Conversão errada: 22,3 s correspondem a aproximadamente 0,37 min. Omite distância. |
| 17 | Sim | Caminho, 42 m, 74,2 s e indicação de tempo sintético conferem. |
| 18 | Sim | Rota pelo lado D, 46 m, 23,7 s e cenário sintético conferem. |
| 19 | Sim | Caminho, 26 m, 30,7 s e ressalvas conferem com a ferramenta. |
| 20 | Sim | Tempo de 7,2 s correto e cenário fictício explícito. A expressão “trabalho normal” não descreve uma medição; convém manter o nome do cenário fornecido. |
| 21 | Não | Zero segundos correto para origem igual ao destino. Não explicita a origem sintética dos dados, embora avise que não considera a realidade física do campus. “Instantaneamente” deve ser entendido como ausência de deslocamento no grafo. |
| 22 | Não | Distância, 23,7 s e ressalva sintética corretos; omite os pontos do caminho que a pergunta solicitava. |
| 23 | Não | Começa dizendo “Para ir da Biblioteca”, embora a origem seja Café Mania, e encerra a lista no Eixo - Norte sem incluir Biblioteca. Distância e tempo copiados estão corretos. |

Os oito casos rejeitados foram 1, 3, 5, 6, 16, 21, 22 e 23. Nem toda rejeição equivale a erro numérico: há omissões, paráfrases e critérios literais. Porém o caso 16 contém uma contradição numérica real, e os casos 5/23 alteram ou deixam incompletas informações de percurso.

## Aprendizado e rota do pátio

A regressão linear voltou a ser escolhida: MAE de validação de 0,854090 s, contra 0,999910 s da árvore. No teste reservado, MAE de 0,837553 s, RMSE de 1,163925 s e R² de 0,972820. Os valores reproduzem os resultados locais até diferenças de arredondamento. O alvo continua sintético e não mede precisão no campus.

A demonstração foi reproduzida: no cenário de cadeiras, a rota de 42 m tem 35,7 s previstos; a alternativa de 46 m tem 23,7 s previstos. O A* escolheu a segunda, economizando aproximadamente 12 s sintéticos. O caso 18 também comunicou corretamente essa alternativa. A passagem física continua condicionada ao espaço entre os móveis.

## Próxima correção recomendada

Priorizar a apresentação dos resultados: deixar o Qwen interpretar origem, destino e cenário, e montar a resposta de rota diretamente em Python a partir do retorno validado da ferramenta. Assim, o caminho completo, os metros, os segundos e o aviso sintético não dependem de uma segunda geração de texto. Conversões para minutos, se necessárias, devem ser calculadas pelo Python.

Essa alteração manteria o papel do LLM na escolha da ferramenta e dos argumentos e o papel do A* no cálculo da rota; mudaria apenas a apresentação após uma consulta bem-sucedida. Ela ainda não foi implementada nesta revisão.

Também permanecem pendentes recuperação de JSON inválido, validação de cenários, registro do motivo de término da geração e testes com perguntas inéditas. Não houve JSON inválido nesta bateria, mas isso não prova que o tratamento do erro esteja resolvido. As frases cortadas são compatíveis com o limite de 200 tokens; os registros não comprovam o motivo de parada.
