# Revisão do artigo: o que foi pedido e o que foi feito

Thomas G. M. Lopes · outubro de 2026 · referência: `Artigo_Fragilidade_Financeira_v5.docx`

Este documento reúne, num só lugar, os pedidos do coorientador, a resposta ao orientador item a item e as decisões tomadas nos pontos que estavam em aberto. As localizações (§, Tabela, Figura) são as da versão 5 do artigo.

## 1. Pedidos do coorientador (áudios de 13 e 14 de outubro)

| # | Pedido | O que foi feito | Onde |
|---|---|---|---|
| 1 | Números do Brasil na introdução | Média de 43,4% das companhias com cobertura de juros abaixo de 1 em 2010-2025, pico de 62,8% em 2015 e 72 companhias com recuperação judicial ou extrajudicial | §1, 3º parágrafo |
| 2 | Seção com o panorama do Brasil antes da investigação | Seção nova com cobertura de juros, EBITDA negativo, patrimônio negativo e recuperações, ano a ano e por subperíodo | Seção 2, Figura 1 e Tabela 1 |
| 3 | Equações no editor de fórmulas | As três equações viraram objetos de fórmula, numeradas e citadas pelo número | Equações (1) e (2) em §4.1 e §4.2; (3) em §4.4 |
| 4 | Renumerar as seções | Seções e remissões renumeradas; todas as remissões conferidas automaticamente | Todo o texto |
| 5 | Responder o orientador item a item, com localização | Resposta completa na parte 3 deste documento | Parte 3 |
| 6 | Apresentação ao orientador | 15 slides para 20 minutos, com notas | Apresentação anexa (link) |
| 7 | Formato de artigo e submissão depois da reunião | Periódico-alvo escolhido e plano de corte definido | Parte 4, itens c e d |
| 8 | Literatura em dois pilares | 3.1 conceitos; 3.2 pilar não supervisionado (medir); 3.3 pilar supervisionado (prever); 3.4 o que a comparação mede | Seção 3 |
| 9 | Deixar claro que a contribuição não é o método | Texto explícito: PCA e PLS não são novos; a contribuição é a comparação controlada e a decomposição por rota | §3.4 |
| 10 | Comparabilidade entre as duas técnicas | O texto explica o que difere entre elas (objetivo e uso do desfecho) e o que fica fixo (indicadores, amostra, avaliação) | §3.4 |
| 11 | Mais citações recentes | De 1 em 48 para 13 em 60 referências de 2020 em diante, todas conferidas na fonte | Seção 3 e Referências |
| 12 | Seção "A lacuna" e apoio no trabalho de 1984 | Seção retirada; o argumento não se apoia mais em Zmijewski (1984), que fica só como parte da literatura de predição | Seção 3 |
| 13 | Retorno sobre os áudios e manter a reunião | Retorno enviado; reunião mantida | — |

Os ajustes combinados em setembro continuam valendo na v5. São quatro de redação:

- sem autorreferências ("este artigo");
- fonte dos dados descrita na seção de dados, e não na introdução;
- equações numeradas;
- ressalva do auditor com redação suavizada.

São cinco de método:

- esquema temporal;
- classificação fora da amostra;
- dados até 2025;
- decomposição pelo critério do evento;
- frequência trimestral na agenda.

Três números daquele registro mudaram com a conferência dos dados na CVM:

- painel: de 7.419 firma-anos e 730 companhias para 7.403 e 727;
- escore nas entradas puras por prejuízo operacional: de 0,649 para 0,647;
- cargas do primeiro componente: o retorno sobre ativos é a segunda maior, de modo que o texto diz que três das quatro maiores cargas são de estrutura patrimonial.

## 2. O que mudou nos dados

O painel foi conferido contra os arquivos originais da CVM:

- três emissores estrangeiros que deveriam ter sido excluídos saíram;
- quatro firma-anos foram refeitos com as demonstrações corretas;
- todo o código foi rodado de novo, mantendo a divisão das firmas entre as partições, para que a diferença venha só dos dados;
- as 596 células numéricas das tabelas conferem com o código.

As conclusões não mudam. Na decomposição por rota (entradas puras, horizonte de um ano):

