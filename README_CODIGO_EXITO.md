# 📋 Análisis del Código - Exito E-commerce Scraper

Este documento explica en detalle qué hace el código dentro de este repositorio y cómo funciona internamente.

## 🎯 Propósito del Sistema

El **Exito E-commerce Scraper** es un sistema profesional diseñado para extraer información estructurada de productos del sitio web de Éxito (exito.com), una de las principales cadenas de retail en Colombia.

### Objetivos Principales:
- ✅ Extraer datos de productos de manera automatizada
- ✅ Limpiar y estructurar la información obtenida
- ✅ Generar datasets en múltiples formatos (JSON, JSONL, CSV)
- ✅ Facilitar análisis de mercado y comparación de precios

---

## ¿Qué hace este código?

### Funcionalidades Principales

1. **Extracción de Productos**: Obtiene información detallada de productos de diferentes categorías disponibles en Exito.com

2. **Múltiples Estrategias de Scraping**:
   - **Estado JSON Embebido** (Recomendado): Extrae objetos JavaScript con datos estructurados del HTML (SSR/SPA state)
   - **HTML Scraping** (Fallback): Parsing tradicional del DOM usando BeautifulSoup
   - **API VTEX** (Indirecto): Aprovecha la infraestructura VTEX que usa Éxito para su e-commerce

3. **Formatos de Salida Flexibles**:
    *Guardados en scrapper-exito/data*
   - **JSONL**: Un producto por línea en formato JSON (eficiente para big data)
   - **CSV**: Archivo estructurado compatible con Excel y herramientas de análisis
   
   El formato JSONL es procesado por la clase `exito_scraper/adapters/json_repo.py` que toma los datos y genera automáticamente un archivo JSON formateado más legible (`*_formatted.json`) que se exporta a `/data/` para facilitar la lectura humana.

4. **Categorías Soportadas**: 7 categorías de productos incluyendo televisores, celulares, electrodomésticos, audio, videojuegos y deportes.

5. **Limpieza Automática de Datos**:
   - **HTML Sanitization**: Convierte descripciones HTML a texto plano legible
   - **Extracción de Precios**: Separa texto de precio y valor numérico
   - **Normalización**: Estructura consistente de datos independientemente de la fuente

### Flujo de Ejecución Paso a Paso

```
1. 🚀 INICIO
   ├─ Usuario ejecuta comando con categoría y número de páginas
   └─ Sistema valida parámetros de entrada

2. 🔧 CONFIGURACIÓN
   ├─ Carga URL base de la categoría desde config.py
   ├─ Inicializa adaptadores (Scraper + Repositorio)
   └─ Configura headers HTTP y rate limiting

3. 🔄 ITERACIÓN POR PÁGINAS
   Para cada página (1 a N):
   
   3.1 📡 SOLICITUD HTTP
       ├─ Construye URL con parámetro de página
       ├─ Aplica delay aleatorio (1-2 segundos)
       ├─ Realiza request con headers realistas
       └─ Valida respuesta HTTP exitosa
   
   3.2 🔍 ESTRATEGIA DE PARSING
       ├─ Intenta extraer JSON embebido del HTML
       │   ├─ Busca patrones: __STATE__, __APOLLO_STATE__, __NEXT_DATA__
       │   └─ Si encuentra: procesa datos estructurados ✅
       │
       └─ Si falla: usa parsing HTML tradicional
           ├─ Parsea DOM con BeautifulSoup
           ├─ Extrae productos de grillas/tarjetas
           └─ Obtiene datos individuales por producto
   
   3.3 🧹 LIMPIEZA DE DATOS
       Para cada producto encontrado:
       ├─ Limpia HTML de descripciones
       ├─ Extrae precio numérico del texto
       ├─ Normaliza campos opcionales
       ├─ Asigna metadatos (fecha, página, contador)
       └─ Valida estructura del objeto Producto
   
   3.4 💾 PERSISTENCIA
       ├─ Agrupa productos de la página
       ├─ Escribe a archivo JSONL (una línea por producto)
       └─ Actualiza contadores globales

4. 📊 POSTPROCESAMIENTO
   ├─ Genera archivo JSON formateado para lectura humana
   ├─ Aplica indentación y estructura legible
   └─ Guarda como *_formatted.json en /data/

5. ✅ FINALIZACIÓN
   ├─ Reporta estadísticas de extracción
   ├─ Cierra conexiones HTTP
   └─ Retorna código de estado del proceso
```

### Orden de Eventos Interno

```
ExitoScraperAdapter → ScrapeCategoryUseCase → Repositories
     ↓                        ↓                    ↓
1. scrape()              2. run()            3. persist()
   ├─ _with_page()          ├─ for pages         ├─ write JSONL
   ├─ _get()                └─ scraper.scrape()  └─ format JSON
   ├─ _extract_state_json()
   ├─ _parse_html_grid()
   └─ return productos[]
```

