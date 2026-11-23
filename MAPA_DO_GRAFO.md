# Grafo do Carrinho IESB — versão 4 — corredores e pátio

Referência: `referencias/iesb_planta_terreo_2026-11-12.png`, enviada em 12/11/2026. O usuário confirmou usar os acessos desta planta para Pátio/Direito, Design, Bloco C e Bloco B.

## Convenções

- Cada sala, banheiro e local nomeado na planta é um nó. Mesa 1 a Mesa 4 são os quatro pontos pedidos para o Pátio/Direito.
- Os corredores e pontos do eixo principal também são nós, para representar as ligações entre locais.
- Cada ligação tem custo em **metros estimados**, conforme autorização do usuário em 14/11/2026. O cálculo do tempo usa velocidade constante configurável, padrão 10 km/h. As estimativas não são medições de campo.
- A heurística do A* usa a diferença absoluta entre as distâncias de cada local até a Entrada Principal. Essas distâncias são calculadas com custo uniforme antes das consultas. Pela desigualdade triangular, a heurística não supera o custo restante no grafo e é consistente.
- As ligações representam a circulação simplificada da planta. Antes de usar o trajeto no espaço físico, o grupo deve conferir portas, largura e obstáculos no local.

## Nós propostos

| Área | Nós |
| --- | --- |
| Eixo principal | Entrada Principal; Eixo - Norte; Eixo - Design; Eixo - Bloco C; Eixo - Bloco B; Eixo - Fundo |
| Pátio/Direito | Pátio/Direito; Mesa 1; Mesa 2; Mesa 3; Mesa 4; Sala dos Professores; Café Mania; Easy Smart; Pátio - A; Pátio - B; Pátio - D; WC Acessível Pátio; WC Feminino Pátio |
| Cinema e Biblioteca | Cinema; WC Cinema; Anexo Creche; Biblioteca |
| Design | Design; Corredor Design; D-01 a D-06; WC Masculino Design; WC Feminino Design |
| Bloco C | Bloco C; Corredor Bloco C; C-01 a C-06; WC Masculino C; WC Feminino C |
| Bloco B | Bloco B; Corredor Bloco B; B-01 a B-06; WC Masculino B; WC Feminino B |
| Blocos I/J | Acesso Lateral I/J; Corredor I/J; Bloco I; Bloco J; I-01 a I-06; J-01 a J-06; WC Masculino I; WC Feminino I; WC Masculino J; WC Feminino J |
| Pontos adicionais de circulação | Três por corredor de Design/C/B (03/06, 02/05, 01/04) e oito em I/J (três grupos de salas e um de banheiros por bloco), listados na tabela de ligações |

**Total atual: 90 nós e 90 ligações bidirecionais, com um ciclo no pátio.** A lista exata das ligações está na célula `LIGACOES` do notebook. Os nomes dos blocos são pontos de destino ligados ao corredor correspondente.

## Leituras que precisam de conferência

### Confirmações do usuário na revisão da circulação

- O pátio é aberto. O usuário confirmou circulação pelo chão nos quatro lados do esboço, mas relatou muitas mesas e cadeiras. As ligações são possibilidades condicionadas ao espaço disponível; posições das quatro mesas e distâncias são didáticas, não medidas.
- As duas lanchonetes são Easy Smart e Café Mania, lado a lado no canto superior direito informado pelo usuário. Ambas se ligam ao ponto B no desenho didático; sua ordem exata e a posição dos balcões não foram medidas. Oasis Smart era o nome incorreto de Easy Smart. Gastro foi retirado a pedido do usuário, sem presumir que seja o nome antigo de Café Mania.
- Não há entrada direta do pátio para o bloco Design: é necessário sair para o eixo principal e acessar o corredor de Design por esse lado. O caminho cadastrado `Pátio/Direito → Eixo - Norte → Eixo - Design → Corredor Design` já respeita essa restrição. Não acrescentar ligação direta entre pátio e Design com base nos símbolos da imagem antiga.
- Os corredores de Design, C, B e I/J permitem andar entre portas sem voltar à entrada do bloco. A representação atual já foi subdividida em trechos, conforme descrito abaixo.
- O usuário confirmou que a posição e a ordem das salas de Design, C, B e I/J na imagem antiga apresentada correspondem ao campus atual. Essa confirmação orienta a subdivisão dos corredores; não fornece medidas exatas entre portas.
- A faixa externa à esquerda de Design, C e B na imagem antiga apresentada é inacessível e deve ser excluída da circulação. Não cadastrar saída por essa faixa nem ligação externa entre os blocos por ela. O grafo atual não contém essa passagem, portanto nenhuma ligação foi removida. Essa faixa não é o `Acesso Lateral I/J`, localizado do outro lado do eixo.

