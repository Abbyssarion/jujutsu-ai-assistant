# Resumen rápido: Introducción a los conceptos de procesamiento de lenguaje natural

El NLP permite que las aplicaciones analicen texto para inferir significado semántico. Este módulo recorre la evolución de las técnicas: desde contar palabras hasta los modelos semánticos.

- **Tokenización:**
  Primer paso para analizar un *corpus* (conjunto de textos). Ejemplo: "We choose to go to the moon" → 7 tokens; "to" aparece dos veces. Técnicas de preprocesamiento:
  - **Normalización:** quitar puntuación y pasar a minúsculas (se puede perder significado: "Mr Banks" vs "banks").
  - **Eliminación de stopwords:** quitar "el", "la", "un", que aportan poco significado.
  - **Extracción de n-gramas:** unigramas, bigramas ("inteligencia artificial"), trigramas.
  - **Stemming:** recortar terminaciones ("powering", "powered", "powerful" → "power"). Puede producir no-palabras.
  - **Lematización:** llevar a la forma de diccionario usando reglas lingüísticas ("running" → "run"). Siempre produce palabras válidas.
  - **Etiquetado POS:** marcar cada token como sustantivo, verbo, adjetivo, etc.

- **Análisis estadístico de texto:**
  - **Análisis de frecuencia:** las palabras más repetidas indican el tema.
  - **TF-IDF:** `tfidf(t, d) = tf(t, d) × log(N / df(t))`. Alto = palabra frecuente en un documento pero rara en el resto.
  - **Bolsa de palabras + Naive Bayes:** clasificación (spam, sentimiento) por frecuencia de palabras, ignorando el orden.
  - **TextRank:** algoritmo de grafos (como PageRank) para **resumen extractivo** y extracción de palabras clave.

- **Modelos de lenguaje semántico:**
  - Representan tokens como **vectores densos** (Word2Vec, GloVe) cuyos valores reflejan el uso de la palabra.
  - Palabras similares apuntan en la misma dirección → **similitud coseno** ("dog"–"cat" ≈ 0.992; "dog"–"tree" ≈ 0.333).
  - **Aritmética de vectores:** `dog + young ≈ puppy`; `kitten − puppy + dog ≈ cat`.
  - Los **embeddings contextualizados** (con atención, como los de GPT) son la base de la IA generativa moderna.
  - Aplicaciones: resumen, extracción de palabras clave, reconocimiento de entidades (NER) y clasificación de textos.

> [!TIP]
> Si en el examen ves "resumen que selecciona oraciones del texto original" → **extractivo** (TextRank). Si ves "genera texto nuevo que resume" → **abstractivo** (modelos semánticos/LLMs).
