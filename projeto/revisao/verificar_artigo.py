"""Verificacao final: compara cada celula numerica das tabelas do artigo revisado (com as alteracoes aceitas)
com o valor recalculado pelo codigo final, na precisao exibida na celula.
Uso: python verificar_artigo.py <diretorio onde o executar.sh rodou> [docx; padrao: o revisado]"""
import sys, os, re, zipfile, pickle
import numpy as np, pandas as pd
from lxml import etree

R = sys.argv[1]
AQUI = os.path.dirname(os.path.abspath(__file__))
DOCX = sys.argv[2] if len(sys.argv) > 2 else os.path.join(AQUI, '..', 'artigo', 'Artigo_Fragilidade_Financeira_revisado.docx')
DADOS = os.path.join(AQUI, '..', 'dados')
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
L = lambda f: pickle.load(open(os.path.join(R, f), 'rb'))
A, EF, RB, N, T, TP, DEC, EV, PU, PF, G3 = (L(f) for f in ['blocoA.pkl', 'blocoEF.pkl', 'robustez.pkl', 'N.pkl', 'tabelas.pkl', 'temporal.pkl',
                                                           'decomposicao.pkl', 'eventos_alternativos.pkl', 'puros.pkl', 'perfil.pkl', 'blocoG3.pkl'])
D = pd.read_csv(os.path.join(R, 'blocoD.csv'))


def auc(x, y):
    r = pd.Series(x).rank().values; n1 = int(y.sum()); return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))


# ---------------------------------------------------------------- leitura das tabelas, com as alteracoes aceitas
root = etree.fromstring(zipfile.ZipFile(DOCX).read('word/document.xml'))
for d in list(root.iter(W + 'del')):
    par = d.getparent()
    if par.tag == W + 'rPr': p = par.getparent().getparent(); p.getparent().remove(p)
    elif par.tag == W + 'trPr': tr = par.getparent(); tr.getparent().remove(tr)
    else: par.remove(d)
tabelas = []
for tbl in root.iter(W + 'tbl'):
    grade = [[''.join(t.text or '' for t in tc.iter(W + 't')).strip() for tc in tr.iter(W + 'tc')] for tr in tbl.iter(W + 'tr')]
    tabelas.append(grade)


def num(s):
    """interpreta uma celula; devolve lista de (valor, casas decimais, e_limite_superior)"""
    s = s.replace('−', '-').replace('−', '-').replace(' ', '')
    out = []
    for m in re.finditer(r'(<)?([+-]?\d{1,3}(?:\.\d{3})*(?:,\d+)?)(%)?', s):
        txt = m.group(2); dec = len(txt.split(',')[1]) if ',' in txt else 0
        v = float(txt.replace('.', '').replace(',', '.'))
        if m.group(3): v /= 100; dec += 2
        out.append((v, dec, bool(m.group(1))))
    return out


erros, conferidas = [], 0


def confere(tab, lin, col, esperado, rot=''):
    global conferidas
    cel = tab[lin][col]; vals = num(cel)
    esp = esperado if isinstance(esperado, (list, tuple)) else [esperado]
    if len(vals) != len(esp):
        erros.append(f'{rot} [{lin},{col}] "{cel}": esperado {esp}'); return
    for (v, dec, menor), e in zip(vals, esp):
        conferidas += 1
        if menor:
            if not e < v + 1e-12: erros.append(f'{rot} [{lin},{col}] "{cel}": esperado {e:.5f}')
        elif abs(v - e) > 0.5 * 10 ** (-dec) + 1e-9:
            erros.append(f'{rot} [{lin},{col}] "{cel}": esperado {e:.5f}')


def acha(*chaves):
    ts = [t for t in tabelas if all(any(k in c for r in t for c in r) for k in chaves)]
    assert len(ts) == 1, (chaves, len(ts)); return ts[0]


def linha(t, rotulo, apos=None):
    ativo = apos is None
    for i, r in enumerate(t):
        if not ativo:
            ativo = r[0] == apos; continue
        if r[0] == rotulo: return i
    raise KeyError(rotulo)


# ---------------------------------------------------------------- Tabelas 2 a 7: dados
c = pd.read_csv(os.path.join(DADOS, 'painel_completo.csv'))
t = acha('Firma-anos atingidos'); confere(t, linha(t, '(a)'), 3, int(c.crit_b.sum()), 'T2')
confere(t, linha(t, '(b)'), 3, int(c.crit_c.sum()), 'T2'); confere(t, linha(t, '(c)'), 3, int(c.crit_d_state.sum()), 'T2')
iu = next(i for i, r in enumerate(t) if r[1] == 'União dos critérios'); ip = next(i for i, r in enumerate(t) if r[1] == 'Proporção do painel')
confere(t, iu, 3, T['vuln'], 'T2'); confere(t, ip, 3, T['vuln_pct'], 'T2')
t = acha('Mínimo', 'P25', 'Máximo'); desc = T['desc']
for sig in desc.index:
    i = linha(t, 'MEB' if sig == 'EBITDA' else sig)
    for j, col in enumerate(['mean', 'std', 'min', '25%', '50%', '75%', 'max'], 1): confere(t, i, j, desc.loc[sig, col], 'T3')
