# Tema 8: ¿Para qué sí y para qué no usar la IA?

### Descripción
Que se *pueda* resolver algo con IA no significa que *se deba*. Un buen AI Engineer sabe cuándo un LLM es la herramienta correcta y cuándo basta un `if`, una consulta SQL o un servicio especializado. El examen premia la **solución más sencilla y económica** que cumple el requisito, y en el mundo real pasa lo mismo: los proyectos de IA que más valor generan atacan un **problema concreto, medible y repetitivo**, con **supervisión humana** donde importa.

Analogía: la IA generativa es como una navaja suiza; sirve para casi todo, pero si vas a clavar 200 clavos, mejor usa un martillo.

En este tema vas a ver los criterios para decidir y, sobre todo, **casos reales documentados por Microsoft** de empresas que sí usaron IA (con sus resultados) y de lecciones aprendidas cuando la IA se usó donde no debía.

---

## 1. Úsala cuando...

| Criterio | Por qué la IA aporta | Caso real documentado por Microsoft |
|---|---|---|
| La entrada es **no estructurada** (texto libre, audio, imágenes, documentos) | El código tradicional no puede "leer" una grabación o un recibo | **Crediclub** analiza grabaciones de reuniones; **Ramp** lee millones de recibos |
| La tarea es **repetitiva y de alto volumen** | Cada minuto ahorrado se multiplica por miles de casos | **Markerstudy** ahorra ~4 minutos por llamada en 840,000 llamadas al año |
| Hay **muchas respuestas válidas** (redactar, resumir, traducir) | Los LLMs generan borradores de calidad en segundos | **Axon** redacta borradores de reportes policiales; **Sayvant** redacta notas clínicas |
| Las reglas son **demasiadas o cambiantes** | Programarlas a mano es imposible de mantener | **Woven by Toyota** corrige violaciones a cientos de páginas de estándares MISRA |
| El conocimiento está **disperso en documentos** | RAG convierte años de documentación en respuestas | **Sandvik** y **Daiichi Sankyo** consultan su documentación interna con Azure OpenAI + Azure AI Search |
| Se necesita **escalar a muchos idiomas o regiones** | Generar y traducir contenido sin multiplicar personal | **Sanoma** genera 78 pronósticos locales diarios; **Welcome Account** atiende en 7 idiomas |
| Hay un **humano que revisa** o el costo de un error es bajo | La IA hace el 80% y la persona valida | Axon y Sayvant: el profesional revisa y firma cada documento |

## 2. No la uses (o úsala con mucho cuidado) cuando...

| Situación | Por qué | Mejor alternativa |
|---|---|---|
| Necesitas un resultado **exacto, determinista y auditable** (impuestos, nómina, saldos) | Un LLM es probabilístico; puede variar o equivocarse | Código tradicional, base de datos |
| Las reglas son **pocas y estables** ("si el monto > 10,000, pide autorización") | Agregar IA solo suma costo, latencia y riesgo | Una regla `if` |
| Existe un **servicio especializado** (OCR, detectar idioma, traducción) | Es más barato, rápido y consistente | Foundry Tools (Azure Language, Speech, Document Intelligence) |
| No tienes **datos** de calidad o permiso para usarlos | El modelo no puede ser mejor que sus datos; riesgo legal | Primero gobierna y limpia tus datos |
| Un error tiene **consecuencias graves** y no hay supervisión humana | Diagnóstico final, decisiones legales, acciones irreversibles | IA como apoyo + decisión humana |
| La IA podría usarse para **inferir rasgos sensibles** (emociones, género, origen) | Riesgo de discriminación y de violar la privacidad | No hacerlo (ver lección de Azure Face más abajo) |
| El **costo o la latencia** no se justifican para el volumen | Cada llamada a un modelo cuesta tokens y tiempo | Caché, reglas, modelos más pequeños |
| El sistema interactúa **sin filtros** con el público | Usuarios malintencionados pueden manipularlo | Guardrails, pruebas adversariales (ver lección de Tay) |

---

## 3. Casos reales: donde la IA **sí** aportó valor

