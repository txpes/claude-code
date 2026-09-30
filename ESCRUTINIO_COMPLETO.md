# Revisão completa do artigo: dados, código, números, metodologia, escrita e referências

*Objeto:* pacote `Projeto_Fragilidade.zip` (28/09/2026), copiado em `projeto/`.
*Método:* reexecutei os 13 scripts do zero, recalculei os números descritivos a partir dos CSV, li todo o código, cruzei cada número do texto com as tabelas, a planilha e a reprodução, e li o artigo e a nota do começo ao fim.

---

## 0. Resumo

**O núcleo empírico se sustenta.** Com os dados do pacote, o código reproduz as Tabelas 2 a 8, 10 a 16, 18 e 19 com três casas decimais, com uma única exceção menor (as árvores impulsionadas, ver 1.2). Nenhum erro encontrado muda a conclusão principal: o escore perde para a cobertura de juros e para o ROA no agregado, e a desvantagem se concentra na rota do prejuízo operacional.

Encontrei, porém, **problemas que um parecerista de periódico de ponta pegaria**. Por ordem de gravidade:

| # | Problema | Tipo | Muda conclusão? |
|---|---|---|---|
| 1 | O contraste da manchete (0,649 contra 0,973) é **majoritariamente mecânico**: as 66 entradas têm EBITDA negativo já em t, e a margem EBITDA isolada chega a 0,978. | Metodologia | Muda o enquadramento |
| 2 | "Calibração adequada em todos os modelos", mas o Brier de três modelos perde para a previsão constante. | Metodologia/texto | Não |
| 3 | Bug no código de saídas: data fixa de 2023 num painel que vai até 2025 (143 saídas em vez de 201). | Código | Não |
| 4 | O sinal do CP2 troca entre partições, então o 0,717 da soma CP1+CP2 não é bem definido. | Código | Não (0,706 ou 0,665) |
| 5 | Bonferroni por 7 no artigo e por 6 no código. | Inferência | Não |
| 6 | Na Tabela 9, o Brito e Assaf Neto dentro da amostra é estimado sem a winsorização declarada. | Código | Não |
| 7 | Uma dúzia de números velhos no texto (período 2010-2023, 47 contra 50, 3,59%, série por estado, correlações). | Texto | Não |
| 8 | "609 observações do último exercício" descreve errado a amostra de risco. | Texto | Não |
| 9 | O pacote não reproduz sozinho: o executor não roda 3 dos 13 scripts e usa o corte temporal errado; há caminhos fixos de outra máquina; a Figura 3 não tem código; as versões não estão fixadas. | Reprodutibilidade | Não |
| 10 | Imagens do .docx com extensão `.undefined`, o que pode fazer o Word acusar arquivo corrompido. | Arquivo | Não |
| 11 | A seção 5.9 afirma que a limitação da data de RJ "não afeta as conclusões" sem ter feito o teste. | Texto | Teste feito (seção 10): não muda a conclusão central, mas derruba um resultado secundário |
| 12 | O mecanismo novo está escrito com a certeza que o orientador pediu para moderar. | Escrita | Não |

**O que já apliquei** (seção 8): as correções dos itens 2 a 12 foram feitas no código e, como alterações controladas, numa cópia do artigo (`Artigo_Fragilidade_Financeira_revisado.docx`). O item 1 recebeu uma quantificação factual no texto, mas o **reenquadramento** do argumento é decisão sua (seção 9).

---

## 1. Reprodução (F1)

### 1.1 O que reproduz

Rodei `01` a `13` a partir dos CSV do pacote (Python 3.11, versões em `codigo/requirements.txt`).

| Tabela | Situação |
|---|---|
| 2, 3, 4, 5, 6, 7 (painel, descritivas, PCA) | ✅ exata |
| 8 (validação minskyana) | ✅ exata |
| 9 (dentro da amostra) | ✅ exata, mas a linha de Brito e Assaf Neto está errada no código (ver 3.5) |
| 10 (validação cruzada) | ✅ exata, exceto árvores em um ano (ver 1.2) e p ajustado (ver 5.3) |
| 11 (temporal) | ✅ (árvores: 0,911 contra 0,910; 0,708 contra 0,713) |
| 12 (probit) | ✅ exata |
| 13, 14, 15 (decomposição, puros, perfil) | ✅ exata (a nota da 15 está errada, ver 4) |
| 16 (diagnóstico) | ✅ exata |
| 17 (métricas) | ✅ exata (a interpretação está errada, ver 5.2) |
| 18, 19, 20 (robustez) | ✅ exata, exceto a linha de saídas da 19 (bug, ver 3.1) |

### 1.2 Árvores impulsionadas não reproduzem na terceira casa

| | Artigo e planilha | Reproduzido (scikit-learn 1.9.1) |
|---|---|---|
| AUC em um ano, referência | 0,900 | 0,897 |
| Diferença contra F | +0,136 [+0,090; +0,184] | +0,133 [+0,086; +0,181] |
| Diferença contra COB | 0,006 | 0,003 |

A causa é a versão da biblioteca: o `HistGradientBoostingClassifier` não garante resultados idênticos entre versões, e o pacote não fixava nenhuma. Nenhuma conclusão muda. **Recomendação:** rodar de novo com as versões de `requirements.txt` e atualizar as três células, ou manter e declarar a versão usada.

---

## 2. Dados (F2)

Recalculado direto dos CSV:

