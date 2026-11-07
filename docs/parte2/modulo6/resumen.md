# Resumen rápido: Introducción a la extracción de información con IA en Azure

Este módulo enseña a usar **Azure Content Understanding en Foundry Tools** para extraer información estructurada de documentos, imágenes, audio y video.

- **¿Qué es Content Understanding?**
  Servicio que extrae **datos estructurados** de contenido no estructurado (formularios, recibos, facturas, grabaciones). Va más allá del OCR: usa un **esquema** para mapear valores a campos con significado, **aunque las etiquetas cambien o no existan** ("Invoice No.", "Factura #" o un número sin etiqueta → `InvoiceNumber`).

- **Flujo de procesamiento:**
  **Ingesta** → **Análisis con IA** (OCR, reconocimiento de voz, comprensión de lenguaje, modelos multimodales) → **Salida estructurada** (JSON + Markdown).

- **Conceptos clave:**
  - **Esquema:** qué extraer y con qué estructura; soporta campos anidados (ej. `Items` con descripción, precio unitario, cantidad y total por línea).
  - **Analizador (analyzer):** unidad que recibe la entrada, aplica IA con un esquema y produce JSON predecible. **Prediseñados** (prebuilt) o **personalizados**.
  - **Analizadores prediseñados:** `prebuilt-invoice`, `prebuilt-imageSearch`, `prebuilt-audioSearch`, `prebuilt-videoSearch`, entre otros.
  - **Campos:** tipo (`string`, `date`, `number`...), valor (`valueString`, `valueDate`) y **confianza**.

- **Tipos de contenido:**
  - **Documentos:** facturas, recibos, formularios.
  - **Imágenes:** ej. contar asistentes presenciales y remotos en una foto de sala de juntas.
  - **Audio:** transcripción + campos (quién llamó, resumen, acciones solicitadas, número de devolución de llamada).
  - **Video:** asistencia por intervalos, quién habló, resumen de la discusión, acciones asignadas.

- **Portal de Foundry:** sube un archivo, elige un analizador, revisa campos detectados, transcripciones y el JSON, sin código.

- **SDK de Python:**
  - `pip install azure-ai-contentunderstanding`
  - `ContentUnderstandingClient(endpoint, AzureKeyCredential(key))` con endpoint `https://<recurso>.services.ai.azure.com/`
  - `begin_analyze(analyzer_id=..., inputs=[...])` inicia una **operación de larga duración (LRO)**; `poller.result()` espera (el SDK hace el *polling*).
  - Resultado: `result.contents[i].markdown` y `.fields`.

> [!TIP]
> "Extraer campos de documentos, imágenes, audio **y** video con un solo servicio" → **Content Understanding**. Es la respuesta a todas las habilidades del dominio *"Implement AI solutions for information extraction"*.
