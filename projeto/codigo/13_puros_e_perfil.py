import pandas as pd, numpy as np, pickle, warnings
warnings.filterwarnings('ignore')
import os
D = os.environ.get('DADOS', 'dados').rstrip('/') + '/'
c = pd.read_csv(D + 'painel_completo.csv'); t = pd.read_csv(D + 'painel_transicao.csv'); ip = pd.read_csv(D + 'painel_inputs.csv')
P = c.merge(t.drop(columns=['DENOM_CIA']), on=['CD_CVM', 'ano']).sort_values(['CD_CVM', 'ano']).reset_index(drop=True)
for h in (1, 2):
    P[f'a{h}'] = P.groupby('CD_CVM').ano.shift(-h)
    P[f'V{h}'] = P.groupby('CD_CVM')['V_entrada'].shift(-h); P.loc[P[f'a{h}'] != P.ano + h, f'V{h}'] = np.nan
    for k in ['crit_b', 'crit_c', 'crit_d_entry']:
        P[f'{k}_h{h}'] = P.groupby('CD_CVM')[k].shift(-h); P.loc[P[f'a{h}'] != P.ano + h, f'{k}_h{h}'] = np.nan
P['r2'] = (P.em_risco == 1) & (P.groupby('CD_CVM')['em_risco'].shift(-1) == 1) & (P.a1 == P.ano + 1)
A = pickle.load(open('blocoA.pkl', 'rb'))
def auc(x, y):
    r = pd.Series(x).rank().values; n1 = int(y.sum()); return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))
def boot(a, b, y, f, B=2000, seed=7):
    rg = np.random.default_rng(seed); u = np.array(sorted(set(f))); idx = {x: np.where(f == x)[0] for x in u}; d = []
    for _ in range(B):
        s = rg.choice(u, len(u), replace=True); ii = np.concatenate([idx[x] for x in s]); yy = y[ii]
        if yy.sum() < 4 or yy.sum() == len(yy): continue
        d.append(auc(b[ii], yy) - auc(a[ii], yy))
    d = np.array(d); return auc(b, y) - auc(a, y), np.percentile(d, 2.5), np.percentile(d, 97.5)
OUT = {}
for h in (1, 2):
    E, y, pred = A[h]['ref']
    Ec = E.merge(P[['CD_CVM', 'ano'] + [f'{k}_h{h}' for k in ['crit_b', 'crit_c', 'crit_d_entry']]], on=['CD_CVM', 'ano'], how='left')
    b_, c_, d_ = (Ec[f'crit_b_h{h}'] == 1).values, (Ec[f'crit_c_h{h}'] == 1).values, (Ec[f'crit_d_entry_h{h}'] == 1).values
    puros = {'EBITDA puras': c_ & ~b_ & ~d_, 'PL puras': b_ & ~c_ & ~d_, 'RJ puras': d_ & ~b_ & ~c_}
    for nome, msk in puros.items():
        k = (y == 0) | (msk & (y == 1)); yk = y[k]
        if yk.sum() < 5: OUT[(h, nome)] = dict(n=int(yk.sum())); continue
        o = dict(n=int(yk.sum()), F=auc(pred['F'][k], yk))
        for m in ['COB', 'ROA', 'PLS', 'GB']:
            dif, lo, hi = boot(pred['F'][k], pred[m][k], yk, E.CD_CVM.values[k]); o[m] = (auc(pred[m][k], yk), dif, lo, hi)
        OUT[(h, nome)] = o
    # amplitude do intervalo como medida de poder, por tipo
    for nome, msk in {'RJ': d_, 'PL': b_, 'EBITDA excl': c_ & ~b_ & ~d_}.items():
        k = (y == 0) | (msk & (y == 1)); yk = y[k]
        if yk.sum() < 5: continue
        _, lo, hi = boot(pred['F'][k], pred['COB'][k], yk, E.CD_CVM.values[k])
        OUT[(h, nome + ' amplitude')] = hi - lo
