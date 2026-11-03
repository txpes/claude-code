"""Testes de aceitação do Apêndice A (com premissas.yaml; tolerância de R$ 5)."""
from pathlib import Path
import sys

import pytest

AQUI = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AQUI))
import simulador as s  # noqa: E402

TOL = 5


@pytest.fixture(scope="module")
def p():
    return s.carregar(AQUI / "premissas.yaml")


def r(p, nome):
    return s.rodar_cenario(p, nome)["resumo"]


def test_base(p):
    b = r(p, "base")
    assert b["pior_caixa"] == pytest.approx(-78746, abs=TOL)
    assert b["mes_pior_caixa"] == 2
    assert b["payback"] == 14
    assert b["caixa_mes_36"] == pytest.approx(318736, abs=TOL)
    assert b["lucro_maduro"] == pytest.approx(14274, abs=TOL)
    assert round(b["margem_madura"], 3) == 0.183
    assert b["mes_expansao"] == 8
    assert b["mes_recepcionista_fixa"] == 12
    assert b["mes_segundo_turno"] == 13


def test_rampa_lenta(p):
    c = r(p, "rampa_lenta")
    assert c["pior_caixa"] == pytest.approx(-84479, abs=TOL)
    assert c["payback"] == 22
    assert c["revisao"] is True


def test_fat_menor(p):
    c = r(p, "fat_menor")
    assert c["pior_caixa"] == pytest.approx(-86089, abs=TOL)
    assert c["payback"] == 21
    assert c["revisao"] is True


def test_obra_cara(p):
    c = r(p, "obra_cara")
    assert c["pior_caixa"] == pytest.approx(-93546, abs=TOL)
    assert c["payback"] == 15


def test_tudo_junto(p):
    assert r(p, "tudo_junto")["mes_parada"] == 6


def test_sem_aumento(p):
    c = r(p, "sem_aumento")
    assert c["pior_caixa"] == pytest.approx(-80050, abs=TOL)
    assert c["payback"] == 16
    assert c["lucro_maduro"] == pytest.approx(12232, abs=TOL)


def test_salao_maduro(p):
    assert s.salao_maduro(p, 0.70) == pytest.approx(5648, abs=TOL)
    assert s.salao_maduro(p, 0.90) == pytest.approx(11308, abs=TOL)
    eq = s.ocupacao_equilibrio(p)
    assert round(eq, 3) == 0.507
    assert round(eq * 100) == 51


def test_escada(p):
    assert s.escada_ancora(p, 20000) == pytest.approx(11750, abs=TOL)
    assert s.escada_ancora(p, 20000) / 20000 == pytest.approx(0.5875, abs=1e-6)


def test_nenhum_numero_no_codigo():
    """Garante que os números de negócio não estão fixos no código."""
    fonte = (AQUI / "simulador.py").read_text(encoding="utf-8")
    for n in ["12000", "0.43", "8700", "9100", "74000", "0.08", "2900", "1650", "4000"]:
        assert n not in fonte, n


def test_excel(p, tmp_path):
    out = tmp_path / "s.xlsx"
    s.gerar_excel(p, out, p)
    import openpyxl
    abas = openpyxl.load_workbook(out).sheetnames
    for a in ["Premissas", "Cenarios", "Alavancas", "Ocupacao", "Sensibilidade", "Escada", "Comparacao"]:
        assert a in abas
