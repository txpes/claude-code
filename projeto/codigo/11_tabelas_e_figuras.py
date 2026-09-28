"""Insumos das tabelas e figuras do artigo, a partir do painel corrente."""
import pandas as pd, numpy as np, warnings, pickle, os, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.stats import ks_2samp, spearmanr
from sklearn.cross_decomposition import PLSRegression
import statsmodels.api as sm
warnings.filterwarnings('ignore')
exec(open('01_pipeline_sem_vazamento.py').read().split("out = {}")[0])
A = pickle.load(open('blocoA.pkl', 'rb'))
T = {}
plt.rcParams.update({'font.family': 'serif', 'font.serif': ['DejaVu Serif'], 'font.size': 9, 'axes.grid': True,
    'grid.alpha': .25, 'grid.linewidth': .5, 'axes.spines.top': False, 'axes.spines.right': False, 'figure.dpi': 200})

# ---------------------------------------------------------------- painel
T['obs'] = len(P); T['firmas'] = P.CD_CVM.nunique(); T['ano_ini'] = int(P.ano.min()); T['ano_fim'] = int(P.ano.max())
T['firmas_ano'] = P.groupby('ano').CD_CVM.nunique().to_dict()
n = P.groupby('CD_CVM').size(); T['exerc_medio'] = n.mean(); T['exerc_mediana'] = n.median()
T['painel_completo_firmas'] = int((n == (T['ano_fim'] - T['ano_ini'] + 1)).sum())

# ---------------------------------------------------------------- eventos
T['vuln'] = int(P.V_estado.sum()); T['vuln_pct'] = P.V_estado.mean()
T['contin'] = int(((P.V_estado == 1) & (P.V_estado_lag == 1)).sum())
T['entradas'] = int(((P.V_estado == 1) & (P.V_estado_lag == 0)).sum())
T['censura'] = int(((P.V_estado == 1) & (P.V_estado_lag.isna())).sum())
T['risco'] = int(P.em_risco.sum()); T['taxa_entrada'] = T['entradas'] / T['risco']
okBA = P[['X12', 'X22']].notna().all(axis=1)
for h in (1, 2):
    E = P[((P.em_risco == 1) if h == 1 else P.r2) & P[f'V{h}'].notna()]
    T[f'est_n{h}'] = len(E); T[f'est_ev{h}'] = int(E[f'V{h}'].sum())
    Ec = E[okBA.reindex(E.index)]
    T[f'com_n{h}'] = len(Ec); T[f'com_ev{h}'] = int(Ec[f'V{h}'].sum()); T[f'com_fi{h}'] = Ec.CD_CVM.nunique()

# ---------------------------------------------------------------- descritivas e correlacao
d = P[IND].astype(float)
T['desc'] = d.describe(percentiles=[.25, .5, .75]).T[['mean', 'std', 'min', '25%', '50%', '75%', 'max']].round(3)
X = orient(P); Z = (X - X.mean()) / X.std(ddof=1)
C = np.corrcoef(Z.values, rowvar=False); T['corr'] = pd.DataFrame(C, index=IND, columns=IND)
ev, vec = np.linalg.eigh(C); o = np.argsort(ev)[::-1]; ev, vec = ev[o], vec[:, o]
v1 = vec[:, 0]; v1 = v1 if v1.sum() > 0 else -v1
T['autovalores'] = ev; T['var_exp'] = ev / len(IND); T['kaiser'] = int((ev > 1).sum())
T['cargas'] = dict(zip(IND, v1)); T['acum3'] = ev[:3].sum() / len(IND)
P['F'] = Z.values @ v1

# ---------------------------------------------------------------- KS, carga, peso PLS e variancia entre firmas
risco = P[P.em_risco == 1]
Eh1 = P[(P.em_risco == 1) & P.V1.notna() & okBA]
pls_full = PLSRegression(n_components=3, scale=False).fit(apply_z(Eh1, X.mean(), X.std(ddof=1)), Eh1.V1.values)
w = np.abs(pls_full.coef_).ravel(); w = w / np.linalg.norm(w) * np.linalg.norm(v1)
linhas = []
for k, c in enumerate(IND):
    ks = ks_2samp(risco.loc[risco.V_entrada == 1, c], risco.loc[risco.V_entrada == 0, c]).statistic
    share = P.groupby('CD_CVM')[c].mean().var() / P[c].var()
    linhas.append(dict(ind=c, ks=ks, carga=abs(v1[k]), peso_pls=w[k], entre=share))
