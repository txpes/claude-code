# F10 — Custos fixos e operacionais

**Status: parcial (6 de 14 linhas com valor).** Confiança: baixa. **Critério "Custo fixo fase 1 ≤ R$ 9,6 mil": falha provável.**

| Linha | R$/mês | Método e fonte |
|---|---|---|
| Aluguel + condomínio + IPTU | **5.200** (4.500–6.500) | FipeZAP + anúncios (F3). Plano: 4.200 |
| Energia | **2.160** (1.730–2.590) | 1.848 kWh × R$ 1,169/kWh (abaixo) |
| Marketing recorrente | 1.200 | valor do plano (F13) |
| Contador | 300–600 | faixa nacional + adicional do Rio; cotar 3 |
| Homologação dos contratos (rateio) | 150 (200 na fase 2) | CCT Rio, cl. 18ª |
| Sistema de gestão | 110 (75–250) | F9 |
| **Subtotal com valor** | **≈ 9.270** | |
| Água e esgoto, internet, ECAD, limpeza, lavanderia, perfurocortantes, seguros, taxas | a confirmar | |

**As linhas já cotadas somam ~R$ 9,3 mil, antes de 8 linhas.** O limite de R$ 9,6 mil para a fase 1 deve estourar se o aluguel ficar perto de R$ 5,2 mil e a energia perto de R$ 2,2 mil.

## Consumo de energia (estimativa)

| Carga | kWh/mês |
|---|---|
| Secadores: 3 postos × 1,9 kW × 3 h × 26 dias | 445 |
| Ar ≈ 60 mil BTU/h: 5,5 kW × 60% × 10 h × 26 dias | 858 |
| Iluminação: 70 m² × 12 W × 11 h × 26 dias | 240 |
| Aquecedor de passagem: 5,5 kW × 1 h × 26 dias | 143 |
| Autoclave: 1,6 kW × 1,5 h × 26 dias | 62 |
| Outros | 100 |
| **Total** | **1.848** |

Tarifa: Light R$ 0,8806/kWh sem impostos (S53) ÷ (1 − 20% de ICMS − 4,65% de PIS/COFINS) = R$ 1,169/kWh. Em 2026, uma liminar elevou o reajuste do subgrupo B3 para +15,12% (ANEEL, S52), e não sei se o valor-base já o inclui. Os horários de uso são hipóteses do analista. **Conferir com a fatura da sala ou com a resolução homologatória.**

## Premissa validada
`fixos_fase1` = R$ 9,7 mil e `fixos_fase2` = R$ 10,1 mil (+R$ 1.000 de aluguel). Mais R$ 150 de homologação em `fixos_extras`. Confiança baixa.
