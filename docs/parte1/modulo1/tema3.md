# Tema 3: IA, Machine Learning, Deep Learning, IA Generativa e IA Agéntica

### Descripción
Estos cinco términos se usan como sinónimos, pero son **capas que se contienen una dentro de otra**, como muñecas rusas (matrioskas). Toda IA generativa es deep learning, todo deep learning es machine learning y todo machine learning es IA, pero no al revés. Entender la diferencia te ayuda a **elegir la herramienta correcta** (y la más barata) y a no caer en las trampas del examen.

```mermaid
flowchart TB
    subgraph IA["Inteligencia Artificial — máquinas que imitan capacidades humanas"]
        direction TB
        R["Sistemas de reglas<br/>(IA simbólica)"]
        subgraph ML["Machine Learning — aprende patrones de los datos"]
            direction TB
            C["ML clásico<br/>árboles, regresión, k-means"]
            subgraph DL["Deep Learning — redes neuronales de muchas capas"]
                direction TB
                D["CNN, RNN,<br/>Transformers discriminativos"]
                subgraph GEN["IA Generativa — crea contenido nuevo"]
                    direction TB
                    G["LLMs, difusión,<br/>modelos de video"]
                    subgraph AG["IA Agéntica — razona y actúa con herramientas"]
                        A["Agentes y<br/>sistemas multiagente"]
                    end
                end
            end
        end
    end
```

> [!NOTE]
> La IA agéntica no es un tipo de modelo nuevo: es una **forma de construir sistemas** alrededor de un modelo generativo (modelo + instrucciones + herramientas + memoria). Por eso aparece dentro de la capa generativa.

---

## 1. Inteligencia Artificial (IA)

### Definición
Cualquier técnica que permite a una máquina imitar capacidades humanas: percibir, razonar, decidir, comunicarse. Es el **paraguas**: incluye desde un sistema de reglas de los años 80 hasta un agente con GPT-5.

### IA simbólica (basada en reglas)
Antes del machine learning, la IA eran **reglas escritas por expertos**: los famosos *sistemas expertos*.

```mermaid
flowchart LR
    E[Experto humano] -- escribe --> RB["Base de reglas<br/>SI fiebre Y tos ENTONCES gripe"]
    H[Datos del caso] --> MI[Motor de inferencia]
    RB --> MI
    MI --> S[Conclusión]
```

```python
# IA "clásica": un filtro de spam con reglas escritas a mano
def es_spam(correo: str) -> bool:
    palabras_prohibidas = ["gana dinero", "cura milagrosa", "haz clic aquí"]
    return any(p in correo.lower() for p in palabras_prohibidas)

print(es_spam("¡HAZ CLIC AQUÍ y gana dinero hoy!"))   # True
print(es_spam("G4na d1nero fácil"))                    # False  ← se rompe con variaciones
```
- **Explicación:** funciona para casos previstos, pero cualquier variación ("G4na d1nero") la evade. Mantener miles de reglas es imposible: por eso nació el machine learning.

### Cuándo sigue siendo la mejor opción
- Reglas **pocas, claras y estables** (validar un RFC, calcular el IVA, aplicar una política fija).
- Se necesita **explicabilidad total y auditoría** (regulación).
- No hay datos para entrenar.

---

## 2. Machine Learning (ML / aprendizaje automático)

### Definición
Modelos que **aprenden patrones a partir de datos** en lugar de seguir reglas explícitas. Un humano elige el algoritmo y prepara las **características** (*features*); el algoritmo encuentra la relación entre características y resultado.

### Tipos de aprendizaje

```mermaid
flowchart TD
    ML[Machine Learning] --> S[Supervisado<br/>datos con etiqueta]
    ML --> U[No supervisado<br/>datos sin etiqueta]
    ML --> R[Por refuerzo<br/>prueba, error y recompensa]
    S --> S1["Regresión → número<br/>ej. precio de una casa"]
    S --> S2["Clasificación → categoría<br/>ej. ¿fraude sí/no?"]
    U --> U1["Clustering → grupos<br/>ej. segmentos de clientes"]
    U --> U2["Detección de anomalías<br/>ej. transacción rara"]
    R --> R1["Política de acciones<br/>ej. robot, juegos, logística"]
```