---

## 🏗️ Arquitectura del Sistema

### Patrón Arquitectónico: **Hexagonal (Puertos y Adaptadores)**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Adaptadores  │    │    Aplicación   │    │     Dominio     │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ Exito       │ │◄───┤ │ Scrape      │ │◄───┤ │ Producto    │ │
│ │ Scraper     │ │    │ │ UseCase     │ │    │ │ (Entity)    │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │                 │    │ ┌─────────────┐ │
│ │ JSON/CSV    │ │◄───┤                 │    │ │ Ports       │ │
│ │ Repository  │ │    │                 │    │ │ (Interfaces)│ │
│ └─────────────┘ │    │                 │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 📁 Estructura del Código

### **1. Dominio (`exito_scraper/domain/`)**

#### `producto.py` - Entidad Principal
```python
@dataclass
class Producto:
    contador_extraccion_total: int
    contador_extraccion: int
    titulo: str
    marca: str
    precio_texto: str
    precio_valor: Optional[int]
    moneda: Optional[str]
    tamaño: str
    calificacion: str
    detalles_adicionales: str
    fuente: str
    categoria: str
    imagen: str
    link: str
    pagina: int
    fecha_extraccion: str
    extraction_status: str = "OK"
```

**Responsabilidades:**
- Definir la estructura de datos de un producto
- Validar que todos los campos requeridos estén presentes
- Proporcionar métodos de serialización (`to_dict()`)
- Generar timestamps automáticos (`now_iso()`)

#### `ports.py` - Contratos de Interfaces
```python
class ScraperPort(Protocol):
    def scrape(self, categoria: str, page: int) -> Iterable[Producto]: ...

class RepositoryPort(Protocol):
    def persist(self, productos: Iterable[Producto]) -> None: ...
```

**Responsabilidades:**
- Definir contratos que deben cumplir los adaptadores
- Garantizar independencia del dominio respecto a implementaciones externas

### **2. Aplicación (`exito_scraper/application/`)**

#### `scrape_usecase.py` - Caso de Uso Principal
```python
class ScrapeCategoryUseCase:
    def run(self, categoria: str, pages: int = 1) -> None:
        for p in range(1, pages + 1):
            productos = list(self.scraper.scrape(categoria, p))
            if not productos:
                continue
            self.repo.persist(productos)
```

**Responsabilidades:**
- Coordinar el proceso de extracción
- Iterar sobre múltiples páginas
- Manejar casos donde no hay productos
- Persistir los resultados obtenidos

### **3. Adaptadores (`exito_scraper/adapters/`)**

#### `exito_scraper_adapter.py` - Scraper Principal
**Funciones clave:**

1. **Manejo de URLs:**
```python
def _with_page(self, url: str, page: int) -> str:
    # Modifica parámetros de página en la URL
```

2. **Control de Rate Limiting:**
```python
def _sleep(self):
    lo, hi = REQUEST_DELAY_SECONDS
    time.sleep(random.uniform(lo, hi))  # 1-2 segundos entre requests
```

3. **Extracción de Estado JSON:**
```python
def _extract_state_json(self, html: str) -> Optional[dict]:
    # Busca objetos JSON embebidos en el HTML (SSR/SPA state)
```

4. **Parsing HTML Tradicional:**
```python
def _parse_html_grid(self, html: str, categoria: str, page: int) -> List[Producto]:
    # Fallback usando BeautifulSoup para extraer productos del DOM
```

#### `json_repo.py` y `csv_repo.py` - Repositorios de Datos
**Responsabilidades:**
- Persistir productos en formatos específicos
- JSONL: Una línea por producto (eficiente para big data)
- JSON: Formato estructurado y legible
- CSV: Compatible con Excel y análisis estadístico

### **4. Utilidades (`exito_scraper/utils/`)**

#### `html_formatter.py` - Limpieza de HTML
```python
def clean_html_details(html_content: str) -> str:
    # Convierte HTML a texto plano
    # Elimina tags, espacios extra, etc.
```

---

## ⚙️ Configuración (`exito_scraper/config.py`)

### **Categorías Soportadas:**
```python
EXPECTED_URLS = {
    "televisores": "https://www.exito.com/tecnologia/televisores?...",
    "celulares": "https://www.exito.com/tecnologia/celulares?...",
    "lavadoras": "https://www.exito.com/electrodomesticos/lavado-y-secado?...",
    "refrigeracion": "https://www.exito.com/electrodomesticos/refrigeracion?...",
    "audio": "https://www.exito.com/tecnologia/audio?...",
    "videojuegos": "https://www.exito.com/tecnologia/consolas-y-videojuegos?...",
    "deportes": "https://www.exito.com/deportes-y-fitness?..."
}
```

