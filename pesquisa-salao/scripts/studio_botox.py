"""Estudo de viabilidade: studio de toxina botulínica e estética na Tijuca.

Fisioterapeuta dermatofuncional (mãe do Thomás) aplica; Manon faz divulgação e CRM;
Thomás investe. Simulação mensal de 60 meses + cascata de distribuição (waterfall).

Valores reais com fonte (acesso 03-04/11/2026):
  - preço ao paciente, terço superior: R$ 950 (dermatologista, Del Castilho, promoção) a
    R$ 1.500-2.500 (clínica do Rio, jun/2026)  -> base R$ 1.000 (posicionamento Tijuca)
  - frasco 100U: Xeomin R$ 595-785, Botox R$ 670-703 -> base R$ 700 / 100U
  - unidades terço superior: 40-60U (guia de clínicas 2026) -> base 50U
  - sala: Rua Conde de Bonfim 112, 48 m², R$ 1.200 + cond. R$ 930 (+ IPTU estimado)
  - CREFITO-2: PJ R$ 307 + certificado R$ 99 + anuidade R$ 577
  - mocho R$ 387, maca 8 em 1 R$ 817, balcão R$ 413 (Maxibel/Pedrosa)
  - Simples Anexo III; Selic 13,75%; IPCA 4,58% (BCB)
Hipóteses (sem fonte, marcadas como tal): ritmo de pacientes novos, retorno, CAC,
custos fixos menores, investimento em reforma leve.
Uso: python scripts/studio_botox.py
"""
import json, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts")); sys.path.insert(0, str(RAIZ / "simulador"))
import fcd  # noqa: E402  (tir, IPCA, SELIC)
from simulador import aliquota_efetiva  # noqa: E402

ANEXO_III = [[180000, 0.06, 0], [360000, 0.112, 9360], [720000, 0.135, 17640], [1800000, 0.16, 35640]]

BASE = {
    "ticket_toxina": 1000,           # R$ por aplicação (terço superior)
    "custo_unidade": 7.0,            # R$ 700 / 100U
    "unidades": 50,
    "descartaveis": 30,              # hipótese
    "outros_por_paciente": 0.25,     # receita de outros procedimentos = 25% da toxina (hipótese)
    "margem_outros": 0.80,           # custo de insumo de 20% nos outros procedimentos (hipótese)
    "novos_rampa": [6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 25, 25],  # pacientes novos/mês (hipótese)
    "novos_maduro": 25,
    "retorno": 0.60,                 # % que volta em 6 meses (hipótese)
    "meses_retorno": 6,
    "cac": 200,                      # R$ de marketing pago por paciente novo (hipótese; Meta R$ 5-40/lead)
    "pct_pago": 0.5,                 # metade dos novos vem de mídia paga; resto de indicação/rede
    "marketing_fixo": 500,           # conteúdo/ferramentas (hipótese)
    "taxa_cartao": 0.02,
    "aluguel_total": 2350,           # 1.200 + 930 + IPTU est. 220
    "fixos_outros": 1500,            # energia, internet 100, sistema, contador, CREFITO, seguro, resíduos, limpeza (hipótese)
    "rem_mae": 5000, "rem_manon": 5000,
    "capacidade_mes": 110,           # atendimentos/mês com 1 profissional (hipótese: ~5/dia, 22 dias)
    "investimento": 30000,
    "capital_giro": 20000,
    "reserva_caixa": 6000,           # caixa mínimo antes de pagar o Thomás
    "pref_multiplo": 1.0,            # mútuo do Thomás: 100% do excedente até quitar...
    "pref_juros_aa": 0.1365,         # ...a CDI (13,65% a.a.)
    "split": {"thomas": 0.20, "mae": 0.40, "manon": 0.40},
    "meses": 60,
}

