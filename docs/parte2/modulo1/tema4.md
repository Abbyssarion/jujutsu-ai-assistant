# Tema 4: Tutorial desde cero y comentado paso a paso — Implementar un agente de Microsoft Foundry con Python

**Objetivo:** Crear un agente de Foundry desde código, conversar con él en varias vueltas manteniendo el contexto y limpiar los recursos al final. Todo con el SDK de Foundry (`azure-ai-projects` 2.x) y autenticación con Microsoft Entra ID.

> [!NOTE]
> Este tutorial cubre las habilidades del examen *"Create and test a single-agent solution"* y *"Create a lightweight client application for an agent"*.

## Paso a Paso:

### 1. Prerrequisitos en Azure
- Un **proyecto de Foundry** con un **modelo desplegado** (por ejemplo `gpt-4.1-mini`). Si no lo tienes, sigue los pasos 1 y 2 del [Tutorial: mi primer agente](../../parte1/modulo2/tema3.md).
- Tu usuario necesita el rol **Foundry User** (antes *Azure AI User*) sobre el recurso de Foundry para crear y usar agentes. Si creaste el recurso, normalmente ya eres *Owner*.
- Copia el **endpoint del proyecto** desde la página **Overview** del proyecto. Tiene esta forma:
  `https://<recurso>.services.ai.azure.com/api/projects/<proyecto>`

### 2. Preparar el entorno local
```bash
mkdir agente-foundry && cd agente-foundry
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1    |    macOS/Linux: source .venv/bin/activate

pip install "azure-ai-projects>=2.0.0" openai azure-identity python-dotenv

az login          # DefaultAzureCredential usará esta sesión
```

Crea un archivo `.env`:
```bash
FOUNDRY_PROJECT_ENDPOINT=https://<recurso>.services.ai.azure.com/api/projects/<proyecto>
FOUNDRY_MODEL_NAME=gpt-4.1-mini
FOUNDRY_AGENT_NAME=agente-viajes
```

### 3. Crear el agente (`crear_agente.py`)
```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

load_dotenv()

# 1) Conectarse al proyecto con Microsoft Entra ID
project_client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# 2) Definir el agente: MODELO + INSTRUCCIONES (+ herramientas, más adelante)
instrucciones = """
Eres "Viajero", un asistente de viajes por México.
- Responde en español de México, tono cercano y profesional.
- Máximo 5 viñetas por respuesta.
- Si no sabes algo, dilo; nunca inventes precios ni horarios.
"""

agente = project_client.agents.create_version(
    agent_name=os.environ["FOUNDRY_AGENT_NAME"],
    definition=PromptAgentDefinition(
        model=os.environ["FOUNDRY_MODEL_NAME"],   # nombre del DEPLOYMENT
        instructions=instrucciones,
    ),
)

print(f"Agente creado -> nombre: {agente.name} | versión: {agente.version} | id: {agente.id}")
```
- **Explicación:**
  - `AIProjectClient` es la puerta de entrada al proyecto. `DefaultAzureCredential` prueba varias formas de autenticarse (variables de entorno, identidad administrada, tu sesión de `az login`...) y usa la primera que funcione.
  - `PromptAgentDefinition` describe un agente basado en prompt: **modelo + instrucciones** (y opcionalmente `tools=[...]`).
  - `create_version` crea el agente o una **nueva versión** si ya existe con ese nombre. Los agentes en Foundry son versionados: puedes iterar instrucciones sin perder las anteriores.
  - Después de correrlo, el agente aparece en el portal de Foundry en **Agents**, donde también puedes probarlo en el Playground.