t = next(t for t in tabelas if t[0][:3] == ['', 'LC', 'CG'] or (len(t[0]) == 9 and t[0][1] == 'LC'))
ordem = ['LC', 'CG', 'ALV', 'CP', 'COB', 'FCO', 'ROA', 'EBITDA']
for a, ra in enumerate(ordem):
    i = linha(t, 'MEB' if ra == 'EBITDA' else ra)
    for b in range(a + 1): confere(t, i, b + 1, T['corr'].loc[ra, ordem[b]], 'T4')
t = acha('Continuações', 'Amostra de risco')
for rot_, v in [('Observações em vulnerabilidade', [T['vuln'], T['vuln_pct']]), ('Continuações', [T['contin'], T['contin'] / T['vuln']]),
                ('Entradas', [T['entradas'], T['entradas'] / T['vuln']]), ('Censuradas à esquerda', [T['censura'], T['censura'] / T['vuln']]),
                ('Amostra de risco', T['risco']), ('Taxa de entrada sobre a amostra de risco', T['taxa_entrada']),
                ('Amostra de estimação, horizonte de um ano', T['est_n1']), ('Eventos na amostra de estimação', [T['est_ev1'], T['est_ev1'] / T['est_n1']]),
                ('Amostra comum a todos os modelos', T['com_n1']), ('Eventos na amostra comum', [T['com_ev1'], T['com_ev1'] / T['com_n1']])]:
    i = linha(t, rot_); vs = v if isinstance(v, list) else [v]
    ini = 2 if rot_.startswith('Taxa de entrada') else 1
    for j, x in enumerate(vs, ini): confere(t, i, j, x, 'T5')
t = acha('Autovalor', 'Variância acumulada'); ac = np.cumsum(T['var_exp'])
for k in range(8): confere(t, linha(t, str(k + 1)), 1, T['autovalores'][k], 'T6'); confere(t, linha(t, str(k + 1)), 2, T['var_exp'][k], 'T6'); confere(t, linha(t, str(k + 1)), 3, ac[k], 'T6')
t = acha('Carga', 'Dimensão', 'Posição')
nome7 = {'Capital de giro': 'CG', 'Retorno sobre ativos': 'ROA', 'Alavancagem': 'ALV', 'Liquidez corrente': 'LC', 'Cobertura de juros': 'COB',
         'Margem EBITDA': 'EBITDA', 'Geração de caixa': 'FCO', 'Perfil da dívida': 'CP'}
for rot_, k in nome7.items(): confere(t, linha(t, rot_), 1, T['cargas'][k], 'T7')

# ---------------------------------------------------------------- Tabela 8
t = acha('Escore sem cobertura de juros')
for rot_, k in [('Escore médio, posição Ponzi', 'pz'), ('Escore médio, demais posições', 'np'), ('Estatística de Kolmogorov-Smirnov', 'ks'),
                ('Área sob a curva para a posição Ponzi', 'auc')]:
    confere(t, linha(t, rot_), 1, N[f'mk8_{k}'], 'T8'); confere(t, linha(t, rot_), 2, N[f'mk7_{k}'], 'T8')

# ---------------------------------------------------------------- Tabelas 9 e 10
t = acha('Efeito dos controles')
E1, y1, p1 = A[1]['ref']
n9 = {'Escore sintético (F)': 'F', 'Cobertura de juros': 'COB', 'Retorno sobre ativos': 'ROA', 'Brito e Assaf Neto': 'BA', 'Liquidez corrente': 'LC', 'Alavancagem': 'ALV'}
for rot_, m in n9.items():
    g = T['grade'][m]; i = linha(t, rot_)
    confere(t, i, 1, g[True], 'T9'); confere(t, i, 2, g[False], 'T9'); confere(t, i, 3, g[True] - g[False], 'T9'); confere(t, i, 4, auc(p1[m], y1), 'T9')
t = acha('p DeLong')
n10 = {'Árvores impulsionadas': 'GB', 'Cobertura de juros': 'COB', 'Mínimos quadrados parciais': 'PLS', 'Retorno sobre ativos': 'ROA',
       'Brito e Assaf Neto': 'BA', 'Liquidez corrente': 'LC', 'Alavancagem': 'ALV'}