### Dúvidas restantes

- A segunda sala do Bloco C aparece como **D-02** na planta; foi cadastrada como **C-02**, seguindo a sequência C-01 a C-06.
- O texto “WC · Anexo Creche” foi separado em dois nós, pois são dois locais nomeados, mas a divisão física não está clara na planta.
- Sala dos Professores e banheiros do pátio mantêm as ligações agregadas anteriores; suas posições e portas ainda não foram detalhadas.
- A planta agrupa a circulação dos Blocos I e J num corredor contínuo. O nó `Corredor I/J` representa a chegada do acesso lateral, com pontos sucessivos para os grupos de portas.

### Subdivisão dos corredores — aplicada ao notebook

Usar pontos de passagem ao longo do corredor, mantendo as salas como destinos ligados a esses pontos. Para esta primeira proposta, portas na mesma faixa longitudinal são agrupadas em um ponto: isso não afirma que estejam perfeitamente alinhadas. Os comprimentos estimados estão na tabela, substituindo os antigos custos que retornavam ao ponto único.

- Design, C e B: manter o nó de corredor existente junto ao acesso pelo eixo e acrescentar três pontos por bloco. Do acesso para o fundo: ponto das salas 03/06, ponto das salas 02/05 e ponto das salas 01/04. Cada sala se liga ao ponto correspondente. Banheiros e nó de referência do bloco mantêm suas ligações atuais junto ao acesso nesta proposta.
- I/J: manter o nó `Corredor I/J` na chegada do acesso lateral e acrescentar oito pontos. Ordem longitudinal proposta de cima para baixo: I-01/I-04, I-02/I-05, I-03/I-06, banheiros I, chegada do acesso lateral, J-01/J-04, J-02/J-05, J-03/J-06, banheiros J. Os nomes Bloco I e Bloco J mantêm suas ligações ao nó de referência existente.
- Não acrescentar passagem pela lateral externa esquerda nem ligação direta entre pátio e Design. Pátio e demais áreas permanecem como estão nesta contagem provisória.

Contagem implementada somente para esta subdivisão: 9 pontos novos nos três blocos horizontais + 8 em I/J = 17 nós adicionais. Partindo dos 70 nós e 69 ligações anteriores, são **87 nós e 86 ligações bidirecionais**. As ligações das salas são remanejadas, não duplicadas. A subdivisão conserva uma árvore; melhora a representação dos percursos internos, mas não cria caminhos alternativos. Essa foi a contagem intermediária; a atualização do pátio acrescentou três nós e quatro ligações líquidas, totalizando 90/90.

## Papel de cada parte

### Pátio incorporado — circulação condicionada aos móveis

O nó Pátio/Direito representa C no circuito. Foram acrescentados A, B e D. Cada mesa se liga a um desses pontos por ramal estimado de 2 m; Easy Smart e Café Mania se ligam a B, por 2 m e 4 m. O acesso ao eixo preserva a ligação anterior com C, estimada em 27,5 m. Os demais apoios mantêm as ligações antigas com C até revisão específica.

Diagrama sem escala; pontos e posições de mesas são uma discretização didática do espaço aberto. Cada trecho precisa estar fisicamente disponível para ser utilizado.

```text
                          [Easy Smart] [Café Mania]
                                 \      /
                                  B
    A --------- 20 m ------------ B
    |                             |
   18 m     Mesa 1/A  Mesa 2/B    18 m
    |       Mesa 3/D  Mesa 4/C     |
    D --------- 24 m ------------ C -- eixo principal
                            (Pátio/Direito)
```

