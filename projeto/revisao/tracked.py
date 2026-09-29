"""Edicao de .docx com alteracoes controladas (w:ins / w:del), para o autor aceitar ou rejeitar no Word."""
import copy, datetime, re, zipfile, shutil, os
import docx
from docx.oxml.ns import qn

AUTOR = 'Revisão'
DATA = datetime.datetime(2026, 9, 28, 12, 0).strftime('%Y-%m-%dT%H:%M:%SZ')
_id = [9000]


def _nid():
    _id[0] += 1
    return str(_id[0])


def _mk(tag, **attrs):
    el = docx.oxml.OxmlElement(tag)
    for k, v in attrs.items():
        el.set(qn(k), v)
    return el


def _run_text(r):
    return ''.join(t.text or '' for t in r.findall(qn('w:t')))


def _split_run(r, pos):
    """divide o run r na posicao pos do seu texto; devolve (esquerda, direita)"""
    txt = _run_text(r)
    left, right = copy.deepcopy(r), copy.deepcopy(r)
    for rr, s in ((left, txt[:pos]), (right, txt[pos:])):
        for t in rr.findall(qn('w:t')):
            rr.remove(t)
        t = _mk('w:t'); t.text = s; t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); rr.append(t)
    r.addnext(right); r.addnext(left); r.getparent().remove(r)
    return left, right


def _runs(p_el):
    return [r for r in p_el.iterchildren(qn('w:r'))]


def replace(p, old, new):
    """substitui old por new no paragrafo p (python-docx Paragraph), como alteracao controlada"""
    el = p._p
    runs = _runs(el)
    texts = [_run_text(r) for r in runs]
    full = ''.join(texts)
    i = full.find(old)
    if i < 0:
        return False
    j = i + len(old)
    # isola os runs que cobrem exatamente [i, j)
    pos = 0
    for r, t in zip(runs, texts):
        a, b = pos, pos + len(t)
        if a < i < b:
            _split_run(r, i - a)
            return replace(p, old, new)
        if a < j < b:
            _split_run(r, j - a)
            return replace(p, old, new)
        pos = b
    pos = 0; alvo = []
    for r, t in zip(runs, texts):
        a, b = pos, pos + len(t)
        if a >= i and b <= j and b > a:
            alvo.append(r)
        pos = b
    rpr = alvo[0].find(qn('w:rPr')) if alvo else None
    d = _mk('w:del', **{'w:id': _nid(), 'w:author': AUTOR, 'w:date': DATA})
    alvo[0].addprevious(d)
    for r in alvo:
        for t in r.findall(qn('w:t')):
            t.tag = qn('w:delText')
        d.append(r)
    if new:
        ins = _mk('w:ins', **{'w:id': _nid(), 'w:author': AUTOR, 'w:date': DATA})
        nr = _mk('w:r')
        if rpr is not None:
            nr.append(copy.deepcopy(rpr))
        t = _mk('w:t'); t.text = new; t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); nr.append(t)
        ins.append(nr); d.addnext(ins)
    return True


def insert_after(p, text, modelo=None):
    """insere um paragrafo novo depois de p, copiando a formatacao de modelo (ou de p)"""
    base = (modelo or p)._p
    novo = copy.deepcopy(base)
    for ch in list(novo):
        if ch.tag != qn('w:pPr'):
            novo.remove(ch)
    ppr = novo.find(qn('w:pPr'))
    if ppr is None:
        ppr = _mk('w:pPr'); novo.insert(0, ppr)
    rp = ppr.find(qn('w:rPr'))
    if rp is None:
        rp = _mk('w:rPr'); ppr.append(rp)
    rp.append(_mk('w:ins', **{'w:id': _nid(), 'w:author': AUTOR, 'w:date': DATA}))
    ins = _mk('w:ins', **{'w:id': _nid(), 'w:author': AUTOR, 'w:date': DATA})
    brun = next(iter(_runs(base)), None)
    nr = _mk('w:r')
    if brun is not None and brun.find(qn('w:rPr')) is not None:
        nr.append(copy.deepcopy(brun.find(qn('w:rPr'))))
    t = _mk('w:t'); t.text = text; t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); nr.append(t)
    ins.append(nr); novo.append(ins)
    p._p.addnext(novo)
    return novo


def delete_paragraph(p):
    """marca todo o paragrafo como excluido"""
    el = p._p
    runs = _runs(el)
    if runs:
        d = _mk('w:del', **{'w:id': _nid(), 'w:author': AUTOR, 'w:date': DATA})
        runs[0].addprevious(d)
        for r in runs:
            for t in r.findall(qn('w:t')):
                t.tag = qn('w:delText')
            d.append(r)
    ppr = el.find(qn('w:pPr'))
    if ppr is None:
        ppr = _mk('w:pPr'); el.insert(0, ppr)
    rp = ppr.find(qn('w:rPr'))
    if rp is None:
        rp = _mk('w:rPr'); ppr.append(rp)
    rp.append(_mk('w:del', **{'w:id': _nid(), 'w:author': AUTOR, 'w:date': DATA}))


def consertar_midia(src, dst):
    """copia o .docx trocando a extensao .undefined das imagens PNG por .png"""
    tmp = dst + '.tmp'
    with zipfile.ZipFile(src) as zi, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
        for item in zi.infolist():
            data = zi.read(item.filename)
            nome = item.filename
            if nome.endswith('.undefined'):
                nome = nome[:-len('.undefined')] + '.png'
            if nome == 'word/_rels/document.xml.rels':
                data = data.replace(b'.undefined"', b'.png"')
            zo.writestr(nome, data)
    shutil.move(tmp, dst)


