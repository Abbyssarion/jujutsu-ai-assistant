# Resumen rápido: Introducción a los conceptos de generación aumentada por recuperación (RAG)

El RAG ayuda a que las aplicaciones de IA generativa produzcan respuestas **fundamentadas (grounded)** en información relevante.

- **El problema:** un modelo responde con patrones de su entrenamiento y con el contexto del prompt. Tiene tres limitaciones:
  - **Límites de conocimiento:** no conoce información privada (catálogos, políticas).
  - **Frescura:** lo aprendido se desactualiza.
  - **Verificabilidad:** puede dar una respuesta segura pero sin respaldo.

- **La solución (RAG):**
  - **Recuperación (retrieval):** buscar en fuentes seleccionadas la información relevante.
  - **Generación aumentada:** agregarla al prompt como contexto y pedir al modelo que responda con base en ella.
  - El resultado es una **respuesta fundamentada** que puede incluir **citas**.
  - **El RAG no cambia los parámetros del modelo:** si cambian los documentos, solo actualizas el índice.

- **Preparar los datos (pipeline de indexación):**
  1. **Ingesta:** cargar, extraer, limpiar y agregar **metadatos** (título, URL, categoría, permisos, fecha).
  2. **Chunking:** dividir en fragmentos enfocados, con un poco de **traslape**. Muy grandes = ruido y tokens; muy pequeños = pierden contexto.
  3. **Embeddings:** un modelo de embeddings convierte cada fragmento en un vector.
  4. **Índice:** guardar fragmentos, vectores y metadatos. Búsqueda **por palabras clave**, **vectorial** o **híbrida**.
  - El índice se mantiene: agregar, actualizar y eliminar contenido.

- **Recuperar y generar:**
  1. El usuario envía el prompt.
  2. Se busca en el índice (la consulta se vectoriza con el **mismo** modelo de embeddings).
  3. Se agrega el contexto al prompt (filtros por metadatos, límite de resultados, ranking).
  4. El modelo genera una respuesta fundamentada con citas.
  - Meta: recuperar **el conjunto más pequeño de contenido suficiente y relevante**.
  - Los documentos recuperados son **datos, no instrucciones** (protección contra *prompt injection*).

- **Evaluar el RAG:**
  - **Recuperación:** relevancia, cobertura, ranking, seguridad y frescura.
  - **Generación:** groundedness, relevancia, completitud, calidad de citas e incertidumbre apropiada.
  - **Conjunto de pruebas:** preguntas realistas, pasajes esperados, criterios de aceptación y casos difíciles.
  - Balancear **calidad, latencia y costo**.

> [!TIP]
> Si el contenido correcto **no se recupera**, cambiar el prompt no lo arregla: hay que mejorar las fuentes, el chunking, los metadatos o la estrategia de búsqueda.
