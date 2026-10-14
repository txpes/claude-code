# Resposta ao orientador, item a item (versão para revisão do Carlos)

*Pedido do coorientador (áudio de 13/10): responder o e-mail do Eduardo item a item, com a localização de cada mudança, e mandar primeiro ao Carlos. Os números de seção e de tabela são os da v3 (`Artigo_Fragilidade_Financeira_v3.docx`).*

---

**Assunto:** Re: Observações sobre o artigo

Eduardo, bom dia!

Obrigado pelas observações. Segue a versão revisada do artigo e, abaixo, o que foi feito em cada ponto, com a indicação de onde está no texto.

**Parte I**

1. **PCA estimado dentro de cada partição.** Médias, desvios-padrão, matriz de correlação e autovetor passaram a ser estimados só nas firmas de treino, e as de teste são projetadas com esses parâmetros. O mesmo vale para a winsorização do modelo de Brito e Assaf Neto e para a escolha de componentes do PLS. A AUC fora da amostra fica em 0,764. *Onde: §4.4.*
2. **Validação minskyana.** A expressão passou a ser "critério externo à variável dependente e não utilizado na calibração supervisionada", e o texto reconhece a sobreposição com a cobertura de juros. Refeita com um escore sem a cobertura, a AUC passa de 0,782 para 0,769, e a validade convergente se mantém. *Onde: §6.2 e Tabela A.1.*
3. **Calendário informacional.** A nova §4.6 explica:
   - a data de referência dos indicadores;
   - quando a informação se torna pública;
   - a janela do evento;
   - a regra quando demonstração e evento caem no mesmo ano civil;
   - como a recuperação judicial é datada.

   A exposição a antecipação artificial é medida (11 entradas), e o resultado não muda sem elas. Fiz também um teste antecipando a data da recuperação judicial. *Onde: §4.6, §6.8 e §6.9.*
4. **Saída do painel.** Classifiquei o motivo das 201 saídas pelo cadastro da CVM:

   | Motivo | Saídas |
   |---|---|
   | Fechamento voluntário | 119 |
   | Recuperação judicial | 28 |
   | Incorporação | 22 |
   | Falência ou liquidação | 12 |
   | Outros | 7 |
   | Sem motivo | 13 |

   Tratar as saídas por dificuldade financeira como evento não muda a conclusão. A limitação passou a ser descrita como censura informativa e risco competitivo, e não só como viés de sobrevivência. *Onde: §6.8 e Tabela A.5; também na introdução.*
5. **Inferência.** O bootstrap agrupado por firma é a inferência principal em todas as comparações, com Bonferroni aplicado sobre ele. O DeLong ficou apenas como referência convencional. *Onde: §4.4 e Tabela 9.*
6. **Métricas além da AUC ROC.** Incluí, com limiar fixado no treino:
   - PR-AUC e Brier;
   - inclinação e intercepto de calibração;
   - sensibilidade, especificidade, VPP e VPN;
   - decisão líquida.

   A calibração passou a ser feita sobre o posto do escore, e todos os modelos superam a previsão constante no Brier. *Onde: §4.4, §6.7 e Tabela 15.*
7. **Múltiplas entradas.** Das 171 firmas com entrada, 149 têm uma e 22 têm duas ou mais. Cada reentrada é tratada como novo evento, e a sensibilidade só com a primeira entrada não muda o resultado. *Onde: §5.3 e Tabela A.5.*
8. **H4.** Está declarada como análise diagnóstica posterior, inclusive no resumo, e o texto usa "a análise diagnóstica fornece evidência consistente com H4". *Onde: §4.5 e §6.6.*
9. **Mecanismo.** As três formulações que você apontou foram substituídas pelas versões moderadas que sugeriu, e o restante do texto segue o mesmo tom. *Onde: §6.5 e §6.6.*

**Parte II**

- **0,730 e 0,735.** A divergência foi eliminada. O texto usa uma convenção única, a atribuição de referência, e as médias entre atribuições aparecem só onde a nota da tabela indica. *Onde: §4.4 e notas das tabelas.*
- **H1.** Agora está "parcialmente sustentada quanto à coerência do eixo e rejeitada quanto à unidimensionalidade". *Onde: §6.1.*
- **Uso do CP1.** Incluí os quatro argumentos que você sugeriu e a verificação com o segundo componente. *Onde: §6.1 e §6.8.*

**Índice agregado.** Ficou apenas como agenda, sem compromisso e sem prometer viabilidade econométrica. *Onde: §7.2.*

**Outras mudanças desde a versão que você leu**
- **Panorama:** nova seção 2, com o panorama da dificuldade financeira das companhias abertas brasileiras de 2010 a 2025 (Figura 1 e Tabela 1).
- **Literatura:** a revisão foi reorganizada em dois pilares, não supervisionado e supervisionado (seção 3), e ganhou trabalhos recentes.
- **Equações:** passaram para o editor de fórmulas.
- **Escore com três indicadores:** um escore só com os três indicadores de maior poder discriminante acompanha o melhor indicador isolado, sem superá-lo, o que reforça a leitura de composição (§6.6).
- **Código e números:** a revisão de código corrigiu alguns números. Nenhum altera a conclusão, e todas as tabelas conferem com o código.
- **Estrutura:** as tabelas de validação e robustez foram para o Apêndice A.

Fico à disposição para apresentar o trabalho na reunião.

Abraço,
Thomas
