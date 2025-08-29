#!/usr/bin/env python3
"""
Script para limpiar y mejorar el formato de los detalles adicionales en archivos JSON existentes
"""
import json
import sys
from pathlib import Path
from exito_scraper.utils.html_formatter import clean_html_details, format_details_as_markdown

def clean_existing_json(input_file: str, output_file: str | None = None):
    """
    Limpia los detalles adicionales de un archivo JSON existente
    
    Args:
        input_file: Archivo JSON/JSONL a limpiar
        output_file: Archivo de salida (opcional)
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"Error: El archivo {input_file} no existe")
        return False
    
    # Generar nombre de archivo de salida si no se proporciona
    if output_file is None:
        if input_path.suffix == '.jsonl':
            output_file = str(input_path.with_name(input_path.stem + '_cleaned.jsonl'))
        else:
            output_file = str(input_path.with_name(input_path.stem + '_cleaned.json'))
    
    try:
        productos = []
        
        # Leer archivo (detectar si es JSONL o JSON)
        if input_path.suffix == '.jsonl':
            # Formato JSONL - una línea por producto
            with open(input_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line:
                        try:
                            producto = json.loads(line)
                            productos.append(clean_product_details(producto))
                        except json.JSONDecodeError as e:
                            print(f"Error en línea {line_num}: {e}")
                            continue
        else:
            # Formato JSON - array de productos
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for producto in data:
                        productos.append(clean_product_details(producto))
                else:
                    productos.append(clean_product_details(data))
        
        # Escribir archivo limpio
        output_path = Path(output_file)
        if output_path.suffix == '.jsonl':
            # Escribir como JSONL
            with open(output_path, 'w', encoding='utf-8') as f:
                for producto in productos:
                    f.write(json.dumps(producto, ensure_ascii=False) + '\n')
        else:
            # Escribir como JSON formateado
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(productos, f, indent=2, ensure_ascii=False)
        
        print(f"Limpiado: {len(productos)} productos")
        print(f"Archivo original: {input_file}")
        print(f"Archivo limpio: {output_file}")
        
        # Mostrar ejemplo de mejora
        if productos:
            example = productos[0]
            if 'detalles_adicionales' in example and example['detalles_adicionales']:
                print(f"\nEjemplo de mejora en detalles:")
                print("Antes (HTML):", example.get('detalles_adicionales_original', 'N/A')[:100] + '...')
                print("Después (limpio):", example['detalles_adicionales'][:100] + '...')
        
        return True
        
    except Exception as e:
        print(f"Error durante la limpieza: {e}")
        return False

def clean_product_details(producto: dict) -> dict:
    """
    Limpia los detalles adicionales de un producto individual
    
    Args:
        producto: Diccionario del producto
        
    Returns:
        Producto con detalles limpiados
    """
    if 'detalles_adicionales' in producto:
        original_details = producto['detalles_adicionales']
        
        if original_details and original_details.strip():
            # Guardar el original para referencia
            producto['detalles_adicionales_original'] = original_details
            
            # Limpiar HTML
            cleaned_details = clean_html_details(original_details)
            producto['detalles_adicionales'] = cleaned_details
            
            # Agregar versión markdown para mayor legibilidad
            markdown_details = format_details_as_markdown(original_details)
            if markdown_details != cleaned_details:
                producto['detalles_adicionales_markdown'] = markdown_details
    
    return producto

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python clean_existing_json.py <archivo_json> [archivo_salida]")
        print("Ejemplo: python clean_existing_json.py data/televisores_formatted.json")
        print("Ejemplo: python clean_existing_json.py data/televisores.jsonl")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    clean_existing_json(input_file, output_file)
