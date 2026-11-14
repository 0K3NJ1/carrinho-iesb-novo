# Grafo do Carrinho IESB — versão 2 — estimativas em metros

Referência: `referencias/iesb_planta_terreo_2026-11-12.png`, enviada em 12/11/2026. O usuário confirmou usar os acessos desta planta para Pátio/Direito, Design, Bloco C e Bloco B.

## Convenções

- Cada sala, banheiro e local nomeado na planta é um nó. Mesa 1 a Mesa 4 são os quatro pontos pedidos para o Pátio/Direito.
- Os corredores e pontos do eixo principal também são nós, para representar as ligações entre locais.
- Cada ligação tem custo em **metros estimados**, conforme autorização do usuário em 14/11/2026. O cálculo do tempo usa velocidade constante configurável, padrão 10 km/h. As estimativas não são medições de campo.
- A heurística do A* é zero, como no caso genérico do gabarito. Sem coordenadas confiáveis, isso mantém o resultado correto para o custo definido.
- As ligações representam a circulação simplificada da planta. Antes de usar o trajeto no espaço físico, o grupo deve conferir portas, largura e obstáculos no local.

## Nós propostos

| Área | Nós |
| --- | --- |
| Eixo principal | Entrada Principal; Eixo - Norte; Eixo - Design; Eixo - Bloco C; Eixo - Bloco B; Eixo - Fundo |
| Pátio/Direito | Pátio/Direito; Mesa 1; Mesa 2; Mesa 3; Mesa 4; Sala dos Professores; Gastro; Oasis Smart; WC Acessível Pátio; WC Feminino Pátio |
| Cinema e Biblioteca | Cinema; WC Cinema; Anexo Creche; Biblioteca |
| Design | Design; Corredor Design; D-01 a D-06; WC Masculino Design; WC Feminino Design |
| Bloco C | Bloco C; Corredor Bloco C; C-01 a C-06; WC Masculino C; WC Feminino C |
| Bloco B | Bloco B; Corredor Bloco B; B-01 a B-06; WC Masculino B; WC Feminino B |
| Blocos I/J | Acesso Lateral I/J; Corredor I/J; Bloco I; Bloco J; I-01 a I-06; J-01 a J-06; WC Masculino I; WC Feminino I; WC Masculino J; WC Feminino J |

**Total: 70 nós e 69 ligações bidirecionais.** A lista exata das ligações está na célula `LIGACOES` do notebook. Os nomes dos blocos são pontos de destino ligados ao corredor correspondente.

## Leituras que precisam de conferência

- A segunda sala do Bloco C aparece como **D-02** na planta; foi cadastrada como **C-02**, seguindo a sequência C-01 a C-06.
- O texto “WC · Anexo Creche” foi separado em dois nós, pois são dois locais nomeados, mas a divisão física não está clara na planta.
- “Gastro” e “Sala dos Professores” foram cadastrados como pontos do Pátio/Direito, pois não há portas individuais claras no desenho.
- A planta agrupa a circulação dos Blocos I e J num corredor contínuo. Este grafo usa um único nó `Corredor I/J`, com distâncias internas estimadas a partir desse ponto, na altura do acesso lateral. Isso pode superestimar trajetos entre salas que passam pelo ponto agregado.

## Papel de cada parte

O **LLM** lê a pergunta e, na etapa final do notebook, escolhe se chama `ferramenta_do_trio` ou `listar_vizinhos`. O **A\*** recebe a origem e o destino já definidos e calcula o caminho de menor distância estimada em metros no grafo. O LLM não calcula o caminho e o A* não interpreta a pergunta em linguagem natural.

## Método das estimativas

Referência: planta enviada em 12/11/2026. As medidas são estimativas, não levantamento topográfico.

- Eixo principal: 210 m divididos em 60 + 48 + 39 + 39 + 24 m, usando aproximadamente a posição vertical dos acessos no desenho.
- Pátio: referência 55 m até o eixo e 53 m de comprimento; ponto central a 27,5 m do eixo. Mesas colocadas por hipótese a 5, 10, 15 e 20 m desse ponto.
- Design, C e B: referência 40 × 20 m; nó do corredor próximo da entrada direita. Distâncias internas estimadas pela posição das salas ao longo dos 40 m, incluindo entrada na sala.
- I/J: referência longitudinal de aproximadamente 75 m; nó do corredor na altura do acesso lateral. A largura está “a conferir”: os 12 m do acesso e os deslocamentos laterais internos são hipóteses.
- Cinema/Biblioteca e apoios: estimativas de circulação compatíveis com a disposição do desenho, sem medir portas individualmente. A biblioteca recebe 60 m, incluindo deslocamento ao norte e passagem até sua entrada.

