# Relatório de mudanças — 24/11/2026

Este relatório descreve o que mudou no projeto desde o commit `c0bb98d` (“Organiza projeto unificado…”) e por quê. As mudanças foram feitas com apoio de IA generativa (Claude), o que deve constar na declaração de uso de IA do relatório final.

## Por que mudar

Comparando o notebook com o enunciado e com o gabarito do professor (`materiais_do_professor/gabaritos/laboratorio_9_aula10_agente_com_ferramenta_gabarito.ipynb`), apareceram três problemas:

1. **O LLM não explicava a rota.** Na v3, o texto da ferramenta era devolvido direto ao usuário. O enunciado (seção 3.3) pede que o LLM “traduza o resultado de volta em linguagem natural”, e o gabarito (TODO 4) devolve o resultado ao modelo com o papel `"tool"`.
2. **A complexidade estava muito acima da aula.** Normalização com várias expressões regulares, nota de similaridade com margem, pendências de conversa e um avaliador com seis critérios e cinco arquivos JSON. Na arguição cruzada, qualquer integrante pode ter que explicar esse código sem consulta.
3. **A v3 nunca tinha sido executada com o Qwen real.**

## O que mudou no notebook

### 1. Ciclo do agente igual ao gabarito (seção 7, função `agente`)

| Antes (v3) | Agora (v5) |
|---|---|
| O Qwen escolhia a ferramenta e o Python devolvia o texto da ferramenta direto | **Pensar → agir → observar → responder**: o resultado volta ao Qwen como mensagem `"tool"`, e ele explica a rota em português |
| Esclarecimento guardado numa “pendência” de conversa | Esclarecimento devolvido ao usuário; a conversa interativa reenvia as duas últimas trocas ao Qwen |
| — | `numeros_fora_da_ferramenta`: se a explicação tiver número que não veio da ferramenta, o agente avisa e mostra o resultado exato |
| — | `fala_do_mapa`: se a pergunta é sobre o mapa e o Qwen respondeu sem ferramenta, o código pede de novo; depois de 3 passos, diz que não conseguiu, em vez de mostrar uma rota inventada |

**Por quê:** cumprir o enunciado e o gabarito, sem perder a proteção contra respostas inventadas. Essa proteção era o motivo de a v3 existir, porque o Qwen tinha convertido 22,3 s em “cerca de 3 minutos”.

### 2. Padronização de nomes mais simples (seção 7)

| Antes | Agora |
|---|---|
| `chave_local` com 9 expressões regulares | `padronizar`: tira acentos e pontuação, separa `b4` em `b 4`, tira zeros à esquerda e usa a tabela `TROCAS` (`banheiro` → `wc`, `fem` → `feminino`, ignora `do`, `sala`, `bloco`) |
| `SequenceMatcher` com nota 0,88 e margem 0,10 | `get_close_matches(..., cutoff=0.85)`, aceito só se houver um único candidato |
| `APELIDOS` misturando apelido e nome genérico | `APELIDOS` (levam a um local) e `GENERICOS` (geram pergunta ao usuário) |
| `citado_no_pedido` comparando o texto literal | `local_na_pergunta`: testa trechos de 1 a 4 palavras da pergunta com o mesmo `resolver_local`, aceitando abreviação e erro de digitação |
| `preparar_pedido` com lista de “ajustes” | `preparar_pedido` devolve só `ok`, `erro` (volta ao Qwen) ou `esclarecimento` (pergunta ao usuário) |

O código dessa parte caiu de 131 para 105 linhas não vazias. Um `assert` garante que dois locais nunca ficam com o mesmo nome padronizado.

**Por quê:** cada função faz uma coisa só e pode ser explicada na arguição. As regras de segurança continuam: número de sala nunca é “corrigido”, local genérico gera pergunta e local que o usuário não escreveu é recusado.

### 3. Avaliação no formato da Etapa 5 do gabarito (seção 9)

| Antes | Agora |
|---|---|
| 39 dicionários e as funções `normalizar_argumentos`, `preparar_resultado_esperado`, `normalizar_texto`, `conferir_conteudo` e `avaliar_caso` | 39 tuplas `(pergunta, o que fazer, argumentos)` |
| Pasta com data e hora e cinco arquivos JSON, com revisão manual pendente | Um laço que imprime `certo`/`ERRADO`, os totais e a lista de casos com erro, e salva um CSV |
| Variável `RESULTADOS` reutilizada, apagando a tabela da Fase 1 | A tabela da avaliação se chama `AVALIACAO` |

