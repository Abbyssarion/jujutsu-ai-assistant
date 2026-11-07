# Resumen rápido: Introducción a los conceptos de computer vision

La visión por computadora es el conjunto de tareas y técnicas en las que el software procesa entrada visual: imágenes, videos o cámaras en vivo.

- **Tareas de visión:**
  - **Clasificación de imágenes:** predice una etiqueta para toda la imagen (báscula que reconoce manzana, naranja o plátano).
  - **Detección de objetos:** encuentra varios objetos y su ubicación con **bounding boxes**.
  - **Segmentación semántica:** clasifica **cada píxel** según el objeto al que pertenece (máscaras).
  - **Análisis contextual de imágenes:** modelos **multimodales** que describen la escena ("una persona comiendo una manzana") o sugieren etiquetas.

- **Imágenes y procesamiento:**
  - Una imagen es un **arreglo de píxeles** de 0 (negro) a 255 (blanco). Filas × columnas = **resolución**.
  - Escala de grises = 1 capa; color = 3 **canales** (RGB).
  - **Filtros:** definidos por **kernels** (matrices de pesos, ej. 3×3) que se **convolucionan** sobre la imagen. Ejemplo: el **filtro Laplace** resalta bordes. Los valores fuera de 0–255 se ajustan y se usa **padding** en los bordes.

- **Redes neuronales convolucionales (CNN):**
  - Los kernels empiezan con pesos aleatorios y generan **mapas de características (feature maps)**.
  - **Pooling** reduce el tamaño de los mapas; se **aplanan** (flatten) y pasan a una **red totalmente conectada**.
  - La capa de salida usa **softmax** → probabilidades por clase, ej. `[0.2, 0.5, 0.3]`.
  - Entrenamiento: se calcula la **pérdida** (loss) y se ajustan pesos durante varias **épocas**.

- **Vision Transformers (ViT) y modelos multimodales:**
  - ViT divide la imagen en **parches**, los convierte en vectores y usa **atención** para relacionarlos (color, forma, textura).
  - Multimodal: combina codificadores de visión y de lenguaje con **atención cruzada (cross-modal attention)** en un espacio vectorial compartido; por eso puede describir imágenes que nunca vio.

- **Generación de imágenes:**
  - Modelos de **difusión**: empiezan con píxeles aleatorios (ruido) y lo eliminan iterativamente, comparando con el prompt en cada paso.
  - **Video:** además debe respetar el comportamiento físico y la progresión temporal.

> [!TIP]
> Palabras clave del examen: "ubicación" → detección; "píxel" → segmentación; "describir/etiquetar escena" → multimodal; "crear imagen a partir de texto" → difusión / modelo generativo.
