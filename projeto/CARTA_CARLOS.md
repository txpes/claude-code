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

**O que ainda depende de você**
1. Os comentários sobre a revisão de literatura.
2. A lista de técnicas de avaliação da predição.
3. O que você quis dizer com "os três indicadores". Entendi como os três de maior poder discriminante (retorno sobre ativos, cobertura de juros e margem EBITDA), mas esperei sua confirmação antes de montar esse escore.

Podemos marcar uma conversa para passar por isso?

Abraço,
Thomas

---
Anexo: `Artigo_Fragilidade_Financeira_v2.docx`
