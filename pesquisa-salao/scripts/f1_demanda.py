"""F1 — Demanda: público num raio de 800 m de cada ponto candidato.

Fonte: Data.Rio / IPP, camada "Censo Demográfico 2022 - Setores" (IBGE, agregados por
setor censitário). Para cada setor que toca o círculo de 800 m, soma-se a população
proporcional à fração da área do setor dentro do círculo (hipótese de densidade uniforme
dentro do setor). Mulheres de 20 a 69 anos = pessoas de 20 a 69 × fração feminina do setor
(o setor não cruza sexo × idade).

Gasto: POF 2017-2018 (IBGE, SIDRA tabela 6715, UF Rio de Janeiro): cabeleireiro R$ 30,96 +
manicuro e pedicuro R$ 11,22 por família/mês (ref. jan/2018), corrigido pelo IPCA
(BCB SGS 433, fev/2018 a set/2026: fator 1,5608).

Uso: python scripts/f1_demanda.py   (grava dados/bairros.csv e dados/f1_raio800.json)
"""
import csv, json, math, sys, urllib.parse, urllib.request
from pathlib import Path

from shapely.geometry import Point, shape
from shapely.ops import transform

RAIZ = Path(__file__).resolve().parent.parent
URL = ("https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Hosted/"
       "Mapa_Rio_Camada_Censo_Demogr%C3%A1fico_Setores/FeatureServer/0/query")
PONTOS = {  # coordenadas OSM/Nominatim (acesso 2026-11-03)
    "R1 Tijuca (Afonso Pena)": (-22.9184484, -43.2177451),
    "R2 Copacabana (Cardeal Arcoverde–Siqueira Campos)": ((-22.9638248 - 22.9673066) / 2,
                                                         (-43.1813721 - 43.1873375) / 2),
    "R3 Humaitá (Largo dos Leões) — referência": (-22.9533219, -43.1966495),
}
RAIO = 800
GASTO_FAMILIA_MES_2018 = 30.96 + 11.22
IPCA = 1.5608
FAT_ANUAL_PLANO = 940000
CAMPOS_IDADE_20_69 = ["f20_a_24_an", "f25_a_29_an", "f30_a_39_an", "f40_a_49_an", "f50_a_59_an", "f60_a_69_an"]


def consulta(params):
    params = {"f": "geojson", "outSR": 4326, **params}
    with urllib.request.urlopen(URL + "?" + urllib.parse.urlencode(params), timeout=120) as r:
        return json.load(r)


def todos_setores_sem_geo():
    feats, off = [], 0
    while True:
        d = consulta({"where": "1=1", "outFields": "total_de_p,total_de_3,valor_do_r,sexo_femin",
                      "returnGeometry": "false", "resultOffset": off, "resultRecordCount": 2000})
        fs = d.get("features", [])
        feats += fs
        if len(fs) < 2000:
            return feats
        off += 2000


def projetor(lat0, lon0):
    k = 111320.0
    return lambda x, y, z=None: ((x - lon0) * k * math.cos(math.radians(lat0)), (y - lat0) * 110540.0)


def main():
    # renda média do município (ponderada por domicílios ocupados) para o ajuste de renda
    cid = todos_setores_sem_geo()
    num = sum((f["properties"]["valor_do_r"] or 0) * (f["properties"]["total_de_3"] or 0) for f in cid
              if f["properties"]["valor_do_r"])
    den = sum((f["properties"]["total_de_3"] or 0) for f in cid if f["properties"]["valor_do_r"])
    renda_cidade = num / den
    gasto_ano_dom = GASTO_FAMILIA_MES_2018 * IPCA * 12
    saida = {"renda_media_responsavel_cidade": renda_cidade, "gasto_ano_domicilio_2026": gasto_ano_dom,
             "n_setores_cidade": len(cid), "regioes": {}}
    for nome, (lat, lon) in PONTOS.items():
        d = 0.012
        env = f"{lon-d},{lat-d},{lon+d},{lat+d}"
        fc = consulta({"where": "1=1", "outFields": "*", "geometry": env, "geometryType": "esriGeometryEnvelope",
                       "inSR": 4326, "spatialRel": "esriSpatialRelIntersects", "resultRecordCount": 2000})
        proj = projetor(lat, lon)
        circ = Point(0, 0).buffer(RAIO, 128)
        acc = {k: 0.0 for k in ["pop", "fem", "m20_69", "p20_69", "p60", "dom", "renda_x_dom", "dom_renda"]}
        bairros = {}
        for f in fc["features"]:
            g = transform(proj, shape(f["geometry"]))
            if not g.intersects(circ):
                continue
            frac = g.intersection(circ).area / g.area if g.area else 0
            pr = f["properties"]
            pop = pr["total_de_p"] or 0
            fem = pr["sexo_femin"] or 0
            p2069 = sum(pr[c] or 0 for c in CAMPOS_IDADE_20_69)
            p60 = (pr["f60_a_69_an"] or 0) + (pr["f70_anos_ou"] or 0)
            dom = pr["total_de_3"] or 0
            acc["pop"] += pop * frac
            acc["fem"] += fem * frac
            acc["p20_69"] += p2069 * frac
            acc["m20_69"] += p2069 * (fem / pop if pop else 0) * frac
            acc["p60"] += p60 * frac
            acc["dom"] += dom * frac
            if pr["valor_do_r"]:
                acc["renda_x_dom"] += pr["valor_do_r"] * dom * frac
                acc["dom_renda"] += dom * frac
            bairros[pr["bairro"]] = bairros.get(pr["bairro"], 0) + pop * frac
        renda = acc["renda_x_dom"] / acc["dom_renda"]
        mercado_baixo = acc["dom"] * gasto_ano_dom
        mercado_alto = mercado_baixo * renda / renda_cidade
        saida["regioes"][nome] = {
            "lat": lat, "lon": lon, "pop_total": round(acc["pop"]), "mulheres": round(acc["fem"]),
            "mulheres_20_69": round(acc["m20_69"]), "pct_60_mais": acc["p60"] / acc["pop"],
            "domicilios": round(acc["dom"]), "renda_media_responsavel": renda,
            "mercado_ano_sem_ajuste": mercado_baixo, "mercado_ano_ajustado_renda": mercado_alto,
            "gasto_ano_por_mulher_20_69_sem_ajuste": mercado_baixo / acc["m20_69"],
            "gasto_ano_por_mulher_20_69_ajustado": mercado_alto / acc["m20_69"],
            "fatia_necessaria_sem_ajuste": FAT_ANUAL_PLANO / mercado_baixo,
            "fatia_necessaria_ajustada": FAT_ANUAL_PLANO / mercado_alto,
            "bairros_no_raio": {k: round(v) for k, v in sorted(bairros.items(), key=lambda x: -x[1])},
        }
    (RAIZ / "dados" / "f1_raio800.json").write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(saida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
