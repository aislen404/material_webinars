# PRD - Aplicación de Recetas con Reconocimiento de Ingredientes

## 1. Información General del Proyecto

### 1.1 Título del Prompt
**CulinaryVision AI - Generador de Recetas Basado en Reconocimiento Visual de Ingredientes**

### 1.2 Versión y Fecha
- **Versión:** v1.0
- **Fecha de creación:** 17/08/2025
- **Última actualización:** 17/08/2025
- **Autor:** Equipo de Desarrollo CulinaryVision

### 1.3 Resumen Ejecutivo
Aplicación Python que utiliza reconocimiento de imágenes para identificar ingredientes disponibles y genera automáticamente al menos 5 recetas personalizadas mediante integración con LLM, optimizando el aprovechamiento de ingredientes disponibles en el hogar.

## 2. Contexto y Justificación

### 2.1 Problema a Resolver
Los usuarios frecuentemente tienen ingredientes disponibles en casa pero carecen de inspiración o conocimiento para crear recetas variadas. El proceso manual de buscar recetas compatibles con ingredientes específicos es tedioso y limitado. Además, muchas veces se desperdician ingredientes por falta de ideas culinarias creativas que los aprovechen eficientemente.

### 2.2 Audiencia Objetivo
- **Usuario primario:** Personas de 25-55 años que cocinan regularmente en casa, con smartphones y conocimientos básicos de tecnología
- **Usuario secundario:** Estudiantes universitarios, profesionales ocupados, entusiastas de la cocina que buscan optimizar sus ingredientes
- **Nivel técnico requerido:** Básico - solo necesitan tomar fotos con su dispositivo

### 2.3 Caso de Uso Principal
Usuario llega a casa después del trabajo, abre su refrigerador y despensa, toma fotos de los ingredientes disponibles, la aplicación los identifica automáticamente y genera 5+ recetas personalizadas considerando tiempo de preparación, dificultad y preferencias dietéticas.

## 3. Objetivos y Metas

### 3.1 Objetivo Principal
Desarrollar una aplicación Python que identifique ingredientes mediante análisis de imágenes y genere automáticamente un mínimo de 5 recetas culinarias personalizadas, reduciendo el desperdicio de alimentos y inspirando creatividad culinaria.

### 3.2 Objetivos Secundarios
- Reducir el tiempo de planificación de comidas de 30 minutos a 5 minutos
- Minimizar el desperdicio alimentario aprovechando ingredientes disponibles
- Educar usuarios sobre nuevas técnicas culinarias y combinaciones de ingredientes
- Ofrecer opciones adaptadas a restricciones dietéticas específicas
- Crear una experiencia culinaria gamificada y engaging

### 3.3 Métricas de Éxito
- **Precisión:** ≥85% de exactitud en identificación de ingredientes comunes
- **Consistencia:** 95% de las sesiones generan exactamente 5+ recetas válidas
- **Tiempo de respuesta:** <30 segundos desde captura hasta recetas generadas
- **Satisfacción del usuario:** ≥4.2/5 estrellas en valoración de recetas
- **Retención:** 70% de usuarios activos después de 30 días

## 4. Requisitos Funcionales

### 4.1 Entrada (Input)
- **Tipo de entrada:** Imágenes digitales (JPG, PNG, HEIC)
- **Formato esperado:** Fotos de ingredientes individuales o grupos de ingredientes
- **Resolución mínima:** 640x480 píxeles, máxima 4K
- **Tamaño archivo:** 100KB - 50MB por imagen
- **Cantidad:** 1-10 imágenes por sesión
- **Idioma:** Independiente (reconocimiento visual)
- **Ejemplos de entrada válida:**
  ```
  - Foto de refrigerador abierto mostrando vegetales, lácteos, carnes
  - Imagen de despensa con granos, especias, conservas
  - Foto individual de tomates, cebollas, ajo sobre mesada
  - Captura de ingredientes organizados en bowls separados
  ```

