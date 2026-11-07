# Tema 1: Tutorial de reconocimiento de voz con Azure Speech

**Objetivo:** Transcribir voz a texto desde el micrófono y desde un archivo de audio usando el SDK de Azure Speech en Python.

Lectura oficial: [Reconocimiento de voz – Microsoft Learn](https://learn.microsoft.com/es-es/training/modules/get-started-speech-azure/2-speech-recognition?pivots=text)

## Paso a Paso:

### 1. Probar sin código
- En el portal de Foundry ve a **Build → Models → AI services** y selecciona **Azure Speech - Speech to Text**.
- Sube un archivo de audio o graba tu voz y observa la transcripción. Así validas el idioma y la calidad antes de programar.

### 2. Preparar el entorno
```bash
pip install azure-cognitiveservices-speech python-dotenv
```
`.env` (usa el endpoint y la llave de tu **recurso de Foundry**):
```bash
ENDPOINT=https://<recurso>.cognitiveservices.azure.com/
FOUNDRY_KEY=<tu-llave>
```

### 3. Reconocimiento de una frase desde el micrófono (`stt_microfono.py`)
```python
import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

# 1) Configuración: endpoint + llave + idioma
speech_config = speechsdk.SpeechConfig(subscription=os.getenv("FOUNDRY_KEY"),
                                       endpoint=os.getenv("ENDPOINT"))
speech_config.speech_recognition_language = "es-MX"

# 2) Entrada de audio: micrófono predeterminado
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

# 3) Reconocedor
recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

print("Habla ahora...")
resultado = recognizer.recognize_once_async().get()   # escucha hasta detectar silencio

if resultado.reason == speechsdk.ResultReason.RecognizedSpeech:
    print(f"Reconocido: {resultado.text}")
elif resultado.reason == speechsdk.ResultReason.NoMatch:
    print("No se reconoció voz.")
elif resultado.reason == speechsdk.ResultReason.Canceled:
    detalles = resultado.cancellation_details
    print(f"Cancelado: {detalles.reason} - {detalles.error_details}")
```
- **Explicación:**
  - `SpeechConfig` guarda la autenticación y opciones (idioma `es-MX`).
  - `AudioConfig` define **de dónde viene el audio**: micrófono, archivo o *stream*.
  - `recognize_once_async()` reconoce **una sola frase** (hasta una pausa o ~15 segundos). Ideal para comandos.
  - Siempre revisa `result.reason`: éxito, sin coincidencia o cancelado (llave/endpoint incorrectos, red).

### 4. Reconocimiento continuo (para dictado o reuniones) (`stt_continuo.py`)
```python
import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()
speech_config = speechsdk.SpeechConfig(subscription=os.getenv("FOUNDRY_KEY"), endpoint=os.getenv("ENDPOINT"))
speech_config.speech_recognition_language = "es-MX"
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

# Manejadores de eventos
def reconociendo(evt):          # resultados PARCIALES mientras hablas
    print(f"  ...{evt.result.text}", end="\r")

def reconocido(evt):            # resultado FINAL de cada frase
    print(f"✅ {evt.result.text}")

recognizer.recognizing.connect(reconociendo)
recognizer.recognized.connect(reconocido)

recognizer.start_continuous_recognition()
input("Habla... presiona Enter para detener\n")
recognizer.stop_continuous_recognition()
```
- **Explicación:**
  - El reconocimiento continuo funciona por **eventos**: `recognizing` llega muchas veces con texto parcial; `recognized` llega una vez por frase con el texto final ya con puntuación.
  - Es el modo **en tiempo real** para subtítulos, presentaciones o dictado.

### 5. Transcribir un archivo de audio (caso buzón de voz) (`stt_archivo.py`)
```python
import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()
speech_config = speechsdk.SpeechConfig(subscription=os.getenv("FOUNDRY_KEY"), endpoint=os.getenv("ENDPOINT"))
speech_config.speech_recognition_language = "es-MX"
speech_config.request_word_level_timestamps()               # marcas de tiempo por palabra

audio_config = speechsdk.audio.AudioConfig(filename="buzon.wav")   # WAV PCM 16 kHz, mono, 16 bits
recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

resultado = recognizer.recognize_once_async().get()
print("Texto:", resultado.text)
print("JSON detallado:", resultado.json)      # incluye confianza y offsets
```
- **Explicación:**
  - Solo cambia `AudioConfig(filename=...)`.
  - `request_word_level_timestamps()` agrega en el JSON el momento exacto de cada palabra (útil para subtítulos o para resaltar palabras de baja confianza).
  - Para audios largos usa el reconocimiento continuo con el archivo, o la **transcripción por lotes**.

### 6. Transcripción por lotes (batch)
- Para **muchos archivos** guardados en un *file share*, servidor o **Azure Storage**.
- Apuntas a los archivos con una **URI SAS** y recibes los resultados de forma **asíncrona**.
- Es *best effort*: normalmente inicia en minutos, sin garantía de cuándo pasa a ejecución.
- Se usa con la **API REST de transcripción por lotes** (no con `SpeechRecognizer`).

| Modo | Cuándo | Cómo |
|---|---|---|
| Tiempo real (una frase) | Comandos de voz | `recognize_once_async()` |
| Tiempo real (continuo) | Subtítulos, dictado | `start_continuous_recognition()` + eventos |
| Archivo individual | Un buzón de voz | `AudioConfig(filename=...)` |
| Batch | Miles de grabaciones de call center | API REST de batch + URI SAS |

## Práctica oficial de Microsoft Learn
- [Ejercicio: Introducción a la voz en Microsoft Foundry](https://learn.microsoft.com/es-es/training/modules/get-started-speech-azure/5-exercise)
- [Ejercicio: Explorar la voz de IA](https://learn.microsoft.com/es-es/training/modules/introduction-ai-speech/5-exercise-speech)
