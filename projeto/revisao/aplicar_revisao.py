"""Aplica ao artigo as correcoes da revisao, como alteracoes controladas.

Uso: python aplicar_revisao.py <valores.json>
O JSON traz os numeros reproduzidos pelo codigo corrigido (saidas, Tabela 9, Tabela 19).
Gera artigo/Artigo_Fragilidade_Financeira_revisado.docx e revisao/log_aplicacao.txt.
"""
import sys, json, os
import docx, docx.text.paragraph
from tracked import replace, insert_after, delete_paragraph, consertar_midia, insert_row_after, insert_column, insert_after_rotulado

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
sub('das 143 companhias que deixam o painel antes do fim do período, seja por cancelamento de registro, seja por interrupção da entrega das demonstrações, 32,2% estavam em vulnerabilidade na última observação, contra 16,0% entre as que permanecem, e 46 saídas apresentam sinal de dificuldade financeira. Dessas, 6 ocorrem a partir do estado saudável, sem desfecho observável, e a sensibilidade as trata como evento. A quinta restringe a amostra às firmas com registro ativo ao fim do período.',
    f"das {V['n_saem']} companhias cuja última observação antecede 2025, {V['vul_saem']} estavam em vulnerabilidade na última observação, contra {V['vul_ficam']} entre as que permanecem, e {V['n_dist']} saídas apresentam sinal de dificuldade financeira, definido como recuperação judicial registrada ou vulnerabilidade em uma das duas últimas observações. Dessas, {V['n_cand']} ocorrem a partir do estado saudável, sem desfecho observável, e a sensibilidade as trata como evento. A quinta linha usa, em lugar dessa classificação, o motivo do cancelamento no cadastro de companhias abertas. Por ele, as {V['n_saem']} saídas se dividem em fechamento voluntário de capital ({V['c_fech']}), recuperação judicial ({V['c_rj']}), incorporação ou reorganização ({V['c_inc']}), falência ou liquidação ({V['c_fal']}), cancelamento por outro motivo ({V['c_out']}) e motivo não identificado ({V['c_nid']}); {V['c_filtro']} delas decorrem apenas do filtro amostral, com o registro ainda ativo. As {V['c_dist']} saídas associadas a dificuldade financeira pelo cadastro, {V['c_dist_pct']} do total, incluem {V['c_cand']} ocorridas a partir do estado saudável, que a sensibilidade trata como evento. Como a saída por dificuldade financeira impede que se observe o desfecho que se pretende prever, ela constitui um risco competitivo, e as duas classificações levam à mesma conclusão. A sexta restringe a amostra às firmas com registro ativo ao fim do período.",
    '5.8, saidas recalculadas e motivo pelo cadastro (ponto 4 do orientador)')
linha19 = [row for t in d.tables if 'Somente a primeira entrada de cada firma' in ' '.join(c.text for r in t.rows for c in r.cells) for row in t.rows if row.cells[0].text.strip() == 'Saídas associadas a distress tratadas como evento']
if len(linha19) == 1:
    insert_row_after(linha19[0], ['Saídas por dificuldade financeira segundo o cadastro, como evento', V['t19b_n'], V['t19b_ev'], V['t19b_F'], V['t19b_PLS'], V['t19b_COB'], V['t19b_ROA']])
    log.append('OK     Tabela 19: linha nova, saidas pelo motivo do cadastro')
else:
    log.append(f'FALHOU Tabela 19: linha de saidas encontrada {len(linha19)} vezes')
sub('Fonte: elaboração própria. Horizonte de um ano, atribuição de referência, com todas as transformações estimadas nas firmas de treino.',
    'Fonte: elaboração própria. Horizonte de um ano, atribuição de referência, com todas as transformações estimadas nas firmas de treino. Na quarta linha, a saída associada a dificuldade financeira é identificada pela recuperação judicial registrada ou pela vulnerabilidade nas duas últimas observações; na quinta, pelo motivo do cancelamento no cadastro de companhias abertas.',
    'nota da Tabela 19')
