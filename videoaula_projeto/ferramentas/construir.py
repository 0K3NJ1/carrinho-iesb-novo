"""Gera a narração (Piper, local) e a linha do tempo de cada capítulo.

Uso: python ferramentas/construir.py [numeros dos capítulos...]
Saída: cache/linha_capNN.json e audio/capNN.wav (narração do capítulo, já com pausas).
Os áudios de cada frase ficam em cache/frases/ (reaproveitados se o texto não mudar).
"""
import hashlib
import importlib.util
import json
import re
import sys
import wave
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from codigo import colorir  # noqa: E402

FPS = 30
TAXA = 22050
VOZ = RAIZ / 'vozes' / 'pt_BR-faber-medium.onnx'
ESCALA = 1.07          # >1 deixa a fala mais lenta (ritmo de aula)
PAUSA_FRASE = 0.32
PAUSA_BLOCO = 0.45

# ---------------- pronúncia ----------------
# Só para o áudio: a legenda mantém o texto original.
TERMOS = [
    (r'\bA\*', 'A estrela'), (r'\bUCS\b', 'u cê ésse'), (r'\bIESB\b', 'i é ésse bê'), (r'\bLLM\b', 'éle éle ême'),
    (r'\bQwen2\.5-1\.5B-Instruct\b', 'Cuén dois ponto cinco, de um ponto cinco bilhão de parâmetros'),
    (r'\bQwen\b', 'Cuén'), (r'\bJSON\b', 'djêison'), (r'\bPython\b', 'Páiton'), (r'\bColab\b', 'Coláb'),
    (r'\bGPU\b', 'gê pê u'), (r'\bCPU\b', 'cê pê u'), (r'\bT4\b', 'tê quatro'), (r'\bRTX 4050\b', 'érre tê xis quarenta e cinquenta'),
    (r'\bCSV\b', 'cê ésse vê'), (r'\bPNG\b', 'pê ene gê'), (r'\bMAE\b', 'ême a é'), (r'\bRMSE\b', 'érre ême ésse é'),
    (r'\bR²', 'érre dois'), (r'\bNumPy\b', 'nâmpai'), (r'\bnumpy\b', 'nâmpai'), (r'\bpandas\b', 'pândas'),
    (r'\bscikit-learn\b', 'sáiquit lârn'), (r'\bsklearn\b', 'ésse cá lârn'), (r'\bPyTorch\b', 'pai tórtch'), (r'\btorch\b', 'tórtch'),
    (r'\btransformers\b', 'transfórmers'), (r'\bMatplotlib\b', 'mét plót lib'), (r'\bmatplotlib\b', 'mét plót lib'),
    (r'\bPygments\b', 'pigments'), (r'\bPlaywright\b', 'plêi ráit'), (r'\bHugging Face\b', 'râguin feice'),
    (r'\bkm/h\b', 'quilômetros por hora'), (r'\bms\b', 'milissegundos'),
    (r'\bf\(n\)', 'éfe de ene'), (r'\bg\(n\)', 'gê de ene'), (r'\bh\(n\)', 'agá de ene'),
    (r'\bO\(', 'ó de '), (r'\bI/J\b', 'i jota'), (r'Pátio/Direito', 'Pátio Direito'),
    (r'\btool_call\b', 'túl cól'), (r'\btool\b', 'túl'), (r'\btokens\b', 'tôquens'), (r'\btoken\b', 'tôquen'),
    (r'\btokenizador\b', 'toquenizador'), (r'\bprompt\b', 'prômpt'), (r'\bprompts\b', 'prômpts'),
    (r'\bpipeline\b', 'páipláin'), (r'\bPipeline\b', 'páipláin'), (r'\bdataset\b', 'dêita sét'),
    (r'\bnotebook\b', 'nôutbuk'), (r'\bdefault\b', 'difólt'), (r'\bfold\b', 'fôuld'), (r'\bfolds\b', 'fôulds'),
    (r'\bone-hot\b', 'uân rót'), (r'\bheap\b', 'rip'), (r'\bheapq\b', 'rip quiú'), (r'\bNetworkX\b', 'nétuork éx'),
    (r'\bhardware\b', 'rárduer'), (r'\bsoftware\b', 'sóftuer'), (r'\bonline\b', 'onláin'), (r'\bchat\b', 'tchét'),
]
CODIGO = {  # palavras de Python lidas em português aproximado
    'def': 'déf', 'return': 'ritârn', 'while': 'uáiou', 'for': 'fór', 'if': 'ífi', 'elif': 'élif', 'else': 'élse',
    'True': 'trú', 'False': 'fóls', 'None': 'nân', 'break': 'brêik', 'continue': 'contíniu', 'in': 'in',
    'not': 'nót', 'and': 'énd', 'or': 'ór', 'import': 'ímport', 'from': 'frôm', 'as': 'és', 'lambda': 'lâmbda',
    'try': 'trái', 'except': 'écsépt', 'raise': 'rêiz', 'assert': 'assért', 'global': 'glôbal', 'with': 'uít',
    'print': 'prínt', 'input': 'ínput', 'strip': 'strípe', 'lower': 'lôuer', 'append': 'apênd', 'remove': 'rimúv',
    'split': 'splít', 'join': 'djóin', 'replace': 'riplêis', 'min': 'mín', 'max': 'máx', 'abs': 'ábis', 'len': 'lén',
    'range': 'rêindj', 'sum': 'sâm', 'sorted': 'sórted', 'enumerate': 'enúmereit', 'zip': 'zíp', 'dict': 'díct',
    'list': 'líst', 'set': 'sét', 'str': 'éstr', 'int': 'int', 'float': 'flôut', 'isinstance': 'iz ínstans',
    'get': 'guét', 'items': 'áitens', 'keys': 'quíis', 'copy': 'cópi', 'extend': 'ecstênd', 'startswith': 'stárts uít',
    'isdigit': 'iz dídjit', 'normalize': 'nórmalaiz', 'category': 'catégori', 'findall': 'faind ól', 'sub': 'sâb',
    'search': 'sârtch', 'loads': 'lôuds', 'dumps': 'dâmps', 'find': 'fáind', 'rfind': 'érre fáind',
    'get_close_matches': 'guét clôuz métches', 'perf_counter': 'pérf cáunter', 'median': 'mídian',
    'fit': 'fít', 'predict': 'pridíct', 'generate': 'djênereit', 'decode': 'dicôud', 'self': 'sélf',
    'apply_chat_template': 'apláy tchét têmpleit', 'from_pretrained': 'frôm pritrêind', 'eval': 'ivál',
    'no_grad': 'nô grád', 'cuda': 'cúda', 'is_available': 'iz aveilabou', 'mkdir': 'méique dír', 'to_csv': 'tu cê ésse vê',
    'iterrows': 'íter rôus', 'groupby': 'grúp bai', 'nlargest': 'ene lárdjest', 'drop_duplicates': 'dróp dúplicats',
    'cross_val_predict': 'crós vál pridíct', 'random': 'rândom', 'gauss': 'gáus', 'choice': 'tchóis', 'randint': 'rândint',
    'np': 'ene pê', 'plt': 'pê éle tê', 're': 'érre é', 'pd': 'pê dê', 'ipynb': 'ai pai ene bê', 'json': 'djêison',
    'LinearRegression': 'línear rigréchon', 'DecisionTreeRegressor': 'dissíjon tri rigrésor', 'ValueError': 'válio érror',
    'StandardScaler': 'stândard squêiler', 'OneHotEncoder': 'uân rót encôder', 'SimpleImputer': 'símpou impiúter',
    'ColumnTransformer': 'cólam transfórmer', 'GroupKFold': 'grup quêi fôuld', 'GroupShuffleSplit': 'grup xâfou splít',
    'DataFrame': 'dêita frêim', 'Random': 'rândom', 'AutoTokenizer': 'ôuto toquenáizer', 'eos': 'i ó ésse',
    'AutoModelForCausalLM': 'ôuto módel for cáusal éle ême', 'float16': 'flôut dezesseis', 'float32': 'flôut trinta e dois',
    'enum': 'ênum', 'assistant': 'assístant', 'system': 'sístem', 'user': 'iúzer', 'add_generation_prompt': 'éd djeneréichon prômpt',
    'return_tensors': 'ritârn ténsors', 'max_tokens': 'máx tôquens', 'do_sample': 'du sêmpou', 'get_json_schema': 'guét djêison squíma',
    'make_pipeline': 'mêique páipláin', 'drop': 'dróp', 'unicodedata': 'iúnicôud dêita', 'difflib': 'dif lib',
    'statistics': 'statístics', 'pathlib': 'péth lib', 'Path': 'péth', 'time': 'táim', 'tool_call': 'túl cól',
    'tools': 'túls', 'generation_config': 'djeneréichon config', 'eos_token_id': 'i ó ésse tôquen ai dí', 'shape': 'xêip',
    'PONTOS_IJ': 'pontos i jota', 'input_ids': 'ínput ai dís', 'skip_special_tokens': 'squíp spécial tôquens', 'maximum': 'mácsimum', 'predict_proba': 'pridíct',
}
SIGLAS_OK = {'IESB', 'JSON', 'SAIR', 'MAE', 'RMSE', 'CSV', 'PNG', 'GPU', 'CPU', 'LLM', 'UCS', 'API', 'NFD', 'WC'}


