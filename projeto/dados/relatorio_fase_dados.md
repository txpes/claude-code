# Relatório da fase de dados

Gerado em 22/09/2026 20:14 por `scripts/55_relatorio_fase_dados.R`.

## 0. Cobertura dos dados nesta execução

- DFP: exercícios 2010 a 2025.
- IPE: arquivos de 2010 a 2026.
- ITR: 15 de 15 anos disponíveis.
- Cadastro: cad_cia_aberta_2025.csv (atualizado).

## 1. Firmas por ano

Painel completo: 7491 firma-anos, 742 firmas. Amostra de risco (transição, variante conservadora): 5751 firma-anos, 196 entradas (3.41%).

| ano | firmas_inputs | firmas_painel | obs_painel | em_risco | entradas | taxa_entrada_pct |
|---|---|---|---|---|---|---|
| 2010 | 381 | 364 | 364 | 0 | 0 |  |
| 2011 | 413 | 394 | 394 | 340 | 15 | 4.41 |
| 2012 | 433 | 410 | 410 | 353 | 14 | 3.97 |
| 2013 | 442 | 417 | 417 | 349 | 18 | 5.16 |
| 2014 | 436 | 414 | 414 | 342 | 11 | 3.22 |
| 2015 | 436 | 418 | 418 | 346 | 21 | 6.07 |
| 2016 | 431 | 414 | 414 | 327 | 19 | 5.81 |
| 2017 | 434 | 417 | 417 | 326 | 18 | 5.52 |
| 2018 | 440 | 428 | 428 | 321 | 13 | 4.05 |
| 2019 | 482 | 471 | 471 | 333 | 5 | 1.50 |
| 2020 | 538 | 524 | 524 | 387 | 12 | 3.10 |
| 2021 | 579 | 559 | 559 | 434 | 7 | 1.61 |
| 2022 | 591 | 578 | 578 | 476 | 10 | 2.10 |
| 2023 | 604 | 586 | 586 | 480 | 10 | 2.08 |
| 2024 | 581 | 568 | 568 | 484 | 15 | 3.10 |
| 2025 | 541 | 529 | 529 | 453 | 8 | 1.77 |

## 2. Entradas por ano e por critério

Uma entrada pode acionar mais de um critério; as colunas de critério somam mais que o total.

| ano | entradas | (b) PL<0 | (c) EBITDA<0 2 anos | (d) RJ | só (d) |
|---|---|---|---|---|---|
| 2011 | 15 | 5 | 12 | 1 | 0 |
| 2012 | 14 | 4 | 9 | 3 | 2 |
| 2013 | 18 | 5 | 10 | 4 | 3 |
| 2014 | 11 | 3 | 8 | 2 | 1 |
| 2015 | 21 | 10 | 13 | 0 | 0 |
| 2016 | 19 | 8 | 15 | 1 | 1 |
| 2017 | 18 | 7 | 11 | 1 | 1 |
| 2018 | 13 | 7 | 5 | 2 | 1 |
| 2019 | 5 | 3 | 2 | 1 | 0 |
| 2020 | 12 | 8 | 4 | 1 | 1 |
| 2021 | 7 | 2 | 5 | 0 | 0 |
| 2022 | 10 | 3 | 7 | 0 | 0 |
| 2023 | 10 | 4 | 7 | 1 | 1 |
| 2024 | 15 | 9 | 6 | 6 | 1 |
| 2025 | 8 | 5 | 4 | 0 | 0 |
| Total | 196 | 83 | 118 | 23 | 12 |

Comparação no período 2010-2023: especificação antiga = 191 entradas em 4682 firma-anos de risco (4.08%); nova = 173 em 4814 (3.59%).

## 3. Detecção de recuperação judicial

A nova regra identifica 96 firmas no IPE (82 na amostra do painel). Por fonte do primeiro documento e tipo:

| fonte | tipo | firmas | na_amostra |
|---|---|---|---|
| principal | extrajudicial | 10 | 10 |
| principal | judicial | 40 | 34 |
| secundaria | extrajudicial | 5 | 4 |
| secundaria | judicial | 41 | 34 |

Natureza do primeiro documento (quando não é o pedido, a data pode ser posterior ao ajuizamento):

| natureza_1o_doc | firmas | na_amostra |
|---|---|---|
| pedido | 64 | 58 |
| andamento | 29 | 21 |
| encerramento/conversao | 3 | 3 |

Firmas com as duas fontes: 81; só principal: 9; só secundária: 6.

### 3.1 Comparação com a regra antiga (firmas da amostra, 2010-2023)

| situacao | N |
|---|---|
| ambas, mesmo ano | 57 |
| só regra antiga (descartada) | 26 |

Contra a classificação manual da Fase 1C (46 firmas):

| classificacao_manual_1C | detectada_pela_nova | firmas |
|---|---|---|
| ambiguo | TRUE | 2 |
| ambiguo | FALSE | 1 |
| proprio | TRUE | 30 |
| terceiro | FALSE | 13 |

Firmas da amostra detectadas pela regra antiga e não classificadas na Fase 1C: 37 (25 mantidas pela regra nova, 12 descartadas).

