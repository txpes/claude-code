"""Gera a v3 do artigo a partir da v2 (versao limpa, sem alteracoes controladas), aplicando uma lista de alteracoes em JSON.

Regras:
  - toda alteracao localiza seu alvo por texto que casa exatamente uma vez; se casar zero ou mais de uma vez, falha e para;
  - a renumeracao de secoes vem primeiro, e as alteracoes seguintes sao escritas ja na numeracao nova;
  - tabelas e figuras novas recebem marcadores ({TAB:id}, {FIG:id}), resolvidos no fim, quando todas as tabelas e figuras
    do corpo sao renumeradas pela ordem em que aparecem; as do apendice mantem a serie A.n.

Uso: python aplicar_v3.py base.docx alteracoes.json saida.docx [pasta das imagens]"""
import sys, re, json, copy, os
import docx
from docx.shared import Emu
from lxml import etree

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
M = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'
XS = '{http://www.w3.org/XML/1998/namespace}space'
src, alt, dst = sys.argv[1:4]
IMG = sys.argv[4] if len(sys.argv) > 4 else '.'
d = docx.Document(src)
body = d.element.body
log = []


class Falha(Exception):
    pass


def texto(el):
    return ''.join(t.text or '' for t in el.iter(W + 't'))


def topo():
    return [el for el in body.iterchildren() if el.tag in (W + 'p', W + 'tbl')]


def paragrafos():
    return list(body.iter(W + 'p'))


def unico_topo(prefixo, onde='inicio'):
    ach = [el for el in topo() if el.tag == W + 'p' and (texto(el).startswith(prefixo) if onde == 'inicio' else prefixo in texto(el))]
    if len(ach) != 1:
        raise Falha(f'ancora {prefixo[:60]!r}: {len(ach)} ocorrencias')
    return ach[0]


def trocar(p, padrao, func):
    """substitui ocorrencias de um padrao no texto do paragrafo, mesmo atravessando varios runs"""
    nos = list(p.iter(W + 't'))
    txt = ''.join(t.text or '' for t in nos)
    ms = list(re.finditer(padrao, txt))
    for m in reversed(ms):
        s, e, novo = m.start(), m.end(), func(m)
        pos = 0
        for t in nos:
            a, b = pos, pos + len(t.text or ''); pos = b
            if b <= s or a >= e:
                continue
            ini, fim = max(s, a) - a, min(e, b) - a
            t.text = t.text[:ini] + (novo if a <= s < b else '') + t.text[fim:]
            t.set(XS, 'preserve')
    return len(ms)


def novo_paragrafo(modelo, conteudo):
    p = etree.Element(W + 'p')
    if modelo.find(W + 'pPr') is not None:
        p.append(copy.deepcopy(modelo.find(W + 'pPr')))
    r0 = next(modelo.iter(W + 'r'), None)
    r = etree.SubElement(p, W + 'r')
    if r0 is not None and r0.find(W + 'rPr') is not None:
        r.append(copy.deepcopy(r0.find(W + 'rPr')))
    t = etree.SubElement(r, W + 't'); t.text = conteudo; t.set(XS, 'preserve')
    return p


def fim_das_referencias():
    tops = topo()
    i = next(k for k, el in enumerate(tops) if texto(el).strip() == 'Referências')
    return set(tops[i:])


# ------------------------------------------------------------------ operacoes
def op_renumerar_secoes(mapa):
    excluir = fim_das_referencias(); n_tit = n_rem = 0
    for el in topo():
        if el.tag != W + 'p' or el in excluir:
            continue
        t = texto(el)
        m = re.match(r'^(\d+(?:\.\d+)?)(\.?) ', t)
        if m and len(t) < 90 and m.group(1) in mapa:            # titulo de secao ou subsecao
            trocar(el, r'^' + re.escape(m.group(0)), lambda mm, g=m: mapa[g.group(1)] + g.group(2) + ' '); n_tit += 1
            continue
    for p in paragrafos():
        if any(p is x or p in x.iter(W + 'p') for x in excluir if x.tag == W + 'p'):
            continue
        n_rem += trocar(p, r'\b((?:sub)?seç(?:ão|ões))\s+(\d+(?:\.\d+)?)((?:(?:,\s*|\s+e\s+)\d+(?:\.\d+)?)*)',
                        lambda m: m.group(1) + ' ' + re.sub(r'\d+(?:\.\d+)?', lambda x: mapa.get(x.group(0), x.group(0)), m.group(2) + m.group(3)))
    log.append(f'OK     secoes renumeradas: {n_tit} titulos, {n_rem} remissoes')


