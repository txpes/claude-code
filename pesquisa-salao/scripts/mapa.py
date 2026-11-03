"""Gera mapas/mapa_concorrencia.html: pontos candidatos, raio de 800 m, concorrentes e metrô.
Uso: python scripts/mapa.py"""
import csv, json
from pathlib import Path
import folium

RAIZ = Path(__file__).resolve().parent.parent
f1 = json.loads((RAIZ / "dados" / "f1_raio800.json").read_text(encoding="utf-8"))
m = folium.Map(location=[-22.94, -43.20], zoom_start=13, tiles="cartodbpositron")
# estações (OSM/Nominatim)
ESTACOES = {"Afonso Pena": (-22.9184484, -43.2177451), "Saens Peña": (-22.9241676, -43.2325745),
            "Cardeal Arcoverde": (-22.9638248, -43.1813721), "Siqueira Campos": (-22.9673066, -43.1873375)}
for n, (la, lo) in ESTACOES.items():
    folium.CircleMarker([la, lo], radius=6, color="#1f4e9c", fill=True, fill_opacity=1,
                        tooltip=f"Metrô {n}").add_to(m)
for nome, r in f1["regioes"].items():
    folium.Circle([r["lat"], r["lon"]], radius=800, color="#1f4e9c", fill=True, fill_opacity=0.06,
                  tooltip=(f"{nome}: {r['mulheres_20_69']:,} mulheres 20–69; renda média resp. "
                           f"R$ {r['renda_media_responsavel']:,.0f}; fatia necessária "
                           f"{r['fatia_necessaria_ajustada']:.1%}–{r['fatia_necessaria_sem_ajuste']:.1%}")).add_to(m)
folium.Marker([-22.9533219, -43.1966495], tooltip="Largo dos Leões (casa — referência de deslocamento)",
              icon=folium.Icon(color="green", icon="home")).add_to(m)
cores = {"esmalteria": "red", "salão": "orange", "estúdio de cílios": "purple", "estúdio de sobrancelha": "purple",
         "spa/estética": "pink", "estética": "pink", "estúdio": "beige", "podologia": "gray"}
for c in csv.DictReader(open(RAIZ / "dados" / "concorrentes.csv", encoding="utf-8")):
    if not c["lat"]:
        continue
    folium.Marker([float(c["lat"]), float(c["lon"])], tooltip=f"{c['id']} {c['nome']} ({c['tipo']})",
                  popup=folium.Popup(f"<b>{c['nome']}</b><br>{c['endereco']}<br>{c['observacao']}", max_width=320),
                  icon=folium.Icon(color=cores.get(c["tipo"], "blue"), icon="scissors", prefix="fa")).add_to(m)
for i in csv.DictReader(open(RAIZ / "dados" / "imoveis.csv", encoding="utf-8")):
    if i["lat"]:
        folium.Marker([float(i["lat"]), float(i["lon"])], tooltip=f"Imóvel {i['id']}",
                      icon=folium.Icon(color="darkblue", icon="building", prefix="fa")).add_to(m)
legenda = ("<div style='position:fixed;bottom:20px;left:20px;z-index:9999;background:#fff;padding:8px 10px;"
           "border:1px solid #999;font:12px sans-serif'><b>Salão da Manon — F2/F3</b><br>Círculos: raio de 800 m<br>"
           "Azul: metrô · Verde: Largo dos Leões<br>Vermelho: esmalteria · Laranja: salão · Roxo: cílios/sobrancelha"
           "<br>Concorrentes sem número de porta geocodificável não aparecem (ver concorrentes.csv)</div>")
m.get_root().html.add_child(folium.Element(legenda))
(RAIZ / "mapas").mkdir(exist_ok=True)
m.save(str(RAIZ / "mapas" / "mapa_concorrencia.html"))
print("ok")