Das 12 firmas descartadas que não estavam na classificação da Fase 1C, 12 foram lidas uma a uma nesta fase, e todas são menção a RJ de terceiro. Com isso, todas as firmas descartadas pela nova regra são falsos positivos da regra antiga.

| CD_CVM | classificacao | motivo |
|---|---|---|
| 15253 | terceiro | RJ das sociedades do Grupo Rede (controladas) |
| 19208 | terceiro | ""receitas recuperadas"" + ação judicial; sem RJ |
| 20087 | terceiro | RJ da Republic Airways (cliente) |
| 20320 | terceiro | RJ da Renova (investida) |
| 23230 | terceiro | RJ da Unialco (UPI adquirida) |
| 23922 | terceiro | RJ da Odebrecht (controladora) |
| 24112 | terceiro | menção a RJ de terceiro em ata |
| 2453 | terceiro | RJ da Renova (investida) |
| 2461 | terceiro | RJ da Empresa Carlos Renaux (devedora) |
| 25097 | terceiro | RJ da Light S.A. (contraparte) |
| 25550 | terceiro | RJ da Estre (leilão de ativos) |
| 80098 | terceiro | RJ da Parmalat Brasil (controlada) |

### 3.2a Exclusões manuais

2 firmas passaram pelos filtros automáticos, mas foram excluídas depois da leitura dos documentos (`outputs/tables/50_rj_exclusoes_manuais.csv`). A Light Energia apareceu como falso positivo na primeira amostra de 40 detecções (1 em 40, ou 2,5%). A Light SESA foi excluída pelo mesmo motivo. As duas são subsidiárias cujos documentos tratam da RJ da controladora. A amostra da seção 3.3 foi sorteada de novo depois da exclusão; por isso, a taxa residual mais conservadora continua sendo a da primeira amostra.

| CD_CVM | motivo |
|---|---|
| 8036 | Light SESA: subsidiária da Light S.A.; documentos tratam da RJ da controladora (a concessionária não é devedora no processo) |
| 23000 | Light Energia: subsidiária da Light S.A.; pede remoção do processo e depois comenta o plano da controladora |

### 3.2 Divergências entre fontes (para revisão manual)

28 firmas (17 na amostra). Arquivo completo: `outputs/tables/50_rj_divergencias.csv`.

| CD_CVM | DENOM | DT_RJ | ano_sufixo_dfp | dt_cadastro_rj | na_amostra | motivo |
|---|---|---|---|---|---|---|
| 4081 | CIA TECIDOS SANTANENSE - EM RECUPERAÇÃO JUDICIAL | 2024-05-08 | 2020 |  | TRUE | ano do sufixo na DFP difere 2+ anos |
| 5150 | DHB IND E COMERCIO SA | 2015-03-17 |  |  | TRUE | só fonte secundária |
| 5762 | ETERNIT S.A. | 2018-03-19 | 2010 |  | TRUE | ano do sufixo na DFP difere 2+ anos |
| 12190 | BOMBRIL S.A. - EM RECUPERAÇÃO JUDICIAL | 2025-02-10 | 2021 | 2025-03-12 | TRUE | ano do sufixo na DFP difere 2+ anos |
| 12572 | RECRUSUL SA | 2016-07-19 |  |  | TRUE | só fonte principal |
| 12858 | DIGITEL S.A. INDUSTRIA ELETRONICA - EM RECUPERAÇÃO JUDICIAL | 2018-08-14 |  | 2018-05-29 | TRUE | ano difere entre principal e secundária |
| 15083 | KOSMOS COMÉRCIO DE VESTUÁRIO S/A - EM RECUPERAÇÃO JUDICIAL | 2015-07-14 | 2010 |  | TRUE | só fonte principal |
| 17868 | INEPAR EQUIPAMENTOS E MONTAGENS S/A - EM RECUPERACAO JUDICIA | 2015-05-14 |  | 2014-09-15 | TRUE | só fonte secundária |
| 21636 | RENOVA ENERGIA S.A. | 2019-10-16 | 2010 |  | TRUE | ano do sufixo na DFP difere 2+ anos |
| 22373 | ELETROSOM S/A - EM RECUPERAÇÃO JUDICIAL | 2015-12-10 |  | 2015-09-08 | TRUE | só fonte principal |
| 22721 | CONC RODOVIAS DO TIETÊ S.A.- EM RECUPERAÇÃO JUDICIAL | 2019-11-11 | 2010 | 2019-12-19 | TRUE | ano do sufixo na DFP difere 2+ anos |
| 23230 | RAÍZEN ENERGIA S.A. | 2026-03-11 |  |  | TRUE | só fonte secundária |
| 24660 | BBM LOGÍSTICA S.A. | 2024-11-04 |  |  | TRUE | só fonte principal |
| 25224 | 2W ECOBANK S.A. - EM RECUPERAÇÃO JUDICIAL | 2024-10-11 | 2021 | 2025-04-23 | TRUE | ano difere entre principal e secundária; ano do sufixo na DFP difere 2+ anos |
| 25461 | GRUPO TOKY S.A. - EM RECUPERAÇÃO JUDICIAL | 2026-05-12 | 2024 | 2026-06-15 | TRUE | ano do sufixo na DFP difere 2+ anos |
| 25658 | AGROGALAXY PARTICIPAÇÕES S.A. - EM RECUPERAÇÃO JUDICIAL | 2024-09-18 | 2020 | 2024-09-18 | TRUE | ano do sufixo na DFP difere 2+ anos |
| 25879 | KORA SAÚDE PARTICIPAÇÕES S.A. | 2026-05-05 |  |  | TRUE | só fonte principal |
| 1686 | PRÓ METALURGIA SA - EM LIQUIDAÇÃO EXTRAJUDICIAL | 2017-04-28 |  |  | FALSE | só fonte principal |
| 2488 | CERAMICA CHIARELLI SA - EM RECUPERAÇÃO JUDICIAL | 2010-03-24 |  | 2009-01-05 | FALSE | só fonte secundária |
| 4111 | CACHOEIRA VELONORTE |  |  | 2010-01-01 | FALSE | cadastro em RJ sem documento IPE |
| 10987 | BOTUCATU TÊXTIL S. A. | 2010-08-10 |  | 2008-01-22 | FALSE | só fonte principal |
| 11681 | S.A. (VIAÇÃO AÉREA RIO-GRANDENSE) - FALIDA | 2010-07-07 |  |  | FALSE | só fonte principal |
| 15334 | BOMBRIL HOLDING SA |  |  | 2005-11-16 | FALSE | cadastro em RJ sem documento IPE |
| 15423 | FASA S.A. - EM RECUPERAÇÃO JUDICIAL | 2014-08-30 | 2022 | 2026-04-17 | FALSE | ano do sufixo na DFP difere 2+ anos |
| 21628 | HABITASEC SECURITIZADORA SA | 2016-06-28 |  |  | FALSE | só fonte secundária |
| 27006 | RIO ALTO STL HOLDING I S.A. | 2025-07-15 |  |  | FALSE | só fonte secundária |
| 501646 | SPERAFICO DA AMAZONIA S/A | 2024-12-05 |  |  | FALSE | só fonte principal |
| 518280 | SIDERÚRGICA NORTE BRASIL S/A | 2017-07-05 |  |  | FALSE | ano difere entre principal e secundária |

