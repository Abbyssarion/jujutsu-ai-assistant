# Tema 1: Cuándo y cómo usar clasificación, detección, segmentación y análisis contextual de imágenes

### Descripción
Las cuatro tareas de visión son como **niveles de zoom** sobre la misma foto. Elegir la correcta depende de qué pregunta de negocio quieres responder y de cuánto detalle necesitas, porque más detalle implica más datos de entrenamiento, más cómputo y más costo.

Analogía con el súper:
- **Clasificación:** "¿Qué fruta pusiste en la báscula?" → "Manzana".
- **Detección:** "¿Qué hay en la banda de la caja y dónde está cada cosa?" → 3 cajas con etiqueta.
- **Segmentación:** "¿Exactamente qué píxeles son el plátano?" → contorno exacto.
- **Análisis contextual:** "¿Qué está pasando?" → "Un cliente pagando frutas en la caja".

Otra forma de verlo: es la diferencia entre decir **"hay un perro"**, **"hay un perro aquí"** (señalando con el dedo un recuadro), **"este es exactamente el perro"** (recortándolo con tijeras) y **"el perro está persiguiendo una pelota en el parque y parece contento"** (contar la historia).

Lectura oficial: [Introducción a los conceptos de computer vision – Microsoft Learn](https://learn.microsoft.com/es-es/training/modules/introduction-computer-vision/)

---

### Aspectos Clave

#### 1. Clasificación de imágenes
- **Qué devuelve:** una (o varias) etiquetas con probabilidad para **toda** la imagen. No dice dónde está nada.
- **Cuándo usarla:** la imagen tiene un solo sujeto principal, o solo te importa la categoría general.
- **Ejemplos:** identificar el tipo de fruta en una báscula; clasificar radiografías como normal/anormal; saber si una foto de producto cumple con las reglas del catálogo.
- **Dos variantes:**
  - **Multiclase:** exactamente una respuesta ("manzana" *o* "naranja"). Capa de salida **softmax**: las probabilidades suman 1.
  - **Multietiqueta:** varias respuestas a la vez ("playa", "atardecer", "personas"). Una **sigmoide** por clase: cada probabilidad es independiente.
- **Salida típica:**
  ```json
  { "predicciones": [ {"etiqueta": "manzana", "probabilidad": 0.94},
                      {"etiqueta": "naranja", "probabilidad": 0.05} ] }
  ```

#### 2. Detección de objetos
- **Qué devuelve:** cada objeto con su clase, confianza y **bounding box** (x, y, ancho, alto).
- **Cuándo usarla:** hay **varios objetos** y te importa **cuántos y dónde**.
- **Ejemplos:** autocobro con varios productos; contar personas en un pasillo; detectar si un trabajador usa casco; huecos en anaqueles.
- **Salida típica:**
  ```json
  { "objetos": [
      {"etiqueta": "manzana", "confianza": 0.91, "caja": {"x": 34, "y": 50, "w": 120, "h": 115}},
      {"etiqueta": "plátano", "confianza": 0.88, "caja": {"x": 210, "y": 40, "w": 180, "h": 90}} ] }
  ```
- **Limitación clave:** el rectángulo incluye fondo. Para objetos delgados, diagonales o con forma irregular (un plátano, una grieta, una carretera) la caja puede ser varias veces más grande que el objeto (lo mides en el código 2).

#### 3. Segmentación
- **Qué devuelve:** una **máscara**: cada píxel tiene asignada una clase.
- **Cuándo usarla:** necesitas la **forma exacta**, medir áreas o separar objeto y fondo.
- **Ejemplos:** medir el área de un tumor en imagen médica; autos autónomos que distinguen carretera, banqueta y peatón; quitar el fondo de una foto; agricultura (porcentaje de hoja con plaga).
- **Tres variantes:**

  | Variante | Qué distingue | Ejemplo: foto con 3 manzanas sobre una mesa |
  |---|---|---|
  | **Semántica** | La **clase** de cada píxel | Todos los píxeles de manzana pintados del mismo color; no sabe cuántas son |
  | **De instancias** | Cada **objeto individual** (solo objetos contables) | Manzana 1 roja, manzana 2 azul, manzana 3 verde; la mesa se ignora |
  | **Panóptica** | Ambas cosas: instancias de objetos + clase de fondos ("cosas" y "regiones") | Cada manzana por separado **y** la mesa y la pared como regiones |

#### 4. Análisis contextual de imágenes (multimodal)
- **Qué devuelve:** **lenguaje natural**: descripciones, etiquetas, respuestas a preguntas sobre la imagen.
- **Cuándo usarla:** quieres entender relaciones y actividades, generar texto alternativo, o hacer preguntas abiertas ("¿hay algún riesgo de seguridad en esta foto?").
- **Ejemplos:** *alt text* automático para accesibilidad; moderar fotos de usuarios; analizar capturas de pantalla, gráficas o diagramas; agentes que "ven".
- **En Foundry:** modelos como GPT-4.1 o GPT-5.x con entrada de imagen ([Parte 2, Módulo 5](../../parte2/modulo5/tema2.md)).
- **Superpoder:** *zero-shot*. No necesitas entrenar ni etiquetar nada; cambias la pregunta y obtienes otra tarea. Hoy el mismo modelo puede clasificar ("¿es perro o gato?"), contar ("¿cuántas personas hay?") y razonar ("¿por qué este anaquel se ve desordenado?").
- **Debilidad:** no es un instrumento de medición. Sus coordenadas y conteos de objetos pequeños o numerosos son menos confiables que los de un detector entrenado, y cada llamada cuesta y tarda más.

---

### Comparativa general: las cuatro tareas lado a lado

| Criterio | Clasificación | Detección | Segmentación | Análisis contextual (multimodal) |
|---|---|---|---|---|
| **Pregunta que responde** | ¿Qué es? | ¿Qué hay, cuántos y dónde? | ¿Exactamente qué píxeles son cada cosa? | ¿Qué está pasando? ¿Qué significa? |
| **Salida** | Etiqueta(s) + probabilidad | Etiquetas + cajas + confianza | Máscara por píxel | Texto libre o JSON |
| **Precisión de ubicación** | Ninguna | Rectángulo | Píxel | Semántica (aproximada) |
| **Costo de etiquetar datos** | Bajo (una etiqueta por imagen, segundos) | Medio (dibujar cajas, ~10–30 s por objeto) | Alto (pintar contornos, minutos por imagen) | Ninguno con un modelo preentrenado |
| **Cómputo en inferencia** | Muy bajo | Bajo–medio | Medio–alto | Alto (modelo grande en la nube) |
| **Latencia típica** | Milisegundos | Milisegundos (tiempo real en video) | Decenas de ms | Segundos |
| **¿Corre en el borde (cámara, celular)?** | Sí, fácilmente | Sí (YOLO, SSD, MobileNet) | Sí con modelos ligeros | Rara vez; normalmente en la nube |
| **Cuenta objetos** | No | **Sí** | Sí (instancias) | Aproximado |
| **Mide áreas o formas** | No | Solo aproximado (caja) | **Sí** | No |
| **Entiende relaciones y acciones** | No | No | No | **Sí** |
| **Métrica de evaluación** | Accuracy, precisión, recall, F1 | **mAP** (con IoU ≥ 0.5) | **IoU** / Dice por clase | Evaluación humana, groundedness, rúbricas |
| **Arquitecturas típicas** | CNN (ResNet), ViT | YOLO, Faster R-CNN, DETR | U-Net, Mask R-CNN, SAM | GPT-4.1, GPT-5.x, Phi-4-multimodal, Florence |

> 💡 **Regla mental:** cada nivel de zoom hacia la derecha te da más detalle a cambio de más datos, más cómputo y más latencia. Siempre empieza preguntando: **¿cuál es el nivel de detalle mínimo que resuelve el problema de negocio?**

---

### Comparativa por pregunta de negocio

| Si la pregunta es... | Usa | ¿Por qué no otra? |
|---|---|---|
| "¿Esta pieza está defectuosa, sí o no?" | Clasificación | No necesitas saber dónde está el defecto, solo aceptar o rechazar la pieza |
| "¿Dónde está el defecto para que el operador lo revise?" | Detección | Clasificación no localiza; segmentación es más cara de lo necesario |
| "¿Qué tan grande es la grieta? ¿Supera los 2 mm?" | Segmentación | La caja de una grieta diagonal es casi toda fondo: el área sería falsa |
| "¿Cuántas personas hay en la fila?" | Detección | Clasificación no cuenta; segmentación es excesiva para contar |
| "¿Cuántas células hay y cuál es el tamaño de cada una?" | Segmentación de instancias | Las células se tocan entre sí; las cajas se encimarían |
| "¿Qué porcentaje del terreno es bosque, agua o urbano?" | Segmentación semántica | Te interesa la superficie por clase, no los objetos individuales |
| "Describe esta foto para una persona ciega" | Multimodal | Ninguna otra tarea produce frases con contexto |
| "¿Este anuncio cumple las políticas de la marca?" | Multimodal | Requiere razonar sobre texto, logos y composición juntos |
| "¿Qué etiquetas pongo a estas 100,000 fotos del archivo?" | Clasificación multietiqueta (o tags de Azure Vision) | Multimodal funcionaría pero costaría mucho más por imagen |
| "¿El trabajador lleva casco **y** chaleco?" | Detección (o clasificación multietiqueta sobre el recorte de cada persona) | Hay varias personas: primero hay que separarlas |
| "Recorta el producto y quita el fondo para el e-commerce" | Segmentación | Necesitas el contorno exacto del producto |
| "¿Qué dice esta gráfica de ventas?" | Multimodal | Leer ejes, tendencias y conclusiones es razonamiento, no localización |

---

### Comparativa por industria (casos reales típicos)

| Industria | Clasificación | Detección | Segmentación | Multimodal |
|---|---|---|---|---|
| **Retail** | Reconocer la fruta en la báscula de autocobro | Contar productos en el anaquel, detectar huecos (*out-of-stock*) | Recortar productos para el catálogo en línea | Verificar que el planograma y las promociones se ven bien; responder preguntas del cliente sobre una foto |
| **Manufactura** | Pieza OK / defectuosa | Ubicar tornillos faltantes o rayones | Medir el área de una mancha o la longitud de una grieta | Explicar en lenguaje natural qué falla tiene la pieza para el reporte de calidad |
| **Salud** | Radiografía normal / con hallazgo | Localizar nódulos en una tomografía | Delimitar un tumor para medir su volumen y planear radioterapia | Generar un borrador del reporte para que el radiólogo lo revise (siempre con supervisión humana) |
| **Agricultura** | ¿La hoja está sana o enferma? ¿Qué enfermedad? | Contar frutos o plantas desde un dron | % de hoja dañada; superficie de cultivo vs maleza | Recomendar acciones a partir de la foto y el contexto del agricultor |
| **Seguridad industrial** | ¿La zona está despejada? | Personas sin casco, sin chaleco, en zona restringida | Zonas de peligro exactas en el piso | "¿Ves algún riesgo en esta foto de la obra?" |
| **Autos y movilidad** | Tipo de señal de tránsito | Peatones, autos, ciclistas (con distancia) | Carretera, banqueta, carril (dónde se puede manejar) | Explicar una escena compleja o un incidente a partir del video |
| **Seguros** | ¿El auto tiene daño o no? | Ubicar cada abolladura | Área de cada daño para estimar el costo | Redactar el resumen del siniestro a partir de las fotos |
| **Medios y redes sociales** | ¿Contenido apto o no apto? | Logos de marcas en un video (patrocinios) | Quitar o difuminar el fondo en videollamadas | *Alt text*, moderación con contexto, resúmenes de video |
| **Documentos** | Tipo de documento (INE, factura, recibo) | Ubicar firma, sello o fotografía | Separar texto de imágenes en un escaneo | Extraer campos y responder preguntas sobre el documento (ver OCR en el siguiente tema y Content Understanding) |

---

### Comparativas finas: cuándo usar cada variante

#### Clasificación multiclase vs multietiqueta

| | Multiclase | Multietiqueta |
|---|---|---|
| Respuesta | Exactamente **una** clase | **Cero, una o varias** clases |
| Capa de salida | Softmax (suma = 1) | Sigmoide por clase (cada una entre 0 y 1) |
| Úsala cuando... | Las clases son **mutuamente excluyentes**: tipo de fruta en la báscula, dígito escrito a mano, especie de flor | Las etiquetas **pueden coexistir**: "playa + atardecer + personas", géneros de una película, atributos de un producto (rojo, de manga larga, de algodón) |
| Error típico | Forzar una sola respuesta cuando hay varias cosas en la foto | No ajustar el umbral por clase (0.5 no siempre es el mejor) |

#### Detección vs segmentación de instancias

| | Detección | Segmentación de instancias |
|---|---|---|
| Ubicación | Caja | Contorno exacto + caja |
| Etiquetado | Rápido (2 clics por objeto) | Lento (polígonos) |
| Velocidad | Más rápida | Más lenta |
| Úsala cuando... | Solo necesitas **contar, rastrear o señalar** objetos; los objetos son más o menos "rectangulares" (personas, autos, cajas) | Necesitas **medir, recortar o separar objetos que se tocan**; formas irregulares (células, grietas, piezas encimadas, frutos en racimo) |

#### Segmentación semántica vs instancias vs panóptica

| Escenario | Variante recomendada | Razón |
|---|---|---|
| % de una imagen satelital que es bosque | Semántica | No importa cuántos árboles hay, sino cuánta superficie |
| Quitar el fondo de una foto de producto | Semántica (2 clases: objeto / fondo) | Solo hay que separar primer plano y fondo |
| Contar y medir cada célula de una muestra | Instancias | Cada célula es un objeto independiente |
| Auto autónomo | Panóptica | Necesita los peatones uno por uno **y** las regiones de carretera y banqueta |

#### Modelo especializado vs modelo multimodal

Esta es la decisión más importante hoy, porque los modelos multimodales pueden hacer "un poco de todo".

| Criterio | Modelo especializado (clasificador, detector o segmentador entrenado) | Modelo multimodal (GPT-4.1 / GPT-5.x en Foundry) |
|---|---|---|
| **Datos necesarios** | Cientos o miles de imágenes etiquetadas | Ninguno (zero-shot) o unos cuantos ejemplos en el prompt |
| **Tiempo para el primer prototipo** | Días o semanas | Minutos |
| **Costo por imagen** | Muy bajo (fracciones de centavo, o gratis en el borde) | Mayor (pagas tokens de entrada por la imagen y de salida por el texto) |
| **Latencia** | Milisegundos; sirve para video en tiempo real | Segundos; no sirve para 30 fps |
| **Precisión de ubicación y conteo** | Alta y medible (mAP, IoU) | Aproximada; empeora con objetos pequeños o numerosos |
| **Consistencia** | Determinista: la misma imagen da el mismo resultado | Puede variar entre llamadas |
| **Preguntas abiertas y razonamiento** | No | **Sí** |
| **Cambiar de tarea** | Reentrenar | Cambiar el prompt |
| **Sin conexión / en el dispositivo** | Sí | Normalmente no |
| **Úsalo cuando...** | Alto volumen, tiempo real, tarea fija y bien definida, medición precisa, operación sin nube | Bajo volumen, tareas variables, necesitas explicación o contexto, no tienes datos etiquetados, prototipos rápidos |

> 💡 **Patrón muy común en producción:** un modelo especializado **filtra** (rápido y barato, procesa el 100% del video) y solo las imágenes sospechosas se envían al multimodal para que **explique** (lento y caro, procesa el 1%). Ejemplo: un detector de personas sin casco corre en la cámara; cuando dispara, GPT-4.1 redacta el reporte del incidente.

#### Modelo preentrenado vs modelo personalizado

| | Preentrenado ("tal cual") | Personalizado (entrenado o ajustado con tus datos) |
|---|---|---|
| Ejemplos | Tags, objetos y personas de Azure Vision; captions; GPT-4.1 | Un detector de "tornillo M6 faltante" entrenado con tus fotos |
| Úsalo cuando... | Tus clases son **comunes** (persona, auto, perro, comida) | Tus clases son **específicas de tu negocio** (tus productos, tus defectos, tus piezas) |
| Ventaja | Cero esfuerzo de datos | Precisión en tu dominio |
| Riesgo | No conoce tu "tornillo M6" ni tu marca | Necesita datos representativos (iluminación, ángulos, cámaras reales) |

#### Nube vs borde (edge)

| Procesa en la **nube** cuando... | Procesa en el **borde** (cámara, celular, gateway) cuando... |
|---|---|
| El volumen es bajo o por lotes | Necesitas respuesta en tiempo real (< 100 ms) |
| Usas modelos grandes (multimodales) | La conexión es mala o costosa (minas, campo, barcos) |
| Quieres actualizar el modelo sin tocar dispositivos | Hay restricciones de privacidad (las imágenes no deben salir del sitio) |
| Necesitas combinar con otros servicios (búsqueda, agentes) | Hay miles de cámaras y enviar todo el video sería carísimo |

---

### Combinar tareas: pipelines reales

En la práctica casi nunca se usa una sola tarea:

| Pipeline | Ejemplo | Por qué combinar |
|---|---|---|
| **Detección → clasificación** del recorte | Detectar cada persona y luego clasificar si lleva casco | El clasificador trabaja mejor sobre un recorte limpio que sobre la escena completa |
| **Detección → segmentación** | Detectar la caja de cada fruta y luego segmentarla (como hace SAM con una caja como "pista") | Etiquetar cajas es barato; la segmentación fina se obtiene después |
| **Detección → OCR** | Encontrar la placa del auto y luego leer sus caracteres | El OCR es más preciso sobre la región correcta |
| **Clasificación → multimodal** | Clasificar fotos de siniestros como "daño grave" y solo esas mandarlas a redactar el reporte | Controla el costo del modelo grande |
| **Multimodal → detección** | Preguntar al modelo qué buscar ("¿qué objetos de riesgo hay?") y usar un detector para ubicarlos con precisión | Combina razonamiento con medición confiable |

---

### Errores comunes al elegir

| Error | Consecuencia | Mejor opción |
|---|---|---|
| Usar clasificación cuando hay varios objetos en la foto | El modelo "elige" uno y se olvida de los demás | Detección o clasificación multietiqueta |
| Usar detección para medir áreas | Áreas infladas (la caja incluye fondo) | Segmentación |
| Usar segmentación solo para contar | Pagas por etiquetar contornos que no usas | Detección |
| Usar un modelo multimodal para video en tiempo real | Latencia de segundos y costo enorme | Detector ligero + multimodal solo en eventos |
| Confiar en las coordenadas o conteos exactos de un LLM multimodal | Cajas imprecisas, conteos equivocados en escenas llenas | Detector especializado para ubicar; multimodal para describir |
| Entrenar con fotos "de estudio" y usar en cámaras reales | El modelo falla con otra luz, ángulo o resolución | Datos de entrenamiento tomados con las cámaras reales |
| Etiquetar 10,000 imágenes antes de probar | Semanas perdidas si la tarea estaba mal elegida | Prototipo zero-shot con multimodal primero, luego decide |

---

### ¿Qué servicio de Azure / Foundry uso para cada tarea?

| Tarea | Opción en el ecosistema de Microsoft | Nota |
|---|---|---|
| Clasificación y detección **preentrenadas** (tags, objetos, personas, captions, OCR) | **Azure Vision – Image Analysis 4.0** (Foundry Tools) | Microsoft anunció su retiro el **25 de septiembre de 2028**; recomienda migrar a las alternativas de su guía |
| Clasificación y detección **personalizadas** | **Azure Custom Vision** (soporte completo hasta el **25/09/2028**) → alternativas: **Azure Machine Learning AutoML** para imágenes, modelos del catálogo de Foundry o **Content Understanding** para clasificación personalizada | Custom Vision permite exportar modelos para usarlos sin conexión |
| Segmentación | **Azure ML AutoML** (segmentación de instancias) o modelos del catálogo (por ejemplo, de la familia SAM) | La API *Segment* / quitar fondo de Image Analysis 4.0 se **retiró el 31 de marzo de 2025** |
| Análisis contextual | **Modelos multimodales en Microsoft Foundry** (GPT-4.1, GPT-5.x, Phi-4-multimodal…) | Ver [Parte 2, Módulo 5](../../parte2/modulo5/tema2.md) |
| Extracción de campos de imágenes y documentos | **Azure Content Understanding** (analizador `prebuilt-image`, analizadores personalizados) | Visto en la Parte 2 |

> ⚠️ Los nombres y fechas de los servicios cambian con frecuencia. Para el examen AI-901 importa más **identificar la tarea** (qué tipo de salida necesitas) que memorizar el nombre del servicio.

---

### Práctica en Python

Los primeros cuatro ejemplos solo usan `numpy` y funcionan sin Azure.

```bash
pip install numpy
```

#### 1) Multiclase (softmax) vs multietiqueta (sigmoide)

```python
import numpy as np

logits = np.array([2.1, 1.3, -0.5, 0.9])        # salida cruda de la red para 4 clases
clases = ["perro", "pelota", "gato", "pasto"]

# MULTICLASE (una sola respuesta): softmax -> las probabilidades suman 1
softmax = np.exp(logits) / np.exp(logits).sum()
print("Softmax :", {c: round(float(p), 3) for c, p in zip(clases, softmax)}, "| suma =", round(float(softmax.sum()), 3))
print("  -> Respuesta única:", clases[softmax.argmax()])

# MULTIETIQUETA (varias respuestas): sigmoide por clase -> cada una es independiente
sigmoide = 1 / (1 + np.exp(-logits))
print("Sigmoide:", {c: round(float(p), 3) for c, p in zip(clases, sigmoide)}, "| suma =", round(float(sigmoide.sum()), 3))
umbral = 0.7
print(f"  -> Etiquetas con p >= {umbral}:", [c for c, p in zip(clases, sigmoide) if p >= umbral])
```

Salida:
```
Softmax : {'perro': 0.548, 'pelota': 0.246, 'gato': 0.041, 'pasto': 0.165} | suma = 1.0
  -> Respuesta única: perro
Sigmoide: {'perro': 0.891, 'pelota': 0.786, 'gato': 0.378, 'pasto': 0.711} | suma = 2.765
  -> Etiquetas con p >= 0.7: ['perro', 'pelota', 'pasto']
```
- **Explicación:**
  - Con los **mismos** números de salida de la red, softmax obliga a elegir: "perro" gana y la pelota y el pasto se pierden.
  - La sigmoide evalúa cada etiqueta por separado (la suma da 2.765, no 1) y devuelve las tres que sí están en la foto.
  - Elegir multiclase o multietiqueta se decide **antes** de entrenar, porque cambia la capa de salida y la forma de etiquetar los datos.

#### 2) ¿Caja o máscara? Por qué la detección no sirve para medir

```python
import numpy as np

H, W = 200, 300
yy, xx = np.mgrid[0:H, 0:W]

# Un "plátano" diagonal: banda curva y delgada (máscara de segmentación verdadera)
centro = 30 + 0.4 * xx + 0.001 * (xx - 150) ** 2
mascara = (np.abs(yy - centro) < 9) & (xx > 30) & (xx < 270)

# Lo que devolvería un DETECTOR: el rectángulo mínimo que contiene al objeto
ys, xs = np.where(mascara)
x1, y1, x2, y2 = xs.min(), ys.min(), xs.max(), ys.max()
area_caja = (x2 - x1 + 1) * (y2 - y1 + 1)
area_real = mascara.sum()

print(f"Bounding box: x={x1}..{x2}, y={y1}..{y2}")
print(f"Área de la caja (detección):  {area_caja:6d} px")
print(f"Área real (segmentación):     {area_real:6d} px")
print(f"La caja sobreestima el área {area_caja/area_real:.1f}x  "
      f"(solo {100*area_real/area_caja:.0f}% de la caja es plátano)")

# Ejemplo agrícola: % de hoja dañada. La caja no sirve; la máscara sí.
hoja = ((xx - 150) / 120) ** 2 + ((yy - 100) / 80) ** 2 <= 1           # hoja elíptica
plaga = hoja & (((xx - 110) / 30) ** 2 + ((yy - 80) / 20) ** 2 <= 1)    # mancha dentro de la hoja
print(f"\nHoja: {hoja.sum()} px | mancha: {plaga.sum()} px | daño = {100*plaga.sum()/hoja.sum():.1f}% de la hoja")
```

Salida:
```
Bounding box: x=31..269, y=48..160
Área de la caja (detección):   27007 px
Área real (segmentación):       4299 px
La caja sobreestima el área 6.3x  (solo 16% de la caja es plátano)

Hoja: 30137 px | mancha: 1881 px | daño = 6.2% de la hoja
```
- **Explicación:**
  - Un objeto delgado y diagonal ocupa solo el **16%** de su propia caja. Si un sistema de calidad midiera grietas con cajas, reportaría daños hasta 6 veces mayores.
  - Para responder "¿qué % de la hoja está dañado?" necesitas contar píxeles de dos máscaras; con cajas la pregunta ni siquiera tiene sentido.
  - Si tu objeto es casi rectangular (una caja de cartón vista de frente), la detección basta y es mucho más barata.

#### 3) ¿Cómo sé si acerté? IoU para detección y segmentación

```python
import numpy as np

def iou_cajas(a, b):
    """a, b = (x1, y1, x2, y2). Intersección sobre unión de dos rectángulos."""
    ix1, iy1 = max(a[0], b[0]), max(a[1], b[1])
    ix2, iy2 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
    union = (a[2]-a[0])*(a[3]-a[1]) + (b[2]-b[0])*(b[3]-b[1]) - inter
    return inter / union

def iou_mascaras(m1, m2):
    return np.logical_and(m1, m2).sum() / np.logical_or(m1, m2).sum()

def dice(m1, m2):
    return 2 * np.logical_and(m1, m2).sum() / (m1.sum() + m2.sum())

# --- Detección: ¿la caja predicha "cuenta" como acierto? ---
real = (50, 50, 150, 150)
for pred in [(55, 52, 152, 148), (80, 80, 180, 180), (120, 120, 220, 220)]:
    v = iou_cajas(real, pred)
    print(f"Caja predicha {pred}: IoU = {v:.2f} -> {'ACIERTO' if v >= 0.5 else 'FALLO'} (umbral 0.5)")

# --- Segmentación: comparar máscara predicha vs real ---
yy, xx = np.mgrid[0:100, 0:100]
m_real = (xx - 50) ** 2 + (yy - 50) ** 2 <= 30 ** 2
m_pred = (xx - 54) ** 2 + (yy - 50) ** 2 <= 28 ** 2
print(f"\nMáscaras: IoU = {iou_mascaras(m_real, m_pred):.3f} | Dice = {dice(m_real, m_pred):.3f}")
```

Salida:
```
Caja predicha (55, 52, 152, 148): IoU = 0.89 -> ACIERTO (umbral 0.5)
Caja predicha (80, 80, 180, 180): IoU = 0.32 -> FALLO (umbral 0.5)
Caja predicha (120, 120, 220, 220): IoU = 0.05 -> FALLO (umbral 0.5)

Máscaras: IoU = 0.821 | Dice = 0.901
```
- **Explicación:**
  - Cada tarea se evalúa distinto. En **clasificación** basta comparar etiquetas (accuracy, precisión, recall). En **detección**, una predicción solo cuenta si la clase es correcta **y** la caja se traslapa lo suficiente (IoU ≥ 0.5 es el criterio clásico de la métrica **mAP@0.5**).
  - La segunda caja encontró el objeto, pero corrida: con IoU 0.32 cuenta como fallo.
  - En **segmentación** se compara píxel a píxel; Dice siempre es ≥ IoU para las mismas máscaras (Dice = 2·IoU / (1 + IoU)).
  - Para el **análisis contextual** no hay una métrica numérica tan simple: se usan rúbricas, evaluadores humanos o evaluadores automáticos de Foundry.

#### 4) Asistente de decisión: ¿qué tarea necesito?

```python
def recomendar_tarea(necesito_ubicacion=False, necesito_forma_exacta=False,
                     separar_instancias=False, varias_etiquetas=False,
                     pregunta_abierta=False, tiempo_real_en_dispositivo=False,
                     tengo_datos_etiquetados=True):
    if pregunta_abierta:
        tarea = "Análisis contextual con modelo multimodal (GPT-4.1 / GPT-5.x en Foundry)"
        if tiempo_real_en_dispositivo:
            tarea += " ⚠️ costoso/lento en el borde: considera un modelo especializado para el filtro inicial"
        return tarea
    if necesito_forma_exacta:
        return "Segmentación de INSTANCIAS" if separar_instancias else "Segmentación SEMÁNTICA"
    if necesito_ubicacion:
        tarea = "Detección de objetos"
    else:
        tarea = "Clasificación " + ("MULTIETIQUETA (sigmoide)" if varias_etiquetas else "MULTICLASE (softmax)")
    if tiempo_real_en_dispositivo:
        tarea += " con modelo ligero exportado al dispositivo (ej. YOLO, MobileNet/SSD)"
    if not tengo_datos_etiquetados:
        tarea += " — sin datos: empieza con un modelo preentrenado o multimodal (zero-shot) y etiqueta después"
    return tarea

casos = {
    "¿La radiografía es normal o anormal?":                dict(),
    "¿Qué etiquetas aplican a esta foto de catálogo?":     dict(varias_etiquetas=True),
    "¿Cuántas cajas hay en la banda y dónde?":             dict(necesito_ubicacion=True),
    "¿Qué % del cultivo tiene plaga?":                     dict(necesito_forma_exacta=True),
    "Separar cada célula para contarlas y medirlas":       dict(necesito_forma_exacta=True, separar_instancias=True),
    "¿Hay algún riesgo de seguridad en esta obra?":        dict(pregunta_abierta=True),
    "Cámara de línea de producción, 30 fps, sin nube":     dict(necesito_ubicacion=True, tiempo_real_en_dispositivo=True),
    "Detectar cascos, pero aún no tengo fotos etiquetadas": dict(necesito_ubicacion=True, tengo_datos_etiquetados=False),
}
for pregunta, params in casos.items():
    print(f"{pregunta:<55} -> {recomendar_tarea(**params)}")
```

Salida:
```
¿La radiografía es normal o anormal?                    -> Clasificación MULTICLASE (softmax)
¿Qué etiquetas aplican a esta foto de catálogo?         -> Clasificación MULTIETIQUETA (sigmoide)
¿Cuántas cajas hay en la banda y dónde?                 -> Detección de objetos
¿Qué % del cultivo tiene plaga?                         -> Segmentación SEMÁNTICA
Separar cada célula para contarlas y medirlas           -> Segmentación de INSTANCIAS
¿Hay algún riesgo de seguridad en esta obra?            -> Análisis contextual con modelo multimodal (GPT-4.1 / GPT-5.x en Foundry)
Cámara de línea de producción, 30 fps, sin nube         -> Detección de objetos con modelo ligero exportado al dispositivo (ej. YOLO, MobileNet/SSD)
Detectar cascos, pero aún no tengo fotos etiquetadas    -> Detección de objetos — sin datos: empieza con un modelo preentrenado o multimodal (zero-shot) y etiqueta después
```
- **Explicación:** el orden de las preguntas refleja el orden de las comparativas: primero "¿es una pregunta abierta?" (multimodal), luego "¿necesito la forma exacta?" (segmentación), luego "¿necesito la ubicación?" (detección); si nada de eso aplica, basta con clasificar. Las condiciones de dispositivo y datos no cambian la **tarea**, cambian el **tipo de modelo** con que la resuelves.

#### 5) Las cuatro tareas "en modo multimodal" con Foundry (requiere un proyecto de Foundry)

El mismo modelo multimodal puede **imitar** las cuatro tareas cambiando solo la pregunta. Es ideal para prototipar y ver qué tarea necesitas antes de entrenar nada.

```python
# pip install azure-ai-projects azure-identity
import os, json
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

proyecto = AIProjectClient(endpoint=os.environ["PROJECT_ENDPOINT"], credential=DefaultAzureCredential())
cliente = proyecto.get_openai_client()

IMAGEN = ("https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/"
          "master/ComputerVision/Images/dog.jpg")

preguntas = {
    "clasificación": 'Responde solo JSON: {"clase": "perro|gato|otro", "confianza": 0-1}',
    "multietiqueta": 'Responde solo JSON: {"etiquetas": [lista de etiquetas que aplican a la imagen]}',
    "detección":     'Responde solo JSON: {"objetos": [{"etiqueta": str, "caja_aprox": [x1, y1, x2, y2] en % del ancho/alto}]}',
    "contextual":    "Describe la escena en una frase para una persona con discapacidad visual.",
}

for tarea, instruccion in preguntas.items():
    r = cliente.responses.create(
        model=os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4.1"),
        input=[{"role": "user", "content": [
            {"type": "input_text", "text": instruccion},
            {"type": "input_image", "image_url": IMAGEN},
        ]}],
    )
    print(f"--- {tarea} ---\n{r.output_text}\n")
```
- **Explicación:**
  - Una sola llamada con `input_text` + `input_image` (Responses API) cubre clasificación, multietiqueta, una "detección aproximada" y descripción contextual: es la flexibilidad *zero-shot* de la comparativa.
  - Observa que pedimos `caja_aprox` en porcentaje: las coordenadas de un LLM son **orientativas**, no una medición. Si el caso real necesita ubicaciones confiables (conteo en video, medición, robots), esa es la señal para pasar a un detector o segmentador especializado.
  - No hay segmentación aquí a propósito: un modelo de lenguaje no devuelve máscaras por píxel. Esa es otra frontera clara entre las tareas.
  - Si pruebas esto con 1,000 imágenes por hora, calcula el costo por tokens contra el de un modelo especializado; esa comparación suele decidir la arquitectura final.

---

### Para el examen
- "Identificar la **ubicación** de cada vehículo en una imagen de tráfico" → **detección de objetos**.
- "Determinar si una foto contiene un perro o un gato" → **clasificación**.
- "Delimitar el contorno exacto de cada célula" → **segmentación**.
- "Generar una descripción para personas con discapacidad visual" → **análisis contextual / modelo multimodal**.
- "Contar cuántas personas entran a la tienda" → **detección** (conteo = objetos individuales).
- "Calcular qué porcentaje de una imagen satelital es agua" → **segmentación semántica**.
- "Asignar varias etiquetas descriptivas a una foto (playa, atardecer, personas)" → **clasificación multietiqueta** / *tagging*.
- "Responder preguntas sobre lo que ocurre en la imagen" → **multimodal**.

**Palabras clave:** "qué es" → clasificación · "dónde / cuántos / bounding box" → detección · "píxel / contorno / máscara / área" → segmentación · "describir / explicar / preguntar / escena" → multimodal.

### Recursos
- [Introducción a los conceptos de computer vision – Microsoft Learn](https://learn.microsoft.com/es-es/training/modules/introduction-computer-vision/)
- [Azure Vision – Image Analysis (incluye avisos de retiro)](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview-image-analysis)
- [Azure Custom Vision – información general y guía de migración](https://learn.microsoft.com/en-us/azure/ai-services/custom-vision-service/overview)
- [AutoML para visión en Azure Machine Learning (clasificación, detección y segmentación de instancias)](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-auto-train-image-models)
- [Kirillov et al. (2019) – Panoptic Segmentation (define semántica vs instancias vs panóptica)](https://arxiv.org/abs/1801.00868)
