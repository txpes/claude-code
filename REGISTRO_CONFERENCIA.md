# Conferência bibliográfica: registro completo do trabalho

*Artigo:* `Artigo_Fragilidade_Financeira (2).docx` · *Branch:* `claude/vibrant-hamilton-waykbq` · *Data:* 28/09/2026

---

## 1. Resumo

| | n |
|---|---|
| Entradas na lista | 33 |
| Pendentes na planilha mais recente | 22 |
| Pendentes que **conferem** | 18 |
| Pendentes **divergentes** | 3 (ids 17, 29, 33) |
| Pendentes **não confirmadas** | 1 (id 3) |
| Já conferidas que reconferi | 5 (ids 2, 6, 16, 25, 31) |
| Divergência entre as reconferidas | 1 (id 16) |
| Correções no JSON | 5 (4 na lista de referências + 1 na citação no texto) |
| Alterações no artigo | nenhuma |

---

## 2. Cronologia

1. **Leitura do repositório.** Encontrei o artigo (.docx e .pdf), a planilha `referencias_para_conferir.csv`, as tabelas, o código e a nota metodológica.
2. **Primeira tentativa, bloqueada.** A política de rede do ambiente recusou `doi.org`, `crossref.org`, BIS, JSTOR, ScienceDirect, Wiley, Levy e `gov.br`. Só a busca na web funcionava, e ela devolve resumos de agregadores, que o prompt proíbe como fonte única. Parei sem gerar os entregáveis.
3. **Checagem que não dependia de rede.** Extraí os parágrafos do `word/document.xml` e comparei com a coluna `entrada_abnt`. As 33 entradas são idênticas ao artigo, caractere a caractere.
4. **Planilha nova.** Você enviou uma versão com as ids 2, 6 e 31 já conferidas (22 pendentes). Anotei que algumas fontes registradas não seguiam a regra do prompt:
   - id 6: a fonte era a lista de referências de outro artigo;
   - ids 2, 31 e 16: sem URL;
   - id 25: página inicial do RePEc.
5. **Liberação da rede.** Você mudou o acesso de rede do ambiente. Crossref, BIS, Levy, JSTOR, Bard, gov.br e PubMed passaram a responder. Taylor & Francis, ScienceDirect, Wiley, OUP e RSNA continuaram recusando acesso automatizado (HTTP 403 ou "Client Challenge"). Os sites da Columbia UP e da Yale UP carregam o conteúdo só por JavaScript.
6. **Conferência** (detalhes nas seções 3 e 4).
7. **Geração e validação dos entregáveis**, depois commit e push.

---

## 3. Método

### 3.1 Fontes usadas, por tipo de referência

| Tipo | Fonte usada | Por quê |
|---|---|---|
| Artigo com DOI | Registro do DOI no Crossref (`api.crossref.org/works/<DOI>`) | São os metadados que o **próprio editor** deposita (Elsevier, Wiley, OUP, T&F, Springer, RSNA, JSTOR). A página do editor bloqueou acesso automatizado. |
| Artigo médico/estatístico | PubMed (NLM), além do Crossref | Página final de DeLong, que o Crossref não traz. |
| BIS Quarterly Review | PDF no `bis.org` | Página da instituição emissora. |
| Working papers do Levy | PDF no `levyinstitute.org` (capa do WP) | Página da instituição emissora. |
| Livros de Minsky | Inventário oficial do *Hyman P. Minsky Archive* (Levy Institute of Bard College, `bard.edu/.../box4.pdf`) e página do livro no Levy | Os sites das editoras não abriram. |
| Documento do Tesouro | Tesouro Transparente, gov.br/tesouronacional, cdn.tesouro.gov.br, DOU | Instituição emissora. |

A busca na web serviu **só para localizar** URLs. Nenhum veredito se apoia apenas nela.

### 3.2 Como estabeleci as páginas quando a fonte trazia só a página inicial

Os registros antigos do JSTOR no Crossref trazem apenas a página inicial. Para esses casos listei todos os artigos do mesmo volume ou fascículo no Crossref e olhei onde começa o artigo seguinte:

- **Zmijewski:** começa na p. 59, e o comentário de Dietrich começa na p. 83. O intervalo 59-82 fica confirmado.
- **Ohlson:** começa na p. 109, e o artigo seguinte do n. 1 começa na p. 132. Isso é compatível com 109-131, mas não confirma a página final.
- **DeLong:** começa na p. 837, e o seguinte começa na 847. O PubMed confirma 837-845.

### 3.3 Validação do JSON

