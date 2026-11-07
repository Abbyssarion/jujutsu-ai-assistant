# Resumen rápido: Introducción a la IA en Azure

Este módulo presenta Azure y sus capacidades para construir soluciones de IA, con foco en **Microsoft Foundry**.

- **Azure:**
  Plataforma de nube con cuatro categorías básicas: **cómputo**, **almacenamiento**, **redes** y **servicios de aplicaciones**. Jerarquía:
  - **Tenant:** la identidad de tu organización en la nube de Microsoft (usuarios, grupos, políticas).
  - **Suscripción:** contenedor de **facturación**, cuotas y control de acceso.
  - **Grupo de recursos:** "carpeta" de recursos relacionados.
  - **Recurso:** cada servicio (cuenta de almacenamiento, base de datos, recurso de Foundry). Tiene tipo, configuración, nombre/ID, región, nivel de desempeño y permisos.
  - Se administra desde el **Azure Portal** o de forma programática (CLI, scripts, plantillas).

- **Desarrollar apps de IA en Azure:**
  - **Seguridad y redes:** **Microsoft Entra ID** + **RBAC**; secretos y llaves en **Azure Key Vault** (recuperados con **identidad administrada**), nunca en el código.
  - **Hosting y escalado:** VMs, **AKS** (contenedores), **App Service** (web/APIs). Escalar **horizontal** (más instancias) o **vertical** (más CPU/RAM).
  - **Datos:** Azure SQL Database, Cosmos DB, Azure Database for PostgreSQL.
  - **IA:** Microsoft Foundry.

- **Microsoft Foundry:**
  Plataforma PaaS unificada para construir, desplegar y administrar **aplicaciones y agentes de IA**:
  - **Modelos:** miles en el catálogo (OpenAI GPT-5, Anthropic Claude, Mistral, Cohere, Meta Llama, DeepSeek, xAI Grok, Black Forest Labs, Hugging Face). Tipos de despliegue: *standard, provisioned, batch*.
  - **Agentes:** razonan, llaman herramientas y automatizan flujos; Foundry maneja hilos, ejecución de herramientas, seguridad y observabilidad.
  - **Tools (Foundry Tools):** Azure Vision, Azure Language, Azure Speech, Document Intelligence, Content Understanding, etc.
  - **Knowledge (Foundry IQ):** capa de conocimiento con permisos y recuperación agéntica.
  - **Recurso de Foundry** (recurso de Azure con modelos, servicio de agentes, gobernanza, cuotas) vs. **Proyecto de Foundry** (espacio de trabajo con agentes, evaluaciones, archivos, índices, conexiones). Patrón típico: un recurso por equipo, varios proyectos.
  - **Flujo recomendado:** crear proyecto → elegir y desplegar modelo → probar en el **Playground** → usarlo desde tu aplicación cliente.
  - **Modelo cliente-servidor:** el cliente captura la entrada y muestra la salida; el servidor (tu **deployment**) ejecuta la inferencia y aplica instrucciones y seguridad.

- **Endpoints:**
  - Interfaces **REST**; peticiones con *headers* y *body* JSON.
  - **Endpoint de proyecto:** `https://<recurso>.services.ai.azure.com/api/projects/<proyecto>`
  - **Endpoint de modelo** (compatible con OpenAI): `https://<recurso>.openai.azure.com/openai/v1/`
  - Autenticación con **API key** o **token de Microsoft Entra ID** (`Authorization: Bearer ...`).
  - Los **SDKs** (Python, JavaScript, C#) envuelven las llamadas REST.

> [!TIP]
> Si en el examen preguntan dónde guardar una API key de forma segura → **Azure Key Vault**. Cómo la obtiene la app sin contraseñas → **identidad administrada**.
