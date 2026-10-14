"""Checagens estruturais do artigo: remissoes a secoes, tabelas, figuras e equacoes; ordem de citacao; referencias.
Uso: python checar_estrutura.py artigo.docx"""
import sys, re, unicodedata
import docx

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
d = docx.Document(sys.argv[1])
tops = [el for el in d.element.body.iterchildren() if el.tag in (W + 'p', W + 'tbl')]
tx = lambda el: ''.join(t.text or '' for t in el.iter(W + 't'))
i_ref = next(k for k, el in enumerate(tops) if tx(el).strip() == 'Referências')
i_ap = next((k for k, el in enumerate(tops) if tx(el).startswith('APÊNDICE')), len(tops))
corpo = [tx(el) for el in tops[:i_ref]]
apend = [tx(el) for el in tops[i_ap:]]
refs = [tx(el) for el in tops[i_ref + 1:i_ap] if tx(el).strip() and tx(el).strip() != 'Disponibilidade de dados e código']
prob = []

# secoes
tit = {m.group(1) for t in corpo if len(t) < 100 for m in [re.match(r'^(\d+(?:\.\d+)?)\.? \S', t)] if m}
for t in corpo + apend:
    for m in re.finditer(r'\b(?:sub)?seç(?:ão|ões)\s+(\d+(?:\.\d+)?(?:(?:,\s*|\s+e\s+)\d+(?:\.\d+)?)*)', t):
        for n in re.findall(r'\d+(?:\.\d+)?', m.group(1)):
            if n not in tit:
                prob.append(f'remissao a secao inexistente {n}: {t[max(0, m.start() - 40):m.end() + 20]!r}')
seq = sorted(tit, key=lambda s: [int(x) for x in s.split('.')])
for a in seq:
    if '.' in a:
        s, k = a.split('.')
        if k != '1' and f'{s}.{int(k) - 1}' not in tit:
            prob.append(f'numeracao de subsecao com salto: {a}')

# tabelas e figuras: legendas sequenciais, toda legenda citada no texto, primeira mencao em ordem
for tipo in ('Tabela', 'Figura'):
    caps = [m.group(1) for t in corpo + apend for m in [re.match(rf'{tipo} (\d+|A\.\d+) – ', t)] if m]
    corpo_caps = [c for c in caps if not c.startswith('A.')]
    if corpo_caps != [str(k) for k in range(1, len(corpo_caps) + 1)]:
        prob.append(f'{tipo}s do corpo fora de sequencia: {corpo_caps}')
    ordem = []
    for t in corpo + apend:
        if re.match(rf'{tipo} (\d+|A\.\d+) – ', t):
            continue
        for m in re.finditer(rf'\b{tipo}s? ((?:\d+|A\.\d+)(?:(?:,\s*|\s+e\s+|\s+a\s+)(?:\d+|A\.\d+))*)', t):
            for n in re.findall(r'A\.\d+|\d+', m.group(1)):
                if n not in caps:
                    prob.append(f'{tipo} {n} citada e inexistente')
                if n not in ordem:
                    ordem.append(n)
    falt = [c for c in caps if c not in ordem]
    if falt:
        prob.append(f'{tipo}s sem mencao no texto: {falt}')
    oc = [o for o in ordem if not o.startswith('A.')]
    if oc != sorted(oc, key=int):
        prob.append(f'{tipo}s do corpo citadas fora de ordem: {oc}')
    print(f'{tipo}s: {len(caps)} legendas; ordem da primeira mencao: {ordem}')

# equacoes
eqs = [el for el in tops[:i_ref] if el.find('.//{http://schemas.openxmlformats.org/officeDocument/2006/math}oMath') is not None]
for n in re.findall(r'equaç(?:ão|ões) \((\d+)\)', ' '.join(corpo)):
    if int(n) > len(eqs):
        prob.append(f'equacao ({n}) citada e inexistente')
print('equacoes como objeto:', len(eqs))

# referencias: ordem alfabetica e cada uma citada
chave = lambda r: unicodedata.normalize('NFKD', r).encode('ascii', 'ignore').decode().upper()
autores = lambda r: chave(re.split(r'\. [A-Z][a-z]', r, 1)[0])      # bloco de autores; mesmos autores em ordem cronologica (ABNT)
for a, b in zip(refs, refs[1:]):
    if autores(a) > autores(b):
        prob.append(f'referencias fora de ordem alfabetica: {a[:30]!r} > {b[:30]!r}')
texto = ' '.join(corpo + apend)
for r in refs:
    sob = re.match(r'([A-ZÀ-ÿĘ\-’\' ]+?),', r)
    ano = re.findall(r'\b(19\d\d|20\d\d)\b', r)
    if not sob or not ano:
        continue
    nome = sob.group(1).strip().split(' ')[-1] if sob.group(1).strip().startswith(('DU ', 'VAN ', 'ADALET', 'TORRES')) else sob.group(1).strip()
    cand = [nome.title(), nome.upper(), nome.capitalize(), nome.title().replace('Mcgowan', 'McGowan')]
    if not any(c.lower() in texto.lower() for c in cand) or ano[-1] not in texto:
        prob.append(f'referencia possivelmente nao citada: {r[:60]!r}')
print('referencias:', len(refs), '| de 2020 em diante:', sum(int(re.findall(r'\b(?:19|20)\d\d\b', r)[-1]) >= 2020 for r in refs if re.findall(r'\b(?:19|20)\d\d\b', r)))
print('PROBLEMAS:', len(prob)); [print('  ', p) for p in prob]
