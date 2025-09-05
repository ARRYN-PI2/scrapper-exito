# 🛒 Scraper Exito.com

## 📋 Comandos completos por categoría

### 📱 Celulares
```bash
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
```

### Instalación Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar scraper
python -m exito_scraper.main scrape --categoria televisores --paginas 2

# Instalar dependencias
pip install -r requirements.txt

```

## Ejemplo de Datos Extraídos

El scraper extrae **17 campos completos** por producto:

```json
{
  "titulo": "Televisor LG 55\" 4K UHD Smart TV",
  "precio": "$1.299.900",
  "precio_original": "$1.599.900",
  "descuento": "19%",
  "descripcion": "Televisor LG con tecnología 4K UHD y Smart TV webOS",
  "sku": "LG55UP7500PSB",
  "marca": "LG",
  "modelo": "55UP7500PSB",
  "disponibilidad": "En stock",
  "calificacion": "4.5",
  "numero_resenas": "342",
  "imagen_principal": "https://www.exito.com/medias/...",
  "imagenes_adicionales": ["https://...", "https://..."],
  "categoria": "Televisores",
  "subcategoria": "Smart TV",
  "detalles_adicionales": "Pantalla: 55 pulgadas. Resolución: 4K UHD (3840x2160)...",
  "link": "https://www.exito.com/televisor-lg-55-4k-uhd-smart-tv"
}
```

### Estadísticas de Completitud

- **98-100%** de campos básicos (título, precio, link)
- **95-98%** de campos descriptivos (marca, modelo, disponibilidad)  
- **90-95%** de campos adicionales (imágenes, reviews)
- **HTML limpiado** automáticamente en descripciones

## Casos de Uso

### Ejecución Programada

```bash
# Cron job diario a las 6 AM
0 6 * * * cd /path/to/scraper && docker-compose run --rm exito-scraper scrape --categoria televisores --paginas 5
```

### Para Empresas

```bash
# Monitoreo de precios de competencia
python -m exito_scraper.main scrape --categoria "computadores portatiles" --paginas 10

# Análisis de inventario
python -m exito_scraper.main scrape --categoria celulares --paginas 5
```

## Configuración

### Variables de Entorno

```bash
# .env
SCRAPER_DELAY=2          # Delay entre requests
SCRAPER_RETRIES=3        # Número de reintentos  
LOG_LEVEL=INFO           # Nivel de logging
OUTPUT_FORMAT=both       # jsonl, json, both
```

## Estructura del Proyecto

```
scrapper-exito/
├── exito_scraper/          # Código principal
│   ├── adapters/           # Adaptadores (scraper, repos)
│   ├── application/        # Casos de uso
│   ├── domain/            # Lógica de dominio
│   ├── utils/             # Utilidades (HTML cleaning)
│   ├── config.py          # Configuración
│   └── main.py            # CLI principal
├── .github/workflows/      # Pipeline CI/CD
├── data/                  # Archivos extraídos
├── Dockerfile             # Imagen Docker
├── docker-compose.yml     # Orquestación
├── requirements.txt       # Dependencias
├── USAGE.md              # Guía completa de uso
└── DOCKER.md             # Documentación Docker

## Limpieza de Datos

El scraper incluye limpieza automática de HTML:

### Antes (HTML crudo)
```html
<p><span>*No se ofrece servicio de instalación.</span></p>
<p><span>El diseño de brazo extensible hace...</span></p>
```

### Después (texto limpio)
```
*No se ofrece servicio de instalación.

El diseño de brazo extensible hace que el modelo sea mucho más fuerte...
```

### Utilidades Adicionales

```bash
# Limpiar archivos existentes
python clean_existing_json.py data/productos.jsonl

# Convertir JSONL a JSON formateado
python format_json.py data/productos.jsonl
```

## Formatos de Salida

### JSONL (Compacto)
```json
{"titulo": "TV Samsung 55\"", "precio_valor": 1200000, "marca": "SAMSUNG"}
{"titulo": "TV LG 43\"", "precio_valor": 800000, "marca": "LG"}
```

### JSON Formateado (Legible)
```json
[
  {
    "titulo": "TV Samsung 55\"",
    "precio_valor": 1200000,
    "marca": "SAMSUNG",
    "detalles_adicionales": "Smart TV con tecnología 4K..."
  }
]
```

