# Verificação da fonte: painel contra os dados abertos da CVM (14/10/2026)

**Objetivo.** Antes de usar o painel no panorama da nova seção 2, conferir se os valores do painel são os que a CVM publica.

**Fontes consultadas** (acesso em 14/10/2026):
- DFP de 2010 a 2025: <https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/>, arquivos `dfp_cia_aberta_AAAA.zip`;
- cadastro de companhias abertas: <https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv>;
- IPE: <https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/IPE/DADOS/>, consultado para conferir a detecção de recuperação judicial.

**Como foi feito.** O script `revisao/conferir_cvm.py` compara, para cada firma-ano do painel, cinco contas com o valor da CVM:
- ativo total;
- patrimônio líquido;
- receita líquida;
- resultado antes do resultado financeiro e dos tributos;
- lucro líquido.

A comparação usa a mesma origem de demonstração do painel (consolidada ou individual), o exercício "último", a versão mais recente e a escala (mil ou unidade). Os 16 anos foram conferidos.

## Resultado

| | Comparações | Iguais | Divergentes |
|---|---|---|---|
| Firma-anos do painel final | 37.015 | 36.999 (99,96%) | 16 |

As 16 divergências se explicam assim:

| Caso | Firma-anos | O que aconteceu | Efeito |
|---|---|---|---|
| Águas do Rio 1 e 4 SPE, 2021 | 2 | O arquivo de 2021 traz duas demonstrações dessas SPEs: uma especial, de 31/07/2021, e a anual, de 31/12/2021. O painel usou a de julho (pré-operacional, receita zero) | Primeiro ano das firmas, fora da amostra de risco, sem eventos. Afeta só o treino do PCA (2 de 7.419 observações) |
| Equatorial Pará, 2025 | 1 | A CVM tem hoje uma versão 2 da DFP, com lucro e EBIT cerca de 10 vezes menores. A versão 1, usada no painel, aparenta erro de escala da própria companhia | Último ano do painel, fora da amostra de estimação. Afeta só o treino do PCA |
| COSERN, 2010 | 1 | Receita líquida ausente no painel, presente na CVM | Uma célula |
| Bradsaúde 2023 e Automob 2023 | 3 | Falso alarme do comparador: a conta aparece duas vezes no arquivo. O valor do painel é um dos dois | Nenhum |

## Achado mais relevante: três emissores estrangeiros ficaram no painel

O texto (§4.1) diz que foram excluídos "doze emissores estrangeiros com recibos de depósito". A conferência encontrou mais três, com código CVM 80xxx e fora do cadastro de companhias abertas, que não foram excluídos:

| Emissor | Firma-anos | Na amostra de risco | Entradas |
|---|---|---|---|
| Aura Minerals Inc. | 7 (2019–2025) | 6 | 0 |
| G2D Investments, Ltd. | 6 (2020–2025) | 5 | 0 |
| Inter & Co, Inc. | 3 (2021–2023) | 2 | 0 |

O Inter & Co é uma holding financeira, o que contraria também a expressão "não financeiras".

**Sensibilidade.** Os modelos foram reestimados sem os três emissores (7.403 firma-anos; amostra comum de 5.037 e 4.288 observações; mesmas 149 e 126 entradas):

| | Um ano: referência | Um ano: média de 10 | Dois anos: média de 10 |
|---|---|---|---|
| Escore (F) | 0,764 → 0,764 | 0,763 → 0,764 | 0,627 → 0,628 |
| Cobertura de juros | 0,894 → 0,894 | 0,894 → 0,894 | 0,681 → 0,681 |
| ROA | 0,874 → 0,874 | 0,874 → 0,874 | 0,731 → 0,731 |
| PLS | 0,875 → 0,873 | 0,874 → 0,874 | 0,727 → 0,726 |
| Árvores | 0,897 → 0,903 | 0,897 → 0,900 | 0,755 → 0,757 |
| Brito e Assaf Neto | 0,735 → 0,716 | 0,725 → 0,725 | 0,666 → 0,662 |

- **Medidas sem estimação** (escore, cobertura, ROA): mudam no máximo 0,001.
- **Modelos estimados, na atribuição de referência:** mudam mais. Retirar firmas reembaralha a atribuição de todas as outras firmas às partições, e o efeito sai disso, e não dos dados. Nas médias de dez atribuições, a maior variação é 0,004.
- **Conclusão:** nenhuma muda.

## Recuperação judicial: conferência pontual

Os casos conhecidos estão na base, com o ano do primeiro documento:

| Companhia | Ano |
|---|---|
| Teka | 2012 |
| OGX (Óleo e Gás Participações) | 2013 |
| OSX | 2013 |
| Oi | 2016 |
| Saraiva | 2018 |
| Americanas | 2023 |
| Light | 2023 |

## Recomendação

1. **Agora:** usar o painel no panorama. A fonte confere em 99,96% das comparações, e os casos divergentes não afetam a amostra de estimação.
2. **Antes da submissão:**
   - excluir os três emissores estrangeiros;
   - corrigir os 4 firma-anos (Águas do Rio 2021, Equatorial Pará 2025 e COSERN 2010);
   - rodar de novo todo o código.

   Para que só o efeito dos dados apareça, a atribuição às partições deve ser feita sobre a lista original de firmas. Até lá, a §4.1 precisa dizer a verdade: a frase dos "doze emissores" deve ser ajustada.