- Sem duplicatas firma-ano e sem valores ausentes nos oito indicadores. O período é 2010-2025.
- Tabela 2: 701 / 482 / 399 / 1.115 (15,0%) ✅.
- Tabela 3: todas as estatísticas conferem. **Texto errado:** a cobertura vai "até 583,3", mas o máximo é 575,6.
- Tabela 4: confere. **Texto errado:** diz "máxima 0,42", mas é 0,44 (LC-CG); diz "COB mais alta 0,22", mas é 0,21 (com ROA).
- Tabela 5: 871 + 194 + 50 = 1.115 ✅. **Texto errado:** fala em "47 censuradas"; são 50.
- Firmas por ano: 358 em 2010, máximo de 584 em 2023, 529 em 2025; média de 10,2 exercícios, mediana 9, e 237 firmas em todos os anos ✅.
- **Série por estado:** o texto diz "de 6,0% em 2010 a 23,0% em 2017, praticamente monotônica ao longo do período". Pelos dados, vai de **5,6% a 20,9%** (pico em 2017) e depois **cai** para cerca de 14%. O número é do painel antigo.
- **3,59%:** vem do painel 2010-2023 (`relatorio_fase_dados.md`). A frequência correta na amostra de estimação é 3,01%.
- **Amostra de risco:** o texto diz que ela resulta de excluir "as 609 observações do último exercício de cada firma". Está errado. A amostra de risco é definida no ano do evento: são as observações cuja firma estava saudável em t−1. Ficam fora dela 921 observações (permanência ou censura) e **803 sem exercício anterior saudável, das quais 689 são a primeira aparição da firma**. O "609" só fecha a conta porque as 194 entradas estão ao mesmo tempo no estado e no conjunto de risco.
- **Saídas:** 201 firmas têm a última observação antes de 2025, e não 143 (ver 3.1). O arquivo `saidas_2025.csv` traz o motivo do cadastro, que **não é usado** pelo código: fechamento voluntário 119, RJ 28, incorporação 22, falência ou liquidação 12, sem motivo 25, outros 7.

---

## 3. Código (F3)

### 3.1 Bug: saídas filtradas por ano fixo (`04_entradas_e_saidas.py`)
`saem = ult[ult < 2023]` foi escrito para o painel antigo. Com o painel até 2025, as firmas que saem em 2023 e 2024 são contadas como "permanecem". O próprio LEIAME do código alerta contra isso. **Corrigido** para `P.ano.max()`:

| | Antes | Depois |
|---|---|---|
| Firmas que saem | 143 | 201 |
| Vulneráveis na última observação (saem / ficam) | 32,2% / 16,0% | 31,8% / 14,4% |
| Saídas com sinal de distress | 46 | 65 |
| Saídas a partir do estado saudável | 6 | 9 |
| Sensibilidade (Tabela 19): obs. / entradas | 5.052 / 155 | 5.055 / 158 |
| Sensibilidade: F / PLS / COB / ROA | 0,767 / 0,878 / 0,895 / 0,876 | 0,771 / 0,880 / 0,896 / 0,877 |

A conclusão não muda.

### 3.2 Bug: sinal arbitrário do CP2 (`05_robustez_e_calendario.py`)
O autovetor do CP2 não tem o sinal fixado e troca entre as partições (+, +, −, −, −). O 0,717 mistura os dois sinais. **Corrigido** com uma referência de sinal fixa e os dois sinais reportados: **CP1+CP2 = 0,706; CP1−CP2 = 0,665**. Os dois ficam abaixo de 0,764, então o argumento da seção 5.1 se mantém.

### 3.3 Família de Bonferroni (`02_inferencia_bootstrap.py`)
O código monta uma família H2 com 6 comparações (COB, ROA, B&A, LC, ALV e árvores) e trata o PLS à parte (H4, m = 1). O artigo e a planilha multiplicam por 7. Valores corretos:
- COB em dois anos: **0,120** (não 0,140);
- B&A em dois anos: **0,690** (não 0,805);
- PLS: não ajustado, **<0,001**.

Observação: as árvores entram na família, embora a seção 3.5 diga que elas "não testam hipótese". O mais coerente seria uma família de 5 (as quatro métricas e B&A). Isso só reduziria os p ajustados.

### 3.4 Calibração (`03_metricas_probabilidade.py`)
A calibração é feita por logística linear sobre escores brutos com caudas longas (ROA de −1,69 a 0,65; COB de −82 a 576). Algumas observações extremas recebem probabilidade próxima de 1: no ROA, 13 observações acima de 0,5, sendo 12 delas não eventos. É isso que leva o Brier acima da referência. Teste feito:

| Modelo | Brier atual | Calibração logística sobre o posto | Isotônica | Referência constante |
|---|---|---|---|---|
| ROA | 0,0289 | **0,0260** | 0,0260 | 0,0287 |
| COB | 0,0280 | **0,0256** | 0,0254 | 0,0287 |
| F | 0,0285 | **0,0275** | 0,0275 | 0,0287 |

**Recomendação:** calibrar sobre o posto (ou por regressão isotônica) e refazer a Tabela 17. Deixei como decisão sua, porque muda uma tabela inteira. O texto corrigido já descreve honestamente o que a tabela atual mostra.

Além disso, o código calcula o intercepto, a especificidade, o VPN e a decisão líquida, que a seção 3.4 promete e a Tabela 17 não mostra. No horizonte de dois anos, que não aparece no artigo, a **inclinação da cobertura de juros é negativa (−0,67)**.

