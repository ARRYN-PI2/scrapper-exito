# appExito/src/infrastructure/config/categories.py
"""
Configuración de categorías específicas de Éxito Colombia
"""

from dataclasses import dataclass
from typing import Dict, Optional, List
from urllib.parse import urlencode


@dataclass
class CategoryConfig:
    """
    Configuración de una categoría específica
    """
    name: str
    path: str
    category_1: str
    category_2: Optional[str] = None
    base_url: str = "https://www.exito.com"
    
    def build_page_url(self, page: int = 1, sort: str = "score_desc") -> str:
        """
        Construye la URL para una página específica de la categoría
        
        Args:
            page: Número de página (empezando en 1)
            sort: Tipo de ordenamiento
            
        Returns:
            URL completa para la página
        """
        # Parámetros base
        params = {
            "category-1": self.category_1,
            "sort": sort,
            "page": page
        }
        
        # Agregar category-2 si existe
        if self.category_2:
            params["category-2"] = self.category_2
            params["facets"] = "category-1,category-2"
        else:
            params["facets"] = "category-1"
        
        # Construir URL completa
        query_string = urlencode(params)
        return f"{self.base_url}{self.path}?{query_string}"
    
    def get_display_name(self) -> str:
        """Obtiene nombre para mostrar de la categoría"""
        return self.name.replace("-", " ").title()


class ExitoCategoriesConfig:
    """
    Configuración centralizada de todas las categorías de Éxito
    """
    
    # Definición de todas las categorías
    CATEGORIES: Dict[str, CategoryConfig] = {
        "televisores": CategoryConfig(
            name="televisores",
            path="/tecnologia/televisores",
            category_1="tecnologia",
            category_2="televisores"
        ),
        
        "celulares": CategoryConfig(
            name="celulares", 
            path="/tecnologia/celulares",
            category_1="tecnologia",
            category_2="celulares"
        ),
        
        "lavadoras": CategoryConfig(
            name="lavadoras-secadoras",
            path="/electrodomesticos/lavado-y-secado",
            category_1="electrodomesticos", 
            category_2="lavado-y-secado"
        ),
        
        "refrigeracion": CategoryConfig(
            name="refrigeracion",
            path="/electrodomesticos/refrigeracion",
            category_1="electrodomesticos",
            category_2="refrigeracion"
        ),
        
        "audio": CategoryConfig(
            name="audio",
            path="/tecnologia/audio", 
            category_1="tecnologia",
            category_2="audio"
        ),
        
        "videojuegos": CategoryConfig(
            name="videojuegos",
            path="/tecnologia/consolas-y-videojuegos",
            category_1="tecnologia",
            category_2="consolas-y-videojuegos"
        ),
        
        "deportes": CategoryConfig(
            name="deportes",
            path="/deportes-y-fitness",
            category_1="deportes-y-fitness",
            category_2=None  # Esta categoría solo tiene category-1
        )
    }
    
    @classmethod
    def get_category(cls, category_key: str) -> Optional[CategoryConfig]:
        """
        Obtiene configuración de una categoría específica
        
        Args:
            category_key: Clave de la categoría
            
        Returns:
            CategoryConfig o None si no existe
        """
        return cls.CATEGORIES.get(category_key)
    
    @classmethod
    def get_all_categories(cls) -> Dict[str, CategoryConfig]:
        """Obtiene todas las categorías configuradas"""
        return cls.CATEGORIES.copy()
    
    @classmethod
    def get_category_names(cls) -> List[str]:
        """Obtiene lista de nombres de categorías"""
        return list(cls.CATEGORIES.keys())
    
    @classmethod
    def get_category_urls(cls, page: int = 1) -> Dict[str, str]:
        """
        Obtiene URLs de todas las categorías para una página específica
        
        Args:
            page: Número de página
            
        Returns:
            Diccionario con {categoria: url}
        """
        urls = {}
        for key, config in cls.CATEGORIES.items():
            urls[key] = config.build_page_url(page)
        return urls


# Función helper para testing
def test_category_urls():
    """
    Función de prueba para verificar que las URLs se generan correctamente
    """
    print("🧪 Probando generación de URLs por categoría...")
    
    config = ExitoCategoriesConfig()
    
    # Probar cada categoría
    for category_key in config.get_category_names():
        category_config = config.get_category(category_key)
        
        if category_config is None:
            print(f"\n❌ {category_key}: Configuración no encontrada")
            continue
        
        print(f"\n📱 {category_config.get_display_name()}:")
        print(f"   Página 1: {category_config.build_page_url(1)}")
        print(f"   Página 2: {category_config.build_page_url(2)}")
        
        # Verificar que las URLs generadas coinciden con las esperadas
        url_page_1 = category_config.build_page_url(1)
        expected_patterns = [
            category_config.category_1 in url_page_1,
            "page=1" in url_page_1,
            "sort=score_desc" in url_page_1
        ]
        
        if all(expected_patterns):
            print(f"   ✅ URL válida")
        else:
            print(f"   ❌ URL inválida")


if __name__ == "__main__":
    test_category_urls()