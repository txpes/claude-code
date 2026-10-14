"""Numeros do texto corrido do artigo, calculados a partir de uma execucao do codigo.
Cada frase-modelo e preenchida duas vezes, com a execucao antiga e com a nova: a versao antiga precisa casar exatamente com
o texto atual (o que confere a origem de cada numero), e a nova o substitui. Gera alteracoes no formato do aplicar_v3.py.
Uso: python numeros_texto.py <execucao antiga> <dados antigos> <execucao nova> <dados novos> <saida.json>"""
import sys, os, json, pickle
import numpy as np, pandas as pd

RA, DA, RB, DB, OUT = sys.argv[1:6]
f3 = lambda x: f'{x:.3f}'.replace('.', ',')
f2 = lambda x: f'{x:.2f}'.replace('.', ',')
f1 = lambda x: f'{x:.1f}'.replace('.', ',')
p1 = lambda x: f1(100 * x)
p2 = lambda x: f2(100 * x)
mil = lambda x: f'{int(round(x)):,}'.replace(',', '.')
neg = lambda x: ('−' if x < 0 else '') + f3(abs(x))
from decimal import Decimal, ROUND_HALF_UP
f2h = lambda x: str(Decimal(f'{x:.3f}').quantize(Decimal('0.01'), ROUND_HALF_UP)).replace('.', ',')   # arredonda o valor exibido com tres casas
r3 = lambda x: round(float(f'{x:.3f}'), 3)


def auc(x, y):
    r = pd.Series(x).rank().values; n1 = int(y.sum())
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))


