"""Monta alteracoes_v6.json: resumo e abstract reescritos para leitor não especialista (pedido do coorientador,
áudio de 06/11/2026): cenário brasileiro nas primeiras linhas, o que se faz e como, dados em termos gerais, resultado
sem números técnicos e conclusão curta. Aplicado sobre a v5."""
import json, os
RESUMO = (
    'Entre 2010 e 2025, a cada ano, cerca de quatro em cada dez companhias abertas não financeiras brasileiras não geraram '
    'resultado operacional suficiente para cobrir suas despesas financeiras, e 72 delas recorreram à recuperação judicial ou '
    'extrajudicial. Identificar com antecedência as empresas que caminham para essa situação interessa a credores, investidores e '
    'reguladores. Investiga-se se reunir vários indicadores contábeis em um único índice de fragilidade financeira permite essa '
    'antecipação melhor do que os melhores indicadores usados isoladamente. O índice é construído por componentes principais, '
    'técnica que resume os indicadores sem usar a informação sobre quais empresas entraram em dificuldade, e é comparado a '
    'indicadores isolados e a modelos que aprendem com essas ocorrências, sempre em empresas que não participaram da estimação. '
    'Uma análise exploratória, feita depois desse teste, separa as dificuldades segundo o caminho que levou a elas: prejuízo '
    'operacional persistente, patrimônio líquido negativo ou recuperação judicial, e compara o perfil das empresas em cada '
    'caminho. Os dados reúnem as demonstrações anuais de 727 companhias registradas na Comissão de Valores Mobiliários, de 2010 '
    'a 2025, e oito indicadores de liquidez, estrutura de capital, rentabilidade e capacidade de pagamento. O índice não supera os melhores indicadores isolados, e a análise exploratória mostra que a diferença se concentra nas '
    'empresas que caminham para o prejuízo operacional: por terem pouca dívida e boa liquidez, elas tendem a parecer sólidas a um '
    'índice dominado pela estrutura do balanço. Nos outros dois caminhos, o índice não se distingue dos indicadores isolados. A '
    'utilidade de agregar indicadores depende, portanto, do tipo de deterioração que se quer antecipar.')
ABSTRACT = (
    'Between 2010 and 2025, in each year about four in ten Brazilian non-financial listed companies did not generate enough '
    'operating income to cover their financial expenses, and 72 of them filed for judicial or out-of-court reorganization. '
    'Identifying in advance the firms heading toward this situation matters to creditors, investors and regulators. We '
    'investigate whether combining several accounting indicators into a single financial fragility index anticipates these '
    'difficulties better than the best indicators used individually. The index is built by principal components, a technique '
    'that summarizes the indicators without using information on which firms ran into difficulty, and it is compared with '
    'individual indicators and with models that learn from those occurrences, always on firms not used in estimation. An '
    'exploratory analysis, carried out after this test, separates the difficulties by the path that led to them: persistent '
    'operating losses, negative equity or judicial reorganization, and compares the profile of firms on each path. The data '
    'comprise the annual statements of 727 companies registered with the Brazilian Securities and Exchange Commission, from 2010 '
    'to 2025, and eight indicators of liquidity, capital structure, profitability and debt-service capacity. The index does not outperform the best individual indicators, and the exploratory analysis shows that the gap is '
    'concentrated among firms heading toward operating losses: with little debt and good liquidity, they tend to look sound to '
    'an index dominated by balance-sheet structure. On the other two paths, the index is indistinguishable from the individual '
    'indicators. The value of aggregating indicators therefore depends on the kind of deterioration one seeks to anticipate.')
A = [dict(op='paragrafo', inicio='Examina-se se a agregação de indicadores contábeis', novo=RESUMO),
     dict(op='paragrafo', inicio='This paper examines whether aggregating', novo=ABSTRACT)]
json.dump(A, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'alteracoes_v6.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print(len(RESUMO.split()), 'palavras no resumo;', len(ABSTRACT.split()), 'no abstract')
