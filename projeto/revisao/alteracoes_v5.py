"""Monta alteracoes_v5.json: grafico de calibracao por decis e taxa de captura no decil de maior risco (secoes 4.4 e
6.7), com os numeros lidos de calibracao_captura.pkl (script 18).
Uso: python alteracoes_v5.py <pasta do executar.sh>"""
import sys, os, json, pickle, math

R = pickle.load(open(os.path.join(sys.argv[1], 'calibracao_captura.pkl'), 'rb'))
f3 = lambda v: f'{v:.3f}'.replace('.', ',')
s3 = lambda v: ('−' if v < 0 else '+') + f'{abs(v):.3f}'.replace('.', ',')
pc = lambda v: f'{100 * v:.1f}'.replace('.', ',') + '%'
u, d = R[1], R[2]
top = lambda h, n: (R[h][n]['prev_decil'][-1], R[h][n]['obs_decil'][-1])
maxprev2 = max(R[2][n]['prev_decil'].max() for n in ('F', 'COB', 'GB'))
assert d['GB']['ic_dif'][0] > 0 and d['COB']['ic_dif'][0] < 0 < d['COB']['ic_dif'][1] and u['COB']['ic_dif'][0] > 0   # redacao abaixo depende disso
assert top(1, 'F')[0] < top(1, 'F')[1]                                                                              # subestimacao no topo

A = []
A.append(dict(op='substituir', antigo='sob diferentes razões de custo entre falso negativo e falso positivo.',
              novo='sob diferentes razões de custo entre falso negativo e falso positivo. Complementam essas métricas o gráfico de '
                   'calibração por decis de probabilidade prevista e a taxa de captura no decil de maior risco, isto é, a fração das '
                   'entradas concentrada nos 10% de firma-anos com maior probabilidade prevista, com intervalo por bootstrap agrupado '
                   'por firma.'))
par = (f'Duas medidas complementares tornam visível a diferença entre ordenar e calibrar. A Figura {{FIG:calibracao}} compara, em '
       f'cada decil de probabilidade prevista, a probabilidade média com a frequência observada de entrada. No horizonte de um ano, os '
       f'três modelos acompanham a diagonal nos decis inferiores; no decil de maior risco, a cobertura de juros e a referência não '
       f'linear preveem {f3(top(1, "COB")[0])} e {f3(top(1, "GB")[0])} e observam {f3(top(1, "COB")[1])} e {f3(top(1, "GB")[1])}, '
       f'enquanto o escore sintético prevê {f3(top(1, "F")[0])} e observa {f3(top(1, "F")[1])}: além de ordenar pior, ele concentra '
       f'menos risco no topo da distribuição e o subestima. A taxa de captura no decil de maior risco traduz o mesmo ponto em termos '
       f'operacionais: os 10% de firma-anos com maior probabilidade prevista concentram {pc(u["F"]["captura"])} das entradas pelo '
       f'escore sintético, contra {pc(u["COB"]["captura"])} pela cobertura de juros (diferença de {f3(u["COB"]["dif"])}, com '
       f'intervalo de {s3(u["COB"]["ic_dif"][0])} a {s3(u["COB"]["ic_dif"][1])}) e {pc(u["GB"]["captura"])} pela referência não '
       f'linear. No horizonte de dois anos, as probabilidades médias previstas não passam de {f"{math.ceil(maxprev2 * 100) / 100:.2f}".replace(".", ",")} em nenhum decil, '
       f'e a captura cai para {pc(d["F"]["captura"])} no escore sintético e {pc(d["COB"]["captura"])} na cobertura de juros, '
       f'diferença não distinguível ({s3(d["COB"]["dif"])}, com intervalo de {s3(d["COB"]["ic_dif"][0])} a '
       f'{s3(d["COB"]["ic_dif"][1])}); só a referência não linear captura mais que o escore sintético com intervalo que exclui o '
       f'zero, com {pc(d["GB"]["captura"])}.')
A.append(dict(op='inserir_apos', ancora='a ordenação em precisão e revocação reproduz', ancora_contem=True,
              modelo='Com prevalência de', textos=[par]))
A.append(dict(op='figura_apos', ancora='Duas medidas complementares tornam visível', modelo_legenda='Figura 4 – ',
              legenda='Figura {FIG:calibracao} – Calibração por decis de probabilidade prevista, fora da amostra',
              imagem='fig_calibracao.png',
              fonte='Fonte: elaboração própria. Firma-anos ordenados pela probabilidade prevista fora da amostra e divididos em dez '
                    'grupos de igual tamanho; probabilidades por regressão logística sobre o posto do escore, estimada nas firmas de '
                    'treino. Atribuição de referência; 5.037 firma-anos e 149 entradas em um ano, 4.288 e 126 em dois.'))
assert (u['_n'], u['_eventos'], d['_n'], d['_eventos']) == (5037, 149, 4288, 126)
json.dump(A, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'alteracoes_v5.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print(par)
