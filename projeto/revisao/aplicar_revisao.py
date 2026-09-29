"""Aplica ao artigo as correcoes da revisao, como alteracoes controladas.

Uso: python aplicar_revisao.py <valores.json>
O JSON traz os numeros reproduzidos pelo codigo corrigido (saidas, Tabela 9, Tabela 19).
Gera artigo/Artigo_Fragilidade_Financeira_revisado.docx e revisao/log_aplicacao.txt.
"""
import sys, json, os
import docx, docx.text.paragraph
from tracked import replace, insert_after, delete_paragraph, consertar_midia

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(AQUI, '..', 'artigo', 'Artigo_Fragilidade_Financeira.docx')
DST = os.path.join(AQUI, '..', 'artigo', 'Artigo_Fragilidade_Financeira_revisado.docx')
V = json.load(open(sys.argv[1]))
log = []

consertar_midia(SRC, DST)
d = docx.Document(DST)


def todos_paragrafos():
    for p in d.paragraphs:
        yield p
    for t in d.tables:
        for row in t.rows:
            for c in row.cells:
                for p in c.paragraphs:
                    yield p


def sub(old, new, motivo):
    achados = [p for p in todos_paragrafos() if old in p.text]
    # celulas mescladas repetem o mesmo paragrafo; deduplica pelo elemento
    vistos = []
    for p in achados:
        if all(p._p is not q._p for q in vistos):
            vistos.append(p)
    if len(vistos) != 1:
        log.append(f'FALHOU ({len(vistos)} ocorrencias): {old[:70]!r}')
        return
    ok = replace(vistos[0], old, new)
    log.append(('OK    ' if ok else 'FALHOU') + f' {motivo}: {old[:60]!r} -> {new[:60]!r}')


def celula(tabela_contem, linha_rotulo, col, old, new, motivo, apos=None):
    for t in d.tables:
        txt = ' '.join(c.text for r in t.rows for c in r.cells)
        if tabela_contem not in txt:
            continue
        ativo = apos is None
        for r in t.rows:
            if not ativo:
                ativo = r.cells[0].text.strip() == apos
                continue
            if r.cells[0].text.strip() == linha_rotulo:
                p = r.cells[col].paragraphs[0]
                if p.text.strip() != old:
                    log.append(f'FALHOU celula {linha_rotulo}[{col}]: esperado {old!r}, encontrado {p.text!r}')
                    return
                replace(p, old, new)
                log.append(f'OK     {motivo}: {linha_rotulo}[{col}] {old} -> {new}')
                return
    log.append(f'FALHOU celula nao encontrada: {tabela_contem[:30]} / {linha_rotulo}')


# ------------------------------------------------------------------ 1. numeros defasados no texto
sub('referentes aos exercícios de 2010 a 2023', 'referentes aos exercícios de 2010 a 2025', 'periodo do painel')
sub('a cobertura varia de menos 82,0 a 583,3', 'a cobertura varia de menos 82,0 a 575,6', 'maximo da cobertura (Tabela 3)')
sub('A correlação máxima é de 0,42', 'A correlação máxima é de 0,44', 'Tabela 4')
sub('sua correlação mais alta é de 0,22 com o retorno sobre ativos', 'sua correlação mais alta é de 0,21 com o retorno sobre ativos', 'Tabela 4')
sub('As 47 observações censuradas à esquerda', 'As 50 observações censuradas à esquerda', 'Tabela 5')
sub('ao passo que 3,59% é a frequência do evento', 'ao passo que 3,01% é a frequência do evento', 'Tabela 5 (3,59% era do painel 2010-2023)')
sub('a taxa cresce de forma praticamente monotônica ao longo do período, de 6,0% em 2010 a 23,0% em 2017',
    'a taxa cresce de forma praticamente monotônica até 2017, de 5,6% em 2010 a 20,9% em 2017', 'serie por estado recalculada')
