from __future__ import annotations
import csv
from typing import Iterable
from pathlib import Path
from ..domain.producto import Producto
from ..domain.ports import RepositoryPort

class CsvRepositoryAdapter(RepositoryPort):
    def __init__(self, filename: str):
        # Usar ruta relativa desde el módulo exito_scraper/data
        base_dir = Path(__file__).parent.parent / "data"  # exito_scraper/data/
        base_dir.mkdir(exist_ok=True)  # Crear si no existe
        
        self.path = base_dir / filename
        self._ensure_header()

    def _ensure_header(self):
        if not self.path.exists():
            with self.path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "contador_extraccion_total","contador_extraccion","titulo","marca",
                    "precio_texto","precio_valor","moneda","tamaño","calificacion","numero_opiniones",
                    "detalles_adicionales","fuente","categoria","imagen","link",
                    "pagina","fecha_extraccion","extraction_status"
                ])

    def persist(self, productos: Iterable[Producto]) -> None:
        with self.path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for p in productos:
                d = p.to_dict()
                writer.writerow([
                    d["contador_extraccion_total"], d["contador_extraccion"], d["titulo"], d["marca"],
                    d["precio_texto"], d["precio_valor"], d["moneda"], d["tamaño"], d["calificacion"], d["numero_opiniones"],
                    d["detalles_adicionales"], d["fuente"], d["categoria"], d["imagen"], d["link"],
                    d["pagina"], d["fecha_extraccion"], d["extraction_status"]
                ])
