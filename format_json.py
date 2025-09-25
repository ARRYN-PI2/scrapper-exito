#!/usr/bin/env python3
"""
Script para convertir archivos JSONL a JSON formateado
"""
import json
import sys
from pathlib import Path

def jsonl_to_formatted_json(jsonl_file: str, output_file: str | None = None):
    """
    Convierte un archivo JSONL a JSON formateado
    
    Args:
        jsonl_file: Ruta al archivo JSONL
        output_file: Ruta del archivo de salida (opcional)
    """
    jsonl_path = Path(jsonl_file)
    
    if not jsonl_path.exists():
        print(f"Error: El archivo {jsonl_file} no existe")
        return False
    
    # Generar nombre de archivo de salida si no se proporciona
    if output_file is None:
        output_file = str(jsonl_path.with_name(jsonl_path.stem + '_formatted.json'))
    
    try:
        # Leer el archivo JSONL
        productos = []
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    try:
                        productos.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        print(f"Error en línea {line_num}: {e}")
                        continue
        
        # Escribir archivo JSON formateado
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(productos, f, indent=2, ensure_ascii=False)
        
        print(f"Convertido: {len(productos)} productos")
        print(f"Archivo original: {jsonl_file}")
        print(f"Archivo formateado: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"Error durante la conversión: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python format_json.py <archivo_jsonl> [archivo_salida]")
        print("Ejemplo: python format_json.py data/televisores.jsonl")
        sys.exit(1)
    
    jsonl_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    jsonl_to_formatted_json(jsonl_file, output_file)
