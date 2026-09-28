import pandas as pd, numpy as np, warnings, pickle
from sklearn.cross_decomposition import PLSRegression
from sklearn.ensemble import HistGradientBoostingClassifier
warnings.filterwarnings('ignore')
exec(open('01_pipeline_sem_vazamento.py').read().split("out = {}")[0])

def evaluate(E, yc, seed=1, k=5):
    E = E.reset_index(drop=True)
    fm = folds(P.CD_CVM.values, k, seed); Pf = P.CD_CVM.map(fm).values; Ef = E.CD_CVM.map(fm).values
    pr = {n: np.zeros(len(E)) for n in ['F','PLS','GB']}
    for j in range(k):
        mu, sd, v1, q, _ = unsup_params(P[Pf != j])
        tr, te = E[Ef != j], E[Ef == j]
        Ztr, Zte = apply_z(tr, mu, sd), apply_z(te, mu, sd); ytr = tr[yc].values.astype(int)
        pr['F'][Ef == j] = Zte @ v1
        nc = choose_ncomp(Ztr, ytr, tr.CD_CVM.values, seed)
        pr['PLS'][Ef == j] = PLSRegression(n_components=nc, scale=False).fit(Ztr, ytr).predict(Zte).ravel()
        g = HistGradientBoostingClassifier(max_depth=3, max_iter=200, learning_rate=.05,
               min_samples_leaf=40, l2_regularization=1., random_state=seed).fit(Ztr, ytr)
        pr['GB'][Ef == j] = g.predict_proba(Zte)[:, 1]
    y = E[yc].values.astype(int)
    r = {n: auc(pr[n], y) for n in pr}
    r['COB'] = auc(-E.COB.values, y); r['ROA'] = auc(-E.ROA.values, y)
    return r, len(E), int(y.sum()), E.CD_CVM.nunique()

base = P[(P.em_risco==1) & P.V1.notna() & P[['X12','X22']].notna().all(axis=1)].copy()

# ------------------------------------------------------------------ BLOCO F
print('='*78); print('BLOCO F  |  MULTIPLAS ENTRADAS POR FIRMA'); print('='*78)
ent = P[P.V_entrada==1].groupby('CD_CVM').ano.apply(sorted)
n1 = (ent.apply(len)==1).sum(); n2 = (ent.apply(len)>=2).sum()
print(f'firmas com entrada: {len(ent)} | uma entrada: {n1} | duas ou mais: {n2} | total de entradas: {int(P.V_entrada.sum())}')
gaps = [e[1]-e[0] for e in ent if len(e)>=2]
print(f'intervalo entre primeira e segunda entrada: media {np.mean(gaps):.1f} anos, min {min(gaps)}, max {max(gaps)}')
first = ent.apply(lambda e: e[0]).to_dict()
# evento em t+1 cujo ano e posterior a primeira entrada da firma = reentrada
base['ano_ev'] = base.ano + 1
base['reentrada'] = base.apply(lambda r: r.V1==1 and r.CD_CVM in first and r.ano_ev > first[r.CD_CVM], axis=1)
print(f'eventos na amostra de estimacao que sao reentradas: {int(base.reentrada.sum())} de {int(base.V1.sum())}')
# sensibilidade: so a primeira entrada; apos a primeira, a firma deixa o conjunto de risco
fe = base[~base.apply(lambda r: r.CD_CVM in first and r.ano_ev > first[r.CD_CVM], axis=1)].copy()
rb, nb, eb, fb = evaluate(base, 'V1'); rf, nf, ef, ff = evaluate(fe, 'V1')
print(f'\n{"":24s} {"obs":>6s} {"ev":>4s} ' + ''.join(f'{n:>7s}' for n in ['F','PLS','GB','COB','ROA']))
print(f'{"todas as entradas":24s} {nb:6d} {eb:4d} ' + ''.join(f'{rb[n]:7.4f}' for n in ['F','PLS','GB','COB','ROA']))
print(f'{"somente primeira entrada":24s} {nf:6d} {ef:4d} ' + ''.join(f'{rf[n]:7.4f}' for n in ['F','PLS','GB','COB','ROA']))
print(f'vantagem PLS - F: {rb["PLS"]-rb["F"]:+.4f} (todas) | {rf["PLS"]-rf["F"]:+.4f} (primeira)')

# ------------------------------------------------------------------ BLOCO E
print('\n'+'='*78); print('BLOCO E  |  SAIDA DO PAINEL E CENSURA INFORMATIVA'); print('='*78)
ult = P.groupby('CD_CVM').ano.max(); saem = set(ult[ult < P.ano.max()].index)   # ultimo ano do painel, nao data fixa
last = P[P.CD_CVM.isin(saem)].sort_values('ano').groupby('CD_CVM').tail(1)
rj_any = P.groupby('CD_CVM')['crit_d_state'].max()
vul_recent = P.sort_values('ano').groupby('CD_CVM').tail(2).groupby('CD_CVM').V_estado.max()
print(f'firmas que deixam o painel antes de {P.ano.max()}: {len(saem)}')
print(f'   vulneraveis na ultima observacao        : {int(last.V_estado.sum())} ({last.V_estado.mean()*100:.1f}%)')
print(f'   com recuperacao judicial em algum momento: {int(rj_any[list(saem)].sum())} ({rj_any[list(saem)].mean()*100:.1f}%)')
dist = [f for f in saem if rj_any.get(f,0)==1 or vul_recent.get(f,0)==1]
print(f'   saida potencialmente associada a distress: {len(dist)} ({len(dist)/len(saem)*100:.1f}%)  [RJ registrada ou vulneravel nas duas ultimas observacoes]')
fica_last = P[~P.CD_CVM.isin(saem)].sort_values('ano').groupby('CD_CVM').tail(1)
print(f'comparacao: firmas que permanecem, vulneraveis na ultima observacao: {fica_last.V_estado.mean()*100:.1f}%')
# observacoes finais em risco, sem desfecho observavel, de firmas com saida por distress
cand = P[(P.CD_CVM.isin(dist)) & (P.em_risco==1) & P[['X12','X22']].notna().all(axis=1)]
cand_last = cand.sort_values('ano').groupby('CD_CVM').tail(1)
cand_last = cand_last[cand_last.V1.isna()]
print(f'\nobservacoes finais em risco, sem t+1, de firmas com saida por distress: {len(cand_last)}')
sens = pd.concat([base.drop(columns=['ano_ev','reentrada']), cand_last.assign(V1=1.0)], ignore_index=True)
rs, ns, es, fs = evaluate(sens, 'V1')
print(f'\n{"":30s} {"obs":>6s} {"ev":>4s} ' + ''.join(f'{n:>7s}' for n in ['F','PLS','GB','COB','ROA']))
print(f'{"especificacao principal":30s} {nb:6d} {eb:4d} ' + ''.join(f'{rb[n]:7.4f}' for n in ['F','PLS','GB','COB','ROA']))
print(f'{"saidas por distress como evento":30s} {ns:6d} {es:4d} ' + ''.join(f'{rs[n]:7.4f}' for n in ['F','PLS','GB','COB','ROA']))
print(f'vantagem PLS - F: {rb["PLS"]-rb["F"]:+.4f} (principal) | {rs["PLS"]-rs["F"]:+.4f} (saidas como evento)')
pickle.dump({'F':(rb,rf,nb,eb,nf,ef,n1,n2,gaps),'E':(rs,ns,es,len(saem),len(dist),len(cand_last),
             last.V_estado.mean(),rj_any[list(saem)].mean(),fica_last.V_estado.mean())},open('blocoEF.pkl','wb'))
