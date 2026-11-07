# Resumen rápido: Introducción a los conceptos de extracción de información con IA

La extracción de información combina varias técnicas de IA para sacar **valores de datos** de documentos, imágenes y otras fuentes no estructuradas.

- **Definición:**
  Un sistema completo usa **visión por computadora** para detectar texto en imágenes y **machine learning o IA generativa** para mapear ese texto a campos específicos. Ejemplo: procesar recibos de gastos y extraer Proveedor, Fecha, Subtotal, Impuesto y Total.

- **Dos etapas principales:**
  1. **OCR:** detectar y extraer el texto de las imágenes.
  2. **Identificación y mapeo de valores:** asignar ese texto a campos de datos.

- **Cómo elegir el enfoque:**
  - *Características del documento:* consistencia del formato (plantillas vs. ML), volumen y precisión requerida (humano en el ciclo).
  - *Infraestructura:* seguridad y privacidad, poder de cómputo, latencia, escalabilidad e integración.
  - Servicios recomendados: **Azure Document Intelligence** y **Azure Content Understanding** en Foundry Tools.

- **OCR en 5 etapas:**
  1. Adquisición de la imagen (foto, escáner, PDF).
  2. Preprocesamiento: reducción de ruido, ajuste de contraste (umbral adaptativo), corrección de inclinación (*deskew*), resolución.
  3. Detección de regiones de texto: análisis de layout, bloques, orden de lectura, clasificación de regiones.
  4. Reconocimiento de caracteres: extracción de rasgos, comparación de patrones, análisis de contexto, **puntajes de confianza**.
  5. Generación de salida: compilación del texto, preservación de formato, **mapeo de coordenadas** y validación.

- **Extracción y mapeo de campos:**
  - El OCR dice **qué texto existe**; la extracción de campos dice **qué significa y a dónde pertenece**.
  - Enfoques: **basado en plantillas** (reglas, regex), **machine learning** (multimodal: texto + visual + posición) e **IA generativa** (le das al LLM el texto y un **esquema**).
  - **Pares clave-valor**, tablas (filas, columnas, encabezados), normalización (fechas ISO, monedas) y validación (formato, rangos, campos requeridos, validación cruzada: la suma de partidas = total).

> [!TIP]
> "OCR" = leer texto. "Extracción de campos" = entender qué es cada dato. El examen te pide distinguirlos.