### 4. Conversar con el agente (`chat.py`)
```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# 1) Recuperar el agente existente por nombre
agente = project_client.agents.get(agent_name=os.environ["FOUNDRY_AGENT_NAME"])
print(f"Usando el agente: {agente.name}")

# 2) Obtener un cliente OpenAI autenticado contra el proyecto
openai_client = project_client.get_openai_client()

# 3) Crear una conversación: guarda el historial del lado del servidor
conversacion = openai_client.conversations.create()
print("Escribe tu pregunta (o 'salir' para terminar)\n")

while True:
    pregunta = input("Tú: ").strip()
    if pregunta.lower() in ("salir", "exit", "quit"):
        break

    # 4) Agregar el mensaje del usuario a la conversación
    openai_client.conversations.items.create(
        conversation_id=conversacion.id,
        items=[{"type": "message", "role": "user", "content": pregunta}],
    )

    # 5) Pedir respuesta AL AGENTE (no al modelo directo) usando agent_reference
    respuesta = openai_client.responses.create(
        conversation=conversacion.id,
        extra_body={"agent_reference": {"name": agente.name, "type": "agent_reference"}},
    )
    print(f"Viajero: {respuesta.output_text}\n")

# 6) Limpieza de la conversación
openai_client.conversations.delete(conversation_id=conversacion.id)
print("Conversación eliminada. ¡Hasta luego!")
```
- **Explicación:**
  - `agents.get` trae el agente por nombre; no necesitas volver a definirlo.
  - `get_openai_client()` devuelve un cliente del SDK `openai` ya autenticado y apuntando a tu proyecto. Los agentes de Foundry usan una **extensión de la Responses API**.
  - `conversations.create()` crea un hilo de conversación que **guarda el historial en el servidor**: no tienes que reenviar todos los mensajes, por eso el agente recuerda lo anterior.
  - `extra_body={"agent_reference": ...}` le indica a Foundry que responda **el agente** (con sus instrucciones y herramientas), no el modelo "pelón".
  - `output_text` es un atajo que junta todo el texto de la respuesta.

> [!IMPORTANT]
> En el módulo de Microsoft Learn el ejemplo usa `extra_body={"agent": {"name": ..., "type": "agent_reference"}}`, que corresponde a las versiones beta del SDK. Con `azure-ai-projects` 2.0.0 estable el campo es `agent_reference`. Si un ejemplo no te funciona, revisa la versión con `pip show azure-ai-projects`.

**Prueba de memoria:**
```
Tú: Quiero ir a Oaxaca 3 días en noviembre
Viajero: • Día 1: Centro histórico y Santo Domingo ...
Tú: ¿Y qué tal el clima en esas fechas?
Viajero: En noviembre Oaxaca suele estar templado y seco ...   ← recordó "Oaxaca" y "noviembre"
```

### 5. Variante: sin conversación, encadenando respuestas
Si no necesitas guardar la conversación, puedes encadenar respuestas con `previous_response_id`:
```python
r1 = openai_client.responses.create(
    input="¿Qué pueblos mágicos hay cerca de Puebla?",
    extra_body={"agent_reference": {"name": agente.name, "type": "agent_reference"}},
)
r2 = openai_client.responses.create(
    input="¿Cuál me recomiendas para ir con niños?",
    previous_response_id=r1.id,
    extra_body={"agent_reference": {"name": agente.name, "type": "agent_reference"}},
)
print(r2.output_text)
```

### 6. Limpieza (`borrar_agente.py`)
```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()
project_client = AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
                                 credential=DefaultAzureCredential())

project_client.agents.delete(agent_name=os.environ["FOUNDRY_AGENT_NAME"])
print("Agente eliminado")
```
- **Explicación:** `agents.delete` elimina el agente con todas sus versiones. Si solo quieres borrar una versión, usa `agents.delete_version(agent_name=..., agent_version=...)`. También puedes eliminarlo desde el portal.

## Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `DefaultAzureCredential failed to retrieve a token` | No iniciaste sesión | `az login` |
| `403 Forbidden` / `PermissionDenied` | Te falta el rol | Asigna **Foundry User** en el recurso de Foundry |
| `DeploymentNotFound` | Usaste el nombre del modelo, no el del deployment | Revisa **Models + endpoints** en el portal |
| `429 Too Many Requests` | Superaste el límite de TPM | Espera, reduce `max_output_tokens` o sube la cuota |

## Práctica oficial de Microsoft Learn
- [Ejercicio: Introducción a Microsoft Foundry](https://learn.microsoft.com/es-es/training/modules/get-started-with-ai-in-azure/6-exercise)
- [Ejercicio: Introducción a la IA generativa y los agentes en Microsoft Foundry](https://learn.microsoft.com/es-es/training/modules/get-started-with-generative-ai-and-agents/6-exercise)