print('=== subconjuntos puros ===')
for (h, nome), v in OUT.items():
    if 'amplitude' in nome: continue
    if 'F' not in v: print(f'h={h} {nome:14s} n={v["n"]} (poucos eventos)'); continue
    print(f'h={h} {nome:14s} n={v["n"]:3d} F={v["F"]:.3f} | ' + ' | '.join(
        f'{m} {v[m][0]:.3f} ({v[m][1]:+.3f} [{v[m][2]:+.3f};{v[m][3]:+.3f}])' for m in ['COB', 'ROA', 'PLS']))
print('\n=== amplitude do intervalo de confianca, escore contra cobertura ===')
for (h, nome), v in OUT.items():
    if 'amplitude' in nome: print(f'h={h} {nome:22s} {v:.3f}')
pickle.dump(OUT, open('puros.pkl', 'wb'))
# perfil das firmas por tipo de entrada, no horizonte de dois anos
E2 = P[P.r2 & P.V2.notna()]
eb = ((E2.crit_c_h2 == 1) & (E2.crit_b_h2 != 1) & (E2.crit_d_entry_h2 != 1)).values
pl = (E2.crit_b_h2 == 1).values; nao = (E2.V2 == 0).values
perfil = {}
for v in ['ALV', 'LC', 'CG', 'COB', 'ROA', 'EBITDA', 'log_ativo_real']:
    perfil[v] = (E2.loc[eb & (E2.V2 == 1).values, v].median(), E2.loc[pl & (E2.V2 == 1).values, v].median(), E2.loc[nao, v].median())
perfil['n'] = (int((eb & (E2.V2 == 1).values).sum()), int((pl & (E2.V2 == 1).values).sum()), int(nao.sum()))
pickle.dump(perfil, open('perfil.pkl', 'wb'))
print('\nperfil (EBITDA, PL, nao eventos):', {k: tuple(round(x, 3) for x in v) for k, v in perfil.items()})

# Figura 3 - desempenho fora da amostra por rota de deterioracao (subconjuntos puros)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.family': 'serif', 'font.serif': ['DejaVu Serif'], 'font.size': 9, 'axes.grid': True, 'grid.alpha': .25,
    'grid.linewidth': .5, 'axes.spines.top': False, 'axes.spines.right': False, 'figure.dpi': 200})
rotas = [('EBITDA puras', 'Prejuízo operacional'), ('PL puras', 'Patrimônio negativo'), ('RJ puras', 'Recuperação judicial')]
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.3), sharey=True)
for ax, h in zip(axs, (1, 2)):
    xs = np.arange(len(rotas)); w = .2
    for i, (m, lab, cor) in enumerate([('F', 'Componentes principais', '#1f3a5f'), ('COB', 'Cobertura de juros', '#b03030'),
                                       ('PLS', 'Mínimos quadrados parciais', '#2e7d32'), ('GB', 'Árvores impulsionadas', '#7a5195')]):
        vals = [OUT[(h, r)]['F'] if m == 'F' else OUT[(h, r)][m][0] if 'F' in OUT[(h, r)] else np.nan for r, _ in rotas]
        ax.bar(xs + (i - 1.5) * w, vals, w, color=cor, label=lab)
    ax.axhline(.5, color='#888', ls='--', lw=.8); ax.set_xticks(xs); ax.set_xticklabels([r[1].replace(' ', '\n', 1) for r in rotas], fontsize=7.5)
    ax.set_title('Horizonte de um ano' if h == 1 else 'Horizonte de dois anos', fontsize=9); ax.set_ylim(.3, 1)
axs[0].set_ylabel('Área sob a curva ROC')
h_, l_ = axs[0].get_legend_handles_labels()
fig.legend(h_, l_, fontsize=7.5, frameon=False, loc='lower center', ncol=4, bbox_to_anchor=(.5, -.02))
fig.tight_layout(rect=(0, .07, 1, 1)); fig.savefig('fig3_decomposicao.png', bbox_inches='tight'); plt.close()
print('figura 3 gerada')
