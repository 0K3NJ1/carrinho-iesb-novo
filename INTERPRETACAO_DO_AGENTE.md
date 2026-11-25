# Interpretação e resposta do agente — versão 5

Em 24/11/2026 o agente voltou ao ciclo do gabarito da Aula 10 (pensar → agir → observar → responder). Na v3, o texto da ferramenta era devolvido direto, sem explicação do Qwen. Isso contrariava o enunciado, que pede que o LLM explique a rota em português.

## Execuções reais de 24/11/2026 (Qwen2.5-1.5B-Instruct)

| Versão | Ambiente | Casos certos (39) | Rotas/vizinhos válidos (30) | Números sinalizados | Mediana por pedido |
|---|---|---|---|---|---|
| v4 | GPU RTX 4050 local | 24 | 21 | 6 | 3,2 s |
| v5 | GPU RTX 4050 local | 31 | 24 | 4 | 3,8 s |
| v5 | Colab **sem GPU** (CPU) | 31 | 24 | 4 | 135 s (88 min no total) |

As duas execuções da v5 deram o mesmo resultado em todos os 39 casos (`do_sample=False`), mudando só o tempo. Isso mostra o custo da inferência local: na CPU do Colab, cada pedido demora cerca de 35 vezes mais do que na GPU. Para a demonstração ao vivo é preciso escolher **T4 GPU** no Colab.

**O que a v4 mostrou:** em 15 pedidos informais o Qwen respondeu sem chamar a ferramenta e inventou rota e números (“78 metros”, “Corredor Bloco C - 04/07”, que não existe).

**O que mudou na v5:**
- As regras dizem que o Qwen não conhece o mapa, e a lista dos 90 locais saiu do prompt.
- Se a pergunta fala do mapa e o Qwen responde sem ferramenta, o código pede de novo; depois de 3 passos, o agente diz que não conseguiu.
- O JSON sem as marcas `<tool_call>` passou a ser aceito.
- A conferência do local agora aceita abreviação e erro de digitação (`local_na_pergunta`).
- O cenário com grafia errada (`tranqulho`, `tranq`) passou a ser aceito.

**Falhas que restam na v5 (limite do modelo de 1,5B):**
- Respostas sem chamada mesmo depois do segundo pedido: “Easy Smart para Café Manai, caminha 203”, “origem=ma1 destinaçao=ma4”, `segue rota_tempo_previsto(origem="biblio", ...)` e a pergunta repetida (“da biblioteca para B-07”).
- “O que há ao lado do Corredor Design?” gerou uma chamada de rota sem destino.
- Números arredondados na explicação (74,2 s → “74 segundos”; 51,8 s → “51 segundos”), que foram sinalizados corretamente.

Nenhuma rota inventada chegou ao usuário na v5: ou veio da ferramenta, ou o agente respondeu que não conseguiu.

## Responsabilidades

1. **Pensar:** o Qwen lê a pergunta e decide se pede `rota_tempo_previsto`, `listar_vizinhos` ou nenhuma ferramenta. Copia os nomes como o usuário escreveu.
2. **Conferir:** o Python padroniza nomes (acentos, `b4` → `B-04`, apelidos), confere se os nomes aparecem na pergunta e valida o cenário. Local genérico, ausente ou desconhecido gera uma pergunta ao usuário, sem escolher por ele.
3. **Agir:** a ferramenta roda o A* com os tempos previstos pelo modelo da Fase 2 (base fixa de 15 km/h, dados sintéticos).
4. **Observar:** o resultado volta ao Qwen como mensagem com papel `"tool"`. Se for erro (JSON inválido, nome fora da pergunta), o Qwen pode corrigir a chamada. O limite é de 3 passos.
5. **Responder:** o Qwen explica caminho, metros e segundos em português.

## Controle de alucinação

Na segunda execução no Colab (v2), o Qwen converteu 22,3 s em “cerca de 3 minutos”. Por isso as regras mandam copiar os números sem converter, e `numeros_fora_da_ferramenta` compara os números da explicação com os do retorno da ferramenta. Se aparecer um número que não veio da ferramenta, o agente acrescenta um aviso e o resultado exato. A triagem é simples: pode dar alarme falso (por exemplo, “1 minuto”) e não detecta caminho reescrito com palavras.

## Escrita aceita e limites

| Entrada | Tratamento |
|---|---|
| `B4`, `b04`, `sala b04` | Normaliza para `B-04`. |
| `biblio`, `bibl`, `patio`, `mesa um` | Apelidos cadastrados. |
| `bibliotca`, `cafe manai`, `easy smrt` | Erro de digitação: `get_close_matches` com semelhança ≥ 0,85 e um único candidato. |
| `banheiro fem do bloco C` | Trocas de palavras (`banheiro` → `wc`, `fem` → `feminino`; ignora `do`, `bloco`, `sala`) → `WC Feminino C`. |
| `lotado`, `tranqüilo` | Cenários `movimentado` e `tranquilo`. |
| `banheiro`, `lanchonete` | Pergunta qual local específico. |
| `sala 02`, `B-07`, `auditorio` | Pede um nome do mapa; não inventa sala. |
| “Quero ir para Biblioteca” | Pergunta a origem. |

Números de salas e mesas nunca são corrigidos por aproximação.

### Como o código padroniza (v4 simplificada)

`padronizar` deixa o texto em minúsculas, sem acentos e sem pontuação, separa letra de número (`b4` → `b 4`), tira zeros à esquerda e aplica a tabela `TROCAS`. Depois `resolver_local` procura, nesta ordem: nome do mapa ou apelido (`NOMES`), nome genérico (`GENERICOS`, que gera pergunta ao usuário) e, só para textos sem número, um nome parecido. Um `assert` garante que dois locais nunca ficam com o mesmo nome padronizado. `preparar_pedido` devolve `ok`, `erro` (volta para o Qwen) ou `esclarecimento` (pergunta ao usuário).

## Conversa por texto

`conversa_interativa()` reenvia ao Qwen as duas últimas trocas. Assim, depois de um esclarecimento (“Qual é o local de destino?”), a resposta “Café Mania” é entendida junto do pedido anterior. Isso depende do Qwen; não é garantido como era a pendência da v3. `cancelar` limpa o histórico e `sair` encerra.

## Validação

A avaliação (seção 9 do notebook) segue a Etapa 5 do gabarito: `CASOS` é uma lista de tuplas `(pergunta, o que fazer, argumentos)`, em que “o que fazer” é a ferramenta, `None` (sem ferramenta) ou `'esclarecer'`. Para cada caso, o laço imprime `certo`/`ERRADO`, a escolha, os números inventados e o tempo. No fim, mostra os totais, lista os casos com erro e salva `resultados_agente/avaliacao_v4.csv`. A versão das regras fica em `VERSAO_REGRAS`.

O código em volta do modelo foi testado em 24/11/2026 com um Qwen falso (respostas fixas), rodando as células no Pyodide: ciclo completo, papel `"tool"`, detecção de número inventado, saudação, esclarecimento, continuação, JSON inválido, padronização de nomes e a avaliação inteira (39 de 39 com o Qwen falso fiel; 30 de 30 explicações sinalizadas com o Qwen falso que inventa números). Esse teste **não mede** o Qwen real. A avaliação ainda precisa ser executada no Colab, e a célula “Sua análise” preenchida com os resultados.
