"""
Servicio de procesamiento de imágenes para reconocimiento de ingredientes.
"""
import os
import base64
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import requests
try:
    from openai import OpenAI
except ImportError:
    # Fallback para versiones anteriores de openai
    import openai
    OpenAI = openai
try:
    from google.cloud import vision
except ImportError:
    vision = None

from config.settings import settings
from models.ingredient import Ingrediente, ListaIngredientes, EstadoIngrediente, UnidadMedida

# Configurar logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

class ImageProcessor:
    """Procesador de imágenes para reconocimiento de ingredientes."""
    
    def __init__(self):
        """Inicializa el procesador de imágenes."""
        self.openai_client = None
        self.vision_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Inicializa los clientes de APIs de visión."""
        # OpenAI Client
        if settings.OPENAI_API_KEY:
            try:
                self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info("Cliente OpenAI inicializado correctamente")
            except Exception as e:
                logger.error(f"Error al inicializar cliente OpenAI: {e}")
        
        # Google Cloud Vision Client
        if settings.GOOGLE_APPLICATION_CREDENTIALS and vision:
            try:
                self.vision_client = vision.ImageAnnotatorClient()
                logger.info("Cliente Google Cloud Vision inicializado correctamente")
            except Exception as e:
                logger.error(f"Error al inicializar cliente Google Cloud Vision: {e}")
    
    def validate_image(self, image_path: str) -> bool:
        """
        Valida que la imagen cumpla con los requisitos.
        
        Args:
            image_path: Ruta de la imagen
            
        Returns:
            True si la imagen es válida, False en caso contrario
        """
        try:
            # Verificar que el archivo existe
            if not os.path.exists(image_path):
                logger.error(f"Archivo no encontrado: {image_path}")
                return False
            
            # Verificar extensión
            file_extension = Path(image_path).suffix.lower()
            if file_extension not in settings.SUPPORTED_IMAGE_FORMATS:
                logger.error(f"Formato de imagen no soportado: {file_extension}")
                return False
            
            # Verificar tamaño del archivo
            file_size = os.path.getsize(image_path)
            if file_size > settings.MAX_FILE_SIZE:
                logger.error(f"Archivo demasiado grande: {file_size} bytes")
                return False
            
            # Verificar resolución
            with Image.open(image_path) as img:
                width, height = img.size
                if width < settings.MIN_IMAGE_RESOLUTION[0] or height < settings.MIN_IMAGE_RESOLUTION[1]:
                    logger.error(f"Resolución demasiado baja: {width}x{height}")
                    return False
                if width > settings.MAX_IMAGE_RESOLUTION[0] or height > settings.MAX_IMAGE_RESOLUTION[1]:
                    logger.error(f"Resolución demasiado alta: {width}x{height}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error al validar imagen {image_path}: {e}")
            return False
    
    def preprocess_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Preprocesa la imagen para mejorar el reconocimiento.
        
        Args:
            image_path: Ruta de la imagen
            
        Returns:
            Imagen preprocesada como array numpy
        """
        try:
            # Cargar imagen
            image = cv2.imread(image_path)
            if image is None:
                logger.error(f"No se pudo cargar la imagen: {image_path}")
                return None
            
            # Convertir a RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Ajustar contraste y brillo
            lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            
            # Aplicar CLAHE (Contrast Limited Adaptive Histogram Equalization)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            l = clahe.apply(l)
            
            # Reconstruir imagen
            lab = cv2.merge([l, a, b])
            processed_image = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
            
            # Redimensionar si es muy grande
            height, width = processed_image.shape[:2]
            if width > 1920 or height > 1080:
                scale = min(1920/width, 1080/height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                processed_image = cv2.resize(processed_image, (new_width, new_height))
            
            return processed_image
            
        except Exception as e:
            logger.error(f"Error al preprocesar imagen {image_path}: {e}")
            return None
    
    def encode_image_to_base64(self, image_path: str) -> Optional[str]:
        """
        Codifica una imagen a base64.
        
        Args:
            image_path: Ruta de la imagen
            
        Returns:
            Imagen codificada en base64
        """
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Error al codificar imagen {image_path}: {e}")
            return None
    
    def detect_ingredients_openai(self, image_path: str) -> ListaIngredientes:
        """
        Detecta ingredientes usando OpenAI Vision API.
        
        Args:
            image_path: Ruta de la imagen
            
        Returns:
            Lista de ingredientes detectados
        """
        if not self.openai_client:
            logger.error("Cliente OpenAI no disponible")
            return ListaIngredientes(error="Cliente OpenAI no disponible")
        
        try:
            # Codificar imagen
            base64_image = self.encode_image_to_base64(image_path)
            if not base64_image:
                return ListaIngredientes(error="No se pudo codificar la imagen")
            
            # Prompt para detección
            from config.prompts import PromptTemplates
            prompt = PromptTemplates.get_ingredient_detection_prompt()
            
            # Llamada a la API
            response = self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.1
            )
            
            # Procesar respuesta
            content = response.choices[0].message.content
            return self._parse_openai_response(content)
            
        except Exception as e:
            logger.error(f"Error en detección OpenAI: {e}")
            return ListaIngredientes(error=f"Error en detección: {str(e)}")
    
    def detect_ingredients_google_vision(self, image_path: str) -> ListaIngredientes:
        """
        Detecta ingredientes usando Google Cloud Vision API.
        
        Args:
            image_path: Ruta de la imagen
            
        Returns:
            Lista de ingredientes detectados
        """
        if not self.vision_client:
            logger.error("Cliente Google Cloud Vision no disponible")
            return ListaIngredientes(error="Cliente Google Cloud Vision no disponible")
        
        try:
            # Leer imagen
            with open(image_path, 'rb') as image_file:
                content = image_file.read()
            
            # Crear objeto de imagen
            image = vision.Image(content=content)
            
            # Realizar detección de objetos y etiquetas
            object_response = self.vision_client.object_localization(image=image)
            label_response = self.vision_client.label_detection(image=image)
            
            # Procesar resultados
            ingredientes = []
            
            # Procesar objetos detectados
            for obj in object_response.localized_object_annotations:
                if obj.score > settings.MIN_CONFIDENCE_THRESHOLD:
                    ingrediente = self._create_ingredient_from_google_object(obj)
                    if ingrediente:
                        ingredientes.append(ingrediente)
            
            # Procesar etiquetas
            for label in label_response.label_annotations:
                if label.score > settings.MIN_CONFIDENCE_THRESHOLD:
                    ingrediente = self._create_ingredient_from_google_label(label)
                    if ingrediente:
                        ingredientes.append(ingrediente)
            
            return ListaIngredientes(ingredientes=ingredientes)
            
        except Exception as e:
            logger.error(f"Error en detección Google Vision: {e}")
            return ListaIngredientes(error=f"Error en detección: {str(e)}")
    
    def _create_ingredient_from_google_object(self, obj) -> Optional[Ingrediente]:
        """Crea un ingrediente desde un objeto detectado por Google Vision."""
        # Mapeo de objetos comunes a ingredientes
        object_to_ingredient = {
            'Food': 'comida',
            'Vegetable': 'vegetal',
            'Fruit': 'fruta',
            'Meat': 'carne',
            'Fish': 'pescado',
            'Bread': 'pan',
            'Cheese': 'queso',
            'Egg': 'huevo',
            'Milk': 'leche',
            'Rice': 'arroz',
            'Pasta': 'pasta',
            'Tomato': 'tomate',
            'Onion': 'cebolla',
            'Garlic': 'ajo',
            'Carrot': 'zanahoria',
            'Potato': 'papa',
            'Chicken': 'pollo',
            'Beef': 'carne de res',
            'Pork': 'cerdo',
            'Salmon': 'salmón',
            'Shrimp': 'camarón'
        }
        
        nombre_objeto = obj.name.lower()
        for key, value in object_to_ingredient.items():
            if key.lower() in nombre_objeto:
                return Ingrediente(
                    nombre=value,
                    confianza=obj.score,
                    detectado=True,
                    categoria=self._categorize_ingredient(value)
                )
        
        return None
    
    def _create_ingredient_from_google_label(self, label) -> Optional[Ingrediente]:
        """Crea un ingrediente desde una etiqueta detectada por Google Vision."""
        # Mapeo de etiquetas a ingredientes
        label_to_ingredient = {
            'food': 'comida',
            'vegetable': 'vegetal',
            'fruit': 'fruta',
            'meat': 'carne',
            'fish': 'pescado',
            'bread': 'pan',
            'cheese': 'queso',
            'egg': 'huevo',
            'milk': 'leche',
            'rice': 'arroz',
            'pasta': 'pasta',
            'tomato': 'tomate',
            'onion': 'cebolla',
            'garlic': 'ajo',
            'carrot': 'zanahoria',
            'potato': 'papa',
            'chicken': 'pollo',
            'beef': 'carne de res',
            'pork': 'cerdo',
            'salmon': 'salmón',
            'shrimp': 'camarón'
        }
        
        nombre_label = label.description.lower()
        for key, value in label_to_ingredient.items():
            if key in nombre_label:
                return Ingrediente(
                    nombre=value,
                    confianza=label.score,
                    detectado=True,
                    categoria=self._categorize_ingredient(value)
                )
        
        return None
    
    def _categorize_ingredient(self, nombre: str) -> str:
        """Categoriza un ingrediente por tipo."""
        nombre_lower = nombre.lower()
        
        if any(word in nombre_lower for word in ['tomate', 'cebolla', 'ajo', 'zanahoria', 'papa', 'lechuga', 'espinaca']):
            return 'vegetal'
        elif any(word in nombre_lower for word in ['manzana', 'naranja', 'plátano', 'fresa', 'uva']):
            return 'fruta'
        elif any(word in nombre_lower for word in ['pollo', 'carne', 'cerdo', 'res', 'ternera']):
            return 'proteina'
        elif any(word in nombre_lower for word in ['pescado', 'salmón', 'camarón', 'atún']):
            return 'pescado'
        elif any(word in nombre_lower for word in ['leche', 'queso', 'yogur', 'mantequilla']):
            return 'lacteo'
        elif any(word in nombre_lower for word in ['arroz', 'pasta', 'pan', 'harina']):
            return 'carbohidrato'
        elif any(word in nombre_lower for word in ['huevo']):
            return 'proteina'
        else:
            return 'otros'
    
    def _parse_openai_response(self, response_text: str) -> ListaIngredientes:
        """Parsea la respuesta de OpenAI para extraer ingredientes."""
        try:
            import json
            
            # Intentar extraer JSON de la respuesta
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                logger.error("No se encontró JSON válido en la respuesta")
                return ListaIngredientes(error="Respuesta no válida")
            
            json_str = response_text[start_idx:end_idx]
            data = json.loads(json_str)
            
            # Procesar ingredientes
            ingredientes = []
            for ing_data in data.get('ingredientes', []):
                try:
                    ingrediente = Ingrediente(
                        nombre=ing_data.get('nombre', ''),
                        cantidad=ing_data.get('cantidad'),
                        unidad=UnidadMedida(ing_data.get('unidad')) if ing_data.get('unidad') else None,
                        estado=EstadoIngrediente(ing_data.get('estado', 'desconocido')),
                        confianza=ing_data.get('confianza', 0.0),
                        detectado=True,
                        categoria=self._categorize_ingredient(ing_data.get('nombre', ''))
                    )
                    ingredientes.append(ingrediente)
                except Exception as e:
                    logger.warning(f"Error al procesar ingrediente {ing_data}: {e}")
                    continue
            
            return ListaIngredientes(
                ingredientes=ingredientes,
                calidad_imagen=data.get('calidad_imagen'),
                error=data.get('error')
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear JSON: {e}")
            return ListaIngredientes(error="Error al parsear respuesta")
        except Exception as e:
            logger.error(f"Error al procesar respuesta: {e}")
            return ListaIngredientes(error=f"Error al procesar respuesta: {str(e)}")
    
    def detect_ingredients(self, image_path: str, use_openai: bool = True) -> ListaIngredientes:
        """
        Detecta ingredientes en una imagen usando el método especificado.
        
        Args:
            image_path: Ruta de la imagen
            use_openai: Si usar OpenAI (True) o Google Vision (False)
            
        Returns:
            Lista de ingredientes detectados
        """
        # Validar imagen
        if not self.validate_image(image_path):
            return ListaIngredientes(error="Imagen no válida")
        
        # Preprocesar imagen
        processed_image = self.preprocess_image(image_path)
        if processed_image is None:
            return ListaIngredientes(error="Error al preprocesar imagen")
        
        # Detectar ingredientes
        if use_openai and self.openai_client:
            return self.detect_ingredients_openai(image_path)
        elif self.vision_client:
            return self.detect_ingredients_google_vision(image_path)
        else:
            return ListaIngredientes(error="No hay servicios de detección disponibles")
    
    def detect_ingredients_batch(self, image_paths: List[str], use_openai: bool = True) -> List[ListaIngredientes]:
        """
        Detecta ingredientes en múltiples imágenes.
        
        Args:
            image_paths: Lista de rutas de imágenes
            use_openai: Si usar OpenAI (True) o Google Vision (False)
            
        Returns:
            Lista de resultados de detección
        """
        results = []
        
        for image_path in image_paths:
            logger.info(f"Procesando imagen: {image_path}")
            result = self.detect_ingredients(image_path, use_openai)
            results.append(result)
        
        return results
    
    def merge_ingredient_lists(self, ingredient_lists: List[ListaIngredientes]) -> ListaIngredientes:
        """
        Combina múltiples listas de ingredientes en una sola.
        
        Args:
            ingredient_lists: Lista de ListaIngredientes
            
        Returns:
            Lista combinada de ingredientes
        """
        all_ingredients = []
        
        for lista in ingredient_lists:
            if lista.ingredientes:
                all_ingredients.extend(lista.ingredientes)
        
        # Eliminar duplicados basándose en nombre
        unique_ingredients = {}
        for ingrediente in all_ingredients:
            nombre = ingrediente.nombre.lower()
            if nombre not in unique_ingredients:
                unique_ingredients[nombre] = ingrediente
            else:
                # Si ya existe, usar el de mayor confianza
                if ingrediente.confianza > unique_ingredients[nombre].confianza:
                    unique_ingredients[nombre] = ingrediente
        
        return ListaIngredientes(ingredientes=list(unique_ingredients.values()))
