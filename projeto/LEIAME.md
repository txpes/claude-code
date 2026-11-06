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

A execução completa roda os dezoito scripts em poucos minutos e não requer acesso à rede. Foi
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
corrigida, e com os quinze emissores estrangeiros de recibos de depósito removidos (doze na extração original e três na
correção de outubro de 2026, com quatro firma-anos refeitos; ver `dados/VERIFICACAO_FONTE_CVM.md`). São 7.403
observações firma-ano, 727 companhias, 194 entradas em vulnerabilidade sobre 5.682 firma-anos de risco. Os arquivos que o Cowork gerou antes dessa exclusão não estão aqui, para não haver
duas versões circulando.

`relatorio_fase_dados.md` descreve a extensão do painel, a correção da detecção de recuperação
judicial e o levantamento de cobertura trimestral.

## Números de referência

Servem para conferir se a reprodução chegou ao mesmo lugar. Horizonte de um ano, validação
cruzada agrupada por firma, atribuição de referência.

| Modelo | Área sob a curva |
|---|---|
| Componentes principais | 0,763 |
| Árvores impulsionadas | 0,897 |
| Cobertura de juros | 0,894 |
| Mínimos quadrados parciais | 0,877 |
| Retorno sobre ativos | 0,874 |

Decomposição por rota de deterioração, subconjuntos puros, horizonte de um ano: prejuízo
operacional 0,647 contra 0,973 da cobertura de juros; patrimônio negativo 0,816, sem diferença
distinguível das alternativas; recuperação judicial 0,828, também sem diferença distinguível.

A mensagem de encaminhamento ao orientador está em `CARTA_EDUARDO.md`.

## Versão 6 (06/11/2026)

A versão em uso é `envio/Artigo_Fragilidade_Financeira_v6.docx`. É a v5 com o resumo e o abstract reescritos para leitores de fora da área, a pedido do coorientador (áudio de 06/11, em `coorientacao/`). Para regenerar: `python revisao/alteracoes_v6.py` e `python revisao/aplicar_v3.py envio/Artigo_Fragilidade_Financeira_v5.docx revisao/alteracoes_v6.json <saída>`.

## Versão 5 (20/10/2026)

A versão em uso é `envio/Artigo_Fragilidade_Financeira_v5.docx`, com o PDF em `artigo/`. Em relação à v4, ela acrescenta:
- o gráfico de calibração por decis (Figura 5) e a taxa de captura no decil de maior risco (§4.4 e §6.7), do script `codigo/18_calibracao_captura.py`;
- as páginas de Rolim et al. (2021).

O material de retorno aos orientadores está em `envio/Retorno_revisao_artigo.docx`, gerado de `envio/Retorno_revisao_artigo.md` por `revisao/md_para_docx.py`. Ele traz os pedidos e onde foram atendidos, a resposta ao orientador e as decisões sobre avaliação, periódico, formato e formatação.

Para regenerar: os mesmos passos da v4, com `python codigo/18_calibracao_captura.py` (incluído no `executar.sh`), `python revisao/alteracoes_v5.py <pasta do executar.sh>` e `revisao/alteracoes_v5.json` acrescentado ao fim da lista do `aplicar_v3.py`.

## Versão 4 (15/10/2026)

A versão em uso é `envio/Artigo_Fragilidade_Financeira_v4.docx`, com o PDF em `artigo/`. Ela é a v3 com o painel corrigido: os três emissores estrangeiros foram excluídos, quatro firma-anos foram refeitos com as demonstrações corretas da CVM e todos os números, tabelas e figuras vieram de uma nova execução. A versão traz também a segunda e a terceira levas de citações recentes: são 60 referências, 13 delas de 2020 em diante.

Para regenerar a v4:

    python dados/corrigir_painel_2026-10.py dados <pasta com dfp_cia_aberta_AAAA.zip>     # já aplicado aos painéis do repositório
    cd codigo && DADOS=../dados bash executar.sh
    python revisao/alteracoes_v3.py <pasta do executar.sh>
    python revisao/numeros_texto.py <execução v3> <dados v3> <execução v4> <dados v4> revisao/alteracoes_v4_numeros.json
    python revisao/aplicar_v3.py envio/Artigo_Fragilidade_Financeira_v2.docx revisao/alteracoes_v4_figuras.json,revisao/alteracoes_v3.json,revisao/alteracoes_v4_numeros.json,revisao/alteracoes_v4_manuais.json <saída> <pasta do executar.sh>
    python revisao/verificar_artigo.py <pasta do executar.sh> <saída> revisao/correcoes_celulas_v4.json
    python revisao/corrigir_celulas.py <saída> revisao/correcoes_celulas_v4.json envio/Artigo_Fragilidade_Financeira_v4.docx

O `numeros_texto.py` usa frases-modelo. Cada uma é preenchida com a execução antiga, precisa casar com o texto atual e é então trocada pela versão preenchida com a nova. Assim, todo número do texto corrido tem origem conferida no código.

## Versão 3 (outubro de 2026)

A v3 (`envio/Artigo_Fragilidade_Financeira_v3.docx`) incorporou os pedidos do coorientador
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

As decisões que estavam em aberto foram tomadas e estão registradas em `envio/Retorno_revisao_artigo.md`: técnicas de avaliação, periódico-alvo, formato e formatação. Restam:

1. **Retorno do orientador na reunião** e, depois dele, a versão curta para submissão (limite de 8.000 palavras), conforme o plano de corte.
2. **E-mail com pontos específicos do coorientador**, ainda não recebido.
3. **Título de Predebom et al. (2025):** conferir no navegador; a página recusa acesso automatizado.
4. **Modelo de formatação do programa**, para a dissertação.

## Expansão para a dissertação

A estratégia é artigo primeiro, dissertação por expansão, e o mapa está no quadro final da nota
de decisões. Cada item da agenda da subseção 6.2 do artigo corresponde a um capítulo.