### Algoritmos típicos

| Algoritmo | Tipo | Para qué | Ventaja |
|---|---|---|---|
| Regresión lineal | Supervisado – regresión | Predecir un valor continuo | Simple y explicable |
| Regresión logística | Supervisado – clasificación | Sí/no (aunque se llame "regresión") | Rápida, da probabilidades |
| Árbol de decisión | Supervisado | Clasificar o predecir con reglas aprendidas | Se puede leer como diagrama |
| Random forest / gradient boosting (XGBoost, LightGBM) | Supervisado | Datos tabulares en producción | Muy preciso en tablas |
| Naive Bayes | Supervisado – clasificación | Texto (spam, sentimiento) | Muy rápido |
| K-means | No supervisado | Agrupar | Fácil de entender |
| Isolation Forest | No supervisado | Anomalías | Detecta lo "raro" sin etiquetas |

### El ciclo de vida de un modelo de ML

```mermaid
flowchart LR
    A[1. Definir el problema] --> B[2. Recolectar datos]
    B --> C["3. Preparar datos<br/>limpieza + feature engineering"]
    C --> D[4. Entrenar]
    D --> E["5. Evaluar<br/>exactitud, precisión, recall, F1, RMSE"]
    E -- "no es suficiente" --> C
    E -- "es suficiente" --> F[6. Desplegar]
    F --> G["7. Monitorear<br/>¿cambian los datos?"]
    G -- "deriva de datos" --> B
```

### Feature engineering: la clave del ML clásico
En ML clásico, **un humano decide qué características** ve el modelo. Para detectar spam podrías crear: número de signos de exclamación, porcentaje de mayúsculas, si contiene enlaces, longitud del correo...

```python
# pip install scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

correos = ["gana dinero ya haz clic", "reunión de equipo a las 10", "cura milagrosa oferta",
           "te envío la minuta", "g4na d1nero fácil oferta", "revisión del presupuesto Q3"]
etiquetas = [1, 0, 1, 0, 1, 0]   # 1 = spam

modelo = make_pipeline(TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4)), LogisticRegression())
modelo.fit(correos, etiquetas)

print(modelo.predict(["G4na d1nero con esta oferta"]))     # [1]  ← detecta la variación
print(modelo.predict_proba(["minuta de la reunión"])[0])   # probabilidad [no spam, spam]
```
- **Explicación:**
  - `TfidfVectorizer` con n-gramas de **caracteres** convierte el texto en características numéricas; por eso "g4na d1nero" se parece a "gana dinero".
  - `LogisticRegression` aprende qué características indican spam.
  - Con más ejemplos, el modelo generaliza mucho mejor que las reglas, y **nadie tuvo que escribir la regla**.

### Cuándo usar ML clásico
- Datos **tabulares y estructurados** (ventas, transacciones, sensores, CRM).
- Necesitas una **predicción numérica o una categoría** con buena explicabilidad.
- Tienes datos históricos etiquetados.
- Ejemplos: predecir demanda, *churn* de clientes, scoring de crédito, mantenimiento predictivo, detección de fraude.
- Suele ser **más barato, rápido y explicable** que un LLM para estas tareas.

---

## 3. Deep Learning (aprendizaje profundo)

### Definición
ML basado en **redes neuronales con muchas capas** que **aprenden por sí solas las características** relevantes directamente de los datos crudos (píxeles, ondas de audio, texto).

### La gran diferencia: quién diseña las características

```mermaid
flowchart LR
    subgraph C["Machine learning clásico"]
        direction LR
        I1[Imagen] --> F1["Humano diseña características<br/>bordes, colores, formas"] --> M1[Modelo] --> O1[Gato]
    end
    subgraph D["Deep learning"]
        direction LR
        I2[Imagen] --> N["Red neuronal<br/>capa 1: bordes → capa 2: texturas → capa 3: orejas, ojos → capa N: concepto"] --> O2[Gato]
    end
```