def valores(R, D):
    L = lambda f: pickle.load(open(os.path.join(R, f), 'rb'))
    N, T, A, RB_, TP, PU, PF, EV, EF, G3, DEC = (L(f) for f in ['N.pkl', 'tabelas.pkl', 'blocoA.pkl', 'robustez.pkl', 'temporal.pkl', 'puros.pkl',
                                                               'perfil.pkl', 'eventos_alternativos.pkl', 'blocoEF.pkl', 'blocoG3.pkl', 'decomposicao.pkl'])
    W = L('within2.pkl'); TI = L('tres_indicadores.pkl'); PN = L('panorama.pkl')
    v = {}
    # painel
    v['obs'], v['firmas'] = mil(T['obs']), str(T['firmas'])
    v['obs_en'] = f"{T['obs']:,}"
    I = pd.read_csv(os.path.join(D, 'painel_inputs.csv')); v['inputs'] = mil(len(I))
    fa = T['firmas_ano']; v['fa_max'], v['fa_fim'] = str(max(fa.values())), str(fa[2025])
    v['ano_max'] = str(max(fa, key=fa.get))
    v['exm'], v['todos'] = f1(T['exerc_medio']), str(T['painel_completo_firmas'])
    v['vuln'], v['vuln_pct'] = mil(T['vuln']), p1(T['vuln_pct'])
    v['risco'], v['censura'] = mil(T['risco']), str(T['censura'])
    v['fora_risco'] = mil(T['obs'] - T['risco'] - T['contin'] - T['censura'])
    Tr = pd.read_csv(os.path.join(D, 'painel_transicao.csv'))
    Tr['primeira'] = Tr.groupby('CD_CVM').ano.transform('min') == Tr.ano
    fora = Tr[(Tr.em_risco == 0) & (Tr.V_estado_lag != 1) & ~((Tr.V_estado == 1) & Tr.primeira)]
    v['primeira'] = str(int(fora.primeira.sum()))
    v['taxa'] = p2(T['taxa_entrada'])
    v['est_n1'], v['est_ev1'] = mil(T['est_n1']), str(T['est_ev1'])
    v['est_pct'] = p2(T['est_ev1'] / T['est_n1'])
    v['com_n1'], v['com_ev1'], v['com_n2'], v['com_ev2'] = mil(T['com_n1']), str(T['com_ev1']), mil(T['com_n2']), str(T['com_ev2'])
    v['prev'] = p2(T['com_ev1'] / T['com_n1'])
    ds = T['desc']; v['cob_min'], v['cob_max'] = f1(abs(ds.loc['COB', 'min'])), f1(ds.loc['COB', 'max'])
    v['meb_min'], v['meb_max'] = f1(abs(ds.loc['EBITDA', 'min'])), f1(ds.loc['EBITDA', 'max'])
    C = T['corr'].abs().copy(); C = C.where(~np.eye(len(C), dtype=bool), 0.0)
    v['corr_max'] = f2(C.values.max())
    v['cob_corr'] = f2(C.loc['COB'].max())
    v['cp1'], v['acum3'] = p2(T['var_exp'][0]), p2(T['acum3'])
    # desempenho agregado
    E, y, pred = A[1]['ref']
    for m in ['F', 'COB', 'ROA', 'GB', 'PLS']:
        v[m + '1'] = f3(auc(pred[m], y))
    v['dBA'] = f3(-N['d_BA1'])
    res = A[1]['res']
    v['Fmu'], v['Fsd'] = f3(np.mean(res['F'])), f3(np.std(res['F'], ddof=1))
    v['PLSmu'], v['PLSsd'] = f3(np.mean(res['PLS'])), f3(np.std(res['PLS'], ddof=1))
    v['GBmu'], v['GBsd'] = f3(np.mean(res['GB'])), f3(np.std(res['GB'], ddof=1))
    v['BAmu'], v['BAmin'], v['BAmax'] = f3(np.mean(res['BA'])), f3(min(res['BA'])), f3(max(res['BA']))
    v['dGBCOB'] = f3(N['d_GB_COB1'])
    # minskyana
    v['pz8'], v['np8'], v['auc8'], v['auc7'] = f3(N['mk8_pz']), neg(N['mk8_np']), f3(N['mk8_auc']), f3(N['mk7_auc'])
    v['queda'] = f3(float(f3(N['mk8_auc']).replace(',', '.')) - float(f3(N['mk7_auc']).replace(',', '.')))
    v['pz_n'], v['pz_pct'] = mil(N['pz_n']), p1(N['pz_pct'])
    # controles (Tabela A.2)
    g = T['grade']
    v['alv_s'], v['alv_c'] = f3(g['ALV'][False]), f3(g['ALV'][True])
    v['lc_s'], v['lc_c'] = f3(g['LC'][False]), f3(g['LC'][True])
    v['cob_perde'] = f3(g['COB'][False] - g['COB'][True])
    # temporal
    t1 = TP[1]; au = t1['auc']
    quatro = [au[m] for m in ['COB', 'ROA', 'PLS', 'GB']]
    v['tdif'] = f3(max(map(r3, quatro)) - min(map(r3, quatro)))   # diferenca entre os valores exibidos na tabela
    v['tBA'], v['tF'] = f3(au['BA']), f3(au['F'])
    v['t_ntr'], v['t_evtr'], v['t_nte'], v['t_evte'] = mil(t1['n_tr']), str(t1['ev_tr']), mil(t1['n_te']), str(t1['ev_te'])
    v['t_nte2'], v['t_evte2'] = mil(TP[2]['n_te']), str(TP[2]['ev_te'])
    # probit
    pr = T['probit']; pv = T['probit_var']
    v['b1'], v['b2'], v['best'] = f3(pr['trans_h1']['coef']), f3(pr['trans_h2']['coef']), f3(pr['est_h1']['coef'])
    v['r2est'], v['r2tr'] = f3(pr['est_h1']['r2']), f3(pr['trans_h1']['r2'])
    v['bporte'], v['bsem'] = f3(pv['porte']['coef']), f3(pv[None]['coef'])
    # decomposicao (subconjuntos puros)
    e1, e2, pl1, rj1 = PU[(1, 'EBITDA puras')], PU[(2, 'EBITDA puras')], PU[(1, 'PL puras')], PU[(1, 'RJ puras')]
    v['eF1'], v['eCOB1'], v['edif1'] = f3(e1['F']), f3(e1['COB'][0]), f3(e1['COB'][1])
    v['eF2'], v['eCOB2'] = f3(e2['F']), f3(e2['COB'][0])
    v['edif1_2'], v['edif2_2'] = f2h(e1['COB'][1]), f2h(e2['COB'][1])
    v['e_n'], v['pl_n'], v['rj_n'] = str(e1['n']), str(pl1['n']), str(rj1['n'])
    v['plF'], v['plCOB'], v['plROA'], v['plPLS'] = f3(pl1['F']), f3(-pl1['COB'][1]), f3(-pl1['ROA'][1]), f3(-pl1['PLS'][1])
    v['amp'] = f3(PU[(1, 'RJ amplitude')])
    sem = EV['sem entradas so EBITDA']
    v['sem_ev'] = str(int(sem['ref'][1].sum()))
    v['semF'], v['semPLS'], v['semGB'] = (f3(np.mean(sem['res'][m])) for m in ['F', 'PLS', 'GB'])
    # sobreposicao mecanica
    P = pd.read_csv(os.path.join(D, 'painel_completo.csv'))
    Ec = E.merge(P[['CD_CVM', 'ano', 'EBITDA']].rename(columns={'EBITDA': 'MEB_t'}), on=['CD_CVM', 'ano'], how='left')
    Tc = Tr[['CD_CVM', 'ano']].copy()
    v['naoev_neg'] = p1((Ec.MEB_t[y == 0] < 0).mean())
    v['meb'] = f3(np.mean(DEC['h1 principal'][('EBITDA, exclusivamente', 'MEB')]))
    Pp = P.sort_values(['CD_CVM', 'ano']).copy(); Pp['a1'] = Pp.groupby('CD_CVM').ano.shift(-1)
    for k in ['crit_b', 'crit_c', 'crit_d_entry']:
        Pp[k + '_1'] = Pp.groupby('CD_CVM')[k].shift(-1); Pp.loc[Pp.a1 != Pp.ano + 1, k + '_1'] = np.nan
    Ex = E[['CD_CVM', 'ano']].merge(Pp[['CD_CVM', 'ano', 'EBITDA', 'crit_b_1', 'crit_c_1', 'crit_d_entry_1']], on=['CD_CVM', 'ano'], how='left')
    pura = (Ex.crit_c_1 == 1).values & ~(Ex.crit_b_1 == 1).values & ~(Ex.crit_d_entry_1 == 1).values
    kk = ((y == 0) | (pura & (y == 1))) & (Ex.EBITDA < 0).values
    v['cob_neg'] = f3(auc(pred['COB'][kk], y[kk]))     # cobertura entre as observacoes com EBITDA negativo em t
    # perfil
    v['alv_e'], v['alv_pl'], v['alv_n'] = (f3(x) for x in PF['ALV'])
    v['lc_e'], v['lc_pl'], v['lc_n'] = (f3(x) for x in PF['LC'])
    # cargas
    cg = T['cargas']
    v['c_cg'], v['c_roa'], v['c_alv'], v['c_lc'] = f3(cg['CG']), f3(cg['ROA']), f3(cg['ALV']), f3(cg['LC'])
    dg = T['diagnostico'].set_index('ind')
    est = dg.loc[['CG', 'LC', 'ALV', 'CP'], 'entre']
    v['entre_min'], v['entre_max'] = p1(est.min()), p1(est.max())
    v['sp'], v['sp_p'] = neg(T['sp_entre_ks'][0]), f3(T['sp_entre_ks'][1])
    # metricas
    g3 = G3[1]
    incl = [g3[m]['incl'] for m in ['GB', 'COB', 'ROA', 'PLS', 'F', 'BA']]
    v['incl_min'], v['incl_max'] = f3(min(incl)), f3(max(incl))
    v['sinF'], v['sinCOB'] = p1(g3['F'][80]['sinalizadas']), p1(g3['COB'][80]['sinalizadas'])
    v['vppF'], v['vppCOB'] = f3(g3['F'][80]['vpp']), f3(g3['COB'][80]['vpp'])
    v['espF'], v['espCOB'] = f3(g3['F'][80]['espec']), f3(g3['COB'][80]['espec'])
    v['nbF'], v['nbGB'] = f3(g3['F']['nb10']), f3(g3['GB']['nb10'])
    vpn = [g3[m][80]['vpn'] for m in ['GB', 'COB', 'ROA', 'PLS', 'F', 'BA']]
    v['vpn_min'], v['vpn_max'] = f3(min(vpn)), f3(max(vpn))
    # robustez
    v['semCP'], v['cp1cp2'], v['cp1mcp2'] = f3(RB_['semCP']), f3(RB_['cp1cp2']), f3(RB_['cp1mcp2'])
    v['within'] = f3(W['within'])
    v['wins_cp1'], v['wins_auc'] = p2(N['wins_cp1']), f3(N['wins_auc'])
    v['P8'], v['P16'] = f3(RB_['lag']['P8']), f3(RB_['lag']['P16'])
    st = RB_['setor']
    cc, tl = st['Construção Civil, Mat. Constr. e Decoração'], st['Serviços Transporte e Logística']
    v['ccF'], v['ccC'], v['tlF'], v['tlC'] = f2(cc['F']), f2(cc['COB']), f2(tl['F']), f2(tl['COB'])
    # saidas
    Ee = EF['E']; v['n_saem'], v['n_dist'], v['n_cand'] = str(Ee[3]), str(Ee[4]), str(Ee[5])
    v['vul_saem'], v['vul_ficam'] = p1(Ee[6]), p1(Ee[8])
    E2 = EF['E2']; cl = E2[3]
    v['c_fech'], v['c_rj'], v['c_inc'], v['c_fal'] = (str(cl[k]) for k in ['fechamento voluntário de capital', 'recuperação judicial', 'incorporação ou reorganização', 'falência ou liquidação'])
    v['c_out'], v['c_nid'] = str(cl['cancelamento por outro motivo']), str(cl['motivo não identificado'])
    v['c_filtro'], v['c_dist'], v['c_cand'] = str(E2[4]), str(E2[5]), str(E2[6])
    v['c_dist_pct'] = p1(E2[5] / Ee[3])
    # taxas por subperiodo
    Pm = P.merge(Tr[['CD_CVM', 'ano', 'em_risco', 'V_entrada']], on=['CD_CVM', 'ano'])
    rk = Pm[Pm.em_risco == 1]
    v['tx_pre'], v['tx_pos'] = p2(rk[rk.ano <= 2019].V_entrada.mean()), p2(rk[rk.ano >= 2020].V_entrada.mean())
    # RJ antecipada
    S = os.path.join(R, 'sens_rj_antecipada'); As = pickle.load(open(os.path.join(S, 'blocoA.pkl'), 'rb'))
    Es, ys, ps = As[1]['ref']; v['rjF'], v['rjCOB'] = f3(auc(ps['F'], ys)), f3(auc(ps['COB'], ys))
    # tres indicadores
    t = TI; c1, c2 = t[1]['cmp'], t[2]['cmp']
    v.update(t3F=f3(t[1]['ref']['F3']), t3dif=neg(c1['COB vs F3'][0]), t3lo=neg(c1['COB vs F3'][1]), t3hi=('+' if c1['COB vs F3'][2] >= 0 else '') + neg(c1['COB vs F3'][2]),
             t3roa=f3(-c1['ROA vs F3'][0]), t3pls=f3(-c1['PLS vs F3'][0]), t3F2=f3(t[2]['ref']['F3']), t3COB2=f3(t[2]['ref']['COB']),
             t3d2=f3(-c2['COB vs F3'][0]), t3lo2='+' + f3(-c2['COB vs F3'][2]), t3hi2='+' + f3(-c2['COB vs F3'][1]),
             t3ROA2=f3(t[2]['ref']['ROA']), t3PLS2=f3(t[2]['ref']['PLS']),
             t3m3=f3(max(abs(t[h]['ref']['M3'] - t[h]['ref']['F3']) for h in (1, 2))),
             t3sel=str(t[1]['trios'].get(('COB', 'EBITDA', 'ROA'), 0) + t[2]['trios'].get(('COB', 'EBITDA', 'ROA'), 0)))
    for h in (1, 2):
        for k in ['EBITDA', 'PL', 'RJ']:
            r_ = t[h]['puros'][f'{k} puras']; v[f't3_{h}{k}'], v[f't3_{h}{k}n'] = f3(r_['auc']['F3']), str(r_['n'])
    return v


