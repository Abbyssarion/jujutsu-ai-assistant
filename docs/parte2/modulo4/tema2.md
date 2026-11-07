# Tema 2: Explicación de los SDK de voz y Voice Live de Microsoft Foundry con Python

### Descripción
En Foundry tienes dos caminos para dar voz a tus aplicaciones:
1. **Speech SDK** (`azure-cognitiveservices-speech`): piezas separadas de **STT** (speech-to-text) y **TTS** (text-to-speech). Tú controlas cada paso y conectas la lógica en medio (un LLM, una base de datos, una traducción…).
2. **Voice Live API** (`azure-ai-voicelive`): un servicio **voz a voz (speech-to-speech)** totalmente administrado que integra reconocimiento, un modelo generativo y síntesis en **una sola conexión WebSocket** en tiempo real, con detección de turnos, cancelación de eco, supresión de ruido e interrupciones.

Analogía: el Speech SDK es armar tu propio equipo de sonido por componentes (micrófono, mezcladora, bocinas). Voice Live es una bocina inteligente que ya trae todo integrado: solo la conectas y le dices cómo comportarse.

**Por qué existe Voice Live.** Si armas un agente de voz "a mano" (STT → LLM → TTS) tienes tres problemas: **latencia** (cada etapa suma cientos de milisegundos y el usuario nota pausas de 2–3 s), **turnos** (¿cuándo terminó de hablar el usuario? ¿y si interrumpe?) y **orquestación** (tres servicios, tres clientes, tres formas de fallar). Voice Live resuelve los tres en el servidor: tú mandas audio y recibes audio (y, si quieres, texto, visemas o video de avatar).

> [!NOTE]
> Para el examen basta con: diferenciar **Speech SDK vs. Voice Live**, saber que Voice Live es **speech-to-speech administrado con manejo de interrupciones**, que se integra a un **agente de Foundry** (voice mode) y conocer las clases básicas del Speech SDK. Lo demás es para que construyas agentes de voz de verdad.

### Aspectos Clave

1. **Text to speech con el Speech SDK:**
   ```python
   import os
   from dotenv import load_dotenv
   import azure.cognitiveservices.speech as speechsdk

   load_dotenv()
   speech_config = speechsdk.SpeechConfig(subscription=os.getenv("FOUNDRY_KEY"), endpoint=os.getenv("ENDPOINT"))

   # Voz neuronal en español de México (prueba también "es-MX-JorgeNeural")
   speech_config.speech_synthesis_voice_name = "es-MX-DaliaNeural"

   # Salida: bocinas. Para guardar a archivo: AudioOutputConfig(filename="saludo.wav")
   audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
   synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

   resultado = synthesizer.speak_text_async("¡Hola! Bienvenido al acordeón de la AI-901.").get()

   if resultado.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
       print("Audio generado")
   elif resultado.reason == speechsdk.ResultReason.Canceled:
       detalles = resultado.cancellation_details
       print(f"Cancelado: {detalles.reason} {detalles.error_details}")
   ```
   - **Explicación:**
     - `speech_synthesis_voice_name` elige la voz. Microsoft Learn usa `en-US-Ava:DragonHDLatestNeural`, una voz **HD multilingüe** que cambia de idioma según el texto.
     - `AudioOutputConfig` define a dónde va el audio: bocina (`use_default_speaker=True`), archivo (`filename=`) o un *stream* en memoria (`stream=speechsdk.audio.PullAudioOutputStream()`) para mandarlo por red sin tocar disco.
     - `speak_text_async(...).get()` sintetiza y espera. `resultado.audio_data` trae los bytes si quieres manejarlos tú.
     - Formato de salida: `speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)` para MP3, Ogg/Opus, WAV a distintas frecuencias, etc.
     - **Eventos útiles:** `synthesizer.synthesis_word_boundary` (te dice en qué milisegundo empieza cada palabra: para subtítulos sincronizados) y `synthesizer.viseme_received` (id de forma de boca: para animar un avatar).

   **Tipos de voz que debes distinguir:**

   | Tipo | Qué es | Ejemplo | Cuándo |
   |---|---|---|---|
   | **Neuronal estándar** | Más de 600 voces en 150+ locales; una voz por idioma/región | `es-MX-DaliaNeural`, `es-MX-JorgeNeural` | La mayoría de los casos |
   | **Multilingüe** | Una voz que habla varios idiomas con el mismo timbre | `en-US-AvaMultilingualNeural` | Apps bilingües, nombres extranjeros |
   | **HD (Dragon HD)** | Voces que **entienden el contexto** y ajustan emoción y ritmo solas; aceptan `temperature` | `en-US-Ava:DragonHDLatestNeural` | Conversación natural, Voice Live |
   | **Custom neural voice** | Voz de marca entrenada con grabaciones propias (acceso limitado, formulario) | tu locutor | Identidad sonora corporativa |
   | **Personal voice** | Clonado rápido con pocos segundos de audio (acceso limitado) | — | Asistentes personalizados |

