"""
Bloco A - pipeline sem vazamento.

Regra: tudo que e estimado a partir dos dados sai exclusivamente das firmas de treino.
  - orientacao, media, desvio, matriz de correlacao e autovetor do PCA
  - padronizacao usada por PLS e arvores
  - quantis de winsorizacao das variaveis do Brito e Assaf (por ano)
  - numero de componentes do PLS (validacao cruzada aninhada dentro do treino)
As firmas de teste nao contribuem com nenhuma observacao, em nenhum exercicio,
para nenhuma dessas estimativas. A avaliacao usa apenas a amostra de estimacao
das firmas de teste.

As estimacoes nao supervisionadas usam todas as observacoes do painel das firmas
de treino, e nao apenas a amostra de risco, o que preserva o desenho original
(PCA sobre o painel) sem vazamento.
"""
import pandas as pd, numpy as np, warnings, pickle
from sklearn.cross_decomposition import PLSRegression
from sklearn.ensemble import HistGradientBoostingClassifier
import statsmodels.api as sm
warnings.filterwarnings('ignore')

import os
U = os.environ.get('DADOS', 'dados').rstrip('/') + '/'
IND = ['LC','CG','ALV','CP','COB','FCO','ROA','EBITDA']
NEG = ['LC','CG','COB','FCO','ROA','EBITDA']
BA = ['X12','X16','X19','X22']

pc = pd.read_csv(U+'painel_completo.csv'); pt = pd.read_csv(U+'painel_transicao.csv'); pi = pd.read_csv(U+'painel_inputs.csv')
m = pc[['CD_CVM','ano']].merge(pi, on=['CD_CVM','ano'], how='left')
P = pc.copy()
P['X12'] = ((m.RES_LUCRO.fillna(0) + m.LUC_ACUM.fillna(0)) / m.ATIVO_TOTAL).values
P['X16'] = P.ALV; P['X19'] = P.CG
P['X22'] = np.where(m.RECEITA_LIQ.isna() | (m.RECEITA_LIQ == 0), np.nan,
    ((m.CAIXA.fillna(0) + m.APLIC_FIN.fillna(0) - m.DIVIDA_CP.fillna(0)) / m.RECEITA_LIQ)).astype(float)
P = P.merge(pt.drop(columns=['DENOM_CIA']), on=['CD_CVM','ano']).sort_values(['CD_CVM','ano']).reset_index(drop=True)
for h in (1, 2):
    P[f'V{h}'] = P.groupby('CD_CVM')['V_entrada'].shift(-h)
    P[f'a{h}'] = P.groupby('CD_CVM')['ano'].shift(-h)
    P.loc[P[f'a{h}'] != P.ano + h, f'V{h}'] = np.nan
P['r2'] = (P.em_risco==1) & (P.groupby('CD_CVM')['em_risco'].shift(-1)==1) & (P.a1==P.ano+1)

def auc(x, y):
    r = pd.Series(x).rank().values; n1 = int(y.sum())
    return (r[y==1].sum() - n1*(n1+1)/2) / (n1*(len(y)-n1))

def folds(firms, k, seed):
    u = np.array(sorted(set(firms))); rg = np.random.default_rng(seed); rg.shuffle(u)
    return {f: i % k for i, f in enumerate(u)}

def orient(df):
    X = df[IND].astype(float).copy(); X[NEG] = -X[NEG]; return X

def unsup_params(train_panel):
    """parametros nao supervisionados estimados SO no painel das firmas de treino"""
    X = orient(train_panel)
    mu, sd = X.mean(), X.std(ddof=1)
    Z = (X - mu) / sd
    C = np.corrcoef(Z.values, rowvar=False)
    ev, vec = np.linalg.eigh(C); o = np.argsort(ev)[::-1]
    v1 = vec[:, o][:, 0]; v1 = v1 if v1.sum() > 0 else -v1
    q = {}
    for c in ['X12','X22']:
        q[c] = train_panel.groupby('ano')[c].quantile([.01,.99]).unstack()
    return mu, sd, v1, q, ev[o]

def apply_z(df, mu, sd): return ((orient(df) - mu) / sd).values

def winsor_ba(df, q):
    out = df[BA].astype(float).copy()
    for c in ['X12','X22']:
        lo = df.ano.map(q[c][0.01]); hi = df.ano.map(q[c][0.99])
        lo = lo.fillna(out[c].min()); hi = hi.fillna(out[c].max())
        out[c] = out[c].clip(lo.values, hi.values)
    return out

