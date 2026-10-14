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

A execução completa roda os dezessete scripts em poucos minutos e não requer acesso à rede. Foi
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

## Versão 3 (outubro de 2026)

A versão em uso é `envio/Artigo_Fragilidade_Financeira_v3.docx`, com o PDF em `artigo/`. Ela incorpora os pedidos do coorientador
(áudios de 13 e 14/10, transcritos em `coorientacao/`):
- seção 2 com o panorama;
- números na introdução;
- equações como objetos de fórmula;
- literatura em dois pilares;
- citações recentes.

Para gerar a v3 a partir da v2:

    python revisao/alteracoes_v3.py <pasta do executar.sh>      # monta alteracoes_v3.json com os números do script 17
    python revisao/aplicar_v3.py envio/Artigo_Fragilidade_Financeira_v2.docx revisao/alteracoes_v3.json envio/Artigo_Fragilidade_Financeira_v3.docx <pasta das imagens>
    python revisao/checar_estrutura.py envio/Artigo_Fragilidade_Financeira_v3.docx   # remissões, ordem de citação, referências
    python revisao/verificar_artigo.py <pasta do executar.sh> envio/Artigo_Fragilidade_Financeira_v3.docx

A conferência do painel contra os arquivos da CVM está em `dados/VERIFICACAO_FONTE_CVM.md`. O script é `revisao/conferir_cvm.py`.

## Versões anteriores e numeração das tabelas

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

As pendências de código, números e referências da revisão de setembro foram resolvidas
(ver `ESCRUTINIO_COMPLETO.md` na raiz do repositório). O enquadramento ficou com os dois horizontes
lado a lado, e a divisão entre corpo e apêndice foi feita. As duas decisões podem ser revistas pelo
orientador. Ficam em aberto:

1. **Correção completa do painel antes da submissão:** excluir os três emissores estrangeiros, corrigir quatro firma-anos e rodar tudo de novo, mantendo a atribuição às partições (ver `dados/VERIFICACAO_FONTE_CVM.md`).
2. **Segunda leva de citações recentes**, ainda em conferência.
3. **Formatação final**, conforme as normas do programa de mestrado.
4. **Retorno do orientador** sobre a estrutura.
5. **Itens pendentes da coorientação.** A revisão de literatura foi tratada a partir do áudio de 14/10; a
   proposta sobre as técnicas de avaliação aguarda a resposta do coorientador.
6. **Conferência visual das páginas dos editores.** As referências com DOI foram conferidas pelo
   registro do DOI (dados depositados pelos editores); as páginas em HTML recusam acesso
   automatizado. As cidades das editoras dos livros de Minsky não constam da fonte consultada.

## Expansão para a dissertação

A estratégia é artigo primeiro, dissertação por expansão, e o mapa está no quadro final da nota
de decisões. Cada item da agenda da subseção 6.2 do artigo corresponde a um capítulo.