Para cada correção conferi que:
- o campo `antigo` aparece **exatamente 1 vez** no texto do `document.xml`;
- o campo `novo` é diferente do `antigo`.

As 5 correções passaram nas duas checagens.

---

## 4. Resultado por entrada

| id | 1º autor | status original | veredito | fonte | observação |
|---|---|---|---|---|---|
| 1 | ALTMAN | pendente | **confere** | <https://api.crossref.org/works/10.1111/j.1540-6261.1968.tb00843.x> | Título, autor, JF v.23 n.4 p.589-609, 1968 conferem. |
| 2 | BOULESTEIX | conferida | **confere** | <https://api.crossref.org/works/10.1093/bib/bbl016> | Reconferida. OUP; online 2006, fascículo v.8 n.1 de 2007. |
| 3 | BRASIL | pendente | **nao_confirmada** | <https://www.tesourotransparente.gov.br/temas/estados-e-municipios/capacidade-de-pagamento-capag> | Documento não localizado em fonte oficial. Ver seção 5. |
| 4 | BANERJEE | pendente | **confere** | <https://www.bis.org/publ/qtrpdf/r_qt1809g.pdf> | PDF do BIS: 1ª página numerada 67, 12 páginas (67-78), "BIS Quarterly Review, September 2018". |
| 5 | BARBOZA | pendente | **confere** | <https://api.crossref.org/works/10.1016/j.eswa.2017.04.006> | Confere integralmente. |
| 6 | BARKER | conferida | **confere** | <https://api.crossref.org/works/10.1002/cem.785> | Reconferida via DOI Wiley (fonte anterior era lista de referências de terceiros). |
| 7 | BRITO | conferida | **—** | <https://www.redalyc.org/pdf/2571/257119525003.pdf> | Conferida anteriormente; não reconferida. |
| 8 | CAMPBELL | pendente | **confere** | <https://api.crossref.org/works/10.1111/j.1540-6261.2008.01416.x> | Versão publicada (JF 2008) tem o mesmo título do WP NBER 2006. |
| 9 | DAVIS | conferida | **—** | <https://econpapers.repec.org/RePEc:oup:cambje:v:43:y:2019:i:3:p:541-583> | Conferida anteriormente; não reconferida. |
| 10 | DELONG | pendente | **confere** | <https://pubmed.ncbi.nlm.nih.gov/3203132/> ; <https://api.crossref.org/works/10.2307/2531595> | PubMed: p. 837-45; Crossref só traz página inicial. |
| 11 | DU JARDIN | pendente | **confere** | <https://api.crossref.org/works/10.1016/j.ejor.2016.03.008> | Confere. |
| 12 | HANLEY | pendente | **confere** | <https://api.crossref.org/works/10.1148/radiology.143.1.7063747> ; <https://pubmed.ncbi.nlm.nih.gov/7063747/> | Crossref (RSNA) e PubMed: p. 29-36, abr. 1982. |
| 13 | GUIMARÃES | conferida | **—** | <https://revistas.ufrj.br/index.php/rec/article/view/19530> | Conferida anteriormente; não reconferida. |
| 14 | JOLLIFFE | pendente | **confere** | <https://api.crossref.org/works/10.1007/b98835> | DOI 10.1007/b98835, Springer-Verlag New York 2002, ISBN 0387954422 (2ª ed.); nº da edição não explícito nos metadados. |
| 15 | MAI | pendente | **confere** | <https://api.crossref.org/works/10.1016/j.ejor.2018.10.024> | Ordem dos 4 autores confere. |
| 16 | MANTOAN | conferida | **divergente** | <https://api.crossref.org/works/10.1007/s43253-021-00051-6> | Reconferida. Falta n. 3. |
| 17 | McGOWAN | pendente | **divergente** | <https://api.crossref.org/works/10.1093/epolic/eiy012> | Sobrenome da 1ª autora é Adalet McGowan. |
| 18 | MERTON | pendente | **confere** | <https://api.crossref.org/works/10.1111/j.1540-6261.1974.tb03058.x> | Crossref Wiley: p. 449-470. |
| 19 | MINUSSI | conferida | **—** | <https://www.redalyc.org/pdf/840/84060307.pdf> | Conferida anteriormente; não reconferida. |
| 20 | MINSKY | pendente | **confere** | <https://www.bard.edu/library/archive/minsky/pdfs/box4.pdf> ; <https://api.crossref.org/works/10.1007/978-1-349-02679-1> | Inventário do arquivo Minsky (Levy/Bard): Columbia UP, 1975. Cidade não textual na fonte. |
| 21 | MINSKY | pendente | **confere** | <https://www.bard.edu/library/archive/minsky/pdfs/box4.pdf> | Mesmo inventário: Armonk, NY: M.E. Sharpe, 1982. |
| 22 | MINSKY | pendente | **confere** | <https://www.bard.edu/library/archive/minsky/pdfs/box4.pdf> ; <https://www.levyinstitute.org/publications/stabilizing-an-unstable-economy/> | Mesmo inventário: Yale UP, 1986. Reedição 2008 (McGraw-Hill) não afeta. Cidade não textual. |
| 23 | MINSKY | pendente | **confere** | <https://www.levyinstitute.org/pubs/wp74.pdf> | Capa do WP 74: "The Financial Instability Hypothesis", maio 1992. |
| 24 | MULLIGAN | pendente | **confere** | <https://api.crossref.org/works/10.1016/j.qref.2013.05.010> | Confere. |
| 25 | NISHI | conferida | **confere** | <https://api.crossref.org/works/10.1093/cje/bey031> | Reconferida. OUP; online 2018, fascículo v.43 n.3 de 2019. |
| 26 | OHLSON | pendente | **confere** | <https://api.crossref.org/works/10.2307/2490395> | Página final 131 inferida (artigo seguinte do n.1 começa na 132). |
| 27 | SCALZER | conferida | **—** | <https://www.redalyc.org/pdf/762/76249690002.pdf> | Conferida anteriormente; não reconferida. |
| 28 | TORRES FILHO | conferida | **—** | <https://www.tandfonline.com/doi/full/10.1080/01603477.2018.1503057> | Conferida anteriormente; não reconferida. |
| 29 | TYMOIGNE | pendente | **divergente** | <https://www.levyinstitute.org/pubs/wp_605.pdf> | Capa do WP 605: "Detecting Ponzi Finance". Ponzi é nome próprio. |
| 30 | TYMOIGNE | pendente | **confere** | <https://api.crossref.org/works/10.2753/pke0160-3477360407> | Versão publicada usa "Minskian" (o SSRN 2012 usa "Minskyan"); a entrada já usa a publicada. |
| 31 | WOLD | conferida | **confere** | <https://api.crossref.org/works/10.1016/s0169-7439(01)00155-1> | Reconferida. Sjöström com ö confere. |
| 32 | ZIĘBA | pendente | **confere** | <https://api.crossref.org/works/10.1016/j.eswa.2016.04.001> | Zięba com ę confere nos metadados Elsevier. |
| 33 | ZMIJEWSKI | pendente | **divergente** | <https://api.crossref.org/works/10.2307/2490859> ; <https://api.crossref.org/journals/0021-8456/works?filter=from-pub-date:1984,until-pub-date:1984> | Sem nº de fascículo no Crossref; intercalado com "Discussion of..." do suplemento; próximo texto começa p. 83. |
---

