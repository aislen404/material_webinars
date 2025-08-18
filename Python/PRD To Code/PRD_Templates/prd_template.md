# 📄 Plantilla PRD Híbrida (Producto + Prompt/IA)

> **Propósito**: Documento vivo para definir, validar y evolucionar un producto o prompt basado en IA.  
> **Formato**: Markdown versionado en Git (controlado en PRs para trazabilidad).  
> **Uso**: Sustituye `{{placeholders}}`, elimina lo que no aplique, mantén lenguaje claro, medible y accionable.  

---

## 1. Información General
- **Título / Nombre del Producto o Prompt**: {{...}}  
- **Versión:** [v1.0]  
- **Fecha de creación / última actualización**: {{DD/MM/AAAA}}  
- **Autor:** {{...}}  
- **Resumen ejecutivo**: {{2–3 líneas sobre propósito y objetivo principal}}

---

## 2. Visión y Contexto
- **Visión**: {{frase clara sobre el cambio esperado}}  
- **Problema a resolver**: {{dolor actual con datos o ejemplos concretos}}  
- **Oportunidad / Valor**: {{beneficio esperado para usuarios y/o negocio}}  
- **Audiencia objetivo**:  
  - Usuario primario: {{perfil, contexto}}  
  - Usuario secundario: {{si aplica}}  
  - Nivel técnico requerido: {{básico/intermedio/avanzado}}  
- **Stakeholders**: {{quiénes intervienen y por qué les importa}}  
- **Caso de uso principal**: {{escenario específico con narrativa breve}}

---

## 3. Objetivos y Métricas
- **Objetivo principal**: {{qué debe lograr el producto/prompt}}  
- **Objetivos secundarios**:  
  - {{objetivo 1}}  
  - {{objetivo 2}}  
- **KPIs / Métricas de éxito**:  
  - Precisión (ej: ≥90% de outputs correctos)  
  - Consistencia (coherencia en 9/10 ejecuciones)  
  - Tiempo de respuesta (ej: <2s)  
  - Satisfacción del usuario (ej: ≥4/5 en encuestas)  
  - Otros (retención, NPS, activación, etc.)  

---

## 4. Personas
### Persona A – {{nombre corto}}
- Perfil: {{rol, edad, contexto}}  
- Necesidades: {{bullets}}  
- Frustraciones: {{bullets}}  
- Escenario típico: {{narrativa breve}}

*(Repetir para 2–3 personas clave)*

---

## 5. Alcance
### In scope
- {{funcionalidad/práctica incluida}}  

### Out of scope
- {{lo que se deja fuera del MVP}}  

> **Nota**: Priorizar impacto/viabilidad y evitar scope creep.  

---

## 6. Historias de Usuario y Especificaciones de Prompt
- **Formato HU**: Como {{persona}} quiero {{necesidad}} para {{valor}}.  
- **Criterios de aceptación (sintaxis Gherkin)**:  
  - Given {{contexto}} When {{acción}} Then {{resultado medible}}  

**Ejemplo**:  
- HU-1: Como {{usuario}} quiero {{buscar por ingredientes}} para {{aprovechar mi despensa}}.  
  - **Criterios**:  
    - Given que introduzco "huevo, tomate"  
      When pulso "Buscar"  
      Then veo al menos 3 recetas disponibles.  

**Prompt asociado (estructura base):**  
```
Actúa como [ROL]. Tu tarea es [TAREA].  
Considera [CONTEXTO].  
Formato de respuesta: [FORMATO]
```

- **Variables dinámicas**: {{lista de placeholders como {usuario}, {contexto}, etc.}}  
- **Instrucciones especiales**: {{si aplica}}  

---

## 7. Requisitos Funcionales
- **Entrada (Input)**:  
  - Tipo: texto, imagen, código, etc.  
  - Formato esperado: {{estructura específica}}  
  - Longitud mínima/máxima: {{...}}  
  - Idioma(s) aceptados: {{...}}  
  - Ejemplos de entrada válida:  
    ```
    [Ejemplo 1]
    [Ejemplo 2]
    ```