### 4.2 Salida (Output)
- **Tipo de salida:** Lista estructurada de recetas en formato JSON/texto
- **Formato requerido:** Cada receta con título, ingredientes, instrucciones paso a paso, tiempo, dificultad
- **Cantidad:** Mínimo 5 recetas, máximo 8 recetas
- **Elementos obligatorios por receta:**
  - Nombre descriptivo y atractivo
  - Lista de ingredientes con cantidades exactas
  - Instrucciones numeradas paso a paso
  - Tiempo de preparación y cocción
  - Nivel de dificultad (1-5 estrellas)
  - Información nutricional básica
  - Tips adicionales o sustituciones
- **Ejemplos de salida deseada:**
  ```json
  {
    "recetas": [
      {
        "nombre": "Pasta Mediterranea con Tomates Cherry",
        "tiempo_prep": "15 min",
        "tiempo_coccion": "20 min",
        "dificultad": 2,
        "porciones": 4,
        "ingredientes": [
          {"item": "Pasta", "cantidad": "400g", "identificado": true},
          {"item": "Tomates cherry", "cantidad": "300g", "identificado": true}
        ],
        "instrucciones": [
          "Hervir agua con sal para la pasta",
          "Cortar tomates cherry por la mitad"
        ],
        "calorias_aproximadas": 450,
        "tags": ["vegetariano", "mediterraneo", "rapido"]
      }
    ]
  }
  ```

### 4.3 Comportamiento Esperado
- **Tono:** Amigable, inspirador y educativo
- **Estilo:** Instructivo pero accesible, con lenguaje culinario apropiado
- **Nivel de detalle:** Alto en instrucciones, medio en explicaciones técnicas
- **Estructura de respuesta:** Lista organizada de recetas con formato consistente
- **Personalización:** Adaptación automática basada en ingredientes detectados

## 5. Requisitos No Funcionales

### 5.1 Restricciones
- **Contenido prohibido:** Recetas con ingredientes tóxicos, peligrosos o no comestibles
- **Limitaciones técnicas:** Máximo 10 imágenes por sesión para optimizar performance
- **Restricciones de tiempo:** Respuesta completa en <30 segundos
- **Idiomas:** Inicialmente español, expansión a inglés en v2.0
- **Plataformas:** Python 3.8+, compatible con Windows, macOS, Linux

### 5.2 Consideraciones de Calidad
- **Exactitud:** 85% precisión mínima en identificación de ingredientes
- **Claridad:** Instrucciones comprensibles para cocineros novatos
- **Relevancia:** Solo recetas factibles con ingredientes detectados (mín. 80% coincidencia)
- **Originalidad:** Combinación única de recetas clásicas y creativas
- **Seguridad alimentaria:** Verificación de compatibilidad de ingredientes

### 5.3 Manejo de Casos Límite
- **Entradas ambiguas:** Solicitar aclaración o foto adicional con mejor ángulo
- **Información insuficiente:** Generar recetas con ingredientes base + sugerencias de compra
- **Solicitudes fuera del alcance:** Redirigir a funcionalidades disponibles con mensaje educativo
- **Ingredientes no identificados:** Permitir identificación manual por el usuario
- **Restricciones dietéticas:** Filtrar recetas automáticamente según perfil usuario

## 6. Especificaciones Técnicas

### 6.1 Estructura del Prompt Principal
```python
"""
Eres un chef experto y nutricionista con 15 años de experiencia internacional. 
Tu especialidad es crear recetas deliciosas y saludables optimizando ingredientes disponibles.

INGREDIENTES DETECTADOS: {lista_ingredientes_identificados}
INGREDIENTES ADICIONALES DISPONIBLES: {ingredientes_despensa_comunes}
RESTRICCIONES DIETÉTICAS: {restricciones_usuario}
TIEMPO DISPONIBLE: {tiempo_maximo_coccion}
NIVEL CULINARIO USUARIO: {nivel_experiencia}

TAREA: Genera exactamente 5 recetas únicas y deliciosas que maximicen el uso de los ingredientes detectados.

FORMATO REQUERIDO:
- JSON válido con estructura predefinida
- Cada receta debe usar mínimo 60% de ingredientes detectados
- Incluir alternativas para ingredientes faltantes
- Ordenar por facilidad de preparación (más fácil primero)
- Agregar tips profesionales para mejorar sabor

CONSIDERACIONES ESPECIALES:
- Priorizar recetas de temporada actual
- Incluir información nutricional básica
- Sugerir maridajes o acompañamientos
- Verificar compatibilidad de sabores
- Adaptar porciones según ingredientes disponibles
"""
```

