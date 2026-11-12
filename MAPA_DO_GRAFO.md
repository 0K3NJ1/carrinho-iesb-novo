# Grafo do Carrinho IESB — versão 1

Referência: `referencias/iesb_planta_terreo_2026-11-12.png`, enviada em 12/11/2026. O usuário confirmou usar os acessos desta planta para Pátio/Direito, Design, Bloco C e Bloco B.

## Convenções

- Cada sala, banheiro e local nomeado na planta é um nó. Mesa 1 a Mesa 4 são os quatro pontos pedidos para o Pátio/Direito.
- Os corredores e pontos do eixo principal também são nós, para representar as ligações entre locais.
- Cada ligação tem custo **1 trecho**. O desenho não informa a distância de cada porta/mesa; o custo não representa metros nem tempo.
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
- A planta agrupa a circulação dos Blocos I e J num corredor contínuo. Este grafo usa um único nó `Corredor I/J`, sem tentar representar distâncias internas.

## Papel de cada parte

O **LLM** lê a pergunta e, na etapa final do notebook, escolhe se chama `ferramenta_do_trio` ou `listar_vizinhos`. O **A\*** recebe a origem e o destino já definidos e calcula o caminho de menor número de trechos no grafo. O LLM não calcula o caminho e o A* não interpreta a pergunta em linguagem natural.
