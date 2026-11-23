# Camada de interpretação: nomes, validação e resposta direta da ferramenta.
import json
import re
import unicodedata
from difflib import SequenceMatcher


def chave_local(texto):
    if not isinstance(texto, str):
        return ''
    texto = unicodedata.normalize('NFD', texto.lower())
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    texto = re.sub(r'[^a-z0-9]+', ' ', texto)
    texto = re.sub(r'\b(?:do|da|de|dos|das)\b', ' ', texto)
    texto = re.sub(r'\bsala\s+(?=[bcdij]\s*\d)', '', texto)
    texto = re.sub(r'\b([bcdij])\s*0?([1-6])\b', r'\1 \2', texto)
    texto = re.sub(r'\bmesa\s*0?([1-4])\b', r'mesa \1', texto)
    texto = re.sub(r'\bbanheiro\b', 'wc', texto)
    texto = re.sub(r'\bfem\b', 'feminino', texto)
    texto = re.sub(r'\bmasc\b', 'masculino', texto)
    texto = re.sub(r'\b(wc\s+(?:feminino|masculino))\s+bloco\b', r'\1', texto)
    return ' '.join(texto.split())


# Somente equivalências de nomes; não acrescenta nós, portas ou acessos.
APELIDOS = {
    'biblio': ['Biblioteca'], 'bibl': ['Biblioteca'],
    'entrada': ['Entrada Principal'], 'patio': ['Pátio/Direito'],
    'cafe mania': ['Café Mania'], 'cafemania': ['Café Mania'],
    'easy': ['Easy Smart'], 'easy smart': ['Easy Smart'],
    'mesa um': ['Mesa 1'], 'mesa dois': ['Mesa 2'],
    'mesa tres': ['Mesa 3'], 'mesa quatro': ['Mesa 4'],
    'lanchonete': ['Easy Smart', 'Café Mania'],
    'cantina': ['Easy Smart', 'Café Mania'],
    'cafe': ['Easy Smart', 'Café Mania'],
    'banheiro': [n for n in LOCAIS if n.startswith('WC ')],
    'bloco': [n for n in LOCAIS if n.startswith('Bloco ')],
}
NOMES_NORMALIZADOS = {}
for nome, destinos in [(n, [n]) for n in LOCAIS] + list(APELIDOS.items()):
    lista = NOMES_NORMALIZADOS.setdefault(chave_local(nome), [])
    for destino in destinos:
        if destino not in lista:
            lista.append(destino)


def resolver_local(texto):
    chave = chave_local(texto)
    if not chave:
        return dict(local=None, opcoes=[], motivo='ausente')
    exatos = NOMES_NORMALIZADOS.get(chave, [])
    if exatos:
        return dict(local=exatos[0] if len(exatos) == 1 else None,
                    opcoes=exatos, motivo='nome_ou_apelido')
    # Nunca corrigir números de salas/mesas por semelhança nem completar bloco.
    if re.search(r'\d', chave) or len(chave) < 6:
        return dict(local=None, opcoes=[], motivo='nao_cadastrado')
    notas = {}
    for variante, locais in NOMES_NORMALIZADOS.items():
        if len(locais) != 1 or re.search(r'\d', variante):
            continue
        nota = SequenceMatcher(None, chave, variante).ratio()
        notas[locais[0]] = max(notas.get(locais[0], 0), nota)
    melhores = sorted(notas, key=notas.get, reverse=True)
    if melhores:
        primeiro = notas[melhores[0]]
        segundo = notas[melhores[1]] if len(melhores) > 1 else 0
        # Limiares heurísticos, não uma probabilidade de intenção correta.
        if primeiro >= 0.88 and primeiro - segundo >= 0.10:
            return dict(local=melhores[0], opcoes=[melhores[0]], motivo='grafia_proxima')
    opcoes = [n for n in melhores[:3] if notas[n] >= 0.65]
    return dict(local=None, opcoes=opcoes, motivo='confirmar_nome')


def resolver_cenario(texto):
    for nome, variantes in CENARIOS_ALTERNATIVOS.items():
        if chave_local(texto) in [chave_local(v) for v in variantes]:
            return nome
    return None


CENARIOS_ALTERNATIVOS = {
    'tranquilo': ['tranquilo', 'calmo', 'padrao', 'normal'],
    'movimentado': ['movimentado', 'cheio', 'lotado', 'fluxo intenso', 'movimento intenso'],
    'cadeiras_no_patio': ['cadeiras no patio', 'cadeiras', 'atraso por cadeiras'],
}


def citado_no_pedido(texto, pergunta, local):
    pergunta = ' ' + chave_local(pergunta) + ' '
    if ' ' + chave_local(texto) + ' ' in pergunta:
        return True
    # Aceita também nome canônico quando o usuário escreveu um apelido inequívoco.
    return any(locais == [local] and ' ' + variante + ' ' in pergunta
               for variante, locais in NOMES_NORMALIZADOS.items())


