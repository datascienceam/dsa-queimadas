# dsa-queimadas

Coleta e padronização de dados de queimadas na Amazônia, mantida pela
comunidade **Data Science Amazônia**. Reúne scripts reprodutíveis e um
catálogo de fontes públicas, que alimenta o site da comunidade.

## O que há aqui

- `scripts/`: scripts de coleta e tratamento
- `catalog.yml`: catálogo de datasets (fonte, URL, formato, licença, observações)
- `notebooks/`: exemplos de uso em Jupyter
- `data/sample/`: amostras pequenas para teste (os dados completos não ficam no Git)

## Fontes

| Fonte | Conteúdo | Observações |
|---|---|---|
| INPE / Programa Queimadas | Focos de calor mensais (CSV) | Reúne vários satélites; ver Metodologia |
| [outras fontes do catalog.yml] | | |

A lista completa e atualizada está em [`catalog.yml`](catalog.yml).

## Como usar

```bash
git clone https://github.com/[ORGANIZACAO]/dsa-queimadas.git
cd dsa-queimadas
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python scripts/baixar_focos_inpe.py --ano 2025 --meses 8 9
```

Opções do script:

- `--ano`: ano desejado (obrigatório)
- `--meses`: lista de meses (padrão: todos)
- `--bioma`: bioma a filtrar (padrão: `Amazônia`)
- `--satelite`: satélite a filtrar (padrão: `AQUA_M-T`; use `todos` para manter todos)

Os arquivos baixados ficam em `data/raw/` e o resultado tratado, em formato
Parquet, em `data/processed/`. Ambos são ignorados pelo Git.

## Metodologia

Os CSVs mensais do INPE reúnem detecções de vários satélites, e o mesmo
fogo pode ser registrado por mais de um. Por isso, o script filtra por
padrão o satélite de referência (AQUA_M-T), que mantém as séries
comparáveis ao longo dos anos. Para análises que exijam todas as
detecções, use `--satelite todos`. [Conferir e citar aqui a documentação
do Programa Queimadas sobre o satélite de referência.]

Um foco de calor indica anomalia térmica detectada por satélite; não
equivale necessariamente a um incêndio, nem a uma área queimada.

## Licenças

- **Código:** MIT (ver `LICENSE`).
- **Dados:** pertencem às fontes originais e seguem as respectivas
  licenças e termos de uso, registrados no `catalog.yml`. Cite sempre a
  fonte primária.

## Como contribuir

Contribuições são bem-vindas: novas fontes no catálogo, correções nos
scripts e exemplos em notebooks. Abra uma *issue* para discutir ou envie
um *pull request*. Novas fontes devem trazer URL, formato, licença e uma
nota de metodologia.

## Sobre a comunidade

A Data Science Amazônia é uma comunidade aberta, sem fins lucrativos, que
explora o potencial científico, acadêmico e tecnológico da Amazônia por
meio de ciência de dados e inteligência artificial.
Instagram: [@datascienceamazonia](https://instagram.com/datascienceamazonia)
