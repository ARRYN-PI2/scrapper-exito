# appExito/src/domain/entities/product.py
"""
Entidad Product - Versión básica para empezar
Representa un producto extraído del sitio web de Éxito
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal


@dataclass
class Product:
    """
    Entidad Product que representa un producto extraído.
    Empezamos con los campos esenciales y vamos agregando más según necesitemos.
    """
    
    # Campos obligatorios
    nombre: str
    url_producto: str
    
    # Campos opcionales básicos
    precio: Optional[Decimal] = None
    marca: Optional[str] = None
    categoria: Optional[str] = None
    imagen: Optional[str] = None
    
    # Metadatos de extracción
    fuente: str = "exito.com"
    timestamp_extraccion: datetime = field(default_factory=datetime.now)
    extraction_status: str = "pending"  # pending, success, failed
    
    # Atributos extra que iremos descubriendo
    atributos_extra: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validaciones básicas después de crear el objeto"""
        self._validate_required_fields()
        self._clean_data()
    
    def _validate_required_fields(self):
        """Valida que los campos requeridos estén presentes"""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del producto es requerido")
        
        if not self.url_producto or not self.url_producto.strip():
            raise ValueError("La URL del producto es requerida")
        
        if self.precio is not None and self.precio < 0:
            raise ValueError("El precio no puede ser negativo")
    
    def _clean_data(self):
        """Limpia y normaliza los datos básicos"""
        self.nombre = self.nombre.strip()
        self.url_producto = self.url_producto.strip()
        
        if self.marca:
            self.marca = self.marca.strip()
        
        if self.categoria:
            self.categoria = self.categoria.strip().lower()
    
    def mark_as_extracted(self, status: str = "success") -> None:
        """Marca el producto como extraído exitosamente"""
        if status not in ["success", "failed", "pending"]:
            raise ValueError("Status debe ser 'success', 'failed' o 'pending'")
        
        self.extraction_status = status
        self.timestamp_extraccion = datetime.now()
    
    def add_extra_attribute(self, key: str, value: Any) -> None:
        """Agrega un atributo extra al producto"""
        self.atributos_extra[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el producto a diccionario para fácil serialización"""
        return {
            "nombre": self.nombre,
            "url_producto": self.url_producto,
            "precio": float(self.precio) if self.precio else None,
            "marca": self.marca,
            "categoria": self.categoria,
            "imagen": self.imagen,
            "fuente": self.fuente,
            "timestamp_extraccion": self.timestamp_extraccion.isoformat(),
            "extraction_status": self.extraction_status,
            "atributos_extra": self.atributos_extra,
        }
    
    def __str__(self) -> str:
        """Representación legible del producto"""
        precio_str = f"${self.precio}" if self.precio else "Sin precio"
        return f"Product(nombre='{self.nombre}', precio={precio_str}, marca={self.marca})"


# Función helper para crear productos fácilmente durante testing
def create_test_product(
    nombre: str = "Producto de Prueba",
    url: str = "https://www.exito.com/test-product/p",
    precio: Optional[float] = None
) -> Product:
    """
    Función helper para crear productos de prueba
    """
    precio_decimal = Decimal(str(precio)) if precio else None
    
    return Product(
        nombre=nombre,
        url_producto=url,
        precio=precio_decimal
    )