### Arquitecturas principales

| Arquitectura | Año clave | Ideal para | Idea central |
|---|---|---|---|
| **MLP** (perceptrón multicapa) | 1980s | Datos tabulares sencillos | Capas totalmente conectadas |
| **CNN** (red convolucional) | 2012 (AlexNet) | Imágenes | Filtros que detectan patrones locales |
| **RNN / LSTM** | 1997–2014 | Secuencias (texto, audio) | Memoria paso a paso; lentas y "olvidadizas" |
| **Transformer** | 2017 | Texto, imágenes, audio, todo | **Atención**: relaciona todas las partes a la vez, en paralelo |

### ¿Por qué despegó en 2012?
Tres ingredientes coincidieron:

```mermaid
flowchart LR
    A["📚 Datos masivos<br/>internet, ImageNet"] --> X((Deep<br/>Learning))
    B["⚡ Cómputo<br/>GPUs"] --> X
    C["🧮 Algoritmos<br/>ReLU, dropout, backprop eficiente"] --> X
```

### Datos vs. rendimiento
El deep learning necesita muchos datos, pero sigue mejorando donde el ML clásico se estanca:

```mermaid
xychart-beta
    title "Rendimiento según la cantidad de datos (ilustrativo)"
    x-axis "Cantidad de datos" ["Muy pocos", "Pocos", "Medios", "Bastantes", "Muchos", "Muchísimos"]
    y-axis "Rendimiento" 0 --> 100
    line [40, 58, 66, 70, 72, 73]
    line [20, 45, 65, 80, 89, 95]
```
*Línea que se estanca: ML clásico. Línea que sigue subiendo: deep learning.*

### Cuándo usar deep learning (entrenado por ti)
- Datos **no estructurados** (imágenes, audio, texto) y **muchos** ejemplos.
- Tareas de percepción: reconocer productos en fotos, transcribir voz, detectar defectos.
- **En la práctica de la AI-901:** rara vez entrenas una red desde cero; usas modelos de deep learning ya entrenados a través de **Foundry Tools** (Vision, Speech, Language) o del **catálogo de modelos**.

---

## 4. IA Generativa

### Definición
Modelos de deep learning que **crean contenido nuevo** (texto, imágenes, video, audio, código) a partir de un *prompt*, aprendiendo la **distribución** de los datos con los que se entrenaron.

### Discriminativo vs. generativo

```mermaid
flowchart LR
    subgraph DIS["Modelo discriminativo"]
        direction LR
        A1[Foto] --> B1[Modelo] --> C1["'Es un gato' (92%)"]
    end
    subgraph GENE["Modelo generativo"]
        direction LR
        A2["'Un gato astronauta<br/>en acuarela'"] --> B2[Modelo] --> C2[🖼️ Imagen nueva]
    end
```

| | Discriminativo | Generativo |
|---|---|---|
| Pregunta | "¿Qué es esto?" | "Crea algo como esto" |
| Aprende | La frontera entre clases | Cómo se ven los datos (su distribución) |
| Salida | Etiqueta, número, probabilidad | Texto, imagen, audio, video, código |
| Ejemplos | Clasificador de spam, detector de objetos | GPT, Claude, GPT-Image, Sora |

### Familias de modelos generativos

| Familia | Cómo genera | Ejemplos |
|---|---|---|
| **Autorregresivos (LLMs)** | Predicen el siguiente token, uno a la vez | GPT-5, Claude, Llama, Phi, Mistral |
| **Difusión** | Parten de ruido y lo eliminan paso a paso | Stable Diffusion, FLUX |
| **GAN** | Un generador compite contra un discriminador | StyleGAN (rostros sintéticos) |
| **VAE** | Comprimen a un espacio latente y reconstruyen | Componentes de modelos de difusión |
| **Multimodales nativos** | Un mismo modelo entiende y genera varias modalidades | GPT-Image, modelos de audio en tiempo real |

### Cómo se construye un LLM moderno

