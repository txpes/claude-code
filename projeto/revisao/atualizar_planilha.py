"""Preenche tabelas/Tabelas_Artigo_revisado.xlsx com as saidas do codigo final.
Uso: python atualizar_planilha.py <diretorio onde o executar.sh rodou>
Mantem o layout e as formulas das abas; substitui apenas os valores numericos."""
import sys, os, pickle
import numpy as np, pandas as pd, openpyxl
from openpyxl.styles import Font

R = sys.argv[1]
AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(AQUI, '..', 'tabelas', 'Tabelas_Artigo.xlsx')
DST = os.path.join(AQUI, '..', 'tabelas', 'Tabelas_Artigo_revisado.xlsx')
L = lambda f: pickle.load(open(os.path.join(R, f), 'rb'))
A, EF, RB, N, T, TP, DEC, EV, PU, PF, G3 = (L(f) for f in ['blocoA.pkl', 'blocoEF.pkl', 'robustez.pkl', 'N.pkl', 'tabelas.pkl', 'temporal.pkl',
                                                           'decomposicao.pkl', 'eventos_alternativos.pkl', 'puros.pkl', 'perfil.pkl', 'blocoG3.pkl'])
D = pd.read_csv(os.path.join(R, 'blocoD.csv'))
wb = openpyxl.load_workbook(SRC)          # parte sempre da planilha original
nomes = {'Componentes principais (F)': 'F', 'Árvores impulsionadas': 'GB', 'Cobertura de juros': 'COB', 'Mínimos quadrados parciais': 'PLS',
         'Retorno sobre ativos': 'ROA', 'Brito e Assaf Neto': 'BA', 'Liquidez corrente': 'LC', 'Alavancagem': 'ALV'}
def auc(x, y):
    r = pd.Series(x).rank().values; n1 = int(y.sum()); return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))

# Tabela 10: AUC da atribuicao de referencia, IC e p do bootstrap; Bonferroni x6 e PLS sem ajuste
for aba, h in [('T10_um_ano', 1), ('T10_dois_anos', 2)]:
    ws = wb[aba]; E, y, pred = A[h]['ref']
    for r in range(4, 12):
        m = nomes[ws[f'A{r}'].value]; ws[f'B{r}'] = float(auc(pred[m], y))
        if m == 'F': continue
        d = D[(D.h == h) & (D.comparacao == f'{m} vs F')].iloc[0]
        ws[f'D{r}'], ws[f'E{r}'], ws[f'F{r}'] = float(d.lo), float(d.hi), float(d.p_boot)
        ws[f'G{r}'] = f'=F{r}' if m == 'PLS' else f'=MIN(1,F{r}*6)'
    ws['A12'] = ('Fonte: 01 e 02. Validação cruzada agrupada por firma, atribuição de referência. Diferença por fórmula. p ajustado por Bonferroni '
                 'para as seis comparações contra benchmarks e referência não linear; a comparação com mínimos quadrados parciais responde a H4 e não é ajustada.')
    ws['A13'] = None

# Tabela 11: esquema temporal
ws = wb['T11_temporal']
for r in range(4, 10):
    m = nomes[ws[f'A{r}'].value]; ws[f'B{r}'] = float(TP[1]['auc'][m]); ws[f'F{r}'] = float(TP[2]['auc'][m])
    if m in TP[1].get('cmp', {}):
        o, lo, hi, p = TP[1]['cmp'][m]; ws[f'D{r}'], ws[f'E{r}'] = float(lo), float(hi)

# Tabela 13: medias sobre dez atribuicoes, com a coluna da margem EBITDA
ws = wb['T13_decomposicao']; ws['H3'] = 'MEB'; ws['H3'].font = Font(bold=True)
mapa = {'Somente por EBITDA negativo': 'EBITDA, exclusivamente', 'Patrimônio líquido negativo': 'PL negativo',
        'Recuperação judicial': 'recuperacao judicial', 'Todas as entradas': 'todas'}