### 6.2 Variables Dinámicas
- **{lista_ingredientes_identificados}:** Array de ingredientes detectados con confianza >70%
- **{ingredientes_despensa_comunes}:** Lista de ingredientes básicos asumidos (sal, aceite, etc.)
- **{restricciones_usuario}:** Preferencias dietéticas del perfil (vegetariano, sin gluten, etc.)
- **{tiempo_maximo_coccion}:** Tiempo disponible seleccionado por usuario (15min, 30min, 1h, >1h)
- **{nivel_experiencia}:** Nivel culinario (principiante, intermedio, avanzado)
- **{temporada_actual}:** Estación del año para ingredientes de temporada
- **{region_usuario}:** Ubicación para adaptar disponibilidad de ingredientes

### 6.3 Instrucciones Especiales
- Validar que cada receta sea ejecutable con ingredientes detectados
- Incluir al menos una receta vegetariana si es posible con ingredientes disponibles
- Priorizar técnicas culinarias educativas pero accesibles
- Generar nombres creativos y apetitosos para cada receta
- Incluir consejos de conservación para ingredientes sobrantes
- Adaptar cantidades según número estimado de porciones

## 7. Validación y Pruebas

### 7.1 Criterios de Aceptación
- [ ] El sistema identifica correctamente ≥85% de ingredientes comunes en imágenes nítidas
- [ ] Genera exactamente 5 recetas válidas por sesión
- [ ] Cada receta utiliza mínimo 60% de ingredientes detectados
- [ ] Formato JSON de salida es válido y parseable
- [ ] Tiempo total de procesamiento <30 segundos
- [ ] Instrucciones son claras y ejecutables por usuario objetivo
- [ ] Sistema maneja graciosamente errores de reconocimiento
- [ ] Interfaz permite retroalimentación sobre calidad de recetas

### 7.2 Casos de Prueba
| ID | Entrada de Prueba | Resultado Esperado | Estado |
|----|-------------------|-------------------|--------|
| TC01 | Imagen con tomate, cebolla, ajo, pasta | 5 recetas italianas/mediterráneas, uso >60% ingredientes | [ ] |
| TC02 | Foto refrigerador con pollo, brócoli, arroz | 5 recetas variadas, al menos 1 asiática, balanceadas nutricionalmente | [ ] |
| TC03 | Imagen borrosa con 2 ingredientes identificables | Solicita imagen adicional + genera 3 recetas con sugerencias compra | [ ] |
| TC04 | Despensa con solo granos y especias | 5 recetas vegetarianas, énfasis en proteínas vegetales | [ ] |
| TC05 | 10 ingredientes diversos alta calidad | 5 recetas gourmet, diferentes técnicas culinarias | [ ] |
| TC06 | Ingredientes con restricción sin gluten activada | 5 recetas certificadas sin gluten, alternativas harinas | [ ] |
| TC07 | Imagen sin ingredientes reconocibles | Mensaje educativo + sugerencias ingredientes básicos | [ ] |
| TC08 | Ingredientes perecederos (pescado, lácteos) | Priorizar recetas que usen ingredientes perecederos primero | [ ] |

### 7.3 Escenarios de Error
- **Error de reconocimiento:** Imagen no contiene ingredientes → **Respuesta:** "No pude identificar ingredientes claros. Intenta con mejor iluminación o acércate más a los ingredientes."
- **Ingredientes incompatibles:** Combinación extraña detectada → **Respuesta:** Generar recetas separadas por grupos de ingredientes compatibles
- **Fallo de LLM:** API externa no responde → **Respuesta:** Usar recetas locales precargadas basadas en ingredientes detectados
- **Imagen corrupta:** Archivo no se puede procesar → **Respuesta:** "Imagen no válida. Intenta con otro formato (JPG/PNG)."
- **Sobrecarga sistema:** Muchas peticiones simultáneas → **Respuesta:** Cola de procesamiento con tiempo estimado de espera

