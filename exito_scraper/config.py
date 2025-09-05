EXPECTED_URLS = {
    "televisores": "https://www.exito.com/tecnologia/televisores?category-1=tecnologia&category-2=televisores&facets=category-1%2Ccategory-2&sort=score_desc&page=1",
    "celulares": "https://www.exito.com/tecnologia/celulares?category-1=tecnologia&category-2=celulares&facets=category-1%2Ccategory-2&sort=score_desc&page=1",
    "lavadoras": "https://www.exito.com/electrodomesticos/lavado-y-secado?category-1=electrodomesticos&category-2=lavado-y-secado&facets=category-1%2Ccategory-2&sort=score_desc&page=1",
    "refrigeracion": "https://www.exito.com/electrodomesticos/refrigeracion?category-1=electrodomesticos&category-2=refrigeracion&facets=category-1%2Ccategory-2&sort=score_desc&page=1",
    "audio": "https://www.exito.com/tecnologia/audio?category-1=tecnologia&category-2=audio&facets=category-1%2Ccategory-2&sort=score_desc&page=1",
    "videojuegos": "https://www.exito.com/tecnologia/consolas-y-videojuegos?category-1=tecnologia&category-2=consolas-y-videojuegos&facets=category-1%2Ccategory-2&sort=score_desc&page=1",
    "deportes": "https://www.exito.com/deportes-y-fitness?category-1=deportes-y-fitness&facets=category-1&sort=score_desc&page=1",
}

# Mapping categories to their API paths for VTEX catalog system
CATEGORY_API_PATHS = {
    "televisores": "tecnologia/televisores",
    "celulares": "tecnologia/celulares", 
    "lavadoras": "electrodomesticos/lavado-y-secado",
    "refrigeracion": "electrodomesticos/refrigeracion",
    "audio": "tecnologia/audio",
    "videojuegos": "tecnologia/consolas-y-videojuegos",
    "deportes": "deportes-y-fitness",
}

BASE_HOST = "https://www.exito.com"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "es-CO,es;q=0.9",
}
TIMEOUT = 25
REQUEST_DELAY_SECONDS = (1.0, 2.0)  # min, max
