"""Confere os insumos do painel (painel_inputs.csv) contra os arquivos DFP brutos da CVM (dados.cvm.gov.br).
Uso: python conferir_cvm.py <pasta com dfp_cia_aberta_AAAA.zip> <painel_inputs.csv> <saida.csv>"""
import sys, zipfile, io, numpy as np, pandas as pd
raw, painel = sys.argv[1], sys.argv[2]
P = pd.read_csv(painel)
CONTAS = {'ATIVO_TOTAL': ('BPA', '1'), 'PATR_LIQUIDO': ('BPP', '2.03'), 'RECEITA_LIQ': ('DRE', '3.01'), 'EBIT': ('DRE', '3.05'), 'LUCRO_LIQ': ('DRE', '3.11')}
res = []
for y in range(2010, 2026):
    z = zipfile.ZipFile(f'{raw}/dfp_cia_aberta_{y}.zip')
    for var, (dem, conta) in CONTAS.items():
        for fonte in ('con', 'ind'):
            nm = f'dfp_cia_aberta_{dem}_{fonte}_{y}.csv'
            d = pd.read_csv(io.BytesIO(z.read(nm)), sep=';', encoding='latin-1', dtype={'CD_CONTA': str})
            d = d[(d.CD_CONTA == conta) & (d.ORDEM_EXERC.str.upper().str.startswith('Ú')) & (d.DT_REFER.str[:4] == str(y))]
            d = d.sort_values('VERSAO').groupby('CD_CVM').tail(1)
            d['v'] = d.VL_CONTA.astype(float) * np.where(d.ESCALA_MOEDA.str.upper() == 'MIL', 1000, 1)
            p = P[(P.ano == y) & (P.fonte == fonte)][['CD_CVM', var]]
            m = p.merge(d[['CD_CVM', 'v']], on='CD_CVM', how='left')
            for _, r in m.iterrows():
                res.append(dict(ano=y, var=var, fonte=fonte, cd=r.CD_CVM, painel=r[var], cvm=r.v))
R = pd.DataFrame(res)
R['achou'] = R.cvm.notna()
R['ok'] = R.achou & (np.isclose(R.painel, R.cvm, rtol=1e-6, atol=1) | (R.painel.isna() & R.cvm.isna()))
print(R.groupby(['ano', 'var']).agg(n=('ok', 'size'), achou=('achou', 'sum'), iguais=('ok', 'sum')).to_string())
print('\nTOTAL:', len(R), 'comparacoes |', int(R.achou.sum()), 'encontradas na CVM |', int(R.ok.sum()), 'iguais')
bad = R[R.achou & ~R.ok]
print('divergentes:', len(bad)); print(bad.head(15).to_string())
R.to_csv(sys.argv[3], index=False)
