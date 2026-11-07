# Resumen rápido: Introducción a los conceptos de IA

Este módulo es la puerta de entrada a la certificación AI-901. No escribes código ni haces matemáticas: el objetivo es que entiendas **qué tipos de soluciones hace posible la IA** y **qué consideraciones de IA responsable** debes tener en cuenta.

- **Introducción a la IA:**
  La IA es software que imita capacidades humanas como entender lenguaje, ver, escuchar, razonar y generar contenido. Toda la IA moderna está construida sobre modelos de *machine learning* (aprendizaje automático), es decir, modelos que aprendieron patrones a partir de datos en lugar de ser programados regla por regla.

- **IA generativa y agentes:**
  La IA generativa crea contenido nuevo (texto, imágenes, video, código) a partir de un *prompt* escrito en lenguaje natural. Se basa en **modelos de lenguaje**:
  - **LLM (Large Language Models):** más datos de entrenamiento y más parámetros. Son potentes y generalizan bien, pero cuestan más.
  - **SLM (Small Language Models):** menos datos y parámetros. Funcionan bien para temas acotados y son fáciles de desplegar en dispositivos locales.

  Un **agente** es una aplicación construida sobre IA generativa que razona, usa herramientas y actúa. Tiene tres elementos: **modelo** (el cerebro), **instrucciones** (su "descripción de puesto") y **herramientas** (de conocimiento y de acción).

- **Visión por computadora (Computer Vision):**
  Software que interpreta imágenes y video: clasificar imágenes, detectar objetos, segmentar píxeles y describir escenas.

- **Voz (Speech):**
  - **Reconocimiento de voz (speech-to-text):** convierte audio en texto.
  - **Síntesis de voz (text-to-speech):** convierte texto en audio.

- **Texto y lenguaje natural (NLP):**
  Analizar texto para extraer significado: detección de idioma, palabras clave, entidades, sentimiento y resumen.

- **Extracción de información:**
  Sacar datos estructurados (campos, tablas, valores) de contenido no estructurado como documentos, formularios, imágenes, audio y video.

- **IA responsable:**
  Seis principios que debes saberte de memoria para el examen (el dominio "Describe principles of responsible AI" pregunta uno por uno):

  | Principio | Idea clave | Ejemplo de Microsoft Learn |
  |---|---|---|
  | **Equidad (Fairness)** | Minimizar sesgos en datos y modelos | Un sistema de admisión universitaria no debe discriminar por factores demográficos irrelevantes |
  | **Confiabilidad y seguridad (Reliability and safety)** | La IA es probabilística, no infalible | Un robot con visión solo actúa si la confianza de la detección supera un umbral |
  | **Privacidad y seguridad (Privacy and security)** | Proteger datos personales y que el modelo no los revele | Un sistema de reconocimiento facial en aeropuerto borra las imágenes cuando ya no se necesitan |
  | **Inclusión (Inclusiveness)** | Que nadie quede excluido | Un agente de voz también genera subtítulos para personas con discapacidad auditiva |
  | **Transparencia (Transparency)** | Explicar cómo funciona y sus límites | Un banco informa que usa IA para aprobar préstamos y describe los datos de entrenamiento |
  | **Responsabilidad (Accountability)** | Las personas y organizaciones responden por la IA | Definir un marco de gobernanza que aplique los principios |

- **Escenarios generativos y agénticos más comunes:**
  Chatbots, asistentes que automatizan tareas, creación de documentos o contenido, traducción automática y resumen o explicación de documentos complejos.

> [!TIP]
> Para el examen, cuando una pregunta describa un escenario ("un sistema que...") identifica primero el **tipo de carga de trabajo** (visión, voz, texto, extracción de información o generativa/agéntica). Ese primer filtro elimina la mitad de las opciones.