> [!NOTE]
> Todos los casos de esta sección están documentados por Microsoft en sus historias de clientes. Las cifras son las que reporta cada historia; revisa el enlace para el detalle completo.

### 🇲🇽 Crediclub — Auditoría automática de reuniones (México)
- **Problema:** una financiera con más de 150 sucursales necesitaba revisar la calidad de las reuniones de sus asesores. Antes se revisaban unas 20 reuniones al día y la auditoría era cara.
- **Solución:** "The Watcher", un sistema que graba, transcribe y guarda las reuniones (SharePoint y **Azure Cosmos DB**) y usa modelos GPT de **Azure OpenAI** para extraer temas clave y evaluarlas con métricas predefinidas. Un sistema relacionado automatiza el análisis de solicitudes de crédito.
- **Resultados:** el gasto mensual de auditoría bajó de ~40,668 a ~1,597 USD (**−96%**); se analizan **150 reuniones en una hora**; las reuniones se evalúan el mismo día; análisis de crédito que tardaban hasta 48 horas ahora toman segundos.
- **Por qué funcionó:** audio no estructurado + tarea repetitiva + criterios de evaluación claros definidos por humanos.
- **Habilidades AI-901 relacionadas:** voz (transcripción), extracción de información, IA generativa.
- 🔗 [Historia de Crediclub](https://www.microsoft.com/en/customers/story/20355-crediclub-azure-cosmos-db)

### 🇲🇽 APEC — Prevención de ceguera en recién nacidos (México)
- **Problema:** la retinopatía del prematuro puede causar ceguera y hay pocos oftalmólogos en zonas rurales.
- **Solución:** la Asociación Para Evitar la Ceguera, con Microsoft México, creó una app que captura imágenes o video de la retina de recién nacidos y usa algoritmos de **redes neuronales profundas en Azure AI** para apoyar el diagnóstico.
- **Resultados:** Microsoft reporta **90% de precisión diagnóstica** frente a 60% del diagnóstico humano en ese contexto, y acceso en zonas rurales.
- **Por qué funcionó:** tarea de **visión por computadora** bien definida, con gran impacto social y escasez de especialistas. La IA **apoya** al médico, no lo reemplaza.
- 🔗 [Mexico is pioneering AI innovation – Microsoft](https://www.microsoft.com/en-us/microsoft-cloud/blog/2024/10/08/how-mexico-is-pioneering-ai-innovation-for-a-global-future/) · [Video de APEC](https://videos.microsoft.com/customer-stories/watch/tCPr5othd5XTDjzoeigU3B)

### 🇲🇽 Cemex — Asistente de conocimiento técnico (México)
- **Problema:** los agentes de ventas tardaban en encontrar información técnica de productos.
- **Solución:** *Technical Xpert*, un asistente de conocimiento con IA generativa (**Azure OpenAI**), además de Microsoft 365 Copilot y GitHub Copilot en otras áreas.
- **Resultados:** **80% menos tiempo de búsqueda** de información técnica.
- **Por qué funcionó:** conocimiento disperso en documentos → patrón **RAG**.
- 🔗 [Mexico is pioneering AI innovation – Microsoft](https://www.microsoft.com/en-us/microsoft-cloud/blog/2024/10/08/how-mexico-is-pioneering-ai-innovation-for-a-global-future/)

### Ramp — Procesamiento masivo de recibos y facturas (EE. UU.)
- **Problema:** una fintech quería eliminar el trabajo manual de capturar recibos y facturas.
- **Solución:** una herramienta de OCR construida con **modelos preentrenados de Azure AI Document Intelligence**: el usuario manda una foto del recibo y el sistema extrae, categoriza y enriquece los datos.
- **Resultados:** **30,000 horas** de trabajo manual ahorradas al mes; **5 millones de recibos** y **400,000 facturas** procesados al mes; **90%+ de precisión** en los campos; construido en menos de una semana.
- **Por qué funcionó:** usaron un **servicio especializado** (no un LLM genérico) para una tarea bien definida: rapidez, bajo costo y baja latencia.
- 🔗 [Historia de Ramp](https://www.microsoft.com/en/customers/story/23693-ramp-azure-ai-services)

### Woven by Toyota — Sistema multiagente que corrige código (Japón)
- **Problema:** el software de manejo autónomo debe cumplir los estándares MISRA C/C++ (cientos de páginas). En un solo módulo había que corregir unos 60,000 errores.
- **Solución:** un sistema **multiagente** con **Azure OpenAI** (GPT-4o y luego modelos de razonamiento o1/o3-mini) orquestado con AutoGen: un agente **Coder** corrige, un **Reviewer** revisa en ciclo y un **Evaluator** explica su razonamiento y un factor de certeza por cambio.
- **Resultados:** la corrección automática pasó de ~50% con GPT-4o a ~80% con o1; en la prueba de concepto se corrigió automáticamente el **81.5%** de los errores de cumplimiento.
- **Lección clave:** **los humanos toman la decisión final** de aceptar o rechazar cada cambio; el Evaluator reduce el efecto "caja negra".
- 🔗 [Historia de Woven by Toyota](https://www.microsoft.com/en/customers/story/24108-woven-by-toyota-inc-azure-openai)

### Axon — Borradores de reportes policiales (EE. UU.)
- **Problema:** los policías dedican hasta 40% de su turno a redactar reportes.
- **Solución:** *Draft One* transcribe el audio de las cámaras corporales y redacta un **borrador** con **Azure OpenAI**.
- **Resultados:** algunas agencias redujeron hasta **82%** el tiempo en reportes; para la mayoría el tiempo se redujo a la mitad. En un estudio doble ciego, los borradores igualaron o superaron a los reportes escritos por policías en las categorías evaluadas.
- **Salvaguardas:** el oficial **debe revisar y firmar** cada reporte; el modelo está calibrado para apegarse al audio y **no especular**; se evaluaron calidad, precisión y **sesgo**.
- **Lección:** un dominio de alto impacto **sí** puede usar IA si la decisión final es humana y hay evaluación rigurosa.
- 🔗 [Historia de Axon](https://www.microsoft.com/en/customers/story/19236-axon-enterprise-azure)

### Sayvant — Documentación clínica en urgencias (EE. UU.)
- **Problema:** los médicos de urgencias pasan ~20% de su tiempo documentando.
- **Solución:** transcripción de la conversación médico–paciente en más de 30 idiomas y redacción de notas clínicas e instrucciones de alta con **Azure OpenAI**.
- **Resultados:** ~**50,000 horas** clínicas ahorradas; el tiempo de documentación por paciente bajó de ~10 minutos a menos de 90 segundos.
- **Salvaguardas:** los profesionales de salud **revisan** los documentos antes de finalizarlos; diseñado con retroalimentación de cientos de clínicos.
- 🔗 [Historia de Sayvant](https://www.microsoft.com/en/customers/story/23516-sayvant-azure-open-ai-service)

### Sanoma — Pronósticos del clima con voz sintética (Finlandia)
- **Problema:** una radio quería pronósticos locales, pero tener equipos regionales era incosteable y cada pronóstico debía durar exactamente lo mismo.
- **Solución:** **Azure OpenAI GPT-4o** redacta reportes de cinco oraciones a partir de datos meteorológicos oficiales, con una estructura de prompt estricta; una **Custom Neural Voice** de **Azure AI Speech** los lee.
- **Resultados:** **78 pronósticos adicionales al día** para 26 regiones, totalmente automatizados; nuevos ingresos por patrocinio local.
- **Transparencia:** cada transmisión **anuncia que el contenido es generado por IA**, y crearon la voz con locutores que no son figuras famosas.
- 🔗 [Historia de Sanoma](https://www.microsoft.com/en/customers/story/24454-sanoma-azure-ai-speech)

### Discovery Bank — Recomendaciones financieras personalizadas (Sudáfrica)
- **Problema:** escalar experiencias financieras hiperpersonalizadas sin administrar infraestructura compleja.
- **Solución:** *Discovery AI* con modelos ajustados (**fine-tuning**) de **Azure OpenAI en Foundry** (4o-mini y 4.1-mini), Azure API Management como puerta de entrada de todas las peticiones de IA, Key Vault para secretos y Container Apps para hospedar.
- **Resultados:** se **duplicó** la interacción de los clientes con las "siguientes mejores acciones"; la latencia bajó de 5–6 a 1.5–2 segundos.
- **Lección:** el fine-tuning se usó para corregir fallas **específicas** (términos financieros propios, formato de consultas SQL), no para "enseñar datos".
- 🔗 [Historia de Discovery Bank](https://www.microsoft.com/en/customers/story/26157-discovery-bank-azure-openai-in-foundry-models)

### Welcome Account — Asistente multilingüe para personas migrantes (Francia)
- **Problema:** personas refugiadas y migrantes enfrentan años de trámites de vivienda, banca e impuestos en un idioma que no dominan.
- **Solución:** un neobanco con un agente conversacional multilingüe en **Azure OpenAI** que da consejos de manejo de dinero y orienta en trámites.
- **Resultados:** atiende en **7 idiomas**, con planes de ampliarlo.
- **Lección:** la IA como herramienta de **inclusión**; por tratarse de personas en situación vulnerable, priorizaron seguridad y confiabilidad.
- 🔗 [Historia de Welcome Account](https://www.microsoft.com/en/customers/story/21221-welcome-account-azure-open-ai-service)

### Más casos para explorar

| Empresa | Qué hizo | Resultado reportado | Historia |
|---|---|---|---|
| Hughes (EchoStar) | 12 apps en producción con Azure AI Foundry (auditoría de llamadas de ventas, servicio de campo) | 35,000 horas proyectadas de ahorro | [Ver](https://www.microsoft.com/en/customers/story/24300-hughes-azure-ai-foundry) |
| Kuwait Finance House | RiskGPT para análisis de riesgo | Evaluación de crédito de 4–5 días a menos de 1 hora | [Ver](https://www.microsoft.com/en/customers/story/20191-kuwait-finance-house-azure-ai-services) |
| Volvo Group | Extracción y traducción de documentos con Document Intelligence | Más de 10,000 horas manuales ahorradas | [Ver](https://www.microsoft.com/en/customers/story/1703814256939529124-volvo-group-automotive-azure-ai-services) |
| Sandvik | Copiloto de manufactura sobre años de documentación (Azure OpenAI + AI Search) | Hasta 30% más productividad | [Ver](https://www.microsoft.com/en/customers/story/22965-sandvik-azure-open-ai-service) |
| Acentra Health | Generación de cartas clínicas | 11,000 horas de enfermería ahorradas; 99% de aprobación | [Ver](https://www.microsoft.com/en/customers/story/19280-acentra-health-azure) |
| Capita | Asistente virtual de primer nivel | Resuelve 70% de la carga del service desk | [Ver](https://www.microsoft.com/en/customers/story/1363135847046352781-capita) |

🔗 Catálogo completo: [Más de 1,000 historias de transformación con IA – Microsoft](https://www.microsoft.com/en-us/microsoft-cloud/blog/2025/07/24/ai-powered-success-with-1000-stories-of-customer-transformation-and-innovation/)

### Patrones que se repiten en los casos exitosos
1. **Problema concreto y medible** (horas, costo, tiempo de respuesta), no "usar IA porque sí".
2. **Datos no estructurados** convertidos en datos útiles (audio, recibos, documentos).
3. **Humano en el ciclo** en dominios sensibles (policía, salud, código de autos).
4. **Servicio especializado cuando existe** (Ramp eligió Document Intelligence).
5. **Empezar pequeño:** varios casos iniciaron como prueba de concepto de semanas.
6. **Transparencia** con el usuario final (Sanoma anuncia que es IA).

---

## 4. Casos reales: lecciones de cuando la IA **no** debía usarse así

### Tay (Microsoft, 2016): un chatbot sin protecciones expuesto al público
- **Qué pasó:** Microsoft lanzó *Tay*, un chatbot en Twitter que aprendía de sus conversaciones. En menos de 24 horas, un grupo coordinado explotó una vulnerabilidad y logró que publicara contenido ofensivo. Microsoft lo desconectó.
- **Lo que reconoció Microsoft:** se habían preparado para muchos tipos de abuso, pero no para ese, y asumieron **total responsabilidad** por no anticiparlo.
- **Lecciones:**
  - No expongas al público un sistema que **aprende en vivo** de usuarios sin filtros.
  - Haz **pruebas adversariales** (*red teaming*) antes de lanzar.
  - Hoy esto se mitiga con **guardrails**, *prompt shields* y el hecho de que los modelos **no cambian sus pesos** con cada conversación.
- 🔗 [Learning from Tay's introduction – Microsoft](https://blogs.microsoft.com/blog/2016/03/25/learning-tays-introduction/)

### Azure Face (2022): capacidades que Microsoft decidió retirar
- **Qué pasó:** Microsoft **retiró** de Azure Face la inferencia de **estados emocionales** y de atributos como **género y edad**, y puso la **identificación facial** bajo **acceso limitado** (se debe solicitar y justificar).
- **Por qué:** estas inferencias pueden facilitar **estereotipos, discriminación o negación injusta de servicios**; además, no hay consenso científico para definir emociones ni para relacionar de forma confiable una expresión facial con un estado emocional.
- **Lecciones:**
  - Que la tecnología **pueda** hacer algo no significa que **deba**.
  - Algunas capacidades solo se justifican en escenarios controlados (por ejemplo, accesibilidad con Seeing AI).
  - La **detección** de rostros (¿hay una cara?) sigue disponible; la **identificación** (¿quién es?) está restringida.
- 🔗 [Responsible AI investments and safeguards for facial recognition – Microsoft](https://azure.microsoft.com/en-us/blog/responsible-ai-investments-and-safeguards-for-facial-recognition/)

### Lo que tienen en común
| Lección | Principio de IA responsable |
|---|---|
| Probar contra usuarios malintencionados antes de lanzar | Confiabilidad y seguridad |
| No inferir rasgos sensibles de las personas | Equidad, privacidad |
| Restringir usos de alto riesgo | Responsabilidad |
| Reconocer errores públicamente y corregirlos | Responsabilidad, transparencia |

---

## 5. Matriz de decisión

| Pregunta | Si la respuesta es "sí"... |
|---|---|
| ¿Puedo escribir la regla en menos de 10 líneas y no cambia? | No uses IA |
| ¿Existe un servicio especializado (OCR, traducción, detección de idioma, transcripción)? | Úsalo antes que un LLM |
| ¿La respuesta depende de información privada o reciente? | LLM + **RAG** |
| ¿La tarea requiere varios pasos y tocar otros sistemas? | **Agente** (o workflow si los pasos son fijos) |
| ¿Un error puede dañar a una persona o es irreversible? | IA con **humano en el ciclo** |
| ¿Implica inferir rasgos sensibles (emociones, salud, origen)? | Probablemente **no** lo hagas |
| ¿Tienes una métrica clara de éxito (horas, costo, precisión)? | Si no la tienes, defínela antes de construir |
| ¿El volumen justifica el costo por llamada? | Calcula el ROI antes de escalar |

## 6. Estimar si vale la pena (ROI rápido)

Antes de construir, haz una cuenta sencilla con tus propios números:

```python
# Estimación rápida de ROI de un caso de uso de IA (cambia los valores por los tuyos)
casos_por_mes = 20_000            # ej. llamadas, recibos o tickets
minutos_ahorrados_por_caso = 3    # tiempo humano que se ahorra por caso
costo_hora_humana = 150           # MXN
costo_ia_por_caso = 0.40          # MXN (tokens, transcripción, extracción...)
costo_fijo_mensual = 15_000       # MXN (hosting, monitoreo, mantenimiento)

ahorro = casos_por_mes * minutos_ahorrados_por_caso / 60 * costo_hora_humana
costo = casos_por_mes * costo_ia_por_caso + costo_fijo_mensual

print(f"Ahorro mensual estimado: ${ahorro:,.0f} MXN")
print(f"Costo mensual de la IA:  ${costo:,.0f} MXN")
print(f"Beneficio neto:          ${ahorro - costo:,.0f} MXN  ({'✅ vale la pena' if ahorro > costo else '❌ no conviene'})")
```
- **Explicación:** si el beneficio neto es negativo o muy pequeño, probablemente una regla, un servicio especializado o un modelo más pequeño sea mejor opción. No olvides los costos **ocultos**: revisión humana, mantenimiento, evaluación y cumplimiento.

## 7. Riesgos a considerar siempre
- **Alucinaciones:** respuestas convincentes pero falsas → RAG, citas, revisión humana.
- **Sesgo:** resultados injustos para ciertos grupos → evaluación por subgrupos.
- **Privacidad:** filtración de datos personales o confidenciales → detección de PII, permisos.
- **Seguridad:** *prompt injection* y *jailbreaks* → guardrails, pruebas adversariales.
- **Costos:** cada token cuesta → modelos adecuados al tamaño de la tarea, caché.
- **Dependencia del proveedor y versiones:** los modelos se retiran y cambian → evaluaciones automatizadas para detectar regresiones.
- **Sobreconfianza:** usuarios que aceptan todo lo que dice la IA → transparencia y avisos de limitaciones.

## 8. Checklist antes de lanzar un caso de uso de IA
- [ ] El problema y la métrica de éxito están definidos (horas, costo, precisión).
- [ ] Comparé contra la alternativa sin IA (regla, SQL, servicio especializado).
- [ ] Tengo datos con calidad y permiso de uso.
- [ ] Identifiqué a quién puede dañar un error y qué tan grave sería.
- [ ] Hay revisión humana en decisiones de alto impacto o irreversibles.
- [ ] Probé con casos difíciles y con intentos de manipulación (red teaming).
- [ ] Configuré guardrails y protección de datos personales.
- [ ] Los usuarios saben que interactúan con IA y cuáles son sus límites.
- [ ] Hay monitoreo, responsables definidos y un plan para revertir.

### Ejemplos rápidos

| Caso | ¿IA? | Por qué |
|---|---|---|
| Calcular el IVA de una factura | ❌ | Es una fórmula exacta |
| Extraer el RFC y el total de 10,000 facturas escaneadas | ✅ Document Intelligence / Content Understanding | Documentos no estructurados, gran volumen (como Ramp) |
| Responder "¿cuántos días de vacaciones me tocan?" según la política interna | ✅ LLM + RAG | Lenguaje natural sobre información privada (como Cemex o Sandvik) |
| Evaluar automáticamente la calidad de miles de llamadas | ✅ STT + LLM | Audio no estructurado y repetitivo (como Crediclub) |
| Aprobar automáticamente un crédito hipotecario sin revisión | ⚠️ | Alto impacto: requiere transparencia, equidad y revisión humana |
| Detectar el idioma de correos entrantes para enrutarlos | ✅ Azure Language | Servicio especializado, determinista y barato |
| Inferir si un candidato está nervioso por su expresión facial en una entrevista | ❌ | Inferencia emocional poco confiable y discriminatoria (Microsoft la retiró) |
| Publicar un chatbot que aprende en vivo de cualquier usuario | ❌ | Riesgo de manipulación (lección de Tay) |

### Para el examen
- La respuesta correcta suele ser **la que cumple el requisito con el menor esfuerzo y el menor costo**.
- Si hay un servicio especializado que resuelve la tarea, normalmente es mejor opción que un LLM.
- En escenarios de alto impacto, busca la opción con **revisión humana**.
- Si el escenario implica inferir emociones o identificar personas por su rostro, recuerda que son capacidades **restringidas** por IA responsable.

### Recursos
- [Historias de clientes de Microsoft](https://www.microsoft.com/en/customers)
- [Más de 1,000 historias de transformación con IA](https://www.microsoft.com/en-us/microsoft-cloud/blog/2025/07/24/ai-powered-success-with-1000-stories-of-customer-transformation-and-innovation/)
- [Microsoft Responsible AI](https://www.microsoft.com/es-mx/ai/responsible-ai)