2. **Controlar la voz con SSML:**
   SSML (*Speech Synthesis Markup Language*) es XML para controlar velocidad, tono, pausas, énfasis, estilo y pronunciación.
   ```python
   ssml = """
   <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
          xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="es-MX">
     <voice name="es-MX-DaliaNeural">
       <mstts:express-as style="customerservice">
         Tu vuelo a Cancún sale a las <say-as interpret-as="time" format="hms12">7:45pm</say-as>.
       </mstts:express-as>
       <break time="500ms"/>
       <prosody rate="-15%" pitch="+5%">Te recomendamos llegar dos horas antes.</prosody>
       La aerolínea es <phoneme alphabet="ipa" ph="biˈba">Viva</phoneme>.
       <lang xml:lang="en-US">Have a nice trip!</lang>
     </voice>
   </speak>
   """
   resultado = synthesizer.speak_ssml_async(ssml).get()
   ```
   - **Explicación:**
     - `<break>` pausas; `<prosody>` velocidad, tono y volumen; `<say-as>` cómo leer horas, fechas, números, teléfonos (`telephone`) o deletrear (`characters`).
     - `<mstts:express-as style="...">` estilos emocionales (`cheerful`, `sad`, `whispering`, `customerservice`, `newscast`…); cada voz soporta un subconjunto, consúltalo en la galería.
     - `<phoneme>` fuerza la pronunciación (alfabeto IPA o SAPI) y `<lexicon uri="...">` carga un diccionario de pronunciaciones para toda tu app (marcas, siglas).
     - `<lang>` cambia de idioma dentro de la misma frase con una voz multilingüe.
     - `<audio src="...">` inserta un efecto de sonido; `<bookmark mark="x"/>` dispara un evento cuando la síntesis llega a ese punto.
     - Es la forma de evitar la "voz robótica" (prosodia plana). Las voces HD necesitan menos SSML porque infieren la emoción del texto.

