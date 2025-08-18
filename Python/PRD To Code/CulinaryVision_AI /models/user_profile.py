"""
Modelo de datos para el perfil de usuario.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum

class NivelCulinario(str, Enum):
    """Niveles de experiencia culinaria."""
    PRINCIPIANTE = "principiante"
    INTERMEDIO = "intermedio"
    AVANZADO = "avanzado"
    EXPERTO = "experto"

class RestriccionDietetica(str, Enum):
    """Restricciones dietéticas comunes."""
    VEGETARIANO = "vegetariano"
    VEGANO = "vegano"
    SIN_GLUTEN = "sin_gluten"
    SIN_LACTOSA = "sin_lactosa"
    SIN_FRUTOS_SECOS = "sin_frutos_secos"
    SIN_MARISCOS = "sin_mariscos"
    BAJO_SODIO = "bajo_sodio"
    BAJO_CALORIAS = "bajo_calorias"
    KETO = "keto"
    PALEO = "paleo"

class PreferenciaCultural(str, Enum):
    """Preferencias culturales de cocina."""
    MEDITERRANEA = "mediterranea"
    ASIATICA = "asiatica"
    MEXICANA = "mexicana"
    ITALIANA = "italiana"
    FRANCESA = "francesa"
    ESPANOLA = "espanola"
    LATINA = "latina"
    ORIENTAL = "oriental"
    INTERNACIONAL = "internacional"
    FUSION = "fusion"

class Alergeno(str, Enum):
    """Alérgenos comunes."""
    GLUTEN = "gluten"
    LACTOSA = "lactosa"
    HUEVOS = "huevos"
    FRUTOS_SECOS = "frutos_secos"
    MARISCOS = "mariscos"
    PESCADO = "pescado"
    SOJA = "soja"
    SESAMO = "sesamo"
    MOSTAZA = "mostaza"
    APIO = "apio"

class PerfilUsuario(BaseModel):
    """Perfil completo del usuario."""
    
    # Información básica
    nombre: Optional[str] = Field(None, description="Nombre del usuario")
    nivel_culinario: NivelCulinario = Field(NivelCulinario.INTERMEDIO, description="Nivel de experiencia culinaria")
    tiempo_disponible: int = Field(30, ge=5, le=180, description="Tiempo disponible en minutos")
    num_personas: int = Field(2, ge=1, le=10, description="Número de personas para cocinar")
    
    # Preferencias dietéticas
    restricciones_dieteticas: List[RestriccionDietetica] = Field(default_factory=list, description="Restricciones dietéticas")
    alergenos: List[Alergeno] = Field(default_factory=list, description="Alérgenos a evitar")
    preferencias_culturales: List[PreferenciaCultural] = Field(default_factory=list, description="Preferencias culturales")
    
    # Preferencias de sabor
    nivel_picante: int = Field(2, ge=1, le=5, description="Nivel de picante preferido (1-5)")
    preferencia_salado: bool = Field(True, description="Prefiere sabores salados")
    preferencia_dulce: bool = Field(True, description="Prefiere sabores dulces")
    preferencia_amargo: bool = Field(False, description="Prefiere sabores amargos")
    preferencia_acido: bool = Field(True, description="Prefiere sabores ácidos")
    
    # Preferencias nutricionales
    objetivo_calorico: Optional[int] = Field(None, ge=800, le=3000, description="Objetivo calórico diario")
    preferencia_proteinas: bool = Field(True, description="Prefiere recetas altas en proteínas")
    preferencia_fibra: bool = Field(True, description="Prefiere recetas altas en fibra")
    evitar_grasas: bool = Field(False, description="Evita recetas altas en grasas")
    
    # Configuración de la aplicación
    max_recetas_por_sesion: int = Field(5, ge=3, le=10, description="Máximo de recetas por sesión")
    mostrar_informacion_nutricional: bool = Field(True, description="Mostrar información nutricional")
    mostrar_consejos_chef: bool = Field(True, description="Mostrar consejos del chef")
    mostrar_variaciones: bool = Field(True, description="Mostrar variaciones de recetas")
    
    # Historial y preferencias aprendidas
    recetas_favoritas: List[str] = Field(default_factory=list, description="IDs de recetas favoritas")
    ingredientes_favoritos: List[str] = Field(default_factory=list, description="Ingredientes favoritos")
    ingredientes_evitados: List[str] = Field(default_factory=list, description="Ingredientes a evitar")
    tecnicas_preferidas: List[str] = Field(default_factory=list, description="Técnicas culinarias preferidas")
    
    @validator('tiempo_disponible')
    def tiempo_disponible_valido(cls, v):
        if v < 5:
            raise ValueError('El tiempo mínimo disponible debe ser 5 minutos')
        if v > 180:
            raise ValueError('El tiempo máximo disponible debe ser 180 minutos')
        return v
    
    @validator('num_personas')
    def num_personas_valido(cls, v):
        if v < 1:
            raise ValueError('Debe cocinar para al menos 1 persona')
        if v > 10:
            raise ValueError('El máximo de personas es 10')
        return v
    
    @validator('nivel_picante')
    def nivel_picante_valido(cls, v):
        if not 1 <= v <= 5:
            raise ValueError('El nivel de picante debe estar entre 1 y 5')
        return v
    
    def es_vegetariano(self) -> bool:
        """Verifica si el usuario es vegetariano."""
        return RestriccionDietetica.VEGETARIANO in self.restricciones_dieteticas
    
    def es_vegano(self) -> bool:
        """Verifica si el usuario es vegano."""
        return RestriccionDietetica.VEGANO in self.restricciones_dieteticas
    
    def tiene_restriccion_gluten(self) -> bool:
        """Verifica si el usuario tiene restricción de gluten."""
        return RestriccionDietetica.SIN_GLUTEN in self.restricciones_dieteticas
    
    def tiene_restriccion_lactosa(self) -> bool:
        """Verifica si el usuario tiene restricción de lactosa."""
        return RestriccionDietetica.SIN_LACTOSA in self.restricciones_dieteticas
    
    def puede_consumir_ingrediente(self, ingrediente: str) -> bool:
        """Verifica si el usuario puede consumir un ingrediente específico."""
        ingrediente_lower = ingrediente.lower()
        
        # Verificar restricciones dietéticas
        if self.es_vegano():
            ingredientes_animales = ['huevo', 'leche', 'queso', 'mantequilla', 'crema', 'yogur', 'pollo', 'carne', 'pescado']
            if any(animal in ingrediente_lower for animal in ingredientes_animales):
                return False
        
        if self.es_vegetariano():
            ingredientes_carne = ['pollo', 'carne', 'cerdo', 'res', 'ternera', 'cordero', 'pavo']
            if any(carne in ingrediente_lower for carne in ingredientes_carne):
                return False
        
        if self.tiene_restriccion_gluten():
            ingredientes_gluten = ['trigo', 'cebada', 'centeno', 'avena', 'harina', 'pan', 'pasta']
            if any(gluten in ingrediente_lower for gluten in ingredientes_gluten):
                return False
        
        if self.tiene_restriccion_lactosa():
            ingredientes_lactosa = ['leche', 'queso', 'mantequilla', 'crema', 'yogur']
            if any(lactosa in ingrediente_lower for lactosa in ingredientes_lactosa):
                return False
        
        # Verificar alérgenos
        for alergeno in self.alergenos:
            if alergeno.value in ingrediente_lower:
                return False
        
        # Verificar ingredientes evitados
        if ingrediente_lower in [ing.lower() for ing in self.ingredientes_evitados]:
            return False
        
        return True
    
    def obtener_preferencias_texto(self) -> str:
        """Obtiene las preferencias en formato texto para el prompt."""
        preferencias = []
        
        if self.restricciones_dieteticas:
            preferencias.append(f"Restricciones: {', '.join([r.value for r in self.restricciones_dieteticas])}")
        
        if self.alergenos:
            preferencias.append(f"Alérgenos a evitar: {', '.join([a.value for a in self.alergenos])}")
        
        if self.preferencias_culturales:
            preferencias.append(f"Preferencias culturales: {', '.join([p.value for p in self.preferencias_culturales])}")
        
        if self.nivel_picante != 2:
            preferencias.append(f"Nivel de picante: {self.nivel_picante}/5")
        
        if self.objetivo_calorico:
            preferencias.append(f"Objetivo calórico: {self.objetivo_calorico} kcal")
        
        return "; ".join(preferencias) if preferencias else "Sin preferencias específicas"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el perfil a diccionario."""
        return {
            "nombre": self.nombre,
            "nivel_culinario": self.nivel_culinario.value,
            "tiempo_disponible": self.tiempo_disponible,
            "num_personas": self.num_personas,
            "restricciones_dieteticas": [r.value for r in self.restricciones_dieteticas],
            "alergenos": [a.value for a in self.alergenos],
            "preferencias_culturales": [p.value for p in self.preferencias_culturales],
            "nivel_picante": self.nivel_picante,
            "preferencia_salado": self.preferencia_salado,
            "preferencia_dulce": self.preferencia_dulce,
            "preferencia_amargo": self.preferencia_amargo,
            "preferencia_acido": self.preferencia_acido,
            "objetivo_calorico": self.objetivo_calorico,
            "preferencia_proteinas": self.preferencia_proteinas,
            "preferencia_fibra": self.preferencia_fibra,
            "evitar_grasas": self.evitar_grasas,
            "max_recetas_por_sesion": self.max_recetas_por_sesion,
            "mostrar_informacion_nutricional": self.mostrar_informacion_nutricional,
            "mostrar_consejos_chef": self.mostrar_consejos_chef,
            "mostrar_variaciones": self.mostrar_variaciones,
            "recetas_favoritas": self.recetas_favoritas,
            "ingredientes_favoritos": self.ingredientes_favoritos,
            "ingredientes_evitados": self.ingredientes_evitados,
            "tecnicas_preferidas": self.tecnicas_preferidas
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PerfilUsuario':
        """Crea un perfil desde un diccionario."""
        # Convertir strings a enums
        if 'nivel_culinario' in data and isinstance(data['nivel_culinario'], str):
            data['nivel_culinario'] = NivelCulinario(data['nivel_culinario'])
        
        if 'restricciones_dieteticas' in data:
            data['restricciones_dieteticas'] = [
                RestriccionDietetica(r) for r in data['restricciones_dieteticas']
            ]
        
        if 'alergenos' in data:
            data['alergenos'] = [Alergeno(a) for a in data['alergenos']]
        
        if 'preferencias_culturales' in data:
            data['preferencias_culturales'] = [
                PreferenciaCultural(p) for p in data['preferencias_culturales']
            ]
        
        return cls(**data)
    
    @classmethod
    def crear_perfil_default(cls) -> 'PerfilUsuario':
        """Crea un perfil con configuraciones por defecto."""
        return cls(
            nivel_culinario=NivelCulinario.INTERMEDIO,
            tiempo_disponible=30,
            num_personas=2,
            restricciones_dieteticas=[],
            alergenos=[],
            preferencias_culturales=[PreferenciaCultural.MEDITERRANEA, PreferenciaCultural.INTERNACIONAL]
        )
