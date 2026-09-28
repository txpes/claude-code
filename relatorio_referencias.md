# Relatório da conferência das referências

Base: `referencias_para_conferir.csv` na versão mais recente enviada (11 conferidas, 22 pendentes).
Data da conferência: 28/09/2026.

## Totais

| | n |
|---|---|
| Pendentes conferidas | 22 |
| — confere | 18 |
| — divergente | 3 (ids 17, 29, 33) |
| — não confirmada em fonte autorizada | 1 (id 3) |
| Entradas já marcadas como conferidas e reconferidas | 5 (ids 2, 6, 16, 25, 31) |
| — divergente | 1 (id 16) |

### Divergências por tipo de campo

| Campo | n | ids |
|---|---|---|
| autoria | 1 | 17 |
| título | 1 | 29 |
| número/suplemento | 2 | 16, 33 |
| **Total** | **4** | |

Além disso, a correção da id 17 exige ajustar a citação no texto. Isso está no JSON como uma quinta entrada, com `campo: "citacao_no_texto"`.

Todas as strings `antigo` do `correcoes_referencias.json` foram comparadas com o `document.xml` do artigo. Cada uma aparece exatamente uma vez.

## Divergências

1. **id 17, McGowan et al. (2018), autoria.** O sobrenome da primeira autora é *Adalet McGowan* (Müge Adalet McGowan), segundo os metadados da Oxford University Press (DOI 10.1093/epolic/eiy012). O próprio texto do BIS (id 4) cita "Adalet McGowan et al (2017)".
   - Referência corrigida: `ADALET McGOWAN, M.; ANDREWS, D.; MILLOT, V. ...`
   - Na citação do texto: "Adalet McGowan, Andrews e Millot (2018)".
   - Com a mudança, a entrada passa a ser ordenada pela letra A, antes de ALTMAN. A reordenação da lista não entra no JSON.

2. **id 29, Tymoigne (2010), título.** A capa do Working Paper n. 605 no site do Levy Institute traz "Detecting Ponzi Finance". Pela ABNT, nomes próprios mantêm a maiúscula, então fica "Detecting Ponzi finance". Os demais campos conferem: autor "Éric Tymoigne", WP n. 605, junho de 2010.

3. **id 33, Zmijewski (1984), suplemento.** O artigo saiu no suplemento de 1984 do *Journal of Accounting Research* (*Studies on Current Econometric Issues in Accounting Research*), não num número regular.
   - Evidência: no Crossref o artigo não tem número de fascículo. Ele fica intercalado com os textos "Discussion of…" do suplemento, e o comentário de Dietrich começa na p. 83, o que confirma o intervalo p. 59-82.
   - Proposta: `v. 22, supl., p. 59-82, 1984.`
   - Ressalva: a página do JSTOR (stable/2490859), que traria o nome do suplemento por extenso, bloqueou o acesso automatizado. A indicação de suplemento vem dos metadados do DOI, não da página do JSTOR.

4. **id 16, Mantoan, Centeno e Feijó (2021), número.** Essa entrada já estava marcada como conferida, mas omite o fascículo: é v. 2, **n. 3**, p. 529-550 (Springer, DOI 10.1007/s43253-021-00051-6). A própria anotação da planilha já registrava "v.2(3)".

## Não confirmada em fonte autorizada

**id 3, BRASIL (2019), Nota Técnica SEI n. 21/2019/CDCOF/SURIN/STN.** Não localizei esse documento em nenhuma fonte oficial: Tesouro Transparente, gov.br/tesouronacional, cdn.tesouro.gov.br e Diário Oficial. Também não apareceu em buscas abertas.

- O Tesouro atribui a metodologia da CAPAG vigente em 2019 à **Portaria MF n. 501/2017** e à **Portaria STN n. 882, de 18/12/2018** (DOU 20/12/2018).
- A metodologia atual está na Portaria Normativa MF n. 1.583/2023, alterada pela Portaria MF n. 1.764/2024, e na Portaria STN/MF n. 857/2026.
- Os documentos SEI de 2019 da STN encontrados seguem outro padrão de numeração, por exemplo "Nota Técnica SEI nº 32/2019/GESEM/CORFI/SURIN/STN". Existe portanto a série SURIN/STN, mas não achei a n. 21/2019 da CDCOF.

Não conseguir encontrar não prova que o documento não existe: pode ser uma nota interna do SEI, sem publicação aberta. Por isso a entrada ficou como `nao_confirmada`, e não `divergente`, e não entrou no JSON.

**Decisão do autor:** se a nota foi obtida por outra via (LAI, anexo de processo), basta registrar a origem. Se a intenção era citar a norma que define a metodologia, a referência precisa ser trocada pela Portaria. Pela restrição do prompt, essa troca não foi feita aqui.

## Observações sobre as fontes

- **Artigos em periódico:** Taylor & Francis, ScienceDirect, Wiley, OUP e RSNA recusam acesso automatizado (HTTP 403 ou "Client Challenge"). Para esses usei os metadados que o próprio editor deposita no registro do DOI (Crossref), com a URL `api.crossref.org/works/<DOI>` registrada no CSV. Esses dados são os do editor, não de um agregador. Mesmo assim, o critério não é literalmente "página do editor".
- **DeLong (id 10) e Hanley (id 12):** as páginas foram confirmadas também no PubMed (NLM). O Crossref traz só a página inicial de DeLong.
- **Ohlson (id 26):** o Crossref traz só a página inicial (109). O artigo seguinte do n. 1 começa na p. 132, o que é compatível com 109-131, mas não confirma diretamente a página final.
- **Livros de Minsky (ids 20, 21, 22):** os sites da Columbia UP, Yale UP e Routledge não renderizaram sem JavaScript.
  - Editora e ano foram confirmados no inventário oficial do Hyman P. Minsky Archive (Levy Economics Institute of Bard College, box4.pdf): "John Maynard Keynes (Columbia University Press, 1975)", "Can "It" Happen Again? (Armonk, NY: M.E. Sharpe, Inc., 1982)" e "Stabilizing an Unstable Economy (Yale University Press, 1986)".
  - A reedição de 2008 (McGraw-Hill, página do Levy) é posterior e não afeta a citação de 1986.
  - As cidades New York (Columbia) e New Haven (Yale) são as sedes das editoras, mas não aparecem textualmente na fonte consultada.
- **Jolliffe (id 14):** o DOI 10.1007/b98835 (Springer-Verlag, New York, 2002, ISBN 0-387-95442-2) corresponde à 2ª edição. Os metadados não trazem o número da edição explicitamente.
- **Grafia de nomes:** Zięba (ę) e Sjöström (ö) conferem com os metadados da Elsevier. "É." de Tymoigne confere com a capa do WP 605.
