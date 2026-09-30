# E-mail ao coorientador

**Assunto:** Mudanças no artigo a partir dos comentários do Eduardo

Carlos, tudo bem?

O Eduardo me mandou comentários sobre a versão anterior do artigo, e fiz as mudanças. Segue em anexo a versão atual. Gostaria de conversar com você sobre elas, principalmente sobre os pontos em que tocam o que tínhamos combinado.

**O que o Eduardo pediu e foi feito**
- **PCA dentro das partições:** padronização, correlação e autovetores agora são estimados só no treino. A AUC fora da amostra fica em 0,764.
- **Validação minskyana:** refeita sem a cobertura de juros. A AUC passa de 0,782 para 0,769.
- **Calendário informacional:** nova §3.6, com a data de referência, a divulgação e a regra quando o evento cai no mesmo ano civil. Fiz também um teste antecipando a data da recuperação judicial.
- **Saídas do painel:** classifiquei o motivo das 201 saídas no cadastro da CVM, tratei as saídas por dificuldade como evento e passei a descrevê-las como censura informativa e risco competitivo.
- **Inferência:** o bootstrap agrupado por firma é o teste principal, e o DeLong ficou só como complemento.
- **Métricas:** além da AUC, entram PR-AUC, Brier, calibração, especificidade, VPP, VPN e decisão líquida (Tabela 14).
- **Múltiplas entradas:** são 22 firmas com duas ou mais entradas, e fiz uma sensibilidade só com a primeira entrada.
- **Moderação:** H4 ficou identificada como análise exploratória, e o texto do mecanismo foi moderado.

**Onde isso toca os seus comentários**
- **Dependência entre os critérios.** O Eduardo não tratou disso, mas a revisão reforçou o seu ponto. As 66 entradas só por prejuízo operacional já têm EBITDA negativo no ano da previsão, e a margem EBITDA sozinha alcança 0,978 nesse grupo. Por isso, o texto trata o contraste de um ano como em boa parte mecânico e destaca o horizonte de dois anos. Os três grupos de entradas puras em um ano:
  - prejuízo operacional, 66 entradas: escore 0,649 contra 0,973 da cobertura;
  - patrimônio negativo, 51 entradas: escore 0,816, sem diferença distinguível;
  - recuperação judicial, 11 entradas: escore 0,828, também sem diferença distinguível.

  Em dois anos, com 52, 46 e 9 entradas, o escore fica em 0,377, 0,796 e 0,801.
- **"Cego a uma das rotas".** Por pedido do Eduardo de moderar as afirmações, a formulação passou a ser "desempenho fraco em uma das rotas".
- **Frequência trimestral.** O Eduardo recomendou não tratar o índice agregado como capítulo obrigatório antes de verificar a viabilidade econométrica. A agenda agora diz que a cobertura dos dados trimestrais é alta, mas não afirma que a extensão é viável. Queria ouvir sua opinião, já que aqui as recomendações de vocês apontam em direções um pouco diferentes.
- **Separação temporal e classificação.** Continuam no artigo. Como as tabelas de robustez foram para um apêndice, a separação temporal é agora a Tabela A.3, a comparação dentro e fora da amostra é a A.2, e a de classificação é a Tabela 14.

**Os três indicadores**

Montei o escore com o retorno sobre ativos, a cobertura de juros e a margem EBITDA, pelo mesmo procedimento não supervisionado e sem vazamento (fim da §5.6):
- **Um ano:** 0,895, contra 0,764 do escore com os oito indicadores e 0,894 da cobertura. Empata com a cobertura.
- **Dois anos:** 0,722. Supera a cobertura (0,681) com diferença significativa e empata com o ROA (0,731).
- **Robustez:** a média simples dos três dá o mesmo resultado. Refazendo a escolha dos três dentro de cada partição de treino, o mesmo trio aparece em 98 de 100 partições.

Ou seja, agregando só os melhores componentes, o escore acompanha o melhor indicador isolado, mas não o supera. Isso reforça a leitura de que o problema do escore original está na composição, e não na agregação em si.

Uma ressalva: em um ano, a margem EBITDA traz de volta a sobreposição mecânica. Por rota:
- **Um ano:** 0,958 nas 66 entradas por prejuízo operacional, 0,784 nas 51 por patrimônio negativo e 0,888 nas 11 por recuperação judicial.
- **Dois anos:** 0,576, 0,801 e 0,798, com 52, 46 e 9 entradas.

**Técnicas de avaliação da predição: uma proposta para fechar**

O artigo já cobre as três dimensões usuais de avaliação:
- **Discriminação:** AUC ROC, com bootstrap agrupado por firma e Bonferroni, e PR-AUC.
- **Calibração:** Brier e inclinação e intercepto de calibração.
- **Utilidade:** sensibilidade, especificidade, VPP, VPN e decisão líquida.

Tudo isso sob dois esquemas de validação: por firma e temporal.

Minha proposta é fechar a lista assim. O KS já está na tabela de diagnóstico, e o Gini (2 × AUC − 1) é equivalente à AUC. Se você achar importante, há duas adições baratas, porque o código já tem tudo:
1. um gráfico de calibração;
2. a taxa de captura dos eventos no decil de maior risco, mais próxima da prática de crédito.

Faz sentido para você?

**Revisão de literatura**

Quando puder, me reenvie seus comentários sobre a revisão de literatura.

Podemos marcar uma conversa para passar por isso?

Abraço,
Thomas

---
Anexo: `Artigo_Fragilidade_Financeira_v2.docx`
