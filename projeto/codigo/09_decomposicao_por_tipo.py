import pandas as pd, numpy as np, warnings, pickle
warnings.filterwarnings('ignore')
exec(open('08_definicoes_de_evento.py').read().split("OUT = {}")[0])      # dados, run(), boot(), SPEC

# criterios no ano do desfecho, para um e dois anos
for h in (1, 2):
    for c in ['crit_b', 'crit_c', 'crit_d_entry']:
        P[f'{c}_h{h}'] = P.groupby('CD_CVM')[c].shift(-h)
        P.loc[P[f'a{h}'] != P.ano + h, f'{c}_h{h}'] = np.nan
def tipos(E, h):
    b, c, d = (E[f'crit_b_h{h}'] == 1).values, (E[f'crit_c_h{h}'] == 1).values, (E[f'crit_d_entry_h{h}'] == 1).values
    return {'EBITDA, exclusivamente': c & ~b & ~d, 'PL negativo': b, 'recuperacao judicial': d}
M = ['F', 'PLS', 'GB', 'BA', 'COB', 'ROA', 'MEB', 'ALV']
okBA = P[['X12', 'X22']].notna().all(axis=1)
BASES = {
 'h1 principal': (P[(P.em_risco == 1) & P.V1.notna() & okBA], 'V1', 1),
 'h2 principal': (P[P.r2 & P.V2.notna() & okBA], 'V2', 2),
 'h1 retreinado sem entradas so por EBITDA': (P[(P.em_risco == 1) & P.V1.notna() & okBA &
        ~((P.V1 == 1) & (P.crit_c_h1 == 1) & (P.crit_b_h1 != 1) & (P.crit_d_entry_h1 != 1))], 'V1', 1),
}
OUT = {}
for nome, (E0, yc, h) in BASES.items():
    acc = {}; ref = None
    for s in range(1, 11):
        E, y, pr = run(E0, yc, s)
        T = tipos(E, h); T['todas'] = np.ones(len(E), bool)
        for tn, msk in T.items():
            k = (y == 0) | (msk & (y == 1)); yk = y[k]
            if yk.sum() < 5: continue
            for m in M: acc.setdefault((tn, m), []).append(auc(pr[m][k], yk))
            acc.setdefault((tn, 'n'), []).append(int(yk.sum()))
        if s == 1: ref = (E, y, pr, T)
    print(f'\n===== {nome} =====')
    print(f'{"tipo de entrada":24s} {"n":>4s} ' + ''.join(f'{m:>7s}' for m in M) + '   PLS-F: min..max nas 10 atribuicoes')
    for tn in ['EBITDA, exclusivamente', 'PL negativo', 'recuperacao judicial', 'todas']:
        if (tn, 'F') not in acc: continue
        d = np.array(acc[(tn, 'PLS')]) - np.array(acc[(tn, 'F')])
        print(f'{tn:24s} {acc[(tn,"n")][0]:4d} ' + ''.join(f'{np.mean(acc[(tn,m)]):7.3f}' for m in M) +
              f'   {d.min():+.3f}..{d.max():+.3f}')
    E, y, pr, T = ref
    for tn in ['EBITDA, exclusivamente', 'PL negativo', 'recuperacao judicial']:
        k = (y == 0) | (T[tn] & (y == 1)); yk = y[k]; fk = E.CD_CVM.values[k]
        if yk.sum() < 5: continue
        cis = []
        for m in ['COB', 'ROA', 'PLS', 'GB']:
            o, lo, hi, p = boot(pr['F'][k], pr[m][k], yk, fk, B=2000)
            cis.append(f'{m} {o:+.3f} [{lo:+.3f};{hi:+.3f}]')
        print(f'   IC agrupado, {tn:22s} | ' + ' | '.join(cis))
    OUT[nome] = acc
pickle.dump(OUT, open('decomposicao.pkl', 'wb'))