def _identificador(m):
    w = m.group(0)
    if w in CODIGO:
        return CODIGO[w]
    if w.isupper() and len(w) > 3 and w not in SIGLAS_OK:       # LOCAIS, DISTANCIA_ENTRADA: lidos como palavras
        w = w.lower()
    return w.replace('_', ' ')


def para_fala(texto):
    texto = re.sub(r'\{([^|{}]*)\|([^{}]*)\}', r'\2', texto)        # {legenda|fala}

    def trecho(m):
        t = m.group(1)
        t = t.replace('#@param', ' cerquilha arroba param ')
        t = re.sub(r'(\d)\.(\d)', r'\1,\2', t)                       # 0.8 -> 0,8 (antes do "ponto")
        t = t.replace('==', ' igual igual ').replace('!=', ' diferente de ').replace('<=', ' menor ou igual a ')
        t = t.replace('>=', ' maior ou igual a ').replace('->', ' seta ').replace('()', '').replace('**', ' dois asteriscos ')
        t = t.replace(' - ', ' menos ').replace(' + ', ' mais ')
        t = re.sub(r'\.(?=[A-Za-z_])', ' ponto ', t)
        t = re.sub(r'[A-Za-z_][A-Za-z0-9_]*', _identificador, t)
        t = t.replace('[', ' ').replace(']', ' ').replace('(', ' ').replace(')', ' ')
        t = t.replace('"', ' ').replace("'", ' ').replace('{', ' ').replace('}', ' ').replace(':', ' ').replace('=', ' igual ')
        return t
    texto = re.sub(r'`([^`]+)`', trecho, texto)
    texto = re.sub(r'\b([A-Z][A-Z_]{3,})\b', lambda m: m.group(1) if m.group(1) in SIGLAS_OK else m.group(1).lower().replace('_', ' '), texto)
    for padrao, troca in TERMOS:
        texto = re.sub(padrao, troca, texto)
    texto = re.sub(r'\b(' + '|'.join(re.escape(k) for k in ['strip', 'lower', 'while', 'return', 'print', 'input']) + r')\b',
                   lambda m: CODIGO[m.group(1)], texto)
    texto = re.sub(r'\bWC\b', 'dáblio cê', texto)
    texto = re.sub(r'\bAPI\b', 'a pê i', texto)
    texto = re.sub(r'\bNFD\b', 'ene éfe dê', texto)
    texto = re.sub(r'(\d)\.(\d)', r'\1,\2', texto)
    texto = re.sub(r'\b([A-Z])-0?(\d)\b', r'\1 \2', texto)          # B-04 -> B 4
    texto = re.sub(r'\b0?(\d)/0?(\d)\b', r'\1 e \2', texto)           # 03/06 -> 3 e 6 (antes de trocar a barra)
    texto = texto.replace('**', '').replace('→', ' vira ').replace('×', ' vezes ').replace('≤', ' menor ou igual a ')
    texto = texto.replace('≥', ' maior ou igual a ').replace('—', ', ').replace('/', ' barra ').replace('*', ' vezes ')
    texto = texto.replace('⇒', ' então ').replace('≈', ' aproximadamente ').replace('·', ', ')
    return re.sub(r'\s+', ' ', texto).strip()


