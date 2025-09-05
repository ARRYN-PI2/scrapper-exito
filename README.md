<<<<<<< Updated upstream
# Scraper Éxito Colombia

Scraper genérico para extraer información de productos del sitio web de Éxito Colombia.

## Descripción

Este proyecto implementa un scraper robusto y escalable utilizando arquitectura hexagonal para extraer información de productos del sitio web de Éxito Colombia. Los datos extraídos se almacenan en formato JSON normalizado para su posterior procesamiento por sistemas de IA y análisis de precios.

## Características

- ✅ Arquitectura hexagonal para máxima flexibilidad y mantenibilidad
- ✅ Scraper genérico que funciona con cualquier producto
- ✅ Compatible con múltiples navegadores
- ✅ Ejecución automática programada cada 15 días
- ✅ Ejecución manual bajo demanda
- ✅ Datos normalizados en formato JSON
- ✅ Manejo robusto de errores y reintentos
- ✅ Logging detallado y monitoreo
- ✅ Configuración flexible mediante variables de entorno

## Datos Extraídos

Para cada producto se extrae la siguiente información:

- **precio**: Precio actual del producto
- **marca**: Marca del producto
- **tamaño**: Tamaño/presentación del producto
- **calificacion**: Calificación promedio del producto
- **imagen**: URL de la imagen principal del producto
- **url_producto**: URL del producto en el sitio web
- **fuente**: Identificador de la fuente (exito.com)
- **categoria**: Categoría del producto
- **nombre**: Nombre completo del producto
- **timestamp_extraccion**: Fecha y hora de la extracción
- **extraction_status**: Estado de la extracción (success/failed)
- **contador_extraccion**: Número de extracción
- **atributos_extra**: Información adicional como cambios y devoluciones, seguro gratis, etc.

## Instalación

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd appExito
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. Instalar drivers de navegador:
```bash
playwright install
```

## Uso

### Ejecución Manual
=======
# 🛒 Scraper Exito.com

## 📋 Comandos completos por categoría
>>>>>>> Stashed changes

### 📱 Celulares
```bash
<<<<<<< Updated upstream
python -m src.interfaces.cli.main --category all
=======
python -m exito_scraper.main scrape --categoria celulares --paginas 10 --output data/celulares.json
python -m exito_scraper.main scrape --categoria celulares --paginas 5 --output data/celulares.csv
```

### 📺 Televisores
```bash
python -m exito_scraper.main scrape --categoria televisores --paginas 15 --output data/televisores.json
python -m exito_scraper.main scrape --categoria televisores --paginas 8 --output data/televisores.csv
```

### 🧺 Lavadoras
```bash
python -m exito_scraper.main scrape --categoria lavadoras --paginas 12 --output data/lavadoras.json
python -m exito_scraper.main scrape --categoria lavadoras --paginas 5 --output data/lavadoras.csv
```

### ❄️ Refrigeración
```bash
python -m exito_scraper.main scrape --categoria refrigeracion --paginas 10 --output data/refrigeradores.json
python -m exito_scraper.main scrape --categoria refrigeracion --paginas 7 --output data/refrigeradores.csv
```

### 🔊 Audio
```bash
python -m exito_scraper.main scrape --categoria audio --paginas 8 --output data/audio.json
python -m exito_scraper.main scrape --categoria audio --paginas 6 --output data/audio.csv
```

### 🎮 Videojuegos
```bash
python -m exito_scraper.main scrape --categoria videojuegos --paginas 12 --output data/videojuegos.json
python -m exito_scraper.main scrape --categoria videojuegos --paginas 5 --output data/videojuegos.csv
```

### 🏃 Deportes
```bash
python -m exito_scraper.main scrape --categoria deportes --paginas 20 --output data/deportes.json
python -m exito_scraper.main scrape --categoria deportes --paginas 10 --output data/deportes.csv
```

---

⭐ **Por defecto se genera JSON con calificaciones incluidas**  
📄 Los productos sin calificación muestran "No tiene Calificacion"
>>>>>>> Stashed changes
```

### Ejecución Programada

```bash
python -m src.infrastructure.schedulers.scheduler
```

## Estructura del Proyecto

```
appExito/
├── src/
│   ├── domain/               # Lógica de negocio
│   ├── application/          # Casos de uso
│   ├── infrastructure/       # Implementaciones específicas
│   └── interfaces/           # Puntos de entrada
├── tests/                    # Pruebas unitarias e integración
├── docs/                     # Documentación
├── config/                   # Archivos de configuración
├── data/                     # Datos extraídos
└── logs/                     # Archivos de log
```

## Contribución

1. Fork el proyecto
2. Crear una rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit los cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Tu Nombre - tu.email@ejemplo.com

Link del Proyecto: https://github.com/tu-usuario/appExito
