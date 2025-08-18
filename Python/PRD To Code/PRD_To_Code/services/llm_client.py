"""
Cliente para la API de LLM (OpenAI).
"""
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
try:
    from openai import OpenAI
except ImportError:
    # Fallback para versiones anteriores de openai
    import openai
    OpenAI = openai
try:
    from openai.types.chat import ChatCompletion
except ImportError:
    # Fallback para versiones anteriores de openai
    ChatCompletion = None

from config.settings import settings
from models.recipe import ColeccionRecetas, Receta, MetadataRecetas
from models.ingredient import ListaIngredientes

# Configurar logging
logger = logging.getLogger(__name__)

class LLMClient:
    """Cliente para interactuar con la API de OpenAI."""
    
    def __init__(self):
        """Inicializa el cliente LLM."""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY es requerida para usar LLMClient")
        
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        logger.info(f"Cliente LLM inicializado con modelo: {self.model}")
    
    def generate_recipes(
        self,
        ingredientes_detectados: ListaIngredientes,
        ingredientes_basicos: List[str],
        restricciones_dieteticas: List[str],
        tiempo_disponible: int,
        nivel_experiencia: str,
        num_personas: int = 2
    ) -> ColeccionRecetas:
        """
        Genera recetas usando el LLM.
        
        Args:
            ingredientes_detectados: Lista de ingredientes detectados
            ingredientes_basicos: Lista de ingredientes básicos disponibles
            restricciones_dieteticas: Restricciones dietéticas del usuario
            tiempo_disponible: Tiempo disponible en minutos
            nivel_experiencia: Nivel culinario del usuario
            num_personas: Número de personas para las que cocinar
            
        Returns:
            Colección de recetas generadas
        """
        try:
            # Generar prompt
            from config.prompts import PromptTemplates
            prompt = PromptTemplates.get_main_recipe_prompt(
                ingredientes_detectados=ingredientes_detectados.ingredientes,
                ingredientes_basicos=ingredientes_basicos,
                restricciones_dieteticas=restricciones_dieteticas,
                tiempo_disponible=tiempo_disponible,
                nivel_experiencia=nivel_experiencia,
                num_personas=num_personas
            )
            
            # Llamar a la API
            response = self._call_openai_api(prompt)
            
            # Procesar respuesta
            return self._parse_recipe_response(response, ingredientes_detectados)
            
        except Exception as e:
            logger.error(f"Error al generar recetas: {e}")
            return self._create_error_response(str(e))
    
    def generate_quick_recipes(
        self,
        ingredientes_detectados: List[str],
        tiempo_maximo: int = 15
    ) -> Dict[str, Any]:
        """
        Genera recetas rápidas.
        
        Args:
            ingredientes_detectados: Lista de ingredientes detectados
            tiempo_maximo: Tiempo máximo en minutos
            
        Returns:
            Diccionario con recetas rápidas
        """
        try:
            from config.prompts import PromptTemplates
            prompt = PromptTemplates.get_quick_recipe_prompt(
                ingredientes_detectados=ingredientes_detectados,
                tiempo_maximo=tiempo_maximo
            )
            
            response = self._call_openai_api(prompt)
            return self._parse_quick_recipe_response(response)
            
        except Exception as e:
            logger.error(f"Error al generar recetas rápidas: {e}")
            return {"error": str(e)}
    
    def generate_gourmet_recipes(
        self,
        ingredientes_detectados: List[str],
        nivel_experiencia: str = "avanzado"
    ) -> Dict[str, Any]:
        """
        Genera recetas gourmet.
        
        Args:
            ingredientes_detectados: Lista de ingredientes detectados
            nivel_experiencia: Nivel de experiencia del usuario
            
        Returns:
            Diccionario con recetas gourmet
        """
        try:
            from config.prompts import PromptTemplates
            prompt = PromptTemplates.get_gourmet_recipe_prompt(
                ingredientes_detectados=ingredientes_detectados,
                nivel_experiencia=nivel_experiencia
            )
            
            response = self._call_openai_api(prompt)
            return self._parse_gourmet_recipe_response(response)
            
        except Exception as e:
            logger.error(f"Error al generar recetas gourmet: {e}")
            return {"error": str(e)}
    
    def generate_healthy_recipes(
        self,
        ingredientes_detectados: List[str],
        restricciones: List[str]
    ) -> Dict[str, Any]:
        """
        Genera recetas saludables.
        
        Args:
            ingredientes_detectados: Lista de ingredientes detectados
            restricciones: Restricciones dietéticas
            
        Returns:
            Diccionario con recetas saludables
        """
        try:
            from config.prompts import PromptTemplates
            prompt = PromptTemplates.get_healthy_recipe_prompt(
                ingredientes_detectados=ingredientes_detectados,
                restricciones=restricciones
            )
            
            response = self._call_openai_api(prompt)
            return self._parse_healthy_recipe_response(response)
            
        except Exception as e:
            logger.error(f"Error al generar recetas saludables: {e}")
            return {"error": str(e)}
    
    def _call_openai_api(self, prompt: str) -> str:
        """
        Realiza la llamada a la API de OpenAI.
        
        Args:
            prompt: Prompt a enviar
            
        Returns:
            Respuesta de la API
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un chef experto y nutricionista con 15 años de experiencia internacional. Tu especialidad es crear recetas deliciosas y saludables optimizando ingredientes disponibles."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=4000,
                temperature=0.7,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error en llamada a OpenAI API: {e}")
            raise
    
    def _parse_recipe_response(self, response_text: str, ingredientes_detectados: ListaIngredientes) -> ColeccionRecetas:
        """
        Parsea la respuesta del LLM para extraer recetas.
        
        Args:
            response_text: Respuesta del LLM
            ingredientes_detectados: Lista de ingredientes detectados
            
        Returns:
            Colección de recetas
        """
        try:
            # Extraer JSON de la respuesta
            json_data = self._extract_json_from_response(response_text)
            if not json_data:
                return self._create_error_response("No se pudo extraer JSON de la respuesta")
            
            # Validar estructura básica
            if 'recetas' not in json_data or 'metadata' not in json_data:
                return self._create_error_response("Estructura de respuesta inválida")
            
            # Procesar metadata
            metadata = self._create_metadata(json_data['metadata'], ingredientes_detectados)
            
            # Procesar recetas
            recetas = []
            for i, receta_data in enumerate(json_data['recetas']):
                try:
                    receta = self._create_recipe_from_data(receta_data, i + 1)
                    recetas.append(receta)
                except Exception as e:
                    logger.warning(f"Error al procesar receta {i + 1}: {e}")
                    continue
            
            if not recetas:
                return self._create_error_response("No se pudieron procesar recetas válidas")
            
            return ColeccionRecetas(metadata=metadata, recetas=recetas)
            
        except Exception as e:
            logger.error(f"Error al parsear respuesta de recetas: {e}")
            return self._create_error_response(f"Error al parsear respuesta: {str(e)}")
    
    def _parse_quick_recipe_response(self, response_text: str) -> Dict[str, Any]:
        """Parsea respuesta de recetas rápidas."""
        try:
            json_data = self._extract_json_from_response(response_text)
            return json_data if json_data else {"error": "No se pudo extraer JSON"}
        except Exception as e:
            return {"error": str(e)}
    
    def _parse_gourmet_recipe_response(self, response_text: str) -> Dict[str, Any]:
        """Parsea respuesta de recetas gourmet."""
        try:
            json_data = self._extract_json_from_response(response_text)
            return json_data if json_data else {"error": "No se pudo extraer JSON"}
        except Exception as e:
            return {"error": str(e)}
    
    def _parse_healthy_recipe_response(self, response_text: str) -> Dict[str, Any]:
        """Parsea respuesta de recetas saludables."""
        try:
            json_data = self._extract_json_from_response(response_text)
            return json_data if json_data else {"error": "No se pudo extraer JSON"}
        except Exception as e:
            return {"error": str(e)}
    
    def _extract_json_from_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """
        Extrae JSON de la respuesta del LLM.
        
        Args:
            response_text: Respuesta del LLM
            
        Returns:
            Datos JSON extraídos
        """
        try:
            # Buscar JSON en la respuesta
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                logger.error("No se encontró JSON en la respuesta")
                return None
            
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
            
        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear JSON: {e}")
            return None
        except Exception as e:
            logger.error(f"Error al extraer JSON: {e}")
            return None
    
    def _create_metadata(self, metadata_data: Dict[str, Any], ingredientes_detectados: ListaIngredientes) -> MetadataRecetas:
        """Crea objeto MetadataRecetas desde datos."""
        return MetadataRecetas(
            total_recetas=metadata_data.get('total_recetas', 0),
            ingredientes_utilizados=metadata_data.get('ingredientes_utilizados', []),
            tiempo_generacion=metadata_data.get('tiempo_generacion', datetime.now().isoformat()),
            temporada=metadata_data.get('temporada', 'general'),
            version=metadata_data.get('version', '1.0')
        )
    
    def _create_recipe_from_data(self, receta_data: Dict[str, Any], recipe_id: int) -> Receta:
        """Crea objeto Receta desde datos."""
        from models.recipe import (
            Instruccion, InformacionNutricional, IngredienteReceta,
            NivelDificultad, TipoCocina
        )
        
        # Procesar ingredientes
        ingredientes = []
        for ing_data in receta_data.get('ingredientes', []):
            ingrediente = IngredienteReceta(
                nombre=ing_data.get('nombre', ''),
                cantidad=ing_data.get('cantidad', ''),
                unidad=ing_data.get('unidad', ''),
                detectado=ing_data.get('detectado', True),
                esencial=ing_data.get('esencial', True),
                opcional=ing_data.get('opcional', False),
                sustitucion=ing_data.get('sustitucion')
            )
            ingredientes.append(ingrediente)
        
        # Procesar instrucciones
        instrucciones = []
        for inst_data in receta_data.get('instrucciones', []):
            instruccion = Instruccion(
                paso=inst_data.get('paso', 1),
                accion=inst_data.get('accion', ''),
                tiempo_estimado=inst_data.get('tiempo_estimado'),
                tip=inst_data.get('tip')
            )
            instrucciones.append(instruccion)
        
        # Procesar información nutricional
        info_nut = receta_data.get('informacion_nutricional', {})
        informacion_nutricional = InformacionNutricional(
            calorias_por_porcion=info_nut.get('calorias_por_porcion'),
            proteinas_g=info_nut.get('proteinas_g'),
            carbohidratos_g=info_nut.get('carbohidratos_g'),
            grasas_g=info_nut.get('grasas_g'),
            fibra_g=info_nut.get('fibra_g'),
            sodio_mg=info_nut.get('sodio_mg'),
            azucares_g=info_nut.get('azucares_g')
        )
        
        # Determinar nivel de dificultad
        nivel_dificultad_str = receta_data.get('nivel_dificultad', 'intermedio')
        try:
            nivel_dificultad = NivelDificultad(nivel_dificultad_str)
        except ValueError:
            nivel_dificultad = NivelDificultad.INTERMEDIO
        
        # Determinar tipo de cocina
        tipo_cocina_str = receta_data.get('tipo_cocina', 'internacional')
        try:
            tipo_cocina = TipoCocina(tipo_cocina_str)
        except ValueError:
            tipo_cocina = TipoCocina.INTERNACIONAL
        
        return Receta(
            id=recipe_id,
            nombre=receta_data.get('nombre', ''),
            descripcion_corta=receta_data.get('descripcion_corta', ''),
            tiempo_preparacion_min=receta_data.get('tiempo_preparacion_min', 0),
            tiempo_coccion_min=receta_data.get('tiempo_coccion_min', 0),
            tiempo_total_min=receta_data.get('tiempo_total_min', 0),
            dificultad_estrellas=receta_data.get('dificultad_estrellas', 3),
            porciones=receta_data.get('porciones', 2),
            tipo_cocina=tipo_cocina,
            ingredientes=ingredientes,
            instrucciones=instrucciones,
            informacion_nutricional=informacion_nutricional,
            tags=receta_data.get('tags', []),
            nivel_dificultad=nivel_dificultad,
            consejos_chef=receta_data.get('consejos_chef', []),
            variaciones=receta_data.get('variaciones', []),
            maridaje=receta_data.get('maridaje'),
            conservacion=receta_data.get('conservacion'),
            presentacion=receta_data.get('presentacion')
        )
    
    def _create_error_response(self, error_message: str) -> ColeccionRecetas:
        """Crea una respuesta de error."""
        metadata = MetadataRecetas(
            total_recetas=0,
            ingredientes_utilizados=[],
            tiempo_generacion=datetime.now().isoformat(),
            temporada='general',
            version='1.0'
        )
        
        return ColeccionRecetas(
            metadata=metadata,
            recetas=[],
            error=error_message
        )
    
    def validate_recipe_data(self, receta_data: Dict[str, Any]) -> bool:
        """
        Valida que los datos de una receta sean correctos.
        
        Args:
            receta_data: Datos de la receta
            
        Returns:
            True si los datos son válidos
        """
        required_fields = ['nombre', 'tiempo_preparacion_min', 'tiempo_coccion_min', 'ingredientes', 'instrucciones']
        
        for field in required_fields:
            if field not in receta_data:
                logger.error(f"Campo requerido faltante: {field}")
                return False
        
        if not receta_data['ingredientes']:
            logger.error("La receta debe tener al menos un ingrediente")
            return False
        
        if not receta_data['instrucciones']:
            logger.error("La receta debe tener al menos una instrucción")
            return False
        
        return True