## 8. Implementación

### 8.1 Prompt Final para LLM
```python
PROMPT_TEMPLATE = """
Actúa como un chef profesional con especialización en cocina internacional y nutrición. 
Tu misión es transformar ingredientes disponibles en recetas extraordinarias.

=== ANÁLISIS DE INGREDIENTES ===
Ingredientes principales detectados: {ingredientes_detectados}
Confianza de detección: {confianzas_deteccion}
Ingredientes básicos disponibles: sal, pimienta, aceite de oliva, agua
Restricciones dietéticas activas: {restricciones}

=== PERFIL DEL USUARIO ===
Nivel culinario: {nivel_usuario}
Tiempo disponible: {tiempo_disponible}
Preferencias culturales: {preferencias_culturales}
Número de comensales: {num_personas}

=== INSTRUCCIONES ESPECÍFICAS ===
1. Genera EXACTAMENTE 5 recetas únicas
2. Cada receta debe usar mínimo 3 de los ingredientes detectados
3. Ordena por dificultad: principiante a intermedio
4. Incluye al menos 1 receta que se complete en <20 minutos
5. Balancea tipos de cocción: crudo, salteado, horneado, hervido

=== FORMATO DE RESPUESTA REQUERIDO ===
Responde únicamente en JSON válido siguiendo esta estructura exacta:

{
  "metadata": {
    "total_recetas": 5,
    "ingredientes_utilizados": ["lista", "de", "ingredientes"],
    "tiempo_generacion": "timestamp"
  },
  "recetas": [
    {
      "id": 1,
      "nombre": "Título Atractivo de la Receta",
      "descripcion_corta": "Descripción en una línea que despierte apetito",
      "tiempo_preparacion_min": 15,
      "tiempo_coccion_min": 20,
      "tiempo_total_min": 35,
      "dificultad_estrellas": 2,
      "porciones": 4,
      "tipo_cocina": "italiana",
      "ingredientes": [
        {
          "nombre": "Ingrediente 1",
          "cantidad": "200g",
          "unidad": "gramos",
          "detectado": true,
          "esencial": true
        }
      ],
      "instrucciones": [
        {
          "paso": 1,
          "accion": "Descripción detallada del primer paso",
          "tiempo_estimado": "5 min",
          "tip": "Consejo profesional opcional"
        }
      ],
      "informacion_nutricional": {
        "calorias_por_porcion": 350,
        "proteinas_g": 25,
        "carbohidratos_g": 45,
        "grasas_g": 12
      },
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
    }
  ]
}

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

Genera las recetas ahora manteniendo el más alto estándar culinario y nutricional.
"""
```

### 8.2 Variaciones del Prompt
- **Versión Express:** Para usuarios con <15 minutos disponibles, enfoque en recetas rápidas
- **Versión Gourmet:** Para usuarios avanzados, técnicas sofisticadas y presentación elaborada
- **Versión Saludable:** Énfasis en balance nutricional y ingredientes orgánicos
- **Versión Familiar:** Recetas adaptadas para niños y grandes cantidades
- **Versión Económica:** Maximizar ingredientes, minimizar desperdicio y costo

### 8.3 Arquitectura de la Aplicación Python
```python
# Estructura modular propuesta
├── main.py                 # Punto de entrada de la aplicación
├── config/
│   ├── settings.py        # Configuraciones generales
│   └── prompts.py         # Plantillas de prompts
├── services/
│   ├── image_processor.py # Reconocimiento de ingredientes
│   ├── llm_client.py      # Cliente para API de LLM
│   └── recipe_generator.py # Lógica de generación
├── models/
│   ├── ingredient.py      # Modelo de datos ingrediente
│   └── recipe.py          # Modelo de datos receta
├── utils/
│   ├── validators.py      # Validaciones de entrada/salida
│   └── helpers.py         # Funciones auxiliares
└── tests/
    ├── test_image_processing.py
    └── test_recipe_generation.py
```

