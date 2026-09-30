# E-mail ao orientador

**Assunto:** Artigo revisado a partir dos seus comentários

Eduardo, bom dia!

Segue em anexo a versão revisada do artigo, com as mudanças feitas a partir dos seus comentários. Abaixo, o que foi feito em cada ponto.

**Parte I**

1. **PCA dentro das partições:** padronização, correlação, autovetores e winsorização agora são estimados só no treino, e o teste é projetado com esses parâmetros (§3.4). A AUC quase não mudou (0,764).
2. **Validação minskyana:**
   - troquei "critério independente" pela formulação que você sugeriu;
   - refiz a validação sem a cobertura de juros: a AUC passa de 0,782 para 0,769, e a validade convergente se sustenta (§5.2).
3. **Calendário informacional:** nova §3.6, com a data de referência, a divulgação, a janela do evento e a regra do mesmo ano civil. Testei também a antecipação da data da recuperação judicial, e o resultado central não muda.
4. **Saídas do painel:**
   - levantei o motivo de cada uma das 201 saídas no cadastro da CVM: 119 fechamentos voluntários, 28 recuperações judiciais, 22 incorporações, 12 falências ou liquidações, 7 outros e 13 sem motivo;
   - tratei as saídas por dificuldade como evento, e a conclusão se mantém;
   - o texto agora fala em censura informativa e risco competitivo.
5. **Inferência:** o bootstrap agrupado por firma virou o teste principal, com Bonferroni aplicado sobre ele. O DeLong ficou apenas como referência complementar.
6. **Métricas além da AUC:** incluí PR-AUC, Brier, inclinação e intercepto de calibração, especificidade, VPP, VPN e decisão líquida, com o limiar definido no treino (§5.7). Com a calibração feita sobre o posto do escore, todos os modelos superam a previsão constante no Brier.
7. **Múltiplas entradas:**
   - são 171 firmas com entrada: 149 com uma e 22 com duas ou mais;
   - cada reentrada é tratada como novo evento;
   - a sensibilidade só com a primeira entrada não muda o resultado (§4.3).
8. **H4:** está identificada como análise diagnóstica e exploratória, inclusive no resumo, com a formulação "evidência consistente com H4".
9. **Mecanismo:** substituí as três frases que você apontou e mantive o mesmo tom moderado no restante do texto.

**Parte II**

- **AUCs:** a divergência entre 0,730 e 0,735 foi eliminada. O texto usa uma convenção única, a partição de referência, e as médias entre atribuições aparecem só onde a nota da tabela indica.
- **H1:** agora está "parcialmente sustentada quanto à coerência do eixo e rejeitada quanto à unidimensionalidade".
- **Uso do CP1:** incluí os quatro argumentos que você sugeriu (§5.1).

**Índice agregado**

Ficou apenas como agenda (§6.2), sem compromisso. Não será um capítulo obrigatório da dissertação.

**Outros ajustes da revisão**

- **Código e números:** corrigi alguns erros de código e números desatualizados no texto. Nenhum altera a conclusão, e todas as tabelas batem com o código.
- **Referências:** conferi as referências e o que o texto atribui a cada autor. Algumas citações foram corrigidas.
- **Prejuízo operacional:** no horizonte de um ano, o contraste nessa rota é em boa parte mecânico, porque o evento já aparece no EBITDA do ano da previsão. Por isso, o texto passou a destacar também o horizonte de dois anos, em que a diferença se mantém.
- **Apêndice:** as tabelas de validação e robustez foram para um apêndice, o que mudou a numeração das tabelas em relação à versão que você comentou.

Fico à disposição para conversarmos.

Abraço,
Thomas

---
Anexo: `Artigo_Fragilidade_Financeira_v2.docx`