```mermaid
flowchart LR
    A["1. Preentrenamiento<br/>billones de tokens de texto<br/>predecir el siguiente token<br/>(autosupervisado)"] --> B["Modelo base<br/>completa texto, no sigue instrucciones"]
    B --> C["2. Ajuste por instrucciones (SFT)<br/>ejemplos de pregunta → buena respuesta"]
    C --> D["3. Alineación<br/>RLHF / DPO con preferencias humanas"]
    D --> E["Modelo de chat / instruct<br/>útil, honesto, más seguro"]
    E --> F["4. Tu adaptación<br/>prompts · RAG · fine-tuning"]
```

### Fortalezas y limitaciones

| Fortalezas | Limitaciones |
|---|---|
| Entiende y genera lenguaje natural en muchos idiomas | **Alucinaciones**: inventa con seguridad |
| Una sola herramienta para cientos de tareas | Conocimiento limitado a su **fecha de corte** |
| No requiere entrenamiento: basta un prompt | Salida **no determinista** |
| Resume, traduce, redacta, programa | Costo por token y latencia |
| Multimodal (texto + imagen + audio) | Sesgos heredados de los datos |

### Cuándo usarla
Redactar, resumir, traducir, conversar, generar código o imágenes, extraer información de texto libre: tareas **abiertas** donde hay muchas respuestas válidas.

### Cuándo NO
Cuando necesitas un resultado **exacto, determinista y auditable** (un cálculo fiscal, una regla de negocio fija) o cuando un servicio especializado lo hace más barato y consistente (detectar idioma, OCR).

---

## 5. IA Agéntica

### Definición
Sistemas que usan un modelo generativo como "cerebro" para **razonar, planear y actuar** usando herramientas, de forma (semi)autónoma, hasta cumplir un **objetivo**.

### Componentes de un agente

```mermaid
flowchart TB
    U[👤 Usuario / evento] --> AG
    subgraph AG["Agente"]
        direction TB
        M["🧠 Modelo (LLM)<br/>razona y decide"]
        I["📋 Instrucciones<br/>rol, reglas, objetivo"]
        MEM["🗂️ Memoria<br/>conversación y estado"]
    end
    AG <--> K["📚 Herramientas de conocimiento<br/>RAG, Foundry IQ, búsqueda web"]
    AG <--> T["🛠️ Herramientas de acción<br/>APIs, MCP, correo, Code Interpreter"]
    AG --> R[✅ Resultado / acción completada]
```

### El ciclo del agente (patrón ReAct: razonar → actuar → observar)

```mermaid
flowchart LR
    O[Objetivo] --> P["🤔 Razonar<br/>¿qué necesito?"]
    P --> A["🛠️ Actuar<br/>llamar herramienta"]
    A --> OB["👀 Observar<br/>resultado de la herramienta"]
    OB --> Q{"¿Objetivo<br/>cumplido?"}
    Q -- No --> P
    Q -- Sí --> F[Responder]
```

```python
# Simulación del ciclo de un agente (sin nube) para entender la lógica
herramientas = {
    "consultar_politica": lambda dias: "100%" if dias > 7 else "50%" if dias >= 2 else "0%",
    "crear_reembolso":    lambda pct: f"Reembolso del {pct} creado con folio R-1042",
}

def agente(objetivo, dias_anticipacion):
    print(f"🎯 Objetivo: {objetivo}")
    # Paso 1: razonar -> necesito saber la política
    print("🤔 Necesito saber cuánto se reembolsa según la anticipación")
    pct = herramientas["consultar_politica"](dias_anticipacion)          # actuar
    print(f"👀 Observación: corresponde {pct}")                          # observar
    # Paso 2: razonar -> ya sé el porcentaje, ahora ejecuto la acción
    if pct == "0%":
        return "No aplica reembolso según la política."
    print("🤔 Ya tengo el porcentaje; ahora creo el reembolso")
    return herramientas["crear_reembolso"](pct)

print("✅", agente("Cancelar el viaje y pedir reembolso", dias_anticipacion=5))
```
- **Explicación:** en un agente real **el LLM decide** qué herramienta llamar, con qué parámetros y cuándo parar; aquí lo simulamos con `if` para ver el flujo. En Foundry las herramientas son MCP, OpenAPI, funciones, Code Interpreter o Foundry IQ.

