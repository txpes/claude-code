"""Testa a leitura por concentracao: a agregacao compensa quando o poder discriminante
esta espalhado entre indicadores, e custa quando esta concentrado em poucos."""
import pandas as pd, numpy as np, pickle, warnings
from scipy.stats import ks_2samp, spearmanr
warnings.filterwarnings('ignore')
import os
D = os.environ.get('DADOS', 'dados').rstrip('/') + '/'
c = pd.read_csv(D + 'painel_completo.csv'); t = pd.read_csv(D + 'painel_transicao.csv'); i = pd.read_csv(D + 'painel_inputs.csv')
P = c.merge(t.drop(columns=['DENOM_CIA']), on=['CD_CVM', 'ano']).sort_values(['CD_CVM', 'ano']).reset_index(drop=True)
m = P[['CD_CVM', 'ano']].merge(i, on=['CD_CVM', 'ano'], how='left')
P['X12'] = ((m.RES_LUCRO.fillna(0) + m.LUC_ACUM.fillna(0)) / m.ATIVO_TOTAL).values
P['X22'] = np.where(m.RECEITA_LIQ.isna() | (m.RECEITA_LIQ == 0), np.nan,
    ((m.CAIXA.fillna(0) + m.APLIC_FIN.fillna(0) - m.DIVIDA_CP.fillna(0)) / m.RECEITA_LIQ)).astype(float)
for h in (1, 2):
    P[f'a{h}'] = P.groupby('CD_CVM').ano.shift(-h)
    P[f'V{h}'] = P.groupby('CD_CVM')['V_entrada'].shift(-h); P.loc[P[f'a{h}'] != P.ano + h, f'V{h}'] = np.nan
    for k in ['crit_b', 'crit_c', 'crit_d_entry']:
        P[f'{k}_h{h}'] = P.groupby('CD_CVM')[k].shift(-h); P.loc[P[f'a{h}'] != P.ano + h, f'{k}_h{h}'] = np.nan
P['r2'] = (P.em_risco == 1) & (P.groupby('CD_CVM')['em_risco'].shift(-1) == 1) & (P.a1 == P.ano + 1)
IND = ['LC', 'CG', 'ALV', 'CP', 'COB', 'FCO', 'ROA', 'EBITDA']; NEG = ['LC', 'CG', 'COB', 'FCO', 'ROA', 'EBITDA']
A = pickle.load(open('blocoA.pkl', 'rb'))
def auc(x, y):
    r = pd.Series(x).rank().values; n1 = int(y.sum()); return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))
linhas = []
for h in (1, 2):
    E, y, pred = A[h]['ref']
    Ec = E.merge(P[['CD_CVM', 'ano'] + [f'{k}_h{h}' for k in ['crit_b', 'crit_c', 'crit_d_entry']]], on=['CD_CVM', 'ano'], how='left')
    X = Ec[IND].astype(float).copy(); X[NEG] = -X[NEG]
    tipos = {'EBITDA exclusivo': ((Ec[f'crit_c_h{h}'] == 1) & (Ec[f'crit_b_h{h}'] != 1) & (Ec[f'crit_d_entry_h{h}'] != 1)).values,
             'PL negativo': (Ec[f'crit_b_h{h}'] == 1).values, 'Recuperação judicial': (Ec[f'crit_d_entry_h{h}'] == 1).values,
             'Todas': np.ones(len(Ec), bool)}
    for nome, msk in tipos.items():
        k = (y == 0) | (msk & (y == 1)); yk = y[k]
        if yk.sum() < 10: continue
        ks = np.array([ks_2samp(X.loc[k & (y == 1) & msk, c_], X.loc[k & (y == 0), c_]).statistic for c_ in IND])
        aucs = {c_: auc(X[c_].values[k], yk) for c_ in IND}
        melhor = max(aucs.values()); aF = auc(pred['F'][k], yk)
        conc = ks.max() / ks.mean()                      # concentracao do poder discriminante
        herf = ((ks / ks.sum()) ** 2).sum() * len(ks)    # medida alternativa
        linhas.append(dict(h=h, tipo=nome, n=int(yk.sum()), ksmax=ks.max(), ksmed=ks.mean(), conc=conc, herf=herf,
                           F=aF, melhor=melhor, ganho=aF - melhor))
R = pd.DataFrame(linhas)
print(R.round(3).to_string(index=False))
print()
for v in ['conc', 'herf', 'ksmax']:
    r = spearmanr(R[v], R.ganho)
    print(f'Spearman(concentração por {v:6s}, ganho da agregação) = {r.statistic:+.3f}  p = {r.pvalue:.3f}  (n={len(R)})')
print(f'\ncélulas em que a agregação supera o melhor indicador isolado: {(R.ganho > 0).sum()} de {len(R)}')
print('ordenadas por concentração:')
print(R.sort_values("conc")[['h', 'tipo', 'n', 'conc', 'F', 'melhor', 'ganho']].round(3).to_string(index=False))
R.to_csv('concentracao.csv', index=False)
