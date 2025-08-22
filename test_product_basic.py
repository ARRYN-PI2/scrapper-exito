# appExito/test_product_basic.py
"""
Prueba básica para verificar que la entidad Product funciona correctamente
Ejecutar desde la carpeta appExito: python test_product_basic.py
"""

import sys
import os
from decimal import Decimal

# Agregar el directorio src al path para poder importar
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from domain.entities.product import Product, create_test_product


def test_crear_producto_basico():
    """Prueba crear un producto básico"""
    print("🧪 Probando crear producto básico...")
    
    try:
        producto = Product(
            nombre="iPhone 15 Pro Max",
            url_producto="https://www.exito.com/iphone-15-pro-max-123456/p"
        )
        
        print(f"✅ Producto creado: {producto}")
        print(f"   Timestamp: {producto.timestamp_extraccion}")
        print(f"   Status: {producto.extraction_status}")
        
        return True
    except Exception as e:
        print(f"❌ Error creando producto: {e}")
        return False


def test_crear_producto_con_precio():
    """Prueba crear un producto con precio"""
    print("\n🧪 Probando crear producto con precio...")
    
    try:
        producto = Product(
            nombre="Samsung Galaxy S24",
            url_producto="https://www.exito.com/galaxy-s24-789012/p",
            precio=Decimal("2500000"),
            marca="Samsung",
            categoria="tecnologia"
        )
        
        print(f"✅ Producto con precio: {producto}")
        print(f"   Precio: ${producto.precio}")
        print(f"   Marca: {producto.marca}")
        
        return True
    except Exception as e:
        print(f"❌ Error creando producto con precio: {e}")
        return False


def test_validaciones():
    """Prueba las validaciones de la entidad"""
    print("\n🧪 Probando validaciones...")
    
    # Probar nombre vacío
    try:
        Product(nombre="", url_producto="https://test.com")
        print("❌ Debería fallar con nombre vacío")
        return False
    except ValueError as e:
        print(f"✅ Validación correcta para nombre vacío: {e}")
    
    # Probar URL vacía
    try:
        Product(nombre="Test", url_producto="")
        print("❌ Debería fallar con URL vacía")
        return False
    except ValueError as e:
        print(f"✅ Validación correcta para URL vacía: {e}")
    
    # Probar precio negativo
    try:
        Product(
            nombre="Test",
            url_producto="https://test.com",
            precio=Decimal("-100")
        )
        print("❌ Debería fallar con precio negativo")
        return False
    except ValueError as e:
        print(f"✅ Validación correcta para precio negativo: {e}")
    
    return True


def test_metodos_principales():
    """Prueba los métodos principales de la entidad"""
    print("\n🧪 Probando métodos principales...")
    
    try:
        producto = create_test_product(
            nombre="MacBook Air M3",
            url="https://www.exito.com/macbook-air-m3-345678/p",
            precio=4500000
        )
        
        # Probar agregar atributo extra
        producto.add_extra_attribute("garantia", "1 año")
        producto.add_extra_attribute("color", "Gris espacial")
        
        print(f"✅ Atributos extra agregados: {producto.atributos_extra}")
        
        # Probar cambiar status
        producto.mark_as_extracted("success")
        print(f"✅ Status cambiado a: {producto.extraction_status}")
        
        # Probar conversión a diccionario
        producto_dict = producto.to_dict()
        print(f"✅ Conversión a dict: {len(producto_dict)} campos")
        print(f"   Campos: {list(producto_dict.keys())}")
        
        return True
    except Exception as e:
        print(f"❌ Error en métodos principales: {e}")
        return False


def main():
    """Función principal que ejecuta todas las pruebas"""
    print("🚀 Iniciando pruebas de la entidad Product")
    print("=" * 50)
    
    tests = [
        test_crear_producto_basico,
        test_crear_producto_con_precio,
        test_validaciones,
        test_metodos_principales
    ]
    
    resultados = []
    for test in tests:
        resultado = test()
        resultados.append(resultado)
    
    print("\n" + "=" * 50)
    print("📊 Resumen de pruebas:")
    print(f"✅ Exitosas: {sum(resultados)}")
    print(f"❌ Fallidas: {len(resultados) - sum(resultados)}")
    
    if all(resultados):
        print("\n🎉 ¡Todas las pruebas pasaron! La entidad Product está funcionando correctamente.")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")


if __name__ == "__main__":
    main()