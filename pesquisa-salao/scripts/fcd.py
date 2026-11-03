"""Fluxo de caixa descontado (5 anos) e TIR do Salão da Manon.

Usa o simulador do Apêndice A com horizonte de 60 meses. Os valores do simulador estão
em preços constantes (sem reajuste), então a TIR calculada é REAL; a TIR nominal
equivalente soma a inflação: (1 + real) x (1 + IPCA) - 1.

Fluxo do projeto: mês 0 = -investimento de montagem; meses 1-60 = resultado do mês
(já depois de impostos do Simples, taxas, produtos, fixos, recepção, pró-labore da Manon
e capex da fase 2). O capital de giro (R$ 26 mil) é caixa parado, não custo: entra no
mês 0 e volta no mês 60, então não altera o VPL a taxa zero, mas reduz a TIR.

Uso: python scripts/fcd.py [--sala TOTAL_MENSAL ...]
"""
import argparse, copy, json, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "simulador"))
import simulador as s  # noqa: E402

IPCA = 0.0458        # BCB SGS 13522, 12 meses até set/2026
SELIC = 0.1375       # BCB SGS 432, 04/11/2026
TAXAS = {"Selic (custo de oportunidade)": SELIC, "Selic + 6 p.p.": SELIC + 0.06, "Selic + 12 p.p. (risco de pequeno negócio)": SELIC + 0.12}
NAO_ALUGUEL_F1, NAO_ALUGUEL_F2 = 4500, 4900   # fixos do plano sem aluguel+cond+IPTU (8.700-4.200; 9.100-4.200)


def tir(fluxos, lo=-0.99, hi=1.0):
    def vpl(r):
        return sum(f / (1 + r) ** t for t, f in enumerate(fluxos))
    if vpl(lo + 1e-9) * vpl(hi) > 0:
        return None
    for _ in range(200):
        m = (lo + hi) / 2
        if vpl(lo) * vpl(m) <= 0:
            hi = m
        else:
            lo = m
    return (lo + hi) / 2


def fluxos(p, cenario="base", meses=60, giro=False, terminal_meses=0):
    q = s.aplicar_cenario(p, cenario)
    q["horizonte_meses"] = meses
    r = s.simular(q)
    f = [-q["investimento_montagem"]] + [m["resultado"] for m in r["meses"]]
    if giro:
        f[0] -= q["capital_giro"]
        f[-1] += q["capital_giro"]
    if terminal_meses:
        f[-1] += terminal_meses * r["meses"][-1]["resultado"]
    return f, r


def resumo(p, cenario="base", giro=False, terminal_meses=0):
    f, r = fluxos(p, cenario, giro=giro, terminal_meses=terminal_meses)
    tm = tir(f)
    ta_real = (1 + tm) ** 12 - 1 if tm is not None else None
    ta_nom = (1 + ta_real) * (1 + IPCA) - 1 if ta_real is not None else None
    real = {k: (1 + v) / (1 + IPCA) - 1 for k, v in TAXAS.items()}
    vpl = {k: sum(x / (1 + rr) ** (t / 12) for t, x in enumerate(f)) for k, rr in real.items()}
    acum, pb, pbd = 0, None, None
    acd = 0
    for t, x in enumerate(f):
        acum += x
        acd += x / (1 + real["Selic + 6 p.p."]) ** (t / 12)
        if pb is None and t > 0 and acum >= 0:
            pb = t
        if pbd is None and t > 0 and acd >= 0:
            pbd = t
    anos = [round(sum(f[1 + 12 * a:13 + 12 * a])) for a in range(5)]
    return {"tir_real_aa": ta_real, "tir_nominal_aa": ta_nom, "vpl": vpl, "payback": pb,
            "payback_descontado_selic+6": pbd, "fluxo_anual": anos, "investimento": -f[0],
            "lucro_mes_60": r["meses"][-1]["resultado"], "parada": r["resumo"]["mes_parada"],
            "multiplo_caixa": (sum(f[1:])) / -f[0]}


def com_sala(p, total, desconto_ano1=600):
    return s.aplicar_overrides(p, {"fixos_fase1": NAO_ALUGUEL_F1 + total, "fixos_fase2": NAO_ALUGUEL_F2 + total,
                                   "desconto_aluguel_ano1": desconto_ano1})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="grava resultados em JSON")
    a = ap.parse_args()
    p = s.carregar(RAIZ / "simulador" / "premissas.yaml")
    v = s.carregar(RAIZ / "simulador" / "premissas_validadas.yaml")
    casos = {
        "Plano (premissas originais)": (p, "base"),
        "Validado (sala R$ 5,2 mil)": (v, "base"),
        "Validado com sala de R$ 4,3 mil": (com_sala(v, 4288), "base"),
        "Validado com sala de R$ 6,2 mil": (com_sala(v, 6200), "base"),
        "Validado + equipamentos/ar +R$ 6 mil": (s.aplicar_overrides(v, {"investimento_montagem": 80000}), "base"),
        "Validado, salão absorve taxa cheia do cartão": (s.aplicar_overrides(v, {"taxa_cartao": 0.034}), "base"),
        "Estresse: rampa lenta": (v, "rampa_lenta"),
        "Estresse: faturamento -25%": (v, "fat_menor"),
        "Estresse: obra +20%": (v, "obra_cara"),
        "Estresse: sem aumento de preço": (v, "sem_aumento"),
        "Estresse: tudo junto": (v, "tudo_junto"),
    }
    out = {}
    for nome, (q, c) in casos.items():
        out[nome] = {"sem_valor_terminal": resumo(q, c), "com_giro": resumo(q, c, giro=True),
                     "valor_terminal_12m": resumo(q, c, terminal_meses=12)}
    for nome, d in out.items():
        x = d["sem_valor_terminal"]
        t = lambda z: "  n/a " if z is None else f"{z:6.1%}"
        print(f"{nome:46s} TIR real {t(x['tir_real_aa'])} nominal {t(x['tir_nominal_aa'])} | c/ giro {t(d['com_giro']['tir_nominal_aa'])} | c/ VT 12m {t(d['valor_terminal_12m']['tir_nominal_aa'])} | "
              f"VPL@S+6 {x['vpl']['Selic + 6 p.p.']:>9,.0f} | payback {x['payback']} desc {x['payback_descontado_selic+6']} | anos {x['fluxo_anual']}")
    if a.json:
        Path(a.json).write_text(json.dumps(out, ensure_ascii=False, indent=1, default=float), encoding="utf-8")


if __name__ == "__main__":
    main()