def op_substituir(antigo, novo):
    ach = [p for p in paragrafos() if antigo in texto(p)]
    if len(ach) != 1 or texto(ach[0]).count(antigo) != 1:
        raise Falha(f'substituir {antigo[:60]!r}: {len(ach)} paragrafos')
    trocar(ach[0], re.escape(antigo), lambda m: novo)
    log.append(f'OK     substituido: {antigo[:50]!r}')


def op_paragrafo(inicio, novo):
    p = unico_topo(inicio)
    rr = list(p.iter(W + 'r')); ts = list(p.iter(W + 't'))
    ts[0].text = novo; ts[0].set(XS, 'preserve')
    for t in ts[1:]:
        t.getparent().remove(t)
    log.append(f'OK     paragrafo reescrito: {inicio[:50]!r}')


def op_inserir_apos(ancora, modelo, textos, ancora_contem=False):
    a = unico_topo(ancora, 'contem' if ancora_contem else 'inicio'); mod = unico_topo(modelo)
    for tx in textos:
        n = novo_paragrafo(mod, tx); a.addnext(n); a = n
    log.append(f'OK     {len(textos)} paragrafo(s) inserido(s) depois de {ancora[:40]!r}')


def op_remover(inicio):
    p = unico_topo(inicio); p.getparent().remove(p)
    log.append(f'OK     removido: {inicio[:50]!r}')


def op_mover_apos(inicio, ancora, n=1):
    p = unico_topo(inicio); bloco = [p]
    for _ in range(n - 1):
        bloco.append(bloco[-1].getnext())
    a = unico_topo(ancora)
    for el in bloco:
        a.addnext(el); a = el
    log.append(f'OK     movido: {inicio[:40]!r} ({n} elementos) depois de {ancora[:40]!r}')


def op_figura_apos(ancora, modelo_legenda, legenda, imagem, fonte, largura_cm=15.24):
    cap = unico_topo(modelo_legenda); fig = cap.getnext(); fon = fig.getnext()
    assert fig.find('.//' + W + 'drawing') is not None and texto(fon).startswith('Fonte')
    novos = [copy.deepcopy(x) for x in (cap, fig, fon)]
    trocar(novos[0], r'.+', lambda m: legenda); trocar(novos[2], r'.+', lambda m: fonte)
    rid, img = d.part.get_or_add_image(os.path.join(IMG, imagem))
    blip = next(novos[1].iter('{http://schemas.openxmlformats.org/drawingml/2006/main}blip'))
    blip.set('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed', rid)
    cx = int(largura_cm / 2.54 * 914400); cy = int(cx * img.px_height / img.px_width)
    for ext in novos[1].iter():
        if ext.tag.endswith('}extent') or ext.tag.endswith('}ext'):
            if ext.get('cx') is not None:
                ext.set('cx', str(cx)); ext.set('cy', str(cy))
    maior = max([int(x.get('id')) for x in body.iter('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}docPr')] + [0])
    for k, x in enumerate(novos[1].iter('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}docPr')):
        x.set('id', str(maior + 1 + k)); x.set('name', f'Figura {maior + 1 + k}')
    a = unico_topo(ancora)
    for el in novos:
        a.addnext(el); a = el
    log.append(f'OK     figura inserida: {legenda[:50]!r}')


def op_tabela_apos(ancora, modelo_legenda, legenda, linhas, fonte, larguras=None):
    """copia a tabela modelo: 1a linha como cabecalho, 2a como corpo, ultima como fecho (bordas)"""
    cap = unico_topo(modelo_legenda); tbl = cap.getnext(); fon = tbl.getnext()
    assert tbl.tag == W + 'tbl' and texto(fon).startswith('Fonte')
    ncol = len(linhas[0]); trs = tbl.findall(W + 'tr')
    assert len(trs[0].findall(W + 'tc')) == ncol, 'numero de colunas do modelo'
    nt = copy.deepcopy(tbl)
    for tr in nt.findall(W + 'tr'):
        nt.remove(tr)
    def linha(modelo_tr, valores):
        tr = copy.deepcopy(modelo_tr)
        for tc, v in zip(tr.findall(W + 'tc'), valores):
            ps = tc.findall(W + 'p')
            for extra in ps[1:]:
                tc.remove(extra)
            ts = list(ps[0].iter(W + 't'))
            if not ts:
                raise Falha('celula modelo sem texto')
            ts[0].text = v; ts[0].set(XS, 'preserve')
            for t in ts[1:]:
                t.text = ''
        return tr
    nt.append(linha(trs[0], linhas[0]))
    for k, vals in enumerate(linhas[1:], 1):
        nt.append(linha(trs[-1] if k == len(linhas) - 1 else trs[2], vals))
    if larguras:
        for gc, w in zip(nt.find(W + 'tblGrid').findall(W + 'gridCol'), larguras):
            gc.set(W + 'w', str(w))
        for tr in nt.findall(W + 'tr'):
            for tc, w in zip(tr.findall(W + 'tc'), larguras):
                tw = tc.find(W + 'tcPr/' + W + 'tcW')
                if tw is not None:
                    tw.set(W + 'w', str(w)); tw.set(W + 'type', 'dxa')
    nc, nf = copy.deepcopy(cap), copy.deepcopy(fon)
    trocar(nc, r'.+', lambda m: legenda); trocar(nf, r'.+', lambda m: fonte)
    a = unico_topo(ancora)
    for el in (nc, nt, nf):
        a.addnext(el); a = el
    log.append(f'OK     tabela inserida: {legenda[:50]!r}')


