# F2 — Concorrência e preços

**Status: incompleto.** Confiança: baixa. **Critério "Preço": não avaliável ainda.**

## O que foi feito
- **22 concorrentes** listados em `dados/concorrentes.csv` (15 na Tijuca, 6 em Copacabana, 1 em Botafogo), a partir das vitrines públicas do Trinks (sitemap, S20), de sites próprios e da rede Unhas Cariocas. Há endereço, tipo, franquia e horário. Abrem aos sábados: 15 de 15 com horário publicado. Funcionam até 21h ou mais: só 3, todos de shopping ou spa (Werner e Sense Spa no Shopping Tijuca, Sense Spa em Copacabana).
- **Preços** (`dados/precos.csv`): só 3 concorrentes têm tabela pública acessível. São as unidades Unhas Cariocas Tijuca Conde de Bonfim e Shopping Tijuca, e a de Botafogo como referência. Somam-se um preço da Booksy na Tijuca e as medianas de 6 capitais (Irrivio/Booksy, set/2026).
- O mapa `mapas/mapa_concorrencia.html` mostra os pontos, os raios de 800 m, o metrô e os 14 concorrentes geocodificados. Os endereços da Conde de Bonfim sem número de porta reconhecido ficaram fora, para não marcar o lugar errado.

## Preços encontrados (unhas)

| Serviço | Unhas Cariocas Conde de Bonfim | Unhas Cariocas Shopping Tijuca | Botafogo Praia Shopping | Mediana 6 capitais (P25–P75) |
|---|---|---|---|---|
| UNH02 Pé | R$ 39 | R$ 47 | R$ 50 | R$ 35 (30–43) |
| UNH03 Mão e pé | R$ 64 | R$ 81 | R$ 79 | R$ 60 (43–70) |
| UNH04 Gel mãos c/ cutilagem | R$ 75 | R$ 85 | R$ 100 | R$ 70 (50–88) |
| UNH05 Alongamento fibra | R$ 205 | R$ 250 | R$ 240 | R$ 155 (120–180) |
| UNH06 Spa dos pés | R$ 70 | R$ 90 | R$ 80 | — |

Corte com escova na Tijuca (Booksy, fora do raio): R$ 95.

## Por que está incompleto e o que falta
- O Google Maps e o Instagram não podem ser consultados sem login ou sem burlar bloqueios (regra 4). As tabelas do Trinks vêm de uma API que o robots.txt do site proíbe. Por isso não há notas do Google, avaliações dos últimos 90 dias nem seguidores.
- **Falta:** 12 ou mais concorrentes com preço por região, sobretudo de **cabelo** (CAB01–CAB06), que é onde está 60% do faturamento.
- **Tarefa da Manon:** `mensagens/salao_cliente.md` (consulta por WhatsApp, com a lista de quem perguntar).

## Tabela proposta (provisória, só unhas)
Mediana da Tijuca + 8%, sem passar do P75: com 2 pontos ainda não existe percentil confiável. Indicação provisória: mão e pé **R$ 69–75**, gel **R$ 80–85**. A tabela de cabelo depende da coleta.

## Lacunas que o salão pode ocupar (hipóteses a testar na F14)
- **Até 21h fora de shopping:** nenhum salão de rua com horário publicado fica aberto até 21h (o Sense Spa de Copacabana é spa express).
- Mão e pé durante a pausa da química (Apêndice I): nenhum concorrente divulga isso.