def esclarecer_local(campo, resolucao):
    mensagem = f'Qual é o local de {campo}?' if campo in ['origem', 'destino'] else 'Qual local deseja consultar?'
    if resolucao['opcoes']:
        mensagem += ' Opções: ' + ', '.join(resolucao['opcoes']) + '.'
    else:
        mensagem += ' Informe o nome do mapa; para sala, inclua bloco e número (ex.: B-04).'
    return mensagem + ' Responda apenas com o nome completo, ou digite cancelar.'


def preparar_pedido(pedido, pergunta=None):
    if not isinstance(pedido, dict):
        return dict(status='erro', mensagem='Erro: envie um objeto JSON com name e arguments.')
    nome, argumentos = pedido.get('name'), pedido.get('arguments')
    campos = {'rota_tempo_previsto': ['origem', 'destino', 'cenario'], 'listar_vizinhos': ['local']}
    if not isinstance(nome, str) or nome not in campos or not isinstance(argumentos, dict):
        return dict(status='erro', mensagem='Erro: ferramenta ou arguments inválidos.')
    if set(pedido) - {'name', 'arguments'} or set(argumentos) - set(campos[nome]):
        return dict(status='erro', mensagem='Erro: parâmetros extras não são aceitos. A base é fixa em 15 km/h.')
    limpos, ajustes = {}, []
    for campo in [c for c in campos[nome] if c != 'cenario']:
        bruto = argumentos.get(campo)
        if bruto is not None and not isinstance(bruto, str):
            return dict(status='erro', mensagem=f'Erro: {campo} precisa ser texto.')
        resolucao = resolver_local(bruto)
        if not resolucao['local']:
            return dict(status='esclarecimento', campo=campo, mensagem=esclarecer_local(campo, resolucao))
        if pergunta is not None and not citado_no_pedido(bruto, pergunta, resolucao['local']):
            return dict(status='erro', mensagem=f'Erro: {campo} não está no texto do usuário. Copie o nome como ele escreveu; se ausente, envie texto vazio.')
        limpos[campo] = resolucao['local']
        if bruto != resolucao['local']:
            ajustes.append(dict(campo=campo, recebido=bruto, usado=resolucao['local'], motivo=resolucao['motivo']))
    if nome == 'rota_tempo_previsto':
        cenario = resolver_cenario(argumentos.get('cenario', 'tranquilo'))
        if cenario is None:
            return dict(status='esclarecimento', campo='cenario', mensagem='Qual cenário deseja: tranquilo, movimentado ou cadeiras_no_patio? Responda com uma dessas opções ou digite cancelar.')
        if pergunta is not None and cenario != 'tranquilo':
            texto = ' ' + chave_local(pergunta) + ' '
            if not any(' ' + chave_local(v) + ' ' in texto for v in CENARIOS_ALTERNATIVOS[cenario]):
                return dict(status='erro', mensagem='Erro: o cenário não aparece no pedido. Use tranquilo por padrão ou copie o cenário solicitado.')
        limpos['cenario'] = cenario
    return dict(status='ok', pedido=dict(name=nome, arguments=limpos), ajustes=ajustes)


def executar(pedido):
    preparado = preparar_pedido(pedido)
    if preparado['status'] != 'ok':
        return preparado['mensagem']
    nome = preparado['pedido']['name']
    argumentos = preparado['pedido']['arguments']
    if nome == 'rota_tempo_previsto':
        return rota_tempo_previsto(**argumentos)
    return listar_vizinhos(**argumentos)


REGRAS = (
    'Você interpreta pedidos sobre o térreo do IESB. Para rota, distância ou tempo, chame rota_tempo_previsto. '
    'Para ligações diretas, chame listar_vizinhos. Não escreva a rota: Python apresentará o resultado. '
    'Copie origem e destino como escritos pelo usuário, inclusive abreviações e erros: Python normalizará. '
    'Não troque origem e destino: "quero chegar a X saindo de Y" significa origem Y e destino X. '
    'Se faltar origem/destino, envie texto vazio no campo. Se o nome for genérico, envie o termo genérico: '
    'para "banheiro", envie banheiro, sem escolher um bloco ou gênero. Nunca invente local nem posição atual. '
    'Exemplo: "biblio para b4" usa origem=biblio e destino=b4. '
    'A base é fixa em 15 km/h; não pergunte nem envie velocidade. '
    'Sem cenário, omita cenario (padrão tranquilo). Fluxo intenso/lotado usa movimentado; '
    'atraso hipotético por cadeiras usa cadeiras_no_patio. Não interprete a mera passagem pelo pátio como cenário de cadeiras. '
    'Todos os tempos são sintéticos. Não detectamos obstáculos físicos. '
    'Responda sem ferramenta somente a saudações e perguntas gerais sem consulta ao mapa. '
    'Uma chamada por vez, em <tool_call>{"name": "...", "arguments": {...}}</tool_call>. '
    'Se receber erro de formato, corrija a chamada; não prometa executá-la depois. '
    'Nomes do mapa: ' + ', '.join(LOCAIS) + '.'
)


