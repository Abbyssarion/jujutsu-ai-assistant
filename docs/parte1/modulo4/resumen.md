# Resumen rápido: Introducción a los conceptos de voz de IA

Este módulo explica los escenarios de voz y **cómo funcionan por dentro** el reconocimiento y la síntesis de voz.

- **Soluciones con voz:**
  - **Beneficios:** accesibilidad, productividad (manos libres), mejor experiencia y alcance global (idiomas y dialectos).
  - **Reconocimiento:** atención a clientes (transcripción, enrutamiento), asistentes de voz, transcripción de reuniones, documentación médica.
  - **Síntesis:** chatbots con voz, lectura en voz alta (accesibilidad, dislexia), notificaciones y GPS, e-learning, entretenimiento.
  - **Combinados:** servicio al cliente por voz, IVR, aprendizaje de idiomas, vehículos controlados por voz.
  - **Consideraciones:** calidad de audio, soporte de idioma/dialecto, privacidad, latencia y estándares de accesibilidad (WCAG).

- **Reconocimiento de voz (6 etapas):**
  1. **Captura:** muestreo de la señal analógica (16 kHz para voz).
  2. **Preprocesamiento:** extracción de **MFCC** (ventanas de 20–30 ms → transformada de Fourier → escala Mel → ~13 coeficientes).
  3. **Modelo acústico:** Transformer que predice probabilidades de **fonemas** por ventana (ej. 80% /æ/, 15% /ɛ/).
  4. **Modelo de lenguaje:** resuelve ambigüedades con vocabulario, gramática y contexto.
  5. **Decodificación:** **beam search** sobre miles de hipótesis.
  6. **Posprocesamiento:** mayúsculas, puntuación, formato de números, filtro de groserías, normalización inversa ("tres p m" → "3 PM"), puntajes de confianza.

- **Síntesis de voz (4 etapas):**
  1. **Normalización de texto:** "Dr." → "Doctor", "$25.50" → "veinticinco dólares con cincuenta centavos".
  2. **Análisis lingüístico:** fonemas, lexicones y conversión **grafema a fonema (G2P)**.
  3. **Prosodia:** tono, duración, intensidad, pausas y acentos (Transformers predicen pitch, duración y energía).
  4. **Síntesis:** un modelo acústico genera **espectrogramas Mel** y un **vocoder neuronal** (WaveNet, WaveGlow, HiFi-GAN) los convierte en onda.

> [!TIP]
> La voz robótica casi siempre se debe a una **prosodia plana**, no a una mala pronunciación de fonemas.
