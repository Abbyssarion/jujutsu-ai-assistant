# Preguntas rápidas para repasar

Banco de repaso por módulo. Léelas, contéstalas de memoria y **después** despliega la respuesta.

> [!NOTE]
> Estas preguntas no son del examen oficial ni pretenden reproducirlo. Son un repaso de los datos que más se confunden.

---

## Parte 1 · Módulo 1 — Conceptos de IA e IA responsable

<details><summary><b>1. ¿Cuál es la diferencia entre un modelo de clasificación y uno generativo?</b></summary>

El de clasificación **asigna una categoría** a información existente (mandar un correo a Spam). El generativo **crea contenido nuevo** a partir de patrones aprendidos (redactar la respuesta a ese correo).
</details>

<details><summary><b>2. ¿Cuáles son los seis principios de IA responsable de Microsoft?</b></summary>

Equidad, confiabilidad y seguridad, privacidad y seguridad, inclusión, transparencia y responsabilidad.
</details>

<details><summary><b>3. Un agente de voz también genera subtítulos para personas con discapacidad auditiva. ¿Qué principio aplica?</b></summary>

**Inclusión**.
</details>

<details><summary><b>4. Un robot solo toma un objeto si la confianza de la detección supera un umbral. ¿Qué principio aplica?</b></summary>

**Confiabilidad y seguridad**.
</details>

<details><summary><b>5. ¿Cuáles son los tres elementos de un agente de IA?</b></summary>

**Modelo** (el cerebro), **instrucciones** (system prompt) y **herramientas** (de conocimiento y de acción).
</details>

<details><summary><b>6. ¿LLM o SLM para un agente que corre en un dispositivo local con un tema acotado?</b></summary>

**SLM**: menos parámetros, fácil de desplegar en dispositivos y bueno para temas enfocados.
</details>

---

## Parte 1 · Módulo 2 — IA generativa y agentes

<details><summary><b>7. ¿Qué es un token?</b></summary>

La unidad mínima de texto que procesa un modelo: una palabra, subpalabra o signo. Cada token tiene un ID entero.
</details>

<details><summary><b>8. ¿Qué diferencia hay entre un vector y un embedding?</b></summary>

El embedding es un vector que ya incluye **contexto** gracias a la **atención**; captura significado.
</details>

<details><summary><b>9. ¿Cómo se mide qué tan parecidos son dos embeddings?</b></summary>

Con la **similitud coseno** (1 = misma dirección, 0 = sin relación).
</details>

<details><summary><b>10. ¿Qué bloque del Transformer predice el siguiente token?</b></summary>

El **decodificador**, usando atención enmascarada (solo ve los tokens anteriores).
</details>

<details><summary><b>11. ¿System prompt o user prompt: dónde se define el tono y las restricciones?</b></summary>

En el **system prompt**.
</details>

<details><summary><b>12. ¿Qué hace el RAG?</b></summary>

Recupera información relevante y la agrega al prompt para que la respuesta esté **fundamentada (grounded)**. No modifica el modelo.
</details>

---

## Parte 1 · Módulos 3 y 4 — NLP y voz

<details><summary><b>13. ¿Stemming o lematización produce siempre una palabra válida?</b></summary>

La **lematización** (usa reglas lingüísticas). El stemming solo recorta terminaciones.
</details>

<details><summary><b>14. ¿Qué indica un TF-IDF alto?</b></summary>

Que la palabra es frecuente en un documento pero **rara en el resto** de la colección.
</details>

<details><summary><b>15. ¿Resumen extractivo o abstractivo genera texto nuevo?</b></summary>

**Abstractivo**. El extractivo (TextRank) selecciona oraciones del original.
</details>

<details><summary><b>16. ¿A qué frecuencia se muestrea normalmente la voz para reconocimiento?</b></summary>

**16 kHz** (8–16 kHz).
</details>

<details><summary><b>17. ¿Qué técnica de extracción de características imita el oído humano?</b></summary>

