"""Aplica as correcoes de celula gravadas por verificar_artigo.py (mesma ordem de tabelas e mesma grade de celulas).
Uso: python corrigir_celulas.py entrada.docx correcoes.json saida.docx"""
import sys, json, re, copy
import docx

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
XS = '{http://www.w3.org/XML/1998/namespace}space'
d = docx.Document(sys.argv[1]); C = json.load(open(sys.argv[2], encoding='utf-8'))
tbls = list(d.element.body.iter(W + 'tbl')); n = 0
for c in C:
    tc = tbls[c['tabela']].findall(W + 'tr')[c['linha']].findall(W + 'tc')[c['coluna']]
    ts = list(tc.iter(W + 't')); atual = ''.join(t.text or '' for t in ts).strip()
    if atual != c['antigo'].strip():
        sys.exit(f"celula {c} nao confere: {atual!r}")
    ts[0].text = c['novo']; ts[0].set(XS, 'preserve')
    for t in ts[1:]: t.text = ''
    n += 1
d.save(sys.argv[3]); print(n, 'celulas corrigidas ->', sys.argv[3])
