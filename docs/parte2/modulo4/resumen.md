# Resumen rápido: Introducción a la voz en Azure

Este módulo enseña a **reconocer** y **sintetizar** voz con **Azure Speech en Foundry Tools** y a crear agentes de voz con **Voice Live**.

- **Reconocimiento de voz (speech-to-text):**
  - Usa un modelo **acústico** (audio → fonemas) y un modelo de **lenguaje** (fonemas → palabras).
  - Usos: subtítulos, transcripción de llamadas, dictado de notas.
  - Se prueba en el portal: **Build → Models → AI services → Azure Speech - Speech to Text**.
  - SDK: `pip install azure-cognitiveservices-speech`. Clases: `SpeechConfig`, `AudioConfig`, `SpeechRecognizer`. Autenticación con llave o Microsoft Entra ID.
  - Eventos: `recognizing` (parcial) y `recognized` (final). Métodos: `start_continuous_recognition()` / `stop_continuous_recognition()`.
  - **Modos:** **tiempo real** (streaming mientras hablas) y **batch** (archivos en almacenamiento con URI SAS; resultados asíncronos, *best effort*).

- **Síntesis de voz (text-to-speech):**
  - Necesita el **texto** y la **voz**. Se puede ajustar velocidad, tono y volumen.
  - **Voces neuronales** (más naturales) y voces personalizadas.
  - Clases: `SpeechConfig` (con `speech_synthesis_voice_name`, ej. `en-US-Ava:DragonHDLatestNeural`), `AudioOutputConfig`, `SpeechSynthesizer`, `speak_text_async(text).get()`, `ResultReason.SynthesizingAudioCompleted`.
  - Usos: apps que hablan al instante o servicios que generan archivos de audio.

- **Agentes de voz con Voice Live:**
  - Servicio **totalmente administrado** que combina **STT + razonamiento con un modelo generativo + TTS** en una sola API en tiempo real; maneja **interrupciones**, puede iniciar la conversación (proactivo) y hasta usar avatares.
  - **Voice mode** del Playground integra Voice Live en la definición de un agente de Foundry.
  - SDK: `pip install azure-ai-voicelive` (más `pyaudio`, `python-dotenv`, `azure-identity`).

> [!TIP]
> "Transcribir miles de grabaciones guardadas en Blob Storage" → **batch transcription**. "Subtítulos en vivo de una conferencia" → **real-time**. "Un agente con el que platicas por voz y puedes interrumpir" → **Voice Live**.