def extrair_json(texto):
    try:
        valor = json.loads(texto.strip())
        return valor if isinstance(valor, dict) else None
    except (ValueError, TypeError):
        return None


def ler_pedido_de_ferramenta(resposta):
    partes = re.findall(r'<tool_call>\s*(.*?)\s*</tool_call>', resposta, flags=re.S)
    if len(partes) != 1:
        return None
    return extrair_json(partes[0])


def parece_consulta_mapa(pergunta):
    texto = ' ' + chave_local(pergunta) + ' '
    termos = r'\b(rota|caminho|chegar|chego|ir|vizinhos|ligados|distancia|banheiro|sala|mesa)\b'
    return (bool(re.search(termos, texto))
            or any(' ' + n + ' ' in texto for n in NOMES_NORMALIZADOS)
            or any(resolver_local(p)['local'] for p in texto.split() if len(p) >= 6))


def agente(pergunta, mostrar=True, retornar_detalhes=False, pendencia=None):
    global ULTIMA_GERACAO
    mensagens = [{'role': 'system', 'content': REGRAS}, {'role': 'user', 'content': pergunta}]
    detalhes = dict(resposta='', chamadas=[], tentativas=[], status='erro', pendencia=None)
    contexto = pergunta
    pedido_pendente = None
    if pendencia:
        if pergunta.strip().lower() == 'cancelar':
            detalhes.update(resposta='Consulta cancelada. Informe uma nova origem e destino.', status='cancelado')
            return detalhes if retornar_detalhes else detalhes['resposta']
        pedido_pendente = json.loads(json.dumps(pendencia['pedido']))
        pedido_pendente['arguments'][pendencia['campo']] = pergunta
        contexto = pendencia['contexto'] + '\nEsclarecimento: ' + pergunta
    for passo in range(3):
        fonte = 'esclarecimento_usuario' if pedido_pendente is not None else 'qwen'
        geracao = {}
        if pedido_pendente is not None:
            pedido = pedido_pendente
            resposta = '<tool_call>' + json.dumps(pedido, ensure_ascii=False) + '</tool_call>'
            pedido_pendente = None
        else:
            ULTIMA_GERACAO = {}
            resposta = conversar(mensagens, FERRAMENTAS)
            geracao = ULTIMA_GERACAO.copy()
            pedido = ler_pedido_de_ferramenta(resposta)
        tentativa = dict(resposta_modelo=resposta if fonte == 'qwen' else None,
                         fonte=fonte, pedido_bruto=pedido,
                         geracao=geracao)
        detalhes['tentativas'].append(tentativa)
        if pedido is None:
            if '<tool_call' not in resposta and passo == 0 and not parece_consulta_mapa(pergunta):
                detalhes.update(resposta=resposta, status='resposta_livre')
                break
            preparado = dict(status='erro', mensagem='Erro: envie exatamente uma chamada com JSON válido e as tags completas.')
        else:
            preparado = preparar_pedido(pedido, contexto)
        tentativa['validacao'] = preparado
        if preparado['status'] == 'esclarecimento':
            detalhes.update(resposta=preparado['mensagem'], status='esclarecimento',
                            pendencia=dict(pedido=pedido, campo=preparado['campo'], contexto=contexto))
            break
        if preparado['status'] == 'ok':
            resultado = executar(preparado['pedido'])
            detalhes['chamadas'].append(dict(pedido=preparado['pedido'], pedido_bruto=pedido,
                                            ajustes=preparado['ajustes'], resultado=resultado))
            if mostrar:
                print('[ferramenta]', preparado['pedido'])
            # O retorno já contém caminho completo, metros, segundos e aviso sintético.
            # Não passa por outra geração do Qwen; ele não converte nem reescreve os valores.
            detalhes.update(resposta=resultado, status='erro' if resultado.startswith('Erro:') else 'concluido')
            break
        mensagens.append({'role': 'assistant', 'content': resposta})
        mensagens.append({'role': 'user', 'content': preparado['mensagem'] + ' Corrija somente o formato/argumentos usando o pedido original.'})
    else:
        detalhes['resposta'] = 'Não consegui interpretar com segurança em 3 tentativas. Informe origem e destino com os nomes do mapa.'
    return detalhes if retornar_detalhes else detalhes['resposta']
