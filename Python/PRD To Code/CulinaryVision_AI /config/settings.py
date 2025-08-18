"""
Configuraciones generales de la aplicación CulinaryVision AI.
"""
import os
from typing import List, Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Settings:
    """Configuraciones de la aplicación."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-vision-preview")
    
    # Google Cloud Vision Configuration
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    # Application Configuration
    MAX_IMAGES_PER_SESSION: int = int(os.getenv("MAX_IMAGES_PER_SESSION", "10"))
    MAX_RESPONSE_TIME: int = int(os.getenv("MAX_RESPONSE_TIME", "30"))
    MIN_CONFIDENCE_THRESHOLD: float = float(os.getenv("MIN_CONFIDENCE_THRESHOLD", "0.7"))
    DEFAULT_MAX_RECIPES: int = int(os.getenv("DEFAULT_MAX_RECIPES", "5"))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "culinary_vision.log")
    
    # Cache Configuration
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))
    
    # Development Configuration
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    TESTING: bool = os.getenv("TESTING", "false").lower() == "true"
    
    # Supported image formats
    SUPPORTED_IMAGE_FORMATS: List[str] = [".jpg", ".jpeg", ".png", ".heic", ".webp"]
    
    # Maximum file size (50MB)
    MAX_FILE_SIZE: int = 50 * 1024 * 1024
    
    # Minimum image resolution
    MIN_IMAGE_RESOLUTION: tuple = (640, 480)
    
    # Maximum image resolution (4K)
    MAX_IMAGE_RESOLUTION: tuple = (3840, 2160)
    
    # Default user preferences
    DEFAULT_USER_PREFERENCES = {
        "nivel_culinario": "intermedio",
        "tiempo_disponible": 30,
        "restricciones_dieteticas": [],
        "preferencias_culturales": ["mediterranea", "internacional"],
        "num_personas": 2
    }
    
    # Ingredientes básicos siempre disponibles
    INGREDIENTES_BASICOS = [
        "sal", "pimienta", "aceite de oliva", "agua", "azúcar", 
        "harina", "huevos", "cebolla", "ajo", "limón"
    ]
    
    # Temporadas del año
    TEMPORADAS = {
        "primavera": ["marzo", "abril", "mayo"],
        "verano": ["junio", "julio", "agosto"],
        "otoño": ["septiembre", "octubre", "noviembre"],
        "invierno": ["diciembre", "enero", "febrero"]
    }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Valida que las configuraciones críticas estén presentes."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY es requerida")
        return True
    
    @classmethod
    def get_temporada_actual(cls) -> str:
        """Obtiene la temporada actual basada en el mes."""
        import datetime
        mes_actual = datetime.datetime.now().strftime("%B").lower()
        
        for temporada, meses in cls.TEMPORADAS.items():
            if mes_actual in meses:
                return temporada
        return "general"

# Instancia global de configuraciones
settings = Settings()