### 3.5 Tabela 9: Brito e Assaf Neto sem winsorização dentro da amostra (`11_tabelas_e_figuras.py`)
A seção 3.4 declara a winsorização nos percentis 1 e 99, e o código fora da amostra a aplica, mas o bloco "dentro da amostra" não aplica. Resultado implausível: 0,703 dentro da amostra contra 0,734 fora. **Corrigido:** passa a 0,810 com controles e 0,755 sem controles, com efeito de +0,054.

### 3.6 Reprodutibilidade do pacote
- `executar.sh` **não rodava 11, 12 e 13**, que produzem as Tabelas 3 a 7, 12, 14, 15 e 16, e usava corte temporal **2023** por padrão, contra 2021 no artigo. **Corrigido.**
- `12` e `13` liam de `/home/claude/dados2025/` e `/home/claude/pipeline/`, caminhos de outra máquina. **Corrigido** para `DADOS` e diretório relativo.
- **A Figura 3 não tinha código.** A imagem do Word não era reproduzível. **Acrescentado** ao `13` um gerador (`fig3_decomposicao.png`, cópia em `revisao/`) que reproduz a figura original: mesmas quatro séries, mesmo layout e mesmos valores. As únicas diferenças estão nas barras das árvores, pela versão da biblioteca (ver 1.2). Não é preciso trocar a imagem no Word.
- Versões não fixadas. **Criado** `requirements.txt`.
- A planilha tem as fórmulas de p ajustado com ×7. **Corrigido** em `Tabelas_Artigo_revisado.xlsx`.

### 3.7 Pontos menores de código (sem efeito, só registro)
- O p-valor do bootstrap é o de percentil (proporção da distribuição que cruza zero), e não um teste centrado sob H0. É prática comum; vale uma frase na nota da Tabela 10.
- No script `05`, o PLS com defasagens usa 3 componentes fixos, sem a validação aninhada.
- No script `07`, a definição de Ponzi (dois anos consecutivos) usa `shift(1)` sem verificar lacunas no painel (18 casos com lacuna).
- A calibração dos modelos supervisionados usa escores de treino fora da partição interna, mas os escores de teste vêm do modelo ajustado no treino completo. É uma pequena inconsistência de distribuição, comum na prática.

---

## 4. Consistência numérica (F4)

Divergências entre texto, tabelas e dados, com a correção aplicada no .docx revisado:

| Onde | Texto | Correto | Aplicado |
|---|---|---|---|
| §3.4 | prevalência "aproximadamente 3,5%" | aproximadamente 3% (2,95% na amostra comum) | ✅ |
| §3.4 e nota da Tab. 10 | "sete comparações" | seis (PLS à parte) | ✅ |
| Tab. 10 | p ajustado 0,140; 0,805; PLS <0,004 | 0,120; 0,690; <0,001 | ✅ |
| §3.6 | "149 entradas da amostra de estimação" | amostra **comum** | ✅ |
| §4.1 | "exercícios de 2010 a 2023" | 2010 a 2025 | ✅ |
| §4.1 | cobertura até 583,3 | 575,6 | ✅ |
| §4.2 | correlações 0,42 e 0,22 | 0,44 e 0,21 | ✅ |
| §4.3 | 47 censuradas | 50 | ✅ |
| §4.3 | 609 do "último exercício" | redação corrigida (921 + 803) | ✅ |
| §4.3 | 3,59% | 3,01% | ✅ |
| §4.3 | estado de 6,0% a 23,0% "ao longo do período" | 5,6% a 20,9%, até 2017 | ✅ |
| §5.1 e §5.8 | CP1+CP2 = 0,717 | 0,706 ou 0,665 | ✅ |
| Tab. 9 | B&A 0,788 / 0,703 / +0,085 | 0,810 / 0,755 / +0,054 | ✅ |
| §1 e §5.8 | saídas 143, 32,2%/16,0%, 46, 6 | 201, 31,8%/14,4%, 65, 9 | ✅ |
| Tab. 19 | linha de saídas | 5.055 / 158 / 0,771 / 0,880 / 0,896 / 0,877 | ✅ |
| §5.5 | "0,649" citado antes da Tab. 14 | convenção explicitada | ✅ |
| §5.5 | PL "0,816" | "exclusivamente por PL" (subconjunto puro) | ✅ |
| Tab. 15, nota | "apenas o critério indicado" | a coluna PL inclui entradas com outros critérios | ✅ |
| Tab. 16 | "EBITDA" | MEB | ✅ |
| Tab. 17 | "Firmas sinalizadas" | firma-anos | ✅ |
| §5.6 | GB − COB "0,006" | 0,003 na reprodução | ❌ depende de 1.2 |
| Nota | "PCA 0,858, o melhor" (PL) | o artigo diz empate; ajustar a nota | ❌ nota |

---

## 5. Metodologia (F5): o que um parecerista de periódico de ponta diria

### 5.1 O resultado da manchete é, em grande parte, mecânico ⚠️ o mais importante
No horizonte de um ano, a entrada por EBITDA exige EBITDA negativo em t e em t+1. Firmas fora do estado em t têm EBITDA ≥ 0 em t−1, então **todas as 66 entradas desse tipo têm EBITDA < 0 já em t**. Isso vale para só 4,6% dos não eventos.

- A **margem EBITDA isolada** alcança **0,978** nesse subconjunto, mais que a cobertura (0,973). A Tabela 13 do artigo não mostra essa coluna, embora o código a calcule.
- **Dentro** das observações com EBITDA < 0 em t, a cobertura cai para **0,591**, a margem para 0,528, o ROA para 0,435 e F para 0,402.
- A regra trivial "EBITDA < 0 em t" captura 58% de **todas** as entradas com 95% de especificidade.