T['diagnostico'] = pd.DataFrame(linhas).sort_values('ks', ascending=False)
for a, b in [('carga', 'ks'), ('entre', 'ks'), ('entre', 'carga')]:
    r = spearmanr(T['diagnostico'][a], T['diagnostico'][b]); T[f'sp_{a}_{b}'] = (r.statistic, r.pvalue)

# ---------------------------------------------------------------- probit
s_ = P.SETOR_ATIV.str.replace(r'^Emp\. Adm\. Part\. - ', '', regex=True).str.strip()
vc = s_.value_counts(); P['setor_ag'] = np.where(s_.isin(vc[vc >= 300].index), s_, 'Outros')
T['setores'] = P.setor_ag.value_counts().to_dict()
for h in (1, 2):
    P[f'E{h}'] = P.groupby('CD_CVM')['V_estado'].shift(-h); P.loc[P[f'a{h}'] != P.ano + h, f'E{h}'] = np.nan
def probit(df, yc, ctrl='completo'):
    Xm = df[['F']].copy()
    if ctrl == 'completo':
        Xm = pd.concat([Xm, df[['log_ativo_real']], pd.get_dummies(df.setor_ag, prefix='s', drop_first=True).astype(float),
                        pd.get_dummies(df.ano, prefix='a', drop_first=True).astype(float)], axis=1)
    elif ctrl == 'porte': Xm = pd.concat([Xm, df[['log_ativo_real']]], axis=1)
    Xm = sm.add_constant(Xm, has_constant='add'); msk = Xm.notna().all(axis=1) & df[yc].notna()
    Xm = Xm[msk].astype(float); y = df.loc[msk, yc].astype(float)
    Xm = Xm[[c for c in Xm.columns if c == 'const' or Xm[c].nunique() > 1]]
    m = sm.Probit(y, Xm).fit(disp=0, maxiter=300)
    try: r = m.get_robustcov_results(cov_type='cluster', groups=df.loc[msk, 'CD_CVM'])
    except Exception: r = m
    j = list(m.model.exog_names).index('F')
    return dict(coef=np.asarray(r.params)[j], ep=np.asarray(r.bse)[j], p=np.asarray(r.pvalues)[j],
                n=len(y), ev=int(y.sum()), k=Xm.shape[1], r2=m.prsquared)
T['probit'] = {lab: probit(df, yc) for lab, df, yc in
   [('trans_h1', P[P.em_risco == 1], 'V1'), ('trans_h2', P[P.r2], 'V2'), ('est_h1', P, 'E1'), ('est_h2', P, 'E2')]}
T['probit_var'] = {c: probit(P[P.em_risco == 1], 'V1', c) for c in ['completo', 'porte', None]}

# ---------------------------------------------------------------- grade: dentro da amostra, com e sem controles
b = P[(P.em_risco == 1) & P.V1.notna() & okBA].copy()
_q = {c: P.groupby('ano')[c].quantile([.01, .99]).unstack() for c in ['X12', 'X22']}   # winsorizacao por ano, percentis 1 e 99
for c in ['X12', 'X22']: b[c] = b[c].clip(b.ano.map(_q[c][0.01]).values, b.ano.map(_q[c][0.99]).values)
def auc_in(df, rhs, ctrl):
    Xm = df[rhs].copy()
    if ctrl: Xm = pd.concat([Xm, df[['log_ativo_real']], pd.get_dummies(df.setor_ag, prefix='s', drop_first=True).astype(float),
                             pd.get_dummies(df.ano, prefix='a', drop_first=True).astype(float)], axis=1)
    Xm = sm.add_constant(Xm, has_constant='add').astype(float)
    Xm = Xm[[c for c in Xm.columns if c == 'const' or Xm[c].nunique() > 1]]
    m = sm.Probit(df.V1.astype(float), Xm).fit(disp=0, maxiter=300)
    return auc(m.predict(Xm).values, df.V1.values.astype(int))
T['grade'] = {nm: {c: auc_in(b, rhs, c) for c in (True, False)} for nm, rhs in
   [('F', ['F']), ('COB', ['COB']), ('ROA', ['ROA']), ('BA', ['X12', 'X16', 'X19', 'X22']), ('LC', ['LC']), ('ALV', ['ALV'])]}

