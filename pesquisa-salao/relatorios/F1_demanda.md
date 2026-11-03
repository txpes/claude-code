# F1 — Demanda e perfil das regiões

**Status: pronto.** Confiança: média (dados oficiais; o gasto por domicílio é estadual e não inclui estética).

## Método
- **Público:** setores censitários do Censo 2022 (camada IPP/Data.Rio, S01) que tocam um círculo de 800 m em volta de cada ponto. Cada setor entra pela fração da área dentro do círculo. O setor não cruza sexo com idade, então mulheres de 20–69 = pessoas de 20–69 × fração feminina do setor. No bairro inteiro, o cruzamento exato (S02) dá a mesma proporção (37,5% contra 38,6% no raio).
- **Gasto:** POF 2017-18, UF Rio de Janeiro (S04): cabeleireiro R$ 30,96 + manicuro/pedicuro R$ 11,22 por família/mês, corrigido pelo IPCA de fev/2018 a set/2026 (fator 1,5608, BCB SGS 433, S05) = **R$ 790/domicílio/ano**.
- **Mercado potencial** = domicílios no raio × R$ 790. Faixa alta: o mesmo valor ajustado pela razão entre a renda média do responsável no raio e a da cidade (R$ 4.378, S01). O briefing pede gasto por mulher; a POF só tem gasto por família, então o valor por mulher é derivado.
- **Fatia necessária** = R$ 940 mil/ano (faturamento planejado) ÷ mercado potencial. Acima de 5%: risco alto.
- Script: `scripts/f1_demanda.py`; saída: `dados/bairros.csv` e `dados/f1_raio800.json`.

## Resultado

| | R1 Tijuca (Afonso Pena) | R2 Copacabana (Cardeal Arcoverde–Siqueira Campos) | R3 Humaitá (só referência) |
|---|---|---|---|
| População no raio de 800 m | 51.806 | 56.322 | 31.439 |
| Mulheres de 20 a 69 anos | 19.995 | 21.952 | 12.076 |
| % de 60 anos ou mais | 30,3% | 34,4% | 26,6% |
| Domicílios ocupados | 22.662 | 28.170 | 14.166 |
| Renda média do responsável | R$ 8.345 | R$ 9.455 | R$ 10.460 |
| Mercado potencial/ano (sem ajuste – ajustado pela renda) | R$ 17,9 – 34,1 mi | R$ 22,3 – 48,1 mi | R$ 11,2 – 26,7 mi |
| **Fatia necessária** | **5,3% – 2,8%** | **4,2% – 2,0%** | 8,4% – 3,5% |

Bairro inteiro (Censo 2022): Tijuca tem 141.652 moradores, 53.122 mulheres de 20 a 69 anos e fatia necessária de 2,0% (sem ajuste). Copacabana tem 127.276 moradores e 48.334 mulheres de 20 a 69 anos, com fatia de 1,9%.

## Leitura
- **Copacabana passa** no critério de mercado (≤ 5%) mesmo sem ajuste de renda. **A Tijuca fica no limite**: 5,3% sem ajuste de renda, 2,8% com ajuste. Os dois cálculos são conservadores: o raio de 800 m ignora quem trabalha na região e quem vem de mais longe, e a POF não inclui estética (sobrancelha, cílios, depilação).
- Copacabana tem público mais velho (34% com 60+). Isso pesa a favor de manicure e pedicure e contra química e cílios.
- Não consultei o Google Trends: o site não oferece acesso público por API e bloqueia coleta automática. Fica para trás, sem impacto no critério.