O cenário sintético `cadeiras_no_patio` modela atraso em A–B. Ele não detecta obstáculos nem trata bloqueios intransponíveis como simples atrasos: uma passagem totalmente bloqueada precisa ser excluída do grafo antes da consulta. Não há implementação de percepção ou controle físico.

O acesso ao Design continua exclusivamente pelo eixo principal. A faixa externa esquerda dos blocos continua excluída. Gastro e sua antiga ligação foram removidos; Café Mania tem uma ligação própria junto a Easy Smart. A contagem 90/90 foi conferida na execução local.

O **LLM** lê a pergunta e, na etapa final do notebook, escolhe se chama `ferramenta_do_trio` ou `listar_vizinhos`. O **A\*** recebe a origem e o destino já definidos e calcula o caminho de menor distância estimada em metros no grafo. O LLM não calcula o caminho e o A* não interpreta a pergunta em linguagem natural.

## Método das estimativas

Referência: planta enviada em 12/11/2026. As medidas são estimativas, não levantamento topográfico.

- Eixo principal: 210 m divididos em 60 + 48 + 39 + 39 + 24 m, usando aproximadamente a posição vertical dos acessos no desenho.
- Pátio: AB=20 m, BC=18 m, CD=24 m e DA=18 m; ramais de 2 m para mesas e Easy Smart, 4 m para Café Mania. São comprimentos de percurso estimados, não lados medidos de um retângulo. Apoios mantêm as estimativas anteriores. Não foram inferidas passagens adicionais por pixels.
- Design, C e B: corredor dividido em três intervalos estimados de 10 m a partir do acesso; ramais de 2 m para as salas. Banheiros mantêm os 4/7 m anteriores junto ao acesso. O corredor representado ocupa 30 m dentro da referência geral de 40 m; não se pretende medir a fachada inteira com a linha de circulação.
- I/J: posições estimadas -35, -25, -15 e -5 m para os grupos do I; chegada lateral em 0; grupos do J em 10, 20, 30 e 35 m. Os 70 m entre os extremos cabem na referência geral aproximada de 75 m. Cada ramal até sala/banheiro tem 2 m. Acesso lateral mantido em 12 m. São hipóteses de distância, não medições de portas.
- Cinema/Biblioteca e apoios: estimativas de circulação compatíveis com a disposição do desenho, sem medir portas individualmente. A biblioteca recebe 60 m, incluindo deslocamento ao norte e passagem até sua entrada.

O croqui tem proporções inconsistentes entre áreas; não se aplica uma única escala de pixels a todo o mapa. Os nós que têm apenas o nome do bloco são pontos de referência a 1 m do nó de acesso do corredor. Em cada tupla abaixo, o terceiro número é o comprimento estimado do trecho. As conexões continuam bidirecionais. O rótulo D-02 do Bloco C continua cadastrado provisoriamente como C-02.