3. **Voice Live: arquitectura**
   ```
   🎤 Audio del usuario ──WebSocket──► Voice Live ──► [STT] → [Modelo generativo / Agente] → [TTS] ──► 🔊
                                           ▲          (o modelo de audio nativo, sin STT/TTS)           │
                                           └──── VAD, fin de turno, eco, ruido, interrupciones ◄────────┘
   ```
   - **Servicio administrado:** no montas ni mantienes el backend. Tu servidor (no el navegador) abre **un WebSocket** y se intercambian **eventos JSON** compatibles con la Azure OpenAI Realtime API (`session.update`, `response.create`, `response.audio.delta`…), más eventos propios de Azure (visemas, avatar, timestamps).
   - **Dos formas de procesar el audio**, según el modelo que elijas:

     | Enfoque | Modelos | Cómo funciona | Pros / contras |
     |---|---|---|---|
     | **Audio nativo** | `gpt-realtime`, `gpt-realtime-mini`, `gpt-realtime-2.1`, `azure-realtime`, `phi4-mm-realtime` (preview) | El modelo **escucha y habla** directamente; no hay STT/TTS intermedios | Mínima latencia, capta entonación y emoción; menos control sobre la transcripción |
     | **Cascada administrada** | `gpt-4o`, `gpt-4.1`, `gpt-4.1-mini/nano`, `gpt-5.x`… | Azure Speech transcribe → el LLM razona en texto → Azure TTS sintetiza, todo dentro del servicio | Cualquier LLM de texto, cualquier voz de Azure (incluida custom), transcripciones exactas; un poco más de latencia |

   - **Niveles de precio** (los define el modelo, no tú): **Pro** (`gpt-realtime`, `gpt-4o`, `gpt-4.1`, `gpt-5`…), **Standard** (`gpt-realtime-mini`, `gpt-4o-mini`, `gpt-4.1-mini`, `gpt-5-mini`), **Lite** (`gpt-4.1-nano`, `gpt-5-nano`, `phi4-mm-realtime`). Se cobra por **tokens de audio** (≈10 tokens/s de entrada y ≈20 tokens/s de salida en modelos OpenAI) más cargos aparte por avatar, custom voice o custom speech.
   - **Pipeline de audio en el servidor:** supresión profunda de ruido (`azure_deep_noise_suppression`), cancelación de eco (`server_echo_cancellation`), **detección de actividad de voz (VAD)** y **detección de fin de turno**; con interrupciones (*barge-in*): si hablas mientras el agente habla, se calla, recorta su respuesta y te escucha.
   - **Modos de uso:** con un **modelo** (tú das `instructions`, voz y herramientas en la sesión) o con un **agente de Foundry** (**voice mode**: instrucciones, conocimiento y herramientas viven en el agente; tu cliente solo maneja audio). En el Playground configuras voz, instrucciones y pruebas con el micrófono.
   - **Extras:** transcripción del usuario (`input_audio_transcription`), **avatares** (video por WebRTC, estándar o fotográfico), **visemas** y **timestamps por palabra**, herramientas por **function calling** y por **MCP** ([Módulo 3, Tema 2](../modulo3/tema2.md)).

4. **La sesión: los parámetros que importan.** Todo se configura con un `session.update` (en el SDK, `RequestSession`). Lo esencial:

   | Parámetro | Valores | Para qué |
   |---|---|---|
   | `model` | ver tabla anterior | El cerebro de la conversación (no se manda si usas agente) |
   | `instructions` | texto | System prompt de la sesión (**no permitido con agente**: las tiene el agente) |
   | `modalities` | `["text","audio"]` | Qué devuelve: audio, texto o ambos |
   | `voice` | `AzureStandardVoice(name, temperature, rate, style, locale…)`, `AzureCustomVoice`, `OpenAIVoice(name="alloy"…)` | Quién habla |
   | `input_audio_format` / `output_audio_format` | `pcm16` (por defecto), `g711_ulaw`, `g711_alaw` | PCM16 para apps; G.711 para telefonía |
   | `input_audio_sampling_rate` | `16000` o `24000` | Frecuencia del micrófono |
   | `turn_detection` | `ServerVad`, `AzureSemanticVad`, `AzureSemanticVadMultilingual` | Cuándo empieza y termina el turno del usuario |
   | `input_audio_noise_reduction` | `{"type": "azure_deep_noise_suppression"}` | Ruido de fondo |
   | `input_audio_echo_cancellation` | `{"type": "server_echo_cancellation"}` | Que el agente no se escuche a sí mismo |
   | `input_audio_transcription` | `model`: `azure-speech`, `mai-transcribe`, `whisper-1`, `gpt-4o-transcribe`; `language`; `phrase_list` | Obtener la transcripción del usuario (y sesgar términos: "Foundry", "Monterrey") |
   | `tools` / `tool_choice` | lista de `FunctionTool` o herramientas MCP | Acciones (consultar pedido, agendar cita) |
   | `temperature`, `max_response_output_tokens` | | Control de la respuesta |
   | `avatar`, `animation`, `output_audio_timestamp_types` | | Video, visemas, timestamps |

   **Detección de turnos (lo que hace o rompe la experiencia):**

   | Tipo | Cómo decide que terminaste de hablar | Cuándo |
   |---|---|---|
   | `server_vad` (por defecto) | Por **volumen y silencio**: `silence_duration_ms` (500 por defecto) de silencio → fin de turno | Ambientes controlados; respuesta rápida |
   | `azure_semantic_vad` | Además del silencio, **entiende si la frase está completa** ("quiero viajar a…" no cierra el turno) y puede quitar muletillas (`remove_filler_words`) | Conversación natural con pausas para pensar |
   | `azure_semantic_vad_multilingual` | Igual, para varios idiomas (`languages=["es","en"]`) | Usuarios bilingües |
   | `semantic_vad` | Versión de OpenAI, solo `gpt-realtime*`; `eagerness` low/medium/high | Si usas audio nativo de OpenAI |

   Parámetros comunes: `threshold` (0–1, sensibilidad), `prefix_padding_ms` (audio que se conserva antes de detectar voz), `silence_duration_ms`, `create_response` (responder automáticamente al terminar el turno) e `interrupt_response` (permitir *barge-in*).

