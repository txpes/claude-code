"""Monta alteracoes_v3.json: as mudancas pedidas pela coorientacao em outubro de 2026 (audios de 13 e 14/10).
Os numeros do panorama vem de panorama.pkl (script 17), para que texto e codigo nao divirjam.
Uso: python alteracoes_v3.py <diretorio onde o executar.sh rodou>  ->  alteracoes_v3.json"""
import sys, os, json, pickle

R = sys.argv[1]
PN = pickle.load(open(os.path.join(R, 'panorama.pkl'), 'rb'))
ano, tab, rs = PN['ano'], PN['tab'], PN['resumo']
pct = lambda x: f'{100 * x:.1f}'.replace('.', ',')
num = lambda x, k=3: f'{x:.{k}f}'.replace('.', ',')
A = []
add = lambda **k: A.append(k)

# ------------------------------------------------------------ 1. secoes: a seção nova 2 desloca as demais
mapa = {'1': '1', '2': '3', '2.1': '3.2', '2.2': '3.3', '2.3': '3.4', '2.4': '3.5', '3': '4', '4': '5', '5': '6', '6': '7'}
mapa.update({f'3.{k}': f'4.{k}' for k in range(1, 7)}); mapa.update({f'4.{k}': f'5.{k}' for k in range(1, 4)})
mapa.update({f'5.{k}': f'6.{k}' for k in range(1, 10)}); mapa.update({f'6.{k}': f'7.{k}' for k in range(1, 3)})
add(op='renumerar_secoes', mapa=mapa)

# ------------------------------------------------------------ 2. introdução: números do Brasil, contribuição e desenho
c15, c14, c10 = ano.cob1.loc[2015], ano.cob1.loc[2014], ano.cob1.loc[2010]
add(op='inserir_apos', ancora='Episódios recentes de deterioração financeira severa', modelo='Episódios recentes de deterioração financeira severa', textos=[
    'Esses episódios não são isolados. Entre 2010 e 2025, em média '
    f"{pct(rs['cob1_media'])}% das companhias abertas não financeiras com despesa financeira registraram, a cada ano, resultado operacional "
    f'inferior às despesas financeiras, isto é, cobertura de juros abaixo da unidade. A parcela passou de {pct(c10)}% em 2010 para '
    f'{pct(c15)}% em 2015, no auge da recessão, e permaneceu acima de 40% na maior parte dos anos seguintes. No mesmo período, '
    f"{rs['rj_total']} companhias recorreram à recuperação judicial ou extrajudicial, e cerca de três em cada dez registraram prejuízo "
    'líquido em um ano típico. A seção 2 detalha esse panorama.'])
add(op='substituir', antigo='no universo das companhias abertas brasileiras.',
    novo='no universo das companhias abertas brasileiras. Nem a análise de componentes principais nem sua contraparte supervisionada '
         'são métodos novos; o que se examina é o uso que se faz deles quando aplicados ao mesmo conjunto de indicadores e avaliados '
         'sob as mesmas condições.')
add(op='inserir_apos', ancora='O achado tem interesse que excede o indicador', modelo='O achado tem interesse que excede o indicador', textos=[
    'Do ponto de vista do desenho, o exercício se distingue da literatura nacional em cinco aspectos. Constrói um fator latente por '
    'redução de dimensionalidade, onde predominam indicadores isolados ou combinações fixadas de forma ad hoc. Adota a vulnerabilidade '
    'como alvo, e não o default, o que desloca a predição para um estágio em que a intervenção ainda é possível. Utiliza as '
    'Demonstrações Financeiras Padronizadas como painel sistemático, em lugar de amostras pareadas de dezenas de firmas. Trata a saída '
    'do painel como censura informativa e risco competitivo, e não apenas como viés de sobrevivência. E testa a superioridade contra '
    'benchmarks pré-especificados, com inferência por bootstrap agrupado por firma e correção para comparações múltiplas.'])
add(op='paragrafo', inicio='A seção 3 revisa a literatura', novo=
    'A seção 2 apresenta o panorama da dificuldade financeira das companhias abertas brasileiras no período. A seção 3 organiza a '
    'literatura em dois pilares, o da medição não supervisionada da fragilidade e o da previsão supervisionada, e explicita o que a '
    'comparação entre eles mede. A seção 4 apresenta a metodologia, as hipóteses e o calendário informacional que sustenta a '
    'interpretação preditiva. A seção 5 descreve a base de dados. A seção 6 reporta os resultados na ordem em que constroem o '
    'argumento: estrutura e validade do indicador, desempenho comparado nos dois esquemas de avaliação, antecipação, decomposição por '
    'tipo de entrada, diagnóstico e agregação supervisionada, métricas de probabilidade e robustez. A seção 7 conclui.')