sub('de aproximadamente 3,5%', 'de aproximadamente 3%', 'prevalencia (2,95% na amostra comum)')
sub('Das 149 entradas da amostra de estimação no horizonte de um ano', 'Das 149 entradas da amostra comum no horizonte de um ano', '149 e a amostra comum')
sub('A amostra de risco de 5.695 observações resulta da exclusão, a partir do painel de 7.419, das 1.115 observações em situação de vulnerabilidade e das 609 observações correspondentes ao último exercício disponível de cada firma, para as quais o desfecho em t + 1 não é observável.',
    'A amostra de risco reúne as 5.695 observações cuja firma estava fora do estado de vulnerabilidade no exercício anterior e que, portanto, podem registrar uma entrada. Ficam fora dela as 921 observações de permanência no estado ou censuradas à esquerda e as 803 observações sem exercício anterior saudável observado, das quais 689 correspondem à primeira aparição da firma no painel.',
    'composicao da amostra de risco (609 nao eram ultimos exercicios)')

# ------------------------------------------------------------------ 2. inferencia: familia de Bonferroni e DeLong na 2.4
sub('com o teste de DeLong, DeLong e Clarke-Pearson (1988) e correção para comparações múltiplas',
    'com inferência por bootstrap agrupado por firma e correção para comparações múltiplas', '2.4 contradizia a 3.4')
sub('considerando conjuntamente as sete comparações de cada horizonte',
    'considerando conjuntamente as seis comparações de cada horizonte contra os benchmarks e a referência não linear; a comparação com o escore supervisionado, que responde a H4, é tratada à parte',
    'familia de Bonferroni do codigo tem 6')
sub('p ajustado por Bonferroni para as sete comparações de cada horizonte',
    'p ajustado por Bonferroni para as seis comparações de cada horizonte contra benchmarks e referência não linear; a comparação com mínimos quadrados parciais responde a H4 e não é ajustada',
    'nota da Tabela 10')
celula('Horizonte de dois anos', 'Cobertura de juros', 5, '0,140', '0,120', 'Tabela 10, p ajustado x6', apos='Horizonte de dois anos')
celula('Horizonte de dois anos', 'Brito e Assaf Neto', 5, '0,805', '0,690', 'Tabela 10, p ajustado x6', apos='Horizonte de dois anos')
celula('Horizonte de dois anos', 'Mínimos quadrados parciais', 5, '<0,004', '<0,001', 'Tabela 10, PLS nao ajustado (H4)')
celula('Horizonte de dois anos', 'Mínimos quadrados parciais', 5, '<0,004', '<0,001', 'Tabela 10, PLS nao ajustado (H4)', apos='Horizonte de dois anos')

# ------------------------------------------------------------------ 3. CP1 + CP2 com sinal arbitrario
sub('em que a soma do primeiro e do segundo componentes reduz a área sob a curva fora da amostra de 0,764 para 0,717',
    f"em que a combinação do primeiro com o segundo componente, com qualquer dos dois sinais possíveis para este, reduz a área sob a curva fora da amostra de 0,764 para {V['cp1cp2']} ou {V['cp1mcp2']}",
    'sinal do CP2 trocava entre particoes')
sub('somar o segundo componente ao primeiro a reduz para 0,717',
    f"somar ou subtrair o segundo componente, cujo sinal é arbitrário, a reduz para {V['cp1cp2']} ou {V['cp1mcp2']}", 'idem, 5.8')

# ------------------------------------------------------------------ 4. Tabela 9: Brito e Assaf winsorizado tambem dentro da amostra
celula('Efeito dos controles', 'Brito e Assaf Neto', 1, '0,788', V['ba_com'], 'Tabela 9, BA winsorizado')
celula('Efeito dos controles', 'Brito e Assaf Neto', 2, '0,703', V['ba_sem'], 'Tabela 9, BA winsorizado')
celula('Efeito dos controles', 'Brito e Assaf Neto', 3, '+0,085', V['ba_efeito'], 'Tabela 9, BA winsorizado')