- **prejuízo operacional (66 entradas):** o escore fica muito atrás, com 0,647 contra 0,973 da cobertura de juros;
- **patrimônio negativo (51 entradas):** sem diferença distinguível contra as razões isoladas; a vantagem sobre o PLS ficou nominal;
- **recuperação judicial (11 entradas):** sem diferença distinguível contra as razões isoladas; o PLS fica à frente por 0,063, com intervalo que exclui o zero por margem mínima.

## 3. Resposta ao orientador, item a item

**Parte I**

1. **PCA estimado dentro de cada partição.** Médias, desvios-padrão, matriz de correlação e autovetor passaram a ser estimados só nas firmas de treino, e as de teste são projetadas com esses parâmetros. O mesmo vale para a winsorização do modelo de Brito e Assaf Neto e para a escolha de componentes do PLS. A AUC fora da amostra fica em 0,763. *Onde: §4.4.*
2. **Validação minskyana.** A expressão passou a ser "critério externo à variável dependente e não utilizado na calibração supervisionada", e o texto reconhece a sobreposição com a cobertura de juros. Sem a cobertura, a AUC passa de 0,781 para 0,768, e a validade convergente se mantém. *Onde: §6.2 e Tabela A.1.*
3. **Calendário informacional.** Uma subseção nova trata da data de referência dos indicadores, da divulgação, da janela do evento e da datação da recuperação judicial. São 11 entradas expostas a antecipação artificial, e o resultado não muda sem elas. Há também um teste com a recuperação judicial antecipada em um ano. *Onde: §4.6, §6.8 e §6.9.*
4. **Saída do painel.** As 200 saídas foram classificadas pelo cadastro da CVM: 119 fechamentos voluntários, 28 recuperações judiciais, 22 incorporações, 12 falências ou liquidações, 7 por outros motivos e 12 sem motivo. Tratar as saídas por dificuldade financeira como evento não muda a conclusão, e a limitação passou a ser descrita como censura informativa e risco competitivo. *Onde: §6.8 e Tabela A.5.*
5. **Inferência.** O bootstrap agrupado por firma é a inferência principal, com Bonferroni aplicado sobre ele; DeLong fica como referência. *Onde: §4.4 e Tabela 9.*
6. **Métricas além da AUC ROC.** Com limiar fixado no treino, o artigo traz:
   - PR-AUC e Brier;
   - inclinação e intercepto de calibração;
   - sensibilidade, especificidade, VPP e VPN;
   - decisão líquida;
   - gráfico de calibração por decis;
   - taxa de captura no decil de maior risco.

   A calibração é feita sobre o posto do escore. *Onde: §4.4, §6.7, Tabela 15 e Figura 5.*
7. **Múltiplas entradas.** Das 171 firmas com entrada, 149 têm uma e 22 têm duas ou mais. Com só a primeira entrada, o resultado não muda. *Onde: §5.3 e Tabela A.5.*
8. **H4.** Está declarada como análise diagnóstica posterior, inclusive no resumo. *Onde: §4.5 e §6.6.*
9. **Mecanismo.** As três formulações apontadas foram trocadas pelas versões moderadas sugeridas. *Onde: §6.5 e §6.6.*

**Parte II**

- **0,730 e 0,735.** Convenção única: a atribuição de referência; as médias entre atribuições aparecem só onde a nota da tabela indica. *Onde: §4.4 e notas das tabelas.*
- **H1.** "Parcialmente sustentada quanto à coerência do eixo e rejeitada quanto à unidimensionalidade". *Onde: §6.1.*
- **Uso do CP1.** Os quatro argumentos sugeridos e a verificação com o segundo componente. *Onde: §6.1 e §6.8.*
- **Índice agregado.** Fica só como agenda, sem prometer viabilidade econométrica. *Onde: §7.2.*

## 4. Decisões tomadas nos pontos que estavam em aberto

**a. Técnicas de avaliação.** Entraram as duas adições propostas, e a lista fica fechada aqui.

- **Gráfico de calibração por decis** (Figura 5). Em um ano, os modelos acompanham a diagonal nos decis inferiores. No decil de maior risco:
  - cobertura de juros: prevê 0,167 e observa 0,185;
  - árvores impulsionadas: prevê 0,173 e observa 0,203;
  - escore sintético: prevê 0,094 e observa 0,135. Além de ordenar pior, ele subestima o risco no topo.