Sobre a verificação pela denominação na DFP: a denominação dos arquivos de DFP também é preenchida retroativamente. Há firmas com o sufixo "em recuperação judicial" em exercícios muito anteriores ao pedido (ver as linhas com "ano do sufixo na DFP difere 2+ anos"). O sufixo serve para indicar que o evento existe, mas não para datá-lo.

### 3.3 Amostra aleatória de 40 detecções

A classificação foi feita pela leitura do assunto do documento que define a data (como na Fase 1C, sem ler o inteiro teor). Resultado: 40 classificadas, 0 falsos positivos. A taxa residual estimada é de 0.0%; o limite superior de 95% é de 7.5% (regra de três quando não há falsos positivos, Clopper-Pearson nos demais casos).


| CD_CVM | DENOM_IPE | DT_RJ | fonte | assunto | link | classificacao | observacao |
|---|---|---|---|---|---|---|---|
| 1520 | BARDELLA S.A. INDS MECANICAS - EM RECUPERAÇÃO JUDICIAL | 2019-07-26 | secundaria | /  / Pedido de Recuperação Judicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=702219&numSequencia=228144&numVersao=1 | própria | própria |
| 2038 | BUETTNER SA IND E COMÉRCIO | 2011-05-05 | secundaria | /  / Ajuizaento de Ação de Recuperação Judicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=289452&numSequencia=0&numVersao=0 | própria | própria |
| 4685 | CONPEL CIA. NORDESTINA DE PAPEL - EM RECUPERAÇÃO JUDICIAL | 2017-08-21 | principal | Outros documentos /  / Fato Relevante Recuperação Judicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=576600&numSequencia=119396&numVersao=1 | própria | própria; primeiro documento é de andamento |
| 5150 | DHB IND E COMERCIO SA | 2015-03-17 | secundaria | /  / Recuperação Judicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=459799&numSequencia=2546&numVersao=1 | própria | própria; primeiro documento é de andamento |
| 6017 | FIBAM CIA INDUSTRIAL - EM RECUPERAÇÃO JUDICIAL | 2014-11-03 | secundaria | /  / Recuperação Judicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=444077&numSequencia=0&numVersao=0 | própria | própria; primeiro documento é de andamento |
| 6505 | GRUPO CASAS BAHIA S.A. | 2024-04-28 | secundaria | Conselho de Administração / Ata / Deliberar acerca do pedido de homologação de plano de Recuperação Extrajudic | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1227811&numSequencia=752537&numVersao=1 | própria | própria; recuperação extrajudicial (abr/2024) |
| 7544 | TÊXTIL RENAUXVIEW S/A | 2010-05-05 | secundaria | /  / Pedido de homologação de Plano de Recuperação Extrajudicial (PRE) | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=244570&numSequencia=0&numVersao=0 | própria | própria; recuperação extrajudicial |
| 7811 | JOAO FORTES ENGENHARIA SA - EM RECUPERAÇÃO JUDICIAL | 2020-04-27 | principal | Outros documentos /  / Quadro Geral de Credores | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=756765&numSequencia=281519&numVersao=1 | própria | própria; primeiro documento é de andamento (quadro de credores) |
| 9393 | PARANAPANEMA S.A. - EM RECUPERAÇÃO JUDICIAL | 2022-11-30 | principal | Outros documentos /  / Demonstrações Financeiras referentes ao pedido de recuperação judicial da Companhia e d | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1037088&numSequencia=561818&numVersao=1 | própria | própria |
| 9989 | REFINARIA PET MANGUINHOS SA | 2011-07-13 | principal | Outros documentos /  / Petição desistência do pedido de recuperação extrajudicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=298121&numSequencia=0&numVersao=0 | própria | própria; companhia já em RJ desde 2005 — documento de 2011 é desistência de pedido de REJ, data não marca início |
| 11991 | WETZEL S.A. EM RECUPERAÇÃO JUDICIAL | 2016-02-03 | principal | Petição Inicial /  / Protocolo e Petição Inicial Ação de Recuperação Judicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=499698&numSequencia=42446&numVersao=1 | própria | própria |
| 12858 | DIGITEL S.A. INDUSTRIA ELETRONICA - EM RECUPERAÇÃO JUDICIAL | 2018-08-14 | secundaria | /  / Petição para a Concessão de Recuperação Judicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=637789&numSequencia=171192&numVersao=1 | própria | própria |
| 13030 | CONST SULTEPA SA - EM RECUPERAÇÃO JUDICIAL | 2015-07-03 | secundaria | AGE / Edital de Convocação / Ratificação Pedido de Recuperação Judicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=476453&numSequencia=19200&numVersao=1 | própria | própria |
| 14826 | COMPANHIA BRASILEIRA DE DISTRIBUIÇÃO | 2026-03-10 | principal | Outros documentos /  / Demonstrações Financeiras (Petição Inicial) - Recuperação Extrajudicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1488512&numSequencia=1013218&numVersao=1 | própria | própria; recuperação extrajudicial (2026) |
| 15083 | KOSMOS COMÉRCIO DE VESTUÁRIO S/A - EM RECUPERAÇÃO JUDICIAL | 2015-07-14 | principal | Contas demonstrativas mensais /  / | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=477776&numSequencia=20523&numVersao=1 | própria | própria; primeiro documento é de andamento (contas mensais) |
| 15377 | HOPI HARI SA | 2016-08-24 | secundaria | AGE / Ata / Aprovação do pedido de recuperação judicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=528963&numSequencia=71711&numVersao=1 | própria | própria |
| 17868 | INEPAR EQUIPAMENTOS E MONTAGENS S.A. - EM RECUPERAÇÃO JUDICIAL | 2015-05-14 | secundaria | /  / Aprovação do Plano de Recuperação Judicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=471494&numSequencia=14241&numVersao=1 | própria | própria; recuperação do grupo Inepar (pedido em ago/2014); primeiro documento da própria é de 2015 |
| 17914 | MMX MINERAÇÃO E METÁLICOS S.A. - EM RECUPERAÇÃO JUDICIAL | 2014-10-15 | secundaria | /  / Pedido de solicitação de Recuperação Judicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=442673&numSequencia=0&numVersao=0 | própria | própria |
| 18309 | EQUATORIAL PARÁ DISTRIBUIDORA DE ENERGIA S.A. | 2012-02-28 | principal | Petição Inicial /  / Pedido de Recuperação Judicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=321806&numSequencia=0&numVersao=0 | própria | própria (Celpa, hoje Equatorial Pará); pedido em fev/2012 |
| 18490 | CLARION S/A AGROINDUSTRIAL | 2013-06-07 | principal | Outros documentos /  / Causas do Pedido de Recuperação | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=383833&numSequencia=0&numVersao=0 | própria | própria |
| 19330 | TPI - TRIUNFO PARTICIPACOES E INVESTIMENTOS S.A. | 2017-07-22 | principal | Plano de Recuperação /  / Planos de recuperação extrajudicial da Concer TPI e suas subsidiárias | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=572361&numSequencia=115161&numVersao=1 | própria | própria; recuperação extrajudicial da Triunfo e subsidiárias |
| 19879 | LIGHT S.A. - EM RECUPERAÇÃO JUDICIAL | 2023-05-12 | principal | Outros documentos /  / Demonstrações contábeis levantadas para pedido de RJ | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1101511&numSequencia=626240&numVersao=1 | própria | própria |
| 20478 | PDG REALTY S.A. EMPREENDIMENTOS E PARTICIPACOES | 2017-02-22 | secundaria | /  / Informações sobre o Ajuizamento do Pedido de Recuperação Judicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=549195&numSequencia=91943&numVersao=1 | própria | própria |
| 20966 | SPRINGS GLOBAL PARTICIPAÇÕES S/A - EM RECUPERAÇÃO JUDICIAL | 2024-05-08 | principal | Petição Inicial /  / Petição inicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1234723&numSequencia=759449&numVersao=1 | própria | própria |
| 21237 | ENEVA S.A. | 2014-12-09 | principal | Petição Inicial /  / Petição Inicial do Pedido de Recuperação Judicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=449096&numSequencia=0&numVersao=0 | própria | própria |
| 21342 | OSX BRASIL S.A. | 2013-11-08 | secundaria |  /  / OSX anuncia mudanças na Diretoria, contratação da consultoria ANGRA PARTNERS e aprovação de pedido de re | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=400302&numSequencia=0&numVersao=0 | própria | própria |
| 21440 | RESTOQUE COMÉRCIO E CONFECÇÕES DE ROUPAS SA | 2020-06-05 | principal | Plano de Recuperação /  / Acordo com Credores Financeiros | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=766709&numSequencia=291461&numVersao=1 | própria | própria; primeiro documento é de andamento |
| 21636 | RENOVA ENERGIA S.A. -  EM RECUPERAÇÃO JUDICIAL | 2019-10-16 | principal | Outros documentos /  / Solicitação de documentos do processo de recuperação judicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=716327&numSequencia=241169&numVersao=1 | própria | própria; primeiro documento é de andamento |
| 22373 | ELETROSOM S/A - EM RECUPERAÇÃO JUDICIAL | 2015-12-10 | principal | Plano de Recuperação /  / Comunicado ao mercado | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=494911&numSequencia=37659&numVersao=1 | própria | própria; primeiro documento é de andamento |
| 22500 | MASSA FALIDA DA BRASIL PHARMA SA | 2018-01-10 | principal | Outros documentos /  / Anexo 5 - Demostrações Financeiras (Parte1) | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=593059&numSequencia=135855&numVersao=1 | própria | própria; primeiro documento é de andamento |
| 22721 | CONC RODOVIAS DO TIETÊ S.A.- EM RECUPERAÇÃO JUDICIAL | 2019-11-11 | principal | Outros documentos /  / Procuração | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=720816&numSequencia=245638&numVersao=1 | própria | própria; primeiro documento é de andamento (procuração) |
| 23230 | RAÍZEN ENERGIA S.A. | 2026-03-11 | secundaria | Conselho de Administração / Ata / Celebração de plano de recuperação extrajudicial e ajuizamento do processo d | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1488796&numSequencia=1013502&numVersao=1 | própria | própria; recuperação extrajudicial do grupo Raízen (2026) |
| 24961 | AMBIPAR PARTICIPAÇÕES E EMPREENDIMENTOS S.A. | 2025-10-21 | secundaria | /  / Pedido de Recuperação Judicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1434222&numSequencia=958934&numVersao=1 | própria | própria |
| 25160 | SEQUOIA LOGÍSTICA E TRANSPORTES S.A. | 2024-10-11 | principal | Pedido de homologação de Plano de Recuperação Extrajudicial /  / Pedido de Homologação de Plano de Recuperação | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1291156&numSequencia=815882&numVersao=1 | própria | própria; recuperação extrajudicial |
| 25720 | RIO ALTO ENERGIAS RENOVÁVEIS S.A. - EM RECUPERAÇÃO JUDICIAL | 2025-07-15 | secundaria | /  / Recuperação Extrajudicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1401039&numSequencia=925751&numVersao=1 | própria | própria; recuperação extrajudicial |
| 25879 | KORA SAÚDE PARTICIPAÇÕES S.A. | 2026-05-05 | principal | Outros documentos /  / Deferimento do Processamento da Recuperação Extrajudicial da Kora Saúde e controladas | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1516340&numSequencia=1041046&numVersao=1 | própria | própria; recuperação extrajudicial (2026) |
| 25992 | INTERCEMENT BRASIL S.A. - EM RECUPERAÇÃO JUDICIAL | 2024-09-16 | principal | Pedido de homologação de Plano de Recuperação Extrajudicial /  / Plano de Homologação de Plano de Recuperação  | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1282656&numSequencia=807382&numVersao=1 | própria | própria; recuperação extrajudicial, depois judicial |
| 26271 | ENVIRONMENTAL ESG PARTICIPAÇÕES S.A. | 2025-10-21 | secundaria | /  / Pedido de Recuperação Judicial | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1434223&numSequencia=958935&numVersao=1 | própria | própria; pedido conjunto com o grupo Ambipar |
| 26301 | UNIGEL PARTICIPAÇÕES S.A. | 2024-02-21 | principal | Pedido de homologação de Plano de Recuperação Extrajudicial /  / Pedido de Homologação Recuperação Extrajudici | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1196888&numSequencia=721614&numVersao=1 | própria | própria; recuperação extrajudicial |
| 26476 | AMMO VAREJO S.A. | 2024-05-09 | secundaria | /  / Pedido de recuperação judicial e tutelas concedidas | https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1235431&numSequencia=760157&numVersao=1 | própria | própria |