for r, base in [(range(5, 9), 'h1 principal'), (range(10, 14), 'h2 principal')]:
    for i in r:
        tn = mapa[ws[f'A{i}'].value]; acc = DEC[base]
        ws[f'B{i}'] = int(acc[(tn, 'n')][0])
        for col, m in zip('CDEFGH', ['F', 'GB', 'COB', 'PLS', 'ROA', 'MEB']):
            ws[f'{col}{i}'] = float(np.mean(acc[(tn, m)]))
ws['A15'] = ('Fonte: 09. Médias sobre dez atribuições. Em cada linha, os não eventos são todos os da amostra e os eventos apenas os do tipo indicado. '
             'MEB: margem EBITDA isolada, cuja condição define o critério de prejuízo operacional.')

# Tabela 14: subconjuntos puros
ws = wb['T14_puros']
chave = {'Prejuízo operacional': 'EBITDA puras', 'Patrimônio negativo': 'PL puras', 'Recuperação judicial': 'RJ puras'}
for i in range(4, 10):
    rot, hz = ws[f'A{i}'].value.rsplit(', ', 1); h = 1 if hz == 'um ano' else 2; o = PU[(h, chave[rot])]
    ws[f'B{i}'], ws[f'C{i}'] = int(o['n']), float(o['F'])
    for cols, m in [('DEF', 'COB'), ('GHI', 'PLS')]:
        _, dif, lo, hi = o[m]
        for c, v in zip(cols, (dif, lo, hi)): ws[f'{c}{i}'] = float(v)

# Tabela 15: perfil (a coluna de patrimonio negativo inclui entradas com outros criterios)
ws = wb['T15_perfil']
lin = {'Alavancagem': 'ALV', 'Liquidez corrente': 'LC', 'Capital de giro sobre ativo': 'CG', 'Cobertura de juros': 'COB',
       'Retorno sobre ativos': 'ROA', 'Margem EBITDA': 'EBITDA', 'Logaritmo do ativo real': 'log_ativo_real', 'Observações': 'n'}
for i in range(4, 12):
    for c, v in zip('BCD', PF[lin[ws[f'A{i}'].value]]): ws[f'{c}{i}'] = float(v) if lin[ws[f'A{i}'].value] != 'n' else int(v)
ws['A13'] = ('Fonte: 13. Horizonte de dois anos, sobre a amostra de risco. A primeira coluna reúne as entradas apenas pelo critério de EBITDA; '
             'a segunda, todas as entradas por patrimônio líquido negativo, inclusive as que satisfazem outro critério.')

# Tabela 16: sem mudanca de valores; so a sigla
wb['T16_diagnostico']['A6'] = 'MEB'

# Tabela 17: substitui pela versao com calibracao sobre o posto, nos dois horizontes
del wb['T17_metricas']
ws = wb.create_sheet('T17_metricas', index=wb.sheetnames.index('T18_definicoes'))
ws['A1'] = 'Tabela 17 – Métricas de probabilidade e desempenho operacional'; ws['A1'].font = Font(bold=True)
cab = ['Horizonte', 'Modelo', 'AUC precisão-revocação', 'Brier', 'Inclinação', 'Intercepto', 'Sensibilidade', 'Especificidade', 'VPP', 'VPN',
       'Firma-anos sinalizados', 'Decisão líquida 5:1', 'Decisão líquida 10:1', 'Decisão líquida 20:1']
for j, c in enumerate(cab, 1):
    ws.cell(3, j, c).font = Font(bold=True)