def op_equacao(inicio, omml):
    p = unico_topo(inicio, 'contem')
    rs = p.findall(W + 'r')
    alvo = next(r for r in rs if r.find(W + 't') is not None and inicio in texto(r))
    tab = alvo.find(W + 'tab')
    novo_r = copy.deepcopy(alvo)
    for ch in list(novo_r):
        if ch.tag != W + 'rPr':
            novo_r.remove(ch)
    if tab is not None:
        etree.SubElement(novo_r, W + 'tab')
    alvo.addprevious(novo_r)
    om = etree.fromstring(f'<m:oMath xmlns:m="{M[1:-1]}" xmlns:w="{W[1:-1]}">{omml}</m:oMath>')
    alvo.addprevious(om)
    p.remove(alvo)
    sp = p.find(W + 'pPr/' + W + 'spacing')                      # entrelinha fixa corta a fracao; a equacao usa a automatica
    if sp is not None:
        sp.set(W + 'line', '240'); sp.set(W + 'lineRule', 'auto')
    log.append(f'OK     equacao convertida: {inicio[:40]!r}')


def renumerar_tabelas_figuras():
    """mapa pela ordem das legendas no corpo; apendice segue A.n; marcadores {TAB:id}/{FIG:id} resolvidos aqui"""
    tops = topo()
    i_ap = next((k for k, el in enumerate(tops) if texto(el).startswith('APÊNDICE')), len(tops))
    mapa = {}
    for tipo in ('Tabela', 'Figura'):
        n = 0
        for el in tops[:i_ap]:
            m = re.match(rf'{tipo} (\d+|\{{(?:TAB|FIG):\w+\}}) – ', texto(el))
            if m:
                n += 1; mapa[(tipo, m.group(1))] = str(n)
    pat = r'\b(Tabelas?|Figuras?) ((?:\d+|A\.\d+|\{(?:TAB|FIG):\w+\})(?:(?:,\s*|\s+e\s+|\s+a\s+)(?:\d+|A\.\d+|\{(?:TAB|FIG):\w+\}))*)'
    def novo(m):
        tipo = m.group(1).rstrip('s')
        return m.group(1) + ' ' + re.sub(r'(?<![.\d])\d+(?![.\d])|\{(?:TAB|FIG):\w+\}', lambda x: mapa.get((tipo, x.group(0)), x.group(0)), m.group(2))  # A.n fica como esta
    total = sum(trocar(p, pat, novo) for p in paragrafos())
    restos = [texto(p)[:80] for p in paragrafos() if '{TAB:' in texto(p) or '{FIG:' in texto(p)]
    if restos:
        raise Falha(f'marcadores nao resolvidos: {restos}')
    mud = {k: v for k, v in mapa.items() if k[1] != v}
    log.append(f'OK     tabelas e figuras renumeradas: {total} mencoes; mudancas {mud}')


OPS = {'renumerar_secoes': op_renumerar_secoes, 'substituir': op_substituir, 'paragrafo': op_paragrafo, 'inserir_apos': op_inserir_apos,
       'remover': op_remover, 'mover_apos': op_mover_apos, 'figura_apos': op_figura_apos, 'tabela_apos': op_tabela_apos, 'equacao': op_equacao}
try:
    for k, a in enumerate(json.load(open(alt, encoding='utf-8'))):
        a = dict(a); op = a.pop('op'); a.pop('motivo', None)
        OPS[op](**a)
    renumerar_tabelas_figuras()
except Falha as e:
    print('\n'.join(log)); print('FALHOU', e); sys.exit(1)
d.save(dst)
print('\n'.join(log)); print(f'{len(log)} operacoes, 0 falhas ->', dst)
