# Tema 2: Tutorial de implementación con el SDK de Python de un modelo multimodal

**Objetivo:** Enviar imágenes (por URL y desde un archivo local) a un modelo multimodal desplegado en Foundry y obtener descripciones, respuestas y datos estructurados.

Lectura oficial: [Modelos multimodales para análisis de imágenes – Microsoft Learn](https://learn.microsoft.com/es-es/training/modules/get-started-vision-azure/2-vision-enabled-models?pivots=text)

## Paso a Paso:

### 1. Probar en el Playground
- Despliega `gpt-4.1-mini` (si no lo tienes).
- En el Playground de chat, sube una foto y pregunta "¿Qué animal es y en qué hábitat vive?".
- Selecciona **View code** para ver el código equivalente.

### 2. Preparar el entorno
```bash
pip install openai python-dotenv
```
`.env`:
```bash
ENDPOINT=https://<recurso>.openai.azure.com/openai/v1/
FOUNDRY_KEY=<tu-llave>
MODEL_NAME=gpt-4.1-mini          # nombre de TU deployment
```

### 3. Analizar una imagen por URL (`vision_url.py`)
```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("FOUNDRY_KEY"), base_url=os.getenv("ENDPOINT"))

image_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/dog.jpg"

response = client.responses.create(
    model=os.getenv("MODEL_NAME"),
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "¿Qué hay en esta imagen? Responde en 3 viñetas."},
            {"type": "input_image", "image_url": image_url},
        ],
    }],
)
print(response.output_text)
```
- **Explicación:**
  - Un mismo mensaje de `role: user` lleva una **lista de partes**: `input_text` (la pregunta) e `input_image` (la imagen).
  - `model` es el **nombre del deployment**, no el nombre del modelo base.
  - `output_text` junta el texto de la respuesta.

### 4. Analizar una imagen local en base64 (`vision_local.py`)
```python
import os, base64, mimetypes
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("FOUNDRY_KEY"), base_url=os.getenv("ENDPOINT"))

def imagen_a_data_url(ruta):
    tipo = mimetypes.guess_type(ruta)[0] or "image/jpeg"
    with open(ruta, "rb") as f:
        return f"data:{tipo};base64,{base64.b64encode(f.read()).decode()}"

response = client.responses.create(
    model=os.getenv("MODEL_NAME"),
    instructions="Eres un guía de safari. Responde en español de México, breve y didáctico.",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "Identifica el animal y da un dato curioso."},
            {"type": "input_image", "image_url": imagen_a_data_url("mi_foto.jpg")},
        ],
    }],
)
print(response.output_text)
```
- **Explicación:**
  - Para archivos locales, la imagen se codifica en **base64** dentro de un **data URL** (`data:image/jpeg;base64,...`).
  - `instructions` es el **system prompt** de la Responses API.

### 5. Extraer datos estructurados de una imagen (`vision_json.py`)
```python
import os, json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("FOUNDRY_KEY"), base_url=os.getenv("ENDPOINT"))

esquema = {
    "type": "object",
    "properties": {
        "animal": {"type": "string"},
        "cantidad": {"type": "integer"},
        "habitat": {"type": "string"},
        "en_peligro": {"type": "boolean"},
    },
    "required": ["animal", "cantidad", "habitat", "en_peligro"],
    "additionalProperties": False,
}

response = client.responses.create(
    model=os.getenv("MODEL_NAME"),
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "Analiza la foto y llena el esquema."},
            {"type": "input_image", "image_url": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/dog.jpg"},
        ],
    }],
    text={"format": {"type": "json_schema", "name": "analisis_safari", "schema": esquema, "strict": True}},
)
datos = json.loads(response.output_text)
print(datos["animal"], datos["cantidad"], datos["en_peligro"])
```
- **Explicación:**
  - Con **salidas estructuradas** (`json_schema` + `strict: True`) el modelo está obligado a devolver un JSON válido con esos campos. Ideal para integrar con bases de datos o APIs.

### 6. Varias imágenes en un mismo prompt
```python
content = [
    {"type": "input_text", "text": "Compara estas dos fotos de anaquel. ¿Qué productos faltan en la segunda?"},
    {"type": "input_image", "image_url": imagen_a_data_url("anaquel_lunes.jpg")},
    {"type": "input_image", "image_url": imagen_a_data_url("anaquel_viernes.jpg")},
]
```

## Errores comunes
| Error | Causa |
|---|---|
| `Invalid image` | URL no pública o base64 mal formado (falta `data:image/...;base64,`) |
| El modelo dice que no puede ver imágenes | El deployment no es multimodal |
| `DeploymentNotFound` | `MODEL_NAME` tiene el nombre del modelo y no el del deployment |

## Práctica oficial de Microsoft Learn
- [Ejercicio: Introducción a computer vision en Microsoft Foundry](https://learn.microsoft.com/es-es/training/modules/get-started-vision-azure/5-exercise)
- [Ejercicio: Explorar computer vision](https://learn.microsoft.com/es-es/training/modules/introduction-computer-vision/5b-exercise)