for col, old, new in [(1, '5.052', V['t19_n']), (2, '155', V['t19_ev']), (3, '0,767', V['t19_F']), (4, '0,878', V['t19_PLS']),
                      (5, '0,895', V['t19_COB']), (6, '0,876', V['t19_ROA'])]:
    if old != new:
        celula('Somente a primeira entrada de cada firma', 'Saídas associadas a distress tratadas como evento', col, old, new, 'Tabela 19, saidas')
sub('O motivo da saída foi recuperado do cadastro de companhias abertas, mas a classificação de saídas associadas a dificuldade financeira permanece aproximada.',
    'A classificação de saídas associadas a dificuldade financeira é aproximada. As duas versões empregadas, uma pelo estado de vulnerabilidade e pela recuperação judicial registrada nas últimas observações, outra pelo motivo do cancelamento no cadastro de companhias abertas, levam à mesma conclusão, mas nenhuma identifica a data em que a dificuldade se instalou.',
    '5.9: saidas pelas duas classificacoes')

# ------------------------------------------------------------------ 6. calibracao e metricas operacionais
sub('A ordenação em precisão e revocação reproduz a da área sob a curva ROC, e a calibração é adequada em todos os modelos, com inclinações entre 0,968 e 1,016, à exceção do modelo de Brito e Assaf Neto, com 0,738.',
    'Na Tabela 17, a ordenação em precisão e revocação reproduz a da área sob a curva ROC, e a calibração é adequada em todos os modelos, com inclinações entre 0,988 e 1,087 e interceptos próximos de zero, e todos superam a previsão constante no escore de Brier. A conversão é feita sobre o posto do escore, e não sobre o seu valor bruto, porque a regressão logística aplicada a indicadores de caudas longas, como o retorno sobre ativos e a cobertura de juros, atribui probabilidades extremas a poucas observações e degrada o escore de Brier: sobre os valores brutos, três dos seis modelos têm escore de Brier pior que o da previsão constante.',
    'Tabela 17 refeita com calibracao sobre o posto (script 14); a tabela passa a ser citada no texto')
sub('Cada escore é convertido em probabilidade por calibração logística estimada nas firmas de treino',
    'Cada escore é convertido em probabilidade por regressão logística sobre o seu posto na distribuição do treino (NICULESCU-MIZIL; CARUANA, 2005), estimada nas firmas de treino',
    'metodo de calibracao')
sub('com valor preditivo positivo de 0,053 contra 0,124.',
    'com valor preditivo positivo de 0,053 contra 0,124. No mesmo limiar, a especificidade é de 0,570 para o escore sintético e de 0,831 para a cobertura de juros, e a decisão líquida sob razão de custo de dez para um é positiva em todos os modelos, de 0,003 para o escore sintético a 0,011 para a referência não linear. No horizonte de dois anos, as métricas de probabilidade aproximam-se das da previsão constante e a decisão líquida é praticamente nula em todos os modelos, o que limita a utilidade operacional da previsão nesse horizonte.',
    'especificidade, decisao liquida e horizonte de dois anos')