lin_ = 4
rot = {v: k for k, v in nomes.items()}
for h in (1, 2):
    for m in ['GB', 'COB', 'ROA', 'PLS', 'F', 'BA']:
        r = G3[h][m]; o = r[80]
        vals = ['um ano' if h == 1 else 'dois anos', rot[m], r['pr_auc'], r['brier'], r['incl'], r['intercepto'], o['sens'], o['espec'], o['vpp'], o['vpn'],
                o['sinalizadas'], r['nb5'], r['nb10'], r['nb20']]
        for j, v in enumerate(vals, 1): ws.cell(lin_, j, float(v) if isinstance(v, (float, np.floating)) else v)
        lin_ += 1
    p = G3[h]['_prev']
    for j, v in enumerate(['um ano' if h == 1 else 'dois anos', 'Referência sem informação', p, p * (1 - p)], 1): ws.cell(lin_, j, float(v) if j > 2 else v)
    lin_ += 1
ws.cell(lin_ + 1, 1, 'Fonte: 14. Calibração logística sobre o posto do escore na distribuição do treino; limiar que atinge sensibilidade de 80% nas firmas '
        'de treino, aplicado às de teste. Decisão líquida por firma-ano; a de não sinalizar ninguém é zero.')
ws.column_dimensions['B'].width = 28
if 'T17_revisada' in wb.sheetnames: del wb['T17_revisada']

# Tabela 18: definicoes alternativas
ws = wb['T18_definicoes']
for i, nome in zip(range(4, 7), ['principal', 'sem entradas so EBITDA', 'restritiva (PL ou RJ)']):
    E, y, _ = EV[nome]['ref']; ws[f'B{i}'], ws[f'C{i}'] = int(len(y)), int(y.sum())
    for c, m in zip('DEFG', ['F', 'GB', 'COB', 'PLS']): ws[f'{c}{i}'] = float(np.mean(EV[nome]['res'][m]))

# Tabela 19: sensibilidades, com a linha nova das saidas pelo cadastro
ws = wb['T19_sensibilidade']
rb, rf, nb, eb, nf, ef, *_ = EF['F']; rs, ns, es, *_ = EF['E']; rc, nc, ec, *_ = EF['E2']; cal = RB['cal']; sv = RB['sobrev']
ws.insert_rows(8)
linhas = [('Especificação principal', nb, eb, rb), ('Excluídas as entradas exclusivamente por recuperação judicial', cal['n'], cal['evk'], cal),
          ('Somente a primeira entrada de cada firma', nf, ef, rf), ('Saídas associadas a distress tratadas como evento', ns, es, rs),
          ('Saídas por dificuldade financeira segundo o cadastro, como evento', nc, ec, rc),
          ('Somente firmas com registro ativo ao fim do período', sv['n'], sv['ev'], dict(F=sv['F'], PLS=sv['PLS'], COB=sv['COB'], ROA=N['sv_ROA']))]
for i, (rot_, n_, e_, v) in zip(range(4, 10), linhas):
    ws[f'A{i}'], ws[f'B{i}'], ws[f'C{i}'] = rot_, int(n_), int(e_)
    for c, m in zip('DEFG', ['F', 'PLS', 'COB', 'ROA']): ws[f'{c}{i}'] = float(v[m])
    ws[f'H{i}'] = f'=E{i}-D{i}'
ws['A11'] = 'Fonte: 04, 05 e 07. Horizonte de um ano, atribuição de referência.'

# Tabela 20: defasagens
ws = wb['T20_defasagens']; lg = RB['lag']
for i, k in zip([4, 5, 6, 7, 8, 9], ['F', 'F_L', 'C', 'C_L', 'P8', 'P16']): ws[f'B{i}'] = float(lg[k])

# Estabilidade entre as dez atribuicoes
for aba, h in [('Estabilidade_h1', 1), ('Estabilidade_h2', 2)]:
    ws = wb[aba]
    for k in range(10):
        for c, m in zip('BCDE', ['F', 'PLS', 'GB', 'BA']): ws[f'{c}{4 + k}'] = float(A[h]['res'][m][k])

wb.save(DST)
print('planilha atualizada:', DST, wb.sheetnames)