# ------------------------------------------------------------ 3. seção 2: panorama
p = {r.periodo: r for r in tab.itertuples()}
add(op='inserir_apos', ancora='A seção 2 apresenta o panorama', modelo='1. Introdução',
    textos=['2. Panorama da fragilidade financeira das companhias abertas brasileiras'])
pl17 = ano.pl.loc[2017]
add(op='inserir_apos', ancora='2. Panorama da fragilidade financeira', modelo='Episódios recentes de deterioração financeira severa', textos=[
    'Antes da investigação, convém situar o objeto. Esta seção descreve, com o mesmo painel utilizado nos testes, a evolução de quatro '
    'sinais de dificuldade financeira entre as companhias abertas não financeiras brasileiras de 2010 a 2025: a cobertura de juros '
    'inferior à unidade, o EBITDA negativo, o patrimônio líquido negativo e o recurso à recuperação judicial ou extrajudicial. A '
    'descrição é deliberadamente simples e não depende de estimação alguma.',
    'A Figura {FIG:panorama} mostra que a parcela de companhias com cobertura de juros inferior à unidade, isto é, com resultado '
    f"operacional insuficiente para pagar as despesas financeiras do exercício, oscilou entre {pct(rs['cob1_min'])}%, em {rs['cob1_min_ano']}, e "
    f"{pct(rs['cob1_max'])}%, em {rs['cob1_max_ano']}, com média de {pct(rs['cob1_media'])}% no período. O salto coincide com a recessão de 2015-2016: "
    f'entre 2014 e 2015, a parcela passou de {pct(c14)}% para {pct(c15)}%, manteve-se em {pct(ano.cob1.loc[2016])}% em 2016 e só voltou a '
    f'patamar inferior a 45% em 2018. A parcela com EBITDA negativo acompanha o mesmo ciclo em nível mais baixo, com máximo de '
    f'{pct(ano.ebitda.max())}% em {int(ano.ebitda.idxmax())}, e a de patrimônio líquido negativo cresce de forma mais lenta e persistente, de '
    f'{pct(ano.pl.loc[2010])}% em 2010 a {pct(pl17)}% em 2017, e fica entre 8% e 10% a partir de 2021.'])
add(op='figura_apos', ancora='A Figura {FIG:panorama} mostra', modelo_legenda='Figura 4 – ',
    legenda='Figura {FIG:panorama} – Sinais de dificuldade financeira das companhias abertas não financeiras, 2010-2025',
    imagem='fig_panorama.png',
    fonte='Fonte: elaboração própria a partir das Demonstrações Financeiras Padronizadas e dos documentos periódicos e eventuais (CVM). '
          'Faixas sombreadas: recessão de 2015-2016 e pandemia de 2020. A cobertura de juros é calculada entre as companhias com despesa '
          'financeira. Painel (b): companhias do painel, pelo ano do primeiro documento que menciona a recuperação.')
add(op='inserir_apos', ancora='Fonte: elaboração própria a partir das Demonstrações Financeiras Padronizadas e dos documentos periódicos e eventuais (CVM). Faixas',
    modelo='Episódios recentes de deterioração financeira severa', textos=[
    f"As recuperações judiciais e extrajudiciais, datadas pelo primeiro documento da companhia que as menciona, somam {rs['rj_total']} "
    f'companhias do painel no período. A distribuição anual é irregular, com sete casos em 2014 e em 2018 e {int(ano.rj.loc[2024])} em 2024, '
    'três deles de um mesmo grupo têxtil. A Tabela {TAB:panorama} resume os indicadores por subperíodo. A recessão de 2015-2016 eleva '
    'todos os sinais ao mesmo tempo. Nos anos seguintes, a cobertura de juros e o EBITDA voltam a patamares próximos ou inferiores aos '
    'do início do período, mas o patrimônio líquido negativo permanece mais frequente do que em 2010-2014, e a alavancagem mediana, '
    'depois de recuar, volta a subir em 2022-2025.'])
cab = ['Período', 'Companhias por ano', 'Cobertura de juros < 1 (%)', 'EBITDA < 0 (%)', 'PL < 0 (%)', 'Prejuízo líquido (%)',
       'Alavancagem mediana', 'Recuperações']
