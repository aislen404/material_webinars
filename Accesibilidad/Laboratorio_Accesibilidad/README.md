# Laboratorio de Accesibilidad — Versión 2 (Refinado Final)

Este proyecto es un **dashboard de accesibilidad** pensado para formación y demostraciones en vivo. Incluye chequeos automáticos heurísticos, comparador, calculadora de contraste, mapa de foco y un generador de prompts para IA.

## ✨ Novedades de la v2
- **Chequeos extra**:
  - `lang` en `<html>`
  - Redundancias ARIA e **roles no válidos**
  - **IDs duplicados**
  - Labels vacíos o `for` apuntando a IDs inexistentes
  - Campos `required` sin `aria-required` (y viceversa)
  - Elementos interactivos con `tabindex="-1"`
  - Textos de enlace repetidos con **destinos diferentes**
  - Encabezados huérfanos (`h3` antes de `h2`, etc.)
- **Mapa de foco estimado** (orden de tabulación)
- **Calculadora de contraste AA/AAA**
- **Exportar informe** en **HTML** y **JSON**
- **Tema claro/oscuro**

## 🧭 Secciones
- **Chequeos básicos**: Editor HTML/CSS, análisis, previsualización con simulador, issues y foco.
- **Panel IA (prompt)**: Genera un prompt WCAG 2.2 AA listo para ChatGPT/Gemini.
- **Comparar ejemplos**: Carga dos páginas en paralelo para contrastar.
- **Ejemplos rápidos**: Snippets listos para cargar en el editor.

## 🚀 Uso rápido
1. Abre `index.html` en tu navegador.
2. Pega tu HTML/CSS y pulsa **Analizar**.
3. Revisa **Resultados** y el **Mapa de foco**.
4. Ajusta contraste con la **calculadora** si hace falta.
5. **Genera el prompt** y úsalo en tu LLM para un informe extendido.
6. Exporta **HTML/JSON** si quieres documentar o integrar con otras herramientas.
7. Usa el **Comparador** para mostrar antes/después de tus cambios.

> Recuerda: estos chequeos son heurísticos. Verifica siempre con WAVE, Accessibility Insights y Lighthouse, y realiza pruebas manuales con teclado y lector de pantalla.