- **Salida (Output)**:  
  - Tipo: texto, análisis, JSON, código…  
  - Formato requerido: {{estructura, estilo}}  
  - Longitud esperada: {{...}}  
  - Elementos obligatorios: {{lista}}  
  - Ejemplos de salida deseada:  
    ```
    [Ejemplo 1]
    [Ejemplo 2]
    ```
- **Comportamiento esperado**: tono, estilo, nivel de detalle, estructura.  
- **Requisitos priorizados (MoSCoW)**:  
  - Must → {{imprescindibles}}  
  - Should → {{importantes}}  
  - Could → {{deseables}}  
  - Won’t (MVP) → {{excluidos ahora}}  

---

## 8. Requisitos No Funcionales
- **Rendimiento**: ej: respuesta <500ms en búsquedas locales  
- **Seguridad / Privacidad**: cumplimiento GDPR, gestión de secretos, mínimos de autenticación  
- **Accesibilidad**: soporte teclado, contraste, alt text  
- **Confiabilidad**: fallback si falla API/LLM  
- **Observabilidad**: logs mínimos, métricas, healthcheck  
- **Restricciones**: contenido prohibido, limitaciones técnicas, restricciones de tiempo  
- **Manejo de casos límite**:  
  - Entradas ambiguas → {{respuesta esperada}}  
  - Información insuficiente → {{qué debe hacer}}  
  - Solicitudes fuera de alcance → {{respuesta adecuada}}  

---

## 9. Flujo de Usuario / Experiencia
1. Paso 1 → {{input del usuario}}  
2. Paso 2 → {{procesamiento del sistema / IA}}  
3. Paso 3 → {{output esperado}}  

*(Agregar diagramas si aplica)*  

---

## 10. Validación y Pruebas
- **Criterios de aceptación** (checklist):  
  - [ ] El output es relevante al objetivo  
  - [ ] Mantiene el formato requerido  
  - [ ] Tono y estilo consistentes  
  - [ ] Manejo correcto de casos límite  
  - [ ] Otros específicos {{...}}  

- **Casos de prueba**:  
| ID | Entrada de Prueba | Resultado Esperado | Estado |  
|----|-------------------|-------------------|--------|  
| TC01 | {{input}} | {{output esperado}} | [ ] |  
| TC02 | {{input}} | {{output esperado}} | [ ] |  

- **Escenarios de error**:  
  - Error 1: {{descripción}} → Respuesta esperada: {{...}}  
  - Error 2: {{descripción}} → Respuesta esperada: {{...}}  

---

## 11. Riesgos, Suposiciones y Dependencias
- Riesgos + mitigación  
- Suposiciones clave  
- Dependencias externas (API, LLM, dataset, equipo externo)  

---

## 12. Roadmap y Evolución
- **MVP**: {{alcance + fecha objetivo}}  
- **v1.1, v1.2…**: mejoras incrementales  
- **Versionado**: historial de cambios (ej: v1.0 inicial, v1.1 fixes, v2.0 cambio mayor)  
- **Feedback y mejoras**:  
  - Fuentes de feedback: {{usuarios, QA, métricas}}  
  - Proceso de actualización: {{cómo se revisa e implementa}}  
  - Frecuencia de revisión: {{ej: mensual/trimestral}}  

---

## 13. Métricas de Rendimiento
- KPI 1: {{definición + target + fuente de datos}}  
- KPI 2: {{…}}  
- KPI 3: {{…}}  

---

## 14. Implementación
- **Prompt final (versión lista para usar)**  
- **Variaciones**:  
  - Versión corta (casos simples)  
  - Versión extendida (casos complejos)  
  - Versión especializada (dominios concretos)  

---

## 15. Glosario y Anexos
- **Glosario de términos clave**: {{definiciones}}  
- **Referencias**: {{fuentes, documentación relacionada}}  
- **Ejemplos completos**:  
```
Input: [ejemplo completo]  
Output: [ejemplo completo]  
Análisis: [por qué funciona bien este ejemplo]  
```

---