def para_legenda(texto):
    return re.sub(r'\{([^|{}]*)\|([^{}]*)\}', r'\1', texto)


def frases_de(fala):
    """Divide a narração em frases (cada uma vira uma legenda)."""
    partes = re.split(r'(?<=[.!?…])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÀÇ`"“(0-9*{])', fala.strip())
    saida = []
    for p in partes:
        while len(para_legenda(p)) > 175:
            corte = None
            for sep in ['; ', ': ', ', ', ' e ']:
                pos = [m.start() for m in re.finditer(re.escape(sep), p) if 60 < m.start() < 165]
                if pos:
                    corte = pos[-1] + len(sep)
                    break
            if corte is None:
                break
            saida.append(p[:corte].strip())
            p = p[corte:].strip()
        saida.append(p)
    saida = [s for s in saida if s]
    # frases muito curtas ("Volta 4.") ficam junto da seguinte, para a legenda não piscar
    juntas = []
    for s in saida:
        if juntas and len(para_legenda(juntas[-1])) < 28 and len(para_legenda(juntas[-1] + ' ' + s)) <= 175:
            juntas[-1] = juntas[-1] + ' ' + s
        else:
            juntas.append(s)
    return juntas


# ---------------- áudio ----------------
_VOZ = None


def sintetizar(texto):
    global _VOZ
    chave = hashlib.sha1(f'{VOZ.name}|{ESCALA}|{texto}'.encode()).hexdigest()[:16]
    arq = RAIZ / 'cache' / 'frases' / f'{chave}.wav'
    if not arq.exists():
        from piper import PiperVoice, SynthesisConfig
        if _VOZ is None:
            _VOZ = PiperVoice.load(str(VOZ))
        arq.parent.mkdir(parents=True, exist_ok=True)
        cfg = SynthesisConfig(length_scale=ESCALA, noise_scale=0.6, noise_w_scale=0.8)
        with wave.open(str(arq), 'wb') as w:
            _VOZ.synthesize_wav(texto, w, syn_config=cfg)
    with wave.open(str(arq), 'rb') as w:
        dados = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    return dados, arq