### **Configuración de Red:**
- **Headers:** User-Agent realista para evitar detección
- **Timeout:** 25 segundos por request
- **Rate Limiting:** 1-2 segundos entre requests
- **Idioma:** es-CO (español Colombia)

---

## 🔄 Flujo de Ejecución

### **1. Inicialización**
```python
# main.py
scraper = ExitoScraperAdapter()        # Adaptador de scraping
repo = _make_repo(args.output)         # Repositorio (JSON/CSV)
usecase = ScrapeCategoryUseCase(scraper, repo)  # Caso de uso
```

### **2. Proceso de Extracción**
```
Para cada página (1 to N):
  ┌─ Construir URL con parámetro de página
  ├─ Realizar request HTTP con delay
  ├─ Parsear HTML/JSON response
  ├─ Extraer productos individuales
  ├─ Limpiar HTML en descripciones
  ├─ Crear objetos Producto
  └─ Persistir en formato seleccionado
```

### **3. Estrategias de Parsing**
1. **Preferida:** Extraer estado JSON embebido (más eficiente)
2. **Fallback:** Parsing HTML tradicional con BeautifulSoup

---

## 📊 Datos Extraídos

### **Por cada producto se obtiene:**

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `titulo` | Nombre del producto | "Smart TV Samsung 55\" UHD 4K" |
| `marca` | Marca del fabricante | "Samsung" |
| `precio_texto` | Precio como aparece | "$1.299.900" |
| `precio_valor` | Precio numérico | 1299900 |
| `moneda` | Código de moneda | "COP" |
| `calificacion` | Rating del producto | "4.5/5" |
| `detalles_adicionales` | Descripción limpia | "Pantalla LED con HDR" |
| `imagen` | URL de imagen | "https://..." |
| `link` | URL del producto | "https://..." |
| `categoria` | Categoría extraída | "televisores" |
| `fecha_extraccion` | Timestamp ISO | "2025-09-25T10:30:00" |

---

## 🐳 Containerización

### **Docker Multi-stage Build:**
```dockerfile
# Imagen base optimizada
FROM python:3.11-slim as base

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código de aplicación
COPY exito_scraper/ ./exito_scraper/
```

### **Docker Compose para desarrollo:**
```yaml
services:
  exito-scraper:
    volumes:
      - ./data:/app/data              # Persistencia de datos
      - ./exito_scraper:/app/exito_scraper:ro  # Hot reload
```

---

## 🚀 Casos de Uso

### **1. Análisis de Mercado**
```bash
# Extraer 5 páginas de televisores
docker-compose run --rm exito-scraper scrape --categoria televisores --paginas 5
```

### **2. Monitoreo de Precios**
```bash
# Obtener datos actuales para comparar con históricos
python -m exito_scraper.main scrape --categoria celulares --paginas 3 --output data/celulares_$(date +%Y%m%d).jsonl
```

### **3. Investigación de Productos**
```bash
# Datos para ML o análisis estadístico
docker run --rm -v $(pwd)/data:/app/data exito-scraper scrape --categoria audio --paginas 2
```

---

## 🛡️ Robustez y Manejo de Errores

### **Estrategias Implementadas:**
- ✅ **Rate limiting** para evitar ser bloqueado
- ✅ **User-Agent realista** para parecer navegador real
- ✅ **Timeouts configurables** para manejar conexiones lentas
- ✅ **Fallback de parsing** (JSON → HTML)
- ✅ **Continuación en páginas vacías** (tolerancia a intermitencias)
- ✅ **Limpieza automática de HTML** en contenido
- ✅ **Validación de datos** en el modelo de dominio

---

## 📈 Métricas y Tracking

### **Contadores Implementados:**
- `contador_extraccion_total`: Productos totales extraídos en la sesión
- `contador_extraccion`: Productos por página
- `extraction_status`: Estado de extracción ("OK", "ERROR", etc.)
- `fecha_extraccion`: Timestamp para auditoría

---

## 🔧 Extensibilidad

### **Para agregar nuevas categorías:**
1. Añadir URL en `config.py`
2. No requiere cambios de código adicionales

### **Para nuevos formatos de salida:**
1. Implementar `RepositoryPort`
2. Registrar en `main.py`

### **Para nuevos sitios web:**
1. Implementar `ScraperPort`
2. Mantener la misma interfaz de dominio

---

## 📋 Resumen

Este scraper es un **sistema empresarial robusto** que combina:
- **Arquitectura limpia** para mantenibilidad
- **Estrategias de parsing híbridas** para confiabilidad
- **Containerización** para despliegue consistente
- **Rate limiting ético** para no sobrecargar el servidor
- **Múltiples formatos** para diferentes análisis
- **Documentación completa** para diferentes roles de usuario

Es ideal para **analistas de datos**, **investigadores de mercado** y **desarrolladores** que necesitan datos estructurados del e-commerce de Éxito de manera automatizada y confiable.