## 4. Verificação de 2010 a 2023

A comparação A roda a extensão com a regra antiga de RJ e mostra se o novo código e os anos acrescentados alteraram o histórico. O resultado esperado é zero divergência. A comparação B usa a regra nova, que é a dos entregáveis, e só pode divergir em colunas derivadas de `crit_d`.

| arquivo | comparacao | linhas_antigo | linhas_novo_ate_2023 | linhas_so_antigo | linhas_so_novo | celulas_divergentes | fora_de_crit_d | nao_explicada |
|---|---|---|---|---|---|---|---|---|
| painel_inputs | A: extensão, regra antiga | 6565 | 6640 | 0 | 75 | 0 | FALSE | FALSE |
| painel_inputs | B: extensão, regra nova | 6565 | 6640 | 0 | 75 | 0 | FALSE | FALSE |
| painel_indicadores | A: extensão, regra antiga | 6565 | 6640 | 0 | 75 | 0 | FALSE | FALSE |
| painel_indicadores | B: extensão, regra nova | 6565 | 6640 | 0 | 75 | 0 | FALSE | FALSE |
| eventos_vulnerabilidade | A: extensão, regra antiga | 6565 | 6640 | 0 | 75 | 119 | FALSE | FALSE |
| eventos_vulnerabilidade | B: extensão, regra nova | 6565 | 6640 | 0 | 75 | 729 | FALSE | FALSE |
| painel_completo | A: extensão, regra antiga | 6315 | 6394 | 0 | 79 | 295 | TRUE | FALSE |
| painel_completo | B: extensão, regra nova | 6315 | 6394 | 0 | 79 | 603 | TRUE | FALSE |
| painel_transicao | A: extensão, regra antiga | 6315 | 6394 | 0 | 79 | 0 | FALSE | FALSE |
| painel_transicao | B: extensão, regra nova | 6315 | 6394 | 0 | 79 | 720 | FALSE | FALSE |

