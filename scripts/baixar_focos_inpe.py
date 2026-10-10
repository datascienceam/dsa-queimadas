"""Baixa focos de calor mensais do INPE e filtra por bioma e satélite."""
import argparse
import unicodedata
from pathlib import Path

import pandas as pd
import requests

BASE_URL = (
    "https://dataserver-coids.inpe.br/queimadas/queimadas/"
    "focos/csv/mensal/Brasil"
)
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def slug(texto: str) -> str:
    """Remove acentos e espaços para usar o texto em nomes de arquivo."""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return sem_acento.lower().replace(" ", "_")


def baixar_mes(ano: int, mes: int) -> Path:
    """Baixa o CSV de um mês (ou reaproveita se já existir)."""
    nome = f"focos_mensal_br_{ano}{mes:02d}.csv"
    destino = RAW_DIR / nome
    if destino.exists():
        return destino
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    resp = requests.get(f"{BASE_URL}/{nome}", timeout=60)
    resp.raise_for_status()
    destino.write_bytes(resp.content)
    return destino


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ano", type=int, required=True)
    parser.add_argument("--meses", type=int, nargs="+", default=list(range(1, 13)))
    parser.add_argument("--bioma", default="Amazônia")
    parser.add_argument(
        "--satelite",
        default="AQUA_M-T",
        help="Satélite a filtrar (use 'todos' para manter todos).",
    )
    args = parser.parse_args()

    tabelas = []
    for mes in args.meses:
        try:
            caminho = baixar_mes(args.ano, mes)
        except requests.HTTPError as erro:
            print(f"{args.ano}-{mes:02d}: indisponível ({erro})")
            continue
        tabelas.append(pd.read_csv(caminho))

    if not tabelas:
        raise SystemExit("Nenhum mês baixado.")

    focos = pd.concat(tabelas, ignore_index=True)
    focos = focos[focos["bioma"] == args.bioma]
    if args.satelite != "todos":
        focos = focos[focos["satelite"] == args.satelite]

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    saida = PROCESSED_DIR / (
        f"focos_{slug(args.bioma)}_{slug(args.satelite)}_{args.ano}.parquet"
    )
    focos.to_parquet(saida, index=False)
    print(f"{len(focos)} focos salvos em {saida}")


if __name__ == "__main__":
    main()
