"""Gera uma copia do .docx com todas as alteracoes controladas aceitas (versao limpa, para leitura).
Uso: python aceitar_alteracoes.py entrada.docx saida.docx"""
import sys, zipfile, shutil
from lxml import etree

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
src, dst = sys.argv[1], sys.argv[2]
tmp = dst + '.tmp'
with zipfile.ZipFile(src) as zi, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
    for item in zi.infolist():
        data = zi.read(item.filename)
        if item.filename == 'word/document.xml':
            root = etree.fromstring(data)
            for d in list(root.iter(W + 'del')):
                pai = d.getparent()
                if pai.tag == W + 'rPr' and pai.getparent().tag == W + 'pPr':
                    p = pai.getparent().getparent(); p.getparent().remove(p)      # paragrafo inteiro excluido
                elif pai.tag == W + 'trPr':
                    tr = pai.getparent(); tr.getparent().remove(tr)                # linha de tabela excluida
                else:
                    pai.remove(d)
            for ins in list(root.iter(W + 'ins')):
                pai = ins.getparent()
                if pai.tag in (W + 'rPr', W + 'trPr'):
                    pai.remove(ins)                                                # marca de insercao
                else:
                    i = pai.index(ins)
                    for k, filho in enumerate(list(ins)):
                        pai.insert(i + k, filho)                                   # desembrulha o conteudo inserido
                    pai.remove(ins)
            for ci in list(root.iter(W + 'cellIns')):
                ci.getparent().remove(ci)
            data = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
        zo.writestr(item, data)
shutil.move(tmp, dst)
print('versao limpa:', dst)