# ------------------------------------------------------------------ 5. saidas do painel (filtro por ultimo ano)
sub('entre as que saem, 32,2% estavam em situação de vulnerabilidade na última observação, contra 16,0% entre as que permanecem',
    f"entre as que saem, {V['vul_saem']} estavam em situação de vulnerabilidade na última observação, contra {V['vul_ficam']} entre as que permanecem",
    'introducao, saidas recalculadas')
sub('das 143 companhias que deixam o painel antes do fim do período, seja por cancelamento de registro, seja por interrupção da entrega das demonstrações, 32,2% estavam em vulnerabilidade na última observação, contra 16,0% entre as que permanecem, e 46 saídas apresentam sinal de dificuldade financeira. Dessas, 6 ocorrem a partir do estado saudável',
    f"das {V['n_saem']} companhias cuja última observação antecede 2025, {V['vul_saem']} estavam em vulnerabilidade na última observação, contra {V['vul_ficam']} entre as que permanecem, e {V['n_dist']} saídas apresentam sinal de dificuldade financeira, definido como recuperação judicial registrada ou vulnerabilidade em uma das duas últimas observações. Dessas, {V['n_cand']} ocorrem a partir do estado saudável",
    '5.8, saidas recalculadas')
for col, old, new in [(1, '5.052', V['t19_n']), (2, '155', V['t19_ev']), (3, '0,767', V['t19_F']), (4, '0,878', V['t19_PLS']),
                      (5, '0,895', V['t19_COB']), (6, '0,876', V['t19_ROA'])]:
    if old != new:
        celula('Somente a primeira entrada de cada firma', 'Saídas associadas a distress tratadas como evento', col, old, new, 'Tabela 19, saidas')
sub('O motivo da saída foi recuperado do cadastro de companhias abertas, mas a classificação de saídas associadas a dificuldade financeira permanece aproximada.',
    'A classificação de saídas associadas a dificuldade financeira é aproximada, construída a partir da recuperação judicial registrada e do estado de vulnerabilidade nas últimas observações; o motivo formal do cancelamento, disponível no cadastro de companhias abertas, não foi incorporado à análise.',
    '5.9: codigo nao usa o cadastro')

# ------------------------------------------------------------------ 6. calibracao e metricas operacionais
sub('a calibração é adequada em todos os modelos, com inclinações entre 0,968 e 1,016, à exceção do modelo de Brito e Assaf Neto, com 0,738.',
    'a calibração é adequada em todos os modelos, com inclinações entre 0,988 e 1,087 e interceptos próximos de zero, e todos superam a previsão constante no escore de Brier. A conversão é feita sobre o posto do escore, e não sobre o seu valor bruto, porque a regressão logística aplicada a indicadores de caudas longas, como o retorno sobre ativos e a cobertura de juros, atribui probabilidades extremas a poucas observações e degrada o escore de Brier: sobre os valores brutos, três dos seis modelos têm escore de Brier pior que o da previsão constante.',
    'Tabela 17 refeita com calibracao sobre o posto (script 14)')
sub('Cada escore é convertido em probabilidade por calibração logística estimada nas firmas de treino',
    'Cada escore é convertido em probabilidade por regressão logística sobre o seu posto na distribuição do treino (NICULESCU-MIZIL; CARUANA, 2005), estimada nas firmas de treino',
    'metodo de calibracao')
sub('com valor preditivo positivo de 0,053 contra 0,124.',
    'com valor preditivo positivo de 0,053 contra 0,124. No mesmo limiar, a especificidade é de 0,570 para o escore sintético e de 0,831 para a cobertura de juros, e a decisão líquida sob razão de custo de dez para um é positiva em todos os modelos, de 0,003 para o escore sintético a 0,011 para a referência não linear. No horizonte de dois anos, as métricas de probabilidade aproximam-se das da previsão constante e a decisão líquida é praticamente nula em todos os modelos, o que limita a utilidade operacional da previsão nesse horizonte.',
    'especificidade, decisao liquida e horizonte de dois anos')
sub('Inclinação de calibração com valor ideal unitário.',
    'Inclinação de calibração com valor ideal unitário. Probabilidades obtidas por regressão logística sobre o posto do escore na distribuição do treino.',
    'nota da Tabela 17')
