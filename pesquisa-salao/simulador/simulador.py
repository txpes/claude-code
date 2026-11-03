"""Simulador de viabilidade do Salão da Manon (Apêndice A do briefing).

Modelo salão-parceiro, Simples Nacional, abertura em fases com gatilhos.
Nenhum número de negócio fica no código: tudo vem do YAML de premissas.

Uso:
    python simulador.py --premissas premissas.yaml --saida saida/simulacao.xlsx
    python simulador.py --premissas premissas.yaml \
        --comparar premissas_validadas.yaml --saida saida/simulacao.xlsx
"""
from __future__ import annotations

import argparse
import copy
from pathlib import Path

import yaml


# --------------------------------------------------------------------------- #
# Leitura e cenários
# --------------------------------------------------------------------------- #
def carregar(caminho: str | Path) -> dict:
    with open(caminho, encoding="utf-8") as f:
        dados = yaml.safe_load(f)
    # premissas_validadas.yaml guarda {valor, fonte, confianca}; extrai o valor.
    return _extrair_valores(dados)


def _extrair_valores(obj):
    if isinstance(obj, dict):
        if "valor" in obj and set(obj) <= {"valor", "fonte", "fontes", "confianca", "justificativa", "plano", "data"}:
            return _extrair_valores(obj["valor"])
        return {k: _extrair_valores(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_extrair_valores(v) for v in obj]
    return obj


def aplicar_cenario(p: dict, nome: str) -> dict:
    """Devolve uma cópia das premissas com o cenário de estresse aplicado."""
    q = copy.deepcopy(p)
    c = p["cenarios"].get(nome, {})
    q["_mult_ocup"] = c.get("multiplicador_ocupacao", 1.0)
    q["_teto_ocup"] = c.get("teto_ocupacao", None)
    if "fator_preco_mult" in c:
        q["fator_preco"] = p["fator_preco"] * c["fator_preco_mult"]
    if "fator_preco" in c:
        q["fator_preco"] = c["fator_preco"]
    if "investimento_mult" in c:
        q["investimento_montagem"] = p["investimento_montagem"] * c["investimento_mult"]
    return q


def aplicar_overrides(p: dict, ov: dict) -> dict:
    q = copy.deepcopy(p)
    for k, v in ov.items():
        if k == "cotas":
            for g in q["postos_fase1"] + q["postos_fase2"]:
                if g["grupo"] in v:
                    g["cota_salao"] = v[g["grupo"]]
        else:
            q[k] = v
    return q


# --------------------------------------------------------------------------- #
# Cálculo
# --------------------------------------------------------------------------- #
def aliquota_efetiva(rbt12: float, tabela: list) -> float:
    if rbt12 <= 0:
        return tabela[0][1]
    for limite, nominal, deducao in tabela:
        if rbt12 <= limite:
            return (rbt12 * nominal - deducao) / rbt12
    limite, nominal, deducao = tabela[-1]
    return (rbt12 * nominal - deducao) / rbt12


def _ocup(p: dict, rampa: list, depois: float, i: int) -> float:
    """i = índice 0-based na rampa."""
    base = rampa[i] if i < len(rampa) else depois
    v = base * p.get("_mult_ocup", 1.0)
    teto = p.get("_teto_ocup")
    if teto is not None:
        v = min(v, teto)
    return v


def _faturamento_grupos(p, grupos, ocup, turno_ativo):
    fat = cota = 0.0
    for g in grupos:
        turno = 1 + p["segundo_turno"] if (turno_ativo and g["tipo"] in p["segundo_turno_tipos"]) else 1
        f = g["qtd"] * g["fat_maduro"] * ocup * (1 - p["faltas"]) * p["fator_preco"] * turno
        fat += f
        cota += f * g["cota_salao"]
    return fat, cota


def simular(p: dict) -> dict:
    """Simula mês a mês. Devolve {'meses': [...], 'resumo': {...}}."""
    g = p["gatilhos"]
    n = p["horizonte_meses"]
    caixa = -p["investimento_montagem"]
    meses = []
    ocup_f1_hist = {}
    caixa_hist = {0: caixa}
    mes_expansao = None
    mes_fixa = None          # mês a partir do qual a recepcionista é fixa
    mes_turno = None
    revisao = False
    mes_parada = None

    for m in range(1, n + 1):
        f1 = _ocup(p, p["rampa_fase1"], p["rampa_fase1_depois"], m - 1)
        ocup_f1_hist[m] = f1

        # gatilho de expansão (avaliado no início do mês m)
        if (mes_expansao is None and m >= g["expansao_mes_minimo"]
                and ocup_f1_hist[m - 1] >= g["expansao_ocupacao_f1"]
                and ocup_f1_hist[m - 2] >= g["expansao_ocupacao_f1"]
                and caixa_hist[m - 1] > g["expansao_caixa_minimo"]):
            mes_expansao = m
        expandido = mes_expansao is not None
        f2 = _ocup(p, p["rampa_fase2"], p["rampa_fase2_depois"], m - mes_expansao) if expandido else 0.0

        # gatilho do segundo turno
        if (mes_turno is None and m >= g["segundo_turno_mes_minimo"]
                and f1 >= g["segundo_turno_ocupacao_f1"]):
            mes_turno = m
        turno_ativo = mes_turno is not None

        fat1, cota1 = _faturamento_grupos(p, p["postos_fase1"], f1, turno_ativo)
        fat2, cota2 = _faturamento_grupos(p, p["postos_fase2"], f2, turno_ativo) if expandido else (0.0, 0.0)
        faturamento = fat1 + fat2
        cota = cota1 + cota2

        varejo = p["varejo_mes_maduro"] * f1
        ociosas = p["horas_ociosas"] if m >= p["horas_ociosas_mes_inicio"] else 0.0
        rbt12 = (cota + varejo + ociosas) * 12
        aliq3 = aliquota_efetiva(rbt12, p["anexo_III"])
        aliq1 = aliquota_efetiva(rbt12, p["anexo_I"])
        aliq_varejo = aliq3 if p.get("varejo_no_anexo_III") else aliq1

        margem = (cota * (1 - aliq3 - p["taxa_cartao"])
                  - faturamento * p["produtos"]
                  + varejo * (p["margem_varejo"] - aliq_varejo)
                  + ociosas * (1 - aliq3))

        ano1 = m <= p["meses_ano1"]
        fixos = ((p["fixos_fase2"] if expandido else p["fixos_fase1"]) + p["fixos_extras"]
                 + (p["extra_ano1"] if ano1 else 0)
                 - (p["desconto_aluguel_ano1"] if ano1 else 0)
                 + (p["segundo_turno_custo_fixo"] if turno_ativo else 0))

        recepcao = p["recepcionista_fixa"] if (mes_fixa is not None and m >= mes_fixa) else p["recepcao_intermitente"]

        lim_pl = p["pro_labore_minimo_ate_mes_revisao"] if revisao else p["pro_labore_minimo_ate_mes"]
        pro_labore = p["pro_labore_minimo"] if m <= lim_pl else p["pro_labore_cheio"]

        capex = p["capex_fase2"] if m == mes_expansao else 0.0
        resultado = margem - fixos - recepcao - pro_labore - capex
        caixa += resultado
        caixa_hist[m] = caixa

        # gatilhos avaliados ao fim do mês
        if m == g["revisao_mes"] and faturamento < g["revisao_faturamento_minimo"]:
            revisao = True
        if mes_fixa is None and expandido:
            pf1, pf2 = g["recepcao_postos_f1"], g["recepcao_postos_f2"]
            if (pf1 * f1 + pf2 * f2) / (pf1 + pf2) > g["recepcao_ocupacao"]:
                mes_fixa = m + 1
        if (mes_parada is None and m >= g["parada_mes_minimo"]
                and caixa <= g["parada_caixa"] and resultado < 0):
            mes_parada = m

        meses.append({
            "mes": m, "ocupacao_f1": f1, "ocupacao_f2": f2, "expandido": expandido,
            "segundo_turno": turno_ativo, "faturamento": faturamento, "cota_salao": cota,
            "varejo": varejo, "horas_ociosas": ociosas, "rbt12": rbt12,
            "aliquota_III": aliq3, "aliquota_I": aliq1, "margem": margem, "fixos": fixos,
            "recepcao": recepcao, "pro_labore": pro_labore, "capex_fase2": capex,
            "resultado": resultado, "caixa_acumulado": caixa,
        })

    pior_mes = min(caixa_hist, key=lambda k: caixa_hist[k])
    payback = next((m for m in range(1, n + 1) if caixa_hist[m] >= 0), None)
    ult = meses[-1]
    resumo = {
        "pior_caixa": caixa_hist[pior_mes], "mes_pior_caixa": pior_mes,
        "payback": payback, "caixa_mes_36": caixa_hist[n],
        "lucro_maduro": ult["resultado"],
        "margem_madura": ult["resultado"] / ult["faturamento"] if ult["faturamento"] else 0.0,
        "faturamento_maduro": ult["faturamento"],
        "mes_expansao": mes_expansao, "mes_recepcionista_fixa": mes_fixa,
        "mes_segundo_turno": mes_turno, "revisao": revisao, "mes_parada": mes_parada,
    }
    return {"meses": meses, "resumo": resumo}


def rodar_cenario(p: dict, nome: str) -> dict:
    return simular(aplicar_cenario(p, nome))


# --------------------------------------------------------------------------- #
# Salão maduro, sensibilidade, escada, alavancas
# --------------------------------------------------------------------------- #
def salao_maduro(p: dict, ocup: float) -> float:
    """Lucro mensal com 8 postos na mesma ocupação, sem segundo turno."""
    q = copy.deepcopy(p)
    fat, cota = _faturamento_grupos(q, q["postos_fase1"] + q["postos_fase2"], ocup, False)
    varejo = q["salao_maduro"]["varejo_base"] * ocup
    ociosas = q["horas_ociosas"]
    rbt12 = (cota + varejo + ociosas) * 12
    a3 = aliquota_efetiva(rbt12, q["anexo_III"])
    a1 = aliquota_efetiva(rbt12, q["anexo_I"])
    av = a3 if q.get("varejo_no_anexo_III") else a1
    margem = (cota * (1 - a3 - q["taxa_cartao"]) - fat * q["produtos"]
              + varejo * (q["margem_varejo"] - av) + ociosas * (1 - a3))
    return margem - (q["fixos_fase2"] + q["fixos_extras"]) - q["recepcionista_fixa"] - q["pro_labore_cheio"]


def ocupacao_equilibrio(p: dict) -> float:
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if salao_maduro(p, mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def sensibilidade(p: dict) -> list[dict]:
    s = p["sensibilidade"]
    linhas = []
    for fat in range(s["fat_cabeleireira_de"], s["fat_cabeleireira_ate"] + 1, s["fat_cabeleireira_passo"]):
        q = copy.deepcopy(p)
        for g in q["postos_fase1"] + q["postos_fase2"]:
            if g["tipo"] == "cabelo":
                g["fat_maduro"] = fat
        r = simular(aplicar_cenario(q, "base"))["resumo"]
        linhas.append({"fat_cabeleireira": fat, "lucro_maduro": r["lucro_maduro"],
                       "payback": r["payback"], "pior_caixa": r["pior_caixa"]})
    return linhas


def escada_ancora(p: dict, faturamento: float) -> float:
    """Quanto a âncora recebe, por faixa (como imposto de renda)."""
    recebe, piso = 0.0, 0.0
    for limite, pct in p["escada_ancora"]["faixas"]:
        topo = faturamento if limite is None else min(faturamento, limite)
        if topo > piso:
            recebe += (topo - piso) * pct
        if limite is None or faturamento <= limite:
            break
        piso = limite
    return recebe


def alavancas(p: dict) -> list[dict]:
    base = rodar_cenario(p, "base")["resumo"]
    linhas = []
    for nome, ov in p.get("alavancas", {}).items():
        r = rodar_cenario(aplicar_overrides(p, ov), "base")["resumo"]
        linhas.append({"alavanca": nome, "lucro_com": base["lucro_maduro"], "lucro_sem": r["lucro_maduro"],
                       "efeito": base["lucro_maduro"] - r["lucro_maduro"],
                       "payback_com": base["payback"], "payback_sem": r["payback"]})
    return linhas


# --------------------------------------------------------------------------- #
# Saída
# --------------------------------------------------------------------------- #
def _achatar(prefixo, obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            _achatar(f"{prefixo}.{k}" if prefixo else k, v, out)
    elif isinstance(obj, list) and obj and isinstance(obj[0], dict):
        for i, v in enumerate(obj):
            _achatar(f"{prefixo}[{v.get('grupo', i)}]", v, out)
    else:
        out[prefixo] = obj if not isinstance(obj, list) else str(obj)


def gerar_excel(p: dict, saida: str | Path, p_validado: dict | None = None) -> None:
    import pandas as pd

    saida = Path(saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    plano = {}
    _achatar("", {k: v for k, v in p.items() if not k.startswith("_")}, plano)

    with pd.ExcelWriter(saida, engine="openpyxl") as xw:
        pd.DataFrame({"premissa": list(plano), "valor": list(plano.values())}).to_excel(xw, sheet_name="Premissas", index=False)
        cen = []
        for nome in p["cenarios"]:
            r = rodar_cenario(p, nome)
            pd.DataFrame(r["meses"]).to_excel(xw, sheet_name=f"Mensal_{nome}"[:31], index=False)
            cen.append({"cenario": nome, **r["resumo"]})
        pd.DataFrame(cen).to_excel(xw, sheet_name="Cenarios", index=False)
        pd.DataFrame(alavancas(p)).to_excel(xw, sheet_name="Alavancas", index=False)
        oc = [{"ocupacao": o, "lucro_mensal": salao_maduro(p, o)} for o in p["salao_maduro"]["ocupacoes_relatorio"]]
        oc.append({"ocupacao": ocupacao_equilibrio(p), "lucro_mensal": 0.0, "nota": "equilíbrio"})
        pd.DataFrame(oc).to_excel(xw, sheet_name="Ocupacao", index=False)
        pd.DataFrame(sensibilidade(p)).to_excel(xw, sheet_name="Sensibilidade", index=False)
        esc = [{"faturamento_ancora": f, "ancora_recebe": escada_ancora(p, f),
                "pct_ancora": escada_ancora(p, f) / f}
               for f in p["escada_ancora"]["faturamentos_exemplo"]]
        pd.DataFrame(esc).to_excel(xw, sheet_name="Escada", index=False)
        if p_validado is not None:
            comparar(p, p_validado).to_excel(xw, sheet_name="Comparacao", index=False)


def comparar(p: dict, pv: dict):
    import pandas as pd
    linhas = []
    for nome in p["cenarios"]:
        a = rodar_cenario(p, nome)["resumo"]
        b = rodar_cenario(pv, nome)["resumo"]
        for k in ["pior_caixa", "mes_pior_caixa", "payback", "caixa_mes_36", "lucro_maduro",
                  "margem_madura", "mes_expansao", "mes_recepcionista_fixa", "mes_segundo_turno",
                  "revisao", "mes_parada"]:
            va, vb = a[k], b[k]
            dif = (vb - va) if isinstance(va, (int, float)) and isinstance(vb, (int, float)) \
                and not isinstance(va, bool) else None
            linhas.append({"cenario": nome, "resultado": k, "plano": va, "validado": vb, "diferenca": dif})
    linhas.append({"cenario": "salao_maduro", "resultado": "ocupacao_equilibrio",
                   "plano": ocupacao_equilibrio(p), "validado": ocupacao_equilibrio(pv),
                   "diferenca": ocupacao_equilibrio(pv) - ocupacao_equilibrio(p)})
    return pd.DataFrame(linhas)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--premissas", required=True)
    ap.add_argument("--comparar", help="premissas_validadas.yaml para a aba Comparacao")
    ap.add_argument("--saida", default="saida/simulacao.xlsx")
    a = ap.parse_args()
    p = carregar(a.premissas)
    pv = carregar(a.comparar) if a.comparar else None
    gerar_excel(p, a.saida, pv)
    for nome in p["cenarios"]:
        r = rodar_cenario(p, nome)["resumo"]
        print(f"{nome:12s} pior caixa {r['pior_caixa']:>10,.0f} (mês {r['mes_pior_caixa']})  "
              f"payback {r['payback']}  caixa36 {r['caixa_mes_36']:>10,.0f}  "
              f"lucro maduro {r['lucro_maduro']:>8,.0f} ({r['margem_madura']:.1%})  "
              f"exp {r['mes_expansao']} fixa {r['mes_recepcionista_fixa']} turno {r['mes_segundo_turno']} "
              f"revisão {r['revisao']} parada {r['mes_parada']}")
    print(f"salão maduro: 70% {salao_maduro(p, .7):,.0f}  90% {salao_maduro(p, .9):,.0f}  "
          f"equilíbrio {ocupacao_equilibrio(p):.3f}")
    print(f"Arquivo: {a.saida}")


if __name__ == "__main__":
    main()