## 5. Divergências em detalhe

### id 17 — McGowan, Andrews e Millot (2018) · campo: **autoria**

- **Evidência:** nos metadados da OUP (DOI 10.1093/epolic/eiy012), a primeira autora é *Müge Adalet McGowan*, com sobrenome composto "Adalet McGowan". O próprio texto do BIS (id 4) cita "Adalet McGowan et al (2017)".
- **Antes:** `McGOWAN, M. A.; ANDREWS, D.; MILLOT, V. The walking dead? ...`
- **Depois:** `ADALET McGOWAN, M.; ANDREWS, D.; MILLOT, V. The walking dead? ...`
- **Citação no texto:** "McGowan, Andrews e Millot (2018)" passa a ser "Adalet McGowan, Andrews e Millot (2018)". É a única ocorrência no artigo e está no JSON.
- **Efeito colateral:** a entrada passa para a letra A na ordem alfabética, antes de ALTMAN. O JSON não reordena a lista.

### id 29 — Tymoigne (2010) · campo: **título**

- **Evidência:** a capa do WP n. 605 no site do Levy traz "Detecting Ponzi Finance: An Evolutionary Approach to the Measure of Financial Fragility", de Éric Tymoigne, junho de 2010.
- **Antes:** `Detecting ponzi finance: ...`
- **Depois:** `Detecting Ponzi finance: ...`
- **Motivo:** pela ABNT, só a primeira palavra e os nomes próprios levam maiúscula, e *Ponzi* é nome próprio.

### id 33 — Zmijewski (1984) · campo: **número (suplemento)**