T17 = [('Árvores impulsionadas', ['0,234','0,0265','1,016','17,2%','0,136'], ['0,230','0,0251','1,087','17,2%','0,134']),
       ('Cobertura de juros', ['0,215','0,0280','0,970','18,7%','0,124'], ['0,184','0,0256','0,988','18,7%','0,124']),
       ('Mínimos quadrados parciais', ['0,172','0,0288','1,005','20,8%','0,113'], ['0,172','0,0260','1,072','20,8%','0,113']),
       ('Retorno sobre ativos', ['0,171','0,0289','0,968','17,6%','0,133'], ['0,175','0,0260','0,993','17,6%','0,133']),
       ('Componentes principais (F)', ['0,110','0,0285','0,973','44,1%','0,053'], ['0,111','0,0275','0,991','44,1%','0,053']),
       ('Brito e Assaf Neto', ['0,077','0,0290','0,738','54,6%','0,044'], ['0,095','0,0278','1,075','54,7%','0,044'])]
for lin, velhos, novos in T17:
    for col, (a, b) in enumerate(zip(velhos, novos), start=1):
        if a != b:
            celula('AUC precisão-revocação', lin, col, a, b, 'Tabela 17, calibracao sobre o posto')
sub('a regra baseada no escore sintético sinaliza 44,1% das firmas', 'a regra baseada no escore sintético sinaliza 44,1% dos firma-anos', 'unidade e firma-ano')
sub('Firmas sinalizadas e valor preditivo positivo referem-se', 'Firma-anos sinalizados e valor preditivo positivo referem-se', 'nota da Tabela 17')
celula('AUC precisão-revocação', 'Modelo', 4, 'Firmas sinalizadas', 'Firma-anos sinalizados', 'cabecalho da Tabela 17')

# ------------------------------------------------------------------ 7. Tabela 15 e Tabela 16
sub('As duas primeiras colunas referem-se a entradas que satisfazem apenas o critério indicado.',
    'A primeira coluna refere-se às entradas que satisfazem apenas o critério de EBITDA; a segunda, a todas as entradas por patrimônio líquido negativo, inclusive as que também satisfazem outro critério.',
    'nota da Tabela 15 nao correspondia ao calculo')
celula('Variância entre firmas', 'EBITDA', 0, 'EBITDA', 'MEB', 'Tabela 16, sigla')

# ------------------------------------------------------------------ 8. 5.5: convencoes e sobreposicao mecanica
sub('o escore sintético fica muito atrás: 0,649 em um ano', 'o escore sintético fica muito atrás: na atribuição de referência, detalhada na Tabela 14, alcança 0,649 em um ano', 'convencao explicitada')
sub('Nas entradas por patrimônio líquido negativo, o escore alcança 0,816', 'Nas entradas exclusivamente por patrimônio líquido negativo, o escore alcança 0,816', '0,816 e do subconjunto puro')
sub('Ela não basta, porém, porque no horizonte de dois anos',
    'Seu peso é mensurável: as 66 entradas desse tipo têm EBITDA negativo já em t, condição que atinge apenas 4,6% dos não eventos, e a margem EBITDA isolada alcança 0,978 nesse subconjunto; restrita às observações com EBITDA negativo em t, a área sob a curva da cobertura de juros cai para 0,591. A explicação mecânica responde, portanto, pela maior parte do contraste no horizonte de um ano. Ela não basta, porém, porque no horizonte de dois anos',
    'quantifica a sobreposicao mecanica')

