# Resumen rápido: Introducción a la IA generativa y los agentes

Este módulo explica **cómo funcionan por dentro los LLMs**, cómo escribir **prompts** efectivos y qué es un **agente de IA**.

- **Modelos de lenguaje (LLM y SLM):**
  Codifican relaciones lingüísticas y semánticas entre palabras. Se entrenan para generar **completions** (continuaciones) a partir de **prompts**, como un "texto predictivo" muy poderoso: predicen el siguiente token más probable, lo agregan y repiten.

- **Tokenización:**
  El texto se parte en **tokens** (palabras, subpalabras como "des-" en "deshacer", signos de puntuación). Cada token tiene un **ID entero único**. Los LLMs actuales tienen vocabularios de cientos de miles de tokens.

- **Vectores y embeddings:**
  Cada token se representa como un **vector** (lista de números) de miles de dimensiones. Al inicio los valores son aleatorios; con el entrenamiento, el mecanismo de **atención** los ajusta según el contexto, y se convierten en **embeddings** que capturan significado.

- **Espacio vectorial:**
  Tokens con significado parecido tienen vectores que apuntan en **direcciones similares** ("perro" y "cachorro" están cerca; "patineta" está lejos). La cercanía se mide con **similitud coseno**.

- **Transformer:**
  - **Codificador (encoder):** crea embeddings aplicando **atención multi-cabeza** (*multi-head attention*).
  - **Decodificador (decoder):** usa esos embeddings para predecir el siguiente token. Durante el entrenamiento usa **atención enmascarada** (solo ve los tokens anteriores).
  - Origen: el paper *"Attention is all you need"* (2017).

- **Prompts:**
  - **System prompt:** define comportamiento, tono y restricciones; normalmente lo pone la aplicación.
  - **User prompt:** la pregunta o instrucción concreta del usuario.
  - **Historial de conversación:** la app reenvía (o resume) los mensajes anteriores para mantener contexto.
  - **RAG:** la app recupera documentos relevantes y los agrega al prompt para que la respuesta esté **fundamentada (grounded)**.
  - **Tips:** sé claro y específico, agrega contexto, da ejemplos y pide estructura (viñetas, tablas).

- **Agentes de IA:**
  Aplicaciones basadas en IA generativa que razonan, usan herramientas y actúan. Tres elementos:
  1. **Modelo** (el cerebro).
  2. **Instrucciones** (system prompt; su "descripción de puesto").
  3. **Herramientas:** de **conocimiento** (buscadores, bases de datos) y de **acción** (enviar correos, actualizar calendarios).

  Los **sistemas multiagente** reparten el trabajo entre agentes especializados que se coordinan mediante prompts.

> [!TIP]
> Pregunta típica: "¿Qué parte del agente define su rol y comportamiento?" → las **instrucciones** (system prompt). "¿Qué le permite consultar una base de datos o mandar un correo?" → las **herramientas**.