for h, apos in [(1, None), (2, 'Horizonte de dois anos')]:
    E, y, pr = A[h]['ref']
    confere(t, linha(t, 'Componentes principais (F)', apos), 1, auc(pr['F'], y), f'T10 h{h}')
    for rot_, m in n10.items():
        i = linha(t, rot_, apos); d = D[(D.h == h) & (D.comparacao == f'{m} vs F')].iloc[0]
        confere(t, i, 1, auc(pr[m], y), f'T10 h{h}'); confere(t, i, 2, d.dif, f'T10 h{h}'); confere(t, i, 3, [d.lo, d.hi], f'T10 h{h}')
        confere(t, i, 4, d.p_boot, f'T10 h{h}'); confere(t, i, 5, d.p_bonf, f'T10 h{h}'); confere(t, i, 6, d.p_delong, f'T10 h{h}')

# ---------------------------------------------------------------- Tabelas 11 e 12
t = acha('AUC, um ano', 'AUC, dois anos')
n11 = {'Componentes principais (F)': 'F', 'Árvores impulsionadas': 'GB', 'Retorno sobre ativos': 'ROA', 'Mínimos quadrados parciais': 'PLS',
       'Cobertura de juros': 'COB', 'Brito e Assaf Neto': 'BA'}
for rot_, m in n11.items():
    i = linha(t, rot_); confere(t, i, 1, TP[1]['auc'][m], 'T11'); confere(t, i, 4, TP[2]['auc'][m], 'T11')
    if m in TP[1].get('cmp', {}):
        o, lo, hi, _ = TP[1]['cmp'][m]; confere(t, i, 2, o, 'T11'); confere(t, i, 3, [lo, hi], 'T11')
t = acha('Coeficiente de F(i,t)')
for j, k in enumerate(['trans_h1', 'trans_h2', 'est_h1', 'est_h2'], 1):
    pb = T['probit'][k]
    for rot_, v in [('Coeficiente de F(i,t)', pb['coef']), ('Erro-padrão', pb['ep']), ('Observações', pb['n']), ('Eventos', pb['ev']),
                    ('Parâmetros', pb['k']), ('Eventos por parâmetro', pb['ev'] / pb['k']), ('Pseudo R² de McFadden', pb['r2'])]:
        confere(t, linha(t, rot_), j, v, 'T12')

# ---------------------------------------------------------------- Tabelas 13 a 16
t = acha('Somente por EBITDA negativo', 'MEB')
m13 = {'Somente por EBITDA negativo': 'EBITDA, exclusivamente', 'Patrimônio líquido negativo': 'PL negativo',
       'Recuperação judicial': 'recuperacao judicial', 'Todas as entradas': 'todas'}
for base, apos in [('h1 principal', 'Horizonte de um ano'), ('h2 principal', 'Horizonte de dois anos')]:
    for rot_, tn in m13.items():
        i = linha(t, rot_, apos); acc = DEC[base]; confere(t, i, 1, acc[(tn, 'n')][0], 'T13')
        for j, m in enumerate(['F', 'GB', 'COB', 'PLS', 'ROA', 'MEB'], 2): confere(t, i, j, np.mean(acc[(tn, m)]), f'T13 {base}')
t = acha('Cobertura menos F', 'PLS menos F')
ch = {'Prejuízo operacional': 'EBITDA puras', 'Patrimônio negativo': 'PL puras', 'Recuperação judicial': 'RJ puras'}
for i, r in enumerate(t):
    if ', ' not in r[0]: continue
    rot_, hz = r[0].rsplit(', ', 1); o = PU[(1 if hz == 'um ano' else 2, ch[rot_])]
    confere(t, i, 1, o['n'], 'T14'); confere(t, i, 2, o['F'], 'T14')
    confere(t, i, 3, o['COB'][1], 'T14'); confere(t, i, 4, [o['COB'][2], o['COB'][3]], 'T14')
    confere(t, i, 5, o['PLS'][1], 'T14'); confere(t, i, 6, [o['PLS'][2], o['PLS'][3]], 'T14')
t = acha('Mediana no exercício t')
p15 = {'Alavancagem': 'ALV', 'Liquidez corrente': 'LC', 'Capital de giro sobre ativo': 'CG', 'Cobertura de juros': 'COB', 'Retorno sobre ativos': 'ROA',
       'Margem EBITDA': 'EBITDA', 'Logaritmo do ativo real': 'log_ativo_real', 'Observações': 'n'}
for rot_, k in p15.items():
    for j in range(3): confere(t, linha(t, rot_), j + 1, PF[k][j], 'T15')
t = acha('Variância entre firmas'); dg = T['diagnostico'].set_index('ind')
for sig in dg.index:
    i = linha(t, 'MEB' if sig == 'EBITDA' else sig)
    for j, col in enumerate(['ks', 'carga', 'peso_pls', 'entre'], 1): confere(t, i, j, dg.loc[sig, col], 'T16')

