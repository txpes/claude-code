import pandas as pd, numpy as np, warnings, pickle
from sklearn.cross_decomposition import PLSRegression
import statsmodels.api as sm
warnings.filterwarnings('ignore')
exec(open('01_pipeline_sem_vazamento.py').read().split("out = {}")[0])
A = pickle.load(open('blocoA.pkl','rb'))
E, y, pred = A[1]['ref']
fm = folds(P.CD_CVM.values, 5, 1); Pf = P.CD_CVM.map(fm).values
def efold(df): return df.CD_CVM.map(fm).values

def pca_cols(train_panel, cols):
    X = train_panel[cols].astype(float).copy()
    for c in [c for c in NEG if c in cols]: X[c] = -X[c]
    mu, sd = X.mean(), X.std(ddof=1); Z = (X-mu)/sd
    ev, vec = np.linalg.eigh(np.corrcoef(Z.values, rowvar=False)); o = np.argsort(ev)[::-1]
    vec = vec[:, o]; v1 = vec[:,0]; v1 = v1 if v1.sum() > 0 else -v1
    v2 = vec[:,1]
    if len(cols) == len(V2REF): v2 = v2 if v2 @ V2REF > 0 else -v2   # sinal do CP2 fixo entre particoes
    return mu, sd, v1, v2
def proj(df, cols, mu, sd, w):
    X = df[cols].astype(float).copy()
    for c in [c for c in NEG if c in cols]: X[c] = -X[c]
    return ((X-mu)/sd).values @ w

R = {}
# referencia de sinal para o CP2: o do painel completo, com soma positiva das cargas (o sinal do CP2 e arbitrario)
_X = orient(P); _Z = (_X - _X.mean()) / _X.std(ddof=1); _ev, _vec = np.linalg.eigh(np.corrcoef(_Z.values, rowvar=False))
V2REF = _vec[:, np.argsort(_ev)[::-1]][:, 1]; V2REF = V2REF if V2REF.sum() > 0 else -V2REF
# ---- robustez do escore: sem CP, e CP1+CP2
Ef = efold(E); f7 = np.zeros(len(E)); f12 = np.zeros(len(E)); f12m = np.zeros(len(E))
I7 = [c for c in IND if c != 'CP']
for j in range(5):
    tr_p = P[Pf != j]; te = E[Ef == j]
    mu, sd, v1, _ = pca_cols(tr_p, I7); f7[Ef == j] = proj(te, I7, mu, sd, v1)
    mu, sd, v1, v2 = pca_cols(tr_p, IND); f12[Ef == j] = proj(te, IND, mu, sd, v1) + proj(te, IND, mu, sd, v2)
    f12m[Ef == j] = proj(te, IND, mu, sd, v1) - proj(te, IND, mu, sd, v2)
R['semCP'] = auc(f7, y); R['cp1cp2'] = auc(f12, y); R['cp1mcp2'] = auc(f12m, y); R['F'] = auc(pred['F'], y)
print(f'escore completo {R["F"]:.4f} | sem perfil da divida {R["semCP"]:.4f} | CP1+CP2 {R["cp1cp2"]:.4f} | CP1-CP2 {R["cp1mcp2"]:.4f}')

# ---- sobreviventes: reestimacao sobre a amostra de firmas ativas em 2023
ult = P.groupby('CD_CVM').ano.max(); ativas = set(ult[ult == P.ano.max()].index)
S = E[E.CD_CVM.isin(ativas)].reset_index(drop=True); Sf = efold(S); ys = S.V1.values.astype(int)
sF = np.zeros(len(S)); sP = np.zeros(len(S))
for j in range(5):
    mu, sd, v1, q, _ = unsup_params(P[(Pf != j)])
    tr, te = S[Sf != j], S[Sf == j]
    Ztr, Zte = apply_z(tr, mu, sd), apply_z(te, mu, sd); ytr = tr.V1.values.astype(int)
    sF[Sf == j] = Zte @ v1
    nc = choose_ncomp(Ztr, ytr, tr.CD_CVM.values, 1)
    sP[Sf == j] = PLSRegression(n_components=nc, scale=False).fit(Ztr, ytr).predict(Zte).ravel()
