"""
Escore restrito aos tres indicadores de maior poder discriminante (pergunta da coorientacao).

Os tres sao o retorno sobre ativos, a cobertura de juros e a margem EBITDA, os de maior estatistica de
Kolmogorov-Smirnov na Tabela 16 (13 na versao final). A pergunta e se a agregacao se justifica quando se
agregam apenas os melhores componentes, e nao os oito.

Duas agregacoes nao supervisionadas, com o mesmo pipeline sem vazamento do script 01:
  F3 - primeiro componente principal dos tres indicadores, estimado no painel das firmas de treino;
  M3 - media simples dos tres indicadores padronizados pelos parametros do treino (pesos iguais).
A escolha do trio usa a estatistica KS sobre toda a amostra de risco, e portanto o desfecho. Para
separar esse efeito, F3sel refaz a escolha em cada particao, pelos tres maiores KS nas firmas de treino.
Comparacoes na atribuicao de referencia, com bootstrap agrupado por firma; medias sobre dez atribuicoes;
decomposicao pelos tres subconjuntos puros, sempre reportados juntos e com o numero de entradas.
"""
import os, pickle, warnings
import numpy as np, pandas as pd
from scipy.stats import ks_2samp
warnings.filterwarnings('ignore')

U = os.environ.get('DADOS', 'dados').rstrip('/') + '/'
IND = ['LC', 'CG', 'ALV', 'CP', 'COB', 'FCO', 'ROA', 'EBITDA']
NEG = ['LC', 'CG', 'COB', 'FCO', 'ROA', 'EBITDA']
TRIO = ['ROA', 'COB', 'EBITDA']

pc = pd.read_csv(U + 'painel_completo.csv'); pt = pd.read_csv(U + 'painel_transicao.csv'); pi = pd.read_csv(U + 'painel_inputs.csv')
m = pc[['CD_CVM', 'ano']].merge(pi, on=['CD_CVM', 'ano'], how='left')
P = pc.copy()
P['X12'] = ((m.RES_LUCRO.fillna(0) + m.LUC_ACUM.fillna(0)) / m.ATIVO_TOTAL).values
P['X22'] = np.where(m.RECEITA_LIQ.isna() | (m.RECEITA_LIQ == 0), np.nan,
                    ((m.CAIXA.fillna(0) + m.APLIC_FIN.fillna(0) - m.DIVIDA_CP.fillna(0)) / m.RECEITA_LIQ)).astype(float)
P = P.merge(pt.drop(columns=['DENOM_CIA']), on=['CD_CVM', 'ano']).sort_values(['CD_CVM', 'ano']).reset_index(drop=True)
for h in (1, 2):
    P[f'V{h}'] = P.groupby('CD_CVM')['V_entrada'].shift(-h)
    P[f'a{h}'] = P.groupby('CD_CVM')['ano'].shift(-h)
    P.loc[P[f'a{h}'] != P.ano + h, f'V{h}'] = np.nan
    for k in ['crit_b', 'crit_c', 'crit_d_entry']:
        P[f'{k}_h{h}'] = P.groupby('CD_CVM')[k].shift(-h); P.loc[P[f'a{h}'] != P.ano + h, f'{k}_h{h}'] = np.nan
P['r2'] = (P.em_risco == 1) & (P.groupby('CD_CVM')['em_risco'].shift(-1) == 1) & (P.a1 == P.ano + 1)


def auc(x, y):
    r = pd.Series(x).rank().values; n1 = int(y.sum())
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))


def folds(firms, k, seed):
    u = np.array(sorted(set(firms))); rg = np.random.default_rng(seed); rg.shuffle(u)
    return {f: i % k for i, f in enumerate(u)}


def orient(df, cols):
    X = df[cols].astype(float).copy()
    for c in cols:
        if c in NEG: X[c] = -X[c]
    return X


def pc1(train_panel, cols):
    X = orient(train_panel, cols); mu, sd = X.mean(), X.std(ddof=1)
    ev, vec = np.linalg.eigh(np.corrcoef(((X - mu) / sd).values, rowvar=False))
    v = vec[:, np.argmax(ev)]; v = v if v.sum() > 0 else -v
    return mu, sd, v, ev.max() / ev.sum()


def boot(a, b, y, f, B=2000, seed=7, minimo=5):
    rg = np.random.default_rng(seed); u = np.array(sorted(set(f))); idx = {x: np.where(f == x)[0] for x in u}; d = []
    for _ in range(B):
        s = rg.choice(u, len(u), replace=True); ii = np.concatenate([idx[x] for x in s]); yy = y[ii]
        if yy.sum() < minimo or yy.sum() == len(yy): continue
        d.append(auc(b[ii], yy) - auc(a[ii], yy))
    d = np.array(d); p = max(2 * min((d <= 0).mean(), (d >= 0).mean()), 1 / len(d))
    return auc(b, y) - auc(a, y), np.percentile(d, 2.5), np.percentile(d, 97.5), p