Com a extensão, firmas que antes tinham menos de três exercícios podem passar a cumprir o filtro e entrar também em anos até 2023 (`linhas_so_novo`). Como a winsorização e a imputação são feitas por ano, essas linhas mexem nos cortes e medianas daquele ano. Divergências nos oito indicadores nesses anos contam como efeito de composição (`nao_explicada = FALSE`); qualquer outra divergência reprova a verificação.

Divergências da comparação B em `painel_completo`, por coluna:

| coluna | celulas | firmas |
|---|---|---|
| LC | 26 | 19 |
| CG | 38 | 25 |
| ALV | 22 | 11 |
| CP | 26 | 19 |
| COB | 32 | 27 |
| FCO | 42 | 32 |
| ROA | 39 | 33 |
| EBITDA | 70 | 50 |
| crit_d_entry | 26 | 26 |
| crit_d_state | 149 | 26 |
| V_provisorio | 133 | 25 |
| <linha só no novo> | 79 | 53 |

Firmas cujo `crit_d_state` mudou em 2010-2023:

| CD_CVM | anos | firma_anos | sentido | DENOM_CIA |
|---|---|---|---|---|
| 2453 | 2019-2023 | 5 | TRUE -> FALSE | CIA ENERGETICA DE MINAS GERAIS - CEMIG |
| 2461 | 2012-2023 | 12 | TRUE -> FALSE | CENTRAIS ELET DE SANTA CATARINA S.A. |
| 3204 | 2014-2023 | 10 | TRUE -> FALSE | CPFL TRANSMISSÃO S.A. |
| 4170 | 2021-2023 | 3 | TRUE -> FALSE | VALE S.A. |
| 5770 | 2020-2023 | 4 | TRUE -> FALSE | EUCATEX S.A. INDUSTRIA E COMERCIO |
| 8036 | 2023-2023 | 1 | TRUE -> FALSE | LIGHT SERVICOS DE ELETRICIDADE S.A. |
| 11975 | 2021-2023 | 3 | TRUE -> FALSE | AZEVEDO E TRAVASSOS S.A. |
| 15253 | 2013-2023 | 11 | TRUE -> FALSE | ENERGISA S.A. |
| 18414 | 2015-2023 | 7 | TRUE -> FALSE | PADTEC HOLDING S.A. |
| 18627 | 2019-2023 | 5 | TRUE -> FALSE | CIA SANEAMENTO DO PARANA - SANEPAR |
| 18775 | 2015-2023 | 9 | TRUE -> FALSE | INVESTIMENTOS E PARTICIP. EM INFRA S.A. - INVEPAR |
| 19208 | 2019-2023 | 5 | TRUE -> FALSE | CONC RIO-TERESOPOLIS S.A. |
| 20010 | 2013-2023 | 11 | TRUE -> FALSE | EQUATORIAL ENERGIA S.A. |
| 20087 | 2016-2023 | 8 | TRUE -> FALSE | EMBRAER S.A. |
| 20303 | 2011-2023 | 13 | TRUE -> FALSE | CEMIG DISTRIBUICAO S.A. |
| 20320 | 2019-2023 | 5 | TRUE -> FALSE | CEMIG GERACAO E TRANSMISSAO S.A. |
| 23000 | 2023-2023 | 1 | TRUE -> FALSE | LIGHT ENERGIA S.A. |
| 23175 | 2015-2023 | 9 | TRUE -> FALSE | IGUA SANEAMENTO S.A. |
| 23230 | 2016-2023 | 8 | TRUE -> FALSE | RAIZEN ENERGIA S.A. |
| 23922 | 2019-2023 | 5 | TRUE -> FALSE | CONCESSIONÁRIA ROTA DO OESTE S.A. |
| 23930 | 2018-2018 | 1 | TRUE -> FALSE | BRASILIANA PARTICIPAÇÕES S/A |
| 24112 | 2019-2023 | 5 | TRUE -> FALSE | AZUL S.A. |
| 25097 | 2023-2023 | 1 | TRUE -> FALSE | NORTE ENERGIA S.A. |
| 25550 | 2021-2023 | 3 | TRUE -> FALSE | ORIZON VALORIZAÇÃO DE RESÍDUOS S.A. |
| 27022 | 2023-2023 | 1 | TRUE -> FALSE | V. TAL - REDE NEUTRA DE TELECOMUNICAÇÕES S.A. |
| 80098 | 2010-2012 | 3 | TRUE -> FALSE | LAEP INVESTMENTS LTD |

