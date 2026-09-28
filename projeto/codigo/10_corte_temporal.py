"""
Corte temporal, conforme pedido do coorientador.

Separacao pelo ANO DO DESFECHO, e nao pelo ano do preditor, para que nenhum desfecho do
periodo de teste participe do treino:
  treino : pares cujo desfecho ocorre ate ANO_CORTE  (preditores ate ANO_CORTE - h)
  teste  : pares cujo desfecho ocorre depois de ANO_CORTE
Os parametros nao supervisionados sao estimados apenas com exercicios ate ANO_CORTE - h,
que sao os unicos disponiveis a um previsor posicionado no corte.
"""
import pandas as pd, numpy as np, warnings, pickle, sys
warnings.filterwarnings('ignore')
from sklearn.cross_decomposition import PLSRegression
from sklearn.ensemble import HistGradientBoostingClassifier
import statsmodels.api as sm
exec(open('08_definicoes_de_evento.py').read().split("OUT = {}")[0])

ANO_CORTE = int(sys.argv[1]) if len(sys.argv) > 1 else 2021

def winsor_temporal(df, q, ultimo):
    out = df[BA].astype(float).copy()
    for c in ['X12', 'X22']:
        lo = df.ano.map(q[c][0.01]).fillna(q[c][0.01].loc[ultimo])
        hi = df.ano.map(q[c][0.99]).fillna(q[c][0.99].loc[ultimo])
        out[c] = out[c].clip(lo.values, hi.values)
    return out

def temporal(h, corte=ANO_CORTE, seed=1):
    yc = f'V{h}'
    okBA = P[['X12', 'X22']].notna().all(axis=1)
    risco = (P.em_risco == 1) if h == 1 else P.r2
    E = P[risco & P[yc].notna() & okBA].copy()
    E['ano_ev'] = E.ano + h
    tr, te = E[E.ano_ev <= corte], E[E.ano_ev > corte]
    anos_tr = corte - h
    Ptr = P[P.ano <= anos_tr]                      # painel disponivel no momento do corte
    mu, sd, v1, q, _ = unsup_params(Ptr)
    ultimo = max(q['X12'][0.01].index)
    Ztr, Zte = apply_z(tr, mu, sd), apply_z(te, mu, sd)
    ytr, yte = tr[yc].values.astype(int), te[yc].values.astype(int)
    pr = {'F': Zte @ v1, 'COB': -te.COB.values, 'ROA': -te.ROA.values, 'MEB': -te.EBITDA.values,
          'LC': -te.LC.values, 'ALV': te.ALV.values}
    nc = choose_ncomp(Ztr, ytr, tr.CD_CVM.values, seed)
    pr['PLS'] = PLSRegression(n_components=nc, scale=False).fit(Ztr, ytr).predict(Zte).ravel()
    pr['GB'] = HistGradientBoostingClassifier(max_depth=3, max_iter=200, learning_rate=.05, min_samples_leaf=40,
                 l2_regularization=1., random_state=seed).fit(Ztr, ytr).predict_proba(Zte)[:, 1]
    Btr = sm.add_constant(winsor_temporal(tr, q, ultimo), has_constant='add')
    Bte = sm.add_constant(winsor_temporal(te, q, ultimo), has_constant='add').reindex(columns=Btr.columns, fill_value=0.)
    pr['BA'] = sm.Probit(ytr.astype(float), Btr).fit(disp=0, maxiter=300).predict(Bte).values
    return tr, te, ytr, yte, pr, nc

RES = {}
print(f'corte no ano de desfecho {ANO_CORTE}; painel de estimacao ate {ANO_CORTE - 1} para um ano\n')
for h in (1, 2):
    tr, te, ytr, yte, pr, nc = temporal(h)
    print(f'=== horizonte de {h} ano(s) ===')
    print(f'  treino: {len(tr)} obs, {int(ytr.sum())} entradas, desfechos {int(tr.ano.min())+h} a {ANO_CORTE}')
    print(f'  teste : {len(te)} obs, {int(yte.sum())} entradas, desfechos {ANO_CORTE+1} a {int(te.ano.max())+h}'
          f'  | componentes do PLS: {nc}')
    RES[h] = dict(n_tr=len(tr), ev_tr=int(ytr.sum()), n_te=len(te), ev_te=int(yte.sum()), nc=nc,
                  auc={m: auc(pr[m], yte) for m in pr}, ano_ini=int(te.ano.min()) + h, ano_fim=int(te.ano.max()) + h)
    if yte.sum() < 5: print('  eventos insuficientes para avaliacao\n'); continue
    ordem = sorted(['F', 'PLS', 'GB', 'BA', 'COB', 'ROA', 'MEB'], key=lambda m: -auc(pr[m], yte))
    print('  AUC: ' + ' | '.join(f'{m} {auc(pr[m], yte):.3f}' for m in ordem))
    for m in ['COB', 'ROA', 'PLS', 'GB']:
        o, lo, hi, p = boot(pr['F'], pr[m], yte, te.CD_CVM.values, B=2000)
        print(f'    {m} menos F: {o:+.3f}  IC95 [{lo:+.3f}; {hi:+.3f}]  p {p:.3f}')
        RES[h].setdefault('cmp', {})[m] = (o, lo, hi, p)
    print()

import pickle; pickle.dump(RES, open('temporal.pkl','wb'))