linhas = [cab] + [[r.periodo, f'{r.companhias:.0f}', pct(r.cob1), pct(r.ebitda), pct(r.pl), pct(r.prejuizo), num(r.alv), str(r.rj)] for r in tab.itertuples()]
add(op='tabela_apos', ancora='As recuperações judiciais e extrajudiciais, datadas', modelo_legenda='Tabela 10 – ',
    legenda='Tabela {TAB:panorama} – Sinais de dificuldade financeira das companhias abertas não financeiras, por subperíodo (2010-2025)',
    linhas=linhas, larguras=[1100, 1300, 1100, 1000, 700, 1000, 1450, 1421],
    fonte='Fonte: elaboração própria a partir das Demonstrações Financeiras Padronizadas e dos documentos periódicos e eventuais (CVM). '
          'Percentuais sobre as companhias do painel em cada ano do subperíodo. Cobertura de juros: EBIT sobre o valor absoluto das '
          'despesas financeiras, entre as companhias com despesa financeira. Alavancagem: dívida bruta sobre ativo total. Recuperações: '
          'companhias cujo primeiro documento de recuperação judicial ou extrajudicial é do subperíodo.')
add(op='inserir_apos', ancora='Fonte: elaboração própria a partir das Demonstrações Financeiras Padronizadas e dos documentos periódicos e eventuais (CVM). Percentuais',
    modelo='Episódios recentes de deterioração financeira severa', textos=[
    'Dois traços do panorama orientam o que se segue. Os sinais não se movem juntos: a cobertura de juros e o EBITDA respondem ao '
    'ciclo, ao passo que o patrimônio líquido negativo se acumula mais lentamente, o que antecipa a distinção entre rotas de '
    'deterioração explorada na subseção 6.5. E a dificuldade financeira é disseminada, e não restrita aos casos de maior repercussão, '
    'o que justifica medi-la em escala contínua e avaliá-la sobre todo o universo de companhias abertas, e não apenas sobre amostras '
    'de firmas que chegaram ao default. Os números referem-se às companhias do painel descrito na subseção 5.1; a datação da '
    'recuperação judicial segue a regra da subseção 4.6, e as limitações dessa detecção estão na subseção 6.9.'])

# ------------------------------------------------------------ 4. revisão de literatura em dois pilares
add(op='substituir', antigo='3. Fragilidade, vulnerabilidade e distress', novo='3. Medir e prever a fragilidade financeira: dois pilares')
add(op='paragrafo', inicio='Esta seção percorre a literatura na ordem', novo=
    'A literatura sobre dificuldade financeira de empresas organiza-se em torno de duas propostas distintas. A primeira mede a '
    'fragilidade sem consultar o desfecho, a partir de uma estrutura teórica ou da covariância entre indicadores, e tem na hipótese de '
    'instabilidade financeira de Minsky sua principal referência: é o pilar não supervisionado. A segunda estima pesos para prever um '
    'desfecho observado, como a falência ou a recuperação judicial: é o pilar supervisionado, da tradição de predição de insolvência. '
    'As duas diferem no objetivo, no uso da informação e no critério de êxito, e é a comparação entre elas que se examina adiante. A '
    'subseção 3.1 delimita os conceitos, as subseções 3.2 e 3.3 percorrem os dois pilares, sempre na perspectiva da fragilidade e da '
    'vulnerabilidade financeira, e a subseção 3.4 explicita o que a comparação mede.')
add(op='inserir_apos', ancora='A literatura sobre dificuldade financeira de empresas organiza-se', modelo='3.2 O fundamento teórico',
    textos=['3.1 Fragilidade, vulnerabilidade e distress'])
add(op='substituir', antigo='3.2 O fundamento teórico e sua operacionalização', novo='3.2 Pilar não supervisionado: medir a fragilidade')
add(op='substituir', antigo='e encontra predominância da posição especulativa, com evolução distinta por setor e porte.',
    novo='e encontra predominância da posição especulativa, com evolução distinta por setor e porte. Novikova e Rozmainsky (2020) '
         'acompanham os regimes de financiamento de 42 grandes companhias não financeiras portuguesas entre 2001 e 2017 e documentam a '
         'redução da parcela em posição hedge e o aumento dos regimes frágeis antes e durante a Grande Recessão.')
add(op='substituir', antigo='e elevaram a preferência pela liquidez.',
    novo='e elevaram a preferência pela liquidez. Rolim, Cattan e Antonioli (2021) examinam dezenove setores das companhias abertas não '
         'financeiras brasileiras entre 2010 e 2016 e encontram redução das firmas em posição hedge e aumento das especulativas e Ponzi '
         'no período de reversão do ciclo, com padrões setoriais distintos.')
