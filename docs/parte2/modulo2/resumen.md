# Resumen rápido: Introducción a la IA generativa y los agentes en Azure

Este módulo te enseña a **elegir, desplegar y usar modelos** en Microsoft Foundry y a **crear agentes** que puedas llamar desde código.

- **Catálogo de modelos:**
  - Dos grupos: **modelos vendidos directamente por Azure** (hospedados por Microsoft, SLAs empresariales, integración profunda) y **modelos de socios y la comunidad** (open source o del proveedor, ideales para experimentar o casos especializados).
  - Cada ficha incluye capacidades, **benchmarks**, tareas soportadas, opciones de fine-tuning y documentación de IA responsable (**model cards**).
  - **Familias** comunes: GPT-5.x (razonamiento, agentes, "niveles de pensamiento"), Claude Opus/Sonnet (agentes complejos, código, contexto largo), Mistral Large 3 (multilingüe, eficiente), GPT-4.1 (rápido, baja latencia, alto volumen).
  - **Modelos fundacionales:** grandes modelos preentrenados que se despliegan directo o se ajustan (fine-tuning).

- **Elegir un modelo:** según **tarea, carga de trabajo y restricciones**. Si el caso está bien definido (idioma, PII, OCR), considera una **Foundry Tool** en lugar de un modelo del catálogo.
  - Compara con **leaderboards** (calidad, seguridad, throughput) y **Benchmarks → Try with your own data**.
  - Métricas de NLP (exactitud, precisión, recall, F1) y asistidas por IA (groundedness, relevancia, coherencia, fluidez, similitud).
  - **Evaluadores** de seguridad: detectan contenido dañino, sesgo, violencia, autolesiones (detectan, no corrigen).

- **Desplegar modelos:**
  - Parámetros: **tipo de despliegue** (standard, global batch, provisioned throughput), **versión del modelo** y límite de **TPM** (tokens por minuto), que también define el RPM.
  - **Throttling:** al acercarte al límite recibes errores; baja `max_output_tokens` o reduce peticiones concurrentes.
  - Al desplegar: se asigna cómputo, se crea el endpoint, se fija la configuración y se activa el monitoreo.

- **Usar un modelo:**
  - **Playground:** configura **temperatura**, **máximo de tokens de salida** e **instrucciones de sistema**; genera código que usa la **Responses API**.
  - **System prompt** = comportamiento, tono y límites; **user prompt** = la petición.
  - **Cliente ligero:** un solo archivo Python que captura la entrada, llama al endpoint y muestra la respuesta.

- **Crear un agente:**
  - **Modelo + instrucciones + herramientas (+ conocimiento)**. *Tools = acciones; knowledge = contexto*.
  - Se guarda como componente reutilizable y versionado.
  - Desde código: `AIProjectClient` → `agents.get(...)` → `get_openai_client()` → `responses.create(..., agent_reference)`.

> [!TIP]
> "¿Qué parámetro hace las respuestas más creativas?" → **temperatura** alta. "¿Qué parámetro evita respuestas demasiado largas y throttling?" → **max output tokens**.
