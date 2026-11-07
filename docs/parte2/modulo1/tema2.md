# Tema 2: Todos los servicios y funcionalidades de Microsoft Foundry

### Descripción
**Microsoft Foundry** es una plataforma como servicio (PaaS) unificada y de nivel empresarial para **construir, desplegar y administrar aplicaciones y agentes de IA**. Reúne en un solo lugar modelos, orquestación de agentes, herramientas, conocimiento, evaluación, monitoreo y gobernanza.

Analogía: Foundry es como una **cocina industrial equipada**. Los **modelos** son los chefs, las **tools** son los electrodomésticos especializados (horno, licuadora), el **conocimiento** es la despensa, los **agentes** son los platillos listos para servir y los **guardrails** son las normas sanitarias.

> [!NOTE]
> Antes se llamaba *Azure AI Studio* y luego *Azure AI Foundry*. Los servicios de IA "precompilados" antes eran *Azure Cognitive Services* / *Azure AI Services* y hoy se agrupan como **Foundry Tools**. El examen puede usar nombres viejos.

### Aspectos Clave

1. **Recurso vs. proyecto:**

   | Recurso de Foundry (Azure) | Proyecto de Foundry (espacio de trabajo) |
   |---|---|
   | Modelos (Microsoft, socios, OpenAI) | Agentes |
   | Servicio de agentes | Evaluaciones |
   | Gobernanza de despliegues | Archivos y datasets |
   | Monitoreo y observabilidad | Índices vectoriales |
   | Límites de seguridad | Conexiones a otros recursos |
   | Cuotas y controles operativos | Configuración del proyecto |

   Patrón típico: **un recurso por equipo o departamento**, con **varios proyectos** (uno por caso de uso).

2. **Mapa de capacidades:**

   | Capacidad | Qué te da | Detalle |
   |---|---|---|
   | **Catálogo de modelos** | Miles de modelos de primera parte, socios y open source | Model cards, benchmarks, *leaderboards*, comparación por calidad, costo y rendimiento |
   | **Despliegues** | Endpoint estable y escalable | Tipos: *Standard / Global Standard*, *Provisioned* (capacidad reservada), *Batch* (lotes, más barato, asíncrono). Límite de **TPM** |
   | **Playgrounds** | Probar sin código | Chat, agentes, imágenes, video, voz, Language. Botón **View code** |
   | **Foundry Agent Service** | Crear y ejecutar agentes | Instrucciones, herramientas, conocimiento, conversaciones, sistemas multiagente y *workflows* |
   | **Tool catalog** | Herramientas para agentes | MCP, OpenAPI, Code Interpreter, File Search, Web Search/Bing, Azure AI Search, Azure Functions, Agent-to-Agent, Fabric, SharePoint, Work IQ... |
   | **Foundry Tools** | Servicios de IA especializados | Azure Language, Azure Speech, Azure Vision, Translator, Document Intelligence, **Content Understanding**, Content Safety |
   | **Foundry IQ** | Capa de conocimiento administrada | Bases de conocimiento sobre Azure AI Search, recuperación agéntica, permisos, citas |
   | **Fine-tuning** | Ajustar modelos con tus datos | SFT, DPO, RFT |
   | **Evaluación** | Medir calidad y seguridad | Evaluadores de groundedness, relevancia, coherencia, violencia, sesgo, etc. |
   | **Guardrails** | Seguridad de modelos y agentes | Filtros de contenido, *prompt shields*, material protegido, PII, adherencia a la tarea |
   | **Observabilidad** | Ver qué pasa en producción | Trazas (OpenTelemetry), métricas, costos, latencia |
   | **Red teaming** | Atacar tu propio agente para encontrar fallas | Pruebas adversariales automatizadas |
   | **Control plane** | Gobierno de toda tu flota de agentes | Inventario, políticas, cumplimiento |

3. **Foundry Tools más importantes para el examen:**

   | Servicio | Para qué | Ejemplo |
   |---|---|---|
   | **Azure Language** | Análisis de texto | Detección de idioma, PII, entidades, sentimiento, frases clave, resumen |
   | **Azure Speech** | Voz | Speech-to-text, text-to-speech, traducción de voz, **Voice Live** |
   | **Azure Vision** | Análisis de imágenes | Etiquetas, descripciones, OCR (Read) |
   | **Azure Translator** | Traducción de texto y documentos | Traducir manuales a 10 idiomas |
   | **Document Intelligence** | Documentos | Facturas, recibos, identificaciones, formularios |
   | **Content Understanding** | Extracción multimodal | Documentos, imágenes, audio y video con esquemas |
   | **Content Safety** | Moderación | Detectar odio, violencia, *jailbreaks* |

4. **Portal de Foundry — flujo de trabajo recomendado:**
   1. Iniciar sesión en [ai.azure.com](https://ai.azure.com) y crear un **proyecto**.
   2. Elegir un modelo del **catálogo** y **desplegarlo**.
   3. Experimentar en el **Playground**: prompts, parámetros (temperatura, máximo de tokens), instrucciones.
   4. Usar el modelo configurado desde tu **aplicación cliente** (SDK o REST).
   5. Convertirlo en **agente**, agregar herramientas y conocimiento, **evaluar**, aplicar **guardrails** y **monitorear**.

5. **Modelo cliente-servidor:**
   - **Cliente:** interfaz (UI o CLI), captura entrada (texto, voz, imagen), arma la petición, la envía y muestra la salida.
   - **Servidor (tu deployment):** recibe el prompt, ejecuta la inferencia, aplica instrucciones de sistema, seguridad y contexto, y devuelve texto, imagen, audio o JSON.

### Para el examen
- "Probar prompts y parámetros sin escribir código" → **Playground**.
- "Comparar modelos por calidad y costo" → **catálogo de modelos / leaderboards / benchmarks**.
- "Medir si las respuestas están fundamentadas" → **evaluadores** (groundedness).
- "Bloquear contenido violento en las respuestas" → **guardrails / filtros de contenido**.
- "Extraer campos de facturas, audio y video" → **Content Understanding**.

### Recursos
- [¿Qué es Microsoft Foundry?](https://learn.microsoft.com/es-es/azure/foundry/what-is-foundry)
