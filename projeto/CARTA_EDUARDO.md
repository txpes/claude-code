# Rascunho de mensagem ao orientador

*Rascunho para você revisar e enviar. Está escrito em primeira pessoa, como vindo de você.*

---

Eduardo,

Segue a versão revisada do artigo. Ela responde aos seus comentários e incorpora uma revisão integral dos dados, do código, dos números e das referências. Vão três arquivos principais:

- `Artigo_Fragilidade_Financeira_revisado.docx`: com alterações controladas, para você ver cada mudança;
- `Artigo_Fragilidade_Financeira_revisado_limpo.docx`, e o PDF correspondente: as mesmas alterações já aceitas, para leitura corrida;
- `Nota_Decisoes_Metodologicas_revisada.docx`: também com a versão limpa e o PDF.

## 1. Seus comentários, item a item

| Comentário | O que foi feito |
|---|---|
| I.1. PCA dentro da partição | Padronização, correlação, autovetores e quantis de winsorização estimados apenas no treino (§3.4) |
| I.2. Validação minskyana não independente | Critério apresentado como externo à variável dependente, mas não independente dos insumos; o escore sem cobertura dá 0,770 contra 0,783 (§5.2, Tabela 8) |
| I.3. Calendário informacional | §3.6 com data de referência, divulgação e regra do mesmo ano civil. A limitação das datas de RJ foi testada (§5.9, ver seção 2) |
| I.4. Saída não é só sobrevivência | Composição das 201 saídas pelo cadastro na §5.8: voluntária 119, RJ 28, incorporação 22, falência ou liquidação 12, outros 7, sem motivo 13. Saída por dificuldade tratada como **risco competitivo**. Linha nova na Tabela 19: as 44 saídas por dificuldade como evento dão F 0,762 e cobertura 0,889, e a conclusão se mantém |
| I.5. DeLong → bootstrap agrupado | Bootstrap agrupado por firma (2.000 réplicas) é o teste principal; o DeLong fica só como referência convencional. A §2.4, que ainda falava em DeLong, foi alinhada |
| I.6. Métricas além da AUC | Tabela 17 refeita nos dois horizontes: PR-AUC, Brier, inclinação e intercepto de calibração, sensibilidade, especificidade, VPP, VPN e decisão líquida a 5:1, 10:1 e 20:1. A calibração passou a ser feita sobre o posto do escore, e com isso os seis modelos batem a previsão constante no Brier |
| I.7. Múltiplas entradas | §4.3 (171 firmas, 22 com duas ou mais entradas) e sensibilidade só com a primeira entrada (Tabela 19) |
| I.8. H4 como diagnóstica | Estatuto declarado na §3.5 e, agora, também no resumo ("de caráter exploratório") |
| I.9. Moderar o mecanismo | O mecanismo de composição está escrito como "os dados são consistentes com", sem afirmação causal |
| II.a. Harmonizar AUCs | Convenção única (atribuição de referência no texto; médias das dez atribuições apenas onde a nota diz) |
| II.b e II.c. H1 e uso do CP1 | Formulação que você sugeriu (§3.5 e §5.1) |
| Cautela com o índice agregado | A §6.2 ficou só como agenda, sem prometer a viabilidade |

## 2. O que a revisão encontrou além dos seus comentários

Nenhuma das correções muda a conclusão central. As que mais importam:

1. **Sobreposição mecânica na rota operacional.** As entradas por prejuízo operacional já têm EBITDA negativo em t, e a margem EBITDA sozinha chega a 0,978. Por isso, o contraste de um ano (0,649 contra 0,973) é em boa parte mecânico. O texto diz isso e traz o horizonte de dois anos (0,377 contra 0,522) no resumo, na introdução e na conclusão. A coluna da margem EBITDA foi incluída na Tabela 13.
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
4. **Números.** Um verificador automático compara as 584 células numéricas das tabelas com a saída do código e não encontra divergência. No original, ele acusava 50 células.
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
- larguras de colunas das Tabelas 13, 14 e 19, para evitar palavras quebradas.

## 4. Onde eu gostaria da sua opinião

1. **Manchete.** Proponho manter a estrutura atual, com os dois horizontes lado a lado. Uma alternativa é tornar o horizonte de dois anos a manchete da rota operacional e tratar o de um ano como sobreposição mecânica. Você prefere assim?
2. **Corpo e apêndice.** São 20 tabelas. Minha proposta é deixar no corpo as Tabelas 1 a 4, 10, 13, 14 e 17, e passar as de robustez (8, 9, 11, 12, 15, 16, 18 a 20) para um apêndice.
3. **Idioma e periódico-alvo.** Se o alvo for internacional, preparo a versão em inglês depois que a estrutura estiver fechada.

Fico aguardando também os comentários da coorientação sobre a revisão de literatura e as técnicas de avaliação.

Abraço,