add(op='mover_apos', inicio='Entre as duas tradições existe um conjunto de abordagens', ancora='No Brasil, Torres Filho, Martins e Miaguti (2019)')
add(op='substituir', antigo='Entre as duas tradições existe um conjunto de abordagens que constrói medidas agregadas sem consultar o desfecho.',
    novo='O mesmo pilar reúne outras medidas construídas sem consultar o desfecho.')
add(op='substituir', antigo='e desde o fim dos anos 1980, na do BIS.',
    novo='e desde o fim dos anos 1980, na do BIS. Banerjee e Hofmann (2022) mostram, para companhias abertas não financeiras de 14 '
         'economias avançadas, que as firmas assim classificadas são menores, menos produtivas e mais alavancadas, e que seu desempenho se '
         'deteriora vários anos antes da classificação.')
add(op='substituir', antigo='3.3 A tradição de predição de insolvência', novo='3.3 Pilar supervisionado: prever a dificuldade financeira')
add(op='substituir', antigo='o que ilustra a diversidade de alvos que a literatura nacional agrupa sob o rótulo de insolvência.',
    novo='o que ilustra a diversidade de alvos que a literatura nacional agrupa sob o rótulo de insolvência. Predebom, Bianchi e '
         'Machado (2025) relacionam as fases do ciclo econômico à insolvência das companhias listadas na B3 entre 2010 e 2019, medida '
         'pelo escore Z, e encontram que o ciclo altera a relação entre insolvência e gerenciamento de resultados.')
add(op='substituir', antigo='Todos partilham o mesmo pressuposto: o desfecho orienta a construção do preditor.',
    novo='Mais recentemente, Jabeur et al. (2021) comparam um modelo de árvores impulsionadas para dados categóricos, o CatBoost, com '
         'oito modelos de referência a um, dois e três anos da falência e reportam ganho de classificação, e Shetty, Musa e Brédart (2022) '
         'alcançam acurácia de 82% a 83% em pequenas e médias empresas belgas com apenas três razões contábeis: retorno sobre ativos, '
         'liquidez corrente e solvência. Todos partilham o mesmo pressuposto: o desfecho orienta a construção do preditor.')
add(op='substituir', antigo='3.4 Agregação supervisionada e não supervisionada', novo='3.4 Duas propostas, uma comparação')
add(op='inserir_apos', ancora='A análise de componentes principais é o instrumento canônico', modelo='A análise de componentes principais é o instrumento canônico', textos=[
    'As duas técnicas não são intercambiáveis, e a comparação precisa ser lida com isso em mente. A análise de componentes principais '
    'busca a direção que melhor resume a variação conjunta dos indicadores, sem saber quais firmas entraram em vulnerabilidade; os '
    'mínimos quadrados parciais buscam a direção que melhor acompanha o desfecho, e por isso usam uma informação que a primeira não '
    'usa. A comparação não pergunta qual técnica é melhor em abstrato. Mantidos fixos os oito indicadores, o pré-processamento, a '
    'amostra e o procedimento de avaliação fora da amostra, a diferença de desempenho entre os dois escores mede quanto vale, na '
    'ponderação dos indicadores, a informação contida no desfecho. Nenhuma das duas técnicas é nova, e a contribuição não está nelas, '
    'mas na comparação controlada e na decomposição do resultado por rota de deterioração.'])
add(op='remover', inicio='3.5 A lacuna')
add(op='remover', inicio='O padrão da literatura nacional é o uso de variáveis isoladas')
add(op='remover', inicio='As cinco primeiras dizem respeito ao desenho.')
add(op='substituir', antigo='A sexta dimensão é a que organiza a contribuição. As duas tradições revisadas',
    novo='O que organiza a contribuição é a relação entre os dois pilares. As duas tradições revisadas')
add(op='substituir', antigo=' Zmijewski (1984) mostrou que a construção da amostra de eventos altera as estimativas de modelos de insolvência; '
                            'o argumento aqui é próximo, mas incide sobre a comparação entre preditores, e não sobre os coeficientes de um deles.',
    novo='')

add(op='substituir', antigo='A Tabela 11 repete a comparação sobre os subconjuntos puros',
    novo='A Tabela 11 e a Figura 3 repetem a comparação sobre os subconjuntos puros')    # a figura nao era citada no texto

# ------------------------------------------------------------ 5. dados: emissores estrangeiros que permaneceram
add(op='substituir', antigo='e não há cadastro de companhia aberta.',
    novo='e não há cadastro de companhia aberta. Três outros emissores na mesma condição, com 16 firma-anos e nenhuma entrada em '
         'vulnerabilidade, permaneceram nesta versão; reestimados os modelos sem eles, as áreas sob a curva das medidas que não envolvem '
         'estimação mudam no máximo 0,001 ponto e nenhuma conclusão se altera.')