Detalhe por coluna, firma e ano: `outputs/verificacao/52_divergencias_detalhe.csv`.

## 5. Atrasos de entrega das DFP

`DT_RECEB_DFP` é a data de recebimento da primeira versão da DFP do exercício; `DT_RECEB_DFP_ULT` é a da versão usada no painel (a mais recente). O atraso é medido contra o prazo regulamentar de três meses após o encerramento do exercício (31/03 para exercícios civis). Valores negativos indicam entrega antecipada.

Firma-anos do painel de insumos com data: 7762 de 7762.

| ano | firma_anos | mediana_dias | p90_dias | no_prazo_pct | atraso_1_30_pct | atraso_31_90_pct | atraso_90p_pct | reapresentadas_pct |
|---|---|---|---|---|---|---|---|---|
| 2010 | 381 | -3.0 | 35.0 | 80.3 | 8.7 | 5.8 | 5.2 | 49.9 |
| 2011 | 413 | -9.0 | 8.8 | 86.2 | 8.0 | 1.7 | 4.1 | 34.9 |
| 2012 | 433 | -9.0 | 11.8 | 86.6 | 5.1 | 3.2 | 5.1 | 32.1 |
| 2013 | 442 | -11.0 | 1.0 | 89.6 | 3.8 | 1.6 | 5.0 | 27.6 |
| 2014 | 436 | -8.0 | 0.0 | 90.4 | 3.4 | 1.8 | 4.4 | 22.7 |
| 2015 | 436 | -8.0 | 0.0 | 92.4 | 3.0 | 3.0 | 1.6 | 20.2 |
| 2016 | 431 | -9.0 | 0.0 | 90.0 | 3.9 | 2.3 | 3.7 | 21.6 |
| 2017 | 434 | -10.0 | -1.0 | 90.6 | 5.8 | 1.2 | 2.5 | 21.0 |
| 2018 | 440 | -6.0 | 0.0 | 90.2 | 3.2 | 1.8 | 4.8 | 25.2 |
| 2019 | 482 | -11.0 | 135.8 | 82.0 | 1.9 | 3.7 | 12.4 | 17.0 |
| 2020 | 538 | -12.0 | 19.3 | 87.2 | 3.7 | 2.2 | 6.9 | 17.8 |
| 2021 | 579 | -13.0 | 0.0 | 91.9 | 2.8 | 1.9 | 3.5 | 18.3 |
| 2022 | 591 | -14.0 | 0.0 | 94.1 | 2.2 | 1.2 | 2.5 | 22.7 |
| 2023 | 604 | -12.0 | 1.0 | 89.2 | 6.8 | 0.7 | 3.3 | 18.0 |
| 2024 | 581 | -12.0 | 0.0 | 94.1 | 2.9 | 1.2 | 1.7 | 18.9 |
| 2025 | 541 | -13.0 | 0.0 | 93.2 | 4.4 | 1.8 | 0.6 | 10.0 |
| Total | 7762 | -10.0 | 1.0 | 89.5 | 4.2 | 2.1 | 4.1 | 22.8 |

