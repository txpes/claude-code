# Indicador sintético de fragilidade financeira — pacote do projeto

Estado em 29 de setembro de 2026, após revisão integral. As versões revisadas do artigo, da nota e da planilha
(`*_revisado*`) trazem as correções como alterações controladas e são consistentes entre si e com o
código: um verificador automático (`revisao/verificar_artigo.py`) compara as 584 células numéricas das
tabelas do artigo com as saídas do código e não encontra divergência. Os originais foram mantidos.

## Como reproduzir

    cd codigo
    DADOS=../dados bash executar.sh

Com as versões usadas na revisão:

    pip install -r codigo/requirements.txt

A execução completa roda os quinze scripts em poucos minutos e não requer acesso à rede. Foi
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

## O que permanece em aberto

Todas as pendências de dados, código, números e referências foram resolvidas na revisão
(ver `ESCRUTINIO_COMPLETO.md` na raiz do repositório). Restam decisões do autor:

1. **Enquadramento do resultado central.** No horizonte de um ano, o contraste na rota operacional é
   em boa parte mecânico; no de dois anos, a leitura de composição é a que se sustenta. O texto já
   traz os números e a ressalva; falta decidir se a manchete passa a ser o horizonte de dois anos.
2. **Separação entre corpo e apêndice.** São vinte tabelas; a proposta está em `CARTA_EDUARDO.md`.
   Versão em inglês, se o periódico-alvo for internacional (o abstract já está no artigo).
3. **Itens pendentes da coorientação.** Os comentários sobre a revisão de literatura e as técnicas
   de avaliação da predição ainda não foram recebidos.
4. **Conferência visual das páginas dos editores.** As referências com DOI foram conferidas pelo
   registro do DOI (dados depositados pelos editores); as páginas em HTML recusam acesso
   automatizado. As cidades das editoras dos livros de Minsky não constam da fonte consultada.

## Expansão para a dissertação

A estratégia é artigo primeiro, dissertação por expansão, e o mapa está no quadro final da nota
de decisões. Cada item da agenda da subseção 6.2 do artigo corresponde a um capítulo.
