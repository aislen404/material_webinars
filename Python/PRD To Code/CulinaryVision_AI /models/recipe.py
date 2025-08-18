"""
Modelo de datos para recetas.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum
from datetime import datetime
from .ingredient import Ingrediente

class NivelDificultad(str, Enum):
    """Niveles de dificultad de las recetas."""
    PRINCIPIANTE = "principiante"
    INTERMEDIO = "intermedio"
    AVANZADO = "avanzado"
    EXPERTO = "experto"

class TipoCocina(str, Enum):
    """Tipos de cocina."""
    ITALIANA = "italiana"
    MEXICANA = "mexicana"
    ASIATICA = "asiatica"
    MEDITERRANEA = "mediterranea"
    FRANCESA = "francesa"
    ESPANOLA = "espanola"
    INTERNACIONAL = "internacional"
    FUSION = "fusion"
    VEGETARIANA = "vegetariana"
    VEGANA = "vegana"

class Instruccion(BaseModel):
    """Modelo para instrucciones paso a paso."""
    
    paso: int = Field(..., description="Número del paso")
    accion: str = Field(..., description="Descripción de la acción")
    tiempo_estimado: Optional[str] = Field(None, description="Tiempo estimado para el paso")
    tip: Optional[str] = Field(None, description="Consejo profesional opcional")
    
    @validator('paso')
    def paso_positivo(cls, v):
        if v <= 0:
            raise ValueError('El número de paso debe ser positivo')
        return v
    
    @validator('accion')
    def accion_no_vacia(cls, v):
        if not v or not v.strip():
            raise ValueError('La acción no puede estar vacía')
        return v.strip()

class InformacionNutricional(BaseModel):
    """Información nutricional de la receta."""
    
    calorias_por_porcion: Optional[int] = Field(None, description="Calorías por porción")
    proteinas_g: Optional[float] = Field(None, description="Proteínas en gramos")
    carbohidratos_g: Optional[float] = Field(None, description="Carbohidratos en gramos")
    grasas_g: Optional[float] = Field(None, description="Grasas en gramos")
    fibra_g: Optional[float] = Field(None, description="Fibra en gramos")
    sodio_mg: Optional[float] = Field(None, description="Sodio en miligramos")
    azucares_g: Optional[float] = Field(None, description="Azúcares en gramos")

class IngredienteReceta(BaseModel):
    """Ingrediente específico para una receta."""
    
    nombre: str = Field(..., description="Nombre del ingrediente")
    cantidad: str = Field(..., description="Cantidad del ingrediente")
    unidad: str = Field(..., description="Unidad de medida")
    detectado: bool = Field(True, description="Si fue detectado en la imagen")
    esencial: bool = Field(True, description="Si es esencial para la receta")
    opcional: bool = Field(False, description="Si es opcional")
    sustitucion: Optional[str] = Field(None, description="Sustitución sugerida")

class Receta(BaseModel):
    """Modelo completo de una receta."""
    
    id: int = Field(..., description="ID único de la receta")
    nombre: str = Field(..., description="Nombre de la receta")
    descripcion_corta: str = Field(..., description="Descripción breve")
    tiempo_preparacion_min: int = Field(..., description="Tiempo de preparación en minutos")
    tiempo_coccion_min: int = Field(..., description="Tiempo de cocción en minutos")
    tiempo_total_min: int = Field(..., description="Tiempo total en minutos")
    dificultad_estrellas: int = Field(..., ge=1, le=5, description="Dificultad en estrellas (1-5)")
    porciones: int = Field(..., description="Número de porciones")
    tipo_cocina: TipoCocina = Field(..., description="Tipo de cocina")
    ingredientes: List[IngredienteReceta] = Field(..., description="Lista de ingredientes")
    instrucciones: List[Instruccion] = Field(..., description="Instrucciones paso a paso")
    informacion_nutricional: InformacionNutricional = Field(..., description="Información nutricional")
    tags: List[str] = Field(default_factory=list, description="Etiquetas de la receta")
    nivel_dificultad: NivelDificultad = Field(..., description="Nivel de dificultad")
    consejos_chef: List[str] = Field(default_factory=list, description="Consejos del chef")
    variaciones: List[str] = Field(default_factory=list, description="Variaciones de la receta")
    maridaje: Optional[str] = Field(None, description="Sugerencias de maridaje")
    conservacion: Optional[str] = Field(None, description="Instrucciones de conservación")
    presentacion: Optional[str] = Field(None, description="Instrucciones de presentación")
    
    @validator('nombre')
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre de la receta no puede estar vacío')
        return v.strip()
    
    @validator('tiempo_total_min')
    def tiempo_total_coherente(cls, v, values):
        prep = values.get('tiempo_preparacion_min', 0)
        coccion = values.get('tiempo_coccion_min', 0)
        if v != prep + coccion:
            raise ValueError('El tiempo total debe ser la suma de preparación y cocción')
        return v
    
    @validator('porciones')
    def porciones_positivas(cls, v):
        if v <= 0:
            raise ValueError('El número de porciones debe ser positivo')
        return v
    
    def calcular_tiempo_total(self) -> int:
        """Calcula el tiempo total de la receta."""
        return self.tiempo_preparacion_min + self.tiempo_coccion_min
    
    def es_vegetariana(self) -> bool:
        """Verifica si la receta es vegetariana."""
        ingredientes_carne = ['pollo', 'carne', 'cerdo', 'res', 'ternera', 'cordero', 'pavo']
        for ingrediente in self.ingredientes:
            if any(carne in ingrediente.nombre.lower() for carne in ingredientes_carne):
                return False
        return True
    
    def es_vegana(self) -> bool:
        """Verifica si la receta es vegana."""
        ingredientes_animales = ['huevo', 'leche', 'queso', 'mantequilla', 'crema', 'yogur']
        for ingrediente in self.ingredientes:
            if any(animal in ingrediente.nombre.lower() for animal in ingredientes_animales):
                return False
        return True
    
    def tiene_alergenos(self, alergenos: List[str]) -> bool:
        """Verifica si la receta contiene alérgenos específicos."""
        for ingrediente in self.ingredientes:
            for alergeno in alergenos:
                if alergeno.lower() in ingrediente.nombre.lower():
                    return True
        return False
    
    def obtener_ingredientes_detectados(self) -> List[IngredienteReceta]:
        """Obtiene solo los ingredientes que fueron detectados."""
        return [ing for ing in self.ingredientes if ing.detectado]
    
    def obtener_ingredientes_esenciales(self) -> List[IngredienteReceta]:
        """Obtiene solo los ingredientes esenciales."""
        return [ing for ing in self.ingredientes if ing.esencial]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la receta a diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion_corta": self.descripcion_corta,
            "tiempo_preparacion_min": self.tiempo_preparacion_min,
            "tiempo_coccion_min": self.tiempo_coccion_min,
            "tiempo_total_min": self.tiempo_total_min,
            "dificultad_estrellas": self.dificultad_estrellas,
            "porciones": self.porciones,
            "tipo_cocina": self.tipo_cocina.value,
            "ingredientes": [ing.dict() for ing in self.ingredientes],
            "instrucciones": [inst.dict() for inst in self.instrucciones],
            "informacion_nutricional": self.informacion_nutricional.dict(),
            "tags": self.tags,
            "nivel_dificultad": self.nivel_dificultad.value,
            "consejos_chef": self.consejos_chef,
            "variaciones": self.variaciones,
            "maridaje": self.maridaje,
            "conservacion": self.conservacion,
            "presentacion": self.presentacion
        }

class MetadataRecetas(BaseModel):
    """Metadatos de la generación de recetas."""
    
    total_recetas: int = Field(..., description="Total de recetas generadas")
    ingredientes_utilizados: List[str] = Field(..., description="Lista de ingredientes utilizados")
    tiempo_generacion: str = Field(..., description="Timestamp de generación")
    temporada: str = Field(..., description="Temporada actual")
    version: str = Field("1.0", description="Versión del sistema")
    
    @validator('tiempo_generacion')
    def tiempo_generacion_valido(cls, v):
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
            return v
        except ValueError:
            raise ValueError('Formato de tiempo de generación inválido')

class ColeccionRecetas(BaseModel):
    """Colección completa de recetas generadas."""
    
    metadata: MetadataRecetas = Field(..., description="Metadatos de la generación")
    recetas: List[Receta] = Field(..., description="Lista de recetas")
    
    def __init__(self, **data):
        super().__init__(**data)
        # Actualizar metadata con información real
        self.metadata.total_recetas = len(self.recetas)
    
    def obtener_por_dificultad(self, dificultad: NivelDificultad) -> List[Receta]:
        """Obtiene recetas por nivel de dificultad."""
        return [receta for receta in self.recetas if receta.nivel_dificultad == dificultad]
    
    def obtener_por_tiempo(self, tiempo_maximo: int) -> List[Receta]:
        """Obtiene recetas que se pueden preparar en el tiempo especificado."""
        return [receta for receta in self.recetas if receta.tiempo_total_min <= tiempo_maximo]
    
    def obtener_vegetarianas(self) -> List[Receta]:
        """Obtiene recetas vegetarianas."""
        return [receta for receta in self.recetas if receta.es_vegetariana()]
    
    def obtener_veganas(self) -> List[Receta]:
        """Obtiene recetas veganas."""
        return [receta for receta in self.recetas if receta.es_vegana()]
    
    def ordenar_por_dificultad(self) -> List[Receta]:
        """Ordena las recetas por dificultad (más fácil primero)."""
        orden_dificultad = {
            NivelDificultad.PRINCIPIANTE: 1,
            NivelDificultad.INTERMEDIO: 2,
            NivelDificultad.AVANZADO: 3,
            NivelDificultad.EXPERTO: 4
        }
        return sorted(self.recetas, key=lambda x: orden_dificultad[x.nivel_dificultad])
    
    def ordenar_por_tiempo(self) -> List[Receta]:
        """Ordena las recetas por tiempo total (más rápido primero)."""
        return sorted(self.recetas, key=lambda x: x.tiempo_total_min)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la colección a diccionario."""
        return {
            "metadata": self.metadata.dict(),
            "recetas": [receta.to_dict() for receta in self.recetas]
        }