# ------------------------------------------------------------ 6. equações como objetos de equação
def r(t, estilo=None):
    sty = '<m:rPr><m:sty m:val="p"/></m:rPr>' if estilo == 'p' else ''
    return f'<m:r>{sty}<m:t xml:space="preserve">{t}</m:t></m:r>'
sub = lambda base, s: f'<m:sSub><m:e>{base}</m:e><m:sub>{s}</m:sub></m:sSub>'
sup = lambda base, s: f'<m:sSup><m:e>{base}</m:e><m:sup>{s}</m:sup></m:sSup>'
subsup = lambda base, s, u: f'<m:sSubSup><m:e>{base}</m:e><m:sub>{s}</m:sub><m:sup>{u}</m:sup></m:sSubSup>'
par = lambda x, a='(', b=')': f'<m:d><m:dPr><m:begChr m:val="{a}"/><m:endChr m:val="{b}"/></m:dPr><m:e>{x}</m:e></m:d>'
frac = lambda n, d_: f'<m:f><m:num>{n}</m:num><m:den>{d_}</m:den></m:f>'
it = par(r('i,t'))
eq1 = subsup(r('x'), r('k'), r('*')) + it + r('=') + frac(sub(r('x'), r('k')) + it + r('−') + sub(r('μ'), r('k')), sub(r('σ'), r('k')))
eq2 = r('F') + it + r('=') + subsup(r('v'), r('1', 'p'), r('′')) + sup(r('x'), r('*')) + it
cond = (f'<m:d><m:dPr><m:begChr m:val="["/><m:sepChr m:val="|"/><m:endChr m:val="]"/></m:dPr>'
        f'<m:e>{r("V") + par(r("i,t+h")) + r("=1")}</m:e><m:e>{r("F") + it + r(", Z") + it}</m:e></m:d>')
eq3 = r('P') + cond + r('=Φ') + par(r('α+β F') + it + r('+') + sup(r('γ'), r('′')) + r('Z') + it)
add(op='equacao', inicio='x*ₖ(i,t) = [xₖ(i,t) − μₖ] / σₖ', omml=eq1)
add(op='equacao', inicio='F(i,t) = v₁′ x*(i,t)', omml=eq2)
add(op='equacao', inicio='P[V(i,t+h) = 1 | F(i,t), Z(i,t)]', omml=eq3)

# ------------------------------------------------------------ 7. referências novas, em ordem alfabética
NOVAS = [('BANERJEE, R.; HOFMANN, B. The rise of zombie firms', 'BANERJEE, R.; HOFMANN, B. Corporate zombies: anatomy and life cycle. Economic Policy, v. 37, n. 112, p. 757-803, 2022.'),
         ('HORN, J. L.', 'JABEUR, S. B.; GHARIB, C.; MEFTEH-WALI, S.; ARFI, W. B. CatBoost model and artificial intelligence techniques for corporate failure prediction. Technological Forecasting and Social Change, v. 166, art. 120658, 2021.'),
         ('NISHI, H.', 'NOVIKOVA, A. Y.; ROZMAINSKY, I. V. The non-financial private firms’ sector of Portugal in 2001–2017: the financial fragility hypothesis-based analysis. Voprosy Ekonomiki, n. 3, p. 115-128, 2020.'),
         ('PEDUZZI, P.', 'PREDEBOM, B.; BIANCHI, M.; MACHADO, V. Influence of economic cycles on the relationship of earnings management and insolvency of publicly traded companies. Brazilian Business Review, v. 22, n. 1, 2025.'),
         ('OHLSON, J. A.', None),
         ('MULLIGAN, R. F.', None),
         ('SCALZER, R. S.', 'SHETTY, S.; MUSA, M.; BRÉDART, X. Bankruptcy prediction using machine learning techniques. Journal of Risk and Financial Management, v. 15, n. 1, art. 35, 2022.'),
         ('PREDEBOM, B.', 'ROLIM, L. N.; CATTAN, R.; ANTONIOLI, J. Fragilidade financeira das empresas não financeiras de capital aberto no Brasil entre 2010 e 2016: uma análise setorial a partir de Minsky. Análise Econômica, v. 39, n. 78, 2021.')]
for ancora, ref in NOVAS:
    if ref:
        add(op='inserir_apos', ancora=ancora, modelo='ALTMAN, E. I.', textos=[ref])

json.dump(A, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'alteracoes_v3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(A), 'alteracoes ->', 'alteracoes_v3.json')