Ou seja, o "0,649 contra 0,973" mede sobretudo quem enxerga o sinal de um componente do evento já observado. O argumento de composição continua válido **no horizonte de dois anos** (F = 0,377, invertido), mas ali a própria cobertura cai para 0,522, e a vantagem dela sobre F é de 0,145.

**O que foi feito:** acrescentei à seção 5.5 um parágrafo factual com esses números, e o resumo agora cita os dois horizontes.

**O que fica para você (seção 9):** reenquadrar o resumo, a introdução e a conclusão para que o **número de dois anos** seja a manchete da rota operacional, e acrescentar a coluna MEB à Tabela 13.

### 5.2 Calibração
Ver 3.4. O texto dizia "calibração adequada em todos os modelos" e foi corrigido. Para um periódico de ponta, recomendo:
- calibrar sobre o posto;
- mostrar a Tabela 17 nos dois horizontes;
- incluir intercepto, especificidade, VPN e a curva de decisão líquida, que já estão calculados.

### 5.3 Inferência
- Bonferroni: ver 3.3.
- O bootstrap agrupado mantém fixas as predições, como declarado. Um parecerista pode pedir o bootstrap com **reestimação** dentro de cada réplica, pelo menos para a comparação principal (F contra COB e PLS). É caro, mas é a forma de capturar a variância de estimação no mesmo intervalo. O artigo usa as dez atribuições para isso, o que é aceitável se dito com clareza.
- Os IC da decomposição (Tabela 14) não são corrigidos, como declarado. Mas essa é a **análise central** do artigo (§5.9: "que é a análise central"), e também **pós-resultado** (§3.5). Essa tensão precisa ser assumida no texto: o resultado central é exploratório.

### 5.4 Estrutura fatorial
- A **análise paralela de Horn** retém os mesmos 3 componentes do critério de Kaiser (autovalores 2,153 / 1,326 / 1,064 contra percentis 95 de 1,064 / 1,042 / 1,027). Foi acrescentada ao texto com as referências.
- Com **correlação de postos**, o CP1 explica 36,4%, e não 26,9%. As caudas achatam as correlações de Pearson. Isso reforça a frase sobre winsorização (§5.8: 26,9% → 31,6%) e sugere um PCA robusto como sensibilidade.

### 5.5 Outros pontos que um parecerista pode levantar
- **Tabela 11:** Brito e Assaf Neto supera F no esquema temporal (0,787 contra 0,744), invertendo a validação cruzada. Não era comentado; acrescentei uma frase.
- **Árvores contra cobertura em dois anos:** +0,071, p = 0,005. As árvores superam a cobertura isolada no horizonte longo, e o artigo só comenta um ano. Isso reforça o argumento de que a supervisão extrai algo além da razão isolada fora da rota mecânica.
- **RJ datada tarde** (30 firmas): o teste de antecipar essas entradas em um ano não foi feito, e a seção 5.9 afirmava o contrário. O texto foi corrigido; o teste fica para você.
- **Saídas:** o motivo do cadastro existe em `saidas_2025.csv` e não é usado. A sensibilidade de "risco competitivo" com o motivo real seria simples, por exemplo tratando falência, liquidação e RJ como evento.
- **Setores:** só dois setores têm 15 eventos ou mais. A frase "a ordenação mantém-se" é fraca como evidência de generalização; está bem qualificada.

---

## 6. Escrita (F6)

**Aplicado** (alterações controladas):
- As afirmações categóricas do mecanismo foram moderadas: "cego", "a razão é", "está nos dados", "desaparece por completo", "concentra-se inteiramente", "o mesmo fato". É o ponto 9 do orientador aplicado ao mecanismo novo.
- §2.4: a frase sobre DeLong, que contradizia a §3.4, foi corrigida, e o parágrafo "Há ainda uma lacuna…" foi movido para depois da sexta dimensão, restaurando a enumeração.
- §5.9: a limitação de saídas agora descreve o que o código faz (sem cadastro), e a limitação de RJ não afirma mais um teste inexistente.

**Não aplicado (sugestões):**
- **§6.2:** ainda apresenta o índice agregado como "extensão viável", enquanto a nota diz que ele foi "retirado". Sugiro manter só uma frase ou cortar.
- **Título:** "Duas rotas" contra três critérios (a RJ é a terceira). Funciona se a leitura for "operacional contra patrimonial", mas vale conferir.
- **Resumo:** para um periódico, faltam o número de dois anos na manchete (acrescentado parcialmente), a menção ao exploratório e a versão em inglês.
- **Vinte tabelas:** para o corpo, sugiro as Tabelas 6-7, 10, 11, 14, 15 e 17 (com a coluna MEB na 13, se ela ficar); o resto vai para o apêndice.
- **Terminologia:** "prejuízo operacional" e "EBITDA negativo" são usados como sinônimos, mas o critério é EBITDA, não lucro operacional. Sugiro "EBITDA negativo persistente" ou uma definição na primeira ocorrência.
- **"Significância inferior a um por mil"** (resumo e §1): é mais usual escrever "significativo a 0,1%" ou "p < 0,001".
- **Nota metodológica:** precisa ser atualizada para os números corrigidos (143 → 201; 0,717 → 0,706; ×7 → ×6; "o melhor" → empate; "retirado" contra a §6.2; a Tabela 17 não traz especificidade).

---

## 7. Referências (F7)