VA, VB = valores(RA, DA), valores(RB, DB)
M = [  # frases-modelo; cada uma precisa casar uma unica vez no texto atual
 'em painel de {obs} observações firma-ano de {firmas} companhias abertas',
 'using a panel of {obs_en} firm-year observations from {firmas} Brazilian',
 'a área sob a curva ROC do escore é de {F1}, contra {COB1} da cobertura de juros e {ROA1} do retorno sobre ativos, em conclusão que se mantém',
 'the area under the ROC curve of the score is {F1_en}, against {COB1_en} for interest coverage and {ROA1_en} for return on assets',
 'o escore fica {edif1_2} ponto atrás da cobertura de juros em um ano',
 'e {edif2_2} ponto atrás em dois anos',
 'the score trails interest coverage by {edif1_2_en} points at one year',
 'and by {edif2_2_en} points at two years',
 'O painel reúne {obs} observações firma-ano, cobrindo {firmas} companhias',
 'entre as que saem, {vul_saem}% estavam em situação de vulnerabilidade na última observação, contra {vul_ficam}% entre as que permanecem. Oito',
 'o escore alcança {F1} fora da amostra, contra {COB1} da cobertura de juros e {ROA1} do retorno sobre ativos, e o escore também',
 'com área sob a curva de {auc8}, ou {auc7} quando excluído',
 'ali o escore alcança {eF1} contra {eCOB1} da cobertura de juros em um ano, diferença de {edif1} ponto em boa parte mecânica, e {eF2} contra {eCOB2} em dois anos',
 'alavancagem mediana de {alv_e} contra {alv_n} das que não entram, liquidez corrente de {lc_e} contra {lc_n} e capital de giro superior à mediana geral',
 'sua área sob a curva para esse tipo de entrada é de {eF2}, abaixo de 0,500',
 'O painel de insumos reúne {inputs} observações firma-ano.',
 'O painel final contém {obs} observações firma-ano referentes a {firmas} companhias.',
 'cresce de 358 em 2010 para um máximo de {fa_max} em {ano_max}, encerrando o período em {fa_fim}.',
 'Cada firma é observada em média por {exm} exercícios, com mediana de 9, e apenas {todos} das {firmas} companhias',
 'a cobertura varia de menos {cob_min} a {cob_max} e a margem de menos {meb_min} a {meb_max}.',
 '{obs} observações em todos os indicadores, sem valores ausentes.',
 'A correlação máxima é de {corr_max}, entre liquidez corrente e capital de giro',
 'sua correlação mais alta é de {cob_corr} com o retorno sobre ativos',
 'Sob a definição ampla, {vuln} observações firma-ano encontram-se em situação de vulnerabilidade, o equivalente a {vuln_pct}% do painel.',
 'A proporção de {vuln_pct}% refere-se à presença no estado de vulnerabilidade',
 'A amostra de risco reúne as {risco} observações',
 'e as {fora_risco} observações sem exercício anterior saudável observado, das quais {primeira} correspondem à primeira aparição',
 'contra {taxa}% de probabilidade de entrada a partir do estado saudável',
 'No horizonte de um ano, ela contém {est_n1} observações e {est_ev1} entradas, ou {est_pct}%. As duas medidas são distintas e ambas relevantes: {taxa}% é a incidência de entrada no painel, ao passo que {est_pct}% é a frequência',
 'ela produz taxa de eventos de {taxa}%',
 'sobre as {obs} observações do painel.',
 'O primeiro componente responde por {cp1}% da variância total, e o critério de Kaiser retém 3 componentes, que juntos explicam {acum3}%.',
 'o primeiro componente responde por {cp1}% da variância e são necessários',
 'reduz a área sob a curva fora da amostra de {F1} para {cp1cp2} ou {cp1mcp2}, ilustra',
 'O escore médio das observações em posição Ponzi é de {pz8}, contra {np8} para as demais, e a área sob a curva para discriminar essa posição é de {auc8} (Tabela A.1). Excluída a cobertura de juros, ela passa a {auc7}. A queda de {queda} ponto',
 'abrangendo {pz_n} firma-anos, ou {pz_pct}% do painel.',
 'A alavancagem isolada passa de {alv_s} para {alv_c} quando o modelo recebe setor, ano e porte, e a liquidez corrente de {lc_s} para {lc_c}; na direção oposta, a cobertura de juros perde {cob_perde} ponto.',
 'Amostra comum de {com_n1} observações e {com_ev1} entradas no horizonte de um ano, e {com_n2} e {com_ev2} no de dois.',
 'No horizonte de um ano, o escore sintético alcança {F1}, contra {COB1} da cobertura de juros, {ROA1} do retorno sobre ativos e {GB1} da referência não linear.',
 'que ele supera por {dBA} ponto sem significância estatística.',
 '{Fmu} para o escore sintético, com desvio-padrão de {Fsd}, {PLSmu} para o escore supervisionado ({PLSsd}) e {GBmu} para a referência não linear ({GBsd}). O modelo de Brito e Assaf Neto é o mais sensível à atribuição, com média de {BAmu} e amplitude de {BAmin} a {BAmax},',
 'com no máximo {tdif} ponto entre eles',
 'o supera no esquema temporal, com {tBA} contra {tF}.',
 'Treino com desfechos até 2021, {t_evtr} entradas em {t_ntr} observações; teste com desfechos de 2022 a 2025, {t_evte} entradas em {t_nte} observações no horizonte de um ano e {t_evte2} em {t_nte2} no de dois.',
 'com coeficientes de {b1} e {b2}.',
 'de {best} sob estado para {b1} sob transição',
 'de {r2est} para {r2tr}.',
 'o coeficiente é de {bporte}; sem controles, em 76,50 eventos por parâmetro, é de {bsem}; e na especificação completa, de {b1}.',
 'alcança {eF1} em um ano, contra {eCOB1} da cobertura de juros, diferença de {edif1} ponto com intervalo',
 'o escore alcança {plF} e fica nominalmente à frente da cobertura de juros e do retorno sobre ativos, por {plCOB} e {plROA} ponto',
 'que o escore sintético supera por {plPLS} ponto',
 '{e_n} entradas apenas por prejuízo operacional, {pl_n} apenas por patrimônio líquido negativo e {rj_n} apenas por recuperação judicial.',
 'tem amplitude de {amp} ponto',
 'Nas {sem_ev} entradas restantes, o escore sintético alcança {semF}, o escore supervisionado {semPLS} e a referência não linear {semGB},',
 'as {e_n} entradas desse tipo têm EBITDA negativo já em t, condição que atinge apenas {naoev_neg}% dos não eventos, e a margem EBITDA isolada alcança {meb} nesse subconjunto',
 'o escore alcança {eF2}, valor abaixo de 0,500',
 'a área sob a curva da cobertura de juros cai para {cob_neg}.',
 'alavancagem mediana de {alv_e} contra {alv_n} das que não entram, liquidez corrente de {lc_e} contra {lc_n} e capital de giro superior. São',
 'com alavancagem de {alv_pl} e liquidez de {lc_pl},',
 'com proporções entre {entre_min}% e {entre_max}%',
 'é de {sp}, com p de {sp_p}.',
 'eleva a área sob a curva de {F1} para {PLS1},',
 'ficam em {semPLS} e {semF}, sem diferença distinguível.',
 'alcançam {GB1}, e a diferença para a cobertura de juros isolada, de {dGBCOB} ponto',
 'escore com área sob a curva de {t3F}, contra {F1} do escore sobre os oito indicadores e {COB1} da cobertura de juros, sem diferença distinguível desta (cobertura menos escore restrito: {t3dif}, com intervalo de {t3lo} a {t3hi}), e supera o retorno sobre ativos e o escore supervisionado sobre os oito indicadores por {t3roa} e {t3pls} ponto. No horizonte de dois anos, alcança {t3F2} e supera a cobertura de juros, com {t3COB2}, por {t3d2} ponto (intervalo de {t3lo2} a {t3hi2}), sem diferença distinguível do retorno sobre ativos ({t3ROA2}) nem do escore supervisionado ({t3PLS2}). A média simples dos três indicadores padronizados difere do componente principal em no máximo {t3m3} ponto, e a seleção refeita pelos três maiores poderes discriminantes dentro de cada partição de treino escolhe o mesmo conjunto em {t3sel} das 100 partições',
 'o escore restrito alcança {t3_1EBITDA} nas {t3_1EBITDAn} entradas por prejuízo operacional, {t3_1PL} nas {t3_1PLn} por patrimônio líquido negativo e {t3_1RJ} nas {t3_1RJn} por recuperação judicial; em dois anos, {t3_2EBITDA}, {t3_2PL} e {t3_2RJ}, com {t3_2EBITDAn}, {t3_2PLn} e {t3_2RJn} entradas.',
 'Com prevalência de {prev}%,',
 'No mesmo limiar, o valor preditivo negativo fica entre {vpn_min} e {vpn_max} em todos os modelos.',
 'com inclinações entre {incl_min} e {incl_max} e interceptos',
 'sinaliza {sinF}% dos firma-anos, contra {sinCOB}% da cobertura de juros, com valor preditivo positivo de {vppF} contra {vppCOB}. No mesmo limiar, a especificidade é de {espF} para o escore sintético e de {espCOB} para a cobertura de juros',
 'de {nbF} para o escore sintético a {nbGB} para a referência não linear.',
 'das {n_saem} companhias cuja última observação antecede 2025, {vul_saem}% estavam em vulnerabilidade na última observação, contra {vul_ficam}% entre as que permanecem, e {n_dist} saídas',
 'Dessas, {n_cand} ocorrem a partir do estado saudável',
 'Por ele, as {n_saem} saídas se dividem em fechamento voluntário de capital ({c_fech}), recuperação judicial ({c_rj}), incorporação ou reorganização ({c_inc}), falência ou liquidação ({c_fal}), cancelamento por outro motivo ({c_out}) e motivo não identificado ({c_nid}); {c_filtro} delas decorrem',
 'As {c_dist} saídas associadas a dificuldade financeira pelo cadastro, {c_dist_pct}% do total, incluem {c_cand} ocorridas',
 'leva a área sob a curva fora da amostra de {F1} para {semCP}; somar ou subtrair o segundo componente, cujo sinal é arbitrário, a reduz para {cp1cp2} ou {cp1mcp2}; e reconstruir o escore sobre desvios da média histórica de cada firma, calculada apenas com exercícios anteriores, a leva a {within}. Winsorizando os oito indicadores nos percentis 1 e 99, a variância explicada pelo primeiro componente sobe de {cp1}% para {wins_cp1}% e o escore alcança {wins_auc} fora da amostra',
 'reduz o escore supervisionado de {P8} para {P16}.',
 'em Construção Civil o escore alcança {ccF} contra {ccC} da cobertura de juros, e em Serviços de Transporte e Logística {tlF} contra {tlC}.',
 'de {tx_pre}% até 2019 e {tx_pos}% a partir de 2020.',
 'A área sob a curva passa a {rjF} para o escore sintético e a {rjCOB} para a cobertura de juros',
 'é superado pelas razões contábeis isoladas: {F1} contra {COB1} da cobertura de juros e {ROA1} do retorno sobre ativos',
 'com {eF1} contra {eCOB1} da cobertura de juros em um ano, contraste em boa parte mecânico, e {eF2} contra {eCOB2} em dois anos',
 'alavancagem mediana de {alv_e} contra {alv_n} das que não entram e liquidez corrente de {lc_e} contra {lc_n}:',
 'Amostra de {com_n1} observações e {com_ev1} entradas. Todas',
 'Amostra comum de {com_n1} observações e {com_ev1} entradas. Controles',
]
for V in (VA, VB):
    for k in ['F1', 'COB1', 'ROA1', 'edif1_2', 'edif2_2']:
        V[k + '_en'] = V[k].replace(',', '.')
ops = []
for m in M:
    a, b = m.format(**VA), m.format(**VB)
    if a != b:
        ops.append(dict(op='substituir', antigo=a, novo=b))
json.dump(ops, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
mud = {k: (VA[k], VB[k]) for k in VA if VA[k] != VB.get(k)}
print(f'{len(M)} frases-modelo; {len(ops)} mudam -> {OUT}')
print('quantidades que mudaram:', mud)