INVESTIMENTO_DETALHE = [  # (item, valor, origem)
    ("Reforma leve (pintura, ponto de água na sala, piso vinílico, iluminação)", 8000, "hipótese — pedir orçamento"),
    ("Maca elétrica/estética", 2500, "maca 8 em 1 R$ 817 (Maxibel); elétrica a cotar"),
    ("Mocho + cadeira de apoio", 800, "mocho R$ 387 (Maxibel)"),
    ("Frigobar com termômetro (toxina 2–8 °C)", 1200, "hipótese"),
    ("Recepção (balcão + 2 cadeiras) e armário", 1500, "balcão R$ 413 (Pedrosa) + hipótese"),
    ("Computador/tablet + luminária com lupa", 3000, "hipótese"),
    ("Legalização (CREFITO PJ R$ 406, alvará, licença sanitária, contador)", 2000, "CREFITO-2 real; resto hipótese"),
    ("Marca, fotos, site e conteúdo pré-lançamento", 3000, "hipótese"),
    ("Estoque inicial (3 frascos + descartáveis)", 2500, "frasco R$ 595–785"),
    ("Garantia do aluguel (seguro-fiança) e custos antes de abrir", 5500, "hipótese ~2 meses de aluguel"),
]


def simular(p):
    n = p["meses"]
    proc = [0.0] * (n + 1)
    saldo_pref = p["investimento"] + p["capital_giro"]
    i_m = (1 + p["pref_juros_aa"]) ** (1 / 12) - 1
    caixa = p["capital_giro"]
    meses, rec12 = [], []
    pago = {"thomas": 0.0, "mae": 0.0, "manon": 0.0}
    for m in range(1, n + 1):
        novos = p["novos_rampa"][m - 1] if m <= len(p["novos_rampa"]) else p["novos_maduro"]
        ret = p["retorno"] * proc[m - p["meses_retorno"]] if m > p["meses_retorno"] else 0
        atend = min(novos + ret, p["capacidade_mes"])
        proc[m] = atend
        rec_tox = atend * p["ticket_toxina"]
        rec_out = rec_tox * p["outros_por_paciente"]
        receita = rec_tox + rec_out
        rec12.append(receita); rec12 = rec12[-12:]
        rbt12 = sum(rec12) * 12 / len(rec12)
        aliq = aliquota_efetiva(rbt12, ANEXO_III)
        insumos = atend * (p["custo_unidade"] * p["unidades"] + p["descartaveis"]) + rec_out * (1 - p["margem_outros"])
        marketing = novos * p["pct_pago"] * p["cac"] + p["marketing_fixo"]
        custos = insumos + marketing + receita * (p["taxa_cartao"] + aliq) + p["aluguel_total"] + p["fixos_outros"]
        operacional = receita - custos                       # antes de pagar as pessoas
        # Camada 1: remuneração do trabalho (mãe e Manon), até o fixo, com o que houver
        alvo = p["rem_mae"] + p["rem_manon"]
        rem = min(alvo, max(0.0, operacional)) if operacional > 0 else 0.0
        rem_mae = rem * p["rem_mae"] / alvo; rem_manon = rem * p["rem_manon"] / alvo
        sobra = operacional - rem
        caixa += sobra
        # Camada 2: Thomás recebe 100% do excedente acima da reserva até zerar capital + CDI
        saldo_pref *= (1 + i_m)
        dist_th = dist_mae = dist_manon = 0.0
        livre = max(0.0, caixa - p["reserva_caixa"])
        if saldo_pref > 0 and livre > 0:
            x = min(livre, saldo_pref); dist_th += x; saldo_pref -= x; caixa -= x; livre -= x
        # Camada 3: depois do preferencial, divide pelo split
        if saldo_pref <= 0 and livre > 0:
            dist_th += livre * p["split"]["thomas"]; dist_mae += livre * p["split"]["mae"]; dist_manon += livre * p["split"]["manon"]
            caixa -= livre
        pago["thomas"] += dist_th; pago["mae"] += rem_mae + dist_mae; pago["manon"] += rem_manon + dist_manon
        meses.append({"mes": m, "atendimentos": round(atend, 1), "novos": novos, "receita": receita,
                      "operacional": operacional, "rem_mae": rem_mae, "rem_manon": rem_manon,
                      "dist_thomas": dist_th, "dist_mae": dist_mae, "dist_manon": dist_manon,
                      "caixa": caixa, "saldo_pref": saldo_pref, "aliquota": aliq})
    return meses, pago