## 9. Mantenimiento y Evolución

### 9.1 Versionado
- **v1.0:** Versión inicial con reconocimiento básico e integración LLM
- **v1.1:** Mejoras en precisión de reconocimiento + base de datos local de recetas
- **v1.2:** Interfaz gráfica mejorada + perfiles de usuario personalizables
- **v2.0:** Reconocimiento de estados de ingredientes (maduro, fresco, etc.) + IA local
- **v2.5:** Integración con APIs nutricionales + planificación semanal de menús
- **v3.0:** Realidad aumentada para detección + asistente de cocina por voz

### 9.2 Feedback y Mejoras
- **Fuentes de feedback:** Ratings de recetas, encuestas in-app, analytics de uso, reviews en tiendas
- **Proceso de actualización:** Sprints quincenales con A/B testing de nuevas características
- **Métricas de seguimiento:** Tasa de éxito de recetas, tiempo promedio de uso, retención de usuarios
- **Feedback loop:** Sistema de aprendizaje continuo basado en preferencias del usuario

### 9.3 Métricas de Rendimiento
- **Precisión de reconocimiento:** Objetivo 85%, actual TBD, medición semanal
- **Tiempo de respuesta:** Objetivo <30s, actual TBD, monitoreo continuo
- **Satisfacción de recetas:** Objetivo 4.2/5, medición por rating post-cocción
- **Engagement diario:** Objetivo 15 min/sesión, medición via analytics
- **Conversión receta→cocinar:** Objetivo 60%, medición por encuestas follow-up

## 10. Anexos

