from __future__ import annotations
import json
from typing import Iterable
from ..domain.ports import RepositoryPort
from ..domain.producto import Producto
from pathlib import Path

class JsonRepositoryAdapter(RepositoryPort):
    def __init__(self, filename: str, generate_formatted: bool = True):
        # Usar ruta relativa desde el módulo exito_scraper/data
        base_dir = Path(__file__).parent.parent / "data"  # exito_scraper/data/
        base_dir.mkdir(exist_ok=True)  # Crear si no existe
        
        self.path = base_dir / filename
        self.generate_formatted = generate_formatted
        self.productos_buffer = []

    def persist(self, productos: Iterable[Producto]) -> None:
        # Guardar en formato JSONL (una línea por producto)
        with self.path.open("a", encoding="utf-8") as f:
            for p in productos:
                producto_dict = p.to_dict()
                self.productos_buffer.append(producto_dict)
                f.write(json.dumps(producto_dict, ensure_ascii=False) + "\n")
        
        # Generar también archivo JSON formateado si está habilitado
        if self.generate_formatted:
            self._generate_formatted_json()
    
    def _generate_formatted_json(self) -> None:
        """Genera un archivo JSON formateado con todos los productos"""
        if not self.productos_buffer:
            return
            
        # Leer todos los productos del archivo JSONL existente
        all_productos = []
        if self.path.exists():
            with self.path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            all_productos.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        
        # Crear archivo JSON formateado
        formatted_path = self.path.with_name(self.path.stem + '_formatted.json')
        with formatted_path.open("w", encoding="utf-8") as f:
            json.dump(all_productos, f, indent=2, ensure_ascii=False)
