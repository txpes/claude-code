# F3 — Salas para alugar em lugares com movimento

**Status: incompleto.** Confiança: baixa. **Critério "Sala": não atendido. Ainda não há sala que passe em todos os eliminatórios, e o nível de preço do mercado sugere que o teto de R$ 4,5 mil é apertado.**

## O que foi possível coletar
- ZAP, Viva Real e Imovelweb bloqueiam coleta automática (HTTP 403). A página de categoria do OLX ignora os filtros de bairro nesse tipo de acesso (trazia anúncios de São Paulo), então descartei a coleta. Pela regra 4, não tentei contornar.
- Ficaram 6 anúncios vistos em trechos de busca (`dados/imoveis.csv`), nenhum com dados completos:

| | Área | Aluguel | Cond. | IPTU | Total | R$/m² total |
|---|---|---|---|---|---|---|
| Tijuca, Conde de Bonfim (ZAP) | 64 m² | 3.300 | 2.068 | 844 | **6.212** | 97 |
| Copacabana, N. Sra. de Copacabana (Imovelweb) | 40 m² | 1.800 | 816 | 506 | 3.122 | 78 |
| Copacabana (Imovelweb) | 29 m² | 1.200 | 723 | — | — | — |

## Referência de mercado
- **Índice FipeZAP Comercial, ago/2026 (S07, S08):** aluguel anunciado no Rio de **R$ 57,51/m²**, alta de **20,97% em 12 meses** (a maior entre as 10 cidades). De janeiro a setembro de 2026, a alta foi de 15,92% (S09).
- Uma sala de 70 m² sai por **R$ 4.026 só de aluguel**, a esse preço médio. Com condomínio e IPTU (R$ 19–45/m² nos anúncios), o total fica entre **R$ 5,3 mil e 7,2 mil**. Os anúncios de bairro mostram aluguel de R$ 45–52/m², o que leva o total para **R$ 4,5–6,5 mil**.
- **Estimativa usada nas premissas validadas: R$ 5,2 mil/mês** (plano: R$ 4,2 mil), confiança baixa.

## O que falta (tarefa do Thomás)
1. Varrer pelo menos 40 anúncios por região nos portais, à mão, e preencher `dados/imoveis.csv`. Incluir lojas em galeria e salas maiores divisíveis.
2. Mandar a mensagem `mensagens/imobiliaria.md` para as 8 melhores e pontuar com o Apêndice E.
3. Deslocamento: medir no Google Maps, saindo do Largo dos Leões às 8h e às 19h. Em linha reta, o Largo dos Leões fica a ~4,4 km do ponto R1 e a ~1,9 km do ponto R2.

## Implicação para o plano
Se o total real ficar em R$ 5,2 mil, o salão continua viável, mas o equilíbrio sobe para 54% (ver relatório final). Acima de R$ 6 mil, o equilíbrio passa de 55% e o critério de viabilidade falha. Alternativas: sala de 60–65 m², andar alto em prédio comercial sem loja, galeria, ou negociar escalonamento maior no 1º ano.