5. **Ciclo de vida de una conversación (eventos).** Voice Live es **orientado a eventos**: tú mandas eventos de cliente y procesas eventos de servidor.
   ```
   CLIENTE                                   SERVIDOR
   session.update ───────────────────────►   session.created / session.updated
   input_audio_buffer.append (chunks) ───►   input_audio_buffer.speech_started     ← el usuario habla (si el agente hablaba: ¡interrupción!)
                                             input_audio_buffer.speech_stopped     ← VAD detectó fin de turno
                                             conversation.item.input_audio_transcription.completed  ← texto del usuario
                                             response.created
                                             response.audio_transcript.delta       ← texto de lo que dirá
                                             response.audio.delta (×N) ──────────► reproducir en bocina
                                             response.function_call_arguments.done ← quiere llamar a una función
   conversation.item.create(function_call_output) + response.create ──►  …sigue la respuesta
                                             response.done                         ← fin del turno del agente (tokens usados)
   ```
   - Con `ServerVad` y `create_response=True` no tienes que mandar `response.create`: el servidor responde solo al detectar el fin del turno.
   - Para que **el agente hable primero** (saludo proactivo), al recibir `session.updated` creas un `MessageItem` de rol `system` ("Saluda al usuario en español") y llamas `response.create()`.
   - En `response.done` viene `usage` con tokens de texto y audio: es tu medidor de costo.

6. **¿Speech SDK o Voice Live?**

   | Necesidad | Usa |
   |---|---|
   | Transcribir audio o generar archivos de voz | Speech SDK |
   | Control total de cada etapa (ej. traducir en medio, guardar transcripción, censurar) | Speech SDK + tu lógica |
   | Subtítulos, dictado, IVR clásico con menús | Speech SDK |
   | Conversación natural en tiempo real, con interrupciones | **Voice Live** |
   | Que un agente de Foundry existente "hable" | **Voice mode** del agente (Voice Live) |
   | Agente de voz con avatar en video | **Voice Live** (avatar) |
   | Responder a prompts hablados con un modelo multimodal (habilidad del examen) | Modelo con entrada de audio o Voice Live |

   > [!TIP]
   > Pregunta típica: *"Necesitas un asistente telefónico que el usuario pueda interrumpir y que responda con voz natural y baja latencia, sin orquestar STT y TTS por separado"* → **Voice Live API**. *"Necesitas generar 10,000 archivos MP3 con las noticias del día"* → **Text to speech del Speech SDK** (o la **batch synthesis API** para volúmenes grandes). *"Transcribir en vivo una conferencia"* → **SpeechRecognizer** con reconocimiento continuo.