R['sobrev'] = dict(n=len(S), ev=int(ys.sum()), F=auc(sF, ys), PLS=auc(sP, ys), COB=auc(-S.COB.values, ys))
print(f'sobreviventes: n={len(S)} ev={int(ys.sum())} F={R["sobrev"]["F"]:.4f} PLS={R["sobrev"]["PLS"]:.4f} COB={R["sobrev"]["COB"]:.4f}')

# ---- setores: fatias das predicoes fora da amostra da particao de referencia
s_ = E.SETOR_ATIV.str.replace(r'^Emp\. Adm\. Part\. - ', '', regex=True).str.strip().values
R['setor'] = {}
for sec in ['Construção Civil, Mat. Constr. e Decoração', 'Serviços Transporte e Logística', 'Energia Elétrica']:
    k = s_ == sec; yk = y[k]
    if yk.sum() >= 15:
        R['setor'][sec] = dict(n=int(k.sum()), ev=int(yk.sum()), F=auc(pred['F'][k], yk), COB=auc(pred['COB'][k], yk), ROA=auc(pred['ROA'][k], yk))
        print(f'  {sec[:34]:36s} n={k.sum():4d} ev={int(yk.sum()):3d} F={R["setor"][sec]["F"]:.3f} COB={R["setor"][sec]["COB"]:.3f} ROA={R["setor"][sec]["ROA"]:.3f}')

# ---- defasagens, dentro do pipeline limpo
P['am'] = P.groupby('CD_CVM')['ano'].shift(1)
L = E.copy()
for c in ['COB','ROA']:
    lag = P.groupby('CD_CVM')[c].shift(1); lag[P.am != P.ano-1] = np.nan
    L = L.merge(pd.DataFrame({'CD_CVM':P.CD_CVM,'ano':P.ano,c+'_L1':lag}), on=['CD_CVM','ano'], how='left')
lagged_cols = {}
Pl = P.copy()
for c in IND:
    lg = Pl.groupby('CD_CVM')[c].shift(1); lg[Pl.am != Pl.ano-1] = np.nan; Pl[c+'_L1'] = lg
L = E.merge(Pl[['CD_CVM','ano']+[c+'_L1' for c in IND]], on=['CD_CVM','ano'], how='left')
L = L[L[[c+'_L1' for c in IND]].notna().all(axis=1)].reset_index(drop=True)
Lf = efold(L); yl = L.V1.values.astype(int)
def oof_probit(cols_fn):
    o = np.zeros(len(L))
    for j in range(5):
        mu, sd, v1, q, _ = unsup_params(P[Pf != j])
        tr, te = L[Lf != j], L[Lf == j]
        Xtr, Xte = cols_fn(tr, mu, sd, v1), cols_fn(te, mu, sd, v1)
        Xtr = sm.add_constant(Xtr, has_constant='add'); Xte = sm.add_constant(Xte, has_constant='add')
        o[Lf == j] = sm.Probit(tr.V1.values.astype(float), Xtr).fit(disp=0, maxiter=300).predict(Xte)
    return auc(o, yl)
