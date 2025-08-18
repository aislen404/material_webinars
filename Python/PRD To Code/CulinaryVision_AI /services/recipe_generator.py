"""
Servicio principal de generación de recetas.
Orquesta todo el proceso desde detección de ingredientes hasta generación de recetas.
"""
import logging
import time
from typing import List, Optional, Dict, Any
from datetime import datetime

from config.settings import settings
from models.ingredient import ListaIngredientes
from models.recipe import ColeccionRecetas
from models.user_profile import PerfilUsuario
from services.image_processor import ImageProcessor
from services.llm_client import LLMClient

# Configurar logging
logger = logging.getLogger(__name__)

class RecipeGenerator:
    """Generador principal de recetas."""
    
    def __init__(self):
        """Inicializa el generador de recetas."""
        self.image_processor = ImageProcessor()
        self.llm_client = LLMClient()
        logger.info("RecipeGenerator inicializado correctamente")
    
    def generate_recipes_from_images(
        self,
        image_paths: List[str],
        user_profile: Optional[PerfilUsuario] = None,
        max_recipes: Optional[int] = None,
        use_openai_vision: bool = True
    ) -> ColeccionRecetas:
        """
        Genera recetas a partir de imágenes de ingredientes.
        
        Args:
            image_paths: Lista de rutas de imágenes
            user_profile: Perfil del usuario (opcional)
            max_recipes: Número máximo de recetas a generar
            use_openai_vision: Si usar OpenAI Vision para detección
            
        Returns:
            Colección de recetas generadas
        """
        start_time = time.time()
        
        try:
            # Validar entrada
            if not image_paths:
                return self._create_error_response("No se proporcionaron imágenes")
            
            if len(image_paths) > settings.MAX_IMAGES_PER_SESSION:
                return self._create_error_response(
                    f"Máximo {settings.MAX_IMAGES_PER_SESSION} imágenes por sesión"
                )
            
            # Usar perfil por defecto si no se proporciona
            if user_profile is None:
                user_profile = PerfilUsuario.crear_perfil_default()
            
            # Establecer número máximo de recetas
            if max_recipes is None:
                max_recipes = user_profile.max_recetas_por_sesion
            
            logger.info(f"Iniciando generación de recetas para {len(image_paths)} imágenes")
            
            # Paso 1: Detectar ingredientes en todas las imágenes
            ingredientes_detectados = self._detect_ingredients_from_images(
                image_paths, use_openai_vision
            )
            
            if ingredientes_detectados.error:
                return self._create_error_response(ingredientes_detectados.error)
            
            if not ingredientes_detectados.ingredientes:
                return self._create_error_response("No se detectaron ingredientes en las imágenes")
            
            logger.info(f"Detectados {len(ingredientes_detectados.ingredientes)} ingredientes")
            
            # Paso 2: Generar recetas usando LLM
            recetas = self._generate_recipes_with_llm(
                ingredientes_detectados, user_profile, max_recipes
            )
            
            # Paso 3: Validar y procesar resultados
            if recetas.error:
                return recetas
            
            # Paso 4: Filtrar recetas según preferencias del usuario
            recetas_filtradas = self._filter_recipes_by_user_preferences(recetas, user_profile)
            
            # Paso 5: Ordenar recetas
            recetas_ordenadas = self._sort_recipes(recetas_filtradas, user_profile)
            
            # Calcular tiempo total
            total_time = time.time() - start_time
            logger.info(f"Generación completada en {total_time:.2f} segundos")
            
            # Actualizar metadata con tiempo de generación
            recetas_ordenadas.metadata.tiempo_generacion = datetime.now().isoformat()
            
            return recetas_ordenadas
            
        except Exception as e:
            logger.error(f"Error en generación de recetas: {e}")
            return self._create_error_response(f"Error interno: {str(e)}")
    
    def _detect_ingredients_from_images(
        self,
        image_paths: List[str],
        use_openai_vision: bool
    ) -> ListaIngredientes:
        """
        Detecta ingredientes en múltiples imágenes.
        
        Args:
            image_paths: Lista de rutas de imágenes
            use_openai_vision: Si usar OpenAI Vision
            
        Returns:
            Lista combinada de ingredientes detectados
        """
        try:
            # Detectar ingredientes en cada imagen
            results = self.image_processor.detect_ingredients_batch(
                image_paths, use_openai_vision
            )
            
            # Combinar resultados
            combined_ingredients = self.image_processor.merge_ingredient_lists(results)
            
            # Filtrar por confianza mínima
            filtered_ingredients = combined_ingredients.obtener_por_confianza(
                settings.MIN_CONFIDENCE_THRESHOLD
            )
            
            return ListaIngredientes(ingredientes=filtered_ingredients)
            
        except Exception as e:
            logger.error(f"Error en detección de ingredientes: {e}")
            return ListaIngredientes(error=f"Error en detección: {str(e)}")
    
    def _generate_recipes_with_llm(
        self,
        ingredientes_detectados: ListaIngredientes,
        user_profile: PerfilUsuario,
        max_recipes: int
    ) -> ColeccionRecetas:
        """
        Genera recetas usando el LLM.
        
        Args:
            ingredientes_detectados: Lista de ingredientes detectados
            user_profile: Perfil del usuario
            max_recipes: Número máximo de recetas
            
        Returns:
            Colección de recetas generadas
        """
        try:
            # Preparar datos para el LLM
            ingredientes_basicos = settings.INGREDIENTES_BASICOS
            restricciones_dieteticas = [
                r.value for r in user_profile.restricciones_dieteticas
            ]
            
            # Generar recetas
            recetas = self.llm_client.generate_recipes(
                ingredientes_detectados=ingredientes_detectados,
                ingredientes_basicos=ingredientes_basicos,
                restricciones_dieteticas=restricciones_dieteticas,
                tiempo_disponible=user_profile.tiempo_disponible,
                nivel_experiencia=user_profile.nivel_culinario.value,
                num_personas=user_profile.num_personas
            )
            
            # Limitar número de recetas si es necesario
            if len(recetas.recetas) > max_recipes:
                recetas.recetas = recetas.recetas[:max_recipes]
                recetas.metadata.total_recetas = len(recetas.recetas)
            
            return recetas
            
        except Exception as e:
            logger.error(f"Error en generación con LLM: {e}")
            return self._create_error_response(f"Error en generación: {str(e)}")
    
    def _filter_recipes_by_user_preferences(
        self,
        recetas: ColeccionRecetas,
        user_profile: PerfilUsuario
    ) -> ColeccionRecetas:
        """
        Filtra recetas según las preferencias del usuario.
        
        Args:
            recetas: Colección de recetas
            user_profile: Perfil del usuario
            
        Returns:
            Colección filtrada de recetas
        """
        try:
            filtered_recipes = []
            
            for receta in recetas.recetas:
                # Verificar restricciones dietéticas
                if not self._recipe_matches_dietary_restrictions(receta, user_profile):
                    continue
                
                # Verificar alérgenos
                if self._recipe_contains_allergens(receta, user_profile):
                    continue
                
                # Verificar tiempo disponible
                if receta.tiempo_total_min > user_profile.tiempo_disponible:
                    continue
                
                # Verificar nivel de dificultad
                if not self._recipe_matches_skill_level(receta, user_profile):
                    continue
                
                filtered_recipes.append(receta)
            
            # Crear nueva colección con recetas filtradas
            filtered_collection = ColeccionRecetas(
                metadata=recetas.metadata,
                recetas=filtered_recipes
            )
            
            logger.info(f"Filtradas {len(filtered_recipes)} recetas de {len(recetas.recetas)}")
            return filtered_collection
            
        except Exception as e:
            logger.error(f"Error al filtrar recetas: {e}")
            return recetas  # Retornar recetas sin filtrar en caso de error
    
    def _sort_recipes(
        self,
        recetas: ColeccionRecetas,
        user_profile: PerfilUsuario
    ) -> ColeccionRecetas:
        """
        Ordena las recetas según las preferencias del usuario.
        
        Args:
            recetas: Colección de recetas
            user_profile: Perfil del usuario
            
        Returns:
            Colección ordenada de recetas
        """
        try:
            # Ordenar por dificultad primero (más fácil primero)
            recetas_ordenadas = recetas.ordenar_por_dificultad()
            
            # Si el usuario prefiere recetas rápidas, priorizar por tiempo
            if user_profile.tiempo_disponible <= 30:
                recetas_ordenadas = recetas.ordenar_por_tiempo()
            
            # Crear nueva colección con recetas ordenadas
            sorted_collection = ColeccionRecetas(
                metadata=recetas.metadata,
                recetas=recetas_ordenadas
            )
            
            return sorted_collection
            
        except Exception as e:
            logger.error(f"Error al ordenar recetas: {e}")
            return recetas  # Retornar recetas sin ordenar en caso de error
    
    def _recipe_matches_dietary_restrictions(
        self,
        receta: 'Receta',
        user_profile: PerfilUsuario
    ) -> bool:
        """Verifica si una receta cumple con las restricciones dietéticas."""
        # Verificar vegetarianismo
        if user_profile.es_vegetariano() and not receta.es_vegetariana():
            return False
        
        # Verificar veganismo
        if user_profile.es_vegano() and not receta.es_vegana():
            return False
        
        # Verificar restricción de gluten
        if user_profile.tiene_restriccion_gluten():
            ingredientes_gluten = ['trigo', 'cebada', 'centeno', 'avena', 'harina', 'pan', 'pasta']
            for ingrediente in receta.ingredientes:
                if any(gluten in ingrediente.nombre.lower() for gluten in ingredientes_gluten):
                    return False
        
        # Verificar restricción de lactosa
        if user_profile.tiene_restriccion_lactosa():
            ingredientes_lactosa = ['leche', 'queso', 'mantequilla', 'crema', 'yogur']
            for ingrediente in receta.ingredientes:
                if any(lactosa in ingrediente.nombre.lower() for lactosa in ingredientes_lactosa):
                    return False
        
        return True
    
    def _recipe_contains_allergens(
        self,
        receta: 'Receta',
        user_profile: PerfilUsuario
    ) -> bool:
        """Verifica si una receta contiene alérgenos del usuario."""
        for alergeno in user_profile.alergenos:
            for ingrediente in receta.ingredientes:
                if alergeno.value in ingrediente.nombre.lower():
                    return True
        return False
    
    def _recipe_matches_skill_level(
        self,
        receta: 'Receta',
        user_profile: PerfilUsuario
    ) -> bool:
        """Verifica si una receta coincide con el nivel de habilidad del usuario."""
        # Mapeo de niveles de dificultad
        difficulty_mapping = {
            'principiante': 1,
            'intermedio': 2,
            'avanzado': 3,
            'experto': 4
        }
        
        user_level = difficulty_mapping.get(user_profile.nivel_culinario.value, 2)
        recipe_level = difficulty_mapping.get(receta.nivel_dificultad.value, 2)
        
        # Permitir recetas hasta un nivel más avanzado que el usuario
        return recipe_level <= user_level + 1
    
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
            return self.llm_client.generate_quick_recipes(
                ingredientes_detectados=ingredientes_detectados,
                tiempo_maximo=tiempo_maximo
            )
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
            return self.llm_client.generate_gourmet_recipes(
                ingredientes_detectados=ingredientes_detectados,
                nivel_experiencia=nivel_experiencia
            )
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
            return self.llm_client.generate_healthy_recipes(
                ingredientes_detectados=ingredientes_detectados,
                restricciones=restricciones
            )
        except Exception as e:
            logger.error(f"Error al generar recetas saludables: {e}")
            return {"error": str(e)}
    
    def _create_error_response(self, error_message: str) -> ColeccionRecetas:
        """Crea una respuesta de error."""
        from models.recipe import MetadataRecetas
        
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
    
    def get_ingredient_suggestions(self, ingredientes_detectados: List[str]) -> List[str]:
        """
        Sugiere ingredientes adicionales que complementen los detectados.
        
        Args:
            ingredientes_detectados: Lista de ingredientes detectados
            
        Returns:
            Lista de ingredientes sugeridos
        """
        # Mapeo de ingredientes complementarios
        complementos = {
            'tomate': ['cebolla', 'ajo', 'albahaca', 'mozzarella'],
            'pollo': ['cebolla', 'ajo', 'limón', 'hierbas'],
            'pasta': ['tomate', 'queso', 'albahaca', 'aceite de oliva'],
            'arroz': ['cebolla', 'ajo', 'zanahoria', 'huevo'],
            'huevo': ['cebolla', 'queso', 'tomate', 'especias'],
            'queso': ['tomate', 'albahaca', 'pan', 'aceite de oliva'],
            'cebolla': ['ajo', 'tomate', 'especias', 'aceite de oliva'],
            'ajo': ['cebolla', 'tomate', 'especias', 'aceite de oliva']
        }
        
        sugerencias = []
        for ingrediente in ingredientes_detectados:
            if ingrediente.lower() in complementos:
                sugerencias.extend(complementos[ingrediente.lower()])
        
        # Eliminar duplicados y ingredientes ya detectados
        sugerencias = list(set(sugerencias))
        sugerencias = [s for s in sugerencias if s not in ingredientes_detectados]
        
        return sugerencias[:5]  # Limitar a 5 sugerencias
    
    def validate_session(self, image_paths: List[str], user_profile: PerfilUsuario) -> Dict[str, Any]:
        """
        Valida una sesión de generación de recetas.
        
        Args:
            image_paths: Lista de rutas de imágenes
            user_profile: Perfil del usuario
            
        Returns:
            Diccionario con resultados de validación
        """
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'ingredients_detected': 0,
            'estimated_time': 0
        }
        
        try:
            # Validar imágenes
            for image_path in image_paths:
                if not self.image_processor.validate_image(image_path):
                    validation_result['valid'] = False
                    validation_result['errors'].append(f"Imagen no válida: {image_path}")
            
            # Validar perfil de usuario
            if user_profile.tiempo_disponible < 5:
                validation_result['warnings'].append("Tiempo disponible muy bajo")
            
            if user_profile.num_personas > 10:
                validation_result['valid'] = False
                validation_result['errors'].append("Máximo 10 personas por sesión")
            
            # Estimar tiempo de procesamiento
            validation_result['estimated_time'] = len(image_paths) * 5 + 15  # 5s por imagen + 15s para LLM
            
            return validation_result
            
        except Exception as e:
            validation_result['valid'] = False
            validation_result['errors'].append(f"Error en validación: {str(e)}")
            return validation_result