### 10.1 Referencias
- [OpenAI Vision API Documentation](https://platform.openai.com/docs/guides/vision)
- [Google Cloud Vision AI - Food Recognition](https://cloud.google.com/vision/docs)
- [Spoonacular API for Recipe Data](https://spoonacular.com/food-api)
- [USDA FoodData Central for Nutritional Information](https://fdc.nal.usda.gov/)
- [Clarifai Food Recognition Models](https://www.clarifai.com/models/food-image-recognition)
- [Python Image Processing Libraries: PIL, OpenCV, scikit-image](https://pillow.readthedocs.io/)

### 10.2 Glosario
- **LLM:** Large Language Model - Modelo de lenguaje grande para generación de texto
- **API:** Application Programming Interface - Interfaz de programación de aplicaciones
- **JSON:** JavaScript Object Notation - Formato de intercambio de datos
- **Computer Vision:** Visión por computadora para análisis de imágenes
- **Confianza:** Porcentaje de certeza en la identificación de un ingrediente
- **OCR:** Optical Character Recognition - Reconocimiento óptico de caracteres
- **Endpoint:** Punto final de conexión de API
- **Tokenización:** Proceso de división de texto en unidades más pequeñas
- **Embedding:** Representación vectorial de datos para procesamiento IA

### 10.3 Ejemplos Completos

#### Ejemplo de Sesión Completa:

**Input:** Imagen de refrigerador con tomates cherry, mozzarella, albahaca, pasta, aceite de oliva

**Proceso:**
1. Reconocimiento visual identifica: tomates cherry (95%), mozzarella (90%), albahaca (85%), pasta (98%)
2. Sistema consulta perfil usuario: vegetariano, nivel intermedio, 30 min disponibles
3. LLM genera 5 recetas con prompt personalizado
4. Validación de salida y formateo final

**Output Esperado:**
```json
{
  "metadata": {
    "total_recetas": 5,
    "ingredientes_utilizados": ["tomates cherry", "mozzarella", "albahaca", "pasta"],
    "tiempo_generacion": "2025-08-17T14:30:00Z"
  },
  "recetas": [
    {
      "id": 1,
      "nombre": "Pasta Caprese Clásica",
      "descripcion_corta": "La combinación perfecta italiana en menos de 20 minutos",
      "tiempo_preparacion_min": 5,
      "tiempo_coccion_min": 15,
      "tiempo_total_min": 20,
      "dificultad_estrellas": 2,
      "porciones": 4,
      "tipo_cocina": "italiana",
      "ingredientes": [
        {
          "nombre": "Pasta (spaghetti o penne)",
          "cantidad": "400g",
          "unidad": "gramos",
          "detectado": true,
          "esencial": true
        },
        {
          "nombre": "Tomates cherry",
          "cantidad": "300g",
          "unidad": "gramos", 
          "detectado": true,
          "esencial": true
        },
        {
          "nombre": "Mozzarella fresca",
          "cantidad": "250g",
          "unidad": "gramos",
          "detectado": true,
          "esencial": true
        },
        {
          "nombre": "Albahaca fresca",
          "cantidad": "20 hojas",
          "unidad": "hojas",
          "detectado": true,
          "esencial": true
        },
        {
          "nombre": "Aceite de oliva virgen extra",
          "cantidad": "3 cucharadas",
          "unidad": "cucharadas",
          "detectado": true,
          "esencial": true
        }
      ],
      "instrucciones": [
        {
          "paso": 1,
          "accion": "Poner a hervir abundante agua con sal para la pasta",
          "tiempo_estimado": "3 min",
          "tip": "El agua debe estar bien salada, como el mar"
        },
        {
          "paso": 2,  
          "accion": "Cortar los tomates cherry por la mitad y la mozzarella en cubos de 1cm",
          "tiempo_estimado": "5 min",
          "tip": "Escurre la mozzarella para evitar exceso de líquido"
        },
        {
          "paso": 3,
          "accion": "Cocinar la pasta según instrucciones del paquete hasta al dente",
          "tiempo_estimado": "10-12 min",
          "tip": "Prueba 2 minutos antes del tiempo indicado"
        },
        {
          "paso": 4,
          "accion": "Escurrir la pasta reservando 1/2 taza del agua de cocción",
          "tiempo_estimado": "1 min",
          "tip": "El agua de pasta ayudará a unir todos los ingredientes"
        },
        {
          "paso": 5,
          "accion": "Mezclar pasta caliente con tomates, mozzarella, albahaca y aceite de oliva",
          "tiempo_estimado": "2 min", 
          "tip": "El calor de la pasta derretirá ligeramente la mozzarella"
        }
      ],
      "informacion_nutricional": {
        "calorias_por_porcion": 485,
        "proteinas_g": 22,
        "carbohidratos_g": 58,
        "grasas_g": 18
      },
      "tags": ["vegetariano", "italiano", "rapido", "saludable"],
      "nivel_dificultad": "principiante",
      "consejos_chef": [
        "Usa mozzarella de búfala para un sabor más intenso",
        "Agrega un toque de pimienta negra recién molida al final"
      ],
      "variaciones": [
        "Versión con proteína: agregar pollo a la plancha cortado en tiras",
        "Versión vegana: sustituir mozzarella por queso vegano o aguacate"
      ]
    }
    // ... 4 recetas adicionales siguiendo la misma estructura
  ]
}
```

**Análisis del Ejemplo:**
- Utiliza 100% de ingredientes detectados
- Tiempo total dentro del límite del usuario (30 min)
- Nivel de dificultad apropiado (intermedio-principiante)
- Instrucciones claras y ejecutables
- Información nutricional balanceada
- Tips profesionales que agregan valor
- Variaciones que amplían opciones del usuario

---

**Notas del Documento:**
- Este PRD define los requisitos completos para la funcionalidad core de la aplicación
- La implementación inicial se enfocará en ingredientes básicos comunes (v1.0)
- Las integraciones con APIs externas requerirán evaluación de costos y límites de uso
- Se recomienda implementar sistema de cache local para reducir llamadas a APIs
- El modelo de reconocimiento de imágenes puede entrenarse específicamente con dataset culinario para mejorar precisión
- Considerar implementación offline para funcionalidad básica en caso de conectividad limitada