- Todas as 33 referências da lista são citadas e toda citação tem entrada ✅.
- A Portaria 882 ganhou seção, número e página do DOU (NBR 6023).
- `(HANLEY; MCNEIL)` foi corrigido para `McNEIL`, como na lista.
- **Referências de método acrescentadas** (todas conferidas no Crossref; dados em `revisao/novas_referencias.txt`):
  - Brier (1950), Cox (1958), Dunn (1961), Field e Welsh (2007), Friedman (2001), Horn (1965), Kaiser (1960), Peduzzi et al. (1996), Saito e Rehmsmeier (2015), Van Calster et al. (2019) e Vickers e Elkin (2006).
  - Ressalva: as **páginas de Friedman (1189-1232)** e o **número do artigo de Van Calster (230)** não constam no Crossref. Vieram do meu conhecimento; confira na página do editor.
- **Sugeridas, não inseridas**, porque exigem uma frase sua na seção 2.2: literatura recente de predição de insolvência, todas conferidas no Crossref:
  - Tian, Yu e Guo (2015), *Journal of Banking & Finance* 52, 89-100, sobre seleção de variáveis;
  - Jones, Johnstone e Wilson (2017), *Journal of Business Finance & Accounting* 44(1-2), 3-34, que comparam arcabouços estatísticos;
  - Veganzones e Séverin (2018), *Decision Support Systems* 112, 111-124, sobre baixa prevalência.

  Hoje a referência mais recente da lista é de 2019.

---

## 8. O que foi entregue

| Arquivo | O que é |
|---|---|
| `projeto/artigo/Artigo_Fragilidade_Financeira_revisado.docx` | O artigo com **103 alterações controladas** (revisão do Word, autor "Revisão"), para aceitar ou rejeitar uma a uma. Imagens corrigidas para .png. Validação estrutural: ids únicos, exclusões bem formadas, referências em ordem alfabética. Não consegui renderizar em PDF aqui (o LibreOffice do ambiente não abre nem um .txt); abra no Word e confira o layout. |
| `projeto/revisao/log_aplicacao.txt` | Cada alteração aplicada, com o motivo |
| `projeto/revisao/aplicar_revisao.py`, `tracked.py` | O script que aplica as alterações, para reaplicar se o original mudar |
| `projeto/codigo/` | Código corrigido: 04 (saídas), 05 (CP2), 11 (B&A), 12 e 13 (caminhos e Figura 3), `executar.sh` (13 scripts, corte 2021), `requirements.txt` |
| `projeto/tabelas/Tabelas_Artigo_revisado.xlsx` | Fórmulas de Bonferroni ×6 e PLS não ajustado |
| O original | Intocado em `projeto/artigo/Artigo_Fragilidade_Financeira.docx` |

O código corrigido foi reexecutado do zero, num diretório limpo, pelo `executar.sh`, e os números da tabela da seção 4 vêm dessa execução.

---

## 9. Decisões que ficam com você, por prioridade

1. **Reenquadrar o resultado central (5.1).** Tornar o horizonte de dois anos a manchete da rota operacional, tratar o de um ano como sobreposição mecânica e pôr a coluna MEB na Tabela 13. Sem isso, o parecerista escreve o parágrafo por você.
2. ~~Refazer a Tabela 17 com calibração sobre o posto~~ **Feito** (seção 10.1). Falta decidir se a versão completa, com os dois horizontes e todas as colunas (planilha, aba `T17_revisada`), substitui a do corpo ou vai para o apêndice.
3. ~~Rodar o teste da RJ atrasada~~ **Feito** (seção 10.2). Atualize também a nota metodológica: são 22 firmas no painel, e não 30.
4. **Decidir sobre as árvores (1.2):** regenerar com as versões fixadas ou declarar a versão usada.
5. **Figura 3:** agora é reproduzível. Se você regenerar as árvores (item 4), troque também a imagem.
6. **Assumir que a análise central é exploratória** (5.3), numa frase no resumo e na §3.5.
7. **Sensibilidade das saídas com o motivo do cadastro** (5.5).
8. **Seção 6.2 e nota metodológica** (seção 6).
9. **Divisão entre corpo e apêndice** e versão em inglês, se o alvo for internacional.

---

## 10. Rodadas complementares (29/09/2026)

### 10.1 Tabela 17 com calibração sobre o posto (novo script `14_metricas_calibradas.py`)

O desenho é o do script 03. A única mudança é a calibração: regressão logística sobre o posto do escore na distribuição do treino, em vez do escore bruto. A ordenação não muda.

| Um ano | PR-AUC | Brier | Inclinação | Intercepto | Especificidade* | VPP* | VPN* | Firma-anos sinalizados* | Decisão líquida 10:1 |
|---|---|---|---|---|---|---|---|---|---|
| Árvores | 0,230 | **0,0251** | 1,087 | −0,028 | 0,846 | 0,134 | 0,992 | 17,2% | +0,011 |
| Cobertura | 0,184 | **0,0256** | 0,988 | −0,004 | 0,831 | 0,124 | 0,992 | 18,7% | +0,009 |
| ROA | 0,175 | **0,0260** | 0,993 | −0,005 | 0,843 | 0,133 | 0,993 | 17,6% | +0,009 |
| PLS | 0,172 | **0,0260** | 1,072 | +0,007 | 0,810 | 0,113 | 0,992 | 20,8% | +0,008 |
| F | 0,111 | **0,0275** | 0,991 | −0,006 | 0,570 | 0,053 | 0,989 | 44,1% | +0,003 |
| Brito e Assaf | 0,095 | **0,0278** | 1,075 | +0,015 | 0,462 | 0,044 | 0,988 | 54,7% | +0,001 |
| Constante | 0,030 | 0,0287 | — | — | — | — | — | — | 0 |