# ---------------- cenas ----------------
def identidade(v):
    t = v['tipo']
    if t == 'dividido':
        return f"div({identidade(v['esquerda'])},{identidade(v['direita'])})"
    if t == 'vertical':
        return f"vert({identidade(v['cima'])},{identidade(v['baixo'])})"
    chave = {'codigo': v.get('celula', v.get('titulo')), 'grafo': '', 'pergunta': v.get('numero'),
             'imagem': v.get('src')}.get(t, v.get('titulo'))
    return f'{t}:{chave}'


def marcar_cena(v, cena):
    v['cena'] = cena
    if v['tipo'] == 'dividido':
        marcar_cena(v['esquerda'], cena + '.e')
        marcar_cena(v['direita'], cena + '.d')
    if v['tipo'] == 'vertical':
        marcar_cena(v['cima'], cena + '.c')
        marcar_cena(v['baixo'], cena + '.b')


def preparar_visual(v):
    if v['tipo'] == 'codigo' and 'livre_fonte' in v:
        v['livre'] = colorir(v.pop('livre_fonte'))
    for lado in ['esquerda', 'direita', 'cima', 'baixo']:
        if lado in v:
            preparar_visual(v[lado])
    return v


def carregar_capitulo(numero):
    arq = sorted((RAIZ / 'roteiro').glob(f'cap{numero:02d}_*.py'))[0]
    spec = importlib.util.spec_from_file_location(arq.stem, arq)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(RAIZ / 'roteiro'))
    spec.loader.exec_module(mod)
    return mod.CAPITULO, arq


