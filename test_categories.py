# appExito/test_categories.py
"""
Prueba de configuración de categorías
Ejecutar desde appExito: python test_categories.py
"""

import sys
import os

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from infrastructure.config.categories import ExitoCategoriesConfig, CategoryConfig


def test_url_generation():
    """Prueba que las URLs se generen igual que las proporcionadas por el usuario"""
    print("🧪 Verificando generación de URLs...")
    
    # URLs esperadas (las que proporcionaste)
    expected_urls = {
        "televisores": "https://www.exito.com/tecnologia/televisores?category-1=tecnologia&category-2=televisores&facets=category-1%2Ccategory-2&sort=score_desc&page=1",
        "celulares": "https://www.exito.com/tecnologia/celulares?category-1=tecnologia&category-2=celulares&facets=category-1%2Ccategory-2&sort=score_desc&page=1",
        "lavadoras": "https://www.exito.com/electrodomesticos/lavado-y-secado?category-1=electrodomesticos&category-2=lavado-y-secado&facets=category-1%2Ccategory-2&sort=score_desc&page=1",
        "refrigeracion": "https://www.exito.com/electrodomesticos/refrigeracion?category-1=electrodomesticos&category-2=refrigeracion&facets=category-1%2Ccategory-2&sort=score_desc&page=1",
        "audio": "https://www.exito.com/tecnologia/audio?category-1=tecnologia&category-2=audio&facets=category-1%2Ccategory-2&sort=score_desc&page=1",
        "videojuegos": "https://www.exito.com/tecnologia/consolas-y-videojuegos?category-1=tecnologia&category-2=consolas-y-videojuegos&facets=category-1%2Ccategory-2&sort=score_desc&page=1",
        "deportes": "https://www.exito.com/deportes-y-fitness?category-1=deportes-y-fitness&facets=category-1&sort=score_desc&page=1"
    }
    
    config = ExitoCategoriesConfig()
    results = []
    
    for category_key, expected_url in expected_urls.items():
        print(f"\n📱 Probando {category_key}...")
        
        category_config = config.get_category(category_key)
        if not category_config:
            print(f"❌ Categoría {category_key} no encontrada")
            results.append(False)
            continue
        
        generated_url = category_config.build_page_url(1)
        
        print(f"   Esperada:  {expected_url}")
        print(f"   Generada:  {generated_url}")
        
        # Comparar componentes principales (el orden de parámetros puede variar)
        if _urls_equivalent(expected_url, generated_url):
            print(f"   ✅ URLs equivalentes")
            results.append(True)
        else:
            print(f"   ❌ URLs diferentes")
            results.append(False)
    
    return results


def _urls_equivalent(url1: str, url2: str) -> bool:
    """Compara si dos URLs son equivalentes (mismo contenido, diferente orden de parámetros)"""
    from urllib.parse import urlparse, parse_qs
    
    parsed1 = urlparse(url1)
    parsed2 = urlparse(url2)
    
    # Comparar esquema, host y path
    if parsed1.scheme != parsed2.scheme:
        return False
    if parsed1.netloc != parsed2.netloc:
        return False
    if parsed1.path != parsed2.path:
        return False
    
    # Comparar parámetros (sin importar orden)
    params1 = parse_qs(parsed1.query)
    params2 = parse_qs(parsed2.query)
    
    return params1 == params2


def test_pagination():
    """Prueba la paginación en diferentes páginas"""
    print("\n🔄 Probando paginación...")
    
    config = ExitoCategoriesConfig()
    televisores = config.get_category("televisores")
    
    if televisores:
        print(f"📺 URLs de Televisores:")
        for page in [1, 2, 5, 10]:
            url = televisores.build_page_url(page)
            print(f"   Página {page}: {url}")
            
            # Verificar que el número de página está correcto
            if f"page={page}" in url:
                print(f"   ✅ Página {page} correcta")
            else:
                print(f"   ❌ Página {page} incorrecta")


def test_all_categories_exist():
    """Verifica que todas las categorías esperadas existen"""
    print("\n📋 Verificando todas las categorías...")
    
    config = ExitoCategoriesConfig()
    expected_categories = [
        "televisores", "celulares", "lavadoras", "refrigeracion", 
        "audio", "videojuegos", "deportes"
    ]
    
    missing_categories = []
    for category in expected_categories:
        if config.get_category(category) is None:
            missing_categories.append(category)
        else:
            print(f"✅ {category} - OK")
    
    if missing_categories:
        print(f"❌ Categorías faltantes: {missing_categories}")
        return False
    else:
        print("✅ Todas las categorías están configuradas")
        return True


def main():
    """Ejecuta todas las pruebas"""
    print("🚀 Iniciando pruebas de configuración de categorías")
    print("=" * 60)
    
    # Ejecutar pruebas
    url_results = test_url_generation()
    test_pagination()
    all_categories_ok = test_all_categories_exist()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 Resumen:")
    print(f"✅ URLs correctas: {sum(url_results)}/{len(url_results)}")
    print(f"✅ Todas las categorías: {'Sí' if all_categories_ok else 'No'}")
    
    if all(url_results) and all_categories_ok:
        print("\n🎉 ¡Configuración de categorías funcionando perfectamente!")
        print("✨ Listo para el siguiente paso: crear el scraper básico")
    else:
        print("\n⚠️  Hay algunos problemas que necesitan corrección")


if __name__ == "__main__":
    main()