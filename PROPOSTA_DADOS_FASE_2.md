# Proposta de dados para a Fase 2

O grupo escolheu dados sintéticos e autorizou a base fixa de 15 km/h em 22/11/2026. A seção 5.3 implementa a geração e o treinamento; os resultados atuais ficam em `work/resultados_fase2_15kmh/`. A pasta anterior `work/resultados_fase2/` mantém a geração a 10 km/h como histórico, assim como as evidências da primeira execução do Colab. Não misturar as métricas dessas versões.

Implementação adotada após subdividir os corredores: semente 42, 90 trechos, 2 cenários fictícios e 12 repetições por cenário (2.160 linhas). A coluna `cenario` substitui a faixa de horário da proposta: não atribuímos condições observadas a horários reais. `fluxo` é um nível fictício inteiro de 0 a 5, `piso` é regular/irregular, `porta` é 0/1 e `obstaculo` é um atraso 0/1. O alvo `tempo_s` e os atributos são sintéticos. A fórmula completa consta da seção 5.3. O arquivo `tempos_sinteticos.csv` preserva origem e destino, identificador de trecho, repetição e proveniência.

Não houve remoções, duplicatas de identificador ou faltantes no conjunto gerado. O pré-processamento usa imputação por mediana/moda, padronização numérica e one-hot dentro de cada fold. Uma divisão por trecho reserva 18 trechos para teste e usa 72 para treino; a validação cruzada agrupa os trechos em cinco folds. Escolhemos entre regressão linear e árvore pelo MAE de validação. O teste reservado não participa da seleção. Previsões são limitadas a pelo menos 0,1 segundo, tanto na avaliação quanto na ferramenta.

A ferramenta oferece os cenários `tranquilo` e `movimentado`, com fluxo fixado em 1/4 e atraso de obstáculo em 0/1. A velocidade base da geração é fixa em 15 km/h, registrada no CSV como proveniência, sem entrar como atributo variável de treinamento. Regra do alvo: `distância × 3,6 / 15 × (1 + 0,15 × fluxo + 0,25 × piso_irregular) + 3 × porta + 12 × obstáculo + ruído`, com mínimo de 0,1 s. Semente, observações e penalidades foram mantidas; os alvos foram regenerados e ambos os modelos treinados novamente. Esses valores são hipóteses didáticas. Os dois sentidos recebem o mesmo peso. O A* recebe uma nova tabela de referência em segundos para cada cenário; a heurística em metros permanece restrita ao Marco 1.

## Resultados atuais — base fixa de 15 km/h

Decisão concluída: opção A. Resultados locais da implementação, não medições físicas:

| Modelo | MAE de validação (s) | RMSE de validação (s) | R² de validação |
| --- | ---: | ---: | ---: |
| Regressão linear | 0,8541 | 1,1655 | 0,9728 |
| Árvore de decisão | 0,9999 | 1,5293 | 0,9532 |

A regressão linear foi escolhida pelo MAE de validação; no teste reservado obteve MAE 0,8376 s, RMSE 1,1639 s e R² 0,9728. Detalhes em `work/resultados_fase2_15kmh/resumo.json` e `previsoes_teste.csv`. A regra do alvo mudou; o erro menor não demonstra melhora de precisão física nem melhora do Qwen. Os trechos de treino/teste permaneceram iguais aos da versão anterior.

O cenário adicional `cadeiras_no_patio` reutiliza entradas do treinamento: todos os trechos têm perfil tranquilo, exceto A–B, com perfil movimentado, fluxo 5 e obstáculo 1. Trata-se de atraso hipotético localizado; não significa que uma cadeira foi detectada ali. O treinamento permanece nos dois cenários originais. Na demonstração Mesa 1 → Mesa 4, a rota mais curta tem 42 m e 35,7 s previstos nesse cenário; a busca em tempo escolhe o outro lado, com 46 m e 23,7 s previstos (economia prevista de aproximadamente 12 s). Os valores são calculados pelo modelo, não inseridos como custos prontos. A saída completa é salva em `demonstracao_patio.json`.

O agente agora recebe somente uma ferramenta de rota, `rota_tempo_previsto`, e a consulta de vizinhos. Origem e destino são obrigatórios; cenário é opcional, com padrão tranquilo. A velocidade não é recebida nem solicitada. O custo do A* é tempo em segundos; a distância retornada é a soma dos metros da rota escolhida por tempo. Não há soma de metros com segundos. A execução real no Colab reproduziu as métricas de treinamento e a demonstração do pátio. Na bateria de 23 casos, ferramenta e argumentos foram corretos em todos, mas restaram falhas de redação final; ver `AVALIACAO_COLAB_15KMH.md`.

### Opção A — dados sintéticos declarados

É a opção mais reprodutível para o prazo e é permitida pelo enunciado. O grafo e as distâncias aproximadas permanecem os atuais, mas os tempos de travessia são gerados por regras públicas e uma semente fixa. Todo gráfico e relatório deve usar a expressão **tempo sintético**, nunca “tempo medido no campus”.

