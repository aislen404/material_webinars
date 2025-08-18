# CulinaryVision AI - Generador de Recetas con Reconocimiento Visual

## 🍳 Descripción

CulinaryVision AI es una aplicación Python que utiliza reconocimiento de imágenes para identificar ingredientes disponibles y genera automáticamente al menos 5 recetas personalizadas mediante integración con LLM, optimizando el aprovechamiento de ingredientes disponibles en el hogar.

## ✨ Características Principales

- **Reconocimiento Visual**: Identifica ingredientes mediante análisis de imágenes
- **Generación Inteligente**: Crea 5+ recetas personalizadas usando IA
- **Optimización**: Maximiza el uso de ingredientes disponibles
- **Reducción de Desperdicio**: Aprovecha ingredientes que podrían perderse
- **Personalización**: Adapta recetas según nivel culinario y preferencias

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- Cuenta de OpenAI (para GPT-4 Vision)
- Cuenta de Google Cloud (opcional, para Vision AI)

### Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd PRD_To_Code
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus API keys
```

## ⚙️ Configuración

Crea un archivo `.env` con las siguientes variables:

```env
# OpenAI API (requerido)
OPENAI_API_KEY=tu_api_key_aqui

# Google Cloud Vision (opcional)
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

# Configuración de la aplicación
MAX_IMAGES_PER_SESSION=10
MAX_RESPONSE_TIME=30
MIN_CONFIDENCE_THRESHOLD=0.7
```

## 🎯 Uso

### Uso Básico

```python
from main import CulinaryVisionAI

# Inicializar la aplicación
app = CulinaryVisionAI()

# Procesar imágenes y generar recetas
recetas = app.generate_recipes_from_images([
    "path/to/ingredient1.jpg",
    "path/to/ingredient2.jpg"
])

print(recetas)
```

### Uso Avanzado

```python
from main import CulinaryVisionAI
from models.user_profile import UserProfile

# Crear perfil de usuario
perfil = UserProfile(
    nivel_culinario="intermedio",
    tiempo_disponible=30,
    restricciones_dieteticas=["vegetariano"],
    preferencias_culturales=["mediterranea", "asiatica"]
)

# Inicializar con perfil personalizado
app = CulinaryVisionAI(user_profile=perfil)

# Generar recetas personalizadas
recetas = app.generate_recipes_from_images(
    image_paths=["fridge.jpg", "pantry.jpg"],
    max_recipes=5
)
```

## 📁 Estructura del Proyecto

```
PRD_To_Code/
├── main.py                 # Punto de entrada principal
├── config/
│   ├── settings.py        # Configuraciones generales
│   └── prompts.py         # Plantillas de prompts para LLM
├── services/
│   ├── image_processor.py # Reconocimiento de ingredientes
│   ├── llm_client.py      # Cliente para API de LLM
│   └── recipe_generator.py # Lógica de generación de recetas
├── models/
│   ├── ingredient.py      # Modelo de datos ingrediente
│   ├── recipe.py          # Modelo de datos receta
│   └── user_profile.py    # Modelo de perfil de usuario
├── utils/
│   ├── validators.py      # Validaciones de entrada/salida
│   └── helpers.py         # Funciones auxiliares
├── tests/
│   ├── test_image_processing.py
│   ├── test_recipe_generation.py
│   └── test_integration.py
├── requirements.txt       # Dependencias del proyecto
├── .env.example          # Ejemplo de variables de entorno
└── README.md             # Este archivo
```

## 🧪 Testing

Ejecutar todas las pruebas:

```bash
pytest tests/
```

Ejecutar pruebas específicas:

```bash
pytest tests/test_image_processing.py -v
pytest tests/test_recipe_generation.py -v
```

## 📊 Métricas de Rendimiento

- **Precisión de reconocimiento**: ≥85% de exactitud en ingredientes comunes
- **Tiempo de respuesta**: <30 segundos desde captura hasta recetas
- **Consistencia**: 95% de sesiones generan exactamente 5+ recetas válidas
- **Satisfacción**: ≥4.2/5 estrellas en valoración de recetas

## 🔧 Desarrollo

### Formateo de código

```bash
black .
flake8 .
```

### Estructura de commits

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bugs
- `docs:` Documentación
- `test:` Pruebas
- `refactor:` Refactorización

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisa la documentación en el PRD
2. Busca en los issues existentes
3. Crea un nuevo issue con detalles del problema

## 🗺️ Roadmap

- [x] Estructura base del proyecto
- [ ] Reconocimiento de ingredientes con OpenAI Vision
- [ ] Generación de recetas con GPT-4
- [ ] Interfaz de línea de comandos
- [ ] Interfaz web con Streamlit
- [ ] Base de datos local de recetas
- [ ] Reconocimiento de estados de ingredientes
- [ ] Planificación semanal de menús
- [ ] Integración con APIs nutricionales
