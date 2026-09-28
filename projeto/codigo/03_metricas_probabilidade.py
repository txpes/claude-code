"""Calibracao e limiares estimados em predicoes fora da particao DENTRO do treino (aninhado),
comparados ao procedimento original, que usava as predicoes ajustadas no proprio treino."""
import pandas as pd, numpy as np, warnings, pickle
from sklearn.cross_decomposition import PLSRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss
import statsmodels.api as sm
warnings.filterwarnings('ignore')
exec(open('01_pipeline_sem_vazamento.py').read().split("out = {}")[0])

def gbm(seed): return HistGradientBoostingClassifier(max_depth=3, max_iter=200, learning_rate=.05,
                                                      min_samples_leaf=40, l2_regularization=1., random_state=seed)
def platt(s_tr, y_tr, s_te):
    lr = LogisticRegression(C=1e6, max_iter=1000).fit(s_tr.reshape(-1,1), y_tr)
    return lr.predict_proba(s_te.reshape(-1,1))[:,1], lr.predict_proba(s_tr.reshape(-1,1))[:,1]
def slope_int(p, y):
    lp = np.log(np.clip(p,1e-6,1-1e-6)/(1-np.clip(p,1e-6,1-1e-6)))
    return sm.Logit(y, sm.add_constant(lp)).fit(disp=0).params[1], sm.Logit(y, np.ones_like(lp), offset=lp).fit(disp=0).params[0]
def nb(p, y, r): pt = 1/(1+r); pos = p >= pt; return ((pos&(y==1)).sum() - (pos&(y==0)).sum()*pt/(1-pt))/len(y)

def run(h, seed=1, k=5):
    yc = f'V{h}'
    E = (P[(P.em_risco==1)&P[yc].notna()&P[['X12','X22']].notna().all(axis=1)] if h==1 else
         P[P.r2&P[yc].notna()&P[['X12','X22']].notna().all(axis=1)]).copy().reset_index(drop=True)
    fm = folds(P.CD_CVM.values, k, seed); Pf = P.CD_CVM.map(fm).values; Ef = E.CD_CVM.map(fm).values
    names = ['F','PLS','GB','BA','COB','ROA']
    prob = {n: np.zeros(len(E)) for n in names}; ops = {n: {50: np.zeros(len(E),bool), 80: np.zeros(len(E),bool)} for n in names}
    for j in range(k):
        mu, sd, v1, q, _ = unsup_params(P[Pf != j])
        tr, te = E[Ef != j].reset_index(drop=True), E[Ef == j]
        Ztr, Zte = apply_z(tr, mu, sd), apply_z(te, mu, sd); ytr = tr[yc].values.astype(int)
        nc = choose_ncomp(Ztr, ytr, tr.CD_CVM.values, seed)
        # escores de teste: modelos ajustados em todo o treino
        pl = PLSRegression(n_components=nc, scale=False).fit(Ztr, ytr); g = gbm(seed).fit(Ztr, ytr)
        Btr = sm.add_constant(winsor_ba(tr, q), has_constant='add')
        Bte = sm.add_constant(winsor_ba(te, q), has_constant='add').reindex(columns=Btr.columns, fill_value=0.)
        bm = sm.Probit(ytr.astype(float), Btr).fit(disp=0, maxiter=300)
        s_te = {'F': Zte@v1, 'PLS': pl.predict(Zte).ravel(), 'GB': g.predict_proba(Zte)[:,1],
                'BA': bm.predict(Bte).values, 'COB': -te.COB.values, 'ROA': -te.ROA.values}
        # escores de calibracao no treino: fora da particao interna para os modelos supervisionados
        fi = folds(tr.CD_CVM.values, 3, 2000+seed); fo = np.array([fi[f] for f in tr.CD_CVM.values])
        s_tr = {'F': Ztr@v1, 'COB': -tr.COB.values, 'ROA': -tr.ROA.values,
                'PLS': np.zeros(len(tr)), 'GB': np.zeros(len(tr)), 'BA': np.zeros(len(tr))}
        for i in range(3):
            a, b = fo != i, fo == i
            s_tr['PLS'][b] = PLSRegression(n_components=nc, scale=False).fit(Ztr[a], ytr[a]).predict(Ztr[b]).ravel()
            s_tr['GB'][b] = gbm(seed).fit(Ztr[a], ytr[a]).predict_proba(Ztr[b])[:,1]
            s_tr['BA'][b] = sm.Probit(ytr[a].astype(float), Btr[a]).fit(disp=0, maxiter=300).predict(Btr[b])
        for n in names:
            p_te, p_tr = platt(s_tr[n], ytr, s_te[n]); prob[n][Ef == j] = p_te
            for sens in (50, 80):
                t = np.quantile(p_tr[ytr==1], 1-sens/100); ops[n][sens][Ef == j] = p_te >= t
    return E[yc].values.astype(int), prob, ops

res = {}
for h in (1, 2):
    y, prob, ops = run(h); prev = y.mean(); res[h] = {}
    print(f'\n===== h={h} | prevalencia {prev:.4f} | Brier ref {prev*(1-prev):.4f} =====')
    print(f'{"modelo":5s} {"PR-AUC":>7s} {"Brier":>7s} {"incl":>6s} {"intercep":>9s} {"sens80":>7s}')
    for n in ['COB','GB','PLS','ROA','BA','F']:
        sl, it = slope_int(prob[n], y); br = brier_score_loss(y, prob[n]); pr = average_precision_score(y, prob[n])
        f80 = ops[n][80]; se80 = (f80 & (y==1)).sum()/(y==1).sum()
        print(f'{n:5s} {pr:7.4f} {br:7.4f} {sl:6.3f} {it:+9.3f} {se80:7.3f}')
        row = dict(pr_auc=pr, brier=br, incl=sl, intercepto=it, nb5=nb(prob[n],y,5), nb10=nb(prob[n],y,10), nb20=nb(prob[n],y,20))
        for a in (50, 80):
            f_ = ops[n][a]; tp=(f_&(y==1)).sum(); fp=(f_&(y==0)).sum(); fn=(~f_&(y==1)).sum(); tn=(~f_&(y==0)).sum()
            row[a] = dict(sens=tp/(tp+fn), espec=tn/(tn+fp), vpp=tp/(tp+fp) if tp+fp else np.nan, vpn=tn/(tn+fn), sinalizadas=f_.mean())
        res[h][n] = row
    print('decisao liquida 10:1:', {n: round(res[h][n]['nb10'],4) for n in ['COB','GB','PLS','ROA','BA','F']})
pickle.dump(res, open('blocoG2.pkl','wb'))
