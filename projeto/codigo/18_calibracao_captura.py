"""Avaliacao complementar: grafico de calibracao por decis e taxa de captura no decil de maior risco.

Usa as mesmas probabilidades fora da amostra do script 14 (calibracao sobre o posto, estimada nas firmas de
treino). Para cada modelo e horizonte:
  - calibracao: firma-anos ordenados pela probabilidade prevista e divididos em dez grupos de igual tamanho;
    em cada grupo, probabilidade media prevista contra frequencia observada de entrada;
  - captura no decil superior: fracao das entradas que caem nos 10% de firma-anos com maior probabilidade
    prevista, com intervalo por bootstrap agrupado por firma (2.000 reamostragens) e diferenca em relacao ao
    escore por componentes principais, sem correcao por multiplicidade (avaliacao complementar)."""
import pickle, numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

src = open('14_metricas_calibradas.py').read().split('res = {}')[0]
exec(src)

MODELOS = ['F', 'COB', 'GB', 'PLS', 'ROA', 'BA']


def captura(p, y, q=.10):
    corte = np.quantile(p, 1 - q)
    return (y[p >= corte]).sum() / y.sum()


def decis(p, y, k=10):
    o = np.argsort(p, kind='mergesort'); g = np.array_split(o, k)
    return np.array([p[i].mean() for i in g]), np.array([y[i].mean() for i in g])


def boot_captura(pa, pb, y, firms, B=2000, seed=7):
    rg = np.random.default_rng(seed)
    u = np.array(sorted(set(firms))); idx = {f: np.where(firms == f)[0] for f in u}
    da, db, dd = [], [], []
    for _ in range(B):
        ii = np.concatenate([idx[f] for f in rg.choice(u, len(u), replace=True)]); yy = y[ii]
        if yy.sum() < 5: continue
        a, b = captura(pa[ii], yy), captura(pb[ii], yy); da.append(a); db.append(b); dd.append(b - a)
    pc = lambda v: (np.percentile(v, 2.5), np.percentile(v, 97.5))
    return pc(da), pc(db), pc(dd)


res = {}
for h in (1, 2):
    yc = f'V{h}'
    E = (P[(P.em_risco == 1) & P[yc].notna() & P[['X12', 'X22']].notna().all(axis=1)] if h == 1 else
         P[P.r2 & P[yc].notna() & P[['X12', 'X22']].notna().all(axis=1)]).copy().reset_index(drop=True)
    y, prob, ops, piso = run(h)
    firms = E.CD_CVM.values
    res[h] = {'_n': len(y), '_eventos': int(y.sum()), '_prev': y.mean()}
    print(f'\n===== h={h} | {len(y)} firma-anos, {int(y.sum())} entradas =====')
    print(f'{"modelo":5s} {"captura":>8s} {"IC95":>17s} {"dif-F":>7s} {"IC95 dif":>17s} {"decil sup obs":>13s} {"prev media":>10s}')
    for n in MODELOS:
        c = captura(prob[n], y); pm, ob = decis(prob[n], y)
        (lo_a, hi_a), (lo, hi), (dlo, dhi) = boot_captura(prob['F'], prob[n], y, firms)
        res[h][n] = dict(captura=c, ic=(lo, hi), dif=c - captura(prob['F'], y), ic_dif=(dlo, dhi),
                         prev_decil=pm, obs_decil=ob)
        print(f'{n:5s} {c:8.3f} [{lo:.3f}; {hi:.3f}] {c - captura(prob["F"], y):+7.3f} [{dlo:+.3f}; {dhi:+.3f}] {ob[-1]:13.3f} {pm[-1]:10.3f}')
pickle.dump(res, open('calibracao_captura.pkl', 'wb'))

# Figura: calibracao por decis, dois horizontes lado a lado, mesmas escalas
COR = {'F': '#2a78d6', 'COB': '#eb6834', 'GB': '#1baf7a'}
ROT = {'F': 'Componentes principais', 'COB': 'Cobertura de juros', 'GB': 'Árvores impulsionadas'}
MARC = {'F': 'o', 'COB': 's', 'GB': '^'}
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})
fig, axs = plt.subplots(1, 2, figsize=(10, 4.6), sharex=True, sharey=True)
lim = max(max(res[h][n]['obs_decil'].max(), res[h][n]['prev_decil'].max()) for h in (1, 2) for n in COR) * 1.08
for ax, h in zip(axs, (1, 2)):
    ax.plot([0, lim], [0, lim], color='#9a9a9a', lw=1, ls='--', zorder=1, label='Calibração perfeita')
    for n in COR:
        pm, ob = res[h][n]['prev_decil'], res[h][n]['obs_decil']
        ax.plot(pm, ob, color=COR[n], lw=2, marker=MARC[n], ms=6, mec='white', mew=1.2, label=ROT[n], zorder=3)
    ax.set_xlim(0, lim); ax.set_ylim(0, lim)
    ax.set_title(f'Horizonte de {"um ano" if h == 1 else "dois anos"}', fontsize=11)
    ax.set_xlabel('Probabilidade média prevista no decil')
    ax.grid(color='#ececec', lw=.8); ax.set_axisbelow(True)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
axs[0].set_ylabel('Frequência observada de entrada')
h_, l_ = axs[0].get_legend_handles_labels()
fig.legend(h_[1:] + h_[:1], l_[1:] + l_[:1], loc='lower center', ncol=4, frameon=False, bbox_to_anchor=(.5, -.01))
fig.tight_layout(rect=(0, .07, 1, 1))
fig.savefig('fig_calibracao.png', dpi=200, bbox_inches='tight')
print('fig_calibracao.png')
