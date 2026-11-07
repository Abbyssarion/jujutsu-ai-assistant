# Resumen rápido: Introducción a Microsoft Foundry IQ

Este módulo explica cómo **Foundry IQ** da a los agentes una **capa de conocimiento administrada y reutilizable** para responder con información empresarial y citas.

- **¿Qué es Foundry IQ?**
  - La **capa de conocimiento administrada** de Microsoft Foundry. Conecta datos estructurados y no estructurados de sistemas empresariales y de la web, y los pone a disposición de los agentes mediante **bases de conocimiento reutilizables**.
  - Los **modelos** razonan, las **herramientas** actúan y **Foundry IQ** aporta información que no estaba en el entrenamiento del modelo.
  - Está construido sobre un recurso de **Azure AI Search**. La identidad administrada del proyecto necesita el rol **Search Index Data Reader** en el servicio de búsqueda.

- **Componentes:**
  - **Base de conocimiento (knowledge base):** recurso de nivel superior que agrupa fuentes y controla el comportamiento de recuperación; ofrece una **interfaz única** de recuperación al agente. Incluye un modelo generativo para la recuperación agéntica y prompts para priorizar fuentes y guiar respuestas.
  - **Fuente de conocimiento (knowledge source):** conexión a contenido **indexado** o **remoto**: índices de Azure AI Search, Blob Storage, SharePoint, OneLake, web pública, Azure SQL, **Work IQ** de Microsoft 365 Copilot...
  - **Recuperación agéntica (agentic retrieval):** **planea** búsquedas (divide la pregunta en subconsultas), busca en varias fuentes en paralelo, **rankea** y devuelve una respuesta unificada con **referencias**.

- **¿Por qué usarlo?**
  En lugar de un pipeline de RAG por agente (duplicando procesamiento, embeddings, índices, permisos y monitoreo), Foundry IQ centraliza el conocimiento por **dominio de negocio** ("Políticas de finanzas", "Instalaciones") y lo **comparte** entre agentes. Una mejora en la base beneficia a todos.

- **Capacidades:** chunking, embeddings y extracción de metadatos automáticos; búsqueda por palabra clave, vectorial o **híbrida**; coordinación entre fuentes; **citas**; respeto de **permisos** del usuario (y etiquetas de Microsoft Purview en fuentes compatibles).

- **Planear una base de conocimiento:** alcance, autoridad (fuente de verdad), frescura, metadatos, calidad del contenido y acceso. Agrupa fuentes que pertenecen juntas: meter todo en una sola base vuelve la recuperación menos precisa.

- **Conectar un agente:**
  1. Crear/conectar Azure AI Search con recuperación agéntica.
  2. Crear la base de conocimiento y sus fuentes.
  3. Crear o elegir un agente con un modelo desplegado.
  4. Agregar la base como **herramienta MCP**.
  5. Escribir **instrucciones**: cuándo recuperar, usar la evidencia, citar y qué hacer si no hay información.
  6. Probar en el Playground: respuestas, citas y actividad de herramientas.
  - **Evaluar en dos etapas:** recuperación (¿evidencia relevante, vigente y autorizada?) y respuesta (¿fundamentada, relevante, completa y bien citada?).

> [!TIP]
> "Varios agentes deben compartir el mismo conocimiento empresarial con permisos y citas, sin construir un RAG para cada uno" → **Foundry IQ**.
