# Comentários do Eduardo × versão final do artigo

*Base:* pacote `Projeto_Fragilidade.zip` de 28/09/2026: artigo (.docx), tabelas (.xlsx), código e dados.
*Método:* li o artigo inteiro, cruzei os números do texto com as tabelas, conferi trechos do código e recalculei algumas contagens a partir de `dados/`.

---

## 1. Resposta curta

**Quase tudo o que o Eduardo pediu foi incorporado.** As mudanças mais pesadas estão feitas: PCA dentro da partição, validação minskyana sem cobertura de juros, subseção de calendário, bootstrap agrupado como inferência principal, múltiplas entradas, H1 com as duas afirmações separadas e justificativa do CP1.

Três pontos dele ficaram **pela metade**:
- as métricas de probabilidade (ponto 6);
- a moderação do mecanismo (ponto 9), que foi feita no mecanismo antigo mas não no novo;
- a harmonização de valores entre tabelas (Parte II).

Além disso, a reestruturação deixou **números velhos no texto** que não batem com as tabelas. Encontrei também um **problema substantivo novo, que ninguém apontou**: a Tabela 17 contradiz a frase "a calibração é adequada em todos os modelos".

---

## 2. Os comentários do Eduardo, item a item

| # | Comentário | Status | Onde está / o que falta |
|---|---|---|---|
| I.1 | PCA estimado dentro de cada partição | ✅ Feito | §3.4 (último parágrafo) e `01_pipeline_sem_vazamento.py`, `unsup_params(train_panel)`. Padronização, correlação, autovetor e quantis de winsorização vêm só do treino. |
| I.2 | Validação minskyana não independente | ✅ Feito | §5.2 e Tabela 8. A expressão foi trocada para "critério externo à variável dependente…" e o escore sem COB dá 0,770 contra 0,783. |
| I.3 | Calendário informacional | ✅ Feito | §3.6 completa: data de referência, divulgação, regra do mesmo ano civil e exposição mensurada (11 entradas só por RJ). Ver 3.8 abaixo sobre a limitação das datas de RJ. |
| I.4 | Saída ≠ só viés de sobrevivência | ⚠️ Parcial | §5.8 usa "censura informativa" e a Tabela 19 trata saídas por distress como evento. Faltam: **(a)** a tabela de motivos de saída que ele pediu, cujos dados já estão prontos em `saidas_2025.csv` (fechamento voluntário 119, RJ 28, incorporação 22, falência/liquidação 12, sem motivo 25, outros 7); **(b)** a expressão "riscos competitivos"; **(c)** os números da §5.8, que não reproduzi (ver 3.5). |
| I.5 | DeLong → bootstrap agrupado | ⚠️ Quase | §3.4 e Tabela 10 estão corretas. **Mas a §2.4 ainda diz** "testa-se a superioridade… com o teste de DeLong… e correção para comparações múltiplas". Isso contradiz a metodologia. |
| I.6 | PR-AUC, Brier, calibração, métricas operacionais | ⚠️ Parcial | A Tabela 17 existe, mas **não entrega o que a §3.4 promete**: faltam intercepto de calibração, sensibilidade, especificidade, VPN e decisão líquida. O código calcula tudo isso (`03_metricas_probabilidade.py`), e a decisão líquida 10:1 está até no .xlsx. Além disso, há a contradição do Brier (ver 3.1). |
| I.7 | Múltiplas entradas por firma | ✅ Feito | §4.3 (171 firmas; 149 com uma entrada e 22 com duas ou mais; conferi nos dados) e Tabela 19 (só a primeira entrada). |
| I.8 | H4 como análise diagnóstica | ✅ Feito | §3.5 declara o estatuto, e a §5.6 diz "evidência consistente com H4". Não sobrou nenhum "H4 é confirmada". |
| I.9 | Moderar o mecanismo | ⚠️ Deslocado | As três frases que ele citou sumiram, e a §5.6 ficou moderada. **Mas o artigo ganhou um mecanismo novo (composição/"cegueira") escrito exatamente no tom que ele criticou.** Ver 3.2. |
| II.a | 0,730 / 0,735 e convenções | ⚠️ Parcial | A convenção está declarada (§3.4, notas das Tabelas 13, 18 e 20), mas o texto da §5.5 mistura as duas convenções. Ver 3.4. |
| II.b | H1: eixo × unidimensionalidade | ✅ Feito | §3.5 e §5.1 usam a formulação que ele sugeriu. |
| II.c | Por que CP1 após rejeitar unidimensionalidade | ✅ Feito | §5.1, "Quatro razões…", segue o argumento dele quase literalmente. |
| Obs. | Cautela com o capítulo agregado/séries temporais | ⚠️ | A §6.2 agora diz que a extensão é "viável, e não apenas desejável", com base na cobertura trimestral. Ele recomendou não prometer. Para o artigo, eu cortaria esse parágrafo ou o reduziria a uma frase. |
| III | Harmonizar AUCs; moderar afirmações | ⚠️ | Ver 3.2 a 3.4. |

---

