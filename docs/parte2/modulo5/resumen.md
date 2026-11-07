# Resumen rápido: Introducción a computer vision en Azure

Este módulo presenta las capacidades de visión en Foundry: **analizar imágenes** con modelos multimodales y **generar imágenes y video** con modelos generativos.

- **Modelos multimodales para análisis de imágenes:**
  - Aceptan más de un tipo de entrada (texto + imagen); describen imágenes y responden preguntas sobre ellas ("GPT con visión").
  - Modelos: **GPT-4.1 / 4.1-mini / 4.1-nano** (descripción, preguntas visuales, documentos, capturas, gráficas, diagramas), **serie GPT-5** (escenarios agénticos, salidas estructuradas, herramientas), modelos de socios.
  - Flujo: probar en el Playground subiendo una imagen → `pip install openai` → mensaje con partes `input_text` + `input_image` → `client.responses.create(...)` → `response.output_text`.
  - Las imágenes se envían como **URL** o **base64**.
  - El parámetro `model` es el **nombre del deployment**.

- **Modelos de generación de imágenes:**
  - **GPT-Image-1.5:** el más avanzado (texto a imagen, imagen a imagen, edición precisa); recomendado para proyectos nuevos.
  - **GPT-Image-1:** propósito general, sucesor de DALL-E; variaciones y edición.
  - **GPT-Image-1-Mini:** más barato y rápido.
  - **FLUX** (Black Forest Labs): familia open source de terceros.
  - Desde código: Responses API con `tools=[{"type": "image_generation"}]`; el resultado viene en **base64** en el elemento `image_generation_call`.

- **Modelos de generación de video:**
  - **Sora** (texto a video, también acepta imagen) y **Sora 2** (texto, imagen y video a video; **remix**; **genera audio**).
  - Únicos modelos nativos de video en Foundry.
  - Trabajo **asíncrono**: crear job → consultar estado → descargar (1–5 minutos).
  - Restricciones de IA responsable: personas reales, personajes con derechos de autor, contenido dañino.

> [!TIP]
> "Describir el contenido de una foto / responder preguntas sobre una imagen" → **modelo multimodal**. "Crear una imagen a partir de una descripción" → **GPT-Image / FLUX**. "Crear un clip de video" → **Sora**.
