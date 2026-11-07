# ¿Cómo es presentar una certificación de Microsoft? Tips y consideraciones

Antes de entrarle al contenido, te conviene saber **contra qué te vas a enfrentar**. La AI-901 es un examen *Fundamentals*, pero es distinto a la AI-900: más de la mitad es de implementación con Microsoft Foundry y Python.

He hecho 15 exámenes de certificación de Microsoft en 11 años de carrera en tecnología y he aprobado 13 de ellos. Cada examen es diferente, pero los patrones entre las certificaciones de Microsoft se repiten. Aquí comparto algunos tips y hacks que me han servido para aprobar los exámenes de certificación de Microsoft.

## Ficha técnica del examen

| Dato | Valor |
|------|-------|
| **Nombre oficial** | Microsoft Certified: Azure AI Fundamentals |
| **Código** | AI-901 |
| **Nivel** | Principiante (Fundamentals) |
| **Calificación aprobatoria** | 700 de 1,000 |
| **Idiomas** | Incluye español (si no está en tu idioma puedes pedir 30 minutos extra) |
| **Proveedor** | Pearson VUE |
| **Producto evaluado** | Microsoft Foundry (modelos, agentes, Foundry Tools, Foundry IQ) |
| **Evaluación de práctica** | Gratuita, en la [página de la certificación](https://learn.microsoft.com/es-es/credentials/certifications/azure-ai-fundamentals/) (AI Skills Navigator) |

> [!NOTE]
> Revisa la duración y el formato exactos al agendar tu examen; Microsoft los puede ajustar.

## Habilidades que se evalúan

1. **Identificar conceptos y capacidades de IA (40–45%)**: IA responsable, componentes y configuración de modelos, y cargas de trabajo (generativa y agéntica, texto, voz, visión y extracción de información).
2. **Implementar soluciones de IA con Microsoft Foundry (55–60%)**: apps y agentes generativos, texto y voz, visión y generación de imágenes, y extracción de información con Content Understanding.

Revisa siempre la [guía de estudio oficial](https://learn.microsoft.com/es-es/credentials/certifications/resources/study-guides/ai-901): ahí aparecen los cambios recientes.

> [!IMPORTANT]
> Aquí **sí** te van a preguntar por código: clases, métodos, parámetros, endpoints y autenticación (llave vs. Microsoft Entra ID). No necesitas memorizar cada línea, pero sí saber **leer** un script de Python con el SDK de Foundry y detectar qué le falta o qué está mal.

## Requisitos previos

Microsoft pide conocimiento conceptual de IA, habilidades técnicas básicas, sintaxis de Python y familiaridad con recursos de Azure. En la práctica eso significa que te muevas sin problema en:

- El portal de Azure (suscripciones, grupos de recursos, recursos)
- El portal de Microsoft Foundry (proyectos, deployments, Playground, agentes)
- Python básico (entornos virtuales, `pip`, variables de entorno, llamadas a SDKs)
- Conceptos de APIs REST (endpoint, headers, JSON)

## Tips para el día del examen

1. **Haz la evaluación de práctica más de una vez.** Es gratuita, ilimitada y las preguntas rotan. Si sacas menos de 85% no te presentes todavía.
2. **Lee el escenario completo antes de las opciones.** La pista suele estar en la restricción: "de forma consistente", "con el menor costo", "sin escribir código", "en tiempo real", "varios agentes".
3. **Cuidado con las respuestas "casi correctas".** Suelen cambiar una sola palabra: *modelo* vs *agente*, *Azure Language* vs *LLM*, *Foundry IQ* vs *Work IQ*, *nombre del modelo* vs *nombre del deployment*, *endpoint del proyecto* vs *endpoint del modelo*.
4. **No te atores.** Marca la pregunta y sigue; regresa al final.
5. **Prepara tu espacio si lo haces en línea** (abajo tienes la lista completa).
6. **Traduce con cuidado.** El examen y Microsoft Learn se redactan en inglés y la traducción al español a veces es rara ("indicaciones" = *prompts*, "implementación" = *deployment*, "fundamentación" = *grounding*). Aprende los términos en ambos idiomas.

Las preguntas son de opción múltiple, de arrastrar y soltar, de completar espacios en blanco con las opciones que te dan, de escenarios o casos de estudio.

> [!WARNING]
> El examen está diseñado para confundirte, así que Microsoft mañosamente puede hacer alguna de estas acciones en las preguntas:
>
> - Poner una respuesta que es correcta pero no es la mejor.
> - Poner una respuesta que es correcta pero no es la más completa.
> - Colocar opciones que no existen.
> - Colocar nombres de servicios antiguos (*Azure AI Studio / Azure AI Foundry* → **Microsoft Foundry**; *Cognitive Services / Azure AI Services* → **Foundry Tools**; *Azure AD* → **Microsoft Entra ID**; *Form Recognizer* → **Document Intelligence**).
> - Colocar dos opciones extremadamente parecidas.
> - En el planteamiento del problema una sola oración o palabra puede cambiar el sentido de la pregunta y por ende la respuesta correcta.

> [!TIP]
> Haz las prácticas y ejercicios que te indica Microsoft Learn: te pueden preguntar sobre el orden de pasos, qué configuración falta para hacer determinada acción o qué servicio de Azure es el que se debe usar.

---

## 1. Antes del examen (en línea con Pearson VUE)


- Ten a la mano tu identificación oficial
- Dónde debes hacer tu examen:
  - En un cuarto donde no haya nadie más
  - Necesitas una computadora con webcam, micrófono y altavoces (audífonos no están permitidos)
  - Si tienes más de un monitor, desconecta todos los demás y quédate solo con uno
  - Tu escritorio o mesa debe estar totalmente despejado y no tener más que tu equipo de cómputo, bocinas, mouse y/o teclado
  - El cuarto debe estar bien iluminado
- Corre antes el [system test de Pearson VUE](https://home.pearsonvue.com/) en la misma computadora y red que vas a usar
- Debes estar media hora antes de la hora agendada de tu examen para hacer el proceso de registro
- Tu celular debe estar al alcance pero no a la vista del examinador
- Asegúrate de que no entre nadie al cuarto durante el examen
- No uses relojes ni ropa de manga larga
- Recoge tu cabello de tal forma que se vean tus orejas

- Con calma, recuerda que has estudiado, que te has preparado y que tú puedes con ello. **Si otras personas han podido, ¿por qué tú no?**

---

## 2. Cómo responder

1. Lee la pregunta **COMPLETAMENTE** y entiende lo que se pide.
2. Vuelve a leer la pregunta.
3. Lee las opciones de respuesta y descarta las que sabes que son incorrectas.
4. Si no sabes la respuesta, marca la pregunta para revisarla después y sigue con el examen.
5. Debes estar dispuesto a regresar a una pregunta anterior, porque una pregunta posterior puede darte una pista para responderla.

> [!IMPORTANT]
> **SIEMPRE**
>
> Aunque el examen no te lo pida explícitamente, responde pensando en la solución más económica y más sencilla que cumpla con los requerimientos del problema. Microsoft quiere que elijas la mejor opción, no la más complicada.
>
> **Responde como alguien perezoso y tacaño**

Responde a tu tiempo y a tu ritmo. Tu examen no vale menos si usaste todo el tiempo disponible o si lo terminaste en 10 minutos. Lo importante es que respondas correctamente. No te quedes atorado en una pregunta que no sabes responder y **NO DEJES NINGUNA PREGUNTA SIN RESPONDER.**

---

## 3. Tips de mentalidad

1. No te estreses, no es un examen de vida o muerte. Si no pasas, puedes volver a intentarlo después de 24 horas.
2. Confía en tu conocimiento y experiencia. Has estudiado para este examen, así que tienes las herramientas necesarias para aprobarlo.
3. Responde como alguien perezoso y tacaño.
4. Piensa que es un examen de certificación y debe ser complicado para que no cualquier persona lo pueda conseguir; si no fuese así, no valdría nada.
5. Toma en cuenta 2 horas o más, ya que se cuenta el tiempo en el que validan tu información, y el tiempo del examen inicia en el momento en el que **TÚ** le das **INICIAR**.

---

## 4. Después del examen

- Sabrás si aprobaste en cuanto envíes el examen. No se redondea: con 699 puntos no apruebas.
- En la hoja final tienes tu desempeño por tema: anótalo para saber qué reforzar.
- Si aprobaste, te llegará un correo y tu insignia en Credly en un máximo de 48 horas.
- Tu historial de certificaciones está en tu perfil: https://learn.microsoft.com/es-es/users/
