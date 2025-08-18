"""
CulinaryVision AI - Aplicación principal
Generador de recetas con reconocimiento visual de ingredientes
"""
import sys
import logging
import argparse
from typing import List, Optional
from pathlib import Path

from config.settings import settings
from models.user_profile import PerfilUsuario
from services.recipe_generator import RecipeGenerator
from utils.validators import Validators
from utils.helpers import Helpers

# Configurar logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class CulinaryVisionAI:
    """Clase principal de la aplicación CulinaryVision AI."""
    
    def __init__(self):
        """Inicializa la aplicación."""
        try:
            # Validar configuración
            self._validate_configuration()
            
            # Inicializar generador de recetas
            self.recipe_generator = RecipeGenerator()
            
            logger.info("CulinaryVision AI inicializado correctamente")
            
        except Exception as e:
            logger.error(f"Error al inicializar la aplicación: {e}")
            raise
    
    def _validate_configuration(self):
        """Valida la configuración de la aplicación."""
        logger.info("Validando configuración...")
        
        # Validar APIs
        api_validation = Validators.validate_api_configuration()
        if not api_validation['valid']:
            raise ValueError(f"Configuración de APIs inválida: {api_validation['errors']}")
        
        if api_validation['warnings']:
            logger.warning(f"Advertencias de configuración: {api_validation['warnings']}")
        
        logger.info(f"Servicios disponibles: {api_validation['available_services']}")
    
    def generate_recipes_from_images(
        self,
        image_paths: List[str],
        user_profile: Optional[PerfilUsuario] = None,
        max_recipes: Optional[int] = None,
        use_openai_vision: bool = True,
        save_to_file: bool = False,
        output_format: str = "json"
    ) -> dict:
        """
        Genera recetas a partir de imágenes de ingredientes.
        
        Args:
            image_paths: Lista de rutas de imágenes
            user_profile: Perfil del usuario (opcional)
            max_recipes: Número máximo de recetas a generar
            use_openai_vision: Si usar OpenAI Vision para detección
            save_to_file: Si guardar resultados en archivo
            output_format: Formato de salida (json, markdown)
            
        Returns:
            Diccionario con resultados
        """
        try:
            logger.info(f"Iniciando generación de recetas para {len(image_paths)} imágenes")
            
            # Validar imágenes
            image_validation = Validators.validate_image_list(image_paths)
            if not image_validation['valid']:
                return {
                    'success': False,
                    'error': 'Validación de imágenes falló',
                    'details': image_validation['errors']
                }
            
            # Usar perfil por defecto si no se proporciona
            if user_profile is None:
                user_profile = PerfilUsuario.crear_perfil_default()
                logger.info("Usando perfil de usuario por defecto")
            
            # Validar sesión
            session_validation = self.recipe_generator.validate_session(image_paths, user_profile)
            if not session_validation['valid']:
                return {
                    'success': False,
                    'error': 'Validación de sesión falló',
                    'details': session_validation['errors']
                }
            
            # Generar recetas
            recetas = self.recipe_generator.generate_recipes_from_images(
                image_paths=image_validation['valid_images'],
                user_profile=user_profile,
                max_recipes=max_recipes,
                use_openai_vision=use_openai_vision
            )
            
            # Verificar si hubo error
            if hasattr(recetas, 'error') and recetas.error:
                return {
                    'success': False,
                    'error': recetas.error
                }
            
            # Preparar resultado
            result = {
                'success': True,
                'metadata': recetas.metadata.dict(),
                'recetas': [receta.to_dict() for receta in recetas.recetas],
                'total_recetas': len(recetas.recetas),
                'ingredientes_detectados': [ing.nombre for ing in recetas.metadata.ingredientes_utilizados]
            }
            
            # Guardar en archivo si se solicita
            if save_to_file:
                self._save_results(result, output_format)
            
            logger.info(f"Generación completada: {len(recetas.recetas)} recetas generadas")
            return result
            
        except Exception as e:
            logger.error(f"Error en generación de recetas: {e}")
            return {
                'success': False,
                'error': f"Error interno: {str(e)}"
            }
    
    def _save_results(self, result: dict, output_format: str):
        """Guarda los resultados en archivo."""
        try:
            # Crear directorio de salida
            output_dir = "output"
            Helpers.create_output_directory(output_dir)
            
            # Generar nombre de archivo
            session_id = Helpers.generate_session_id()
            
            if output_format.lower() == "json":
                filename = f"{output_dir}/recetas_{session_id}.json"
                Helpers.save_recipes_to_file(result, filename)
                logger.info(f"Resultados guardados en {filename}")
            
            elif output_format.lower() == "markdown":
                # Crear archivo Markdown para cada receta
                for i, receta in enumerate(result['recetas']):
                    filename = f"{output_dir}/receta_{i+1}_{session_id}.md"
                    markdown_content = Helpers.create_recipe_markdown(receta)
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)
                    
                    logger.info(f"Receta {i+1} guardada en {filename}")
            
            else:
                logger.warning(f"Formato de salida no soportado: {output_format}")
                
        except Exception as e:
            logger.error(f"Error al guardar resultados: {e}")
    
    def generate_quick_recipes(self, ingredientes_detectados: List[str], tiempo_maximo: int = 15) -> dict:
        """Genera recetas rápidas."""
        try:
            result = self.recipe_generator.generate_quick_recipes(ingredientes_detectados, tiempo_maximo)
            return {
                'success': 'error' not in result,
                'data': result
            }
        except Exception as e:
            logger.error(f"Error al generar recetas rápidas: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_gourmet_recipes(self, ingredientes_detectados: List[str], nivel_experiencia: str = "avanzado") -> dict:
        """Genera recetas gourmet."""
        try:
            result = self.recipe_generator.generate_gourmet_recipes(ingredientes_detectados, nivel_experiencia)
            return {
                'success': 'error' not in result,
                'data': result
            }
        except Exception as e:
            logger.error(f"Error al generar recetas gourmet: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_healthy_recipes(self, ingredientes_detectados: List[str], restricciones: List[str]) -> dict:
        """Genera recetas saludables."""
        try:
            result = self.recipe_generator.generate_healthy_recipes(ingredientes_detectados, restricciones)
            return {
                'success': 'error' not in result,
                'data': result
            }
        except Exception as e:
            logger.error(f"Error al generar recetas saludables: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_ingredient_suggestions(self, ingredientes_detectados: List[str]) -> List[str]:
        """Obtiene sugerencias de ingredientes complementarios."""
        return self.recipe_generator.get_ingredient_suggestions(ingredientes_detectados)
    
    def validate_images(self, image_paths: List[str]) -> dict:
        """Valida una lista de imágenes."""
        return Validators.validate_image_list(image_paths)
    
    def get_system_info(self) -> dict:
        """Obtiene información del sistema."""
        return {
            'version': '1.0.0',
            'config': {
                'max_images_per_session': settings.MAX_IMAGES_PER_SESSION,
                'max_response_time': settings.MAX_RESPONSE_TIME,
                'min_confidence_threshold': settings.MIN_CONFIDENCE_THRESHOLD,
                'supported_formats': settings.SUPPORTED_IMAGE_FORMATS
            },
            'apis': Validators.validate_api_configuration()
        }

def main():
    """Función principal para uso desde línea de comandos."""
    parser = argparse.ArgumentParser(
        description="CulinaryVision AI - Generador de recetas con reconocimiento visual"
    )
    
    parser.add_argument(
        'images',
        nargs='+',
        help='Rutas de las imágenes de ingredientes'
    )
    
    parser.add_argument(
        '--profile',
        type=str,
        help='Archivo JSON con perfil de usuario'
    )
    
    parser.add_argument(
        '--max-recipes',
        type=int,
        default=5,
        help='Número máximo de recetas a generar (default: 5)'
    )
    
    parser.add_argument(
        '--use-google-vision',
        action='store_true',
        help='Usar Google Cloud Vision en lugar de OpenAI Vision'
    )
    
    parser.add_argument(
        '--save',
        action='store_true',
        help='Guardar resultados en archivo'
    )
    
    parser.add_argument(
        '--format',
        choices=['json', 'markdown'],
        default='json',
        help='Formato de salida (default: json)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Mostrar información detallada'
    )
    
    args = parser.parse_args()
    
    # Configurar logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Inicializar aplicación
        app = CulinaryVisionAI()
        
        # Cargar perfil de usuario si se especifica
        user_profile = None
        if args.profile:
            try:
                profile_data = Helpers.load_recipes_from_file(args.profile)
                if profile_data:
                    user_profile = PerfilUsuario.from_dict(profile_data)
                    logger.info("Perfil de usuario cargado")
            except Exception as e:
                logger.warning(f"No se pudo cargar perfil de usuario: {e}")
        
        # Generar recetas
        result = app.generate_recipes_from_images(
            image_paths=args.images,
            user_profile=user_profile,
            max_recipes=args.max_recipes,
            use_openai_vision=not args.use_google_vision,
            save_to_file=args.save,
            output_format=args.format
        )
        
        # Mostrar resultados
        if result['success']:
            print(f"\n✅ Generación exitosa!")
            print(f"📊 Total de recetas: {result['total_recetas']}")
            print(f"🥕 Ingredientes detectados: {', '.join(result['ingredientes_detectados'])}")
            
            if args.verbose:
                print("\n📋 Recetas generadas:")
                for i, receta in enumerate(result['recetas'], 1):
                    summary = Helpers.get_recipe_summary(receta)
                    print(f"  {i}. {summary}")
            
            if args.save:
                print(f"\n💾 Resultados guardados en directorio 'output'")
        
        else:
            print(f"\n❌ Error: {result['error']}")
            if 'details' in result:
                print(f"Detalles: {result['details']}")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⏹️  Operación cancelada por el usuario")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        if args.verbose:
            logger.exception("Error detallado:")
        sys.exit(1)

if __name__ == "__main__":
    main()