**MFCC** (escala Mel).
</details>

<details><summary><b>18. ¿Qué componente convierte el espectrograma Mel en audio en la síntesis?</b></summary>

El **vocoder neuronal** (WaveNet, HiFi-GAN).
</details>

---

## Parte 1 · Módulos 5, 6 y 7 — Visión, extracción y RAG

<details><summary><b>19. Necesitas saber **dónde** está cada producto en una imagen. ¿Qué tarea usas?</b></summary>

**Detección de objetos** (bounding boxes).
</details>

<details><summary><b>20. ¿Qué tarea clasifica cada píxel?</b></summary>

**Segmentación semántica**.
</details>

<details><summary><b>21. ¿Qué hace la capa softmax en una CNN?</b></summary>

Convierte la salida en **probabilidades por clase** que suman 1.
</details>

<details><summary><b>22. ¿Cómo procesa una imagen un Vision Transformer?</b></summary>

La divide en **parches**, los convierte en vectores y usa **atención** para relacionarlos.
</details>

<details><summary><b>23. ¿Cómo generan imágenes los modelos de difusión?</b></summary>

Parten de **ruido aleatorio** y lo eliminan iterativamente guiados por el prompt.
</details>

<details><summary><b>24. ¿Diferencia entre OCR y extracción de campos?</b></summary>

El OCR dice **qué texto existe**; la extracción de campos dice **qué significa y a qué campo pertenece**.
</details>

<details><summary><b>25. En RAG, ¿por qué se usa traslape entre chunks?</b></summary>

Para no perder contexto en los bordes de cada fragmento.
</details>

<details><summary><b>26. Si el contenido correcto no se recupera, ¿mejorar el prompt lo arregla?</b></summary>

**No.** Hay que mejorar fuentes, chunking, metadatos o estrategia de búsqueda.
</details>

---

## Parte 2 · Módulos 1 y 2 — Azure, Foundry, modelos y agentes

<details><summary><b>27. ¿Dónde guardas una API key de forma segura?</b></summary>

En **Azure Key Vault**, y la app la obtiene con una **identidad administrada**.
</details>

<details><summary><b>28. ¿Diferencia entre recurso de Foundry y proyecto de Foundry?</b></summary>

El **recurso** es el recurso de Azure (modelos, cuotas, gobernanza); el **proyecto** es el espacio de trabajo (agentes, evaluaciones, archivos, índices).
</details>

<details><summary><b>29. En el código, ¿usas el nombre del modelo o del deployment?</b></summary>

El **nombre del deployment**.
</details>

<details><summary><b>30. ¿Qué parámetro controla creatividad vs. determinismo?</b></summary>

**temperature**.
</details>

<details><summary><b>31. ¿Qué puede causar errores 429 (throttling)?</b></summary>

Superar el límite de **TPM**; baja `max_output_tokens` o reduce peticiones concurrentes.
</details>

<details><summary><b>32. ¿Qué clase del SDK de Foundry se conecta al proyecto?</b></summary>

`AIProjectClient` (paquete `azure-ai-projects`).
</details>

<details><summary><b>33. ¿Cómo obtienes un cliente para la Responses API desde el proyecto?</b></summary>

Con `project_client.get_openai_client()`.
</details>

<details><summary><b>34. Herramientas vs. conocimiento en un agente</b></summary>

**Tools = acciones**; **knowledge = contexto**.
</details>

---

## Parte 2 · Módulos 3 a 6 — Texto, voz, visión y extracción

<details><summary><b>35. ¿LLM o Azure Language para resultados consistentes en un pipeline?</b></summary>

**Azure Language** (salida estructurada y determinista).
</details>

<details><summary><b>36. ¿Qué método de `TextAnalyticsClient` detecta y oculta datos personales?</b></summary>

`recognize_pii_entities()` (devuelve `redacted_text`).
</details>