### Práctica 1: Voice Live con Python (SDK asíncrono)
```python
# pip install "azure-ai-voicelive[aiohttp]" azure-identity python-dotenv pyaudio
import asyncio, os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.voicelive.aio import connect
from azure.ai.voicelive.models import (
    RequestSession, Modality, InputAudioFormat, OutputAudioFormat,
    AzureSemanticVadMultilingual, AzureStandardVoice, ServerEventType,
    AudioNoiseReduction, AudioEchoCancellation, AudioInputTranscriptionOptions,
)

load_dotenv()

async def main():
    async with connect(
        endpoint=os.environ["AZURE_VOICELIVE_ENDPOINT"],          # https://<recurso>.cognitiveservices.azure.com/
        credential=AzureKeyCredential(os.environ["AZURE_VOICELIVE_API_KEY"]),
        model="gpt-realtime",                     # modelo que razona en la conversación
    ) as conexion:
        # 1) Configurar la sesión: instrucciones, voz, formatos, audio y detección de turnos
        await conexion.session.update(session=RequestSession(
            modalities=[Modality.TEXT, Modality.AUDIO],
            instructions="Eres un asistente de viajes amable. Responde en español de México, breve.",
            voice=AzureStandardVoice(name="es-MX-DaliaNeural", type="azure-standard"),
            input_audio_format=InputAudioFormat.PCM16,
            output_audio_format=OutputAudioFormat.PCM16,
            input_audio_sampling_rate=24000,
            turn_detection=AzureSemanticVadMultilingual(
                threshold=0.5, prefix_padding_ms=400, silence_duration_ms=500,
                languages=["es", "en"], remove_filler_words=True,
            ),
            input_audio_noise_reduction=AudioNoiseReduction(type="azure_deep_noise_suppression"),
            input_audio_echo_cancellation=AudioEchoCancellation(type="server_echo_cancellation"),
            input_audio_transcription=AudioInputTranscriptionOptions(
                model="azure-speech", language="es", phrase_list=["Cancún", "Tulum", "Foundry"]),
        ))

        # 2) Procesar los eventos que manda el servidor
        async for evento in conexion:
            if evento.type == ServerEventType.SESSION_UPDATED:
                print("Sesión lista: empieza a enviar audio del micrófono")
                # aquí arrancas la tarea que lee PyAudio y hace:
                #   await conexion.input_audio_buffer.append(audio=base64_chunk)
            elif evento.type == ServerEventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED:
                print("El usuario empezó a hablar → vaciar la cola de reproducción (interrupción)")
            elif evento.type == ServerEventType.CONVERSATION_ITEM_INPUT_AUDIO_TRANSCRIPTION_COMPLETED:
                print("Usuario dijo:", evento.transcript)
            elif evento.type == ServerEventType.RESPONSE_AUDIO_TRANSCRIPT_DELTA:
                print(evento.delta, end="", flush=True)   # lo que el agente va a decir, en texto
            elif evento.type == ServerEventType.RESPONSE_AUDIO_DELTA:
                audio_pcm = evento.delta              # bytes PCM16 24 kHz → encolar para la bocina
            elif evento.type == ServerEventType.RESPONSE_DONE:
                print("\nTokens usados:", evento.response.usage)
            elif evento.type == ServerEventType.ERROR:
                print("Error:", evento.error.message)

asyncio.run(main())
```
- **Explicación:**
  - El SDK es **solo asíncrono** (`async/await`) y mantiene una **conexión WebSocket** abierta; `connect(...)` acepta `model=` (modo modelo) **o** `agent_name=` + `project_name=` (modo agente). La versión de API por defecto en el SDK 1.3 es `2026-07-15`.
  - `session.update` configura instrucciones, **voz** (una voz neuronal de Azure, una custom, o una de OpenAI con `OpenAIVoice(name="alloy")`), formatos **PCM16** y la **detección de turnos** (aquí semántica y multilingüe: deja pausas para pensar sin cortar el turno).
  - El audio del micrófono se manda con `conexion.input_audio_buffer.append(audio=<base64>)` en trozos pequeños (20–50 ms); el VAD del servidor decide los turnos, así que no tienes que llamar `commit`.
  - Todo es **orientado a eventos**: `RESPONSE_AUDIO_DELTA` trae trozos de audio para reproducir; `INPUT_AUDIO_BUFFER_SPEECH_STARTED` indica que el usuario interrumpió: **vacía tu cola de reproducción** en ese momento o el agente seguirá "hablando" desde tu búfer local aunque el servidor ya se calló.
  - Este esqueleto no incluye la captura ni la reproducción. El portal de Foundry genera un **ejemplo completo** (con PyAudio y dos hilos: uno que captura y otro que reproduce) que maneja sesión, dispositivos, streams e interrupciones: cópialo desde el Playground de Voice Live.

