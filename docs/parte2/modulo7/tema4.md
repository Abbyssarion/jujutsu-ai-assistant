# Tema 4: Tutorial de conexión de Foundry IQ con un agente de Microsoft Foundry

**Objetivo:** Crear una base de conocimiento en Foundry IQ, conectarla a un agente como herramienta MCP y probar respuestas fundamentadas con citas, primero en el portal y después con Python.

Lectura oficial: [Bases de conocimiento – Microsoft Learn](https://learn.microsoft.com/es-es/training/modules/get-started-foundry-iq/3-knowledge-bases?pivots=text)

## Paso a Paso (portal):

### 1. Crear el recurso de Foundry IQ (Azure AI Search)
- En tu proyecto de Foundry, ve a la sección de **Knowledge / Foundry IQ** y crea o conecta un **servicio de Azure AI Search** que soporte recuperación agéntica.
- Asigna a la **identidad administrada de tu proyecto** el rol **Search Index Data Reader** sobre el servicio de Azure AI Search. Sin esto, el agente recibirá errores **403** al intentar recuperar información en el Playground.

### 2. Crear la base de conocimiento
- Crea una base llamada, por ejemplo, `politicas-viajes`.
- **Agrega fuentes de conocimiento** (knowledge sources):
  - Sube documentos a **Azure Blob Storage** (por ejemplo `politica_viaticos_2026.pdf`, `politica_cancelaciones.pdf`), o
  - Conecta un sitio de **SharePoint**, **OneLake**, un índice existente de Azure AI Search o contenido web.
- Foundry IQ hace automáticamente el **chunking**, los **embeddings** y la **extracción de metadatos**.
- Configura el **modelo** para la recuperación agéntica y, si quieres, prompts que indiquen qué fuentes priorizar.

> [!TIP]
> Agrupa fuentes que pertenecen al mismo dominio. Meter todos los documentos de la empresa en una sola base hace la recuperación **menos precisa** porque el contenido no relacionado o contradictorio diluye los resultados.

### 3. Conectar la base al agente
- Abre (o crea) tu agente en **Build → Agents**.
- En **Knowledge** o **Tools**, agrega la base de conocimiento de Foundry IQ. Se conecta como **herramienta MCP**.
- Escribe **instrucciones** claras sobre cuándo y cómo usarla. Ejemplo de Microsoft Learn (adaptado):
  ```text
  Usa la base de conocimiento para responder preguntas sobre políticas de viajes y gastos.
  Basa tus afirmaciones en el contenido recuperado y cita las fuentes.
  Si la base de conocimiento no tiene suficiente información, di que no lo sabes en lugar de adivinar.
  ```

### 4. Probar en el Playground
Prueba distintos tipos de preguntas (las que recomienda Microsoft Learn):

| Tipo de pregunta | Ejemplo | Qué revisar |
|---|---|---|
| Directa, una fuente | "¿Cuánto me pagan de hotel en el extranjero?" | Respuesta y cita correctas |
| Varias fuentes | "Si cancelo un viaje de trabajo 3 días antes, ¿qué me reembolsan y qué gastos puedo comprobar?" | Que combine ambas políticas |
| Ambigua | "¿Cuánto me dan?" | Que pida aclaración |
| Sin respuesta | "¿Puedo llevar a mi mascota?" | Que diga que no lo sabe |
| Permisos distintos | La misma pregunta con usuarios de distintas áreas | Que solo devuelva lo autorizado |
| Inyección | Un documento con "ignora tus instrucciones" | Que no cambie su comportamiento |

- Revisa las **citas** y la **actividad de la herramienta** (qué subconsultas hizo y qué fragmentos recuperó).

## Paso a Paso (Python):

### 5. Crear la conexión del proyecto hacia la base de conocimiento
```python
# pip install "azure-ai-projects>=2.0.0" openai azure-identity requests python-dotenv
import os, requests
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

load_dotenv()
credential = DefaultAzureCredential()

project_resource_id = os.environ["PROJECT_RESOURCE_ID"]
# /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<recurso>/projects/<proyecto>
connection_name = "kb-politicas-viajes"
mcp_endpoint = (f"{os.environ['SEARCH_ENDPOINT']}/knowledgebases/politicas-viajes/mcp"
                "?api-version=2026-08-01-preview")

token = get_bearer_token_provider(credential, "https://management.azure.com/.default")()
resp = requests.put(
    f"https://management.azure.com{project_resource_id}/connections/{connection_name}"
    "?api-version=2025-10-01-preview",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "name": connection_name,
        "type": "Microsoft.MachineLearningServices/workspaces/connections",
        "properties": {
            "authType": "ProjectManagedIdentity",     # el proyecto se autentica con su identidad
            "category": "RemoteTool",
            "target": mcp_endpoint,
            "isSharedToAll": True,
            "audience": "https://search.azure.com/",
            "metadata": {"ApiType": "Azure"},
        },
    },
)
resp.raise_for_status()
print("Conexión creada")
```
- **Explicación:**
  - Cada base de conocimiento expone un **endpoint MCP**: `{servicio-search}/knowledgebases/{nombre}/mcp?api-version=...`.
  - La **conexión del proyecto** guarda ese endpoint y define que el proyecto se autentique con su **identidad administrada** (sin llaves en el código).
  - Este paso solo se hace una vez; en el portal ocurre automáticamente al agregar la base al agente.

### 6. Crear el agente con la herramienta MCP de la base de conocimiento
```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool

load_dotenv()
project_client = AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
                                 credential=DefaultAzureCredential())

mcp_endpoint = (f"{os.environ['SEARCH_ENDPOINT']}/knowledgebases/politicas-viajes/mcp"
                "?api-version=2026-08-01-preview")

herramienta_kb = MCPTool(
    server_label="knowledge-base",
    server_url=mcp_endpoint,
    require_approval="never",
    allowed_tools=["knowledge_base_retrieve"],      # solo la herramienta de recuperación
    project_connection_id="kb-politicas-viajes",    # la conexión del paso 5
)

instrucciones = """
Eres el asistente de viajes corporativos de Contoso. Responde en español de México.
- Usa SIEMPRE la base de conocimiento para preguntas de políticas; nunca respondas de memoria.
- Cita la fuente de cada afirmación.
- Si la base de conocimiento no contiene la respuesta, responde: "No encontré esa información en las políticas".
"""

agente = project_client.agents.create_version(
    agent_name="agente-viajes-iq",
    definition=PromptAgentDefinition(
        model=os.environ["FOUNDRY_MODEL_NAME"],
        instructions=instrucciones,
        tools=[herramienta_kb],
    ),
)

openai_client = project_client.get_openai_client()
r = openai_client.responses.create(
    input="¿Cuánto me pagan de hotel en un viaje a Madrid?",
    extra_body={"agent_reference": {"name": agente.name, "type": "agent_reference"}},
)
print(r.output_text)
```
- **Explicación:**
  - `MCPTool` apunta al endpoint MCP de la base y usa la **conexión del proyecto** para autenticarse.
  - `allowed_tools=["knowledge_base_retrieve"]` limita al agente a **recuperar** (principio de mínimo privilegio).
  - Las **instrucciones** son clave: conectar la base **no garantiza** que el agente la use siempre; hay que decirle cuándo recuperar, cómo citar y qué hacer si no hay evidencia.

## Permisos necesarios (resumen)

| Ámbito | Rol | Para qué |
|---|---|---|
| Recurso de Foundry | **Foundry User** | Usar deployments y crear agentes |
| Recurso de Foundry | **Foundry Project Manager** | Crear la conexión MCP del proyecto |
| Azure AI Search | **Search Index Data Reader** (identidad del proyecto) | Evitar 403 al recuperar |
| Recurso de Foundry | **Cognitive Services User** (identidad del servicio de búsqueda) | Solo si la base usa un LLM para planear consultas o sintetizar respuestas |

> [!NOTE]
> Las versiones de API (`2026-08-01-preview`, `2025-10-01-preview`) son las de la documentación de Microsoft al momento de escribir este acordeón. Si cambian, revisa [Conectar Foundry IQ a un agente](https://learn.microsoft.com/es-es/azure/foundry/agents/how-to/foundry-iq-connect).

## Práctica oficial de Microsoft Learn
- [Ejercicio: Introducción a Foundry IQ en Microsoft Foundry](https://learn.microsoft.com/es-es/training/modules/get-started-foundry-iq/5-exercise)
- [Ejercicio: Explorar RAG](https://learn.microsoft.com/es-es/training/modules/rag-fundamentals/6-exercise)