# ---------------------------------------------------------------- minskyana e series
P['c1'] = (P.COB < 1).astype(int); P['ponzi'] = ((P.c1 == 1) & (P.groupby('CD_CVM')['c1'].shift(1) == 1)).astype(int)
T['ponzi_n'] = int(P.ponzi.sum()); T['ponzi_pct'] = P.ponzi.mean()
T['ponzi_serie'] = P.groupby('ano').ponzi.mean().to_dict()
T['serie_entrada'] = P[P.em_risco == 1].groupby('ano').V_entrada.mean().to_dict()
T['serie_estado'] = P.groupby('ano').V_estado.mean().to_dict()
pre, pos = risco[risco.ano <= 2019], risco[risco.ano >= 2020]
T['pre_covid'] = pre.V_entrada.mean(); T['pos_covid'] = pos.V_entrada.mean()

# ---------------------------------------------------------------- figuras
fig, ax = plt.subplots(figsize=(4.6, 3.2))
ax.plot(range(1, 9), ev, 'o-', color='#1f3a5f', lw=1.4, ms=4)
ax.axhline(1, color='#b03030', ls='--', lw=1)
ax.set_xlabel('Componente'); ax.set_ylabel('Autovalor'); ax.set_xticks(range(1, 9))
fig.tight_layout(); fig.savefig('fig1_scree.png', bbox_inches='tight'); plt.close()
E, y, pred = A[1]['ref']
def roc(x, yy):
    o = np.argsort(-x); yy = yy[o]; return np.r_[0, np.cumsum(1 - yy) / (1 - yy).sum()], np.r_[0, np.cumsum(yy) / yy.sum()]
fig, ax = plt.subplots(figsize=(4.3, 4.1))
for nm, k, c, ls in [('Cobertura de juros', 'COB', '#b03030', '--'), ('Árvores impulsionadas', 'GB', '#7a5195', '-.'),
                     ('Mínimos quadrados parciais', 'PLS', '#2e7d32', '-'), ('Componentes principais', 'F', '#1f3a5f', '-')]:
    f_, t_ = roc(pred[k], y); ax.plot(f_, t_, color=c, ls=ls, lw=1.5, label=nm)
ax.plot([0, 1], [0, 1], color='#bbb', lw=.8); ax.set_xlabel('1 − especificidade'); ax.set_ylabel('Sensibilidade')
ax.legend(loc='lower right', fontsize=7.5, frameon=False); fig.tight_layout(); fig.savefig('fig2_roc.png', bbox_inches='tight'); plt.close()
fig, ax = plt.subplots(figsize=(5.4, 3.2))
anos = sorted(T['serie_entrada']); ax.plot(anos, [T['serie_entrada'][a] * 100 for a in anos], 'o-', color='#1f3a5f', lw=1.4, ms=4, label='Entrada, sobre a amostra de risco')
ax.plot(anos, [T['serie_estado'][a] * 100 for a in anos], 's--', color='#b03030', lw=1.4, ms=4, label='Estado, sobre o painel')
ax.set_xlabel('Exercício'); ax.set_ylabel('Percentual'); ax.legend(fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig('fig3_series.png', bbox_inches='tight'); plt.close()

pickle.dump(T, open('tabelas.pkl', 'wb'))
print(f"painel {T['obs']} obs, {T['firmas']} firmas, {T['ano_ini']}-{T['ano_fim']}")
print(f"eventos: {T['vuln']} vulneraveis = {T['contin']} continuacoes + {T['entradas']} entradas + {T['censura']} censuradas")
print(f"risco {T['risco']}, taxa {T['taxa_entrada']*100:.2f}% | estimacao h1 {T['est_n1']}/{T['est_ev1']} | comum h1 {T['com_n1']}/{T['com_ev1']}")
print(f"CP1 {T['var_exp'][0]*100:.2f}%, Kaiser {T['kaiser']}, acumulada tres {T['acum3']*100:.2f}%")
print('cargas:', {k: round(v, 3) for k, v in sorted(T['cargas'].items(), key=lambda x: -x[1])})
print('\ndiagnostico:'); print(T['diagnostico'].round(3).to_string(index=False))
print('spearman carga-ks %.3f (p %.3f) | entre-ks %.3f (p %.3f)' % (*T['sp_carga_ks'], *T['sp_entre_ks']))
print('\nprobit:', {k: (round(v['coef'], 3), round(v['ep'], 3), v['ev'], v['k'], round(v['r2'], 3)) for k, v in T['probit'].items()})
print('grade dentro da amostra:', {k: (round(v[True], 3), round(v[False], 3)) for k, v in T['grade'].items()})
print(f"ponzi {T['ponzi_n']} ({T['ponzi_pct']*100:.1f}%) | pre-covid {T['pre_covid']*100:.2f}% pos {T['pos_covid']*100:.2f}%")
