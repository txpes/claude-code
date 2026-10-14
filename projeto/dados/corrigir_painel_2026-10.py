"""Correcao do painel apontada pela conferencia contra a CVM (VERIFICACAO_FONTE_CVM.md, 14/10/2026).

1. Exclui os tres emissores estrangeiros que ficaram fora da exclusao original (codigo CVM 80xxx, fora do cadastro
   de companhias abertas): Aura Minerals (80187), G2D Investments (80195) e Inter & Co (80217).
2. Refaz quatro firma-anos com as demonstracoes corretas da CVM:
   - Aguas do Rio 1 e 4 SPE, 2021: demonstracao anual de 31/12/2021, e nao a especial de 31/07/2021;
   - Equatorial Para, 2025: versao mais recente da DFP (a versao 1 tinha EBIT e lucro cerca de dez vezes maiores);
   - COSERN, 2010: receita liquida, ausente no painel.
   Os insumos sao lidos com o mesmo mapa de contas do painel (inferido e conferido em 37 mil comparacoes) e os
   indicadores recalculados pelas definicoes da Tabela de indicadores. Os criterios de vulnerabilidade dessas linhas
   sao conferidos: se algum mudasse, a correcao pararia, porque a codificacao de transicao teria de ser refeita.
Idempotente: rodar de novo sobre os paineis corrigidos nao muda nada.
Uso: python corrigir_painel_2026-10.py <pasta dos paineis> <pasta com dfp_cia_aberta_AAAA.zip>"""
import sys, zipfile, io
import numpy as np, pandas as pd

D, RAW = sys.argv[1].rstrip('/') + '/', sys.argv[2].rstrip('/') + '/'
EXCLUIR = [80187, 80195, 80217]
REFAZER = [(26735, 2021), (26743, 2021), (18309, 2025), (18139, 2010)]
CONTAS = {'ATIVO_TOTAL': ('BPA', '1'), 'ATIVO_CIRC': ('BPA', '1.01'), 'CAIXA': ('BPA', '1.01.01'), 'APLIC_FIN': ('BPA', '1.01.02'),
          'PASSIVO_CIRC': ('BPP', '2.01'), 'DIVIDA_CP': ('BPP', '2.01.04'), 'DIVIDA_LP': ('BPP', '2.02.01'), 'PATR_LIQUIDO': ('BPP', '2.03'),
          'RES_LUCRO': ('BPP', '2.03.04'), 'LUC_ACUM': ('BPP', '2.03.05'), 'RECEITA_LIQ': ('DRE', '3.01'), 'EBIT': ('DRE', '3.05'),
          'DESP_FIN': ('DRE', '3.06.02'), 'LUCRO_LIQ': ('DRE', '3.11'), 'FCO': ('DFC', '6.01')}

C = pd.read_csv(D + 'painel_completo.csv'); T = pd.read_csv(D + 'painel_transicao.csv'); I = pd.read_csv(D + 'painel_inputs.csv')
log = []
for nome, df in [('completo', C), ('transicao', T), ('inputs', I)]:
    log.append(f'{nome}: {int(df.CD_CVM.isin(EXCLUIR).sum())} linhas dos emissores estrangeiros excluidas')
C, T, I = (df[~df.CD_CVM.isin(EXCLUIR)].copy() for df in (C, T, I))