def lagdf(df): d = df.copy(); d[IND] = d[[c+'_L1' for c in IND]].values; return d
fF   = lambda d, mu, sd, v1: (apply_z(d, mu, sd) @ v1).reshape(-1,1)
fFL  = lambda d, mu, sd, v1: np.c_[apply_z(d, mu, sd) @ v1, apply_z(lagdf(d), mu, sd) @ v1]
fFD  = lambda d, mu, sd, v1: np.c_[apply_z(d, mu, sd) @ v1, apply_z(d, mu, sd) @ v1 - apply_z(lagdf(d), mu, sd) @ v1]
fC   = lambda d, mu, sd, v1: d[['COB']].values
fCL  = lambda d, mu, sd, v1: d[['COB','COB_L1']].values
fR   = lambda d, mu, sd, v1: d[['ROA']].values
fRD  = lambda d, mu, sd, v1: np.c_[d.ROA.values, d.ROA.values - d.ROA_L1.values]
R['lag'] = {k: oof_probit(f) for k, f in [('F',fF),('F_L',fFL),('F_D',fFD),('C',fC),('C_L',fCL),('R',fR),('R_D',fRD)]}
pl8 = np.zeros(len(L)); pl16 = np.zeros(len(L))
for j in range(5):
    mu, sd, v1, q, _ = unsup_params(P[Pf != j])
    tr, te = L[Lf != j], L[Lf == j]; ytr = tr.V1.values.astype(int)
    Z8tr, Z8te = apply_z(tr, mu, sd), apply_z(te, mu, sd)
    Z16tr = np.c_[Z8tr, Z8tr - apply_z(lagdf(tr), mu, sd)]; Z16te = np.c_[Z8te, Z8te - apply_z(lagdf(te), mu, sd)]
    pl8[Lf == j] = PLSRegression(n_components=3, scale=False).fit(Z8tr, ytr).predict(Z8te).ravel()
    pl16[Lf == j] = PLSRegression(n_components=3, scale=False).fit(Z16tr, ytr).predict(Z16te).ravel()
R['lag']['P8'] = auc(pl8, yl); R['lag']['P16'] = auc(pl16, yl); R['lag']['n'] = len(L); R['lag']['ev'] = int(yl.sum())
print('defasagens:', {k: round(v,4) if isinstance(v,float) else v for k, v in R['lag'].items()})

# ---- calendario informacional: exposicao do criterio de recuperacao judicial no horizonte de um ano
Pn = P.copy()
for c in ['crit_b','crit_c','crit_d_entry']:
    Pn[c+'_n'] = Pn.groupby('CD_CVM')[c].shift(-1)
Pn.loc[Pn.a1 != Pn.ano+1, ['crit_b_n','crit_c_n','crit_d_entry_n']] = np.nan
Ec = E.merge(Pn[['CD_CVM','ano','crit_b_n','crit_c_n','crit_d_entry_n']], on=['CD_CVM','ano'], how='left')
evs = Ec[Ec.V1 == 1]
so_rj = evs[(evs.crit_d_entry_n == 1) & (evs.crit_b_n != 1) & (evs.crit_c_n != 1)]
com_rj = evs[evs.crit_d_entry_n == 1]
R['cal'] = dict(ev=len(evs), com_rj=len(com_rj), so_rj=len(so_rj))
print(f'calendario: {len(evs)} entradas em t+1 | com RJ em t+1: {len(com_rj)} | exclusivamente por RJ: {len(so_rj)}')
keep = ~((Ec.V1 == 1) & (Ec.crit_d_entry_n == 1) & (Ec.crit_b_n != 1) & (Ec.crit_c_n != 1))
Ek = E[keep.values].reset_index(drop=True); yk = Ek.V1.values.astype(int); Ekf = efold(Ek)
kF = np.zeros(len(Ek)); kP = np.zeros(len(Ek))
for j in range(5):
    mu, sd, v1, q, _ = unsup_params(P[Pf != j])
    tr, te = Ek[Ekf != j], Ek[Ekf == j]; Ztr, Zte = apply_z(tr, mu, sd), apply_z(te, mu, sd); ytr = tr.V1.values.astype(int)
    kF[Ekf == j] = Zte @ v1
    kP[Ekf == j] = PLSRegression(n_components=choose_ncomp(Ztr, ytr, tr.CD_CVM.values, 1), scale=False).fit(Ztr, ytr).predict(Zte).ravel()
R['cal'].update(n=len(Ek), evk=int(yk.sum()), F=auc(kF, yk), PLS=auc(kP, yk), COB=auc(-Ek.COB.values, yk), ROA=auc(-Ek.ROA.values, yk))
print(f'sem entradas exclusivamente por RJ: n={len(Ek)} ev={int(yk.sum())} F={R["cal"]["F"]:.4f} PLS={R["cal"]["PLS"]:.4f} COB={R["cal"]["COB"]:.4f} ROA={R["cal"]["ROA"]:.4f}')
pickle.dump(R, open('robustez.pkl','wb'))