### Práctica 2: herramientas (function calling) en la conversación de voz
Un agente de voz sin herramientas solo platica. Con `tools`, el modelo puede **consultar tu sistema** en medio de la conversación.
```python
import json
from azure.ai.voicelive.models import FunctionTool, FunctionCallOutputItem

consultar_vuelo = FunctionTool(
    name="consultar_vuelo",
    description="Devuelve el estado de un vuelo dado su número, por ejemplo VB1234.",
    parameters={"type": "object",
                "properties": {"numero": {"type": "string"}},
                "required": ["numero"]},
)

# ...en RequestSession agrega: tools=[consultar_vuelo], tool_choice="auto"

def buscar_en_mi_sistema(numero: str) -> dict:          # tu lógica real (API, base de datos)
    return {"numero": numero, "estado": "a tiempo", "sala": "B7", "hora": "19:45"}

# ...dentro del bucle de eventos:
            elif evento.type == ServerEventType.RESPONSE_FUNCTION_CALL_ARGUMENTS_DONE:
                args = json.loads(evento.arguments)                       # {"numero": "VB1234"}
                resultado = buscar_en_mi_sistema(**args)
                await conexion.conversation.item.create(item=FunctionCallOutputItem(
                    call_id=evento.call_id,
                    output=json.dumps(resultado),
                ))
                await conexion.response.create()      # el agente continúa hablando con el dato
```
- **Explicación:**
  - Es el mismo patrón de *function calling* de los modelos de texto, pero en vivo: el modelo decide llamar, el servidor manda `response.function_call_arguments.done` con `name`, `call_id` y `arguments` (JSON en texto), tú ejecutas y devuelves un `function_call_output` con el **mismo `call_id`**, y pides una nueva respuesta.
  - Mientras tu función tarda, el usuario escucha silencio. Para operaciones lentas, Voice Live puede generar una **respuesta provisional** (`interim_response`, "déjame revisarlo…") y tú mantienes la función rápida (cachés, timeouts).
  - En la sesión también puedes registrar **servidores MCP** como herramientas (`Tool` con `type="mcp"`): lo que aprendiste en el [Módulo 3, Tema 2](../modulo3/tema2.md) aplica igual en voz.
  - Si usas **modo agente**, las herramientas se definen en el agente de Foundry (incluido Foundry IQ para RAG por voz: patrón *VoiceRAG*) y tu cliente no tiene que manejar este evento.