def choose_ncomp(Ztr, ytr, firms_tr, seed):
    """validacao cruzada aninhada, apenas dentro do treino"""
    fm = folds(firms_tr, 3, 1000 + seed); fo = np.array([fm[f] for f in firms_tr])
    best, best_auc = 1, -1
    for nc in range(1, 7):
        pr = np.zeros(len(ytr))
        for j in range(3):
            if ytr[fo==j].sum() < 2 or ytr[fo!=j].sum() < 2: continue
            pr[fo==j] = PLSRegression(n_components=nc, scale=False).fit(Ztr[fo!=j], ytr[fo!=j]).predict(Ztr[fo==j]).ravel()
        a = auc(pr, ytr)
        if a > best_auc: best, best_auc = nc, a
    return best

def run(h, seed, k=5):
    yc = f'V{h}'
    if h == 1: E = P[(P.em_risco==1) & P[yc].notna() & P[['X12','X22']].notna().all(axis=1)].copy()
    else:      E = P[P.r2 & P[yc].notna() & P[['X12','X22']].notna().all(axis=1)].copy()
    E = E.reset_index(drop=True)
    fm = folds(P.CD_CVM.values, k, seed)
    P_fold = P.CD_CVM.map(fm).values; E_fold = E.CD_CVM.map(fm).values
    pred = {n: np.zeros(len(E)) for n in ['F','PLS','GB','BA']}
    ncomps = []
    for j in range(k):
        Ptr = P[P_fold != j]
        mu, sd, v1, q, _ = unsup_params(Ptr)
        tr, te = E[E_fold != j], E[E_fold == j]
        Ztr, Zte = apply_z(tr, mu, sd), apply_z(te, mu, sd)
        ytr = tr[yc].values.astype(int)
        pred['F'][E_fold == j] = Zte @ v1
        nc = choose_ncomp(Ztr, ytr, tr.CD_CVM.values, seed); ncomps.append(nc)
        pred['PLS'][E_fold == j] = PLSRegression(n_components=nc, scale=False).fit(Ztr, ytr).predict(Zte).ravel()
        g = HistGradientBoostingClassifier(max_depth=3, max_iter=200, learning_rate=.05,
                min_samples_leaf=40, l2_regularization=1., random_state=seed)
        g.fit(Ztr, ytr); pred['GB'][E_fold == j] = g.predict_proba(Zte)[:, 1]
        Btr = sm.add_constant(winsor_ba(tr, q), has_constant='add')
        Bte = sm.add_constant(winsor_ba(te, q), has_constant='add').reindex(columns=Btr.columns, fill_value=0.)
        pred['BA'][E_fold == j] = sm.Probit(ytr.astype(float), Btr).fit(disp=0, maxiter=300).predict(Bte).values
    pred['COB'] = -E.COB.values; pred['ROA'] = -E.ROA.values
    pred['LC'] = -E.LC.values;   pred['ALV'] = E.ALV.values
    y = E[yc].values.astype(int)
    return E, y, pred, ncomps

out = {}
for h in (1, 2):
    res = {n: [] for n in ['F','PLS','GB','BA','COB','ROA','LC','ALV']}; nc_all = []
    ref = None
    for s in range(1, 11):
        E, y, pred, ncs = run(h, s)
        for n in res: res[n].append(auc(pred[n], y))
        nc_all += ncs
        if s == 1: ref = (E, y, pred)
    out[h] = {'res': res, 'ref': ref, 'ncomps': nc_all}
    print(f'\n{"="*66}\nHORIZONTE h={h}  |  {len(ref[1])} obs, {int(ref[1].sum())} entradas, {ref[0].CD_CVM.nunique()} firmas\n{"="*66}')
    print(f'{"modelo":6s} {"media":>8s} {"dp":>7s} {"min":>7s} {"max":>7s}   referencia')
    for n in ['COB','GB','PLS','ROA','BA','F','LC','ALV']:
        a = np.array(res[n])
        print(f'{n:6s} {a.mean():8.4f} {a.std(ddof=1):7.4f} {a.min():7.4f} {a.max():7.4f}   {a[0]:.4f}')
    vc = pd.Series(nc_all).value_counts().sort_index()
    print('componentes do PLS escolhidos nos 50 folds:', dict(vc))

pickle.dump(out, open('blocoA.pkl', 'wb'))

print(f'\n{"="*66}\nPONTO DE VERIFICACAO: a vantagem da supervisao se mantem?\n{"="*66}')
for h in (1, 2):
    F = np.mean(out[h]['res']['F']); PLS = np.mean(out[h]['res']['PLS'])
    print(f'h={h}: PCA {F:.4f} | PLS {PLS:.4f} | vantagem {PLS-F:+.4f}')
