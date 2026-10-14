"""Compara duas execucoes do codigo (antes e depois da correcao do painel) e lista os numeros do texto do artigo que
precisam ser revistos.

1. Achata todos os escalares dos pickles e CSV das duas execucoes (mesma chave nas duas) e separa as quantidades cuja
   forma exibida mudou (tres casas, quatro casas e percentual com uma casa).
2. Varre os paragrafos do artigo, fora das tabelas, e marca cada numero exibido que coincide com a forma antiga de uma
   quantidade que mudou. Numeros que tambem coincidem com quantidades que nao mudaram sao marcados como ambiguos.
Uso: python comparar_execucoes.py <execucao antiga> <execucao nova> <artigo.docx> <saida.csv>"""
import sys, os, re, pickle, glob
import numpy as np, pandas as pd
import docx

A, B, DOC, OUT = sys.argv[1:5]
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def achatar(x, pref, out, prof=0):
    if prof > 8:
        return
    if isinstance(x, (bool, np.bool_)):
        return
    if isinstance(x, (int, float, np.integer, np.floating)):
        if np.isfinite(x): out[pref] = float(x)
    elif isinstance(x, dict):
        for k, v in x.items(): achatar(v, f'{pref}/{k}', out, prof + 1)
    elif isinstance(x, (list, tuple)):
        if len(x) <= 60:
            for k, v in enumerate(x): achatar(v, f'{pref}[{k}]', out, prof + 1)
    elif isinstance(x, pd.Series):
        if len(x) <= 400:
            for k, v in x.items(): achatar(v, f'{pref}/{k}', out, prof + 1)
    elif isinstance(x, pd.DataFrame):
        if x.size <= 4000:
            for c in x.columns:
                for k, v in x[c].items(): achatar(v, f'{pref}/{c}/{k}', out, prof + 1)
    elif isinstance(x, np.ndarray):
        if x.size <= 60:
            for k, v in enumerate(x.ravel()): achatar(v, f'{pref}[{k}]', out, prof + 1)


def carregar(d):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, '*.pkl'))):
        try: achatar(pickle.load(open(f, 'rb')), os.path.basename(f), out)
        except Exception: pass
    for f in sorted(glob.glob(os.path.join(d, '*.csv'))):
        try: achatar(pd.read_csv(f), os.path.basename(f), out)
        except Exception: pass
    return out


a, b = carregar(A), carregar(B)
comuns = sorted(set(a) & set(b))
formas = lambda v: {f'{v:.3f}'.replace('.', ','), f'{v:.4f}'.replace('.', ','), f'{100 * v:.1f}'.replace('.', ',')} if abs(v) < 1000 else {f'{v:,.0f}'.replace(',', '.')}
mudou, igual = {}, set()
for k in comuns:
    fa, fb = formas(a[k]), formas(b[k])
    for s in fa:
        alvo = s.lstrip('−-')
        if s in fb: igual.add(alvo)
        else: mudou.setdefault(alvo, set()).add(k)
print(f'{len(comuns)} quantidades comparadas; {len({k for v in mudou.values() for k in v})} com alguma forma exibida diferente')

d = docx.Document(DOC); linhas = []
for p in d.element.body.iterchildren():
    if p.tag != W + 'p': continue
    t = ''.join(x.text or '' for x in p.iter(W + 't'))
    if t.startswith(('Tabela ', 'Fonte:')) or len(t) < 40: continue
    for m in re.finditer(r'(?<![\d,.])\d{1,3}(?:\.\d{3})*,\d{1,4}(?![\d])|(?<![\d,.])\d{1,3}\.\d{3}(?![\d,])', t):
        s = m.group(0)
        if s in mudou:
            chaves = sorted(mudou[s])[:4]
            novos = sorted({f for k in mudou[s] for f in formas(b[k]) if len(f) == len(s) or f.count(',') == s.count(',')})[:6]
            linhas.append(dict(valor=s, ambiguo=s in igual, contexto=t[max(0, m.start() - 70):m.end() + 40], candidatos=' | '.join(novos), chaves=' ; '.join(chaves)))
pd.DataFrame(linhas).to_csv(OUT, index=False)
print(f'{len(linhas)} ocorrencias no texto a revisar ({sum(not x["ambiguo"] for x in linhas)} sem ambiguidade) -> {OUT}')
