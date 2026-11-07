# Tema 1: Tutorial de implementación con el SDK de Python de un modelo de Content Understanding

**Objetivo:** Extraer información estructurada de una factura con un analizador prediseñado, de un audio con `prebuilt-audioSearch` y crear un analizador personalizado con tu propio esquema.

Lectura oficial: [Extraer información de documentos – Microsoft Learn](https://learn.microsoft.com/es-es/training/modules/get-started-information-extraction/2-documents?pivots=text)

## Paso a Paso:

### 1. Preparar el recurso de Foundry
- Crea (o usa) un **recurso de Foundry** en una región que soporte Content Understanding.
- Asígnate el rol **Cognitive Services User** sobre el recurso (*Access control (IAM) → Add role assignment*). La documentación del SDK indica que es necesario **aunque seas Owner**.
- Content Understanding usa modelos de lenguaje por debajo. **Despliega**:
  - `gpt-4.1` y `text-embedding-3-large` → para analizadores como `prebuilt-invoice` y `prebuilt-receipt`.
  - `gpt-4.1-mini` y `text-embedding-3-large` → para `prebuilt-documentSearch`, `prebuilt-imageSearch`, `prebuilt-audioSearch`, `prebuilt-videoSearch`.
- La primera vez que abras Content Understanding en el portal de Foundry te pedirá asociar esos deployments como **predeterminados**. También se puede hacer por código con `client.update_defaults(...)` ([ejemplo oficial](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples/sample_update_defaults.py)).

### 2. Probar en el portal
- En el portal de Foundry abre Content Understanding, sube una factura, elige `prebuilt-invoice` y revisa los **campos detectados** y el **JSON**.

### 3. Preparar el entorno
```bash
pip install azure-ai-contentunderstanding python-dotenv
```
`.env`:
```bash
FOUNDRY_ENDPOINT=https://<recurso>.services.ai.azure.com/
FOUNDRY_KEY=<tu-llave>
```

### 4. Analizar una factura con un analizador prediseñado (`factura.py`)
```python
import os
from dotenv import load_dotenv
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.ai.contentunderstanding.models import AnalysisInput
from azure.core.credentials import AzureKeyCredential

load_dotenv()
client = ContentUnderstandingClient(endpoint=os.environ["FOUNDRY_ENDPOINT"],
                                    credential=AzureKeyCredential(os.environ["FOUNDRY_KEY"]))

url_factura = ("https://github.com/Azure-Samples/azure-ai-content-understanding-python/"
               "raw/refs/heads/main/data/invoice.pdf")

# 1) Iniciar el análisis: operación de larga duración (LRO)
poller = client.begin_analyze(analyzer_id="prebuilt-invoice",
                              inputs=[AnalysisInput(url=url_factura)])

# 2) Esperar el resultado (el SDK hace el polling por ti)
resultado = poller.result()

# 3) Leer Markdown y campos estructurados
contenido = resultado.contents[0]
print(contenido.markdown[:500])

for nombre in ["CustomerName", "InvoiceId", "InvoiceDate", "InvoiceTotal"]:
    campo = contenido.fields.get(nombre)
    if campo:
        print(f"{nombre:15s} = {campo.value}   (confianza: {campo.confidence})")
```
- **Explicación:**
  - `begin_analyze` **inicia** el trabajo y regresa un *poller*; `poller.result()` **espera** a que termine. Esto es una **operación de larga duración (LRO)**: con REST tendrías que consultar tú la URL `Operation-Location` hasta que el estado sea `Succeeded`.
  - Cada elemento de `contents` trae el **Markdown** (texto con estructura: títulos, tablas) y los **fields** con su valor, tipo y **confianza**.
  - En el JSON crudo verás campos como `"CustomerName": {"type": "string", "valueString": "MICROSOFT CORPORATION", "confidence": 0.95}`. La propiedad `.value` del SDK te da el valor sin importar el tipo.
  - Para un archivo local usa `client.begin_analyze_binary(analyzer_id=..., binary_input=open("factura.pdf","rb").read())`.

### 5. Extraer información de audio (`buzon_voz.py`)
```python
import os
from dotenv import load_dotenv
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.ai.contentunderstanding.models import AnalysisInput
from azure.core.credentials import AzureKeyCredential

load_dotenv()
client = ContentUnderstandingClient(endpoint=os.environ["FOUNDRY_ENDPOINT"],
                                    credential=AzureKeyCredential(os.environ["FOUNDRY_KEY"]))

poller = client.begin_analyze(
    analyzer_id="prebuilt-audioSearch",                         # para video: prebuilt-videoSearch
    inputs=[AnalysisInput(url="https://<tu-storage>/muestras/buzon.wav")],
)
resultado = poller.result()

for contenido in resultado.contents:
    print("=== TRANSCRIPCIÓN / MARKDOWN ===")
    print(getattr(contenido, "markdown", None))
    print("=== CAMPOS ===")
    print(getattr(contenido, "fields", None))
```
- **Explicación:** el mismo cliente y el mismo patrón sirven para **audio y video**; solo cambia el `analyzer_id`. El resultado incluye la **transcripción** y los campos que defina el analizador.

### 6. Crear un analizador personalizado con tu esquema (`analizador_buzon.py`)
Caso de Microsoft Learn: de cada mensaje de voz queremos *quién llama, resumen, acciones solicitadas, número de devolución y contacto alterno*.
```python
import os
from dotenv import load_dotenv
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.ai.contentunderstanding.models import (
    AnalysisInput, ContentAnalyzer, ContentFieldSchema, ContentFieldDefinition,
    ContentFieldType, GenerationMethod,
)
from azure.core.credentials import AzureKeyCredential

load_dotenv()
client = ContentUnderstandingClient(endpoint=os.environ["FOUNDRY_ENDPOINT"],
                                    credential=AzureKeyCredential(os.environ["FOUNDRY_KEY"]))

esquema = ContentFieldSchema(
    name="buzon_de_voz",
    description="Datos clave de un mensaje de voz de un cliente",
    fields={
        "quien_llama": ContentFieldDefinition(
            type=ContentFieldType.STRING, method=GenerationMethod.EXTRACT,
            description="Nombre y empresa de quien llama"),
        "resumen": ContentFieldDefinition(
            type=ContentFieldType.STRING, method=GenerationMethod.GENERATE,
            description="Resumen del mensaje en una o dos oraciones, en español"),
        "acciones_solicitadas": ContentFieldDefinition(
            type=ContentFieldType.STRING, method=GenerationMethod.GENERATE,
            description="Qué pide la persona que hagamos"),
        "telefono_devolucion": ContentFieldDefinition(
            type=ContentFieldType.STRING, method=GenerationMethod.EXTRACT,
            description="Número telefónico para devolver la llamada"),
        "prioridad": ContentFieldDefinition(
            type=ContentFieldType.STRING, method=GenerationMethod.CLASSIFY,
            description="Urgencia del mensaje", enum=["alta", "media", "baja"]),
    },
)

analizador = ContentAnalyzer(
    base_analyzer_id="prebuilt-audio",          # base: prebuilt-document | prebuilt-image | prebuilt-audio | prebuilt-video
    description="Analizador de buzón de voz de ventas",
    field_schema=esquema,
    models={"completion": "gpt-4.1", "embedding": "text-embedding-3-large"},   # nombres de tus deployments
)

client.begin_create_analyzer(analyzer_id="buzon_ventas", resource=analizador).result()
print("Analizador creado")

resultado = client.begin_analyze(analyzer_id="buzon_ventas",
                                 inputs=[AnalysisInput(url="https://<tu-storage>/muestras/buzon.wav")]).result()
for nombre, campo in resultado.contents[0].fields.items():
    print(f"{nombre:22s}: {campo.value}")
```
- **Explicación:**
  - **Métodos de generación de campos:**
    - `EXTRACT`: el valor aparece literalmente en el contenido (un teléfono, un nombre).
    - `GENERATE`: el modelo **genera** el valor a partir del contenido (un resumen).
    - `CLASSIFY`: el modelo elige una opción de una lista (`enum`).
  - `base_analyzer_id` indica la modalidad (documento, imagen, audio o video).
  - Una vez creado, el analizador se reutiliza como cualquier prebuilt: solo cambias el `analyzer_id`.

### Salida esperada (similar al ejemplo de Microsoft Learn)
```
quien_llama           : Ava de Contoso
resumen               : Ava da seguimiento a la reunión y comenta que pueden cumplir con el precio esperado.
acciones_solicitadas  : Devolver la llamada o enviar un correo para acordar siguientes pasos.
telefono_devolucion   : 555-12345
prioridad             : alta
```

## Errores comunes
| Error | Causa | Solución |
|---|---|---|
| `401/403` | Falta el rol o la llave es incorrecta | Asigna **Cognitive Services User** y revisa la llave |
| Error de "default model deployments" | No hay deployments asociados | Despliega gpt-4.1 / gpt-4.1-mini / text-embedding-3-large y configúralos en el portal o con `update_defaults` |
| `InvalidRequest` con URL | El archivo no es accesible públicamente | Usa una URL con SAS o `begin_analyze_binary` |

## Práctica oficial de Microsoft Learn
- [Ejercicio: Introducción a la extracción de información en Microsoft Foundry](https://learn.microsoft.com/es-es/training/modules/get-started-information-extraction/4-exercise)
- [Ejercicio: Explorar la extracción de información con IA](https://learn.microsoft.com/es-es/training/modules/introduction-information-extraction/6b-exercise)