\* No limiar que atinge sensibilidade de 80% no treino.

- **A contradição some.** Os seis modelos batem a previsão constante no Brier. As inclinações ficam entre 0,99 e 1,09, e o Brito e Assaf Neto sai de 0,738 para 1,075. A isotônica dá o mesmo Brier (checagem interna do script).
- **Horizonte de dois anos**, que o artigo não mostrava: todos os Brier ficam entre 0,0277 e 0,0283, contra 0,0285 da constante, e a **decisão líquida é praticamente zero em todos os modelos**. Nenhum modelo tem utilidade operacional a 10:1 em dois anos. É um achado que vale uma frase no texto (já incluída) e reforça a leitura de que a vantagem dos benchmarks em um ano vem, em boa parte, da sobreposição mecânica. A inclinação negativa da cobertura (−0,67 na calibração antiga) passa a 0,948.
- **Aplicado no artigo:** as células da Tabela 17, a nota, o método na §5.7 (com a referência Niculescu-Mizil e Caruana, 2005), a frase de calibração reescrita e especificidade, decisão líquida e horizonte de dois anos no texto. A tabela completa está na aba `T17_revisada` de `Tabelas_Artigo_revisado.xlsx`.
- A ordem das linhas da Tabela 17 no artigo seguia a PR-AUC. Com os valores novos, ROA (0,175) passa à frente do PLS (0,172). Não reordenei; troque as duas linhas se quiser manter o critério.

### 10.2 Sensibilidade à data da recuperação judicial (novo script `15_rj_antecipada.py`)

- **Quantas firmas:** no painel, **22** firmas têm o primeiro documento de RJ classificado como "andamento" (`rj_detectada_2025.csv`), e não 30, como dizem o LEIAME e a nota. As 3 firmas de "encerramento/conversão" não afetam a amostra; testei com e sem elas e o resultado é idêntico.
- **Como:** a RJ dessas firmas é antecipada em um ano, e estado, entrada e conjunto de risco são reconstruídos. A reconstrução **reproduz exatamente** os painéis originais quando nenhuma data é alterada, e o script verifica isso antes de rodar. Mudam 8 células de entrada; o total segue em 194.

| Um ano | Original | RJ antecipada |
|---|---|---|
| Amostra comum: obs. / entradas | 5.046 / 149 | 5.042 / 150 |
| F / COB / ROA / PLS | 0,764 / 0,894 / 0,874 / 0,875 | 0,765 / 0,887 / 0,867 / 0,872 |
| COB − F | +0,129 [+0,080; +0,181] | +0,122 [+0,072; +0,175] |
| Rota operacional (puras, 66): COB − F | +0,324 | +0,324 |
| PL puras: PLS − F | **−0,066 [−0,129; −0,003]** | **−0,055 [−0,118; +0,009]** |
| RJ puras: COB − F | +0,012 [−0,097; +0,117] (11) | −0,064 [−0,187; +0,063] (12) |
| Dois anos: COB − F, p Bonferroni | 0,120 | **0,048** |

- **Conclusão:** o resultado central não muda. Duas qualificações, ambas aplicadas no texto:
  1. A frase "o escore supera o supervisionado nas entradas por patrimônio negativo" **não resiste**: o intervalo passa a conter o zero. A §5.5 e a conclusão agora dizem isso.
  2. Em dois anos, a vantagem da cobertura sobre o escore **fica mais forte** e resiste ao Bonferroni.
- A §5.9 agora descreve o teste e o resultado, em vez de dizer que a sensibilidade não foi estimada.

### 10.3 Nota de execução
O `executar.sh` agora roda 15 scripts e limita as threads do OpenMP. Rodando em paralelo, os scripts disputam os núcleos e um que leva 22 segundos passou de 45 minutos.

---

## 11. Rodada final (29/09/2026): fechamento das pendências

### 11.1 O que foi feito

| Pendência | Resultado |
|---|---|
| Motivo da saída pelo cadastro (ponto 4 do orientador) | Composição das 201 saídas no texto (§5.8): fechamento voluntário 119, RJ 28, incorporação 22, falência ou liquidação 12, outros 7, sem motivo 13; 28 são só filtro amostral. Linha nova na Tabela 19: tratar como evento as 44 saídas por dificuldade (cadastro) dá F 0,762 e COB 0,889, e a conclusão não muda. A saída passa a ser tratada como **risco competitivo** (termo do orientador). Script 04, bloco E2 |
| Árvores com números de outra versão | Todas as ocorrências alinhadas à versão fixada: Tabelas 10, 11, 13 e 18; §5.3, §5.5 e §5.6 (0,897; 0,003 contra a cobertura); Figuras 2 e 3 regeneradas |
| Ponzi sem checar anos consecutivos | Corrigido (07 e 11). Tabela 8: 0,782 e 0,769, 2.254 firma-anos (30,4%); a queda continua em 0,013 |
| Coluna MEB na Tabela 13 | Inserida (0,978 na rota operacional em um ano), com a nota |
| Estabilidade prometida e ausente | A §3.4 remetia à §5.6 e os números não estavam em lugar nenhum. Agora estão na §5.3: F 0,763 (dp 0,002), PLS 0,874 (0,003), árvores 0,897 (0,004); B&A mais sensível (0,705 a 0,739) |
| Afirmações sobre a literatura | 20 obras conferidas na fonte; 13 correções (seção 10.2 do `REGISTRO_CONFERENCIA.md`). As mais importantes: Mantoan et al. dizem o **contrário** do que o texto afirmava; Torres Filho et al. (2008-2013, e não "após 2013"); Davis et al.; Zmijewski; zumbis (três anos, e não dois); CAPAG (regra, e não pesos); a winsorização do Brito e Assaf Neto não é "da implementação original" |
| Figuras 1, 2 e 4 | 1 e 4 idênticas ao código; 2 e 3 substituídas pelas do código, com a altura ajustada à proporção |
| Planilha | Todas as abas preenchidas pelo código final (`revisao/atualizar_planilha.py`); Tabela 17 substituída pela versão completa; nota duplicada removida |
| Nota de decisões | `Nota_Decisoes_Metodologicas_revisada.docx`, com 16 alterações controladas e um parágrafo que lista para o orientador as correções da revisão |
| Registro bibliográfico | Id 3 (Portaria) conferida no DOU; 12 referências novas; Friedman confirmado no Project Euclid e Van Calster no Europe PMC |
| §6.2 | Moderada: o índice agregado fica como agenda, sem compromisso |
| LEIAME do pacote | Atualizado para o estado final |

