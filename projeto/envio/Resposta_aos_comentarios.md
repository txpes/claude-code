# Resposta aos comentários do orientador, item a item

Thomas G. M. Lopes · novembro de 2026 · artigo: versão 6

Este documento segue a ordem do e-mail com as observações sobre o artigo. Para cada item, indica o que foi feito e onde está no texto. As seções, tabelas e figuras citadas são as da versão 6.

## Parte I

1. **PCA estimado dentro de cada partição.** Médias, desvios-padrão, matriz de correlação e autovetor passaram a ser estimados só nas firmas de treino, e as de teste são projetadas com esses parâmetros. O mesmo vale para a winsorização do modelo de Brito e Assaf Neto e para a escolha de componentes do PLS. A AUC fora da amostra fica em 0,763. *Onde: §4.4.*
2. **Validação minskyana.** A expressão passou a ser "critério externo à variável dependente e não utilizado na calibração supervisionada", e o texto reconhece a sobreposição com a cobertura de juros. Refeita com um escore sem a cobertura, a AUC passa de 0,781 para 0,768, e a validade convergente se mantém. *Onde: §6.2 e Tabela A.1.*
3. **Calendário informacional.** Uma subseção nova explica a data de referência dos indicadores, o momento em que a informação se torna pública, a janela do evento, a regra quando demonstração e evento caem no mesmo ano civil e a datação da recuperação judicial. A exposição a antecipação artificial é medida (11 entradas), e o resultado não muda sem elas. Há também um teste com a data da recuperação judicial antecipada em um ano. *Onde: §4.6, §6.8 e §6.9.*
4. **Saída do painel.** O motivo das 200 saídas foi classificado pelo cadastro da CVM: 119 fechamentos voluntários, 28 recuperações judiciais, 22 incorporações, 12 falências ou liquidações, 7 por outros motivos e 12 sem motivo identificado. Tratar as saídas por dificuldade financeira como evento não muda a conclusão. A limitação passou a ser descrita como censura informativa e risco competitivo, e não só como viés de sobrevivência. *Onde: §6.8 e Tabela A.5; também na introdução.*
5. **Inferência.** O bootstrap agrupado por firma é a inferência principal em todas as comparações, com Bonferroni aplicado sobre ele. O teste de DeLong ficou apenas como referência convencional. *Onde: §4.4 e Tabela 9.*
6. **Métricas além da AUC ROC.** Com limiar fixado no treino, o artigo traz:
   - PR-AUC e Brier;
   - inclinação e intercepto de calibração;
   - sensibilidade, especificidade, VPP e VPN;
   - decisão líquida;
   - gráfico de calibração por decis e taxa de captura no decil de maior risco.

   A calibração passou a ser feita sobre o posto do escore, e todos os modelos superam a previsão constante no Brier. No decil de maior risco, o escore concentra 46,3% das entradas em um ano, contra 62,4% da cobertura de juros. *Onde: §4.4, §6.7, Tabela 15 e Figura 5.*
7. **Múltiplas entradas.** Das 171 firmas com entrada, 149 têm uma e 22 têm duas ou mais. Cada reentrada é tratada como novo evento, e a sensibilidade só com a primeira entrada não muda o resultado. *Onde: §5.3 e Tabela A.5.*
8. **H4.** Está declarada como análise posterior, de caráter exploratório, inclusive no resumo, e o texto usa "a análise diagnóstica fornece evidência consistente com H4". *Onde: §4.5 e §6.6.*
9. **Mecanismo.** As três formulações apontadas foram substituídas pelas versões moderadas sugeridas, e o restante do texto segue o mesmo tom. *Onde: §6.5 e §6.6.*

## Parte II

- **0,730 e 0,735.** A divergência foi eliminada. O texto usa uma convenção única, a atribuição de referência, e as médias entre atribuições aparecem só onde a nota da tabela indica. *Onde: §4.4 e notas das tabelas.*
- **H1.** Agora está "parcialmente sustentada quanto à coerência do eixo e rejeitada quanto à unidimensionalidade". *Onde: §6.1.*
- **Uso do CP1.** Entraram os quatro argumentos sugeridos e a verificação com o segundo componente. *Onde: §6.1 e §6.8.*
- **Índice agregado.** Ficou apenas como agenda, sem compromisso e sem prometer viabilidade econométrica. *Onde: §7.2.*

## Outras mudanças desde a versão anterior

- **Panorama:** nova seção 2, com o panorama da dificuldade financeira das companhias abertas brasileiras de 2010 a 2025 (Figura 1 e Tabela 1).
- **Literatura:** a revisão foi reorganizada em dois pilares, não supervisionado e supervisionado (seção 3), e ganhou trabalhos recentes: 13 das 60 referências são de 2020 em diante.
- **Equações:** passaram para o editor de fórmulas.
- **Escore com três indicadores:** um escore só com os três indicadores de maior poder discriminante acompanha o melhor indicador isolado, sem superá-lo, o que reforça a leitura de composição (§6.6).
- **Dados conferidos com a CVM:** o painel foi conferido contra os arquivos originais da CVM. Saíram três emissores estrangeiros que deveriam ter sido excluídos, e quatro firma-anos com valores errados foram corrigidos. Nenhuma conclusão muda, e todas as tabelas conferem com o código.
- **Estrutura:** as tabelas de validação e robustez foram para o Apêndice A.
- **Resumo:** reescrito para ser acessível a quem não é da área, mantendo o registro de que a decomposição é análise exploratória posterior.
