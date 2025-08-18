"""
Modelo de datos para ingredientes.
"""
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum

class EstadoIngrediente(str, Enum):
    """Estados posibles de un ingrediente."""
    FRESCO = "fresco"
    MADURO = "maduro"
    COCIDO = "cocido"
    CRUDO = "crudo"
    CONGELADO = "congelado"
    ENLATADO = "enlatado"
    SECO = "seco"
    DESCONOCIDO = "desconocido"

class UnidadMedida(str, Enum):
    """Unidades de medida comunes."""
    GRAMOS = "g"
    KILOGRAMOS = "kg"
    MILILITROS = "ml"
    LITROS = "l"
    TAZAS = "taza"
    CUCHARADAS = "cucharada"
    CUCHARADITAS = "cucharadita"
    UNIDADES = "unidad"
    PIEZAS = "pieza"
    MANOJOS = "manojo"
    RODAJAS = "rodaja"
    TROZOS = "trozo"

class Ingrediente(BaseModel):
    """Modelo de ingrediente detectado o especificado."""
    
    nombre: str = Field(..., description="Nombre del ingrediente")
    cantidad: Optional[float] = Field(None, description="Cantidad del ingrediente")
    unidad: Optional[UnidadMedida] = Field(None, description="Unidad de medida")
    estado: EstadoIngrediente = Field(EstadoIngrediente.DESCONOCIDO, description="Estado del ingrediente")
    confianza: float = Field(0.0, ge=0.0, le=1.0, description="Nivel de confianza en la detección")
    detectado: bool = Field(True, description="Si fue detectado por IA o especificado manualmente")
    esencial: bool = Field(True, description="Si es esencial para la receta")
    categoria: Optional[str] = Field(None, description="Categoría del ingrediente (vegetal, proteína, etc.)")
    alergenos: List[str] = Field(default_factory=list, description="Alérgenos contenidos")
    temporada: Optional[str] = Field(None, description="Temporada óptima del ingrediente")
    
    @validator('nombre')
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre del ingrediente no puede estar vacío')
        return v.strip().lower()
    
    @validator('confianza')
    def confianza_rango(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('La confianza debe estar entre 0.0 y 1.0')
        return v
    
    def __str__(self) -> str:
        """Representación string del ingrediente."""
        cantidad_str = f"{self.cantidad} {self.unidad}" if self.cantidad and self.unidad else ""
        confianza_str = f" (confianza: {self.confianza:.1%})" if self.detectado else ""
        return f"{self.nombre} {cantidad_str}{confianza_str}"
    
    def to_dict(self) -> dict:
        """Convierte el ingrediente a diccionario."""
        return {
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "unidad": self.unidad.value if self.unidad else None,
            "estado": self.estado.value,
            "confianza": self.confianza,
            "detectado": self.detectado,
            "esencial": self.esencial,
            "categoria": self.categoria,
            "alergenos": self.alergenos,
            "temporada": self.temporada
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Ingrediente':
        """Crea un ingrediente desde un diccionario."""
        return cls(**data)

class ListaIngredientes(BaseModel):
    """Lista de ingredientes con metadatos."""
    
    ingredientes: List[Ingrediente] = Field(default_factory=list, description="Lista de ingredientes")
    total_ingredientes: int = Field(0, description="Total de ingredientes")
    calidad_imagen: Optional[str] = Field(None, description="Calidad de la imagen analizada")
    error: Optional[str] = Field(None, description="Mensaje de error si aplica")
    
    def __init__(self, **data):
        super().__init__(**data)
        self.total_ingredientes = len(self.ingredientes)
    
    def agregar_ingrediente(self, ingrediente: Ingrediente) -> None:
        """Agrega un ingrediente a la lista."""
        self.ingredientes.append(ingrediente)
        self.total_ingredientes = len(self.ingredientes)
    
    def obtener_por_confianza(self, confianza_minima: float = 0.7) -> List[Ingrediente]:
        """Obtiene ingredientes con confianza mínima."""
        return [ing for ing in self.ingredientes if ing.confianza >= confianza_minima]
    
    def obtener_por_categoria(self, categoria: str) -> List[Ingrediente]:
        """Obtiene ingredientes por categoría."""
        return [ing for ing in self.ingredientes if ing.categoria == categoria]
    
    def obtener_esenciales(self) -> List[Ingrediente]:
        """Obtiene ingredientes marcados como esenciales."""
        return [ing for ing in self.ingredientes if ing.esencial]
    
    def obtener_nombres(self) -> List[str]:
        """Obtiene lista de nombres de ingredientes."""
        return [ing.nombre for ing in self.ingredientes]
    
    def tiene_alergenos(self, alergenos_buscar: List[str]) -> bool:
        """Verifica si contiene alguno de los alérgenos especificados."""
        for ingrediente in self.ingredientes:
            for alergeno in alergenos_buscar:
                if alergeno.lower() in [a.lower() for a in ingrediente.alergenos]:
                    return True
        return False
