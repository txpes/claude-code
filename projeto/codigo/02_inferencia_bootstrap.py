import pandas as pd, numpy as np, pickle, warnings
from scipy.stats import norm
warnings.filterwarnings('ignore')
out = pickle.load(open('blocoA.pkl','rb'))

def auc(x, y):
    r = pd.Series(x).rank().values; n1 = int(y.sum())
    return (r[y==1].sum() - n1*(n1+1)/2) / (n1*(len(y)-n1))

def boot(a, b, y, firms, B=2000, seed=7):
    rg = np.random.default_rng(seed)
    u = np.array(sorted(set(firms))); idx = {f: np.where(firms==f)[0] for f in u}
    obs = auc(b, y) - auc(a, y); d = []
    for _ in range(B):
        s = rg.choice(u, len(u), replace=True)
        ii = np.concatenate([idx[f] for f in s]); yy = y[ii]
        if yy.sum() < 5 or yy.sum() == len(yy): continue
        d.append(auc(b[ii], yy) - auc(a[ii], yy))
    d = np.array(d)
    p = max(2*min((d <= 0).mean(), (d >= 0).mean()), 1/len(d))
    return obs, np.percentile(d, 2.5), np.percentile(d, 97.5), p

def delong(pa, pb, y):
    m = int(y.sum()); n = len(y) - m
    P1, N1, P2, N2 = pa[y==1], pa[y==0], pb[y==1], pb[y==0]
    a1 = np.array([(np.sum(N1<x) + .5*np.sum(N1==x))/n for x in P1]); a2 = np.array([(np.sum(P1>t) + .5*np.sum(P1==t))/m for t in N1])
    b1 = np.array([(np.sum(N2<x) + .5*np.sum(N2==x))/n for x in P2]); b2 = np.array([(np.sum(P2>t) + .5*np.sum(P2==t))/m for t in N2])
    S = np.cov(np.vstack([a1,b1]))/m + np.cov(np.vstack([a2,b2]))/n
    v = S[0,0] + S[1,1] - 2*S[0,1]
    z = (b1.mean() - a1.mean())/np.sqrt(v) if v > 0 else 0
    return 2*(1 - norm.cdf(abs(z)))

rows = []
for h in (1, 2):
    E, y, pred = out[h]['ref']; firms = E.CD_CVM.values
    # familia H2: escore contra benchmarks (m = 6)
    fam_h2 = ['COB','ROA','BA','LC','ALV','GB']
    for n in fam_h2 + ['PLS']:
        o, lo, hi, p = boot(pred['F'], pred[n], y, firms)
        pdl = delong(pred['F'], pred[n], y)
        rows.append(dict(h=h, comparacao=f'{n} vs F', familia='H4' if n=='PLS' else 'H2',
                         dif=o, lo=lo, hi=hi, p_boot=p, p_delong=pdl))
    # comparacao adicional: arvores contra cobertura de juros
    o, lo, hi, p = boot(pred['COB'], pred['GB'], y, firms)
    rows.append(dict(h=h, comparacao='GB vs COB', familia='teto', dif=o, lo=lo, hi=hi, p_boot=p,
                     p_delong=delong(pred['COB'], pred['GB'], y)))
T = pd.DataFrame(rows)
# Bonferroni sobre os valores do bootstrap agrupado, por familia e horizonte
T['m'] = T.groupby(['h','familia']).comparacao.transform('count')
T['p_bonf'] = (T.p_boot * T.m).clip(upper=1)
pd.set_option('display.width', 200)
for h in (1, 2):
    print(f'\n{"="*96}\nh={h}  |  bootstrap agrupado por firma (2.000 reamostragens) como inferencia principal\n{"="*96}')
    t = T[T.h==h][['comparacao','familia','dif','lo','hi','p_boot','m','p_bonf','p_delong']]
    print(t.to_string(index=False, float_format=lambda x: f'{x:.4f}'))
T.to_csv('blocoD.csv', index=False)

print('\n=== divergencias de conclusao entre bootstrap agrupado e DeLong (a 5%) ===')
for _, r in T.iterrows():
    sb = r.p_bonf < .05; sd = r.p_delong*r.m < .05
    if sb != sd:
        print(f'  h={r.h} {r.comparacao}: bootstrap Bonferroni {r.p_bonf:.4f} | DeLong Bonferroni {min(r.p_delong*r.m,1):.4f}')