### Workflow vs. agente
No todo lo que usa un LLM debe ser un agente:

| | Workflow (flujo fijo) | Agente |
|---|---|---|
| Quién decide los pasos | **Tu código** | **El modelo** |
| Predecibilidad | Alta | Menor |
| Costo y latencia | Menores | Mayores (varias llamadas) |
| Ideal para | Procesos repetibles y conocidos | Tareas abiertas con caminos variables |
| Ejemplo | Siempre: extraer factura → validar → guardar | "Resuelve la queja de este cliente" |

### Niveles de autonomía

```mermaid
flowchart LR
    L1["Nivel 1<br/>Asistente<br/>sugiere, el humano actúa"] --> L2["Nivel 2<br/>Copiloto<br/>actúa con aprobación"]
    L2 --> L3["Nivel 3<br/>Agente supervisado<br/>actúa y reporta"]
    L3 --> L4["Nivel 4<br/>Agente autónomo<br/>actúa solo en un dominio acotado"]
```
A mayor autonomía, más importantes son los **guardrails**, la **aprobación humana** en acciones irreversibles y la **observabilidad**.

### Sistemas multiagente
Varios agentes especializados se coordinan (un orquestador reparte el trabajo):

```mermaid
sequenceDiagram
    actor U as Usuario
    participant O as Agente orquestador
    participant I as Agente investigador
    participant A as Agente analista
    participant E as Agente ejecutor
    U->>O: "Prepara la propuesta para Contoso"
    O->>I: Busca historial del cliente
    I-->>O: Compras, contactos, tickets
    O->>A: Calcula precio y margen
    A-->>O: Propuesta numérica
    O->>E: Genera documento y agenda reunión
    E-->>O: Documento + invitación enviada
    O-->>U: "Listo: propuesta y reunión el jueves"
```

### Cuándo usarla
Procesos de **varios pasos** que requieren **decidir qué hacer** y **tocar otros sistemas**: atender una solicitud de reembolso completa, investigar y redactar un reporte, resolver tickets de soporte.

### Cuándo NO
Si el flujo es siempre el mismo y predecible, un **workflow** tradicional (o un solo prompt) es más barato, rápido y confiable.

---

## 6. Comparación global

| Criterio | IA basada en reglas | ML clásico | Deep learning | IA generativa | IA agéntica |
|---|---|---|---|---|---|
| ¿Aprende de datos? | ❌ | ✅ | ✅ | ✅ | ✅ (usa un modelo que aprendió) |
| Datos típicos | Ninguno | Tabulares | Imágenes, audio, texto | Texto, imagen, multimodal | Cualquiera + sistemas externos |
| Cantidad de datos para entrenar | — | Cientos a miles | Miles a millones | Billones de tokens (lo hace el proveedor) | — (usa modelos existentes) |
| Cómputo | Mínimo | CPU | GPU | Muchas GPUs | Varias llamadas al modelo |
| Explicabilidad | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ (mejora con trazas) |
| Salida | Decisión fija | Número o categoría | Etiqueta, cajas, transcripción | Contenido nuevo | Acciones + contenido |
| Determinista | ✅ | ✅ | ✅ | ❌ | ❌ |
| En Microsoft | Lógica de tu app | Azure Machine Learning | Foundry Tools | Catálogo de modelos de Foundry | Foundry Agent Service |

## 7. Árbol de decisión

```mermaid
flowchart TD
    Q1{"¿Puedes escribir la regla<br/>en pocas líneas y no cambia?"} -- Sí --> R1[✅ Reglas / código tradicional]
    Q1 -- No --> Q2{"¿Tus datos son tablas<br/>y quieres un número o categoría?"}
    Q2 -- Sí --> R2[✅ Machine learning clásico]
    Q2 -- No --> Q3{"¿Es una tarea de percepción bien definida?<br/>OCR, transcribir, detectar idioma, objetos"}
    Q3 -- Sí --> R3["✅ Deep learning preentrenado<br/>(Foundry Tools)"]
    Q3 -- No --> Q4{"¿Necesitas generar, resumir<br/>o conversar en lenguaje natural?"}
    Q4 -- No --> R2
    Q4 -- Sí --> Q5{"¿Debe ejecutar varios pasos<br/>y usar otros sistemas?"}
    Q5 -- No --> R4["✅ IA generativa<br/>(prompt + RAG si hay datos privados)"]
    Q5 -- Sí --> Q6{"¿Los pasos son siempre<br/>los mismos?"}
    Q6 -- Sí --> R5[✅ Workflow con LLM]
    Q6 -- No --> R6[✅ IA agéntica]
```