def run(h, seed, k=5):
    yc = f'V{h}'
    if h == 1: E = P[(P.em_risco == 1) & P[yc].notna() & P[['X12', 'X22']].notna().all(axis=1)].copy()
    else:      E = P[P.r2 & P[yc].notna() & P[['X12', 'X22']].notna().all(axis=1)].copy()
    E = E.reset_index(drop=True)
    fm = folds(P.CD_CVM.values, k, seed)
    P_fold = P.CD_CVM.map(fm).values; E_fold = E.CD_CVM.map(fm).values
    pred = {n: np.zeros(len(E)) for n in ['F3', 'M3', 'F3sel']}; trios, var1 = [], []
    for j in range(k):
        Ptr = P[P_fold != j]; te = E[E_fold == j]; tr = E[E_fold != j]
        mu, sd, v, share = pc1(Ptr, TRIO); var1.append(share)
        Zte = ((orient(te, TRIO) - mu) / sd).values
        pred['F3'][E_fold == j] = Zte @ v
        pred['M3'][E_fold == j] = Zte.mean(axis=1)
        # escolha do trio dentro do treino: tres maiores KS nas firmas de treino
        ytr = tr[yc].values.astype(int); Xtr = orient(tr, IND)
        ks = {c: ks_2samp(Xtr[c][ytr == 1], Xtr[c][ytr == 0]).statistic for c in IND}
        sel = sorted(ks, key=ks.get, reverse=True)[:3]; trios.append(tuple(sorted(sel)))
        mu_s, sd_s, v_s, _ = pc1(Ptr, sel)
        pred['F3sel'][E_fold == j] = ((orient(te, sel) - mu_s) / sd_s).values @ v_s
    pred['MEB'] = -E.EBITDA.values
    return E, E[yc].values.astype(int), pred, trios, var1


A = pickle.load(open('blocoA.pkl', 'rb'))
OUT = {}
for h in (1, 2):
    res = {n: [] for n in ['F3', 'M3', 'F3sel', 'MEB']}; trios_all, var_all = [], []
    for s in range(1, 11):
        E, y, pred, trios, var1 = run(h, s)
        for n in res: res[n].append(auc(pred[n], y))
        trios_all += trios; var_all += var1
        if s == 1: ref = (E, y, pred)
    E, y, pred = ref
    Ea, ya, pa = A[h]['ref']
    assert len(Ea) == len(E) and (Ea.CD_CVM.values == E.CD_CVM.values).all() and (Ea.ano.values == E.ano.values).all()
    pred.update({m: pa[m] for m in ['F', 'PLS', 'COB', 'ROA', 'GB']})
    firms = E.CD_CVM.values
    o = dict(n=len(y), ev=int(y.sum()), ref={m: auc(pred[m], y) for m in pred},
             media={m: float(np.mean(v)) for m, v in res.items()}, dp={m: float(np.std(v, ddof=1)) for m, v in res.items()},
             trios=pd.Series(trios_all).value_counts().to_dict(), var1=float(np.mean(var_all)))
    o['cmp'] = {f'{b} vs {a}': boot(pred[a], pred[b], y, firms) for a, b in
                [('F', 'F3'), ('F', 'M3'), ('F3', 'COB'), ('F3', 'ROA'), ('F3', 'PLS'), ('M3', 'COB'), ('F3', 'F3sel')]}
    # subconjuntos puros: os tres, sempre juntos
    Ec = E                                   # E ja traz os criterios de t + h, vindos de P
    b_, c_, d_ = (Ec[f'crit_b_h{h}'] == 1).values, (Ec[f'crit_c_h{h}'] == 1).values, (Ec[f'crit_d_entry_h{h}'] == 1).values
    o['puros'] = {}
    for nome, msk in {'EBITDA puras': c_ & ~b_ & ~d_, 'PL puras': b_ & ~c_ & ~d_, 'RJ puras': d_ & ~b_ & ~c_}.items():
        kk = (y == 0) | (msk & (y == 1)); yk = y[kk]
        r = dict(n=int(yk.sum()), auc={m: auc(pred[m][kk], yk) for m in ['F', 'F3', 'M3', 'COB', 'PLS']})
        r['COB vs F3'] = boot(pred['F3'][kk], pred['COB'][kk], yk, firms[kk], minimo=4)
        r['F3 vs F'] = boot(pred['F'][kk], pred['F3'][kk], yk, firms[kk], minimo=4)
        o['puros'][nome] = r
    OUT[h] = o

pickle.dump(OUT, open('tres_indicadores.pkl', 'wb'))
for h in (1, 2):
    o = OUT[h]
    print(f'\n{"=" * 70}\nh={h} | {o["n"]} obs, {o["ev"]} entradas | variancia do CP1 dos tres: {o["var1"]:.3f}\n{"=" * 70}')
    print('atribuicao de referencia:', ' '.join(f'{m} {v:.3f}' for m, v in o['ref'].items()))
    print('media de dez atribuicoes:', ' '.join(f'{m} {o["media"][m]:.3f} ({o["dp"][m]:.3f})' for m in o['media']))
    print('trios escolhidos dentro do treino (50 particoes):', o['trios'])
    for k, (d, lo, hi, p) in o['cmp'].items(): print(f'  {k:14s} {d:+.3f} [{lo:+.3f}; {hi:+.3f}] p={p:.3f}')
    for nome, r in o['puros'].items():
        print(f'  {nome:13s} n={r["n"]:3d} ' + ' '.join(f'{m} {v:.3f}' for m, v in r['auc'].items()) +
              ' | COB-F3 {:+.3f} [{:+.3f}; {:+.3f}]'.format(*r['COB vs F3'][:3]) + ' | F3-F {:+.3f} [{:+.3f}; {:+.3f}]'.format(*r['F3 vs F'][:3]))
