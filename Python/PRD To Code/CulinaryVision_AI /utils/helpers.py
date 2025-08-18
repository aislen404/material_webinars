"""
Funciones auxiliares para la aplicación.
"""
import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class Helpers:
    """Clase con funciones auxiliares."""
    
    @staticmethod
    def format_time(minutes: int) -> str:
        """
        Formatea tiempo en minutos a formato legible.
        
        Args:
            minutes: Tiempo en minutos
            
        Returns:
            Tiempo formateado
        """
        if minutes < 60:
            return f"{minutes} min"
        else:
            hours = minutes // 60
            remaining_minutes = minutes % 60
            if remaining_minutes == 0:
                return f"{hours}h"
            else:
                return f"{hours}h {remaining_minutes}min"
    
    @staticmethod
    def format_difficulty(stars: int) -> str:
        """
        Formatea dificultad en estrellas a texto.
        
        Args:
            stars: Número de estrellas (1-5)
            
        Returns:
            Dificultad formateada
        """
        difficulty_map = {
            1: "Muy fácil",
            2: "Fácil", 
            3: "Intermedio",
            4: "Difícil",
            5: "Muy difícil"
        }
        return difficulty_map.get(stars, "Intermedio")
    
    @staticmethod
    def save_recipes_to_file(recipes: Dict[str, Any], filename: str) -> bool:
        """
        Guarda recetas en un archivo JSON.
        
        Args:
            recipes: Diccionario con recetas
            filename: Nombre del archivo
            
        Returns:
            True si se guardó correctamente
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(recipes, f, ensure_ascii=False, indent=2)
            logger.info(f"Recetas guardadas en {filename}")
            return True
        except Exception as e:
            logger.error(f"Error al guardar recetas: {e}")
            return False
    
    @staticmethod
    def load_recipes_from_file(filename: str) -> Optional[Dict[str, Any]]:
        """
        Carga recetas desde un archivo JSON.
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            Diccionario con recetas o None si hay error
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                recipes = json.load(f)
            logger.info(f"Recetas cargadas desde {filename}")
            return recipes
        except Exception as e:
            logger.error(f"Error al cargar recetas: {e}")
            return None
    
    @staticmethod
    def create_output_directory(directory: str) -> bool:
        """
        Crea un directorio de salida si no existe.
        
        Args:
            directory: Ruta del directorio
            
        Returns:
            True si se creó correctamente
        """
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Error al crear directorio {directory}: {e}")
            return False
    
    @staticmethod
    def get_file_size_mb(file_path: str) -> float:
        """
        Obtiene el tamaño de un archivo en MB.
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            Tamaño en MB
        """
        try:
            size_bytes = os.path.getsize(file_path)
            return size_bytes / (1024 * 1024)
        except Exception as e:
            logger.error(f"Error al obtener tamaño de archivo: {e}")
            return 0.0
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitiza un nombre de archivo para que sea seguro.
        
        Args:
            filename: Nombre original del archivo
            
        Returns:
            Nombre sanitizado
        """
        # Caracteres no permitidos en nombres de archivo
        invalid_chars = '<>:"/\\|?*'
        
        # Reemplazar caracteres inválidos
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limitar longitud
        if len(filename) > 255:
            filename = filename[:255]
        
        return filename
    
    @staticmethod
    def format_ingredient_list(ingredients: List[Dict[str, Any]]) -> str:
        """
        Formatea una lista de ingredientes para mostrar.
        
        Args:
            ingredients: Lista de ingredientes
            
        Returns:
            Lista formateada
        """
        formatted = []
        for ingredient in ingredients:
            nombre = ingredient.get('nombre', '')
            cantidad = ingredient.get('cantidad', '')
            unidad = ingredient.get('unidad', '')
            
            if cantidad and unidad:
                formatted.append(f"• {cantidad} {unidad} de {nombre}")
            else:
                formatted.append(f"• {nombre}")
        
        return '\n'.join(formatted)
    
    @staticmethod
    def format_instructions(instructions: List[Dict[str, Any]]) -> str:
        """
        Formatea instrucciones para mostrar.
        
        Args:
            instructions: Lista de instrucciones
            
        Returns:
            Instrucciones formateadas
        """
        formatted = []
        for instruction in instructions:
            paso = instruction.get('paso', 1)
            accion = instruction.get('accion', '')
            tiempo = instruction.get('tiempo_estimado', '')
            tip = instruction.get('tip', '')
            
            line = f"{paso}. {accion}"
            if tiempo:
                line += f" ({tiempo})"
            formatted.append(line)
            
            if tip:
                formatted.append(f"   💡 {tip}")
        
        return '\n'.join(formatted)
    
    @staticmethod
    def calculate_nutritional_totals(recipes: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calcula totales nutricionales de una lista de recetas.
        
        Args:
            recipes: Lista de recetas
            
        Returns:
            Diccionario con totales nutricionales
        """
        totals = {
            'calorias': 0,
            'proteinas': 0,
            'carbohidratos': 0,
            'grasas': 0,
            'fibra': 0
        }
        
        for recipe in recipes:
            info_nut = recipe.get('informacion_nutricional', {})
            totals['calorias'] += info_nut.get('calorias_por_porcion', 0)
            totals['proteinas'] += info_nut.get('proteinas_g', 0)
            totals['carbohidratos'] += info_nut.get('carbohidratos_g', 0)
            totals['grasas'] += info_nut.get('grasas_g', 0)
            totals['fibra'] += info_nut.get('fibra_g', 0)
        
        return totals
    
    @staticmethod
    def get_recipe_summary(recipe: Dict[str, Any]) -> str:
        """
        Genera un resumen de una receta.
        
        Args:
            recipe: Datos de la receta
            
        Returns:
            Resumen de la receta
        """
        nombre = recipe.get('nombre', '')
        tiempo_total = recipe.get('tiempo_total_min', 0)
        dificultad = recipe.get('dificultad_estrellas', 3)
        porciones = recipe.get('porciones', 2)
        tipo_cocina = recipe.get('tipo_cocina', 'internacional')
        
        tiempo_formateado = Helpers.format_time(tiempo_total)
        dificultad_formateada = Helpers.format_difficulty(dificultad)
        
        return f"{nombre} • {tiempo_formateado} • {dificultad_formateada} • {porciones} porciones • {tipo_cocina}"
    
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
    
    @staticmethod
    def generate_session_id() -> str:
        """
        Genera un ID único para la sesión.
        
        Returns:
            ID de sesión
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        import random
        random_suffix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
        return f"session_{timestamp}_{random_suffix}"
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """
        Formatea tamaño de archivo en bytes a formato legible.
        
        Args:
            size_bytes: Tamaño en bytes
            
        Returns:
            Tamaño formateado
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    @staticmethod
    def get_image_info(image_path: str) -> Dict[str, Any]:
        """
        Obtiene información de una imagen.
        
        Args:
            image_path: Ruta de la imagen
            
        Returns:
            Diccionario con información de la imagen
        """
        try:
            from PIL import Image
            
            with Image.open(image_path) as img:
                width, height = img.size
                format_name = img.format
                mode = img.mode
                file_size = os.path.getsize(image_path)
                
                return {
                    'width': width,
                    'height': height,
                    'format': format_name,
                    'mode': mode,
                    'file_size': file_size,
                    'file_size_formatted': Helpers.format_file_size(file_size),
                    'aspect_ratio': round(width / height, 2)
                }
        except Exception as e:
            logger.error(f"Error al obtener información de imagen: {e}")
            return {}
    
    @staticmethod
    def create_recipe_markdown(recipe: Dict[str, Any]) -> str:
        """
        Crea un archivo Markdown con una receta.
        
        Args:
            recipe: Datos de la receta
            
        Returns:
            Contenido Markdown
        """
        markdown = f"# {recipe.get('nombre', 'Receta')}\n\n"
        
        # Información básica
        markdown += f"**Tiempo total:** {Helpers.format_time(recipe.get('tiempo_total_min', 0))}\n"
        markdown += f"**Dificultad:** {Helpers.format_difficulty(recipe.get('dificultad_estrellas', 3))}\n"
        markdown += f"**Porciones:** {recipe.get('porciones', 2)}\n"
        markdown += f"**Tipo de cocina:** {recipe.get('tipo_cocina', 'internacional')}\n\n"
        
        # Descripción
        if recipe.get('descripcion_corta'):
            markdown += f"## Descripción\n\n{recipe['descripcion_corta']}\n\n"
        
        # Ingredientes
        markdown += "## Ingredientes\n\n"
        markdown += Helpers.format_ingredient_list(recipe.get('ingredientes', []))
        markdown += "\n\n"
        
        # Instrucciones
        markdown += "## Instrucciones\n\n"
        markdown += Helpers.format_instructions(recipe.get('instrucciones', []))
        markdown += "\n\n"
        
        # Información nutricional
        info_nut = recipe.get('informacion_nutricional', {})
        if info_nut:
            markdown += "## Información Nutricional\n\n"
            markdown += f"- **Calorías por porción:** {info_nut.get('calorias_por_porcion', 0)} kcal\n"
            markdown += f"- **Proteínas:** {info_nut.get('proteinas_g', 0)}g\n"
            markdown += f"- **Carbohidratos:** {info_nut.get('carbohidratos_g', 0)}g\n"
            markdown += f"- **Grasas:** {info_nut.get('grasas_g', 0)}g\n"
            if info_nut.get('fibra_g'):
                markdown += f"- **Fibra:** {info_nut['fibra_g']}g\n"
            markdown += "\n"
        
        # Consejos del chef
        consejos = recipe.get('consejos_chef', [])
        if consejos:
            markdown += "## Consejos del Chef\n\n"
            for consejo in consejos:
                markdown += f"- {consejo}\n"
            markdown += "\n"
        
        # Variaciones
        variaciones = recipe.get('variaciones', [])
        if variaciones:
            markdown += "## Variaciones\n\n"
            for variacion in variaciones:
                markdown += f"- {variacion}\n"
            markdown += "\n"
        
        return markdown