## 8. El mismo problema, resuelto en cada capa

**Problema:** una aseguradora recibe miles de correos de clientes al día.

| Capa | Solución | Resultado |
|---|---|---|
| Reglas | Si el asunto contiene "siniestro" → área de siniestros | Rápido, pero falla con "choqué mi carro" |
| ML clásico | Clasificador entrenado con correos históricos etiquetados | Enruta por categoría con 90%+ de exactitud |
| Deep learning | Modelo preentrenado de NLP detecta idioma, sentimiento y entidades (póliza, fecha) | Prioriza clientes molestos y extrae el número de póliza |
| IA generativa | LLM + RAG con las pólizas redacta una respuesta personalizada | Borrador de respuesta en segundos para que lo revise un humano |
| IA agéntica | Agente que lee el correo, consulta la póliza, abre el siniestro en el sistema, agenda al ajustador y responde | Caso resuelto de principio a fin; humano aprueba los pasos críticos |

En una solución real **se combinan**:

```mermaid
flowchart LR
    C[📧 Correo] --> R["Reglas<br/>filtro de remitentes bloqueados"]
    R --> L["Azure Language<br/>idioma, PII, sentimiento"]
    L --> CL["Clasificador ML<br/>categoría y prioridad"]
    CL --> AG["Agente (LLM)<br/>RAG con pólizas + herramientas"]
    AG --> H{"¿Acción<br/>irreversible?"}
    H -- Sí --> HU[👤 Aprobación humana]
    H -- No --> OK[✅ Respuesta y acciones]
    HU --> OK
```

## Tabla de decisión rápida

| Necesito... | Usa |
|---|---|
| Validar que un RFC tenga el formato correcto | Reglas (regex) |
| Predecir ventas del próximo mes con datos históricos | Machine learning (regresión) |
| Segmentar clientes sin categorías previas | Machine learning (clustering) |
| Detectar defectos en fotos de una línea de producción | Deep learning (visión) |
| Detectar el idioma de miles de correos de forma consistente | Servicio especializado (Azure Language), no un LLM |
| Responder preguntas de clientes en lenguaje natural | IA generativa (+ RAG) |
| Atender una solicitud completa: entender, consultar sistemas y ejecutar acciones | IA agéntica |

### Para el examen
- "Crear contenido nuevo a partir de un prompt" → **IA generativa**.
- "Usar herramientas para completar tareas de forma autónoma" → **agente**.
- "Agente que define su rol" → **instrucciones**; "agente que consulta datos o actúa" → **herramientas**.
- "Varios agentes especializados colaborando" → **sistema multiagente**.
- "Predecir un número / una categoría / agrupar" → **regresión / clasificación / clustering** (ML).
- "LLM vs. SLM": LLM = más datos y parámetros, generaliza; SLM = enfocado, barato, ideal en dispositivos.
- Distractor común: proponer un LLM para una tarea que un servicio especializado o una regla resuelve más barato.

### Recursos
- [Introducción a los conceptos de machine learning – Microsoft Learn](https://learn.microsoft.com/es-es/training/modules/fundamentals-machine-learning/)
- [Building effective agents – Anthropic](https://www.anthropic.com/research/building-effective-agents)
- [AI Agents for Beginners – Microsoft](https://github.com/microsoft/ai-agents-for-beginners)
- [Ligera introducción a Deep Learning (acordeón AI-900)](https://github.com/josejesusguzman/acordeon-ia-900/blob/main/docs/intro_deep_learning.md)
