# Interpretação e resposta direta — versão 3

Implementação autorizada em 22/11/2026 após a segunda execução no Colab. O Qwen acertou as ferramentas naquela bateria, mas reescreveu nomes, omitiu caminhos e converteu 22,3 segundos para “cerca de 3 minutos”. Agora o retorno de uma consulta válida é apresentado diretamente pelo Python, sem segunda geração do LLM.

## Responsabilidades

1. O Qwen identifica ferramenta, origem, destino e cenário a partir da pergunta, copiando os nomes como escritos. Não conhece a posição atual do carrinho e não deve inventar uma origem.
2. O Python normaliza os nomes, confere parâmetros, procura os locais no cadastro e pede esclarecimento quando necessário.
3. O modelo de regressão prevê os custos sintéticos dos trechos; o A* minimiza a soma desses tempos. A base permanece fixa em 15 km/h.
4. A ferramenta formata caminho completo, distância da rota escolhida, tempo em segundos, base fixa e aviso sintético. O agente devolve esse texto sem paráfrase do Qwen.

Essa separação garante fidelidade ao retorno de uma ferramenta executada com sucesso. Não garante que os argumentos escolhidos correspondam à intenção da pessoa: origem/destino invertidos, cenários mal interpretados e ambiguidades de linguagem ainda precisam de avaliação.

## Escrita aceita e limites

| Entrada | Tratamento |
|---|---|
| `B4`, `b04`, `sala b04` | Normaliza para `B-04`. |
| `biblio`, `bibl` | Apelidos explícitos de `Biblioteca`. |
| `patio`, `CAFÉ MANIA`, `mesa um` | Acentos/maiúsculas e apelidos cadastrados. |
| `banheiro fem do bloco C` | Normaliza para `WC Feminino C`. |
| `bibliotca`, `cafe manai`, `easy smrt` | Grafias próximas inequívocas nos testes locais. |
| `tranqüilo`, `lotado` | Cenários `tranquilo` e `movimentado`. |
| `banheiro`, `lanchonete`, `cafe` | Pede o local específico, sem escolher arbitrariamente. |
| `sala 02`, `B-07`, `auditorio` | Solicita um nome do cadastro; não inventa bloco, sala nem acesso. |
| “Quero ir para Biblioteca” | Pede a origem. |

Normalização ignora acentos e pontuação e reconhece códigos existentes. Similaridade de grafia só é aplicada a nomes com pelo menos seis caracteres e sem números: exige nota mínima de 0,88 e diferença de 0,10 para o segundo local. Esses limiares são heurísticos, não probabilidades de acerto. Números de salas e mesas nunca são corrigidos por aproximação. O dicionário de apelidos não altera a topologia do mapa.

O agente também verifica se os nomes recebidos aparecem na pergunta, literalmente após normalização ou por apelido inequívoco. Se o Qwen transformar uma palavra desconhecida em um local arbitrário, a chamada pode ser rejeitada. Essa checagem reduz invenções, mas não interpreta completamente negação, referência a “lá”, múltiplos destinos ou a intenção gramatical. Os testes reais devem incluir essas situações; não prometer entendimento de qualquer frase.

## Esclarecimento na conversa

Execute `conversa_interativa()` depois de carregar o Qwen. Exemplo:

```text
Você: mesa 1 pra lanchonete
Agente: Qual é o local de destino? Opções: Easy Smart, Café Mania. ...
Você: Café Mania
Agente: Caminho: Mesa 1 -> ... -> Café Mania
```

O programa guarda o pedido pendente e preenche somente o campo solicitado. A resposta de esclarecimento é tratada pelo Python, sem nova inferência. `cancelar` limpa o pedido; `sair` encerra a interface. Não há uma memória geral de todos os locais mencionados em conversas anteriores. Se usar `agente()` diretamente, a continuidade exige passar a `pendencia` devolvida por `retornar_detalhes=True`.

## Falhas e registros

JSON inválido, ferramenta desconhecida, parâmetros extras ou nomes não sustentados pelo texto recebem até três tentativas de interpretação. Nenhuma rota é executada antes da validação. Ao esgotar o limite, o agente pede uma reformulação e não exibe o JSON quebrado como resposta. Nome ambíguo, ausente ou não cadastrado gera esclarecimento em vez de repetição automática.

Os detalhes guardam texto bruto do modelo, pedido bruto, pedido normalizado, ajustes, chamadas efetivamente executadas, estado e pendência. Cada geração real registra quantidade de tokens e motivo de término (`eos`, `limite_tokens` ou `outro`). A recuperação não garante sucesso; seu limite evita um laço indefinido.

## Validação e próxima execução

A bateria `v3_interpretacao_resposta_direta` mantém os 23 pedidos da v2 e acrescenta 16, totalizando 39. Inclui ordem invertida (“chegar a X saindo de Y”), abreviações, grafia incorreta, informação ausente e nomes ambíguos. Os casos 33–38 devem solicitar esclarecimento sem calcular rota. Os argumentos avaliados são os normalizados; os brutos continuam disponíveis para análise. `apresentacao_fiel` mede igualdade com o retorno da ferramenta, não compreensão da intenção.

Testes controlados em `work/verificar_interpretacao.py`, também acessíveis por `work/verificar_avaliacao.py`, verificaram os 39 resultados de referência, rejeições, recuperação, resposta direta e continuidade/cancelamento. Evidência em `work/verificacao_interpretacao_v3.txt`. Esses testes substituem o Qwen por saídas conhecidas; não medem entendimento real de linguagem natural. Mapa, pesos e treinamento permanecem os mesmos da v2.

Ainda é necessário executar a v3 no Colab e revisar cada resposta. Além da bateria, o grupo deve preparar perguntas próprias sem copiar os exemplos: trocar a ordem das informações, omitir dados, usar nomes parecidos e testar abreviações novas. Registrar tanto acertos quanto esclarecimentos e falhas; não ajustar apenas às frases que já passaram. As evidências das duas execuções anteriores foram preservadas.
