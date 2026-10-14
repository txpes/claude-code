"""
Panorama descritivo da dificuldade financeira das companhias abertas nao financeiras brasileiras, 2010-2025
(secao 2 do artigo, pedido da coorientacao). Usa apenas os paineis e a base de recuperacao judicial.

Por ano: numero de companhias; parcela com cobertura de juros inferior a unidade, calculada diretamente como
EBIT sobre o valor absoluto das despesas financeiras, entre as companhias com despesa financeira; parcela com
patrimonio liquido negativo; parcela com EBITDA negativo; parcela com prejuizo liquido; alavancagem mediana; e
numero de companhias do painel cujo primeiro documento de recuperacao judicial ou extrajudicial e do ano.
Gera panorama.pkl, a tabela por subperiodo e a figura de duas partes (sem eixo duplo).
"""
import os, pickle
import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker

D = os.environ.get('DADOS', 'dados').rstrip('/') + '/'
C = pd.read_csv(D + 'painel_completo.csv'); I = pd.read_csv(D + 'painel_inputs.csv'); R = pd.read_csv(D + 'rj_detectada_2025.csv')
M = C[['CD_CVM', 'ano', 'ALV']].merge(I[['CD_CVM', 'ano', 'EBIT', 'DESP_FIN', 'PATR_LIQUIDO', 'EBITDA', 'LUCRO_LIQ']], on=['CD_CVM', 'ano'], how='left')
M['com_desp'] = M.DESP_FIN.fillna(0) != 0
M['cob_menor_1'] = np.where(M.com_desp, (M.EBIT / M.DESP_FIN.abs()) < 1, np.nan)

ano = M.groupby('ano').agg(n=('CD_CVM', 'size'), n_desp=('com_desp', 'sum'),
                           cob1=('cob_menor_1', 'mean'), pl=('PATR_LIQUIDO', lambda s: (s < 0).mean()),
                           ebitda=('EBITDA', lambda s: (s < 0).mean()), prejuizo=('LUCRO_LIQ', lambda s: (s < 0).mean()),
                           alv=('ALV', 'median'))
rj = R[(R.na_amostra == True) & (R.ano_rj.between(2010, 2025))]
ano['rj'] = rj.groupby('ano_rj').CD_CVM.nunique().reindex(ano.index).fillna(0).astype(int)

periodos = [('2010–2014', 2010, 2014), ('2015–2016', 2015, 2016), ('2017–2019', 2017, 2019), ('2020–2021', 2020, 2021), ('2022–2025', 2022, 2025)]
linhas = []
for rot, a, b in periodos:
    x = ano.loc[a:b]; m = M[M.ano.between(a, b)]
    linhas.append(dict(periodo=rot, companhias=x.n.mean(), cob1=m.cob_menor_1.mean(), pl=(m.PATR_LIQUIDO < 0).mean(),
                       ebitda=(m.EBITDA < 0).mean(), prejuizo=(m.LUCRO_LIQ < 0).mean(), alv=m.ALV.median(), rj=int(x.rj.sum())))
tab = pd.DataFrame(linhas)
resumo = dict(cob1_media=M.cob_menor_1.mean(), cob1_max=ano.cob1.max(), cob1_max_ano=int(ano.cob1.idxmax()),
              cob1_min=ano.cob1.min(), cob1_min_ano=int(ano.cob1.idxmin()), rj_total=int(rj.CD_CVM.nunique()),
              rj_judicial=int(rj[rj.tipo == 'judicial'].CD_CVM.nunique()), prejuizo_media=(M.LUCRO_LIQ < 0).mean(),
              pl_media=(M.PATR_LIQUIDO < 0).mean(), firmas=int(M.CD_CVM.nunique()), obs=len(M), sem_desp=int((~M.com_desp).sum()))
pickle.dump(dict(ano=ano, tab=tab, resumo=resumo), open('panorama.pkl', 'wb'))

# figura: (a) parcelas, tres series com marcadores distintos e rotulo direto; (b) recuperacoes judiciais, barras
cores = {'cob1': '#2a78d6', 'ebitda': '#eb6834', 'pl': '#1baf7a'}          # paleta categorica validada (ordem fixa)
rot = {'cob1': 'Cobertura de juros < 1', 'ebitda': 'EBITDA negativo', 'pl': 'Patrimônio líquido negativo'}
mk = {'cob1': 'o', 'ebitda': 's', 'pl': '^'}
fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.3, 5.6), sharex=True, gridspec_kw=dict(height_ratios=[2.2, 1]))
anos = ano.index.values
for k in ['cob1', 'ebitda', 'pl']:
    a1.plot(anos, ano[k] * 100, color=cores[k], lw=2, marker=mk[k], ms=4.5, label=rot[k])
    dy = {'cob1': 0, 'ebitda': 6, 'pl': -6}[k]                       # afasta os rotulos das duas series proximas
    a1.annotate(rot[k], (anos[-1], ano[k].iloc[-1] * 100), xytext=(6, dy), textcoords='offset points', va='center', fontsize=7.5, color='#333')
for x0, x1 in [(2014.5, 2016.5), (2019.5, 2020.5)]:
    a1.axvspan(x0, x1, color='#e8e7e2', zorder=0); a2.axvspan(x0, x1, color='#e8e7e2', zorder=0)
a1.set_ylabel('% das companhias', fontsize=8.5); a1.set_ylim(0, 70)
a1.text(2015.5, 67, 'Recessão', ha='center', fontsize=7, color='#555'); a1.text(2020, 67, 'Pandemia', ha='center', fontsize=7, color='#555')
a1.legend(fontsize=7.5, frameon=False, loc='upper right', bbox_to_anchor=(1, 0.93))
a1.set_title('(a) Parcela das companhias em cada condição', fontsize=8.5, loc='left')
a2.bar(anos, ano.rj, width=0.6, color='#2a78d6')
for x, v in zip(anos, ano.rj):
    a2.text(x, v + 0.2, str(v), ha='center', fontsize=7, color='#333')
a2.set_ylabel('Companhias', fontsize=8.5); a2.set_ylim(0, ano.rj.max() + 2); a2.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
a2.set_title('(b) Recuperações judiciais e extrajudiciais, pelo ano do primeiro documento', fontsize=8.5, loc='left')
for ax in (a1, a2):
    ax.spines[['top', 'right']].set_visible(False); ax.tick_params(labelsize=7.5); ax.grid(axis='y', color='#ececec', lw=.6); ax.set_axisbelow(True)
a2.set_xticks(anos); a2.set_xticklabels([str(y) for y in anos], rotation=45)
a1.set_xlim(2009.5, 2027.3)
fig.tight_layout(); fig.savefig('fig_panorama.png', dpi=200)

pd.set_option('display.width', 200)
print(ano.assign(**{c: ano[c] * 100 for c in ['cob1', 'pl', 'ebitda', 'prejuizo']}).round(1).to_string())
print(tab.round(3).to_string(index=False)); print(resumo)