def resumo(p):
    meses, pago = simular(p)
    aporte = p["investimento"] + p["capital_giro"]
    fluxo_th = [-aporte] + [m["dist_thomas"] for m in meses]
    fluxo_th[-1] += max(0.0, meses[-1]["caixa"]) * p["split"]["thomas"]  # parte dele no caixa final
    tm = fcd.tir(fluxo_th)
    tir_th = None if tm is None else (1 + tm) ** 12 - 1
    fluxo_proj = [-p["investimento"]] + [m["operacional"] - m["rem_mae"] - m["rem_manon"] for m in meses]
    tp = fcd.tir(fluxo_proj)
    tir_proj = None if tp is None else (1 + tp) ** 12 - 1
    pb = next((m["mes"] for m in meses if m["saldo_pref"] <= 0), None)
    full = next((m["mes"] for m in meses if m["rem_mae"] + m["rem_manon"] >= p["rem_mae"] + p["rem_manon"] - 1), None)
    mad = meses[-1]
    ano = lambda k, a: round(sum(m[k] for m in meses[12 * a:12 * a + 12]))
    return {"tir_projeto_aa": tir_proj, "tir_thomas_aa": tir_th, "mes_thomas_recupera": pb,
            "mes_remuneracao_cheia": full, "atend_mes60": mad["atendimentos"], "receita_mes60": mad["receita"],
            "operacional_mes60": mad["operacional"], "pior_caixa": min(m["caixa"] for m in meses),
            "pago_5a": {k: round(v) for k, v in pago.items()},
            "thomas_ano": [ano("dist_thomas", a) for a in range(5)],
            "mae_ano": [ano("rem_mae", a) + ano("dist_mae", a) for a in range(5)],
            "manon_ano": [ano("rem_manon", a) + ano("dist_manon", a) for a in range(5)],
            "receita_ano": [ano("receita", a) for a in range(5)]}


def ponto_equilibrio(p, extra=0.0):
    """Atendimentos de toxina/mês para cobrir custos + remunerações (+ extra)."""
    tox = p["ticket_toxina"]; rec = tox * (1 + p["outros_por_paciente"])
    marg = rec * (1 - p["taxa_cartao"] - 0.08) - (p["custo_unidade"] * p["unidades"] + p["descartaveis"]) - tox * p["outros_por_paciente"] * (1 - p["margem_outros"])
    fixo = p["aluguel_total"] + p["fixos_outros"] + p["marketing_fixo"] + p["rem_mae"] + p["rem_manon"] + extra
    return fixo / (marg - p["pct_pago"] * p["cac"] * 0.4)  # ~40% dos atendimentos maduros são de novos


CENARIOS = {
    "base": {},
    "preço R$ 800": {"ticket_toxina": 800},
    "preço R$ 1.300": {"ticket_toxina": 1300},
    "metade dos pacientes novos": {"novos_rampa": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12, 12], "novos_maduro": 12.5},
    "retorno de 40%": {"retorno": 0.40},
    "CAC R$ 400": {"cac": 400},
    "toxina R$ 9/U e 60U": {"custo_unidade": 9.0, "unidades": 60},
}


def main():
    out = {}
    for nome, ov in CENARIOS.items():
        p = {**BASE, **ov}
        r = resumo(p); out[nome] = r
        f = lambda x: "neg/n.a." if x is None else f"{x:.0%}"
        print(f"{nome:28s} TIR proj {f(r['tir_projeto_aa']):>9} | TIR Thomás {f(r['tir_thomas_aa']):>9} | Thomás recupera mês {r['mes_thomas_recupera']} | "
              f"rem. cheia mês {r['mes_remuneracao_cheia']} | atend m60 {r['atend_mes60']:.0f} | oper m60 {r['operacional_mes60']:,.0f} | pior caixa {r['pior_caixa']:,.0f} | pago 5a {r['pago_5a']}")
    out["ponto_equilibrio_atend_mes"] = ponto_equilibrio(BASE)
    out["ponto_equilibrio_com_5k_thomas"] = ponto_equilibrio(BASE, 5000)
    out["investimento_detalhe"] = INVESTIMENTO_DETALHE
    print("equilíbrio:", round(out["ponto_equilibrio_atend_mes"]), "atend/mês; com +5k p/ Thomás:", round(out["ponto_equilibrio_com_5k_thomas"]))
    print("investimento:", sum(v for _, v, _ in INVESTIMENTO_DETALHE))
    b = out["base"]; print("anos base: receita", b["receita_ano"], "| Thomás", b["thomas_ano"], "| mãe", b["mae_ano"], "| Manon", b["manon_ano"])
    (RAIZ / "dados" / "studio_botox.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=float), encoding="utf-8")


if __name__ == "__main__":
    main()