### 11.2 Como sei que não criamos lacunas novas
- **Código:** o pacote final roda do zero pelo `executar.sh`, com os 15 scripts, sem erro.
- **Tabelas:** `revisao/verificar_artigo.py` compara **584 células numéricas** das 20 tabelas do artigo revisado, com as alterações aceitas, contra as saídas do código final: **0 divergências**.
  - **Controle:** o mesmo verificador, rodado no artigo original, acusa exatamente as **50 células** corrigidas. O verificador não passa por construção.
- **Texto:** os números do texto corrido que não estão em tabela (intrafirma 0,689, winsorização 31,55% e 0,799, probit parcimonioso 0,332 e 0,348, pré e pós-pandemia, reentradas, série por estado) foram conferidos um a um contra o código. Uma varredura por 30 valores e expressões antigas no artigo e na nota não encontrou resíduo.
- **Referências:** 45 entradas em ordem alfabética, todas citadas no texto.
- **Arquivo:** ids das alterações únicos, exclusões bem formadas, sem imagens `.undefined`, e o arquivo abre na biblioteca de leitura de .docx.

### 11.3 O que continua fora do meu alcance
- ~~**PDF:** o LibreOffice deste ambiente não funciona.~~ Resolvido na seção 12: o PDF foi gerado e conferido página a página.
- **Páginas dos editores:** a conferência visual das páginas em HTML (Elsevier, Wiley, T&F, OUP) e as cidades das editoras dos livros de Minsky.
- **Decisões do autor:** o enquadramento do resultado central (horizonte de dois anos como manchete), a divisão entre corpo e apêndice e a versão em inglês.

---

## 12. Rodada de fechamento para envio ao orientador (29/09/2026)

### 12.1 Decisões menores aplicadas
Todas estão no `aplicar_revisao.py`, com registro no `log_aplicacao.txt`. O resultado foi 170 alterações aplicadas e 0 falhas.

| Decisão | Onde |
|---|---|
| Estatuto exploratório da decomposição explicitado no resumo | Resumo |
| "Significância inferior a um por mil" → "p < 0,001" (3 ocorrências) | §4 e §5 |
| Declarada uma vez a equivalência entre critério (b) e "prejuízo operacional" | §3.3 |
| Conclusão com os dois horizontes (0,649 × 0,973 em um ano; 0,377 × 0,522 em dois), coerente com o resumo e a introdução | §6.1 |
| Literatura recente de aprendizado de máquina (Jones, Johnstone e Wilson, 2017; Tian, Yu e Guo, 2015; Veganzones e Séverin, 2018), conferida na fonte | §2.2 e referências (48 entradas) |
| Classificação JEL, abstract e keywords em inglês | Abertura |
| Seção "Disponibilidade de dados e código" | Antes das referências |
| Larguras das colunas das Tabelas 13, 14 e 19, sem palavras quebradas nem intervalos em três linhas | Tabelas |

### 12.2 Versões limpas e PDF
- `revisao/aceitar_alteracoes.py` aceita todas as alterações controladas e gera:
  - `Artigo_Fragilidade_Financeira_revisado_limpo.docx`;
  - `Nota_Decisoes_Metodologicas_revisada_limpa.docx`.
- Os PDFs correspondentes (40 e 5 páginas) foram gerados com o LibreOffice depois da instalação do `libreoffice-writer`.
- A conferência visual das páginas encontrou dois problemas de layout, ambos corrigidos na etapa 14b:
  - cabeçalhos quebrados no meio da palavra;
  - intervalos da Tabela 14 em três linhas.
- A paginação final do periódico dependerá do template dele.

### 12.3 Checagens depois das mudanças
- `verificar_artigo.py` na versão limpa: 584 células conferidas, 0 divergências.
- Referências: 48 entradas, em ordem alfabética, todas citadas no texto.
- Comentários do orientador: os itens que estavam parciais em `REVISAO_COMENTARIOS_EDUARDO.md` (I.4, I.5, I.6, I.9, II.a, a observação sobre o índice agregado e III) foram conferidos no texto limpo e estão resolvidos.

### 12.4 Encaminhamento
- `projeto/CARTA_EDUARDO.md` traz um rascunho de mensagem ao orientador com:
  - a resposta a cada comentário;
  - as correções da revisão;
  - os ajustes menores;
  - três perguntas: manchete, corpo × apêndice (com proposta) e idioma.
- As três decisões continuam com o autor.

---

## 13. Decisões de estrutura (29/09/2026, com o de acordo do autor)

