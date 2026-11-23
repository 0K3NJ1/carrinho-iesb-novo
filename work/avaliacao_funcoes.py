# Funções incorporadas à seção 9 do notebook; sem classes próprias.
import re
import unicodedata


def normalizar_argumentos(nome, argumentos):
    if not isinstance(argumentos, dict):
        return None
    normalizados = argumentos.copy()
    if nome == 'rota_tempo_previsto':
        normalizados.setdefault('cenario', 'tranquilo')
    # Preserva parâmetros extras: ignorá-los esconderia um erro do LLM.
    return normalizados


def preparar_resultado_esperado(caso):
    nome, argumentos = caso['ferramenta'], caso['argumentos']
    if nome is None:
        return None, dict(caminho=[], vizinhos=[], valores=[], sintetico=False)
    resultado = executar({'name': nome, 'arguments': argumentos})
    assert not resultado.startswith('Erro:'), 'Referência inválida: ' + str(caso['id'])
    referencia = dict(caminho=[], vizinhos=[], valores=[], sintetico=False)
    if nome == 'listar_vizinhos':
        referencia['vizinhos'] = [v for v, _ in VIZINHOS[argumentos['local']]]
    else:
        grafo = prever_grafo_tempo(argumentos.get('cenario', 'tranquilo'))
        referencia['sintetico'] = True
        # Custo uniforme como referência independente da heurística do A*.
        caminho, custo, _ = buscar(argumentos['origem'], argumentos['destino'], grafo, False)
        # Casos que pedem apenas tempo não exigem enumeração de todo o trajeto.
        referencia['caminho'] = caminho if caso.get('exigir_caminho', True) else []
        metros = sum(dict(VIZINHOS[a])[b] for a, b in zip(caminho, caminho[1:]))
        referencia['valores'] = [f'{custo:.1f} s']
        if caso.get('exigir_caminho', True):
            referencia['valores'].append(f'{metros:.1f} m')
    return resultado, referencia


def normalizar_texto(texto):
    texto = unicodedata.normalize('NFD', texto.lower())
    texto = ''.join(letra for letra in texto if unicodedata.category(letra) != 'Mn')
    texto = texto.replace(',', '.')
    texto = re.sub(r'\b(metros?|segundos?)\b', lambda m: 'm' if m[0].startswith('metro') else 's', texto)
    return ' '.join(texto.split())


def conferir_conteudo(resposta, referencia):
    # Triagem literal conservadora; a revisão humana continua obrigatória.
    texto = normalizar_texto(resposta)
    posicao = 0
    for local in referencia['caminho']:
        achado = texto.find(normalizar_texto(local), posicao)
        if achado < 0:
            return False
        posicao = achado + len(normalizar_texto(local))
    if not all(normalizar_texto(v) in texto for v in referencia['vizinhos']):
        return False
    for valor in referencia['valores']:
        numero, unidade = valor.split()
        # Aceita 30 s, 30.0 s e 30,0 segundos; rejeita 130 s como se fosse 30 s.
        numero = numero[:-2] + r'(?:\.0)?' if numero.endswith('.0') else re.escape(numero)
        if re.search(r'(?<![\d.])' + numero + r'\s*' + unidade + r'\b', texto) is None:
            return False
    return not referencia['sintetico'] or any(p in texto for p in ['sintetic', 'fictici'])


def avaliar_caso(caso):
    inicio = perf_counter()
    erro = None
    try:
        detalhes = agente(caso['pergunta'], mostrar=False, retornar_detalhes=True)
    except Exception as falha:
        detalhes = {'resposta': '', 'chamadas': [], 'status': 'erro'}
        erro = type(falha).__name__ + ': ' + str(falha)
    duracao_s = perf_counter() - inicio
    chamadas = detalhes['chamadas']
    primeira = chamadas[0] if chamadas else None
    escolhida = primeira['pedido'].get('name') if primeira else None
    recebidos = primeira['pedido'].get('arguments', {}) if primeira else {}
    ferramenta_ok = erro is None and escolhida == caso['ferramenta']
    argumentos_ok = ferramenta_ok and normalizar_argumentos(escolhida, recebidos) == normalizar_argumentos(caso['ferramenta'], caso['argumentos'])
    quantidade_ok = len(chamadas) == (0 if caso['ferramenta'] is None else 1)
    resposta = detalhes['resposta']
    terminou = bool(resposta.strip()) and detalhes['status'] in ['concluido', 'resposta_livre', 'esclarecimento']
    resultado_ok = ferramenta_ok and argumentos_ok and quantidade_ok and terminou
    if caso.get('campo_esclarecimento'):
        resultado_ok = resultado_ok and detalhes['status'] == 'esclarecimento' and (
            (detalhes.get('pendencia') or {}).get('campo') == caso['campo_esclarecimento'])
    elif caso['ferramenta'] is None:
        resultado_ok = resultado_ok and detalhes['status'] == 'resposta_livre'
    if caso['ferramenta'] is not None:
        resultado_ok = resultado_ok and primeira['resultado'] == caso['resultado_esperado']
        conteudo_ok = resultado_ok and conferir_conteudo(resposta, caso['referencia'])
    else:
        conteudo_ok = None  # Saudação e fora de escopo exigem julgamento humano.
    return dict(id=caso['id'], pergunta=caso['pergunta'], ferramenta=ferramenta_ok,
                argumentos=argumentos_ok, chamadas_esperadas=quantidade_ok,
                resultado_valido=resultado_ok, conteudo_automatico=conteudo_ok,
                resposta_fiel=None, revisao='pendente', justificativa_revisao='',
                duracao_s=duracao_s, escolhida=escolhida, recebidos=recebidos,
                chamadas=chamadas, resposta=resposta, erro=erro, status=detalhes['status'],
                tentativas=detalhes.get('tentativas', []), pendencia=detalhes.get('pendencia'),
                apresentacao_fiel=(resposta == primeira['resultado']) if primeira else None)


# Todas as referências são produzidas antes da primeira inferência da bateria.
for caso in CASOS:
    resultado, referencia = preparar_resultado_esperado(caso)
    caso['resultado_esperado'] = resultado
    caso['referencia'] = referencia
    caso['criterio_manual'] = (
        'Conferir caminho na ordem, números/unidades e ausência de locais ou fatos inventados. '
        'Em tempo aprendido, identificar dados sintéticos e não afirmar que detectou cadeiras. '
        'Em vizinhos, conferir lista sem acréscimos. Em saudação/fora de escopo, não inventar rota. '
        'Nos esclarecimentos, não escolher arbitrariamente o local nem executar a rota. '
        'Argumentos avaliados são os normalizados; pedido bruto e ajustes estão nas chamadas/tentativas.'
    )
    print(caso['id'], '|', caso['ferramenta'], '|', caso['argumentos'], '|', resultado)