def construir(numero):
    cap, arq = carregar_capitulo(numero)
    blocos, faixa, anterior, cena, ident_ant = [], [], None, 0, None
    import copy
    for b in cap['blocos']:
        visual = copy.deepcopy(b['visual']) if b['visual'] is not None else copy.deepcopy(anterior)
        visual = preparar_visual(visual)
        ident = identidade(visual)
        if ident != ident_ant or visual['tipo'] == 'titulo' or visual.get('nova'):
            cena += 1
        marcar_cena(visual, f'c{cena}')
        mesma = ident == ident_ant and visual['tipo'] != 'titulo'
        anim = b['anim'] if b['anim'] is not None else (0.7 if mesma else 1.0)
        trans = max(1, round(anim * FPS))
        frases = []
        for i, frase in enumerate(frases_de(b['fala'])):
            audio, arq_audio = sintetizar(para_fala(frase))
            dur = len(audio) / TAXA
            pausa = PAUSA_FRASE + (PAUSA_BLOCO if i == len(frases_de(b['fala'])) - 1 else 0)
            quadros = round((dur + pausa) * FPS)
            frases.append(dict(legenda=para_legenda(frase), fala=para_fala(frase), audio=arq_audio.name,
                               dur=round(dur, 3), quadros=quadros))
            faixa.append((audio, quadros))
        if frases[0]['quadros'] < trans + 1:          # a transição cabe dentro da primeira frase
            extra = trans + 1 - frases[0]['quadros']
            frases[0]['quadros'] += extra
            a, q = faixa[-len(frases)]
            faixa[-len(frases)] = (a, q + extra)
        blocos.append(dict(visual=visual, transicao=trans, frases=frases,
                           quadros=sum(f['quadros'] for f in frases)))
        anterior, ident_ant = b['visual'] if b['visual'] is not None else anterior, ident
    # áudio do capítulo: cada frase começa no seu quadro, com silêncio até a próxima
    total = sum(q for _, q in faixa)
    som = np.zeros(int(round(total / FPS * TAXA)) + TAXA, dtype=np.int16)
    pos = 0
    for audio, q in faixa:
        ini = int(round(pos / FPS * TAXA))
        som[ini:ini + len(audio)] = audio[: max(0, len(som) - ini)]
        pos += q
    som = som[: int(round(total / FPS * TAXA))]
    (RAIZ / 'audio').mkdir(exist_ok=True)
    with wave.open(str(RAIZ / 'audio' / f'cap{numero:02d}.wav'), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(TAXA)
        w.writeframes(som.tobytes())
    linha = dict(numero=numero, rotulo=f'Capítulo {numero}', titulo=cap['titulo'], fps=FPS,
                 quadros=total, segundos=round(total / FPS, 2), blocos=blocos, arquivo_roteiro=arq.name)
    (RAIZ / 'cache').mkdir(exist_ok=True)
    (RAIZ / 'cache' / f'linha_cap{numero:02d}.json').write_text(json.dumps(linha, ensure_ascii=False), encoding='utf-8')
    print(f'capítulo {numero}: {len(blocos)} blocos, {sum(len(b["frases"]) for b in blocos)} frases, '
          f'{total / FPS / 60:.1f} min')
    return linha


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    nums = [int(a) for a in sys.argv[1:]] or sorted(int(p.stem[3:5]) for p in (RAIZ / 'roteiro').glob('cap*_*.py'))
    for n in nums:
        construir(n)
