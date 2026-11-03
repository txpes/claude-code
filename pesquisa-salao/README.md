# Pesquisa e viabilidade — Salão da Manon

Execução do *Briefing para o Claude Code* (v1, 03/11/2026). Rodada 1: tudo o que foi possível pesquisar sem contatar pessoas e sem burlar bloqueios de sites.

**Recomendação: AJUSTAR.** Leia `relatorios/relatorio_final.md` ou o `.pdf`.

## Como reproduzir
```bash
pip install pyyaml pandas openpyxl pytest shapely folium matplotlib
cd simulador && python -m pytest -q                      # testes de aceitação do Apêndice A
python simulador.py --premissas premissas.yaml --comparar premissas_validadas.yaml --saida saida/simulacao.xlsx
python simulador.py --premissas premissas_validadas.yaml --comparar premissas.yaml --saida saida/simulacao_validada.xlsx
cd .. && python scripts/f1_demanda.py                    # público no raio de 800 m (Censo 2022, Data.Rio)
python scripts/f2_unhas_cariocas.py                      # preços públicos da rede Unhas Cariocas
python scripts/mapa.py                                   # mapas/mapa_concorrencia.html
```

## Status por frente

| Frente | Status | Principal resultado |
|---|---|---|
| F1 Demanda | ✅ pronto | Fatia necessária: Copacabana 2,0–4,2%; Tijuca 2,8–5,3% (limite de 5%) |
| F2 Concorrência | ⚠️ incompleto | 22 concorrentes; preços só de 3 (unhas). Falta cabelo: Manon |
| F3 Imóveis | ⚠️ incompleto | Portais bloqueiam coleta. FipeZAP indica ~R$ 5,2 mil total (plano: 4,2) |
| F4 Licenças | 🟡 parcial | Sequência CPL → alvará → sanitária → CBMERJ (CAS); homologação sindical obrigatória |
| F5 Equipamentos | ⚠️ parcial | 8 de 31 itens; ar precisa de ~61 mil BTU/h |
| F6 Obra | ❌ sem preços | Itens por perfil listados |
| F7 Produtos | ⚠️ parcial | Custo de coloração de raiz ≈ R$ 39 (varejo) |
| F8 Profissionais | 🟡 parcial | Recepção fixa R$ 2.913 (CCT Rio); mínimo de 20% de repasse |
| F9 Tecnologia | ✅ pronto | InfinitePay ~1,5–2,1%; taxa precisa ser descontada antes da divisão |
| F10 Custos fixos | ⚠️ parcial | Linhas cotadas ≈ R$ 9,3 mil antes de 8 linhas (limite de 9,6) |
| F11 Tributário | ✅ para parecer | Perguntas em `mensagens/perguntas_contador.md` |
| F12 Benchmarks | 🟡 parcial | Poucas fontes com metodologia |
| F13 Marketing | ✅ plano | 90 dias, ~R$ 4 mil |
| F14 Clientes | ⏳ aguardando | Questionário pronto |

## Tarefas para o Thomás e a Manon
Ver `mensagens/README_tarefas.md`. Portão: **2 cartas das âncoras até 18/12/2026**.

## O que não foi possível e por quê
- ZAP, Viva Real e Imovelweb (HTTP 403), Google Maps, Instagram e a API de preços do Trinks (proibida pelo robots.txt): não acessados (regra 4).
- Planalto e portal do Simples: sem resposta neste ambiente; normas vieram de compilações e precisam ser conferidas no texto oficial.
- PDF do Decreto 23.915/2004 (Vigilância Sanitária): acesso automático negado pelo portal.
- IBGE SIDRA: alguns endpoints com bloqueio do Cloudflare; a tabela 6715 veio pela API.

## Estrutura
`dados/` (CSVs no esquema da seção 7, com `fontes.csv`) · `relatorios/` (F1–F14 e relatório final) · `mapas/` · `mensagens/` · `simulador/` (Apêndice A, testes e saídas) · `scripts/`.