### Práctica 3: voice mode — conectar Voice Live a un agente de Foundry
```python
# pip install "azure-ai-voicelive[aiohttp]" azure-identity python-dotenv pyaudio
import asyncio, os
from dotenv import load_dotenv
from azure.identity.aio import DefaultAzureCredential
from azure.ai.voicelive.aio import connect
from azure.ai.voicelive.models import (RequestSession, Modality, AzureStandardVoice,
                                       ServerVad, MessageItem, InputTextContentPart, ServerEventType)
load_dotenv()

async def main():
    async with connect(
        endpoint=os.environ["AZURE_VOICELIVE_ENDPOINT"],
        credential=DefaultAzureCredential(),                  # modo agente: SOLO Entra ID, no acepta llave
        agent_name=os.environ["AGENT_NAME"],                  # el agente creado en Build → Agents
        project_name=os.environ["PROJECT_NAME"],              # último segmento del endpoint del proyecto
        # agent_version="3",            # opcional: fijar versión; si no, usa la más reciente
        # conversation_id="conv_123",   # opcional: continuar una conversación previa
    ) as conexion:
        # Sin instructions: las trae el agente. Solo configuras lo "físico" de la voz
        await conexion.session.update(session=RequestSession(
            modalities=[Modality.TEXT, Modality.AUDIO],
            voice=AzureStandardVoice(name="es-MX-DaliaNeural", type="azure-standard"),
            turn_detection=ServerVad(threshold=0.5, prefix_padding_ms=400, silence_duration_ms=500),
        ))
        async for evento in conexion:
            if evento.type == ServerEventType.SESSION_UPDATED:
                # Saludo proactivo: el agente habla primero
                await conexion.conversation.item.create(item=MessageItem(
                    role="system",
                    content=[InputTextContentPart(text="Saluda al usuario en español y pregunta en qué le ayudas.")]))
                await conexion.response.create()
            elif evento.type == ServerEventType.RESPONSE_AUDIO_DELTA:
                audio_pcm = evento.delta
            # ...captura, reproducción e interrupciones igual que en la Práctica 1

asyncio.run(main())
```
- **Explicación:**
  - En vez de `model=` pasas `agent_name` y `project_name`: Voice Live invoca al **agente de Foundry** con sus instrucciones, conocimiento (Foundry IQ), guardrails y herramientas. Cambias el comportamiento en el portal sin tocar el cliente.
  - Requiere **Microsoft Entra ID** (`DefaultAzureCredential`, `AzureCliCredential`) y el rol **Foundry User** (antes *Azure AI User*) sobre el recurso. La llave de API **no** sirve para invocar agentes.
  - Si la voz, el VAD y la supresión de ruido ya están guardados en el agente (voice mode del Playground), puedes omitirlos en `session.update`; lo que mandes desde el cliente sobreescribe lo del agente.
  - Para una app real, el patrón recomendado es **servidor a servidor**: tu backend abre el WebSocket con Voice Live y tu app web/móvil le manda el audio; nunca expongas la credencial en el navegador.

### Práctica 4: avatar y visemas (cuando la voz necesita cara)
```python
from azure.ai.voicelive.models import (
    AvatarConfig,
    AnimationOptions,
    RequestSession,
    Modality,
    AzureStandardVoice,
)

sesion = RequestSession(
    modalities=[Modality.TEXT, Modality.AUDIO],
    voice=AzureStandardVoice(name="es-MX-DaliaNeural", type="azure-standard"),
    animation=AnimationOptions(outputs=["viseme_id"]),                       # ids de forma de boca por tiempo
    avatar=AvatarConfig(character="lisa", style="casual-sitting", customized=False),
)
# El servidor devuelve ice_servers en session.updated; después negocias WebRTC con
# session.avatar.connect (client_sdp) → session.avatar.connecting (server_sdp) y recibes video sincronizado.
```
- **Explicación:**
  - `animation.outputs=["viseme_id"]` genera eventos `response.animation_viseme.delta` con `audio_offset_ms` y `viseme_id`: con eso animas tu propio personaje 2D/3D.
  - `avatar` enciende el **avatar en video** (estándar como `lisa`, o **fotográfico** con `avatar_type="photo-avatar"` y modelo `vasa-1`); el video viaja por **WebRTC**, el audio y los eventos por el WebSocket. Se factura aparte y el avatar personalizado tiene acceso limitado.
  - `output_audio_timestamp_types=["word"]` da `response.audio_timestamp.delta` con el milisegundo de cada palabra: subtítulos sincronizados o resaltar texto mientras habla.