Entre as firma-anos do painel de risco, o atraso mediano é de -3 dias nas entradas (V_entrada = 1) e de -11 dias nas demais; entregam depois do prazo 21.9% e 9.8%, respectivamente.

## 6. Motivos de saída do painel

Firmas cujo último exercício no painel é anterior a 2025: 213. Classificadas como potencialmente associadas a distress (falência ou liquidação, RJ, cancelamento de ofício ou emissor paralisado): 44 (20.7%).

| classe | firmas | em_V_no_ultimo_ano | saida_por_filtro | pct |
|---|---|---|---|---|
| fechamento voluntário de capital | 119 | 24 | 9 | 55.9 |
| recuperação judicial | 28 | 24 | 6 | 13.1 |
| motivo não identificado | 25 | 6 | 10 | 11.7 |
| incorporação ou reorganização | 22 | 0 | 0 | 10.3 |
| falência ou liquidação | 12 | 9 | 3 | 5.6 |
| cancelamento por outro motivo | 7 | 4 | 0 | 3.3 |

Detalhe do motivo:

| classe | detalhe | N |
|---|---|---|
| cancelamento por outro motivo | cancelamento de ofício | 4 |
| cancelamento por outro motivo | ELISÃO POR EXTINÇÃO DA CIA | 3 |
| falência ou liquidação | cancelamento de ofício | 6 |
| falência ou liquidação |  | 3 |
| falência ou liquidação | LIQUIDAÇÃO EXTRAJUDICIAL | 1 |
| falência ou liquidação | ELISÃO POR LIQUIDAÇÃO | 1 |
| falência ou liquidação | CANCELAMENTO VOLUNTÁRIO | 1 |
| fechamento voluntário de capital | CANCELAMENTO VOLUNTÁRIO | 118 |
| fechamento voluntário de capital | CANCELAMENTO A PEDIDO (Cia Incentivada) | 1 |
| incorporação ou reorganização | ELISÃO POR INCORPORAÇÃO | 22 |
| motivo não identificado | emissor estrangeiro (BDR); fora do cadastro de companhias abertas | 12 |
| motivo não identificado | registro ativo; continua entregando DFP (saída por filtro amostral) | 10 |
| motivo não identificado | registro ativo; parou de entregar DFP | 2 |
| motivo não identificado | registro suspenso(a) - decisão adm; parou de entregar DFP | 1 |
| recuperação judicial | cancelamento de ofício | 10 |
| recuperação judicial |  | 10 |
| recuperação judicial | CANCELAMENTO VOLUNTÁRIO | 8 |

