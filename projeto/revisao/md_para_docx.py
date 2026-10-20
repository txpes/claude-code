"""Converte um markdown simples (titulos, paragrafos, listas, tabelas, negrito e italico) em docx, com Times New Roman 12.
Uso: python md_para_docx.py entrada.md saida.docx"""
import sys, re
import docx
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

src, dst = sys.argv[1:3]
d = docx.Document()
sec = d.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.top_margin = sec.left_margin = Cm(3); sec.bottom_margin = sec.right_margin = Cm(2)
st = d.styles['Normal']; st.font.name = 'Times New Roman'; st.font.size = Pt(12)
st.element.rPr.rFonts.set(docx.oxml.ns.qn('w:eastAsia'), 'Times New Roman')
st.paragraph_format.space_after = Pt(6); st.paragraph_format.line_spacing = 1.15
for nome in ('Title', 'Heading 1', 'Heading 2', 'List Bullet', 'List Bullet 2', 'List Number'):
    s = d.styles[nome]; s.font.name = 'Times New Roman'; s.font.color.rgb = docx.shared.RGBColor(0x1d, 0x24, 0x33)
    rf = s.element.rPr.rFonts
    for k in ('w:asciiTheme', 'w:hAnsiTheme', 'w:eastAsiaTheme', 'w:cstheme'):
        rf.attrib.pop(docx.oxml.ns.qn(k), None)
    for k in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        rf.set(docx.oxml.ns.qn(k), 'Times New Roman')
d.styles['Title'].font.size = Pt(16); d.styles['Heading 1'].font.size = Pt(13)


def inline(p, txt, tam=None):
    for parte in re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)', txt):
        if not parte: continue
        if parte.startswith('**'): r = p.add_run(parte[2:-2]); r.bold = True
        elif parte.startswith('*'): r = p.add_run(parte[1:-1]); r.italic = True
        elif parte.startswith('`'): r = p.add_run(parte[1:-1])
        else: r = p.add_run(parte)
        if tam: r.font.size = Pt(tam)


linhas = open(src, encoding='utf-8').read().split('\n'); i = 0
while i < len(linhas):
    l = linhas[i]
    if l.startswith('# '): d.add_paragraph(l[2:], style='Title')
    elif l.startswith('## '): d.add_paragraph(l[3:], style='Heading 1')
    elif l.startswith('|'):
        bloco = []
        while i < len(linhas) and linhas[i].startswith('|'):
            if not re.match(r'^\|[\s\-|:]+\|$', linhas[i]):
                bloco.append([c.strip() for c in linhas[i].strip('|').split('|')])
            i += 1
        t = d.add_table(rows=len(bloco), cols=len(bloco[0])); t.style = 'Table Grid'; t.autofit = False
        larg = {4: [1.0, 4.0, 7.6, 3.4], 3: [6.0, 3.0, 7.0]}.get(len(bloco[0]))
        if bloco[0][0] == 'Parte': larg = [4.6, 1.6, 2.2, 7.6]
        if larg:
            for c, col in enumerate(t.columns): col.width = Cm(larg[c])
            grade = t._tbl.tblGrid.findall(docx.oxml.ns.qn('w:gridCol'))
            for c, g in enumerate(grade): g.set(docx.oxml.ns.qn('w:w'), str(int(larg[c] * 567)))
        for r, row in enumerate(bloco):
            for c, val in enumerate(row):
                cel = t.cell(r, c); cel.text = ''; p = cel.paragraphs[0]
                if larg: cel.width = Cm(larg[c])
                p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.0
                inline(p, f'**{val}**' if r == 0 and not val.startswith('**') else val, 10)
        d.add_paragraph()
        continue
    elif re.match(r'^ {2,}- ', l): inline(d.add_paragraph(style='List Bullet 2'), l.strip()[2:])
    elif l.startswith('- '): inline(d.add_paragraph(style='List Bullet'), l[2:])
    elif re.match(r'^\d+\. ', l):
        p = d.add_paragraph(); p.paragraph_format.left_indent = Cm(0.8); p.paragraph_format.first_line_indent = Cm(-0.6)
        inline(p, l)
    elif l.startswith('   ') and l.strip():
        p = d.add_paragraph(); p.paragraph_format.left_indent = Cm(1.27); inline(p, l.strip())
    elif l.strip():
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; inline(p, l)
    i += 1
d.core_properties.author = 'Thomas G. M. Lopes'; d.core_properties.title = 'Revisão do artigo: o que foi pedido e o que foi feito'
d.save(dst); print('->', dst)