## Configuración

### Variables de Entorno (.env)

```bash
# Versiones Python para CI/CD
PYTHON_VERSION_MAIN=3.11
PYTHON_VERSIONS=["3.9", "3.10", "3.11", "3.12"]

# Configuración Docker
DOCKER_IMAGE_NAME=exito-scraper
DOCKER_TAG=latest

# Configuración del scraper
DEFAULT_TIMEOUT=30
DEFAULT_DELAY=2
```

### Personalización

Edita `exito_scraper/config.py` para:
- Agregar nuevas categorías
- Modificar headers HTTP
- Ajustar timeouts y delays

## Docker

### Construcción

```bash
# Construcción simple
docker build -t exito-scraper .

# Construcción con tests
./docker-build.sh

# Con versión específica
./docker-build.sh v1.0.0
```

### Ejecución

```bash
# Scraping básico
docker run --rm -v $(pwd)/data:/app/data exito-scraper \
  python -m exito_scraper.main scrape --categoria televisores --paginas 1 --output data/tv.jsonl

# Shell interactivo
docker run --rm -it -v $(pwd)/data:/app/data exito-scraper /bin/bash

# Con variables de entorno
docker run --rm --env-file .env -v $(pwd)/data:/app/data exito-scraper \
  python -m exito_scraper.main scrape --categoria celulares --paginas 1 --output data/phones.jsonl
```

## CI/CD Pipeline

El pipeline automático incluye:

1. **Setup**: Lee versiones Python desde `.env`
2. **Lint & Format**: Black, isort, flake8, mypy
3. **Test**: Pruebas en múltiples versiones Python
4. **Security**: Escaneo con safety y bandit
5. **Docker Build**: Construcción y prueba de imagen
6. **Integration Tests**: Pruebas de integración
7. **Release**: Creación automática de releases

### Activación

```bash
# Push a main/develop activa el pipeline
git push origin main

# Manual trigger
gh workflow run ci-cd.yml
```

## Arquitectura

### Patrones Utilizados

- **Ports & Adapters**: Separación clara de responsabilidades
- **Repository Pattern**: Abstracción de persistencia  
- **Command Pattern**: CLI estructurado
- **Strategy Pattern**: Múltiples formatos de salida

### Componentes Principales

1. **Domain**: Entidades (`Producto`) y puertos
2. **Application**: Casos de uso (`ScrapeUseCase`)
3. **Adapters**: Implementaciones concretas

---

## Enlaces Rápidos

| Documento | Descripción | Audiencia |
|-----------|-------------|-----------|
| **[USAGE.md](./USAGE.md)** | Guía completa de uso y deployment | Todos los roles |
| **[DOCKER.md](./DOCKER.md)** | Documentación de Docker | Desarrolladores |
| **[CI/CD Pipeline](./.github/workflows/ci-cd.yml)** | Configuración de automatización | DevOps |
| **[requirements.txt](./requirements.txt)** | Dependencias del proyecto | Desarrolladores |

## Uso Rápido por Rol

### Ejecutor/Operador
```bash
# Ejecutar scraper diariamente
docker-compose run --rm exito-scraper scrape --categoria televisores --paginas 5
```

### Desarrollador  
```bash
# Setup local
pip install -r requirements.txt
python -m exito_scraper.main scrape --categoria televisores --debug
```

### Arquitecto AWS
```bash
# Deploy a ECS Fargate
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

---

**¡Listo para usar!** - Ver [USAGE.md](./USAGE.md) para instrucciones detalladas
4. **Utils**: Utilidades transversales

## Testing

```bash
# Tests locales (cuando estén disponibles)
pytest tests/ -v --cov=exito_scraper

# Tests en Docker
docker-compose run --rm test-runner

# Tests del pipeline
./docker-build.sh
```

## Datos Extraídos

Cada producto incluye:

- **Información básica**: título, marca, categoría
- **Precios**: texto y valor numérico, moneda
- **Metadatos**: imagen, link, fecha de extracción
- **Detalles**: descripción limpia (sin HTML)
- **Técnicos**: contadores, estado de extracción

### Estadísticas de Calidad

- **Campos básicos**: 100% cobertura
- **Precios**: 98% cobertura
- **Detalles**: 64% cobertura
- **Tamaños**: 86% cobertura (solo TVs)


