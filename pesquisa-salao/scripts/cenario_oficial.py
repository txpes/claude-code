"""Cenário oficial do estudo (decisões tomadas em 03/11/2026) e FCD de 5 anos.

Decisões (justificativa em relatorios/decisoes_do_estudo.md):
  D1 região Tijuca; sala-base T1 (Afonso Pena 101, R$ 4.288/mês, valor fechado no anúncio)
  D2 retirada da Manon: R$ 1.650 nos meses 1-6, R$ 5.000 a partir do mês 7
  D3 repasse da manicure: salão fica com 50% (plano 45%, mercado 60%)
  D4 taxa de cartão descontada antes da divisão: 1,6% sobre a cota
  D5 investimento de montagem R$ 87 mil (equipamentos cotados + faltantes; obra R$ 25 mil)
  D6 funding: mútuo do Thomás R$ 120 mil a CDI, carência 15 meses
  D7 taxa de desconto: Selic + 12 p.p.; 5 anos; sem valor terminal
  D8 riscos que o simulador não tem: aluguel sobe 5%/ano acima da inflação a partir do
     mês 13; reposição de equipamentos de R$ 10 mil no mês 42
Uso: python scripts/cenario_oficial.py
"""
import json, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts")); sys.path.insert(0, str(RAIZ / "simulador"))
import fcd, simulador as s  # noqa: E402

SALA = 4288
MUTUO, CARENCIA = 120000, 15
CDI = 0.1365
ALUGUEL_REAL_AA, ALUGUEL_PARTE = 0.05, 3600   # só o aluguel é reajustado acima do IPCA
REPOSICAO, MES_REPOSICAO = 10000, 42


def premissas():
    v = s.carregar(RAIZ / "simulador" / "premissas_validadas.yaml")
    return s.aplicar_overrides(fcd.com_sala(v, SALA), {
        "pro_labore_minimo": 1650, "pro_labore_cheio": 5000,
        "cotas": {"manicure": 0.50, "manicure_f2": 0.50},
        "taxa_cartao": 0.016, "investimento_montagem": 87000})


def fluxo_ajustado(p, cenario="base", riscos=True):
    f, r = fcd.fluxos(p, cenario)
    if riscos:
        for t in range(13, 61):
            anos = (t - 1) // 12
            f[t] -= ALUGUEL_PARTE * ((1 + ALUGUEL_REAL_AA) ** anos - 1)
        f[MES_REPOSICAO] -= REPOSICAO
    return f, r


def indicadores(f):
    tm = fcd.tir(f)
    nom = None if tm is None else ((1 + tm) ** 12) * (1 + fcd.IPCA) - 1
    taxa = (1 + fcd.SELIC + 0.12) / (1 + fcd.IPCA) - 1
    vpl = sum(x / (1 + taxa) ** (t / 12) for t, x in enumerate(f))
    ac, pb, pior = 0, None, 0
    for t, x in enumerate(f):
        ac += x; pior = min(pior, ac)
        if pb is None and t > 0 and ac >= 0:
            pb = t
    return {"tir_nominal": nom, "vpl_25_75": vpl, "payback": pb, "pior_caixa": pior,
            "anos": [round(sum(f[1 + 12 * a:13 + 12 * a])) for a in range(5)], "investimento": -f[0]}


def caixa_empresa(f):
    i = (1 + CDI) ** (1 / 12) - 1
    saldo = MUTUO * (1 + i) ** CARENCIA
    n = 60 - CARENCIA
    pmt = saldo * i / (1 - (1 + i) ** -n)
    caixa, mn = MUTUO, 1e12
    for t, x in enumerate(f):
        caixa += x - (pmt if t > CARENCIA else 0)
        mn = min(mn, caixa)
    return pmt, mn, caixa


def main():
    p = premissas()
    out = {}
    for c in ["base", "rampa_lenta", "fat_menor", "obra_cara", "sem_aumento", "tudo_junto"]:
        f, r = fluxo_ajustado(p, c)
        ind = indicadores(f)
        pmt, mn, fim = caixa_empresa(f)
        ind.update({"parcela_mutuo": pmt, "menor_caixa_empresa_com_mutuo": mn, "caixa_final": fim,
                    "lucro_maduro_mes60": r["meses"][-1]["resultado"]})
        out[c] = ind
        t = "negativa" if ind["tir_nominal"] is None or ind["tir_nominal"] < 0 else f"{ind['tir_nominal']:.0%}"
        print(f"{c:12s} TIR {t:>9} | VPL {ind['vpl_25_75']:>10,.0f} | payback {ind['payback']} | pior {ind['pior_caixa']:>10,.0f} | "
              f"menor caixa c/ mútuo {mn:>10,.0f} | anos {ind['anos']}")
    f0, _ = fluxo_ajustado(p, "base", riscos=False)
    out["base_sem_riscos_extras"] = indicadores(f0)
    print("base sem os riscos extras:", f"{out['base_sem_riscos_extras']['tir_nominal']:.0%}")
    print("equilíbrio maduro:", f"{s.ocupacao_equilibrio(p):.1%}", "| parcela do mútuo:", f"{out['base']['parcela_mutuo']:,.0f}")
    (RAIZ / "dados" / "cenario_oficial.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=float), encoding="utf-8")


if __name__ == "__main__":
    main()
