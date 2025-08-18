"""
Plantillas de prompts para la generación de recetas con LLM.
Basado en las especificaciones del PRD v1.0
"""

from typing import List, Dict, Any
from config.settings import settings

class PromptTemplates:
    """Plantillas de prompts para diferentes escenarios."""
    
    @staticmethod
    def get_main_recipe_prompt(
        ingredientes_detectados: List[Dict[str, Any]],
        ingredientes_basicos: List[str],
        restricciones_dieteticas: List[str],
        tiempo_disponible: int,
        nivel_experiencia: str,
        num_personas: int = 2
    ) -> str:
        """
        Genera el prompt principal para la generación de recetas.
        
        Args:
            ingredientes_detectados: Lista de ingredientes identificados
            ingredientes_basicos: Lista de ingredientes básicos disponibles
            restricciones_dieteticas: Restricciones dietéticas del usuario
            tiempo_disponible: Tiempo disponible en minutos
            nivel_experiencia: Nivel culinario del usuario
            num_personas: Número de personas para las que cocinar
            
        Returns:
            Prompt formateado para el LLM
        """
        
        # Formatear ingredientes detectados
        ingredientes_formateados = []
        for ingrediente in ingredientes_detectados:
            confianza = ingrediente.get('confianza', 0)
            if confianza >= settings.MIN_CONFIDENCE_THRESHOLD:
                ingredientes_formateados.append(
                    f"- {ingrediente['nombre']} (confianza: {confianza:.1%})"
                )
        
        ingredientes_texto = "\n".join(ingredientes_formateados) if ingredientes_formateados else "No se detectaron ingredientes claros"
        
        # Formatear restricciones dietéticas
        restricciones_texto = ", ".join(restricciones_dieteticas) if restricciones_dieteticas else "Ninguna"
        
        # Obtener temporada actual
        temporada_actual = settings.get_temporada_actual()
        
        return f"""
Actúa como un chef profesional con especialización en cocina internacional y nutrición. 
Tu misión es transformar ingredientes disponibles en recetas extraordinarias.

=== ANÁLISIS DE INGREDIENTES ===
Ingredientes principales detectados:
{ingredientes_texto}

Ingredientes básicos disponibles: {", ".join(ingredientes_basicos)}
Restricciones dietéticas activas: {restricciones_texto}

=== PERFIL DEL USUARIO ===
Nivel culinario: {nivel_experiencia}
Tiempo disponible: {tiempo_disponible} minutos
Número de comensales: {num_personas}
Temporada actual: {temporada_actual}

=== INSTRUCCIONES ESPECÍFICAS ===
1. Genera EXACTAMENTE 5 recetas únicas y deliciosas
2. Cada receta debe usar mínimo 3 de los ingredientes detectados
3. Ordena por dificultad: principiante a intermedio
4. Incluye al menos 1 receta que se complete en <20 minutos
5. Balancea tipos de cocción: crudo, salteado, horneado, hervido
6. Prioriza ingredientes de temporada: {temporada_actual}
7. Adapta porciones para {num_personas} personas

=== FORMATO DE RESPUESTA REQUERIDO ===
Responde únicamente en JSON válido siguiendo esta estructura exacta:

{{
  "metadata": {{
    "total_recetas": 5,
    "ingredientes_utilizados": ["lista", "de", "ingredientes"],
    "tiempo_generacion": "timestamp",
    "temporada": "{temporada_actual}"
  }},
  "recetas": [
    {{
      "id": 1,
      "nombre": "Título Atractivo de la Receta",
      "descripcion_corta": "Descripción en una línea que despierte apetito",
      "tiempo_preparacion_min": 15,
      "tiempo_coccion_min": 20,
      "tiempo_total_min": 35,
      "dificultad_estrellas": 2,
      "porciones": {num_personas},
      "tipo_cocina": "italiana",
      "ingredientes": [
        {{
          "nombre": "Ingrediente 1",
          "cantidad": "200g",
          "unidad": "gramos",
          "detectado": true,
          "esencial": true
        }}
      ],
      "instrucciones": [
        {{
          "paso": 1,
          "accion": "Descripción detallada del primer paso",
          "tiempo_estimado": "5 min",
          "tip": "Consejo profesional opcional"
        }}
      ],
      "informacion_nutricional": {{
        "calorias_por_porcion": 350,
        "proteinas_g": 25,
        "carbohidratos_g": 45,
        "grasas_g": 12
      }},
      "tags": ["rapido", "saludable", "familiar"],
      "nivel_dificultad": "principiante",
      "consejos_chef": [
        "Tip 1 para mejorar el sabor",
        "Tip 2 para la presentación"
      ],
      "variaciones": [
        "Versión vegetariana: sustituir X por Y",
        "Versión picante: agregar Z"
      ]
    }}
  ]
}}

=== VALIDACIONES OBLIGATORIAS ===
- Verificar que todos los ingredientes principales estén disponibles
- Confirmar que las cantidades sean realistas para las porciones
- Asegurar que las instrucciones sean ejecutables paso a paso
- Validar que los tiempos de cocción sean precisos
- Comprobar que las técnicas culinarias coincidan con el nivel de dificultad

=== CONSIDERACIONES ESPECIALES ===
- Si faltan ingredientes para una receta completa, sugiérelos como "opcionales" o "para mejorar"
- Prioriza técnicas que realcen sabores naturales de los ingredientes
- Incluye información sobre conservación de sobras
- Adapta las porciones si hay ingredientes en cantidad limitada
- Sugiere acompañamientos que complementen nutritivamente
- Considera la temporada {temporada_actual} para ingredientes frescos

Genera las recetas ahora manteniendo el más alto estándar culinario y nutricional.
"""

    @staticmethod
    def get_ingredient_detection_prompt() -> str:
        """
        Prompt para el reconocimiento de ingredientes en imágenes.
        
        Returns:
            Prompt para análisis de imágenes
        """
        return """
Analiza esta imagen y identifica todos los ingredientes alimentarios visibles.

INSTRUCCIONES:
1. Identifica solo ingredientes comestibles y alimentos
2. Proporciona el nombre en español
3. Especifica la cantidad aproximada si es visible
4. Indica el estado (fresco, maduro, cocido, etc.) si es relevante
5. Ignora objetos no alimentarios

FORMATO DE RESPUESTA:
Responde únicamente en JSON válido:

{
  "ingredientes": [
    {
      "nombre": "nombre del ingrediente",
      "cantidad": "cantidad aproximada",
      "unidad": "unidad de medida",
      "estado": "fresco/maduro/cocido/etc",
      "confianza": 0.95
    }
  ],
  "total_ingredientes": 5,
  "calidad_imagen": "buena/regular/mala"
}

Si no puedes identificar ingredientes claros, responde:
{
  "ingredientes": [],
  "total_ingredientes": 0,
  "calidad_imagen": "mala",
  "error": "No se pudieron identificar ingredientes claros"
}
"""

    @staticmethod
    def get_quick_recipe_prompt(
        ingredientes_detectados: List[str],
        tiempo_maximo: int = 15
    ) -> str:
        """
        Prompt para recetas rápidas (menos de 15 minutos).
        
        Args:
            ingredientes_detectados: Lista de ingredientes
            tiempo_maximo: Tiempo máximo en minutos
            
        Returns:
            Prompt para recetas rápidas
        """
        return f"""
Eres un chef experto en recetas rápidas y eficientes.
Genera 3 recetas que se puedan preparar en menos de {tiempo_maximo} minutos.

INGREDIENTES DISPONIBLES: {", ".join(ingredientes_detectados)}
TIEMPO MÁXIMO: {tiempo_maximo} minutos

REQUISITOS:
- Máximo {tiempo_maximo} minutos de preparación
- Usar al menos 2 ingredientes detectados por receta
- Técnicas simples y rápidas
- Instrucciones paso a paso claras

FORMATO JSON requerido:
{{
  "recetas_rapidas": [
    {{
      "nombre": "Nombre de la receta",
      "tiempo_total": {tiempo_maximo},
      "ingredientes": ["lista"],
      "instrucciones": ["paso 1", "paso 2"],
      "dificultad": "muy fácil"
    }}
  ]
}}
"""

    @staticmethod
    def get_gourmet_recipe_prompt(
        ingredientes_detectados: List[str],
        nivel_experiencia: str = "avanzado"
    ) -> str:
        """
        Prompt para recetas gourmet para usuarios avanzados.
        
        Args:
            ingredientes_detectados: Lista de ingredientes
            nivel_experiencia: Nivel del usuario
            
        Returns:
            Prompt para recetas gourmet
        """
        return f"""
Eres un chef de alta cocina con experiencia en restaurantes Michelin.
Genera 3 recetas gourmet sofisticadas para un chef {nivel_experiencia}.

INGREDIENTES DISPONIBLES: {", ".join(ingredientes_detectados)}
NIVEL: {nivel_experiencia}

CARACTERÍSTICAS REQUERIDAS:
- Técnicas culinarias avanzadas
- Presentación elegante
- Combinaciones de sabores sofisticadas
- Instrucciones detalladas de técnica
- Tips de chef profesional

FORMATO JSON requerido:
{{
  "recetas_gourmet": [
    {{
      "nombre": "Nombre Gourmet",
      "descripcion": "Descripción elegante",
      "tiempo_preparacion": 45,
      "tiempo_coccion": 30,
      "dificultad": "avanzado",
      "ingredientes": ["lista detallada"],
      "instrucciones": ["pasos detallados"],
      "tecnicas_culinarias": ["técnicas usadas"],
      "presentacion": "instrucciones de presentación",
      "maridaje": "sugerencias de bebidas"
    }}
  ]
}}
"""

    @staticmethod
    def get_healthy_recipe_prompt(
        ingredientes_detectados: List[str],
        restricciones: List[str]
    ) -> str:
        """
        Prompt para recetas saludables.
        
        Args:
            ingredientes_detectados: Lista de ingredientes
            restricciones: Restricciones dietéticas
            
        Returns:
            Prompt para recetas saludables
        """
        return f"""
Eres un nutricionista y chef especializado en cocina saludable.
Genera 3 recetas nutritivas y balanceadas.

INGREDIENTES: {", ".join(ingredientes_detectados)}
RESTRICCIONES: {", ".join(restricciones) if restricciones else "Ninguna"}

ENFOQUE:
- Balance nutricional óptimo
- Ingredientes naturales y frescos
- Técnicas de cocción saludables
- Información nutricional detallada
- Alternativas saludables

FORMATO JSON requerido:
{{
  "recetas_saludables": [
    {{
      "nombre": "Nombre Saludable",
      "calorias_por_porcion": 300,
      "proteinas": "25g",
      "carbohidratos": "35g",
      "grasas": "8g",
      "fibra": "6g",
      "ingredientes": ["lista"],
      "instrucciones": ["pasos"],
      "beneficios_nutricionales": ["beneficios"],
      "alternativas_saludables": ["sustituciones"]
    }}
  ]
}}
"""