<details><summary><b>37. ¿Qué es MCP?</b></summary>

Un **estándar abierto** para conectar agentes con herramientas y datos (cliente MCP = agente; servidor MCP = servicio).
</details>

<details><summary><b>38. ¿Qué clase del Speech SDK transcribe voz?</b></summary>

`SpeechRecognizer` (con `SpeechConfig` y `AudioConfig`).
</details>

<details><summary><b>39. ¿Qué modo usas para transcribir miles de grabaciones guardadas en Storage?</b></summary>

**Transcripción por lotes (batch)** con URI SAS.
</details>

<details><summary><b>40. ¿Qué servicio da conversación voz a voz en tiempo real con interrupciones?</b></summary>

**Voice Live**.
</details>

<details><summary><b>41. ¿Cómo envías una imagen junto con un prompt en la Responses API?</b></summary>

Con partes `input_text` + `input_image` (URL o base64) en el mismo mensaje.
</details>

<details><summary><b>42. ¿Qué modelos generan video en Foundry?</b></summary>

**Sora** y **Sora 2** (trabajo asíncrono: crear → consultar → descargar).
</details>

<details><summary><b>43. ¿Qué servicio extrae campos de documentos, imágenes, audio y video?</b></summary>

**Azure Content Understanding**.
</details>

<details><summary><b>44. ¿Qué significan EXTRACT, GENERATE y CLASSIFY en un esquema de Content Understanding?</b></summary>

Extraer un valor literal, generar un valor (ej. resumen) y elegir de una lista (`enum`).
</details>

---

## Parte 2 · Módulo 7 — Foundry IQ y guardrails

<details><summary><b>45. ¿Sobre qué servicio está construido Foundry IQ?</b></summary>

**Azure AI Search**.
</details>

<details><summary><b>46. ¿Qué es la recuperación agéntica?</b></summary>

Un LLM **planea subconsultas**, busca en varias fuentes en paralelo, rankea y devuelve resultados con citas.
</details>

<details><summary><b>47. ¿Cómo se conecta una base de conocimiento a un agente?</b></summary>

Como **herramienta MCP**.
</details>

<details><summary><b>48. ¿Qué rol necesita la identidad del proyecto en Azure AI Search?</b></summary>

**Search Index Data Reader**.
</details>

<details><summary><b>49. ¿Para qué NO sirve el fine-tuning?</b></summary>

Para enseñarle datos que cambian; para eso es el **RAG**.
</details>

<details><summary><b>50. Un agente tiene guardrail propio y su modelo tiene otro. ¿Cuál aplica?</b></summary>

**El del agente** (reemplaza por completo al del modelo).
</details>

<details><summary><b>51. ¿Qué guardrail tienen los modelos por defecto?</b></summary>

**Microsoft.DefaultV2**.
</details>

---

## Trampas frecuentes

| Suena parecido | Pero |
|---|---|
| **Modelo** vs **Agente** | El modelo responde un prompt; el agente tiene instrucciones, herramientas, conocimiento y es reutilizable |
| **Nombre del modelo** vs **nombre del deployment** | En el código siempre va el del deployment |
| **Endpoint del proyecto** vs **endpoint del modelo** | `services.ai.azure.com/api/projects/...` vs `openai.azure.com/openai/v1/` |
| **Azure Language** vs **LLM** | Determinista y estructurado vs flexible y variable |
| **Foundry IQ** vs **Work IQ** | Conocimiento para agentes (devs) vs contexto de trabajo en Microsoft 365 |
| **File Search** vs **Foundry IQ** | Archivos de un agente vs capa de conocimiento compartida con permisos |
| **RAG** vs **Fine-tuning** | Le das información vs cambias su comportamiento |
| **Real-time** vs **Batch** (voz) | Streaming en vivo vs archivos asíncronos |
| **Clasificación** vs **Detección** vs **Segmentación** | Qué es vs dónde está vs qué píxeles |
