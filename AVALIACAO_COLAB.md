# Avaliação da execução no Colab — 22/11/2026

**Registro histórico:** esta execução é anterior à mudança para base fixa de 15 km/h e ferramenta única de rota. A comparação de código abaixo foi feita antes dessa mudança. As taxas registradas aqui não avaliam a versão atual; os arquivos originais continuam preservados.

O notebook executou os 23 casos com Qwen real, mas o agente ainda confunde pedidos de velocidade constante com previsão aprendida. A execução completa não significa que as respostas estejam corretas. Os Marcos permanecem em andamento.

## Evidências e integridade

Os dois arquivos enviados pelo usuário foram preservados, sem alterar seus bytes, em [evidencias/colab_20261122T172315_085694Z](evidencias/colab_20261122T172315_085694Z/). Essa pasta contém o ZIP original, o notebook executado, os JSON extraídos e `auditoria_arquivos.json` com hashes SHA-256 e verificações. Os resultados individuais ficam em `resultados_agente/20261122T172315_085694Z/resultados.json` dentro dessa pasta.

- As 17 células de código coincidem com o notebook principal do projeto e têm contagens consecutivas de 2 a 18. Não há saídas de erro registradas. Isso não comprova que a sessão começou sem variáveis anteriores.
- Os IDs 1 a 23 estão presentes, sem duplicação. As contagens e a mediana de `resumo.json` foram recalculadas e conferem.
- Modelo: `Qwen/Qwen2.5-1.5B-Instruct`, CUDA, `transformers=5.22.1`, `torch=2.14.1+cu130`, geração determinística, limite de 200 novos tokens e até três passos.
- A revisão exata do modelo está nula nos metadados. Versões de bibliotecas de aprendizado, tipo de GPU e pico de memória não foram registrados; a reprodução exata ainda tem limitações.
- Esta análise é assistida pelo Codex. O arquivo original `revisao_manual.json` continua pendente e deve ser validado e assinado pelo grupo. Não houve nova inferência nesta revisão.

## Resultado automático

| Critério | Resultado | Interpretação |
|---|---:|---|
| Escolha da ferramenta, incluindo não chamar quando esperado | 15/23 (65,2%) | Nos 20 pedidos que exigem ferramenta, são 12/20. |
| Argumentos corretos | 14/23 (60,9%) | Nos 20 pedidos com ferramenta, são 11/20. |
| Quantidade esperada de chamadas | 20/23 (87,0%) | Uma chamada pode usar a ferramenta errada. |
| `resultado_valido` | 14/23 (60,9%) | Verifica o fluxo e resultado da ferramenta; não comprova fidelidade do texto final. |
| Conteúdo mínimo automático | 5/20 (25,0%) | Contém falsos negativos; não usar como taxa final de qualidade. |

A mediana foi 6,05 s por caso; mínimo de 1,04 s, máximo de 18,80 s e soma de 160,57 s. São tempos da avaliação nessa sessão, sem incluir todo o carregamento/treino. Não houve exceção registrada pelo avaliador, embora existam chamadas inválidas e respostas erradas. Não houve medição de custo financeiro: execução local não cobra uma API por resposta, mas consome recursos do ambiente Colab.

## Leitura dos 23 casos

As observações abaixo comparam pergunta, chamada, retorno e resposta final. São apoio à revisão humana, não preenchimento automático de fidelidade.

