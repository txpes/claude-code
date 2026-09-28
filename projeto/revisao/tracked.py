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