- **Evidência:** no Crossref o artigo não tem número de fascículo. Os itens de 1984 sem número são justamente o conjunto artigo + "Discussion of…" do suplemento *Studies on Current Econometric Issues in Accounting Research*, e os itens dos números regulares têm "1" ou "2".
- **Antes:** `v. 22, p. 59-82, 1984.`
- **Depois:** `v. 22, supl., p. 59-82, 1984.`
- **Ressalva:** a página do JSTOR, que traz o nome do suplemento por extenso, não abriu. A indicação vem dos metadados do DOI.

### id 16 — Mantoan, Centeno e Feijó (2021) · campo: **número** *(entrada que já estava como conferida)*

- **Evidência:** nos metadados da Springer (DOI 10.1007/s43253-021-00051-6), o artigo está no v. 2, n. 3 (dez. 2021), p. 529-550. A anotação da própria planilha já dizia "v.2(3)".
- **Antes:** `v. 2, p. 529-550, 2021.`
- **Depois:** `v. 2, n. 3, p. 529-550, 2021.`
- **Nota:** o Crossref grafa "Feijo" sem acento. Mantive "FEIJÓ", que é a grafia correta do nome da autora. O Crossref também lista o grupo FINDE/UFF como coautor institucional; não incluí, seguindo o padrão das demais entradas.

---

## 6. Não confirmada: id 3 — BRASIL (2019), Nota Técnica SEI n. 21/2019/CDCOF/SURIN/STN

**Onde procurei:**
- Tesouro Transparente: página da CAPAG e PDFs de metadados;
- gov.br/tesouronacional;
- cdn.tesouro.gov.br;
- DOU;
- busca aberta pelo número exato.

**O que encontrei:**
- Não há nenhuma ocorrência de "Nota Técnica SEI nº 21/2019" ligada à STN.
- As páginas oficiais atribuem a metodologia da CAPAG:
  - **até 2023:** Portaria MF n. 501/2017 e **Portaria STN n. 882, de 18/12/2018** (DOU 20/12/2018);
  - **depois:** Portaria Normativa MF n. 1.583/2023 (alterada pela Portaria MF n. 1.764/2024) e Portaria STN/MF n. 857/2026.
- Existem notas SEI de 2019 da SURIN/STN, mas de outras coordenações, por exemplo "Nota Técnica SEI nº 32/2019/GESEM/CORFI/SURIN/STN".

**Veredito:** `nao_confirmada`. Esse valor está fora do par `confere`/`divergente` pedido no prompt. Não marquei `divergente` porque não consigo provar que o documento não existe: pode ser uma nota interna do SEI, nunca publicada. Por isso a id 3 também não entrou no JSON.

**Decisão sua:**
- (a) se a nota foi obtida por outra via, registre a origem;
- (b) se a intenção era citar a norma da metodologia, troque pela Portaria STN n. 882/2018 (ou a vigente no período dos dados). Não fiz essa troca porque o prompt proíbe substituir a obra.

---

## 7. Limitações

1. **Página do editor.** Nenhum artigo de periódico foi conferido na página HTML do editor, porque todas bloquearam acesso automatizado. A base foi o registro do DOI (dados do editor via Crossref), complementado pelo PubMed. Se o critério exigir a página em si, os 17 artigos com DOI precisariam de uma olhada manual rápida.
2. **Livros de Minsky.** Editora e ano vêm do inventário do arquivo Minsky no Levy/Bard, não do catálogo das editoras. As cidades (New York, New Haven) não aparecem nessa fonte. Armonk aparece.
3. **Jolliffe.** O DOI e o ISBN correspondem à 2ª edição (2002), mas o número da edição não está explícito nos metadados.
4. **Ohlson.** A página final 131 foi inferida, não lida diretamente.
5. **Entradas conferidas antes (7, 9, 13, 19, 27, 28):** não reconferi. Ficam com a fonte e o veredito que você registrou.

---

## 8. Arquivos entregues

| Arquivo | Conteúdo |
|---|---|
| `referencias_conferidas.csv` | As 33 linhas, com `veredito`, `correcao_proposta` e `fonte_confirmada` preenchidos para as 22 pendentes e as 5 reconferidas |
| `correcoes_referencias.json` | 5 objetos `{id, antigo, novo, campo, fonte}`, com `antigo` validado contra o artigo |
| `relatorio_referencias.md` | Relatório resumido pedido no prompt |
| `REGISTRO_CONFERENCIA.md` | Este documento |

## 9. O que falta você decidir

- [ ] id 3: manter a Nota Técnica (e registrar a origem) ou trocar pela Portaria
- [ ] id 17: mover ADALET McGOWAN para o início da lista (ordem alfabética)
- [ ] Opcional: abrir manualmente, no navegador, as páginas do editor dos artigos com DOI e as de Columbia/Yale para fechar as limitações 1 e 2