def ler(cd, ano, fonte):
    z = zipfile.ZipFile(f'{RAW}dfp_cia_aberta_{ano}.zip'); v = {}
    def tab(dem):
        nomes = [n for n in z.namelist() if f'_{dem}' in n and f'_{fonte}_' in n]
        d = pd.concat(pd.read_csv(io.BytesIO(z.read(n)), sep=';', encoding='latin-1', dtype={'CD_CONTA': str}) for n in nomes)
        d = d[(d.CD_CVM == cd) & d.ORDEM_EXERC.str.upper().str.startswith('Ú') & (d.DT_REFER == f'{ano}-12-31')]
        d = d[d.VERSAO == d.VERSAO.max()]
        d['v'] = d.VL_CONTA.astype(float) * np.where(d.ESCALA_MOEDA.str.upper() == 'MIL', 1000, 1)
        return d
    T_ = {dem: tab(dem) for dem in ('BPA', 'BPP', 'DRE', 'DFC')}
    for campo, (dem, conta) in CONTAS.items():
        x = T_[dem][T_[dem].CD_CONTA == conta].v
        v[campo] = float(x.iloc[0]) if len(x) else np.nan
    dfc = T_['DFC']; da = dfc[dfc.CD_CONTA.str.startswith('6.01.01.') & dfc.DS_CONTA.str.lower().str.contains('deprecia')].v
    v['DA'] = float(da.iloc[0]) if len(da) else 0.0
    v['EBITDA'] = v['EBIT'] + abs(v['DA'])
    v['versao'] = int(T_['BPA'].VERSAO.max())
    return v


fator = (C.ATIVO_TOTAL_real / C.ATIVO_TOTAL).groupby(C.ano).first()
for cd, ano in REFAZER:
    li = (I.CD_CVM == cd) & (I.ano == ano); lc = (C.CD_CVM == cd) & (C.ano == ano)
    assert li.sum() == 1 and lc.sum() == 1, (cd, ano)
    fonte = I.loc[li, 'fonte'].iloc[0]; v = ler(cd, ano, fonte)
    antes = C.loc[lc, ['LC', 'CG', 'ALV', 'CP', 'COB', 'FCO', 'ROA', 'EBITDA']].iloc[0].round(4).to_dict()
    for campo in list(CONTAS) + ['DA', 'EBITDA']:
        I.loc[li, campo] = v[campo]
    div = np.nansum([v['DIVIDA_CP'], v['DIVIDA_LP']])
    novo = dict(LC=v['ATIVO_CIRC'] / v['PASSIVO_CIRC'], CG=(v['ATIVO_CIRC'] - v['PASSIVO_CIRC']) / v['ATIVO_TOTAL'],
                ALV=div / v['ATIVO_TOTAL'], CP=(np.nan_to_num(v['DIVIDA_CP']) / div) if div else 0.0,
                COB=v['EBIT'] / abs(v['DESP_FIN']), FCO=(v['FCO'] / div) if div else np.nan, ROA=v['LUCRO_LIQ'] / v['ATIVO_TOTAL'],
                EBITDA=v['EBITDA'] / v['RECEITA_LIQ'])
    for k, x in novo.items():
        if not np.isfinite(x):
            raise SystemExit(f'{cd} {ano} {k}: valor nao finito; revisar a linha antes de aplicar')
        C.loc[lc, k] = x
    C.loc[lc, 'ATIVO_TOTAL'] = v['ATIVO_TOTAL']; C.loc[lc, 'ATIVO_TOTAL_real'] = v['ATIVO_TOTAL'] * fator[ano]
    C.loc[lc, 'log_ativo_real'] = np.log(v['ATIVO_TOTAL'] * fator[ano])
    if (v['PATR_LIQUIDO'] < 0) != bool(C.loc[lc, 'crit_b'].iloc[0]):
        raise SystemExit(f'{cd} {ano}: criterio de PL muda; refazer a codificacao de transicao')
    if novo['EBITDA'] < 0:
        raise SystemExit(f'{cd} {ano}: EBITDA negativo; conferir o criterio (c) antes de aplicar')
    log.append(f'{cd} {ano} ({fonte}, versao {v["versao"]}): antes {antes} | depois { {k: round(x, 4) for k, x in novo.items()} }')

C.to_csv(D + 'painel_completo.csv', index=False); T.to_csv(D + 'painel_transicao.csv', index=False); I.to_csv(D + 'painel_inputs.csv', index=False)
print('\n'.join(log)); print(f'painel: {len(C)} firma-anos, {C.CD_CVM.nunique()} companhias')