sub('Inclinação de calibração com valor ideal unitário.',
    'Inclinação de calibração com valor ideal unitário. Probabilidades obtidas por regressão logística sobre o posto do escore na distribuição do treino. Decisão líquida por firma-ano, sob razão de custo de dez para um; a de não sinalizar ninguém é zero. No mesmo limiar, o valor preditivo negativo fica entre 0,988 e 0,993 em todos os modelos. Modelos na ordem da área sob a curva ROC da Tabela 10.',
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
sub('Firmas sinalizadas e valor preditivo positivo referem-se', 'Firma-anos sinalizados, valor preditivo positivo e especificidade referem-se', 'nota da Tabela 17')
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

# ------------------------------------------------------------------ 11b. Ponzi com exercicios consecutivos (Tabela 8)
for lin, c8, c7, n8, n7 in [('Escore médio, posição Ponzi', '0,909', '0,874', V['pz8'], V['pz7']),
                            ('Escore médio, demais posições', '−0,400', '−0,384', V['np8'], V['np7']),
                            ('Estatística de Kolmogorov-Smirnov', '0,434', '0,416', V['ks8'], V['ks7']),
                            ('Área sob a curva para a posição Ponzi', '0,783', '0,770', V['auc8'], V['auc7'])]:
    if c8 != n8: celula('Escore sem cobertura de juros', lin, 1, c8, n8, 'Tabela 8, Ponzi com exercicios consecutivos')
    if c7 != n7: celula('Escore sem cobertura de juros', lin, 2, c7, n7, 'Tabela 8, Ponzi com exercicios consecutivos')
sub('abrangendo 2.265 firma-anos, ou 30,5% do painel', f"abrangendo {V['pz_n']} firma-anos, ou {V['pz_pct']} do painel", 'nota da Tabela 8')
sub('O escore médio das observações em posição Ponzi é de 0,909, contra −0,400 para as demais, e a área sob a curva para discriminar essa posição é de 0,783. Excluída a cobertura de juros, ela passa a 0,770.',
    f"O escore médio das observações em posição Ponzi é de {V['pz8']}, contra {V['np8']} para as demais, e a área sob a curva para discriminar essa posição é de {V['auc8']}. Excluída a cobertura de juros, ela passa a {V['auc7']}.", '5.2, Ponzi')
sub('com área sob a curva de 0,783, ou 0,770 quando excluído', f"com área sob a curva de {V['auc8']}, ou {V['auc7']} quando excluído", 'introducao, Ponzi')

# ------------------------------------------------------------------ 11c. arvores: valores reproduzidos com as versoes de requirements.txt
for lin, col, a, b, apos in [('Árvores impulsionadas', 1, '0,900', '0,897', None), ('Árvores impulsionadas', 2, '+0,136', '+0,133', None),
                             ('Árvores impulsionadas', 3, '[+0,090; +0,184]', '[+0,086; +0,181]', None),
                             ('Árvores impulsionadas', 1, '0,752', '0,753', 'Horizonte de dois anos'), ('Árvores impulsionadas', 2, '+0,125', '+0,126', 'Horizonte de dois anos'),
                             ('Árvores impulsionadas', 3, '[+0,060; +0,191]', '[+0,060; +0,192]', 'Horizonte de dois anos')]:
    celula('p DeLong', lin, col, a, b, 'Tabela 10, arvores (versao fixada)', apos=apos)
for col, a, b in [(1, '0,910', '0,911'), (2, '+0,166', '+0,167'), (4, '0,713', '0,708')]:
    celula('AUC, um ano', 'Árvores impulsionadas', col, a, b, 'Tabela 11, arvores (versao fixada)')
for lin, a, b in [('Somente por EBITDA negativo', '0,723', '0,719'), ('Patrimônio líquido negativo', '0,772', '0,771'),
                  ('Recuperação judicial', '0,849', '0,850'), ('Todas as entradas', '0,757', '0,755')]:
    celula('Somente por EBITDA negativo', lin, 3, a, b, 'Tabela 13, arvores (versao fixada)', apos='Horizonte de dois anos')
celula('Restritiva', 'Sem as entradas exclusivas do critério de EBITDA', 4, '0,858', '0,857', 'Tabela 18, arvores (versao fixada)')
celula('Restritiva', 'Restritiva: patrimônio líquido negativo ou recuperação judicial', 4, '0,955', '0,954', 'Tabela 18, arvores (versao fixada)')
sub('0,874 do retorno sobre ativos e 0,900 da referência não linear', '0,874 do retorno sobre ativos e 0,897 da referência não linear', '5.3, arvores')
sub('e a referência não linear 0,858, sem diferença', 'e a referência não linear 0,857, sem diferença', '5.5, arvores')
sub('as árvores impulsionadas alcançam 0,900, e a diferença para a cobertura de juros isolada, de 0,006 ponto,',
    'as árvores impulsionadas alcançam 0,897, e a diferença para a cobertura de juros isolada, de 0,003 ponto,', '5.6, arvores')

# ------------------------------------------------------------------ 11d. estabilidade entre as dez atribuicoes (prometida no texto e ausente)
sub('cujas médias e desvios-padrão são reportados na subseção 5.6', 'cujas médias e desvios-padrão são reportados na subseção 5.3', 'remissao corrigida')
sub('que ele supera por 0,030 ponto sem significância estatística.',
    f"que ele supera por 0,030 ponto sem significância estatística. Sob as dez atribuições aleatórias de firmas a partições, as médias praticamente coincidem com os valores da atribuição de referência: {V['st1_F_mu']} para o escore sintético, com desvio-padrão de {V['st1_F_sd']}, {V['st1_PLS_mu']} para o escore supervisionado ({V['st1_PLS_sd']}) e {V['st1_GB_mu']} para a referência não linear ({V['st1_GB_sd']}). O modelo de Brito e Assaf Neto é o mais sensível à atribuição, com média de {V['st1_BA_mu']} e amplitude de {V['st1_BA_min']} a {V['st1_BA_max']}, o que reforça a leitura de que sua diferença para o escore sintético não é distinguível.",
    'estabilidade reportada')

# ------------------------------------------------------------------ 11e. Tabela 13: coluna da margem EBITDA
MEB13 = {2: '0,978', 3: '0,689', 4: '0,780', 5: '0,824', 7: '0,618', 8: '0,678', 9: '0,724', 10: '0,654'}
t13 = [t for t in d.tables if 'Somente por EBITDA negativo' in ' '.join(c.text for r in t.rows for c in r.cells)]
if len(t13) == 1 and len(t13[0].columns) == 7:
    insert_column(t13[0], 6, 'MEB', lambda i, txt: MEB13.get(i, ''), largura_twips=1000)
    log.append('OK     Tabela 13: coluna MEB (margem EBITDA isolada)')
else:
    log.append(f'FALHOU Tabela 13: {len(t13)} tabelas encontradas')
sub('e não os da atribuição de referência.', 'e não os da atribuição de referência. A última coluna reporta a margem EBITDA isolada, cuja condição define o critério de prejuízo operacional.', 'nota da Tabela 13')

# ------------------------------------------------------------------ 11f. literatura: o que o texto afirma de cada obra, conferido na fonte
sub('e reporta que o porte, a estrutura de capital e a liquidez concentram o poder preditivo.',
    'e reporta que o porte, a estrutura de capital, o desempenho e a liquidez corrente são os fatores estatisticamente significativos.', 'Ohlson: quatro fatores')
sub('documenta que a amostragem por pareamento entre falidas e não falidas enviesa as estimativas, recomendando o uso de amostras que preservem a frequência populacional do evento.',
    'mostra que estimar esses modelos em amostras não aleatórias, com sobrerrepresentação das firmas em dificuldade ou selecionadas pela disponibilidade de dados, enviesa as estimativas de parâmetros e probabilidades, argumento que favorece amostras que preservem a frequência populacional do evento.',
    'Zmijewski: sobreamostragem e selecao, nao pareamento')
sub('quanto ao viés de amostragem por pareamento', 'quanto ao viés das amostras não aleatórias', 'Zmijewski, 2.4')
sub('comparam florestas aleatórias e máquinas de vetores de suporte com o discriminante clássico em amostra norte-americana e reportam ganho de aproximadamente dez pontos percentuais de acurácia.',
    'comparam técnicas de aprendizado de máquina, como bagging, boosting e florestas aleatórias, com modelos tradicionais em amostra de firmas norte-americanas e reportam ganho expressivo de acurácia fora da amostra.',
    'Barboza: numero nao confirmado na fonte')
sub('propõe classificação em dois estágios que melhora o desempenho em horizontes longos',
    'propõe classificação em dois estágios, baseada em perfis financeiros das firmas, que melhora as previsões quando combinada a técnicas de conjunto', 'du Jardin')
sub('constrói indicadores de fragilidade a partir de razões de fluxo de caixa e endividamento, com finalidade macroprudencial, e encontra deterioração sistemática das posições no período que antecede a crise de 2008.',
    'constrói indicadores de fragilidade para o financiamento imobiliário residencial, nos Estados Unidos e, no segundo trabalho, também no Reino Unido e na França, com finalidade macroprudencial, e encontra fragilidade elevada no setor residencial norte-americano a partir de 2004, no período que antecede a crise de 2008.',
    'Tymoigne: setor residencial')
sub('aplica a classificação em nível setorial na economia norte-americana e reporta migração generalizada de posições hedge para especulativas ao longo das expansões.',
    'aplica a classificação, definida pela cobertura de juros, a grupos setoriais da economia norte-americana e examina em que medida cada setor evolui de acordo com a hipótese de instabilidade financeira.',
    'Mulligan: achado nao confirmado na fonte')
sub('e mostram que a distribuição das firmas entre regimes varia sistematicamente ao longo do ciclo.',
    'e documentam crescimento expressivo da participação de firmas Ponzi a partir de 1970, concentrado nas companhias de menor porte.', 'Davis et al.')
sub('Nishi (2019) obtém resultado análogo para setores não financeiros japoneses.',
    'Nishi (2019) aplica a taxonomia aos setores não financeiros japoneses e encontra predominância da posição especulativa, com evolução distinta por setor e porte.', 'Nishi')
sub('empregando limiares absolutos de cobertura de juros, e documentam deterioração acentuada das posições após 2013.',
    'adaptando os indicadores e a taxonomia de Minsky aos dados contábeis regulatórios de mais de 60 firmas, e documentam aumento da fragilidade financeira ao longo do período, sobretudo entre 2008 e 2013.',
    'Torres Filho et al.: 2008-2013, nao apos 2013')
sub('investigam o comportamento financeiro das companhias não financeiras brasileiras na década de 2010 e associam a estagnação do investimento à fragilização das posições patrimoniais.',
    'investigam o comportamento financeiro das grandes companhias não financeiras brasileiras entre 2012 e 2019 e associam a estagnação do investimento a uma postura defensiva das firmas, que após a recessão de 2015-2016 reestruturaram o endividamento e elevaram a preferência pela liquidez.',
    'Mantoan et al.: postura defensiva')
sub('ambos documentando aumento da proporção de firmas assim classificadas após 2008.',
    'documentando aumento da proporção de firmas assim classificadas desde meados dos anos 2000, na amostra da OCDE, e desde o fim dos anos 1980, na do BIS.',
    'zumbis: periodos corretos')
sub('agrega três indicadores fiscais com pesos fixados de forma exógena para classificar entes subnacionais',
    'combina três indicadores fiscais, por meio de limiares e de uma regra de classificação fixados de forma exógena, para classificar entes subnacionais', 'CAPAG: regra, nao pesos')
sub('seguindo o critério absoluto adotado por Torres Filho, Martins e Miaguti (2019) e pela literatura de firmas zumbis.',
    'critério absoluto na linha da taxonomia de Minsky e próximo do adotado pela literatura de firmas zumbis, que exige cobertura inferior à unidade por três exercícios consecutivos.',
    '3.3: criterio Ponzi nao e o dos zumbis (3 anos)')
sub('as duas últimas winsorizadas por ano nos percentis 1 e 99, conforme a implementação original, com os quantis estimados exclusivamente nas firmas de treino.',
    'a primeira e a última winsorizadas por ano nos percentis 1 e 99, com os quantis estimados exclusivamente nas firmas de treino, tratamento ausente do trabalho original e adotado aqui para conter os valores extremos produzidos por denominadores próximos de zero.',
    'Brito e Assaf: winsorizacao nao e da implementacao original; variaveis corretas')

sub('o que a qualifica como extensão viável, e não apenas desejável.',
    'mas a viabilidade de um exercício econométrico com o índice agregado ainda depende de avaliação própria, anterior a qualquer compromisso com essa extensão.',
    '6.2: moderacao do indice agregado (recomendacao do orientador)')

# ------------------------------------------------------------------ 11g. apresentacao: exploratorio, p-valores, terminologia
sub('Uma análise diagnóstica posterior decompõe o evento pelo critério que o define',
    'Uma análise diagnóstica posterior, de caráter exploratório, decompõe o evento pelo critério que o define', 'resumo: estatuto exploratorio')
sub('antecipando a entrada com significância inferior a um por mil.', 'antecipando a entrada com p < 0,001.', 'p-valor')
sub('O coeficiente é positivo e significativo a menos de um por mil nos quatro modelos.', 'O coeficiente é positivo e significativo, com p < 0,001, nos quatro modelos.', 'p-valor')
sub('Os três são significativos a menos de um por mil,', 'Os três são significativos, com p < 0,001,', 'p-valor')
sub('A conversão de uma medida na outra é tratada na subseção 4.3, onde se apresenta a decomposição dos eventos e a construção da amostra de risco.',
    'A conversão de uma medida na outra é tratada na subseção 4.3, onde se apresenta a decomposição dos eventos e a construção da amostra de risco. No restante do texto, o critério (b) é também designado como prejuízo operacional persistente, e as entradas que o satisfazem, como entradas por prejuízo operacional; a denominação refere-se ao resultado antes de juros, impostos, depreciação e amortização, e não ao lucro operacional contábil.',
    'terminologia: prejuizo operacional = criterio (b)')

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
 ('JOLLIFFE', 'JONES, S.; JOHNSTONE, D.; WILSON, R. Predicting corporate bankruptcy: an evaluation of alternative statistical frameworks. Journal of Business Finance & Accounting, v. 44, n. 1-2, p. 3-34, 2017.'),
 ('SCALZER', 'TIAN, S.; YU, Y.; GUO, H. Variable selection and corporate bankruptcy forecasts. Journal of Banking & Finance, v. 52, p. 89-100, 2015.'),
 ('VAN CALSTER', 'VICKERS, A. J.; ELKIN, E. B. Decision curve analysis: a novel method for evaluating prediction models. Medical Decision Making, v. 26, n. 6, p. 565-574, 2006.'),
 ('VAN CALSTER', 'VEGANZONES, D.; SÉVERIN, E. An investigation of bankruptcy prediction in imbalanced datasets. Decision Support Systems, v. 112, p. 111-124, 2018.'),
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

sub('com 0,649 contra 0,973 da cobertura de juros.',
    'com 0,649 contra 0,973 da cobertura de juros em um ano, contraste em boa parte mecânico, e 0,377 contra 0,522 em dois anos, horizonte em que a ordenação do escore se inverte.',
    'conclusao: horizonte de dois anos, coerente com resumo e introducao')

sub('e Mai et al. (2019) incorporam informação textual das divulgações corporativas.',
    'e Mai et al. (2019) incorporam informação textual das divulgações corporativas. Jones, Johnstone e Wilson (2017), comparando dezesseis classificadores, concluem que modelos simples como o logit têm desempenho razoável, mas que métodos de conjunto como boosting e florestas aleatórias os superam; Tian, Yu e Guo (2015) mostram, por seleção de variáveis, que razões construídas apenas com dados contábeis carregam informação incremental sobre o risco de falência; e Veganzones e Séverin (2018) documentam que o forte desbalanceamento entre firmas em dificuldade e saudáveis degrada o desempenho dos classificadores, ponto que motiva as métricas sensíveis à prevalência da subseção 5.7.',
    'literatura recente (2015-2018), conferida na fonte')

# ------------------------------------------------------------------ 13b. JEL, abstract em ingles e disponibilidade de dados
pk = next(p for p in d.paragraphs if p.text.startswith('Palavras-chave:'))
resumo_tit = next(p for p in d.paragraphs if p.text.strip() == 'Resumo')
resumo_txt = next(p for p in d.paragraphs if p.text.startswith('Examina-se se a agregação'))
ABSTRACT = ('This paper examines whether aggregating accounting indicators into a synthetic financial fragility score is justified relative to its best '
            'individual components, using a panel of 7,419 firm-year observations from 730 Brazilian non-financial listed companies between 2010 and 2025. '
            'Over the pooled set of events, aggregation is not justified: the area under the ROC curve of the score is 0.764, against 0.894 for interest '
            'coverage and 0.874 for return on assets, a conclusion that holds under firm-clustered cross-validation and under temporal evaluation. A '
            'subsequent, exploratory diagnostic analysis decomposes the event by the criterion that defines it and shows that the aggregate result is '
            'produced by one of the deterioration routes. For entries through persistent operating losses, the score trails interest coverage by 0.32 '
            'points at one year, a contrast in which the mechanical overlap between the event and the predictors weighs, and by 0.15 points at two years; '
            'for entries through negative equity and judicial reorganization, the differences are not statistically distinguishable. The data are '
            'consistent with a composition explanation: firms heading toward operating losses show, at the time of prediction, lower leverage and higher '
            'liquidity than average, and a score dominated by balance-sheet structure classifies them as robust. The conclusion about aggregation '
            'therefore depends on the deterioration route one seeks to anticipate.')
insert_after_rotulado(pk, 'Keywords: ', 'Financial fragility; Synthetic indicator; Principal components; Financial vulnerability; Listed companies.', pk)
insert_after(pk, ABSTRACT, resumo_txt)
insert_after(pk, 'Abstract', resumo_tit)
insert_after_rotulado(pk, 'Classificação JEL: ', 'G33; G32; C38; C53; E12.', pk)
log.append('OK     JEL, abstract e keywords inseridos')
ult = next(p for p in d.paragraphs if p.text.startswith('A agregação do escore em índice setorial'))
refs_tit = next(p for p in d.paragraphs if p.text.strip() == 'Referências')
insert_after(ult, 'Os painéis foram construídos a partir dos dados abertos da Comissão de Valores Mobiliários: Demonstrações Financeiras Padronizadas, '
             'documentos periódicos e eventuais e cadastro de companhias abertas. Os painéis construídos, o código que reproduz todas as tabelas e figuras '
             'e a lista das versões das bibliotecas utilizadas estão disponíveis com o autor.', ult)
insert_after(ult, 'Disponibilidade de dados e código', refs_tit)
log.append('OK     secao de disponibilidade de dados e codigo')

# ------------------------------------------------------------------ 14. 2.4: paragrafo fora de ordem
fora = next(p for p in d.paragraphs if p.text.startswith('Há ainda uma lacuna de avaliação'))
sexta = next(p for p in d.paragraphs if p.text.startswith('A sexta dimensão é a que organiza'))
texto = fora.text
delete_paragraph(fora)
insert_after(sexta, texto, sexta)
log.append('OK     2.4: paragrafo "Ha ainda uma lacuna" movido para depois da sexta dimensao')

# ------------------------------------------------------------------ 14b. larguras de colunas (palavras quebradas no meio e intervalos em tres linhas)
from docx.oxml.ns import qn as _qn
def larguras(contem, novas, motivo):
    ts = [t for t in d.tables if contem in ' '.join(c.text for r in t.rows for c in r.cells)]
    if len(ts) != 1: log.append(f'FALHOU larguras {motivo}: {len(ts)} tabelas'); return
    tbl = ts[0]._tbl; cols = tbl.find(_qn('w:tblGrid')).findall(_qn('w:gridCol'))
    if len(cols) != len(novas): log.append(f'FALHOU larguras {motivo}: {len(cols)} colunas'); return
    for c, w in zip(cols, novas): c.set(_qn('w:w'), str(w))
    for tr in tbl.findall(_qn('w:tr')):
        for k, tc in enumerate(tr.findall(_qn('w:tc'))):
            w = tc.find(_qn('w:tcPr') + '/' + _qn('w:tcW'))
            if w is not None and k < len(novas): w.set(_qn('w:w'), str(novas[k])); w.set(_qn('w:type'), 'dxa')
    log.append(f'OK     larguras: {motivo} (soma {sum(novas)})')
# Tabela 17: especificidade e decisao liquida no mesmo limiar (pedido I.6 do orientador; valores do script 14). O VPN, quase
# constante entre os modelos, vai na nota. As colunas sao inseridas da ultima para a primeira, sempre depois da do VPP, para herdar o formato dela.
T17N = {'Árvores impulsionadas': ('0,846', '0,011'), 'Cobertura de juros': ('0,831', '0,009'), 'Mínimos quadrados parciais': ('0,810', '0,008'),
        'Retorno sobre ativos': ('0,843', '0,009'), 'Componentes principais (F)': ('0,570', '0,003'), 'Brito e Assaf Neto': ('0,462', '0,001'),
        'Referência sem informação': ('—', '—')}
t17 = [t for t in d.tables if 'AUC precisão-revocação' in t.rows[0].cells[1].text]
if len(t17) == 1 and len(t17[0].columns) == 6:
    for k, cab in [(1, 'Decisão líquida 10:1'), (0, 'Especificidade')]:
        insert_column(t17[0], 5, cab, lambda i, txt, k=k: T17N[txt.strip()][k] if txt.strip() in T17N else '', largura_twips=1000)
    log.append('OK     Tabela 17: colunas de especificidade e decisao liquida')
else:
    log.append(f'FALHOU Tabela 17: {len(t17)} tabelas encontradas')
larguras('AUC precisão-revocação', [1421, 1100, 800, 1150, 1150, 750, 1500, 1200], 'Tabela 17')
larguras('Somente por EBITDA negativo', [2071, 1000, 1000, 1000, 1100, 1000, 1000, 900], 'Tabela 13')
larguras('Cobertura menos F', [1771, 1000, 850, 1100, 1650, 1050, 1650], 'Tabela 14')
larguras('Somente a primeira entrada de cada firma', [2971, 900, 1000, 1000, 1000, 1200, 1000], 'Tabela 19')

d.save(DST)

# ------------------------------------------------------------------ 15. figuras regeneradas pelo codigo (Figuras 2 e 3 mudam com a versao das arvores)
import zipfile, struct, re, shutil
FIGS = {'media/b291c90bff9762b12cfefcdeb9eaac8533714c5a.png': os.path.join(AQUI, 'fig2_roc.png'),
        'media/decomposicao.png': os.path.join(AQUI, 'fig3_decomposicao.png')}
tmp = DST + '.tmp'
with zipfile.ZipFile(DST) as zi, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
    rels = zi.read('word/_rels/document.xml.rels').decode()
    rid = {}
    for el in re.findall(r'<Relationship [^>]*/>', rels):
        t = re.search(r'Target="([^"]+)"', el).group(1); i = re.search(r'Id="([^"]+)"', el).group(1)
        if t in FIGS: rid[i] = t
    for item in zi.infolist():
        data = zi.read(item.filename)
        alvo = 'media/' + item.filename.split('word/media/')[-1] if item.filename.startswith('word/media/') else None
        if alvo in FIGS:
            data = open(FIGS[alvo], 'rb').read()
        if item.filename == 'word/document.xml':
            x = data.decode()
            for i, t in rid.items():
                w, h = struct.unpack('>II', open(FIGS[t], 'rb').read()[16:24])
                # ajusta a altura do desenho que usa esta imagem a proporcao da imagem nova
                for m in re.finditer(r'<w:drawing>.*?</w:drawing>', x, re.S):
                    bloco = m.group(0)
                    if f'r:embed="{i}"' not in bloco: continue
                    cx = int(re.search(r'<wp:extent cx="(\d+)"', bloco).group(1)); cy = round(cx * h / w)
                    novo_b = re.sub(r'(<wp:extent cx="\d+" cy=")\d+(")', rf'\g<1>{cy}\2', bloco)
                    novo_b = re.sub(r'(<a:ext cx="\d+" cy=")\d+(")', rf'\g<1>{cy}\2', novo_b)
                    x = x.replace(bloco, novo_b); break
            data = x.encode()
        zo.writestr(item, data)
shutil.move(tmp, DST)
log.append('OK     Figuras 2 e 3 substituidas pelas geradas pelo codigo (versao fixada), com a altura ajustada a proporcao')
open(os.path.join(AQUI, 'log_aplicacao.txt'), 'w').write('\n'.join(log) + '\n')
print('\n'.join(log))
print(f"\n{sum(l.startswith('OK') for l in log)} aplicadas, {sum(l.startswith('FALHOU') for l in log)} falhas")
