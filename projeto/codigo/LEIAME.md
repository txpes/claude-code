# Código de reprodução

Reproduz todos os números do artigo a partir dos painéis 2010–2025.

## Execução

    DADOS=/caminho/para/os/paineis bash executar.sh

O diretório deve conter `painel_completo.csv`, `painel_transicao.csv` e `painel_inputs.csv`, já
sem os emissores estrangeiros. O corte do esquema temporal é definido por `ANO_CORTE`, com
padrão no último ano de desfecho usado em treino.
Dependências: pandas, numpy, scipy, scikit-learn, statsmodels, matplotlib, openpyxl.

## Ordem e conteúdo

| Script | Produz | Tabelas e figuras |
|---|---|---|
| 01_pipeline_sem_vazamento.py | Predições fora da amostra, dez atribuições, dois horizontes | 9, 10 e estabilidade |
| 02_inferencia_bootstrap.py | Bootstrap agrupado por firma, Bonferroni, DeLong | 10 |
| 03_metricas_probabilidade.py | Calibração e limiares sobre predições fora de partições internas ao treino | 16 |
| 04_entradas_e_saidas.py | Múltiplas entradas e censura informativa | 18 |
| 05_robustez_e_calendario.py | Calendário, sobreviventes, especificações do escore, defasagens, setores | 18 e 19 |
| 06_consolidacao.py | Consolidação dos valores, escore intrafirma e Figura 2 | Figura 2 |
| 07_complementos.py | Validação minskyana e winsorização fora da amostra | 8 |
| 08_definicoes_de_evento.py | Definições alternativas do evento | 17 |
| 09_decomposicao_por_tipo.py | Decomposição por tipo de entrada, com intervalos | 13 e 14 |
| 10_corte_temporal.py | Avaliação temporal, separada pelo ano do desfecho | 11 |
| 11_tabelas_e_figuras.py | Estrutura fatorial, probit, descritivas, séries e Figuras 1, 2 e 4 | 3 a 7, 12, 16 |
| 12_concentracao.py | Concentração do poder discriminante por tipo de entrada, verificação exploratória | — |
| 13_puros_e_perfil.py | Subconjuntos puros, amplitude dos intervalos e perfil das firmas por rota | 14, 15 e Figura 3 |

## Princípio do desenho

Nenhuma estimativa utiliza informação das firmas de teste, inclusive as não supervisionadas.
Em cada partição, a padronização, a matriz de correlação e o autovetor da análise de
componentes principais, os quantis de winsorização do modelo de Brito e Assaf Neto e o
número de componentes do escore supervisionado são estimados apenas nas firmas de treino,
este último por validação cruzada aninhada. A calibração em probabilidade e os limiares
operacionais usam predições fora de partições internas ao treino, nunca os valores ajustados
do próprio modelo. No esquema temporal, a separação é feita pelo ano do desfecho, e os
parâmetros não supervisionados usam apenas exercícios anteriores ao corte.

## Convenção de apresentação

Os valores das tabelas derivam da atribuição de referência de firmas a partições; as médias
sobre dez atribuições aparecem na análise de estabilidade e na decomposição por tipo.
Diferenças são calculadas sobre valores não arredondados.

## Armadilhas documentadas

Escores construídos a partir da matriz padronizada seguem a ordem das linhas do painel:
junte por `CD_CVM` e `ano`, nunca por posição. O autovetor tem sinal arbitrário e é
normalizado para soma positiva das cargas. Filtros por último ano devem usar o último ano do
painel, e não uma data fixa.