- **Captura no decil de maior risco** (§6.7):
  - em um ano, os 10% de firma-anos de maior risco concentram 46,3% das entradas pelo escore, 62,4% pela cobertura de juros (diferença de +0,161, intervalo de +0,057 a +0,263) e 68,5% pelas árvores;
  - em dois anos, 25,4% pelo escore e 19,8% pela cobertura, diferença não distinguível; só as árvores, com 38,9%, superam o escore com intervalo que exclui o zero.

Outras medidas, como KS e Gini, não acrescentam informação: são transformações da mesma ordenação que a AUC ROC já mede.

**b. Escore com três indicadores.** O escore usa retorno sobre ativos, cobertura de juros e margem EBITDA, os três de maior poder discriminante, com PCA estimado só no treino.

- **No agregado:** em um ano, 0,895, contra 0,894 da cobertura de juros; em dois anos, 0,722, contra 0,681 (diferença de +0,041, intervalo de +0,020 a +0,063). A seleção refeita dentro do treino escolhe o mesmo trio em 99 das 100 partições.
- **Por rota, um ano:** 0,959 no prejuízo operacional (66 entradas), 0,784 no patrimônio negativo (51) e 0,888 na recuperação judicial (11).
- **Por rota, dois anos:** 0,576 (52 entradas), 0,802 (46) e 0,798 (9).

*Onde: §6.6.*

**c. Periódico-alvo: Revista Contabilidade & Finanças (USP).** É a revista com melhor encaixe: indicadores contábeis de companhias abertas brasileiras, e o modelo de Brito e Assaf Neto, usado como referência, foi publicado nela. Pelas instruções aos autores na página da revista no SciELO:

- aceita submissão em português e publica em inglês, com tradução a cargo dos autores depois da aprovação;
- limite de 8.000 palavras sem as referências e resumo de 250 a 300 palavras;
- citações em APA, avaliação triplo-cega e nenhuma taxa.

A página antiga da revista no portal da USP diz que não aceita submissões, mas foi atualizada pela última vez em 2023; a página do SciELO aponta para o sistema de submissão em uso. Isso será confirmado no momento da submissão. Se a RC&F não estiver aberta, a alternativa é a Brazilian Business Review.

**d. Formato de artigo: duas versões do mesmo trabalho.** O corpo do texto atual tem cerca de 15.600 palavras, quase o dobro do limite. A decisão é manter a versão longa como base da dissertação e derivar dela uma versão curta para submissão. Orçamento de palavras da versão curta:

| Parte | Hoje | Versão curta | Como |
|---|---|---|---|
| Resumo, introdução e panorama | 2.500 | 1.200 | Panorama reduzido a uma figura e um parágrafo |
| Literatura (seção 3) | 2.400 | 1.300 | Manter os dois pilares e a §3.4; resumir os estudos citados |
| Metodologia e dados (seções 4 e 5) | 4.300 | 1.900 | Calendário e detalhes do painel para o apêndice |
| Resultados (6.1 a 6.7) | 4.400 | 2.600 | 6.2 e 6.4 para o apêndice; manter 6.3, 6.5 e 6.6 inteiras |
| Robustez, limitações e conclusão | 2.000 | 1.000 | Robustez em tabela única no apêndice |
| **Total** | **15.600** | **8.000** | |

A versão curta é feita depois da reunião com o orientador, para incorporar o que ele pedir. A tradução para o inglês só é necessária depois da aprovação.

**e. Formatação.** A v5 já segue a ABNT: A4, margens de 3 e 2 cm, Times New Roman 12, espaçamento 1,5, referências em ABNT e páginas numeradas. A versão de submissão será convertida para as normas da revista: margens de 2,5 cm, espaçamento duplo, APA, sem notas de rodapé e sem identificação de autoria. A dissertação seguirá o modelo do programa.

**f. Nota de decisões.** Não será enviada à parte; o conteúdo dela está consolidado neste documento.

## 5. Próximos passos

1. Reunião com o orientador: apresentação do que foi feito e definição da versão curta.
2. Em até duas semanas depois da reunião: versão curta, nas normas da revista, para revisão dos dois.
3. Submissão, com tradução para o inglês depois da aprovação.
4. Dissertação a partir da versão longa: cada item da agenda (§7.2) vira um capítulo.

Fica pendente um único ponto, que depende de terceiros: o e-mail com pontos específicos que o coorientador mencionou ainda não chegou. Quando chegar, cada ponto será tratado no artigo.
