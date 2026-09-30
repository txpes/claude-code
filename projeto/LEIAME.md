# Indicador sintético de fragilidade financeira — pacote do projeto

Estado em 29 de setembro de 2026, após revisão integral. As versões revisadas do artigo, da nota e da planilha
(`*_revisado*`) trazem as correções como alterações controladas e são consistentes entre si e com o
código: um verificador automático (`revisao/verificar_artigo.py`) compara as 596 células numéricas das
tabelas do artigo com as saídas do código e não encontra divergência. Os originais foram mantidos.

## Como reproduzir

    cd codigo
    DADOS=../dados bash executar.sh

Com as versões usadas na revisão:

    pip install -r codigo/requirements.txt

A execução completa roda os dezesseis scripts em poucos minutos e não requer acesso à rede. Foi
testada em diretório limpo. As árvores impulsionadas dependem da versão do scikit-learn; com as
versões de `requirements.txt`, os números reproduzem os do artigo revisado.

## O que tem em cada pasta

| Pasta | Conteúdo |
|---|---|
| `artigo/` | Versão original (Word e PDF). Versões revisadas do artigo e da nota com alterações controladas (`*_revisado*.docx`) e com as alterações aceitas (`*_limpo*` / `*_limpa*`, em Word e PDF) |
| `tabelas/` | Planilha original e revisada (`Tabelas_Artigo_revisado.xlsx`), preenchida pelo código final |
| `codigo/` | Quinze scripts, o executor, `requirements.txt` e o leia-me com a ordem e as armadilhas |
| `dados/` | Painéis 2010–2025 já sem os emissores estrangeiros, mais os arquivos auxiliares e o relatório da fase de dados |
| `referencias/` | Planilha de conferência bibliográfica (48 entradas) e o registro do trabalho de verificação |
| `revisao/` | Scripts que aplicam as alterações controladas, geram a versão limpa, atualizam a planilha e verificam o artigo contra o código |

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
| Árvores impulsionadas | 0,897 |
| Cobertura de juros | 0,894 |
| Mínimos quadrados parciais | 0,875 |
| Retorno sobre ativos | 0,874 |

Decomposição por rota de deterioração, subconjuntos puros, horizonte de um ano: prejuízo
operacional 0,649 contra 0,973 da cobertura de juros; patrimônio negativo 0,816, sem diferença
distinguível das alternativas; recuperação judicial 0,828, também sem diferença distinguível.

A mensagem de encaminhamento ao orientador está em `CARTA_EDUARDO.md`.

## Versões do artigo e numeração das tabelas

Para regenerar o artigo a partir do original, rode os scripts de `revisao/` nesta ordem:

    python aplicar_revisao.py valores.json                      # original -> revisado, com alterações controladas
    python aceitar_alteracoes.py <revisado> <limpo_ordem_original>
    python montar_apendice.py artigo <limpo_ordem_original> <limpo>
    python verificar_artigo.py <pasta do executar.sh> <docx>     # células das tabelas contra o código

As duas versões do artigo numeram as tabelas de forma diferente:
- **Versão com alterações controladas:** mantém a ordem e a numeração originais, a mesma usada nos comentários do orientador, nos relatórios de revisão e nas abas da planilha.
- **Versão limpa:** é a estrutura final. Tem 14 tabelas no corpo, e as antigas 8, 9, 11, 18, 19 e 20 estão no Apêndice A (A.1 a A.6).

A correspondência completa está na aba `Numeracao_final` da planilha.

## O que permanece em aberto

Todas as pendências de dados, código, números e referências foram resolvidas na revisão
(ver `ESCRUTINIO_COMPLETO.md` na raiz do repositório). O enquadramento ficou com os dois horizontes
lado a lado, e a divisão entre corpo e apêndice foi feita. As duas decisões podem ser revistas pelo
orientador. Ficam em aberto:

1. **Formatação final**, conforme as normas do programa de mestrado.
2. **Retorno do orientador** sobre a estrutura.
3. **Itens pendentes da coorientação.** Os comentários sobre a revisão de literatura e as técnicas
   de avaliação da predição ainda não foram recebidos.
4. **Conferência visual das páginas dos editores.** As referências com DOI foram conferidas pelo
   registro do DOI (dados depositados pelos editores); as páginas em HTML recusam acesso
   automatizado. As cidades das editoras dos livros de Minsky não constam da fonte consultada.

## Expansão para a dissertação

A estratégia é artigo primeiro, dissertação por expansão, e o mapa está no quadro final da nota
de decisões. Cada item da agenda da subseção 6.2 do artigo corresponde a um capítulo.
