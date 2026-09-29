"""Tabela 17 revisada: metricas de probabilidade com calibracao sobre o posto.

Mesmo desenho do script 03 (calibracao e limiares estimados nas firmas de treino, sobre predicoes
fora de particoes internas para os modelos supervisionados). A unica diferenca e a calibracao: a
regressao logistica e ajustada sobre o posto do escore na distribuicao do treino, e nao sobre o escore
bruto. A transformacao e monotona, de modo que a ordenacao e a AUC nao mudam, mas evita as
probabilidades extremas que a logistica linear produz sobre escores de caudas longas (ROA, cobertura).
Como verificacao, reporta tambem o Brier sob calibracao isotonica."""
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
from sklearn.isotonic import IsotonicRegression
def _posto(ref, x):
    srt = np.sort(ref); return (np.searchsorted(srt, x, side='left') + np.searchsorted(srt, x, side='right')) / (2 * len(srt))
def platt(s_tr, y_tr, s_te):
    r_tr, r_te = _posto(s_tr, s_tr), _posto(s_tr, s_te)
    lr = LogisticRegression(C=1e6, max_iter=1000).fit(r_tr.reshape(-1,1), y_tr)
    return lr.predict_proba(r_te.reshape(-1,1))[:,1], lr.predict_proba(r_tr.reshape(-1,1))[:,1]
def isot(s_tr, y_tr, s_te):
    return IsotonicRegression(out_of_bounds='clip', y_min=1e-4, y_max=1-1e-4).fit(s_tr, y_tr).predict(s_te)
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
    prob = {n: np.zeros(len(E)) for n in names}; piso = {n: np.zeros(len(E)) for n in names}; ops = {n: {50: np.zeros(len(E),bool), 80: np.zeros(len(E),bool)} for n in names}
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
            p_te, p_tr = platt(s_tr[n], ytr, s_te[n]); prob[n][Ef == j] = p_te; piso[n][Ef == j] = isot(s_tr[n], ytr, s_te[n])
            for sens in (50, 80):
                t = np.quantile(p_tr[ytr==1], 1-sens/100); ops[n][sens][Ef == j] = p_te >= t
    return E[yc].values.astype(int), prob, ops, piso

res = {}
for h in (1, 2):
    y, prob, ops, piso = run(h); prev = y.mean(); res[h] = {'_prev': prev, '_brier_ref': prev*(1-prev)}
    print(f'\n===== h={h} | prevalencia {prev:.4f} | Brier ref {prev*(1-prev):.4f} =====')
    print(f'{"modelo":5s} {"PR-AUC":>7s} {"Brier":>7s} {"B.iso":>7s} {"incl":>6s} {"intercep":>9s} {"sens":>6s} {"espec":>6s} {"VPP":>6s} {"VPN":>6s} {"sinal":>6s} {"DL10":>8s}')
    for n in ['COB','GB','PLS','ROA','BA','F']:
        sl, it = slope_int(prob[n], y); br = brier_score_loss(y, prob[n]); pr = average_precision_score(y, prob[n])
        f80 = ops[n][80]; se80 = (f80 & (y==1)).sum()/(y==1).sum()
        row = dict(pr_auc=pr, brier=br, brier_iso=brier_score_loss(y, piso[n]), incl=sl, intercepto=it,
                   nb5=nb(prob[n],y,5), nb10=nb(prob[n],y,10), nb20=nb(prob[n],y,20))
        for a in (50, 80):
            f_ = ops[n][a]; tp=(f_&(y==1)).sum(); fp=(f_&(y==0)).sum(); fn=(~f_&(y==1)).sum(); tn=(~f_&(y==0)).sum()
            row[a] = dict(sens=tp/(tp+fn), espec=tn/(tn+fp), vpp=tp/(tp+fp) if tp+fp else np.nan, vpn=tn/(tn+fn), sinalizadas=f_.mean())
        res[h][n] = row; o = row[80]
        print(f'{n:5s} {pr:7.4f} {br:7.4f} {row["brier_iso"]:7.4f} {sl:6.3f} {it:+9.3f} {o["sens"]:6.3f} {o["espec"]:6.3f} {o["vpp"]:6.3f} {o["vpn"]:6.4f} {o["sinalizadas"]:6.3f} {row["nb10"]:+8.4f}')
    tudo = prev - (1 - prev) / 10          # decisao liquida de sinalizar todos, 10:1
    print(f'referencia constante: Brier {prev*(1-prev):.4f} | PR-AUC {prev:.4f} | decisao liquida 10:1 sinalizar todos {tudo:+.4f}, nenhum 0')
pickle.dump(res, open('blocoG3.pkl','wb'))
