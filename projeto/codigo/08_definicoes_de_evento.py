import pandas as pd, numpy as np, warnings, pickle
from sklearn.cross_decomposition import PLSRegression
from sklearn.ensemble import HistGradientBoostingClassifier
import statsmodels.api as sm
warnings.filterwarnings('ignore')
exec(open('01_pipeline_sem_vazamento.py').read().split("out = {}")[0])

# evento restritivo: entrada por patrimonio liquido negativo ou recuperacao judicial (sem o criterio de EBITDA)
P['VS1'] = P.groupby('CD_CVM')['V_entrada_sev'].shift(-1); P.loc[P.a1 != P.ano+1, 'VS1'] = np.nan
# criterios em t+1, para a variante que remove apenas as entradas exclusivamente por EBITDA
for c in ['crit_b','crit_c','crit_d_entry']:
    P[c+'_n'] = P.groupby('CD_CVM')[c].shift(-1); P.loc[P.a1 != P.ano+1, c+'_n'] = np.nan
okBA = P[['X12','X22']].notna().all(axis=1)
SPEC = {
 'principal':            (P[(P.em_risco==1) & P.V1.notna() & okBA], 'V1'),
 'sem entradas so EBITDA': (P[(P.em_risco==1) & P.V1.notna() & okBA &
                            ~((P.V1==1) & (P.crit_c_n==1) & (P.crit_b_n!=1) & (P.crit_d_entry_n!=1))], 'V1'),
 'restritiva (PL ou RJ)': (P[(P.em_risco_sev==1) & P.VS1.notna() & okBA], 'VS1'),
}
def run(E, yc, seed, k=5):
    E = E.reset_index(drop=True); fm = folds(P.CD_CVM.values, k, seed)
    Pf = P.CD_CVM.map(fm).values; Ef = E.CD_CVM.map(fm).values
    pr = {n: np.zeros(len(E)) for n in ['F','PLS','GB','BA']}
    for j in range(k):
        mu, sd, v1, q, _ = unsup_params(P[Pf != j])
        tr, te = E[Ef != j], E[Ef == j]; Ztr, Zte = apply_z(tr, mu, sd), apply_z(te, mu, sd)
        ytr = tr[yc].values.astype(int)
        pr['F'][Ef == j] = Zte @ v1
        nc = choose_ncomp(Ztr, ytr, tr.CD_CVM.values, seed)
        pr['PLS'][Ef == j] = PLSRegression(n_components=nc, scale=False).fit(Ztr, ytr).predict(Zte).ravel()
        pr['GB'][Ef == j] = HistGradientBoostingClassifier(max_depth=3, max_iter=200, learning_rate=.05, min_samples_leaf=40,
                              l2_regularization=1., random_state=seed).fit(Ztr, ytr).predict_proba(Zte)[:, 1]
        Btr = sm.add_constant(winsor_ba(tr, q), has_constant='add')
        Bte = sm.add_constant(winsor_ba(te, q), has_constant='add').reindex(columns=Btr.columns, fill_value=0.)
        pr['BA'][Ef == j] = sm.Probit(ytr.astype(float), Btr).fit(disp=0, maxiter=300).predict(Bte).values
    pr['COB'] = -E.COB.values; pr['ROA'] = -E.ROA.values; pr['MEB'] = -E.EBITDA.values
    pr['LC'] = -E.LC.values; pr['ALV'] = E.ALV.values
    return E, E[yc].values.astype(int), pr
def boot(a, b, y, firms, B=2000, seed=7):
    rg = np.random.default_rng(seed); u = np.array(sorted(set(firms))); idx = {f: np.where(firms==f)[0] for f in u}
    d = []
    for _ in range(B):
        s = rg.choice(u, len(u), replace=True); ii = np.concatenate([idx[f] for f in s]); yy = y[ii]
        if yy.sum() < 5 or yy.sum() == len(yy): continue
        d.append(auc(b[ii], yy) - auc(a[ii], yy))
    d = np.array(d); return auc(b,y)-auc(a,y), np.percentile(d,2.5), np.percentile(d,97.5), max(2*min((d<=0).mean(),(d>=0).mean()),1/len(d))

OUT = {}
M = ['F','PLS','GB','BA','COB','ROA','MEB','LC','ALV']
for nome, (E0, yc) in SPEC.items():
    res = {m: [] for m in M}; ref = None
    for s in range(1, 11):
        E, y, pr = run(E0, yc, s)
        for m in M: res[m].append(auc(pr[m], y))
        if s == 1: ref = (E, y, pr)
    E, y, pr = ref
    print(f'\n===== {nome} | {len(y)} obs, {int(y.sum())} entradas, {E.CD_CVM.nunique()} firmas =====')
    print('AUC (media de 10 atribuicoes): ' + ' | '.join(f'{m} {np.mean(res[m]):.3f}' for m in M))
    for m in ['COB','ROA','PLS','GB']:
        o, lo, hi, p = boot(pr['F'], pr[m], y, E.CD_CVM.values)
        print(f'   {m} menos F: {o:+.3f}  IC95 [{lo:+.3f}; {hi:+.3f}]  p {p:.4f}')
    OUT[nome] = {'res': res, 'ref': ref}
pickle.dump(OUT, open('eventos_alternativos.pkl', 'wb'))