# ------------------------------------------------------------------ 9. calendario: RJ atrasada nao foi testada
sub('O tratamento conservador da subseção 5.8 mostra que a limitação não afeta as conclusões.',
    'O tratamento da subseção 5.8 cobre a antecipação por divulgação anterior às demonstrações de t. Para o eventual atraso da data registrada em relação ao ajuizamento, a recuperação judicial das 22 firmas do painel cujo primeiro documento trata do andamento do processo foi antecipada em um ano e os modelos foram reestimados. A área sob a curva passa a 0,765 para o escore sintético e a 0,887 para a cobertura de juros, e as conclusões agregadas e por rota de deterioração se mantêm, com duas qualificações: nas entradas exclusivamente por patrimônio líquido negativo, a vantagem do escore sintético sobre o supervisionado deixa de ser distinguível, e no horizonte de dois anos a diferença entre a cobertura de juros e o escore sintético passa a resistir à correção de Bonferroni.',
    '5.9: teste da RJ atrasada (script 15)')
sub('A única diferença significativa nesse tipo de entrada é contra o escore supervisionado, que o escore sintético supera por 0,066 ponto.',
    'A única diferença significativa nesse tipo de entrada é contra o escore supervisionado, que o escore sintético supera por 0,066 ponto, resultado que não resiste à antecipação das datas de recuperação judicial examinada na subseção 5.9.',
    '5.5: resultado fragil')
sub('e o escore supera o escore supervisionado nas primeiras.',
    'e o escore supera nominalmente o escore supervisionado nas primeiras, com diferença sensível à datação da recuperação judicial.',
    'conclusao: resultado fragil')

# ------------------------------------------------------------------ 10. esquema temporal: Brito e Assaf
sub('No horizonte de dois anos, com 34 entradas, nenhuma diferença alcança significância, e o esquema temporal é informativo apenas quanto à direção.',
    'No horizonte de dois anos, com 34 entradas, nenhuma diferença alcança significância, e o esquema temporal é informativo apenas quanto à direção. A exceção à ordenação é o modelo de Brito e Assaf Neto, que no esquema temporal supera o escore sintético, com 0,787 contra 0,744, ao contrário do que ocorre na validação cruzada.',
    'Tabela 11 mostrava inversao nao comentada')

# ------------------------------------------------------------------ 11. moderacao do mecanismo (ponto 9 do orientador)
sub('A razão é de composição:', 'Os dados são consistentes com uma explicação de composição:', 'resumo')
sub('Nas entradas por prejuízo operacional persistente o escore fica 0,32 ponto atrás da cobertura de juros;',
    'Nas entradas por prejuízo operacional persistente o escore fica 0,32 ponto atrás da cobertura de juros em um ano, contraste em que pesa a sobreposição mecânica entre o evento e os preditores, e 0,15 ponto atrás em dois anos;',
    'resumo: horizonte de dois anos e ressalva mecanica')
sub('O escore não é, portanto, uniformemente inferior: ele é cego a uma das rotas.',
    'O escore não é, portanto, uniformemente inferior: seu desempenho é fraco em uma das rotas.', 'introducao')
sub('A razão dessa cegueira é de composição, e é verificável nos dados.',
    'Os dados são consistentes com uma explicação de composição.', 'introducao')
sub('A segunda explicação é de composição, e é a que os dados sustentam:',
    'A segunda explicação é de composição, e os dados são consistentes com ela:', '5.5')
sub('A limitação não é de agregação em geral, e sim da composição deste escore: ele mede deterioração patrimonial e é cego à rota que começa no resultado operacional de firmas pouco endividadas.',
    'A limitação parece ser menos da agregação em geral do que da composição deste escore, que mede sobretudo deterioração patrimonial e tem desempenho fraco na rota que começa no resultado operacional de firmas pouco endividadas.', '5.5')
sub('o ganho concentra-se inteiramente nas entradas pelo critério de EBITDA e desaparece quando os modelos são reestimados sem elas',
    'o ganho concentra-se nas entradas pelo critério de EBITDA e deixa de ser distinguível quando os modelos são reestimados sem elas', '5.6')
sub('Retiradas as entradas por prejuízo operacional, a vantagem da agregação supervisionada desaparece por completo.',
    'Retiradas as entradas por prejuízo operacional, a vantagem da agregação supervisionada deixa de ser distinguível.', 'conclusao')
