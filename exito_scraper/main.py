from __future__ import annotations
import argparse
from pathlib import Path

from .config import EXPECTED_URLS
from .adapters.exito_scraper_adapter import ExitoScraperAdapter
from .adapters.json_repo import JsonRepositoryAdapter
from .adapters.csv_repo import CsvRepositoryAdapter
from .application.scrape_usecase import ScrapeCategoryUseCase

def _make_repo(output: str):
    # Usar solo el nombre del archivo, la ruta se maneja internamente
    filename = Path(output).name
    
    if filename.endswith('.csv'):
        return CsvRepositoryAdapter(filename)
    elif filename.endswith('.jsonl'):
        return JsonRepositoryAdapter(filename, generate_formatted=True)
    else:
        # Default to JSONL format 
        if not filename.endswith(('.json', '.jsonl')):
            filename = filename + '.jsonl'
        return JsonRepositoryAdapter(filename, generate_formatted=True)

def main():
    parser = argparse.ArgumentParser(description="Scraper Exito.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scrape", help="Extraer productos por categoría")
    s.add_argument("--categoria", required=True, choices=sorted(EXPECTED_URLS.keys()), help="Categoría a scrapear")
    s.add_argument("--paginas", type=int, default=1, help="Numero de páginas a extraer (>=1)")
    s.add_argument("--output", required=True, help="Nombre del archivo de salida (.json, .jsonl o .csv) - se guarda en exito_scraper/data/")

    args = parser.parse_args()

    if args.cmd == "scrape":
        scraper = ExitoScraperAdapter()
        repo = _make_repo(args.output)
        usecase = ScrapeCategoryUseCase(scraper, repo)
        usecase.run(args.categoria, pages=max(1, int(args.paginas)))

if __name__ == "__main__":
    main()