O croqui tem proporções inconsistentes entre áreas; não se aplica uma única escala de pixels a todo o mapa. Os nós que têm apenas o nome do bloco são pontos de referência 1 m após o corredor. Em cada tupla abaixo, o terceiro número é o comprimento estimado do trecho. As conexões continuam bidirecionais. O rótulo D-02 do Bloco C continua cadastrado provisoriamente como C-02.

A menor distância também tem o menor tempo neste cálculo porque a velocidade é constante em todas as ligações. Sem rotas alternativas, mudar a velocidade ou os pesos não muda a sequência de nós.

## Tabela completa de distâncias estimadas

| Origem | Destino | Metros estimados |
| --- | --- | ---: |
| Entrada Principal | Eixo - Norte | 60 |
| Eixo - Norte | Eixo - Design | 48 |
| Eixo - Design | Eixo - Bloco C | 39 |
| Eixo - Bloco C | Eixo - Bloco B | 39 |
| Eixo - Bloco B | Eixo - Fundo | 24 |
| Eixo - Norte | Pátio/Direito | 27.5 |
| Eixo - Norte | Cinema | 15 |
| Eixo - Norte | Biblioteca | 60 |
| Eixo - Design | Corredor Design | 5 |
| Eixo - Bloco C | Corredor Bloco C | 5 |
| Eixo - Bloco B | Corredor Bloco B | 5 |
| Eixo - Bloco C | Acesso Lateral I/J | 5 |
| Acesso Lateral I/J | Corredor I/J | 12 |
| Corredor Design | Design | 1 |
| Corredor Bloco C | Bloco C | 1 |
| Corredor Bloco B | Bloco B | 1 |
| Corredor I/J | Bloco I | 1 |
| Corredor I/J | Bloco J | 1 |
| Pátio/Direito | Mesa 1 | 5 |
| Pátio/Direito | Mesa 2 | 10 |
| Pátio/Direito | Mesa 3 | 15 |
| Pátio/Direito | Mesa 4 | 20 |
| Pátio/Direito | Sala dos Professores | 15 |
| Pátio/Direito | Gastro | 20 |
| Pátio/Direito | Oasis Smart | 30 |
| Pátio/Direito | WC Acessível Pátio | 40 |
| Pátio/Direito | WC Feminino Pátio | 35 |
| Cinema | WC Cinema | 20 |
| Cinema | Anexo Creche | 25 |
| Corredor Design | D-01 | 35 |
| Corredor Design | D-02 | 25 |
| Corredor Design | D-03 | 15 |
| Corredor Design | D-04 | 35 |
| Corredor Design | D-05 | 25 |
| Corredor Design | D-06 | 8 |
| Corredor Design | WC Masculino Design | 4 |
| Corredor Design | WC Feminino Design | 7 |
| Corredor Bloco C | C-01 | 35 |
| Corredor Bloco C | C-02 | 25 |
| Corredor Bloco C | C-03 | 15 |
| Corredor Bloco C | C-04 | 35 |
| Corredor Bloco C | C-05 | 25 |
| Corredor Bloco C | C-06 | 8 |
| Corredor Bloco C | WC Masculino C | 4 |
| Corredor Bloco C | WC Feminino C | 7 |
| Corredor Bloco B | B-01 | 35 |
| Corredor Bloco B | B-02 | 25 |
| Corredor Bloco B | B-03 | 15 |
| Corredor Bloco B | B-04 | 35 |
| Corredor Bloco B | B-05 | 25 |
| Corredor Bloco B | B-06 | 8 |
| Corredor Bloco B | WC Masculino B | 4 |
| Corredor Bloco B | WC Feminino B | 7 |
| Corredor I/J | I-01 | 37 |
| Corredor I/J | I-02 | 28 |
| Corredor I/J | I-03 | 16 |
| Corredor I/J | I-04 | 37 |
| Corredor I/J | I-05 | 29 |
| Corredor I/J | I-06 | 20 |
| Corredor I/J | J-01 | 13 |
| Corredor I/J | J-02 | 25 |
| Corredor I/J | J-03 | 36 |
| Corredor I/J | J-04 | 13 |
| Corredor I/J | J-05 | 22 |
| Corredor I/J | J-06 | 30 |
| Corredor I/J | WC Masculino I | 13 |
| Corredor I/J | WC Feminino I | 8 |
| Corredor I/J | WC Masculino J | 36 |
| Corredor I/J | WC Feminino J | 40 |