def insert_row_after(row, valores):
    """insere, como alteracao controlada, uma linha de tabela depois de row (python-docx _Row), copiando o formato"""
    novo = copy.deepcopy(row._tr)
    trpr = novo.find(qn('w:trPr'))
    if trpr is None:
        trpr = _mk('w:trPr'); novo.insert(0, trpr)
    trpr.append(_mk('w:ins', **{'w:id': _nid(), 'w:author': AUTOR, 'w:date': DATA}))
    tcs = novo.findall(qn('w:tc'))
    assert len(tcs) == len(valores), (len(tcs), len(valores))
    for tc, v in zip(tcs, valores):
        ps = tc.findall(qn('w:p'))
        for extra in ps[1:]:
            tc.remove(extra)
        p = ps[0]
        brun = next(iter(_runs(p)), None)
        rpr = copy.deepcopy(brun.find(qn('w:rPr'))) if brun is not None and brun.find(qn('w:rPr')) is not None else None
        for ch in list(p):
            if ch.tag != qn('w:pPr'):
                p.remove(ch)
        ins = _mk('w:ins', **{'w:id': _nid(), 'w:author': AUTOR, 'w:date': DATA})
        nr = _mk('w:r')
        if rpr is not None:
            nr.append(rpr)
        t = _mk('w:t'); t.text = v; t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); nr.append(t)
        ins.append(nr); p.append(ins)
    row._tr.addnext(novo)
    return novo


def insert_column(table, depois_de, cabecalho, valores_por_rotulo, largura_twips=None):
    """insere, como alteracao controlada, uma coluna depois da coluna de indice depois_de.
    valores_por_rotulo: funcao(indice_linha, texto_primeira_celula) -> texto da nova celula"""
    tbl = table._tbl
    grid = tbl.find(qn('w:tblGrid'))
    cols = grid.findall(qn('w:gridCol'))
    novo_gc = copy.deepcopy(cols[depois_de]); cols[depois_de].addnext(novo_gc)
    if largura_twips:
        # redistribui: reduz proporcionalmente as demais para manter a largura total
        tot = sum(int(c.get(qn('w:w'))) for c in cols)
        novo_gc.set(qn('w:w'), str(largura_twips))
        fator = (tot - largura_twips) / tot
        for c in cols:
            c.set(qn('w:w'), str(int(int(c.get(qn('w:w'))) * fator)))
    for i, tr in enumerate(tbl.findall(qn('w:tr'))):
        tcs = tr.findall(qn('w:tc'))
        base = tcs[depois_de] if depois_de < len(tcs) else tcs[-1]
        span = base.find(qn('w:tcPr') + '/' + qn('w:gridSpan'))
        texto0 = ''.join(t.text or '' for t in tcs[0].iter(qn('w:t')))
        novo = copy.deepcopy(base)
        tcpr = novo.find(qn('w:tcPr'))
        if tcpr is not None:
            w = tcpr.find(qn('w:tcW'))
            if w is not None and largura_twips:
                w.set(qn('w:w'), str(largura_twips)); w.set(qn('w:type'), 'dxa')
            cell_ins = _mk('w:cellIns', **{'w:id': _nid(), 'w:author': AUTOR, 'w:date': DATA})
            tcpr.append(cell_ins)
        if span is not None:
            # linha de titulo mesclada: apenas amplia o gridSpan da celula existente
            span.set(qn('w:val'), str(int(span.get(qn('w:val'))) + 1))
            continue
        ps = novo.findall(qn('w:p'))
        for extra in ps[1:]:
            novo.remove(extra)
        p = ps[0]
        brun = next(iter(_runs(p)), None)
        rpr = copy.deepcopy(brun.find(qn('w:rPr'))) if brun is not None and brun.find(qn('w:rPr')) is not None else None
        for ch in list(p):
            if ch.tag != qn('w:pPr'):
                p.remove(ch)
        v = cabecalho if i == 0 else valores_por_rotulo(i, texto0)
        if v:
            ins = _mk('w:ins', **{'w:id': _nid(), 'w:author': AUTOR, 'w:date': DATA})
            nr = _mk('w:r')
            if rpr is not None:
                nr.append(rpr)
            t = _mk('w:t'); t.text = v; t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); nr.append(t)
            ins.append(nr); p.append(ins)
        base.addnext(novo)
    # alinha a largura de cada celula a grade redistribuida
    larg = [c.get(qn('w:w')) for c in grid.findall(qn('w:gridCol'))]
    for tr in tbl.findall(qn('w:tr')):
        for k, tc in enumerate(tr.findall(qn('w:tc'))):
            w = tc.find(qn('w:tcPr') + '/' + qn('w:tcW'))
            if w is not None and k < len(larg) and tc.find(qn('w:tcPr') + '/' + qn('w:gridSpan')) is None:
                w.set(qn('w:w'), larg[k]); w.set(qn('w:type'), 'dxa')


def insert_after_rotulado(p, rotulo, texto, modelo):
    """insere depois de p um paragrafo 'rotulo + texto', com o rotulo no formato do 1o run do modelo e o texto no do 2o"""
    novo = insert_after(p, rotulo, modelo)
    runs_modelo = _runs(modelo._p)
    rpr2 = runs_modelo[1].find(qn('w:rPr')) if len(runs_modelo) > 1 else None
    ins = _mk('w:ins', **{'w:id': _nid(), 'w:author': AUTOR, 'w:date': DATA})
    nr = _mk('w:r')
    if rpr2 is not None:
        nr.append(copy.deepcopy(rpr2))
    t = _mk('w:t'); t.text = texto; t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); nr.append(t)
    ins.append(nr); novo.append(ins)
    return novo
