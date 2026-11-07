# Tema 2: Reconocimiento óptico de caracteres (OCR) — Fundamentos técnicos

### Descripción
El **OCR** convierte automáticamente el texto visual de imágenes (documentos escaneados, fotos, PDFs, capturas de pantalla, notas a mano) en texto editable y buscable. Es el primer eslabón de cualquier solución de extracción de información: si el OCR falla, todo lo que sigue falla.

Analogía: el OCR es como una persona que transcribe un documento viejo. Primero lo limpia y endereza, luego ubica dónde hay texto, después reconoce letra por letra (ayudándose del contexto para las letras borrosas) y al final lo pasa en limpio respetando párrafos.

### Aspectos Clave: el pipeline de 5 etapas

1. **Adquisición de la imagen:**
   - Fuentes: foto del celular, escáner, cuadro de video, página PDF renderizada como imagen.
   - **La calidad de la imagen en esta etapa impacta directamente la precisión final.**

2. **Preprocesamiento y mejora de imagen:**

   | Técnica | Qué hace | Métodos clásicos | Métodos con ML |
   |---|---|---|---|
   | Reducción de ruido | Quita manchas, polvo e imperfecciones | Filtros gaussianos, de mediana | Autoencoders de *denoising*, CNN |
   | Ajuste de contraste / binarización | Separa texto del fondo | Ecualización de histograma, **umbral adaptativo** | Modelos que aprenden parámetros por tipo de documento |
   | Corrección de inclinación (*deskew*) | Endereza las líneas de texto | Transformada de Hough, perfiles de proyección | CNN de regresión que predicen el ángulo |
   | Optimización de resolución | Ajusta la resolución ideal | Interpolación bicúbica, Lanczos | Súper resolución (GANs) |

3. **Detección de regiones de texto:**
   - **Análisis de layout:** distingue texto, imágenes, gráficos y espacios en blanco (U-Net, Mask R-CNN, LayoutLM).
   - **Identificación de bloques:** agrupa caracteres en palabras, líneas y párrafos.
   - **Orden de lectura:** izquierda a derecha y de arriba abajo en español; crítico en documentos a dos columnas.
   - **Clasificación de regiones:** encabezados, cuerpo, pies de foto, tablas.

4. **Reconocimiento y clasificación de caracteres:**
   - **Extracción de rasgos:** forma, tamaño, bucles, extremos, intersecciones (hoy lo hacen CNNs a partir de píxeles).
   - **Comparación de patrones:** clasificadores (SVM, k-NN, redes como LeNet, ResNet).
   - **Análisis de contexto:** usa palabras vecinas para corregir: n-gramas, diccionarios con **distancia de Levenshtein**, modelos de lenguaje. "Fact0ra" → "Factura".
   - **Puntaje de confianza:** probabilidad por carácter o palabra (softmax).

5. **Generación de salida y posprocesamiento:**
   - **Compilación** de caracteres en palabras y oraciones.
   - **Preservación del formato:** párrafos, saltos de línea, espacios.
   - **Mapeo de coordenadas:** guarda la posición exacta (bounding box) de cada elemento. Fundamental para la extracción de campos: la posición de "12345" ayuda a saber si es número de factura o teléfono.
   - **Validación de calidad:** revisión ortográfica y gramatical.

### Práctica 1: OCR local con Tesseract
```python
# Instala Tesseract: https://github.com/tesseract-ocr/tesseract (Windows: instalador UB Mannheim)
# pip install pytesseract opencv-python
import cv2
import pytesseract

imagen = cv2.imread("recibo.jpg")
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)                       # 1. escala de grises
sin_ruido = cv2.medianBlur(gris, 3)                                   # 2. reducción de ruido
binaria = cv2.adaptiveThreshold(sin_ruido, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 31, 15)            # 3. umbral adaptativo

datos = pytesseract.image_to_data(binaria, lang="spa", output_type=pytesseract.Output.DICT)
for palabra, conf, x, y in zip(datos["text"], datos["conf"], datos["left"], datos["top"]):
    if palabra.strip():
        print(f"{palabra:20s} confianza={conf:>5}  posición=({x},{y})")
```
- **Explicación:**
  - Los pasos 1–3 son el **preprocesamiento** del pipeline.
  - `image_to_data` devuelve cada palabra con su **confianza** y **coordenadas** (etapas 4 y 5).
  - `lang="spa"` requiere el paquete de idioma español de Tesseract.

### Práctica 2: OCR en la nube con un modelo multimodal de Foundry
```python
import os, base64
from openai import OpenAI

client = OpenAI(base_url=os.environ["AZURE_OPENAI_ENDPOINT"], api_key=os.environ["FOUNDRY_KEY"])

with open("recibo.jpg", "rb") as f:
    imagen_b64 = base64.b64encode(f.read()).decode()

respuesta = client.responses.create(
    model=os.environ["FOUNDRY_MODEL_NAME"],   # deployment multimodal, ej. gpt-4.1-mini
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "Transcribe todo el texto de este recibo respetando las líneas."},
            {"type": "input_image", "image_url": f"data:image/jpeg;base64,{imagen_b64}"},
        ],
    }],
)
print(respuesta.output_text)
```
- **Explicación:** un modelo multimodal hace OCR "de pasada", pero **no devuelve coordenadas ni confianza** por palabra. Para eso, y para extracción a escala, se usan **Azure Document Intelligence** o **Content Understanding** ([Parte 2, Módulo 6](../../parte2/modulo6/tema1.md)).

### Para el examen
- "Convertir texto de imágenes escaneadas en texto buscable" → **OCR**.
- "Obtener el total, la fecha y el proveedor de un recibo" → **extracción de campos** (OCR + mapeo), en Foundry: **Content Understanding**.