A menor distância também tem o menor tempo neste cálculo porque a velocidade é constante em todas as ligações. A velocidade constante aplicada igualmente a todas as arestas não muda a rota mínima; custos aprendidos por trecho podem mudar a escolha no ciclo do pátio.

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
| Pátio - A | Pátio - B | 20 |
| Pátio - B | Pátio/Direito | 18 |
| Pátio/Direito | Pátio - D | 24 |
| Pátio - D | Pátio - A | 18 |
| Pátio - A | Mesa 1 | 2 |
| Pátio - B | Mesa 2 | 2 |
| Pátio - D | Mesa 3 | 2 |
| Pátio/Direito | Mesa 4 | 2 |
| Pátio - B | Easy Smart | 2 |
| Pátio - B | Café Mania | 4 |
| Pátio/Direito | Sala dos Professores | 15 |
| Pátio/Direito | WC Acessível Pátio | 40 |
| Pátio/Direito | WC Feminino Pátio | 35 |
| Cinema | WC Cinema | 20 |
| Cinema | Anexo Creche | 25 |
| Corredor Design | Corredor Design - 03/06 | 10 |
| Corredor Design - 03/06 | D-03 | 2 |
| Corredor Design - 03/06 | D-06 | 2 |
| Corredor Design - 03/06 | Corredor Design - 02/05 | 10 |
| Corredor Design - 02/05 | D-02 | 2 |
| Corredor Design - 02/05 | D-05 | 2 |
| Corredor Design - 02/05 | Corredor Design - 01/04 | 10 |
| Corredor Design - 01/04 | D-01 | 2 |
| Corredor Design - 01/04 | D-04 | 2 |
| Corredor Design | WC Masculino Design | 4 |
| Corredor Design | WC Feminino Design | 7 |
| Corredor Bloco C | Corredor Bloco C - 03/06 | 10 |
| Corredor Bloco C - 03/06 | C-03 | 2 |
| Corredor Bloco C - 03/06 | C-06 | 2 |
| Corredor Bloco C - 03/06 | Corredor Bloco C - 02/05 | 10 |
| Corredor Bloco C - 02/05 | C-02 | 2 |
| Corredor Bloco C - 02/05 | C-05 | 2 |
| Corredor Bloco C - 02/05 | Corredor Bloco C - 01/04 | 10 |
| Corredor Bloco C - 01/04 | C-01 | 2 |
| Corredor Bloco C - 01/04 | C-04 | 2 |
| Corredor Bloco C | WC Masculino C | 4 |
| Corredor Bloco C | WC Feminino C | 7 |
| Corredor Bloco B | Corredor Bloco B - 03/06 | 10 |
| Corredor Bloco B - 03/06 | B-03 | 2 |
| Corredor Bloco B - 03/06 | B-06 | 2 |
| Corredor Bloco B - 03/06 | Corredor Bloco B - 02/05 | 10 |
| Corredor Bloco B - 02/05 | B-02 | 2 |
| Corredor Bloco B - 02/05 | B-05 | 2 |
| Corredor Bloco B - 02/05 | Corredor Bloco B - 01/04 | 10 |
| Corredor Bloco B - 01/04 | B-01 | 2 |
| Corredor Bloco B - 01/04 | B-04 | 2 |
| Corredor Bloco B | WC Masculino B | 4 |
| Corredor Bloco B | WC Feminino B | 7 |
| Corredor I/J - I-01/04 | I-01 | 2 |
| Corredor I/J - I-01/04 | I-04 | 2 |
| Corredor I/J - I-01/04 | Corredor I/J - I-02/05 | 10 |
| Corredor I/J - I-02/05 | I-02 | 2 |
| Corredor I/J - I-02/05 | I-05 | 2 |
| Corredor I/J - I-02/05 | Corredor I/J - I-03/06 | 10 |
| Corredor I/J - I-03/06 | I-03 | 2 |
| Corredor I/J - I-03/06 | I-06 | 2 |
| Corredor I/J - I-03/06 | Corredor I/J - WC I | 10 |
| Corredor I/J - WC I | WC Masculino I | 2 |
| Corredor I/J - WC I | WC Feminino I | 2 |
| Corredor I/J - WC I | Corredor I/J | 5 |
| Corredor I/J | Corredor I/J - J-01/04 | 10 |
| Corredor I/J - J-01/04 | J-01 | 2 |
| Corredor I/J - J-01/04 | J-04 | 2 |
| Corredor I/J - J-01/04 | Corredor I/J - J-02/05 | 10 |
| Corredor I/J - J-02/05 | J-02 | 2 |
| Corredor I/J - J-02/05 | J-05 | 2 |
| Corredor I/J - J-02/05 | Corredor I/J - J-03/06 | 10 |
| Corredor I/J - J-03/06 | J-03 | 2 |
| Corredor I/J - J-03/06 | J-06 | 2 |
| Corredor I/J - J-03/06 | Corredor I/J - WC J | 5 |
| Corredor I/J - WC J | WC Masculino J | 2 |
| Corredor I/J - WC J | WC Feminino J | 2 |
