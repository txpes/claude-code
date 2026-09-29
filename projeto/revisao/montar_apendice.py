"""Monta a versao final do artigo: move as tabelas de validacao, avaliacao complementar e robustez para o
Apendice A (depois das referencias) e renumera todas as mencoes a tabelas no texto, nas notas e nas celulas.
Opera sobre a versao limpa (alteracoes ja aceitas); a versao com alteracoes controladas mantem a ordem e a
numeracao originais, para que cada mudanca de conteudo possa ser conferida contra o original.
A nota de decisoes, que remete a tabelas do artigo, recebe so a renumeracao.
Uso: python montar_apendice.py artigo|nota entrada_limpa.docx saida.docx"""
import sys, re, zipfile, shutil, copy
from lxml import etree

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
XML_SPACE = '{http://www.w3.org/XML/1998/namespace}space'
modo, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
assert modo in ('artigo', 'nota')

# numeracao original -> final. Corpo: tabelas que sustentam hipoteses ou o argumento central.
APENDICE = [8, 9, 11, 18, 19, 20]
CORPO = [1, 2, 3, 4, 5, 6, 7, 10, 12, 13, 14, 15, 16, 17]
MAPA = {n: str(i) for i, n in enumerate(CORPO, 1)}
MAPA.update({n: f'A.{i}' for i, n in enumerate(APENDICE, 1)})

texto = lambda el: ''.join(t.text or '' for t in el.iter(W + 't'))
log = []


def trocar_no_paragrafo(p, padrao, func):
    """Substitui ocorrencias de `padrao` no texto do paragrafo, mesmo quando a ocorrencia atravessa varios runs."""
    nos = [t for t in p.iter(W + 't')]
    if not nos: return 0
    txt = ''.join(t.text or '' for t in nos)
    ms = list(re.finditer(padrao, txt))
    for m in reversed(ms):
        s, e, novo = m.start(), m.end(), func(m)
        pos = 0
        for t in nos:
            a, b = pos, pos + len(t.text or ''); pos = b
            if b <= s or a >= e: continue
            ini, fim = max(s, a) - a, min(e, b) - a
            t.text = t.text[:ini] + (novo if a <= s < b else '') + t.text[fim:]
            t.set(XML_SPACE, 'preserve')
    return len(ms)


def renumerar(body):
    """Renumeracao simultanea de todas as mencoes, no singular e no plural ("Tabelas 9 a 11", "Tabelas 13 e 14")."""
    lista = lambda ns: ', '.join(ns[:-1]) + ' e ' + ns[-1]
    def novo(m):                                   # um unico padrao, para que nenhum numero seja trocado duas vezes
        if m.group(1): return 'Tabelas ' + lista([MAPA[k] for k in range(int(m.group(1)), int(m.group(2)) + 1)])
        if m.group(3): return f'Tabelas {MAPA[int(m.group(3))]} e {MAPA[int(m.group(4))]}'
        return 'Tabela ' + MAPA[int(m.group(5))]
    padrao = r'\bTabelas (\d+) a (\d+)\b|\bTabelas (\d+) e (\d+)\b|\bTabela (\d+)\b'
    total = sum(trocar_no_paragrafo(p, padrao, novo) for p in body.iter(W + 'p'))
    log.append(f'OK     {total} mencoes renumeradas')
    return total


def paragrafo_como(modelo, conteudo):
    """Novo paragrafo com a formatacao de paragrafo e do primeiro run de `modelo`."""
    p = etree.Element(W + 'p')
    ppr = modelo.find(W + 'pPr')
    if ppr is not None: p.append(copy.deepcopy(ppr))
    r = etree.SubElement(p, W + 'r')
    r0 = modelo.find(W + 'r')
    if r0 is not None and r0.find(W + 'rPr') is not None: r.append(copy.deepcopy(r0.find(W + 'rPr')))
    t = etree.SubElement(r, W + 't'); t.text = conteudo; t.set(XML_SPACE, 'preserve')
    return p


tmp = dst + '.tmp'
with zipfile.ZipFile(src) as zi, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
    for item in zi.infolist():
        data = zi.read(item.filename)
        if item.filename == 'word/document.xml' and modo == 'nota':
            root = etree.fromstring(data); renumerar(root.find(W + 'body'))
            data = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
        elif item.filename == 'word/document.xml':
            root = etree.fromstring(data)
            body = root.find(W + 'body')
            filhos = list(body)

            # 1. blocos a mover: legenda, tabela e nota de fonte, exatamente nessa sequencia
            blocos = []
            for n in APENDICE:
                cap = [el for el in filhos if el.tag == W + 'p' and re.match(rf'Tabela {n} – ', texto(el))]
                assert len(cap) == 1, f'legenda da Tabela {n}: {len(cap)}'
                i = filhos.index(cap[0])
                tbl, fonte = filhos[i + 1], filhos[i + 2]
                assert tbl.tag == W + 'tbl' and texto(fonte).startswith('Fonte:'), f'Tabela {n}: sequencia inesperada'
                blocos.append((n, [cap[0], tbl, fonte]))

            # 2. titulo e abertura do apendice, depois da ultima referencia
            tit_ref = next(el for el in filhos if el.tag == W + 'p' and texto(el).strip() == 'Referências')
            corpo_modelo = next(el for el in filhos if el.tag == W + 'p' and texto(el).startswith('Esse resultado delimita'))
            ultima = [el for el in filhos if el.tag == W + 'p' and texto(el).strip()][-1]
            assert texto(ultima).startswith('ZMIJEWSKI'), texto(ultima)[:40]
            tit = paragrafo_como(tit_ref, 'APÊNDICE A – TABELAS COMPLEMENTARES')
            ppr = tit.find(W + 'pPr')
            if ppr is None: ppr = etree.SubElement(tit, W + 'pPr'); tit.remove(ppr); tit.insert(0, ppr)
            antes = [c for c in ppr if c.tag in (W + 'pStyle', W + 'keepNext', W + 'keepLines')]   # ordem do esquema
            ppr.insert(len(antes), etree.Element(W + 'pageBreakBefore'))
            abertura = paragrafo_como(corpo_modelo,
                'Este apêndice reúne as tabelas de validação convergente, de avaliação complementar e de robustez citadas no texto. '
                'A numeração segue a ordem em que são mencionadas.')
            ancora = ultima
            for el in [tit, abertura] + [x for _, b in blocos for x in b]:
                ancora.addnext(el); ancora = el
            log.append(f'OK     apendice A com as Tabelas {", ".join(map(str, APENDICE))} (originais)')

            # 3. a Tabela 8 original nao era citada no texto; passa a ser
            alvo = next(el for el in body.iter(W + 'p') if 'a área sob a curva para discriminar essa posição é de 0,782' in texto(el))
            k = trocar_no_paragrafo(alvo, r'a área sob a curva para discriminar essa posição é de 0,782',
                                    lambda m: m.group(0) + ' (Tabela A.1)')
            assert k == 1
            log.append('OK     5.2: remissao a Tabela A.1')

            # 4. renumeracao de todas as mencoes (texto, legendas, notas e celulas)
            renumerar(body)
            data = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
        zo.writestr(item, data)
shutil.move(tmp, dst)
print('\n'.join(log)); print('saida:', dst)
print('mapa:', ', '.join(f'{k}->{v}' for k, v in sorted(MAPA.items())))
