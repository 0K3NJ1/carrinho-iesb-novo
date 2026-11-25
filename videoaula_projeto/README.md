# Videoaula — Carrinho IESB, linha por linha

Videoaula narrada (pt-BR) que explica todo o código do notebook `../carrinho_iesb_unificado.ipynb`: Python, grafo, busca de custo uniforme, heurística, A*, Fase 2 (dados e modelos), Fase 3 (Qwen e agente), avaliação real e perguntas para a defesa.

O código original do projeto **não é modificado**: tudo aqui lê o notebook e executa cópias.

## Arquivos entregues

| arquivo | conteúdo |
|---|---|
| `Videoaula_Projeto_IESB.mp4` | vídeo completo (1920×1080, 30 fps, H.264 + AAC, com marcadores de capítulo) |
| `capitulos/capNN.mp4` | cada capítulo em separado |
| `capitulos.txt` | tempos reais de início de cada capítulo |
| `legendas.srt` | legendas sincronizadas (também aparecem dentro do vídeo) |
| `roteiro_completo.md` | toda a narração, bloco a bloco, com tempo e descrição do visual |
| `analise_codigo.md` | inventário: células, bibliotecas, funções, algoritmos, fluxo, resultados e limitações |
| `matriz_de_cobertura.md` | cada função e célula × capítulo e momento do vídeo em que é explicada |
| `perguntas_e_respostas.md` | perguntas da defesa com respostas |
| `audio/capNN.wav` | narração de cada capítulo |

### O que está no GitHub

O vídeo completo tem 315 MB e passa do limite de 100 MB por arquivo do GitHub, por isso **não está no repositório**. No GitHub estão os 16 capítulos em `capitulos/` (cada um com menos de 40 MB, juntos formam o vídeo inteiro), os documentos e todo o código que gera o vídeo.

Também ficam fora do git, porque podem ser gerados de novo:
- `audio/` (narração em WAV): `ferramentas/construir.py`
- `Videoaula_Projeto_IESB.mp4`: `ferramentas/juntar.py`
- `vozes/pt_BR-faber-medium.onnx` (60 MB): baixar `pt_BR-faber-medium.onnx` no repositório público de vozes do Piper (`rhasspy/piper-voices`, pasta `pt/pt_BR/faber/medium`) e salvar em `vozes/`
- `cache/` e `testes/`

## Como funciona

1. `ferramentas/inventario.py` — lista células, importações e funções do notebook (`dados/inventario.json`).
2. `ferramentas/codigo.py` — colore o código das células com Pygments (`dados/codigo.json`).
3. `ferramentas/tracos.py` — executa as Fases 1 e 2 do notebook numa cópia e registra cada volta real da busca e os resultados (`dados/tracos.json`).
4. `ferramentas/exemplos_agente.py` — saídas reais das funções de padronização (`dados/exemplos_agente.json`).
5. `ferramentas/layout.py` — posições **só para desenhar** o grafo (o projeto não tem coordenadas).
6. `roteiro/capNN_*.py` — o roteiro: cada `bloco(narração, visual)` é uma cena. `roteiro/base.py` tem os tipos de visual.
7. `ferramentas/construir.py` — gera a narração com **Piper** (voz local `pt_BR-faber-medium`, em `vozes/`), mede a duração real de cada frase e monta a linha do tempo (`cache/linha_capNN.json`, `audio/capNN.wav`).
8. `ferramentas/renderizar.py` — abre `motor/index.html` no Chrome (Playwright), desenha cada quadro com `desenhar(bloco, progresso, frase)` e monta o MP4 com FFmpeg. Quadros parados são capturados uma vez só e recebem a duração exata; blocos sem mudança são reaproveitados do cache.
9. `ferramentas/juntar.py` — junta os capítulos e gera `capitulos.txt`, `legendas.srt`, `roteiro_completo.md` e `matriz_de_cobertura.md`.
10. `ferramentas/documentos.py` — gera `analise_codigo.md` e `perguntas_e_respostas.md`.

Os dados reais do agente (Qwen) vêm da execução no Colab (`dados/colab_zip/`).

## Como alterar

```powershell
cd videoaula_projeto                                        # a partir da raiz do repositório
..\.venv\Scripts\python.exe ferramentas\construir.py 7        # narração do capítulo 7
..\.venv\Scripts\python.exe ferramentas\renderizar.py 7       # vídeo do capítulo 7
..\.venv\Scripts\python.exe ferramentas\juntar.py             # vídeo final e documentos
```

- **Texto falado:** edite o `bloco(...)` no arquivo do capítulo. Para trocar só a pronúncia, use `{texto da legenda|texto falado}`; termos recorrentes ficam em `TERMOS` e `CODIGO`, em `construir.py`.
- **Visual:** os tipos estão em `roteiro/base.py` (`codigo`, `grafo`, `tabela`, `fluxo`, `formula`, `transf`, `terminal`, `pergunta`, `imagem`, `dividido`...). O desenho fica em `motor/motor.js` e `motor/estilo.css`.
- **Teste rápido:** `renderizar.py 7 --ate 5` gera só os 5 primeiros blocos em `testes/`.
- **Se o notebook mudar:** rode `inventario.py`, `codigo.py`, `tracos.py` e `exemplos_agente.py` antes de construir, e confira as linhas citadas no roteiro.

Dependências (no `.venv` do projeto): `piper-tts`, `playwright` (usa o Chrome instalado), `pygments`, `numpy`, `pandas`, `scikit-learn`, `matplotlib`; e FFmpeg no PATH.
