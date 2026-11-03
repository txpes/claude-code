"""F2 — preços publicados nas páginas públicas de unidades da rede Unhas Cariocas.
Lê só a vitrine pública (unidades.unhascariocas.com.br/<código>), uma página por unidade.
Saída: imprime (unidade, serviço, preço) para os serviços equivalentes ao Apêndice B.
"""
import html, re, sys, time, urllib.request, json

UNIDADES = {"rtb": ("R1", "Unhas Cariocas Tijuca Conde de Bonfim"),
            "str": ("R1", "Unhas Cariocas Shopping Tijuca"),
            "rbp": ("R3", "Unhas Cariocas Botafogo Praia Shopping")}
MAPA = {  # nome no site (minúsculas, contém) -> código do Apêndice B
    "UNH01": [r"^manicure$", r"^m[aã]o$", r"^manicure tradicional", r"^m[aã]o tradicional"],
    "UNH02": [r"^pedicure$", r"^p[eé]$", r"^pedicure tradicional", r"^p[eé] tradicional"],
    "UNH03": [r"^p[eé] e m[aã]o$", r"^m[aã]o e p[eé]$", r"^manicure e pedicure$", r"^p[eé] e m[aã]o tradicional", r"^p[eé] \+ m[aã]o$"],
    "UNH04": [r"^esmalta[cç][aã]o em gel m[aã]os \(com cutilagem\)"],
    "UNH05": [r"^alongamento de fibra de vidro$", r"^alongamento gel moldado$"],
    "UNH06": [r"spa dos p[eé]s"],
}

def main():
    out = []
    for cod, (reg, nome) in UNIDADES.items():
        url = f"https://unidades.unhascariocas.com.br/{cod}"
        t = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8", "ignore")
        x = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
        x = html.unescape(re.sub(r"<[^>]+>", "|", x))
        x = re.sub(r"\s*\|[\s|]*", "|", x)
        pares = re.findall(r"\|([^|]{2,80})\|R\$ ?([\d.]+,\d{2})\|", x)
        for serv, preco in pares:
            s = serv.strip().lower()
            for codb, pats in MAPA.items():
                if any(re.search(p, s) for p in pats):
                    out.append({"unidade": nome, "regiao": reg, "url": url, "servico_site": serv.strip(),
                                "servico_codigo": codb, "preco": float(preco.replace(".", "").replace(",", "."))})
        time.sleep(3)
    print(json.dumps(out, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
