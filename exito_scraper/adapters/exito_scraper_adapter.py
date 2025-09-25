from __future__ import annotations
import re, json, time, random
from typing import Iterable, List, Dict, Any, Optional
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import requests
from bs4 import BeautifulSoup

from ..domain.producto import Producto
from ..domain.ports import ScraperPort
from ..config import EXPECTED_URLS, CATEGORY_API_PATHS, BASE_HOST, DEFAULT_HEADERS, TIMEOUT, REQUEST_DELAY_SECONDS
from ..utils.html_formatter import clean_html_details

class ExitoScraperAdapter(ScraperPort):
    def __init__(self, session: Optional[requests.Session] = None):
        self.session = session or requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        self._global_counter = 0

    def _with_page(self, url: str, page: int) -> str:
        """Reemplaza (o añade) el query param ?page=N."""
        parts = list(urlparse(url))
        qs = parse_qs(parts[4])
        qs["page"] = [str(page)]
        parts[4] = urlencode(qs, doseq=True)
        return urlunparse(parts)

    def _sleep(self):
        lo, hi = REQUEST_DELAY_SECONDS
        time.sleep(random.uniform(lo, hi))

    def _get(self, url: str) -> str:
        r = self.session.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        return r.text

    def _extract_rating_from_product_page(self, product_url: str) -> tuple[str, str]:
        """
        Extrae la calificación y número de opiniones de la página individual del producto.
        Retorna (rating, review_count) como strings.
        """
        try:
            # Headers para evitar detección como bot
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept-Language': 'es-CO,es;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = self.session.get(product_url, headers=headers, timeout=TIMEOUT)
            if response.status_code != 200:
                return "", ""
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar patrones de calificación en el texto
            page_text = soup.get_text()
            
            # Patrón para "X.X Calificación promedio entre Y opiniones"
            rating_pattern = r'(\d+\.?\d*)\s*Calificación\s+promedio\s+entre\s+(\d+)\s+opiniones'
            rating_match = re.search(rating_pattern, page_text, re.IGNORECASE)
            
            if rating_match:
                rating = rating_match.group(1)
                review_count = rating_match.group(2)
                return rating, review_count
            
            # Patrón alternativo para "X.X de 5 estrellas (Y opiniones)"
            alt_pattern = r'(\d+\.?\d*)\s*de\s+5\s+estrellas.*?(\d+)\s+opiniones'
            alt_match = re.search(alt_pattern, page_text, re.IGNORECASE)
            
            if alt_match:
                rating = alt_match.group(1)
                review_count = alt_match.group(2)
                return rating, review_count
                
            # Buscar solo número de opiniones si no hay rating
            review_pattern = r'(\d+)\s+[Oo]piniones'
            review_match = re.search(review_pattern, page_text)
            
            if review_match:
                review_count = review_match.group(1)
                return "No tiene Calificacion", review_count
                
            return "No tiene Calificacion", "0"
            
        except Exception as e:
            # En caso de error, retornar valores por defecto
            return "No tiene Calificacion", "0"

    # ---------- Parsers helpers ----------

    def _extract_state_json(self, html: str) -> Optional[dict]:
        """
        Intenta extraer un gran objeto JSON embebido en el HTML (estado/SSR),
        común en catálogos modernos. Fallback a None si no existe.
        """
        # Busca llaves típicas de estado embebido
        # 1) __STATE__ = {...};  2) __APOLLO_STATE__ = {...};  3) __NEXT_DATA__ = {...}
        patterns = [
            r"__STATE__\s*=\s*(\{.*?\})\s*;\s*</script>",
            r"__APOLLO_STATE__\s*=\s*(\{.*?\})\s*;\s*</script>",
            r'"__NEXT_DATA__"\s*:\s*(\{.*?\})\s*,\s*"__APOLLO_STATE__"',
            r'"__NEXT_DATA__"\s*:\s*(\{.*?\})\s*<\/script>',
        ]
        for pat in patterns:
            m = re.search(pat, html, re.DOTALL)
            if m:
                try:
                    return json.loads(m.group(1))
                except json.JSONDecodeError:
                    # Algunos sitios minifican con caracteres no estándar; intenta limpieza básica
                    cleaned = m.group(1).replace("\n", "").replace("\t", "")
                    try:
                        return json.loads(cleaned)
                    except Exception:
                        continue
        return None

    def _guess_items_from_state(self, state: dict) -> List[Dict[str, Any]]:
        """
        Dado un estado embebido, intenta recuperar una lista de productos
        normalizados con campos clave (name, brand, price, currency, image, link).
        """
        items: List[Dict[str, Any]] = []

        # Heurística 1: Objetos con 'productName' y 'brand'
        for v in (state.values() if isinstance(state, dict) else []):
            if isinstance(v, dict) and ("productName" in v and "brand" in v):
                name = v.get("productName") or v.get("product-name") or ""
                brand = v.get("brand") or ""
                link_text = v.get("linkText") or v.get("slug") or ""
                # Intenta bajar a la primera SKU/offer
                price, currency, image = None, None, ""
                try:
                    # rutas comunes en catálogos VTEX/SSR
                    # items -> sellers -> commertialOffer -> Price/CurrencyCode
                    it0 = (v.get("items") or [])[0]
                    images = it0.get("images") or []
                    if images:
                        image = images[0].get("imageUrl") or images[0].get("url") or ""
                    sellers = it0.get("sellers") or []
                    if sellers:
                        offer = sellers[0].get("commertialOffer") or sellers[0].get("commercialOffer") or {}
                        price = offer.get("Price") or offer.get("price") or None
                        currency = offer.get("CurrencyCode") or offer.get("currency") or None
                except Exception:
                    pass

                items.append({
                    "name": name,
                    "brand": brand,
                    "price": price,
                    "currency": currency,
                    "image": image,
                    "link": f"{BASE_HOST}/{link_text}/p" if link_text else "",
                    "rating": "",   # si existe en el estado, podría mapearse aquí
                    "details": "",
                })

        # Heurística 2: __NEXT_DATA__ (cuando la página es Next.js)
        if not items and isinstance(state, dict):
            # Busca en props -> pageProps -> ... listas de productos
            props = (state.get("props") or {}).get("pageProps") or {}
            candidates = []
            for k, v in props.items():
                if isinstance(v, list) and v and isinstance(v[0], dict) and ("name" in v[0] or "productName" in v[0]):
                    candidates = v
                    break
            for c in candidates:
                items.append({
                    "name": c.get("name") or c.get("productName") or "",
                    "brand": c.get("brand") or "",
                    "price": (c.get("price") or {}).get("value") if isinstance(c.get("price"), dict) else c.get("price"),
                    "currency": (c.get("price") or {}).get("currency") if isinstance(c.get("price"), dict) else None,
                    "image": (c.get("image") or [""])[0] if isinstance(c.get("image"), list) else c.get("image") or "",
                    "link": c.get("url") or c.get("link") or "",
                    "rating": str(c.get("aggregateRating", {}).get("ratingValue", "")) if isinstance(c.get("aggregateRating"), dict) else "",
                    "details": c.get("description") or "",
                })

        return items

    def _guess_items_from_html(self, html: str) -> List[Dict[str, Any]]:
        """
        Fallback: parsea tarjetas de producto en el HTML.
        """
        soup = BeautifulSoup(html, "lxml")
        items: List[Dict[str, Any]] = []
        # Selector genérico para catálogos (ajustable)
        for card in soup.select("a[href*='/p']"):
            # Evita anchors vacíos
            title_raw = card.get("title") or ""
            title = (title_raw[0] if isinstance(title_raw, list) and title_raw else str(title_raw)).strip()
            link = card.get("href") or ""
            if not link or not title:
                continue

            # Sube al contenedor para buscar precio/imagen/brand si están cerca
            container = card.parent
            price_text = ""
            img = card.select_one("img")
            if img and (img.get("src") or img.get("data-src")):
                image = img.get("src") or img.get("data-src")
            else:
                image = ""

            # heurística para precio visible en el contenedor
            price_el = None
            for sel in [".price", ".selling-price", "[class*='price']", "[data-testid*='price']"]:
                price_el = card.select_one(sel) or (container.select_one(sel) if container else None)
                if price_el:
                    break
            if price_el:
                price_text = price_el.get_text(strip=True)

            # Ensure link is a string
            link_str = link[0] if isinstance(link, list) and link else str(link)
            
            # Ensure image is a string
            image_str = image[0] if isinstance(image, list) and image else str(image) if image else ""

            items.append({
                "name": title,
                "brand": "",
                "price": None,
                "currency": None,
                "image": (BASE_HOST + image_str) if image_str and image_str.startswith("/") else image_str,
                "link": (BASE_HOST + link_str) if link_str.startswith("/") else link_str,
                "rating": "",
                "details": "",
                "price_text": price_text,
            })
        return items

    def _first_int_or_none(self, s: str) -> Optional[int]:
        s = s or ""
        m = re.search(r"(\d[\d\.\, ]+)", s)
        if not m:
            return None
        num = m.group(1).replace(".", "").replace(" ", "").replace(",", "")
        try:
            return int(num)
        except Exception:
            return None

    def _infer_size(self, title: str) -> str:
        # Detecta pulgadas típicas (e.g., 55", 65 pulgadas)
        m = re.search(r"(\d{2}(?:\.\d)?)\s*(?:\"|pulg|pulgadas)", title, re.IGNORECASE)
        return f'{m.group(1)}"' if m else ""

    # ---------- Public Port ----------

    def scrape(self, categoria: str, page: int) -> Iterable[Producto]:
        if categoria not in EXPECTED_URLS:
            raise ValueError(f"Categoría no soportada: {categoria}")

        # Use VTEX API with proper category path to ensure we get products only from the specific category
        items_per_page = 50
        _from = (page - 1) * items_per_page
        _to = _from + items_per_page - 1
        
        # Get the category path for the API
        category_path = CATEGORY_API_PATHS.get(categoria)
        if not category_path:
            raise ValueError(f"No se encontró el path de categoría para: {categoria}")
        
        # Build the VTEX API URL using the category path (this ensures we get products from the exact category)
        api_url = f"https://www.exito.com/api/catalog_system/pub/products/search/{category_path}?_from={_from}&_to={_to}"
        
        try:
            response = self.session.get(api_url, timeout=TIMEOUT)
            response.raise_for_status()
            
            # Parse JSON response
            import json
            items = json.loads(response.text)
            
        except Exception as e:
            print(f"Error accessing VTEX API: {e}")
            # Fallback to original HTML scraping method
            url = self._with_page(EXPECTED_URLS[categoria], page)
            html = self._get(url)

            # 1) Intenta estado embebido
            state = self._extract_state_json(html)
            items = self._guess_items_from_state(state) if state else []
            # 2) Fallback: tarjetas HTML
            if not items:
                items = self._guess_items_from_html(html)

        productos: List[Producto] = []

        for idx, it in enumerate(items, start=1):
            self._global_counter += 1
            
            # Handle both VTEX API format and old format
            if 'productName' in it:  # VTEX API format
                titulo = (it.get("productName") or "").strip()
                marca = (it.get("brand") or "").strip()
                link_text = (it.get("linkText") or "").strip()
                link = f"{BASE_HOST}/{link_text}/p" if link_text else ""
                
                # Get pricing from VTEX structure
                precio_valor = None
                moneda = "COP"
                precio_texto = ""
                img = ""
                
                if 'items' in it and it['items']:
                    item = it['items'][0]
                    # Get image
                    if 'images' in item and item['images']:
                        img = item['images'][0].get('imageUrl', '')
                    
                    # Get price
                    if 'sellers' in item and item['sellers']:
                        seller = item['sellers'][0]
                        offer = seller.get('commertialOffer', {})
                        precio_valor = offer.get('Price')
                        if precio_valor:
                            precio_valor = int(round(float(precio_valor)))
                            precio_texto = f"COP {precio_valor}"
                
                # Extract detailed specifications from VTEX data
                rating = "No tiene Calificacion"
                review_count = "0"
                
                # Extract rating from individual product page (only for first few products to save time)
                if link and idx <= 10:  # Only check ratings for first 10 products per page
                    try:
                        rating, review_count = self._extract_rating_from_product_page(link)
                    except:
                        rating = "No tiene Calificacion"
                        review_count = "0"
                
                # Build detailed specifications from allSpecifications
                details_parts = []
                
                # Add metaTagDescription if available
                meta_desc = it.get('metaTagDescription', '').strip()
                if meta_desc:
                    details_parts.append(f"Descripción: {meta_desc}")
                
                # Extract key specifications
                specs_dict = {}
                for spec_name in it.get('allSpecifications', []):
                    if spec_name in it:
                        value = it[spec_name]
                        if isinstance(value, list) and value:
                            specs_dict[spec_name] = value[0]
                        elif value:
                            specs_dict[spec_name] = value
                
                # Format important specifications
                important_specs = []
                spec_priority = [
                    'Tamaño de Pantalla', 'Resolución de la pantalla', 'Resolución', 'Sistema operativo',
                    'Tipo de pantalla', 'Tipo De pantalla', 'Smart TV', 'Conexión Wi-fi', 'Bluetooth',
                    'Número De Puertos HDMI', 'Número De Puertos USB', 'Potencia de Audio', 'Procesador',
                    'Garantía', 'Peso', 'Ancho', 'Alto', 'Profundidad', 'Modelo', 'Referencia'
                ]
                
                # Add prioritized specs
                for spec_name in spec_priority:
                    if spec_name in specs_dict and specs_dict[spec_name]:
                        value = str(specs_dict[spec_name]).strip()
                        if value and value.lower() not in ['no', 'false', '0']:
                            important_specs.append(f"{spec_name}: {value}")
                            
                # Add remaining specs (limit total)
                added_specs = set(spec_priority)
                for spec_name, value in specs_dict.items():
                    if len(important_specs) >= 15:  # Limit to 15 specs
                        break
                    if spec_name not in added_specs and value:
                        value_str = str(value).strip()
                        if value_str and value_str.lower() not in ['no', 'false', '0']:
                            important_specs.append(f"{spec_name}: {value_str}")
                            added_specs.add(spec_name)
                
                if important_specs:
                    details_parts.append("Especificaciones: " + ". ".join(important_specs))
                
                details = ". ".join(details_parts)
                
            else:  # Old format from HTML scraping
                titulo = (it.get("name") or "").strip()
                marca = (it.get("brand") or "").strip()
                img = (it.get("image") or "").strip()
                link = (it.get("link") or "").strip()
                rating = str(it.get("rating") or "").strip()
                if not rating or rating == "" or rating == "0":
                    rating = "No tiene Calificacion"
                review_count = "0"  # Not available in old format
                details = (it.get("details") or "").strip()

                # precio
                precio_valor = it.get("price")
                moneda = it.get("currency")
                precio_texto = it.get("price_text") or ""
                if precio_valor and not precio_texto:
                    precio_texto = f"{moneda or 'COP'} {int(round(float(precio_valor)))}"
                if not precio_valor and precio_texto:
                    precio_valor = self._first_int_or_none(precio_texto)

            # tamaño: heurística por título
            tam = self._infer_size(titulo) if "televisor" in categoria or "televisores" in categoria else ""

            # Limpiar detalles adicionales de HTML
            details_cleaned = clean_html_details(details) if details else ""

            # Convertir calificación "0" a "No tiene Calificacion"
            if rating == "0":
                rating = "No tiene Calificacion"

            status = "OK"
            if not titulo:
                status = "MISSING_FIELDS"

            productos.append(Producto(
                contador_extraccion_total=self._global_counter,
                contador_extraccion=idx,
                titulo=titulo,
                marca=marca,
                precio_texto=precio_texto,
                precio_valor=precio_valor if isinstance(precio_valor, int) else (int(precio_valor) if isinstance(precio_valor, float) else None),
                moneda=moneda or ("COP" if precio_valor else None),
                tamaño=tam,
                calificacion=rating,
                numero_opiniones=review_count,
                detalles_adicionales=details_cleaned,
                fuente="exito.com",
                categoria=categoria,
                imagen=img,
                link=link if link.startswith("http") else (BASE_HOST + link if link else ""),
                pagina=page,
                fecha_extraccion=Producto.now_iso(),
                extraction_status=status
            ))

        self._sleep()
        return productos
