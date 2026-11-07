# Tema 1: Onboarding — Qué instalar y qué conceptos debes saber antes de iniciar

### Descripción
La AI-901 es una certificación *Fundamentals*, pero a diferencia de la AI-900, más de la mitad del examen (55–60%) es sobre **implementar soluciones con Microsoft Foundry**: desplegar modelos, crear agentes y escribir clientes ligeros en Python. Por eso conviene preparar tu entorno desde el día uno, aunque los primeros módulos sean conceptuales.

Piensa en este tema como preparar tu cocina antes de empezar la receta: si ya tienes los ingredientes y utensilios a la mano, cada práctica posterior fluye sin interrupciones.

### Aspectos Clave

1. **Cuenta de Azure:**
   - Crea una [cuenta gratuita de Azure](https://azure.microsoft.com/es-mx/free/) o usa una suscripción de tu empresa/escuela.
   - Si eres estudiante, revisa [Azure for Students](https://azure.microsoft.com/es-mx/free/students/) (no pide tarjeta de crédito).
   - Necesitarás permisos para crear un **recurso de Microsoft Foundry** y un **proyecto** dentro de él.

   > [!WARNING]
   > Algunos modelos (por ejemplo la familia GPT-5) pueden requerir registro previo y no todos los modelos están disponibles en todas las regiones. Si un modelo no aparece, prueba otra región.

2. **Herramientas a instalar:**

   | Herramienta | Para qué la usarás | Cómo verificar |
   |---|---|---|
   | [Python 3.10 o superior](https://www.python.org/downloads/) | Todos los clientes y tutoriales del acordeón (el SDK de Voice Live pide 3.10+) | `python --version` |
   | [Visual Studio Code](https://code.visualstudio.com/) + extensión de Python | Editor recomendado por Microsoft Learn | — |
   | [Azure CLI](https://learn.microsoft.com/es-es/cli/azure/install-azure-cli) | Iniciar sesión con `az login` para que `DefaultAzureCredential` funcione | `az --version` |
   | [Git](https://git-scm.com/) | Clonar repos de ejemplo | `git --version` |
   | [Postman](https://www.postman.com/) (opcional) | Probar endpoints REST sin código | — |

3. **Entorno virtual de Python:**
   Aísla las librerías de cada proyecto para evitar conflictos de versiones.
   ```bash
   # Crear y activar un entorno virtual
   python -m venv .venv

   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   # macOS / Linux
   source .venv/bin/activate

   # Librerías que usarás a lo largo del acordeón
   pip install openai "azure-ai-projects>=2.0.0" azure-identity python-dotenv
   ```
   - **Explicación:**
     - `openai`: cliente oficial de OpenAI. En Foundry se usa para hablar con la **Responses API**.
     - `azure-ai-projects`: el **SDK de Foundry** (`AIProjectClient`) para trabajar con proyectos y agentes.
     - `azure-identity`: autenticación con Microsoft Entra ID (`DefaultAzureCredential`).
     - `python-dotenv`: lee variables desde un archivo `.env` para no escribir llaves en el código.

4. **Conceptos que debes dominar antes de empezar:**
   - **API y endpoint:** un *endpoint* es una URL a la que tu código le manda peticiones HTTP. En Foundry hay endpoints de **proyecto** (`https://<recurso>.services.ai.azure.com/api/projects/<proyecto>`) y endpoints de **modelo**.
   - **REST y JSON:** las peticiones llevan *headers* (autenticación, tipo de contenido) y un *body* en JSON. Las respuestas también son JSON.
   - **Llave (key) vs. Microsoft Entra ID:** puedes autenticarte con una API key o con un token de identidad. La llave es como la llave de tu casa: quien la tenga entra. Entra ID es como un gafete con tu nombre y permisos.
   - **Variables de entorno:** donde guardas endpoints y llaves.
     ```bash
     # .env (NUNCA lo subas a GitHub; agrégalo a tu .gitignore)
     FOUNDRY_PROJECT_ENDPOINT=https://<recurso>.services.ai.azure.com/api/projects/<proyecto>
     FOUNDRY_MODEL_NAME=gpt-4.1-mini
     FOUNDRY_KEY=<tu-llave>
     ```
   - **Token:** la unidad mínima de texto que procesa un modelo (palabra, subpalabra o signo). Los límites y costos se miden en tokens.
   - **Deployment (despliegue):** un modelo del catálogo no se puede usar hasta que lo despliegas. En tu código usas el **nombre del deployment**, no el nombre del modelo.

5. **Prueba de humo (smoke test):**
   Cuando tengas tu proyecto y un modelo desplegado (lo harás en la [Parte 2](../../parte2/modulo1/tema4.md)), este script confirma que todo está bien conectado:
   ```python
   import os
   from dotenv import load_dotenv
   from azure.identity import DefaultAzureCredential
   from azure.ai.projects import AIProjectClient

   load_dotenv()

   project_client = AIProjectClient(
       endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
       credential=DefaultAzureCredential(),  # usa tu sesión de `az login`
   )

   # Lista los modelos desplegados en tu proyecto
   for deployment in project_client.deployments.list():
       print(deployment.name)
   ```
   - **Explicación:** si ves el nombre de tu deployment, tu autenticación, endpoint y permisos están listos.

### Recursos
- [Página oficial de la certificación Azure AI Fundamentals (AI-901)](https://learn.microsoft.com/es-es/credentials/certifications/azure-ai-fundamentals/)
- [Guía de estudio del examen AI-901](https://learn.microsoft.com/es-es/credentials/certifications/resources/study-guides/ai-901)
- [Introducción a Python (acordeón AI-900)](https://github.com/josejesusguzman/acordeon-ia-900/blob/main/docs/intro_python.md)
