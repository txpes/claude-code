# Rascunho de mensagem ao orientador

*Rascunho para você revisar e enviar. Está escrito em primeira pessoa, como vindo de você.*

---

Eduardo,

Segue a versão revisada do artigo. Ela responde aos seus comentários e incorpora uma revisão integral dos dados, do código, dos números e das referências. Vão três arquivos principais:

- `Artigo_Fragilidade_Financeira_revisado.docx`: com alterações controladas, para você ver cada mudança;
- `Artigo_Fragilidade_Financeira_revisado_limpo.docx`, e o PDF correspondente: as mesmas alterações já aceitas, para leitura corrida;
- `Nota_Decisoes_Metodologicas_revisada.docx`: também com a versão limpa e o PDF.

As duas versões diferem na numeração das tabelas:
- **Versão com alterações controladas:** mantém a ordem e a numeração originais, as mesmas dos seus comentários, para que cada mudança possa ser comparada com o original.
- **Versão limpa:** já traz a estrutura final, com as tabelas de validação e de robustez no Apêndice A (ver seção 4).

Esta mensagem usa a numeração final. A correspondência com a original está na seção 4.

## 1. Seus comentários, item a item

| Comentário | O que foi feito |
|---|---|
| I.1. PCA dentro da partição | Padronização, correlação, autovetores e quantis de winsorização estimados apenas no treino (§3.4) |
| I.2. Validação minskyana não independente | Critério apresentado como externo à variável dependente, mas não independente dos insumos; o escore sem cobertura dá 0,770 contra 0,783 (§5.2, Tabela A.1) |
| I.3. Calendário informacional | §3.6 com data de referência, divulgação e regra do mesmo ano civil. A limitação das datas de RJ foi testada (§5.9, ver seção 2) |
| I.4. Saída não é só sobrevivência | Composição das 201 saídas pelo cadastro na §5.8: voluntária 119, RJ 28, incorporação 22, falência ou liquidação 12, outros 7, sem motivo 13. Saída por dificuldade tratada como **risco competitivo**. Linha nova na Tabela A.5: as 44 saídas por dificuldade como evento dão F 0,762 e cobertura 0,889, e a conclusão se mantém |
| I.5. DeLong → bootstrap agrupado | Bootstrap agrupado por firma (2.000 réplicas) é o teste principal; o DeLong fica só como referência convencional. A §2.4, que ainda falava em DeLong, foi alinhada |
| I.6. Métricas além da AUC | Tabela 14 refeita: PR-AUC, Brier, inclinação de calibração, firma-anos sinalizados, VPP, especificidade e decisão líquida a 10:1, no limiar de 80% de sensibilidade. Interceptos e VPN estão no texto e na nota. O horizonte de dois anos está no texto, e a versão completa (dois horizontes, decisão líquida a 5:1, 10:1 e 20:1) está na planilha. A calibração passou a ser feita sobre o posto do escore, e com isso os seis modelos batem a previsão constante no Brier |
| I.7. Múltiplas entradas | §4.3 (171 firmas, 22 com duas ou mais entradas) e sensibilidade só com a primeira entrada (Tabela A.5) |
| I.8. H4 como diagnóstica | Estatuto declarado na §3.5 e, agora, também no resumo ("de caráter exploratório") |
| I.9. Moderar o mecanismo | O mecanismo de composição está escrito como "os dados são consistentes com", sem afirmação causal |
| II.a. Harmonizar AUCs | Convenção única (atribuição de referência no texto; médias das dez atribuições apenas onde a nota diz) |
| II.b e II.c. H1 e uso do CP1 | Formulação que você sugeriu (§3.5 e §5.1) |
| Cautela com o índice agregado | A §6.2 ficou só como agenda, sem prometer a viabilidade |

## 2. O que a revisão encontrou além dos seus comentários

Nenhuma das correções muda a conclusão central. As que mais importam:

1. **Sobreposição mecânica na rota operacional.** As entradas por prejuízo operacional já têm EBITDA negativo em t, e a margem EBITDA sozinha chega a 0,978. Por isso, o contraste de um ano (0,649 contra 0,973) é em boa parte mecânico. O texto diz isso e traz o horizonte de dois anos (0,377 contra 0,522) no resumo, na introdução e na conclusão. A coluna da margem EBITDA foi incluída na Tabela 10.
2. **Teste da data de RJ.** Antecipei em um ano a RJ das 22 firmas cujo primeiro documento é de andamento. São 22, e não 30 como constava na nota. O resultado central não muda, com duas consequências:
   - a vantagem do escore sobre o PLS nas entradas por patrimônio negativo deixa de ser significativa, e o texto foi ajustado;
   - em dois anos, a vantagem da cobertura sobre o escore passa a resistir ao Bonferroni.
3. **Código.** Corrigi estes problemas:
   - as saídas usavam uma data fixa de 2023, o que dava 143 saídas em vez de 201;
   - o sinal do CP2 trocava entre partições;
   - o critério Ponzi não exigia anos consecutivos;
   - o Brito e Assaf Neto dentro da amostra não era winsorizado;
   - o Bonferroni aparecia como ×7 no texto e ×6 no código (agora é ×6 nos dois).

   O pacote roda do zero com um único comando, com as versões das bibliotecas fixadas.
4. **Números.** Um verificador automático compara as 596 células numéricas das tabelas com a saída do código e não encontra divergência. No original, ele acusava 50 células.
5. **Literatura.** Conferi na fonte o que o texto afirma de 20 obras, e 13 afirmações foram corrigidas. A mais séria era sobre Mantoan et al. (2021): o artigo dizia o contrário do que eles concluem. As outras correções:
   - Torres Filho et al.;
   - Davis et al.;
   - Zmijewski;
   - a definição de firma zumbi (três anos);
   - a CAPAG (regra de classificação, e não pesos).

   A lista agora tem 48 referências, todas conferidas pelo DOI ou na fonte oficial, entre elas as de método que faltavam e três trabalhos recentes de previsão com aprendizado de máquina.

## 3. Ajustes menores que tomei nesta rodada

Todos são de baixo risco e reversíveis:

- estatuto exploratório da decomposição explicitado no resumo;
- significâncias escritas como p < 0,001;
- equivalência entre "critério (b)" e "prejuízo operacional" declarada uma vez;
- classificação JEL (G33; G32; C38; C53; E12), abstract e keywords;
- seção "Disponibilidade de dados e código";
- larguras de colunas das Tabelas 10, 11 e A.5, para evitar palavras quebradas;
- a antiga Tabela 8 (validação minskyana) e a de métricas, que não eram citadas no texto, passaram a ser.

## 4. Estrutura e próximos passos

1. **Manchete.** Mantive os dois horizontes lado a lado: um ano, com a ressalva da sobreposição mecânica, e dois anos, em que a leitura de composição se sustenta. Se você preferir fazer do horizonte de dois anos a manchete da rota operacional, a mudança fica restrita ao resumo, à introdução e à conclusão.
2. **Corpo e apêndice.** O corpo ficou com as 14 tabelas que sustentam as hipóteses e o argumento central. As 6 de validação, avaliação complementar e robustez foram para o Apêndice A, depois das referências. Todas são citadas no texto, e a numeração segue a ordem de citação.

| Original | Final | | Original | Final |
|---|---|---|---|---|
| 1 a 7 | 1 a 7 | | 14 | 11 |
| 8 (validação minskyana) | A.1 | | 15 | 12 |
| 9 (controles e dentro da amostra) | A.2 | | 16 | 13 |
| 10 | 8 | | 17 | 14 |
| 11 (esquema temporal) | A.3 | | 18 (definições alternativas) | A.4 |
| 12 | 9 | | 19 (sensibilidade) | A.5 |
| 13 | 10 | | 20 (defasagens) | A.6 |

3. **Idioma e periódico-alvo.** O abstract já está no artigo. Se o alvo for internacional, preparo a versão em inglês quando você der o de acordo com a estrutura.

Fico aguardando também os comentários da coorientação sobre a revisão de literatura e as técnicas de avaliação.

Abraço,