**Por quê:** é o que o gabarito ensina e o que o enunciado pede (pelo menos 15 pedidos, quantos acertos e análise das falhas).

### 4. Prompt versionado

`VERSAO_REGRAS` guarda a versão atual, e um comentário resume v1 a v5. A versão vai no nome do CSV da avaliação.

**Por quê:** o enunciado pede “prompts versionados”.

### 5. Célula “Sua análise”

Uma célula nova, como no gabarito, preenchida com os resultados reais: escolha da ferramenta, argumentos, números inventados, custo e o caso de falha para o seminário.

### 6. Textos

- O título e a introdução falam das três fases, não mais de “Marcos 1 e 2”.
- Foram removidas as referências a `O_QUE_FALTA.md` e `evidencias/`, que não existem mais.
- As seções 7, 8.1, 9 e “Limites” foram reescritas.

## O que mudou nos documentos

- `INTERPRETACAO_DO_AGENTE.md`: reescrito para a v5, com a tabela das execuções reais e as falhas que restam.
- `README.md`: o parágrafo sobre o agente e o resultado da avaliação.
- `RELATORIO_MUDANCAS.md`: este arquivo.

## Testes feitos

1. **Qwen falso (respostas fixas), no Pyodide:** ciclo completo, papel `"tool"`, detecção de número inventado, saudação, esclarecimento, continuação, JSON inválido, local que não está na pergunta, 23 casos de padronização de nomes e a avaliação inteira. Passaram todos.
2. **Qwen real, notebook inteiro do começo ao fim:** GPU RTX 4050 local e Google Colab.

| Versão | Ambiente | Casos certos (39) | Rotas válidas (30) | Números sinalizados | Mediana por pedido |
|---|---|---|---|---|---|
| v4 | RTX 4050 | 24 | 21 | 6 | 3,2 s |
| v5 | RTX 4050 | 31 | 24 | 4 | 3,8 s |
| v5 | Colab sem GPU | 31 | 24 | 4 | 135 s |

### O que o teste real mostrou e como foi corrigido (v4 → v5)

| Problema encontrado | Correção |
|---|---|
| Em 15 pedidos informais, o Qwen respondeu sem ferramenta e inventou rotas (“78 metros”, “Corredor Bloco C - 04/07”) | As regras dizem que ele não conhece o mapa; `fala_do_mapa` pede a ferramenta de novo; depois de 3 passos, o agente diz que não conseguiu |
| O Qwen usava a lista dos 90 locais do prompt para inventar nomes de corredor | A lista saiu do prompt; a padronização é feita pelo código |
| O Qwen escrevia o JSON sem as marcas `<tool_call>` | `ler_pedido_de_ferramenta` aceita JSON começando com `{` |
| O Qwen escrevia “Café Mania” quando o usuário digitou “cafe manai”, e a conferência recusava | `local_na_pergunta` aceita abreviação e erro de digitação |
| Cenário com grafia errada (“tranqulho”, “tranq”) | `resolver_cenario` aceita nomes parecidos |
| Listas numeradas (“1.”, “2.”) e “46” contra “46.0” contavam como números inventados | Marcadores de lista são ignorados, e os números são comparados como valores |
| O Qwen mandou `movimentado` num pedido sobre cadeiras | O erro devolvido indica o cenário citado na pergunta |

## Limites que continuam

- **O Qwen 1.5B ainda falha em 8 de 39 casos.** A maioria é escrita informal (3 de 10 certos). Ele escreve “origem=ma1 destinaçao=ma4” ou repete a pergunta. Nesses casos, o agente responde que não conseguiu.
- **A explicação pode arredondar números** (74,2 s → “74 segundos”, sempre sinalizado) e **acrescentar frases que não vieram da ferramenta**, que a verificação por números não detecta.
- **No Colab sem GPU, cada pedido leva cerca de 135 s.** Para a apresentação, é obrigatório escolher **T4 GPU**.
- **Continuam sem alteração:** o A* expande o mesmo número de nós que o custo uniforme no experimento (a origem é o ponto de referência da heurística), os dados não têm faltantes, não há variável de horário e o agente só calcula um destino por vez.
- **Ainda falta:** preencher `AUTORES_PREENCHER.md`, escrever o relatório em PDF e corrigir o `MAPA_DO_GRAFO.md` (ainda diz 10 km/h).