# ---------------------------------------------------------------- Tabelas 17 a 20
t = acha('AUC precisão-revocação')
for rot_, m in [('Árvores impulsionadas', 'GB'), ('Cobertura de juros', 'COB'), ('Mínimos quadrados parciais', 'PLS'), ('Retorno sobre ativos', 'ROA'),
                ('Componentes principais (F)', 'F'), ('Brito e Assaf Neto', 'BA')]:
    r = G3[1][m]; o = r[80]; i = linha(t, rot_)
    for j, v in enumerate([r['pr_auc'], r['brier'], r['incl'], o['sinalizadas'], o['vpp'], o['espec'], r['nb10']], 1): confere(t, i, j, v, 'T17')
vpn = [G3[1][m][80]['vpn'] for m in ['GB', 'COB', 'PLS', 'ROA', 'F', 'BA']]
assert f'{min(vpn):.3f}' == '0.988' and f'{max(vpn):.3f}' == '0.993', vpn   # faixa do VPN citada na nota
i = linha(t, 'Referência sem informação'); confere(t, i, 1, G3[1]['_prev'], 'T17'); confere(t, i, 2, G3[1]['_brier_ref'], 'T17')
t = acha('Restritiva')
for rot_, nome in [('Definição principal', 'principal'), ('Sem as entradas exclusivas do critério de EBITDA', 'sem entradas so EBITDA'),
                   ('Restritiva: patrimônio líquido negativo ou recuperação judicial', 'restritiva (PL ou RJ)')]:
    E, y, _ = EV[nome]['ref']; i = linha(t, rot_); confere(t, i, 1, len(y), 'T18'); confere(t, i, 2, int(y.sum()), 'T18')
    for j, m in enumerate(['F', 'GB', 'COB', 'PLS'], 3): confere(t, i, j, np.mean(EV[nome]['res'][m]), 'T18')
t = acha('Somente a primeira entrada de cada firma')
rb, rf, nb, eb, nf, ef, *_ = EF['F']; rs, ns, es, *_ = EF['E']; rc, nc, ec, *_ = EF['E2']; cal = RB['cal']; sv = RB['sobrev']
for rot_, n_, e_, v in [('Especificação principal', nb, eb, rb), ('Excluídas as entradas exclusivamente por recuperação judicial', cal['n'], cal['evk'], cal),
                        ('Somente a primeira entrada de cada firma', nf, ef, rf), ('Saídas associadas a distress tratadas como evento', ns, es, rs),
                        ('Saídas por dificuldade financeira segundo o cadastro, como evento', nc, ec, rc),
                        ('Somente firmas com registro ativo ao fim do período', sv['n'], sv['ev'], dict(F=sv['F'], PLS=sv['PLS'], COB=sv['COB'], ROA=N['sv_ROA']))]:
    i = linha(t, rot_); confere(t, i, 1, n_, 'T19'); confere(t, i, 2, e_, 'T19')
    for j, m in enumerate(['F', 'PLS', 'COB', 'ROA'], 3): confere(t, i, j, v[m], 'T19')
t = acha('Escore em nível e defasado'); lg = RB['lag']
for rot_, k, base in [('Escore sintético em nível', 'F', None), ('Escore em nível e defasado', 'F_L', 'F'), ('Cobertura de juros em nível', 'C', None),
                      ('Cobertura em nível e defasada', 'C_L', 'C'), ('Escore supervisionado, oito níveis', 'P8', None),
                      ('Escore supervisionado, oito níveis e oito variações', 'P16', 'P8')]:
    i = linha(t, rot_); confere(t, i, 1, lg[k], 'T20')
    if base: confere(t, i, 2, lg[k] - lg[base], 'T20')

# ---------------------------------------------------------------- texto da 5.6: escore com os tres indicadores (script 16)
if os.path.exists(os.path.join(R, 'tres_indicadores.pkl')):
    TI = L('tres_indicadores.pkl'); txt = ''.join(t.text or '' for t in root.iter(W + 't'))
    f3 = lambda x: f'{x:.3f}'.replace('.', ',')
    esperados = [f3(TI[1]['ref']['F3']), f3(TI[2]['ref']['F3']), f3(-TI[2]['cmp']['COB vs F3'][0]), f3(-TI[1]['cmp']['ROA vs F3'][0])]
    esperados += [f3(TI[h]['puros'][k]['auc']['F3']) for h in (1, 2) for k in ['EBITDA puras', 'PL puras', 'RJ puras']]
    faltam = [e for e in esperados if e not in txt]
    print(f'texto do escore com tres indicadores: {len(esperados) - len(faltam)} de {len(esperados)} valores encontrados', faltam or '')
    if faltam: erros.append(f'5.6 tres indicadores: {faltam}')

print(f'celulas conferidas: {conferidas} | divergencias: {len(erros)}')
for e in erros: print('  ', e)