Das 44 saídas com distress potencial, 36 estavam em estado de vulnerabilidade (V_estado = 1) no último exercício observado, e 8 estavam fora dele. Essas últimas são as que a censura pode estar escondendo como não-eventos.

| CD_CVM | DENOM_CIA | ultimo_ano | classe | detalhe | ano_evento | anos_ate_evento |
|---|---|---|---|---|---|---|
| 16950 | DALETH PARTICIPAÇÕES SA - EM LIQUIDAÇÃO | 2012 | falência ou liquidação | ELISÃO POR LIQUIDAÇÃO | 2015 | 3 |
| 21865 | BRAZAL BRASIL ALIMENTOS SA | 2013 | cancelamento por outro motivo | cancelamento de ofício | 2016 | 3 |
| 8648 | METALURGICA DUQUE SA | 2013 | recuperação judicial | cancelamento de ofício | 2014 | 1 |
| 22373 | ELETROSOM S/A | 2014 | recuperação judicial | cancelamento de ofício | 2015 | 1 |
| 21652 | CTX PARTICIPAÇÕES S/A | 2015 | falência ou liquidação | CANCELAMENTO VOLUNTÁRIO | 2017 | 2 |
| 12319 | BLUE TECH SOLUTIONS EQI S.A. | 2021 | falência ou liquidação | cancelamento de ofício | 2022 | 1 |
| 24961 | AMBIPAR PARTICIPAÇÕES E EMPREENDIMENTOS S.A. | 2024 | recuperação judicial |  | 2025 | 1 |
| 26271 | ENVIRONMENTAL ESG PARTICIPAÇÕES S.A. | 2024 | recuperação judicial |  | 2025 | 1 |

Arquivo completo: `data/final/saidas_2025.csv`.

## 7. Cobertura de ITR

Firmas do painel em cada ano com ITR nos três trimestres. Nenhum indicador trimestral foi construído.

| ano | firmas_painel_no_ano | itr_disponivel | firmas_3_trimestres | pct | firmas_painel_qualquer_ano_3_tri |
|---|---|---|---|---|---|
| 2011 | 394 | TRUE | 381 | 96.7 | 403 |
| 2012 | 410 | TRUE | 398 | 97.1 | 420 |
| 2013 | 417 | TRUE | 402 | 96.4 | 425 |
| 2014 | 414 | TRUE | 397 | 95.9 | 428 |
| 2015 | 418 | TRUE | 412 | 98.6 | 429 |
| 2016 | 414 | TRUE | 403 | 97.3 | 423 |
| 2017 | 417 | TRUE | 409 | 98.1 | 433 |
| 2018 | 428 | TRUE | 409 | 95.6 | 433 |
| 2019 | 471 | TRUE | 412 | 87.5 | 432 |
| 2020 | 524 | TRUE | 468 | 89.3 | 490 |
| 2021 | 559 | TRUE | 530 | 94.8 | 554 |
| 2022 | 578 | TRUE | 563 | 97.4 | 575 |
| 2023 | 586 | TRUE | 565 | 96.4 | 584 |
| 2024 | 568 | TRUE | 568 | 100.0 | 589 |
| 2025 | 529 | TRUE | 529 | 100.0 | 554 |

## 8. Colunas novas e arquivos

Nenhuma coluna existente foi alterada em definição ou posição. Colunas novas, sempre ao final:

- `painel_inputs_2025.csv`: `DT_RECEB_DFP` (primeira entrega), `DT_RECEB_DFP_ULT` (entrega da versão usada), `N_VERSOES_DFP`, `ATRASO_DFP_DIAS` (dias além do prazo de três meses).
- `painel_indicadores_2025.csv`, `eventos_vulnerabilidade_2025.csv`, `painel_completo_2025.csv`, `painel_transicao_2025.csv`: mesmo esquema dos originais.

Arquivos novos: `data/final/rj_detectada_2025.csv`, `data/final/saidas_2025.csv`, `outputs/tables/50_*`, `53_*`, `54_*`, `outputs/verificacao/52_*`.

Scripts: `01b_download_2025.R`, `50_rj_deteccao_2025.R`, `51_painel_2025.R`, `52_verificacao_2025.R`, `53_saidas_2025.R`, `54_cobertura_itr.R`, `55_relatorio_fase_dados.R` e `run_fase_dados.R`, que roda tudo em ordem.

