# Docker Guide - Exito Scraper

Esta guía explica cómo usar el scraper de Éxito con Docker.

## Inicio Rápido

### 1. Construir la imagen

```bash
# Opción 1: Script automatizado (recomendado)
./docker-build.sh

# Opción 2: Construcción manual
docker build -t exito-scraper .
```

### 2. Ejecutar el scraper

```bash
# Scraping básico
docker run --rm -v $(pwd)/data:/app/data exito-scraper:latest \
  python -m exito_scraper.main scrape --categoria televisores --paginas 2 --output data/productos.jsonl

# Con docker-compose
docker-compose up exito-scraper
```

## Comandos Disponibles

### Scraping de productos

```bash
# Televisores (2 páginas)
docker run --rm -v $(pwd)/data:/app/data exito-scraper:latest \
  python -m exito_scraper.main scrape --categoria televisores --paginas 2 --output data/tv.jsonl

# Celulares (1 página)
docker run --rm -v $(pwd)/data:/app/data exito-scraper:latest \
  python -m exito_scraper.main scrape --categoria celulares --paginas 1 --output data/celulares.jsonl

# Refrigeración (3 páginas)
docker run --rm -v $(pwd)/data:/app/data exito-scraper:latest \
  python -m exito_scraper.main scrape --categoria refrigeracion --paginas 3 --output data/neveras.jsonl
```

### Utilidades de formateo

```bash
# Formatear archivo JSONL a JSON legible
docker run --rm -v $(pwd)/data:/app/data exito-scraper:latest \
  python format_json.py /app/data/productos.jsonl

# Limpiar HTML de archivos existentes
docker run --rm -v $(pwd)/data:/app/data exito-scraper:latest \
  python clean_existing_json.py /app/data/productos_formatted.json
```

### Modo interactivo

```bash
# Shell interactivo
docker run --rm -it -v $(pwd)/data:/app/data exito-scraper:latest /bin/bash

# Python interactivo
docker run --rm -it -v $(pwd)/data:/app/data exito-scraper:latest python
```

## Docker Compose

### Servicios disponibles

```bash
# Ejecutar scraper principal
docker-compose up exito-scraper

# Modo desarrollo con shell interactivo
docker-compose run --rm exito-scraper-dev

# Ejecutar tests
docker-compose run --rm test-runner
```

### Configuración personalizada

Edita `docker-compose.yml` para:
- Cambiar volúmenes montados
- Modificar variables de entorno
- Ajustar comandos por defecto

## Gestión de Datos

### Volúmenes

```bash
# Mount data directory (recomendado)
-v $(pwd)/data:/app/data

# Mount todo el proyecto (desarrollo)
-v $(pwd):/app/workspace:ro

# Mount archivos de configuración
-v $(pwd)/.env:/app/.env:ro
```

### Persistencia

Los datos se guardan en `/app/data` dentro del contenedor:
- `productos.jsonl` - Formato compacto
- `productos_formatted.json` - Formato legible
- Logs y archivos temporales

## Variables de Entorno

```bash
# Usar archivo .env
docker run --rm --env-file .env -v $(pwd)/data:/app/data exito-scraper:latest

# Variables individuales
docker run --rm \
  -e PYTHONUNBUFFERED=1 \
  -e DEFAULT_TIMEOUT=60 \
  -v $(pwd)/data:/app/data \
  exito-scraper:latest
```

### Variables principales

- `PYTHONUNBUFFERED=1` - Output inmediato
- `DEFAULT_TIMEOUT` - Timeout de requests
- `DEFAULT_DELAY` - Delay entre requests
- `DEFAULT_OUTPUT_DIR` - Directorio de salida

## Desarrollo

### Build de desarrollo

```bash
# Build con target específico
docker build --target builder -t exito-scraper:builder .

# Build sin cache
docker build --no-cache -t exito-scraper:latest .

# Build con argumentos
docker build --build-arg PYTHON_VERSION=3.12 -t exito-scraper:py312 .
```

### Debugging

```bash
# Logs detallados
docker run --rm -e PYTHONUNBUFFERED=1 \
  -v $(pwd)/data:/app/data \
  exito-scraper:latest \
  python -m exito_scraper.main scrape --categoria televisores --paginas 1 --output data/debug.jsonl

# Inspeccionar imagen
docker run --rm -it exito-scraper:latest /bin/bash
docker inspect exito-scraper:latest
```

## Testing

### Tests automáticos

```bash
# Script de tests completo
./docker-build.sh

# Tests individuales
docker run --rm exito-scraper:latest python -c "import exito_scraper; print('OK')"
docker run --rm exito-scraper:latest python -m exito_scraper.main --help
```

### Validación

```bash
# Verificar estructura
docker run --rm exito-scraper:latest find /app -name "*.py" | head -10

# Verificar dependencias
docker run --rm exito-scraper:latest pip list

# Verificar configuración
docker run --rm exito-scraper:latest python -c "from exito_scraper.config import EXPECTED_URLS; print(list(EXPECTED_URLS.keys()))"
```

## Troubleshooting

### Problemas comunes

1. **Error "No such file or directory"**
   ```bash
   # Verificar que los archivos existen
   ls -la format_json.py clean_existing_json.py
   
   # Reconstruir imagen
   docker build --no-cache -t exito-scraper .
   ```

2. **Error de permisos en /app/data**
   ```bash
   # Cambiar propietario del directorio data
   sudo chown -R $USER:$USER data/
   
   # Usar usuario específico
   docker run --rm --user $(id -u):$(id -g) -v $(pwd)/data:/app/data exito-scraper:latest
   ```

3. **Timeout en requests**
   ```bash
   # Aumentar timeout
   docker run --rm -e DEFAULT_TIMEOUT=120 -v $(pwd)/data:/app/data exito-scraper:latest
   ```

### Logs y debug

```bash
# Logs detallados
docker run --rm \
  -e PYTHONUNBUFFERED=1 \
  -e PYTHONDEBUG=1 \
  -v $(pwd)/data:/app/data \
  exito-scraper:latest

# Ejecutar con verbose
docker run --rm -v $(pwd)/data:/app/data exito-scraper:latest \
  python -v -m exito_scraper.main scrape --categoria televisores --paginas 1 --output data/test.jsonl
```

## Monitoreo

### Health checks

```bash
# Verificar salud del contenedor
docker run --rm --name scraper-health exito-scraper:latest &
docker exec scraper-health python -c "import exito_scraper; print('Healthy')"
```

### Métricas

```bash
# Uso de recursos
docker stats

# Tamaño de imagen
docker images exito-scraper

# Información detallada
docker system df
```

## CI/CD con Docker

El pipeline automático incluye:

1. **Build**: Construcción de imagen
2. **Test**: Pruebas en contenedor
3. **Security**: Escaneo de vulnerabilidades
4. **Push**: Publicación en registry (opcional)

Ver `.github/workflows/ci-cd.yml` para detalles.

## Referencias

- [Dockerfile](./Dockerfile) - Configuración de imagen
- [docker-compose.yml](./docker-compose.yml) - Orquestación
- [docker-build.sh](./docker-build.sh) - Script de construcción
- [.dockerignore](./.dockerignore) - Archivos excluidos
