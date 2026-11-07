# Resumen rápido: Introducción al análisis de texto en Azure

Este módulo muestra dos caminos para analizar texto en Foundry: **modelos de propósito general (LLMs)** y **Azure Language en Foundry Tools**, y cómo exponerlo a un agente con **MCP**.

- **Modelos de propósito general (LLMs):**
  - Hacen muchas tareas con un prompt, sin configuración ni entrenamiento.
  - Permiten refinar en la misma conversación y combinar tareas (traducir y luego resumir).
  - La salida depende de cómo escribas el prompt: entre más específico, más estructurado.
  - Tareas: extracción de frases clave, vinculación de entidades, sentimiento y minería de opiniones, resumen, traducción, clasificación, preguntas sobre un texto.

- **Azure Language en Foundry Tools:**
  - Analizadores especializados con salida **estructurada y determinista**, ideales para **pipelines automatizados**.
  - **Detección de idioma:** idioma, código ISO 639-1 y confianza ("¡Hola! Me llamo Josefina..." → Spanish, `es`, 1.00).
  - **Detección de PII:** nombres, teléfonos, correos, direcciones (y PHI); puede **redactar** (ocultar) el texto.
  - Se prueba en el portal en **Build → Models → AI services**.

- **Cliente en Python:**
  - Responses API con el SDK `openai`.
  - Azure Language con `azure-ai-textanalytics`: `TextAnalyticsClient` + `AzureKeyCredential`, métodos `detect_language()` y `recognize_pii_entities()` (devuelve `redacted_text` y `entities`).
  - Usa Azure Language cuando necesites resultados consistentes; la Responses API varía entre llamadas.

- **Azure Language con un agente (MCP):**
  - **MCP (Model Context Protocol):** estándar abierto para conectar agentes con herramientas y datos ("adaptador universal").
  - **Cliente MCP** = el agente; **servidor MCP** = el servicio que expone herramientas.
  - El **servidor MCP de Azure Language** expone NER, sentimiento, detección de idioma, etc. En el Playground agregas la herramienta *Azure Language in Foundry Tools* y la conectas con el nombre de tu recurso de Foundry (ya incluye acceso a Language).

> [!TIP]
> "Resultados consistentes en un pipeline automatizado" → **Azure Language**. "Flexibilidad y combinar tareas con lenguaje natural" → **LLM**.