### Buenas prácticas y errores comunes
- **Latencia:** usa modelos de audio nativo (`gpt-realtime-mini`) o cascada con modelos *mini*; manda audio en trozos de 20–50 ms; despliega el recurso en la región más cercana a tus usuarios; en telefonía usa `g711_ulaw` para no transcodificar.
- **Eco:** si tu cliente reproduce por bocina y captura por micrófono, activa `server_echo_cancellation`; en apps donde controlas la reproducción puedes mandar el audio de referencia (`reference_source="client"`, 2 canales) para una cancelación más precisa.
- **Interrupciones:** al recibir `speech_started` **vacía tu búfer local**; si no, el usuario escucha al agente "terminar" una frase que el servidor ya canceló.
- **Transcripción:** actívala siempre en producción (`input_audio_transcription`): la necesitas para logs, analítica, auditoría y para alimentar guardrails de texto.
- **Vocabulario del dominio:** `phrase_list` (términos, nombres de productos, ciudades) y, si no alcanza, **custom speech**.
- **Seguridad y cumplimiento:** modo agente con Entra ID; sin llaves en clientes; informa al usuario que habla con una IA; aplica guardrails de contenido en el agente ([Módulo 7, Tema 5](../modulo7/tema5.md)); recuerda que la voz es **dato biométrico** en varias legislaciones (custom voice requiere consentimiento del locutor).
- **Costos:** mide `usage` en `response.done`; un minuto de conversación ≈ 600 tokens de entrada + 1,200 de salida de audio con modelos OpenAI, más el texto del contexto que se re-procesa (parte va a caché).
- **Compatibilidad:** `instructions` no se acepta con agente; los eventos de Voice Live son casi iguales a los de la Azure OpenAI Realtime API, pero no idénticos (los de avatar, visemas, timestamps y `azure_semantic_vad` son exclusivos de Azure).

> [!WARNING]
> `ServerVad` con `silence_duration_ms` muy bajo (200 ms) corta a la gente que piensa mientras habla; muy alto (1,500 ms) hace sentir al agente lento. 500 ms es el punto de partida; si el caso es conversacional, prueba `azure_semantic_vad` antes de seguir ajustando números.

> [!TIP]
> Para el examen memoriza esto: **Speech SDK** = `SpeechConfig` + `AudioConfig`/`AudioOutputConfig` + `SpeechRecognizer`/`SpeechSynthesizer`; **SSML** controla la prosodia; **Voice Live** = speech-to-speech **administrado**, **tiempo real**, **WebSocket**, con **interrupciones, VAD, eco y ruido** resueltos en el servidor, y se integra a un **agente de Foundry** (voice mode) o a un modelo generativo; se programa con `azure-ai-voicelive` (asíncrono).

### Recursos
- [Galería de voces de Azure Speech](https://speech.microsoft.com/portal/voicegallery)
- [Referencia de SSML](https://learn.microsoft.com/es-es/azure/ai-services/speech-service/speech-synthesis-markup)
- [Voice Live API: descripción, modelos y precios](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/voice-live)
- [Cómo usar Voice Live: parámetros de sesión (VAD, ruido, eco, voz, avatar, transcripción)](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/voice-live-how-to)
- [Quickstart: Voice Live con agentes de Foundry (Python)](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/voice-live-agents-quickstart)
- [Referencia de eventos de la Azure OpenAI Realtime API](https://learn.microsoft.com/en-us/azure/ai-services/openai/realtime-audio-reference)
- [Paquete azure-ai-voicelive en PyPI](https://pypi.org/project/azure-ai-voicelive/) y [ejemplos del SDK en GitHub](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-voicelive/samples)