| Caso | Observação |
|---:|---|
| 1 | Ferramenta, caminho, distância e tempo constante corretos. |
| 2 | Pediu 15 km/h; chamou previsão no cenário movimentado. Resposta termina no meio de um nome de nó. |
| 3 | Pediu velocidade constante; chamou previsão com `tranqüilo`, valor rejeitado. Prometeu recalcular, mas não fez nova chamada. |
| 4 | Caminho coerente, mas substituiu o cálculo a velocidade constante por previsão sintética de 90,9 s. Não atende ao pedido. |
| 5 | Ferramenta errada; texto repete/reordena pontos do corredor e termina incompleto. |
| 6 | Pediu 10 km/h; recebeu previsão movimentada de 82,9 s em vez do cálculo constante de 15,1 s. |
| 7 | Exibiu `<tool_call>` com JSON inválido; nenhuma ferramenta foi executada. |
| 8 | Mesmo problema de JSON inválido, além da intenção incorreta de usar previsão para um pedido de 15 km/h. |
| 9 | Vizinhos diretos do pátio conferem com a ferramenta. |
| 10 | Não consultou a ferramenta; enumerou pontos distantes como vizinhos e terminou incompleto. |
| 11 | Vizinhos diretos de Cinema corretos. |
| 12 | Vizinhos diretos de Corredor I/J corretos. |
| 13 | Saudação respondida sem ferramenta, como esperado. |
| 14 | Agradecimento respondido sem ferramenta, como esperado. |
| 15 | Respondeu Brasília sem ferramenta. O teste aceita essa pergunta geral; não testa uma política de recusar assuntos fora do campus. |
| 16 | Ferramenta correta, mas cenário `tranqüilo` rejeitado. Prometeu tentar novamente sem executar. |
| 17 | Caminho e 82,9 s corretos; explicita cenário fictício. Falso negativo da exigência literal de “sintético”. |
| 18 | Ferramenta e 30,9 s corretos. Diz “fictício”, mas a enumeração termina no Pátio/Direito; Mesa 4 aparece apenas na apresentação do destino. O grupo deve julgar se a descrição é suficientemente clara. |
| 19 | Caminho e 35,6 s corretos, com aviso de cenário fictício e ausência de correspondência garantida com o campus. Falso negativo lexical. |
| 20 | Tempo padrão de 7,8 s correto. A pergunta pede tempo, mas o avaliador exige também todos os nós. A resposta avisa falta de validação no campus, sem explicitar a origem sintética dos dados. |
| 21 | Tempo zero correto para origem igual ao destino. A afirmação de que o modelo não considera tempo de passagem entre móveis é uma generalização sem apoio: há penalidade sintética por obstáculo. Não explicita dados sintéticos. |
| 22 | Caminho inverso e 30,9 s corretos; cenário fictício explicitado. Falso negativo lexical. |
| 23 | Distinguiu corretamente o pedido explícito de velocidade constante: 42 m e 10,1 s a 15 km/h. |

Os casos 17, 19 e 22 mostram que a checagem literal por `sintetic` rejeita descrições semanticamente equivalentes. Isso precisa ser corrigido sem retirar verificações de caminho, valores ou origem dos dados. Os casos 18, 20 e 21 exigem análise própria; aceitar a palavra “fictício” não resolve todas as ressalvas.

## Busca e aprendizado

A regressão linear foi selecionada por MAE de validação de 1,037762 s, frente a 1,158831 s da árvore. No teste reservado por trecho: MAE de 1,014002 s, RMSE de 1,520730 s e R² de 0,969581. São resultados sobre dados sintéticos, não precisão medida no campus. A árvore teve números um pouco diferentes da execução local anterior; sem as versões completas das dependências, não se pode atribuir uma causa comprovada.

A demonstração do pátio foi reproduzida no Colab: no cenário de cadeiras, a rota curta `Mesa 1 → A → B → Pátio/Direito → Mesa 4` mede 42 m e custa 42,9 s previstos. O A* com custo aprendido escolhe `Mesa 1 → A → D → Pátio/Direito → Mesa 4`, com 46 m e 30,9 s previstos, economizando cerca de 12 s sintéticos. A passagem física continua condicionada à disposição dos móveis.

O LLM interpreta o pedido e escolhe a ferramenta. O A* calcula o caminho sobre o grafo e os custos recebidos. Uma ferramenta escolhida incorretamente pode devolver uma rota matematicamente válida para uma tarefa diferente da solicitada. No experimento do Marco 1, custo uniforme e A* mantiveram os mesmos custos e expansões nos três recortes; esta execução não demonstra vantagem de expansões do A*.

## Próximas correções e validação

1. Reforçar a distinção entre velocidade constante e previsão aprendida nas descrições e exemplos das ferramentas; testar novamente sem presumir melhora.
2. Validar JSON, argumentos e cenários, tratar variantes conhecidas de escrita e permitir recuperação de erro. Não entregar chamada malformada como resposta ao usuário nem encerrar com promessa de execução.
3. Investigar as respostas incompletas, registrar o motivo de parada e revisar o limite de tokens. Os cortes observados são compatíveis com o limite de 200, mas o arquivo não registra a causa de término.
4. Corrigir a triagem semântica e adequar o conteúdo exigido à pergunta. Manter os resultados brutos desta execução e identificar separadamente qualquer reavaliação.
5. Executar novamente os 23 casos após as correções em sessão nova, acrescentar perguntas inéditas para evitar ajuste apenas à bateria conhecida e preencher a revisão humana.

Nenhuma dessas correções de código foi aplicada nesta revisão dos arquivos. O checklist foi atualizado apenas com o que as evidências recebidas comprovam.