## 3. O que está passando

### Bloqueantes: um parecerista pega na primeira leitura

**3.1 A Tabela 17 contradiz o texto sobre calibração.**
O texto diz: "a calibração é adequada em todos os modelos, com inclinações entre 0,968 e 1,016". Mas o Brier de três modelos é **pior que o da previsão constante**:

| Modelo | Brier | Referência sem informação |
|---|---|---|
| PLS | 0,02885 | 0,02866 |
| ROA | 0,02892 | 0,02866 |
| Brito e Assaf Neto | 0,02902 | 0,02866 |
| F | 0,02851 | 0,02866 (quase empata) |

Um modelo com AUC de 0,87 e inclinação próxima de 1 que perde para a prevalência constante quase certamente tem **erro de calibração global (intercepto)**. É justamente o número que o código calcula e o artigo não publica.

- **Provável causa:** a prevalência do treino difere da do teste, e a calibração logística herda a do treino.
- **O que fazer:** publicar o intercepto, verificar a causa e reescrever a frase. Se a causa for a diferença de prevalência, isso também é um achado a relatar.

**3.2 O mecanismo novo está escrito com a certeza que o Eduardo pediu para tirar.**
Algumas frases da versão atual:
- "ele é cego a uma das rotas";
- "A razão dessa cegueira é de composição, e é verificável nos dados";
- "é a que os dados sustentam";
- "A explicação é de composição e está nos dados";
- "são, assim, o mesmo fato observado de dois ângulos";
- "desaparece por completo";
- "concentra-se inteiramente".

A evidência por trás delas são **medianas descritivas de 52 firmas** (Tabela 15), sem teste, numa análise que o próprio artigo declara pós-resultado e descritiva (§3.5). Pelo critério do Eduardo, isso deveria virar algo como: "os dados são consistentes com uma explicação de composição"; "o escore tem desempenho fraco nessa rota"; "a vantagem não é distinguível após…".

**3.3 A explicação mecânica foi descartada rápido demais, e é ela que produz o número da manchete.**
O resumo, a introdução e a conclusão abrem com "0,649 contra 0,973". Mas no horizonte de um ano o critério de EBITDA exige EBITDA negativo **já em t**. Cobertura, ROA e margem, que usam o resultado operacional de t, "veem" metade do evento, e o escore dominado por balanço não vê. O artigo descarta essa via com o horizonte de dois anos (F = 0,377), só que nesse horizonte:

- **a cobertura de juros cai para 0,522**, praticamente aleatória (Tabela 13);
- a vantagem dela sobre F cai de +0,324 para +0,145 (Tabela 14).

Ou seja, **a maior parte do contraste de um ano é compatível com a sobreposição mecânica**, e a parte que sobra em dois anos (F invertido) é a que sustenta a leitura de composição. Um parecerista vai perguntar isso.

A correção é de enquadramento, não de análise:
- apresentar o número de dois anos ao lado do de um ano no resumo e na conclusão;
- dizer explicitamente que o contraste de um ano mistura os dois efeitos.

O resultado continua interessante, e fica mais difícil de derrubar.

**3.4 Números velhos no texto que não batem com as tabelas.**

| Onde | Texto diz | Tabela / dados dizem |
|---|---|---|
| §4.1 | "exercícios de 2010 a 2023" | título, resumo e dados: 2010-2025 |
| §4.1 | cobertura "até 583,3" | Tabela 3: máximo 575,572 |
| §4.2 | "correlação máxima é de 0,42" (LC-CG) | Tabela 4: 0,44 |
| §4.2 | COB "mais alta 0,22 com ROA" | Tabela 4: 0,21 |
| §4.3 | "As 47 observações censuradas à esquerda" | Tabela 5: 50 |
| §4.3 | "3,59% é a frequência do evento na amostra" | Tabela 5: 153/5.086 = 3,01%. O 3,59% é do painel antigo 2010-2023 (`relatorio_fase_dados.md`). |
| §3.4 | prevalência "aproximadamente 3,5%" | §5.7: 2,95%; Tabela 5: 3,41% / 3,01% / 2,95% |
| §3.6 | "149 entradas da amostra de estimação" | 149 é a amostra **comum**; a de estimação tem 153 |
| §5.5 | "o escore alcança 0,649" logo após a Tabela 13 | Tabela 13 (média de 10 atribuições): 0,646. O 0,649 é da Tabela 14 (atribuição de referência), que só aparece depois. |
| §5.5 | PL: "o escore alcança 0,816" logo após a Tabela 13 | Tabela 13 (PL, não puro): 0,858. O 0,816 é o puro da Tabela 14. |
| Tabela 15 | "Entram por patrimônio negativo", 65 obs., nota: "apenas o critério indicado" | Tabela 14, puros PL em dois anos: **46**. 65 não bate com nenhuma das duas definições. |
| Tabela 14 | nota não diz qual convenção usa | pelos números, é a atribuição de referência; declarar |