### 13.1 O que foi decidido
- **Manchete:** ficam os dois horizontes lado a lado, como já estavam no resumo, na introdução e na conclusão. Nenhuma mudança de texto.
- **Corpo e apêndice:** o corpo ficou com 14 tabelas e o Apêndice A com 6 (as antigas 8, 9, 11, 18, 19 e 20).
  - A proposta da carta listava apenas 8 tabelas no corpo e omitia as 5, 6 e 7.
  - Ela também mandava para o apêndice as Tabelas 12 (probit de H3), 15 (perfil que sustenta a explicação de composição) e 16 (diagnóstico de H4).
  - Essas três sustentam hipóteses ou o argumento central e ficaram no corpo, para que nenhuma subseção de resultado dependa só de tabela no apêndice.
- **Inglês:** fica para depois do de acordo do orientador com a estrutura.

### 13.2 Como foi feito
- **Script novo (`revisao/montar_apendice.py`):** opera sobre a versão limpa e faz três coisas:
  - move cada bloco (legenda, tabela e nota) para o Apêndice A, depois das referências, com quebra de página;
  - renumera as 45 menções do artigo num único padrão, para que nenhum número seja trocado duas vezes;
  - renumera as 11 menções da nota de decisões, inclusive "Tabelas 9 a 11" e "Tabelas 13 e 14".
- **Versão com alterações controladas:** mantém a ordem e a numeração originais, para comparação com o original e com os comentários do orientador.
- **Planilha:** a aba `Numeracao_final` traz a correspondência.

### 13.3 Lacunas que a mudança revelou e foram fechadas
- **Duas tabelas não eram citadas no texto:**
  - a antiga Tabela 8 (validação minskyana), que agora é citada na §5.2 como Tabela A.1;
  - a antiga Tabela 17 (métricas), que agora é citada na §5.7.
- **Pedido I.6 do orientador:** a Tabela 17 (14 na final) mostrava só PR-AUC, Brier, inclinação, sinalizadas e VPP.
  - Ganhou as colunas de especificidade e de decisão líquida a 10:1.
  - O VPN, quase constante (0,988 a 0,993), foi para a nota.
  - A carta dizia que a tabela tinha os dois horizontes e todas as métricas, o que não era verdade no artigo (a versão completa está na planilha). A carta foi corrigida.
- **Formatação das colunas inseridas (`tracked.py`):** a busca do formato não enxergava runs dentro de `w:ins`/`w:del`, e as colunas novas saíam em fonte maior. Foi corrigida.

### 13.4 Checagens
- Alterações controladas: 172 aplicadas, 0 falhas.
- `verificar_artigo.py`: **596 células, 0 divergências**, tanto na versão com alterações controladas quanto na final com apêndice. As 12 células a mais são as colunas novas da Tabela 14. A faixa do VPN citada na nota é conferida por asserção.
- **Menções:** todas as 20 tabelas são citadas no texto. A primeira menção segue a ordem de numeração no corpo (1 a 14) e no apêndice (A.1 a A.6). Não sobrou menção a um número antigo.
- **PDF:** 40 páginas, conferido nas páginas da Tabela 14, da §5.8 e do Apêndice (39 e 40), sem palavras quebradas.

---

## 14. Escore com os três indicadores de maior poder discriminante (30/09/2026)

- **Origem:** pergunta da coorientação, confirmada pelo autor: o escore usa os três indicadores de maior KS, retorno sobre ativos, cobertura de juros e margem EBITDA.
- **Script novo (`codigo/16_tres_indicadores.py`):** usa o mesmo pipeline sem vazamento do 01.
  - Os escores são o primeiro componente principal dos três (F3) e a média simples padronizada (M3).
  - Para testar se escolher o trio na amostra completa enviesa o resultado, o script refaz a escolha pelos três maiores KS dentro de cada partição de treino.
- **Resultados** (atribuição de referência, bootstrap agrupado por firma):
  - **Um ano:** F3 0,895 contra F 0,764 e COB 0,894. COB − F3 = −0,001 [−0,015; +0,015]. F3 supera o ROA por 0,021 e o PLS de oito indicadores por 0,019, com intervalos que excluem o zero.
  - **Dois anos:** F3 0,722 contra COB 0,681 (+0,040 [+0,018; +0,062]). Sem diferença do ROA (0,731) nem do PLS (0,725).
  - **Média simples (M3):** difere de F3 em no máximo 0,001.
  - **Escolha dentro do treino:** o mesmo trio aparece em 98 de 100 partições.
  - **Rotas puras:**
    - um ano: 0,958 (66), 0,784 (51) e 0,888 (11);
    - dois anos: 0,576 (52), 0,801 (46) e 0,798 (9).
- **Leitura:** agregados apenas os melhores componentes, o escore acompanha o melhor indicador isolado nos dois horizontes, sem superá-lo. Isso é consistente com a explicação de composição e não altera a conclusão central.
- **No artigo** (alterações controladas):
  - parágrafo novo no fim da §5.6;
  - frase de estatuto na §3.5 (análise posterior aos resultados);
  - frase na conclusão.
- **Checagens:**
  - o `verificar_artigo.py` confere os 10 valores do parágrafo contra o `tres_indicadores.pkl`;
  - tabelas: 596 células, 0 divergências;
  - alterações controladas: 179 aplicadas, 0 falhas.
- **Correção desta rodada:** a §5.3 e a introdução diziam que o esquema temporal "reproduz a ordenação" da validação cruzada. Agora dizem que ele reproduz o resultado central, e que a ordem entre os benchmarks muda.
