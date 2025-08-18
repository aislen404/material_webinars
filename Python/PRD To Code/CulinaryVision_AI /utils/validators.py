"""
Utilidades de validación para la aplicación.
"""
import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

from config.settings import settings

logger = logging.getLogger(__name__)

class Validators:
    """Clase con métodos de validación."""
    
    @staticmethod
    def validate_image_file(image_path: str) -> Dict[str, Any]:
        """
        Valida un archivo de imagen.
        
        Args:
            image_path: Ruta del archivo de imagen
            
        Returns:
            Diccionario con resultado de validación
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            # Verificar que el archivo existe
            if not os.path.exists(image_path):
                result['valid'] = False
                result['errors'].append(f"Archivo no encontrado: {image_path}")
                return result
            
            # Verificar extensión
            file_extension = Path(image_path).suffix.lower()
            if file_extension not in settings.SUPPORTED_IMAGE_FORMATS:
                result['valid'] = False
                result['errors'].append(f"Formato no soportado: {file_extension}")
                return result
            
            # Verificar tamaño del archivo
            file_size = os.path.getsize(image_path)
            if file_size > settings.MAX_FILE_SIZE:
                result['valid'] = False
                result['errors'].append(f"Archivo demasiado grande: {file_size} bytes")
                return result
            
            # Verificar que el archivo no esté vacío
            if file_size == 0:
                result['valid'] = False
                result['errors'].append("Archivo vacío")
                return result
            
            # Verificar permisos de lectura
            if not os.access(image_path, os.R_OK):
                result['valid'] = False
                result['errors'].append("Sin permisos de lectura")
                return result
            
            return result
            
        except Exception as e:
            result['valid'] = False
            result['errors'].append(f"Error al validar archivo: {str(e)}")
            return result
    
    @staticmethod
    def validate_image_list(image_paths: List[str]) -> Dict[str, Any]:
        """
        Valida una lista de archivos de imagen.
        
        Args:
            image_paths: Lista de rutas de archivos
            
        Returns:
            Diccionario con resultado de validación
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'valid_images': [],
            'invalid_images': []
        }
        
        if not image_paths:
            result['valid'] = False
            result['errors'].append("No se proporcionaron imágenes")
            return result
        
        if len(image_paths) > settings.MAX_IMAGES_PER_SESSION:
            result['valid'] = False
            result['errors'].append(f"Máximo {settings.MAX_IMAGES_PER_SESSION} imágenes por sesión")
            return result
        
        for image_path in image_paths:
            validation = Validators.validate_image_file(image_path)
            if validation['valid']:
                result['valid_images'].append(image_path)
            else:
                result['invalid_images'].append(image_path)
                result['errors'].extend(validation['errors'])
        
        if not result['valid_images']:
            result['valid'] = False
            result['errors'].append("No hay imágenes válidas")
        
        return result
    
    @staticmethod
    def validate_recipe_data(recipe_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida los datos de una receta.
        
        Args:
            recipe_data: Datos de la receta
            
        Returns:
            Diccionario con resultado de validación
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Campos requeridos
        required_fields = [
            'nombre', 'tiempo_preparacion_min', 'tiempo_coccion_min',
            'ingredientes', 'instrucciones'
        ]
        
        for field in required_fields:
            if field not in recipe_data:
                result['valid'] = False
                result['errors'].append(f"Campo requerido faltante: {field}")
        
        # Validar nombre
        if 'nombre' in recipe_data:
            nombre = recipe_data['nombre']
            if not nombre or not nombre.strip():
                result['valid'] = False
                result['errors'].append("Nombre de receta no puede estar vacío")
            elif len(nombre) > 100:
                result['warnings'].append("Nombre de receta muy largo")
        
        # Validar tiempos
        if 'tiempo_preparacion_min' in recipe_data:
            tiempo_prep = recipe_data['tiempo_preparacion_min']
            if not isinstance(tiempo_prep, int) or tiempo_prep < 0:
                result['valid'] = False
                result['errors'].append("Tiempo de preparación debe ser un entero positivo")
        
        if 'tiempo_coccion_min' in recipe_data:
            tiempo_coccion = recipe_data['tiempo_coccion_min']
            if not isinstance(tiempo_coccion, int) or tiempo_coccion < 0:
                result['valid'] = False
                result['errors'].append("Tiempo de cocción debe ser un entero positivo")
        
        # Validar ingredientes
        if 'ingredientes' in recipe_data:
            ingredientes = recipe_data['ingredientes']
            if not isinstance(ingredientes, list) or not ingredientes:
                result['valid'] = False
                result['errors'].append("Debe tener al menos un ingrediente")
            else:
                for i, ingrediente in enumerate(ingredientes):
                    if not isinstance(ingrediente, dict):
                        result['valid'] = False
                        result['errors'].append(f"Ingrediente {i+1} debe ser un diccionario")
                    elif 'nombre' not in ingrediente:
                        result['valid'] = False
                        result['errors'].append(f"Ingrediente {i+1} debe tener nombre")
        
        # Validar instrucciones
        if 'instrucciones' in recipe_data:
            instrucciones = recipe_data['instrucciones']
            if not isinstance(instrucciones, list) or not instrucciones:
                result['valid'] = False
                result['errors'].append("Debe tener al menos una instrucción")
            else:
                for i, instruccion in enumerate(instrucciones):
                    if not isinstance(instruccion, dict):
                        result['valid'] = False
                        result['errors'].append(f"Instrucción {i+1} debe ser un diccionario")
                    elif 'accion' not in instruccion:
                        result['valid'] = False
                        result['errors'].append(f"Instrucción {i+1} debe tener acción")
        
        return result
    
    @staticmethod
    def validate_user_profile(profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida los datos del perfil de usuario.
        
        Args:
            profile_data: Datos del perfil
            
        Returns:
            Diccionario con resultado de validación
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Validar tiempo disponible
        if 'tiempo_disponible' in profile_data:
            tiempo = profile_data['tiempo_disponible']
            if not isinstance(tiempo, int) or tiempo < 5:
                result['valid'] = False
                result['errors'].append("Tiempo disponible debe ser al menos 5 minutos")
            elif tiempo > 180:
                result['warnings'].append("Tiempo disponible muy alto")
        
        # Validar número de personas
        if 'num_personas' in profile_data:
            num_personas = profile_data['num_personas']
            if not isinstance(num_personas, int) or num_personas < 1:
                result['valid'] = False
                result['errors'].append("Número de personas debe ser al menos 1")
            elif num_personas > 10:
                result['valid'] = False
                result['errors'].append("Máximo 10 personas por sesión")
        
        # Validar nivel de picante
        if 'nivel_picante' in profile_data:
            nivel_picante = profile_data['nivel_picante']
            if not isinstance(nivel_picante, int) or not 1 <= nivel_picante <= 5:
                result['valid'] = False
                result['errors'].append("Nivel de picante debe estar entre 1 y 5")
        
        return result
    
    @staticmethod
    def validate_json_response(response_text: str) -> Dict[str, Any]:
        """
        Valida que una respuesta contenga JSON válido.
        
        Args:
            response_text: Texto de respuesta
            
        Returns:
            Diccionario con resultado de validación
        """
        result = {
            'valid': True,
            'errors': [],
            'json_data': None
        }
        
        try:
            # Buscar JSON en la respuesta
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                result['valid'] = False
                result['errors'].append("No se encontró JSON en la respuesta")
                return result
            
            json_str = response_text[start_idx:end_idx]
            json_data = json.loads(json_str)
            result['json_data'] = json_data
            
            return result
            
        except json.JSONDecodeError as e:
            result['valid'] = False
            result['errors'].append(f"JSON inválido: {str(e)}")
            return result
        except Exception as e:
            result['valid'] = False
            result['errors'].append(f"Error al procesar JSON: {str(e)}")
            return result
    
    @staticmethod
    def validate_api_configuration() -> Dict[str, Any]:
        """
        Valida la configuración de las APIs.
        
        Returns:
            Diccionario con resultado de validación
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'available_services': []
        }
        
        # Validar OpenAI
        if not settings.OPENAI_API_KEY:
            result['warnings'].append("OPENAI_API_KEY no configurada")
        else:
            result['available_services'].append('openai')
        
        # Validar Google Cloud Vision
        if not settings.GOOGLE_APPLICATION_CREDENTIALS:
            result['warnings'].append("GOOGLE_APPLICATION_CREDENTIALS no configurada")
        else:
            if os.path.exists(settings.GOOGLE_APPLICATION_CREDENTIALS):
                result['available_services'].append('google_vision')
            else:
                result['warnings'].append("Archivo de credenciales de Google Cloud no encontrado")
        
        if not result['available_services']:
            result['valid'] = False
            result['errors'].append("No hay servicios de IA disponibles")
        
        return result
    
    @staticmethod
    def validate_ingredient_data(ingredient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida los datos de un ingrediente.
        
        Args:
            ingredient_data: Datos del ingrediente
            
        Returns:
            Diccionario con resultado de validación
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Validar nombre
        if 'nombre' not in ingredient_data:
            result['valid'] = False
            result['errors'].append("Nombre de ingrediente es requerido")
        else:
            nombre = ingredient_data['nombre']
            if not nombre or not nombre.strip():
                result['valid'] = False
                result['errors'].append("Nombre de ingrediente no puede estar vacío")
        
        # Validar confianza
        if 'confianza' in ingredient_data:
            confianza = ingredient_data['confianza']
            if not isinstance(confianza, (int, float)) or not 0.0 <= confianza <= 1.0:
                result['valid'] = False
                result['errors'].append("Confianza debe estar entre 0.0 y 1.0")
        
        # Validar cantidad si está presente
        if 'cantidad' in ingredient_data and ingredient_data['cantidad'] is not None:
            cantidad = ingredient_data['cantidad']
            if not isinstance(cantidad, (int, float)) or cantidad <= 0:
                result['warnings'].append("Cantidad debe ser un número positivo")
        
        return result
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Valida formato de email.
        
        Args:
            email: Email a validar
            
        Returns:
            True si el email es válido
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
