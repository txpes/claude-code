# Indicador sintético de fragilidade financeira — pacote do projeto

Estado em 28 de setembro de 2026. Tudo o que está aqui é consistente entre si: os números do
artigo, das tabelas e da nota vêm da mesma estimação, e o código reproduz essa estimação a
partir dos painéis incluídos.

## Como reproduzir

    cd codigo
    DADOS=../dados bash executar.sh

Se faltar alguma dependência:

    pip install pandas numpy scipy scikit-learn statsmodels matplotlib openpyxl

A execução completa leva cerca de trinta minutos e não requer acesso à rede. O pacote foi
testado a partir do zip extraído em diretório limpo, e os números reproduzem os do artigo.

## O que tem em cada pasta

| Pasta | Conteúdo |
|---|---|
| `artigo/` | Versão final, em Word e PDF, e a nota de decisões metodológicas |
| `tabelas/` | Planilha com 13 abas e as fórmulas das tabelas do artigo |
| `codigo/` | Treze scripts, o executor e o leia-me com a ordem e as armadilhas |
| `dados/` | Painéis 2010–2025 já sem os emissores estrangeiros, mais os arquivos auxiliares e o relatório da fase de dados |
| `referencias/` | Planilha de conferência bibliográfica e o registro do trabalho de verificação |

## Estado dos painéis

Os três painéis em `dados/` são os de 2010 a 2025, com a detecção de recuperação judicial já
corrigida, e com os doze emissores estrangeiros de recibos de depósito removidos. São 7.419
observações firma-ano, 730 companhias, 194 entradas em vulnerabilidade sobre 5.695 firma-anos
de risco. Os arquivos que o Cowork gerou antes dessa exclusão não estão aqui, para não haver
duas versões circulando.

`relatorio_fase_dados.md` descreve a extensão do painel, a correção da detecção de recuperação
judicial e o levantamento de cobertura trimestral.

## Números de referência

Servem para conferir se a reprodução chegou ao mesmo lugar. Horizonte de um ano, validação
cruzada agrupada por firma, atribuição de referência.

| Modelo | Área sob a curva |
|---|---|
| Componentes principais | 0,764 |
| Árvores impulsionadas | 0,900 |
| Cobertura de juros | 0,894 |
| Mínimos quadrados parciais | 0,875 |
| Retorno sobre ativos | 0,874 |

Decomposição por rota de deterioração, subconjuntos puros, horizonte de um ano: prejuízo
operacional 0,649 contra 0,973 da cobertura de juros; patrimônio negativo 0,816, sem diferença
distinguível das alternativas; recuperação judicial 0,828, também sem diferença distinguível.

## O que permanece em aberto

1. **Conferência manual de duas classes de referência.** Os metadados vieram do registro do
   DOI no Crossref, depositados pelos próprios editores, porque as páginas em HTML recusaram
   acesso automatizado. Restam duas verificações de olho: as páginas dos artigos com DOI e os
   catálogos da Columbia e da Yale para cidade e editora dos livros de Minsky. O detalhamento
   está em `referencias/REGISTRO_CONFERENCIA.md`.

2. **Sensibilidade das datas de recuperação judicial.** Em trinta firmas o primeiro documento
   entregue trata do andamento do processo, e não do pedido, de modo que a data registrada pode
   estar atrasada em relação ao ajuizamento. Está declarado como limitação na subseção 5.9. A
   verificação consiste em antecipar em um ano a entrada dessas firmas e reestimar.

3. **Separação entre corpo e apêndice.** São vinte tabelas, número alto para submissão a
   periódico. Para o corpo ficariam a estrutura fatorial, a comparação principal nos dois
   esquemas, a decomposição, os subconjuntos puros e o perfil das firmas.

4. **Itens pendentes da coorientação.** Os comentários sobre a revisão de literatura e a lista
   de técnicas de avaliação da predição ainda não foram recebidos.

## Expansão para a dissertação

A estratégia é artigo primeiro, dissertação por expansão, e o mapa está no quadro final da nota
de decisões. Cada item da agenda da subseção 6.2 do artigo corresponde a um capítulo.