sub('A explicação é de composição e está nos dados.', 'Os dados são consistentes com uma explicação de composição.', 'conclusao')
sub('A limitação não é da agregação em geral, e sim da composição deste escore, que mede deterioração patrimonial e é cego à rota que começa no resultado operacional de firmas pouco endividadas.',
    'A limitação parece ser menos da agregação em geral do que da composição deste escore, que mede sobretudo deterioração patrimonial e tem desempenho fraco na rota que começa no resultado operacional de firmas pouco endividadas.', 'conclusao')
sub('a desvantagem do escore concentra-se inteiramente naquelas definidas por prejuízo operacional persistente: ali o escore alcança 0,649 contra 0,973 da cobertura de juros, diferença de 0,324 ponto',
    'a desvantagem do escore concentra-se naquelas definidas por prejuízo operacional persistente: ali o escore alcança 0,649 contra 0,973 da cobertura de juros em um ano, diferença de 0,324 ponto em boa parte mecânica, e 0,377 contra 0,522 em dois anos, horizonte em que a ordenação do escore se inverte',
    'introducao: moderacao e horizonte de dois anos')
sub('e a qual delas o escore é cego', 'e em qual delas o escore tem desempenho fraco', '5.1')
sub('revela se o indicador é uniformemente inferior ou apenas cego a uma das rotas', 'revela se o indicador é uniformemente inferior ou fraco em apenas uma das rotas', 'conclusao')
sub('são, assim, o mesmo fato observado de dois ângulos', 'são, assim, compatíveis com um mesmo fato observado de dois ângulos', 'conclusao')

# ------------------------------------------------------------------ 12. referencias de metodo no texto
sub('pelo número de componentes retidos pelo critério de Kaiser', 'pelo número de componentes retidos pelo critério de Kaiser (KAISER, 1960)', 'citacao')
sub('e o critério de Kaiser retém 3 componentes, que juntos explicam 56,80%.',
    'e o critério de Kaiser retém 3 componentes, que juntos explicam 56,80%. A análise paralela de Horn (1965), mais conservadora, retém o mesmo número.', 'Horn: 3 componentes')
sub('a área sob a curva de precisão e revocação, o escore de Brier, a inclinação e o intercepto de calibração',
    'a área sob a curva de precisão e revocação (SAITO; REHMSMEIER, 2015), o escore de Brier (BRIER, 1950), a inclinação e o intercepto de calibração (COX, 1958; VAN CALSTER et al., 2019)', 'citacoes')
sub('e a decisão líquida sob diferentes razões de custo', 'e a decisão líquida (VICKERS; ELKIN, 2006) sob diferentes razões de custo', 'citacao')
sub('é conduzida por bootstrap agrupado por firma, com 2.000 reamostragens', 'é conduzida por bootstrap agrupado por firma (FIELD; WELSH, 2007), com 2.000 reamostragens', 'citacao')
sub('A correção de Bonferroni é aplicada', 'A correção de Bonferroni (DUNN, 1961) é aplicada', 'citacao')
sub('a referência usual de ao menos dez eventos por parâmetro estimado', 'a referência usual de ao menos dez eventos por parâmetro estimado (PEDUZZI et al., 1996)', 'citacao')
sub('obtido por árvores impulsionadas com gradiente sobre as mesmas oito variáveis', 'obtido por árvores impulsionadas com gradiente (FRIEDMAN, 2001) sobre as mesmas oito variáveis', 'citacao')
sub('(HANLEY; MCNEIL, 1982)', '(HANLEY; McNEIL, 1982)', 'grafia igual a da lista')