**3.5 Números da saída do painel que não consegui reproduzir.**
A §5.8 fala em 143 companhias que saem, 32,2% contra 16,0%, 46 saídas com sinal de distress e 6 a partir do estado saudável. Recalculando a partir de `dados/`:

- 201 firmas têm a última observação antes de 2025;
- 31,8% contra 14,4% estão vulneráveis na última observação;
- `saidas_2025.csv` marca 44 como `distress_potencial`, e 8 delas estão saudáveis na última observação;
- a §4.3 diz que 609 últimos exercícios foram excluídos, mas há 590 firmas com última observação saudável.

Pode ser só diferença de definição (por exemplo, "sair" = cancelamento no cadastro, e não fim das DFPs). Mas precisa bater, e a definição precisa estar escrita.

**3.6 Resquício na §2.4.**
- A frase sobre DeLong (item I.5).
- O parágrafo "Há ainda uma lacuna de avaliação…" foi inserido **entre** "seis dimensões" e "As cinco primeiras…", o que quebra a enumeração. Ele precisa ir para depois da sexta dimensão.

### Importantes para um periódico de ponta

**3.7 A Tabela 11 (esquema temporal) tem um resultado que o texto ignora.**
Brito e Assaf Neto alcança **0,787 contra 0,744 do escore** no teste temporal, invertendo a ordem da validação cruzada (0,734 contra 0,764). O texto só comenta a ordenação dos demais modelos. Basta uma frase.

**3.8 A limitação de datas de RJ está afirmada como resolvida sem o teste.**
A §5.9 diz que "o tratamento conservador da subseção 5.8 mostra que a limitação não afeta as conclusões". Mas o teste da 5.8 trata da RJ divulgada **cedo demais**, antes das demonstrações de t. O problema das 30 firmas é o oposto: datas **atrasadas** em relação ao ajuizamento. O próprio LEIAME diz que o teste certo, antecipar essas 30 entradas em um ano e reestimar, ainda não foi feito. Ou se roda o teste, ou se retira a frase.

**3.9 Métodos usados sem referência.**
Não há referência para:
- critério de Kaiser (Kaiser, 1960);
- árvores impulsionadas (Friedman, 2001);
- Brier (1950);
- bootstrap agrupado (por exemplo, Field & Welsh, 2007, ou Cameron, Gelbach & Miller, 2008);
- calibração (Van Calster et al., 2019);
- decisão líquida (Vickers & Elkin, 2006);
- PR-AUC com baixa prevalência (Saito & Rehmsmeier, 2015);
- McFadden;
- Bonferroni.

Também faltam referências recentes de predição de insolvência (pós-2019). A lista de referências tem 33 entradas, todas de 2019 ou antes. Um parecerista de periódico de ponta nota as duas coisas.

**3.10 Vinte tabelas.**
O LEIAME já registra isso como pendência. Para submissão, o corpo do artigo ficaria com as Tabelas 6-7, 10, 11, 14, 15 e 17; o resto vai para um apêndice online.

**3.11 Winsorização melhora o escore em 0,035.**
Com winsorização, F sobe de 0,764 para 0,799 (§5.8). A escolha principal "sem winsorização" é defensável, mas a melhora não é pequena. Vale uma frase dizendo que ela não muda nenhuma conclusão, porque a distância para COB continua de cerca de 0,10.

### Menores

- A Tabela 16 usa "EBITDA" onde o resto do artigo usa "MEB" ou "Margem EBITDA".
- A citação "(HANLEY; MCNEIL, 1982)" deveria ser "McNEIL", como na lista de referências.
- A referência da Portaria 882 não traz "seção 1, n. 244, p. 143", como pede a NBR 6023 (conferido no DOU).
- `referencias/REGISTRO_CONFERENCIA.md` no pacote ainda trata a id 3 como pendente, embora a Portaria já esteja no artigo.
- Não há declaração de disponibilidade de dados e código, que a maioria dos periódicos exige.

---

## 4. Ordem sugerida

1. **Calibração (3.1):** publicar o intercepto, diagnosticar o Brier e completar a Tabela 17 com especificidade, VPN e decisão líquida.
2. **Enquadramento do resultado central (3.3 + 3.2):** dar peso igual a um e dois anos no resumo e na conclusão e moderar a linguagem do mecanismo de composição.
3. **Varredura de números (3.4 + 3.5):** um script que extraia cada número do texto e confira com as tabelas e os dados. Resolve 3.4 de uma vez e evita regressões.
4. **Saídas (I.4 + 3.5):** tabela de motivos de saída a partir de `saidas_2025.csv`, com definição explícita de "sair".
5. **RJ atrasada (3.8):** rodar o teste de antecipar as 30 entradas em um ano, ou retirar a frase.
6. Correções de texto: §2.4 (3.6), Tabela 11 (3.7), §6.2 (Obs.) e itens menores.
7. Referências de método (3.9) e divisão entre corpo e apêndice (3.10).

Os itens 3, 4 e 6 eu consigo fazer aqui, direto nos arquivos. Os itens 1 e 5 exigem reexecutar o código (cerca de 30 minutos, sem rede), o que também é possível neste ambiente.