Proposta de geração:

- uma linha representa um trecho em um cenário;
- repetir cada ligação cadastrada em diferentes cenários e níveis de fluxo;
- usar uma semente aleatória fixa para permitir a reprodução;
- calcular um tempo-base pela distância e acrescentar penalidades declaradas para fluxo de pessoas, porta estreita, obstáculo temporário e tipo de piso;
- acrescentar um ruído pequeno e controlado apenas para evitar um alvo perfeitamente determinístico;
- salvar as regras e os parâmetros junto do CSV.

Essa opção permite comparar modelos, mas não prova o tempo físico do carrinho. Ela avalia se o agente aprende as regras do cenário fictício criado pelo grupo.

### Opção B — coleta real no campus

É mais fiel ao local, porém exige trabalho de campo. O grupo percorre cada trecho com o mesmo procedimento e registra o tempo com cronômetro, sem estimar valores ausentes.

Protocolo mínimo proposto:

- identificar a ligação pelos dois nós do grafo;
- registrar data, faixa de horário e duração em segundos;
- fazer pelo menos três repetições por ligação em mais de uma faixa de fluxo;
- manter o mesmo ponto de início e fim em todas as repetições;
- anotar somente condições do trajeto, sem nomes, imagens ou identificação de pessoas;
- marcar medições interrompidas, sem substituí-las por valores inventados;
- revisar as distâncias aproximadas durante a coleta, quando possível.

Essa opção demanda centenas de percursos se cobrir todas as ligações em vários horários. Se o grupo reduzir o escopo, a limitação precisa ser declarada e a integração só poderá prever os trechos contemplados de forma justificável.

## Colunas propostas

| Coluna | Tipo | Significado |
| --- | --- | --- |
| `origem` | categoria | Primeiro nó da ligação |
| `destino` | categoria | Segundo nó da ligação |
| `distancia_m` | número | Distância aproximada ou conferida |
| `faixa_horario` | categoria | Por exemplo: início da manhã, intervalo, noite |
| `fluxo_pessoas` | categoria ordinal | baixo, médio ou alto, segundo regra definida |
| `obstaculo_temporario` | 0/1 | Presença de bloqueio no cenário ou na observação |
| `porta_estreita` | 0/1 | Característica cadastrada e conferida do trecho |
| `tipo_piso` | categoria | Categoria conferida ou definida no cenário sintético |
| `tempo_s` | número | Alvo: tempo real medido ou tempo sintético, nunca misturados sem uma coluna de origem |
| `origem_do_dado` | categoria | `real` ou `sintetico` |

Características não confirmadas devem ficar ausentes até a conferência. Não preencher portas, pisos ou obstáculos olhando apenas os pixels da planta.

## Pré-processamento proposto

1. Conferir duplicatas, valores negativos e unidades.
2. Separar entradas e alvo antes do treino.
3. Preencher faltantes somente com uma regra documentada; se uma característica essencial não puder ser recuperada, remover a linha e contar a remoção.
4. Aplicar codificação one-hot nas categorias nominais.
5. Normalizar variáveis numéricas nos modelos sensíveis à escala, usando parâmetros aprendidos apenas no conjunto de treino.
6. Manter todas as etapas dentro de um `Pipeline` para evitar vazamento de dados.

## Modelos e validação propostos

Comparar, no mínimo:

- regressão linear, como referência simples e explicável;
- árvore de decisão, para relações não lineares.

Uma floresta aleatória pode ser acrescentada, mas não substitui a explicação dos dois modelos básicos. Avaliar com validação cruzada e registrar MAE, RMSE e R². Se houver várias linhas para a mesma ligação, usar grupos por ligação na validação para evitar que cenários quase iguais do mesmo trecho apareçam simultaneamente em treino e validação.

O modelo escolhido deve ser o que apresentar melhor equilíbrio entre erro e explicabilidade, não simplesmente o resultado mais conveniente. Também é necessário mostrar onde ele erra mais.

## Integração com o A*

Para uma consulta, o modelo prevê o tempo de cada ligação no cenário escolhido. O A* usa esses tempos positivos como custo das arestas. A distância continua disponível para comparação, mas deixa de ser o custo principal da Fase 2.

O grafo atual tem um ciclo no pátio. A demonstração local usa trajetos confirmados como possíveis pelo chão, condicionados à disposição de móveis. O cenário hipotético de atraso por cadeiras altera o custo previsto de A–B e a rota escolhida. Isso não é percepção do ambiente: um trecho fisicamente intransponível deve ser excluído, e não receber apenas um tempo maior. A verificação da largura livre continua pendente.

## Evidências a guardar

- CSV e dicionário de dados;
- código que gera os dados sintéticos ou protocolo das medições reais;
- contagem de linhas removidas ou corrigidas;
- parâmetros da validação cruzada e semente aleatória;
- métricas por modelo e previsões fora do esperado;
- versão do notebook executada do início ao fim no Colab.

