"""Verifica se as URLs do catlogo.yml respondem."""

import sys

import requests
import yaml

def main() -> None:
    with open("catalog.yml", encoding="utf-8") as arquivo:
        catalogo = yaml.safe_load(arquivo)

    falhas = []
    for item in catalogo:
        try:
            resp = requests.get(
                item["url"],
                timeout=30,
                stream=True,
                headers={"User-Agent": "dsa-checagem-de-links"},
                )
            status = resp.status_code
        except requests.RequestException as erro:
            status = f"erro: {erro.__class__.__name__}"

        ok = isinstance(status, int) and status < 400
        print(f"{'OK ' if ok else 'FALHA'} {item['id']}: {status}")
        if not ok:
            falhas.append(item["id"])

        if falhas:
            sys.exit(f"Links com problema: {', '.join(falhas)}")

if __name__=="__main__":
    main()