# ------------------------------------------------------------------ 13. referencias: Portaria e novas entradas
sub('Diário Oficial da União, Brasília, DF, 20 dez. 2018.', 'Diário Oficial da União: seção 1, Brasília, DF, n. 244, p. 143, 20 dez. 2018.', 'NBR 6023, conferido no DOU')
NOVAS = [
 ('BRASIL', 'BRIER, G. W. Verification of forecasts expressed in terms of probability. Monthly Weather Review, v. 78, n. 1, p. 1-3, 1950.'),
 ('CAMPBELL', 'COX, D. R. Two further applications of a model for binary regression. Biometrika, v. 45, n. 3-4, p. 562-565, 1958.'),
 ('DU JARDIN', 'DUNN, O. J. Multiple comparisons among means. Journal of the American Statistical Association, v. 56, n. 293, p. 52-64, 1961.'),
 ('DUNN', 'FIELD, C. A.; WELSH, A. H. Bootstrapping clustered data. Journal of the Royal Statistical Society: Series B (Statistical Methodology), v. 69, n. 3, p. 369-390, 2007.'),
 ('FIELD', 'FRIEDMAN, J. H. Greedy function approximation: a gradient boosting machine. The Annals of Statistics, v. 29, n. 5, p. 1189-1232, 2001.'),
 ('HANLEY', 'HORN, J. L. A rationale and test for the number of factors in factor analysis. Psychometrika, v. 30, n. 2, p. 179-185, 1965.'),
 ('JOLLIFFE', 'KAISER, H. F. The application of electronic computers to factor analysis. Educational and Psychological Measurement, v. 20, n. 1, p. 141-151, 1960.'),
 ('MULLIGAN', 'NICULESCU-MIZIL, A.; CARUANA, R. Predicting good probabilities with supervised learning. In: INTERNATIONAL CONFERENCE ON MACHINE LEARNING, 22., 2005, Bonn. Proceedings [...]. New York: ACM, 2005. p. 625-632.'),
 ('OHLSON', 'PEDUZZI, P.; CONCATO, J.; KEMPER, E.; HOLFORD, T. R.; FEINSTEIN, A. R. A simulation study of the number of events per variable in logistic regression analysis. Journal of Clinical Epidemiology, v. 49, n. 12, p. 1373-1379, 1996.'),
 ('PEDUZZI', 'SAITO, T.; REHMSMEIER, M. The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. PLOS ONE, v. 10, n. 3, e0118432, 2015.'),
 ('TYMOIGNE, É. Measuring', 'VAN CALSTER, B.; McLERNON, D. J.; VAN SMEDEN, M.; WYNANTS, L.; STEYERBERG, E. W. Calibration: the Achilles heel of predictive analytics. BMC Medicine, v. 17, art. 230, 2019.'),
 ('VAN CALSTER', 'VICKERS, A. J.; ELKIN, E. B. Decision curve analysis: a novel method for evaluating prediction models. Medical Decision Making, v. 26, n. 6, p. 565-574, 2006.'),
]
ref_ini = max(i for i, p in enumerate(d.paragraphs) if p.text.strip() == 'Referências')
modelo = next(p for p in d.paragraphs[ref_ini:] if p.text.startswith('ALTMAN'))
inseridos = {}
for antes, texto in NOVAS:
    alvo = inseridos.get(antes) or next((p for p in d.paragraphs[ref_ini:] if p.text.startswith(antes)), None)
    if alvo is None:
        log.append(f'FALHOU referencia: ancora {antes!r} nao encontrada'); continue
    novo = insert_after(alvo, texto, modelo)
    inseridos[texto.split(',')[0]] = docx.text.paragraph.Paragraph(novo, alvo._parent)
    log.append(f'OK     referencia inserida: {texto[:50]}')

# ------------------------------------------------------------------ 14. 2.4: paragrafo fora de ordem
fora = next(p for p in d.paragraphs if p.text.startswith('Há ainda uma lacuna de avaliação'))
sexta = next(p for p in d.paragraphs if p.text.startswith('A sexta dimensão é a que organiza'))
texto = fora.text
delete_paragraph(fora)
insert_after(sexta, texto, sexta)
log.append('OK     2.4: paragrafo "Ha ainda uma lacuna" movido para depois da sexta dimensao')

d.save(DST)
open(os.path.join(AQUI, 'log_aplicacao.txt'), 'w').write('\n'.join(log) + '\n')
print('\n'.join(log))
print(f"\n{sum(l.startswith('OK') for l in log)} aplicadas, {sum(l.startswith('FALHOU') for l in log)} falhas")
