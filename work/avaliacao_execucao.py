# Executar somente após carregar o Qwen real; não usar respostas artificiais nesta célula.
from datetime import datetime, timezone
from importlib.metadata import version

PASTA_AVALIACAO = Path('resultados_agente') / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
PASTA_AVALIACAO.mkdir(parents=True, exist_ok=False)
metadados = dict(modelo=nome_qwen, revisao_modelo=getattr(qwen.config, '_commit_hash', None),
                 dispositivo=dispositivo, transformers=version('transformers'),
                 torch=version('torch'), regras=REGRAS, quantidade_casos=len(CASOS),
                 velocidade_base_kmh=VELOCIDADE_BASE_KMH, custo_rota='tempo_previsto_s',
                 versao_avaliacao='v3_interpretacao_resposta_direta', tipo_execucao='Qwen real',
                 apelidos=APELIDOS, similaridade_minima=0.88, margem_minima=0.10,
                 politica='Uma ferramenta executada após validação; retorno direto sem reescrita pelo LLM.',
                 sklearn=version('scikit-learn'), numpy=version('numpy'), pandas=version('pandas'),
                 geracao='do_sample=False; max_new_tokens=200; até 3 tentativas de interpretação; sem geração final de rota',
                 nos=LOCAIS, ligacoes=LIGACOES, modelo_custo=MELHOR_MODELO,
                 semente_dados=SEMENTE_DADOS)
(PASTA_AVALIACAO / 'metadados.json').write_text(json.dumps(metadados, ensure_ascii=False, indent=2), encoding='utf-8')
(PASTA_AVALIACAO / 'casos_esperados.json').write_text(json.dumps(CASOS, ensure_ascii=False, indent=2), encoding='utf-8')

AVALIACOES = []
for caso in CASOS:
    avaliacao = avaliar_caso(caso)
    AVALIACOES.append(avaliacao)
    # Salva após cada caso para preservar o trabalho se a sessão for interrompida.
    (PASTA_AVALIACAO / 'resultados.json').write_text(json.dumps(AVALIACOES, ensure_ascii=False, indent=2), encoding='utf-8')
    print(avaliacao)

resumo = dict(executados=len(AVALIACOES), fidelidade_manual='pendente', criterios={})
for criterio in ['ferramenta', 'argumentos', 'chamadas_esperadas', 'resultado_valido', 'conteudo_automatico', 'apresentacao_fiel']:
    aplicaveis = [a for a in AVALIACOES if a[criterio] is not None]
    acertos = sum(a[criterio] for a in aplicaveis)
    resumo['criterios'][criterio] = dict(acertos=acertos, total=len(aplicaveis))
    print(criterio, ':', acertos, 'de', len(aplicaveis))
resumo['duracao_mediana_s'] = median(a['duracao_s'] for a in AVALIACOES)
(PASTA_AVALIACAO / 'resumo.json').write_text(json.dumps(resumo, ensure_ascii=False, indent=2), encoding='utf-8')
revisao = [dict(id=a['id'], resposta_fiel=None, justificativa='', revisor='',
                criterio=CASOS[i]['criterio_manual']) for i, a in enumerate(AVALIACOES)]
(PASTA_AVALIACAO / 'revisao_manual.json').write_text(json.dumps(revisao, ensure_ascii=False, indent=2), encoding='utf-8')
print('Revisão humana da fidelidade pendente. Evidências salvas em:', PASTA_AVALIACAO)
