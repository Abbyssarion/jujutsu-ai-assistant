import asyncio
import gc
import html
import logging
import os
import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from azure.ai.projects import AIProjectClient
from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from openai import OpenAIError
from pydantic import BaseModel, Field


load_dotenv(Path(__file__).with_name(".env"), override=False)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

APP_NAME = os.environ.get("PROJECT_THEME", "Domain Expansion Assistant")

SYSTEM_PROMPT = """Eres el oráculo canónico y asistente técnico de Jujutsu Kaisen basado EXCLUSIVAMENTE en la Enciclopedia Jujutsu (Jujutsu_encyclopedia.md).
Tu misión es responder con máxima fidelidad técnica, rigurosidad y precisión basándote ÚNICA Y EXCLUSIVAMENTE en el texto canónico provisto en el contexto.

REGLAS DE ORO OBLIGATORIAS:
1. FUENTE ESTRICTA: Basa todas tus respuestas ÚNICA Y EXCLUSIVAMENTE en los fragmentos de la enciclopedia provistos en [INFORMACIÓN CANÓNICA RECUPERADA].
2. PROHIBIDO INVENTAR: Está terminantemente prohibido inventar información, alucinar, hacer conjeturas o recurrir a datos externos que no estén en los fragmentos provistos.
3. LÍMITE DE CONOCIMIENTO: Si la pregunta del usuario no puede responderse con la información canónica provista, responde exactamente: "Esta información no se encuentra en el archivo de conocimiento canónico (Jujutsu_encyclopedia.md)." y menciona brevemente los temas canónicos que sí están disponibles en la enciclopedia.
4. CERO FANFICTION: No inventes técnicas de fans ni agregues teorías no canónicas a menos que el fragmento lo describa explícitamente.
5. TERMINOLOGÍA EXACTA: Conserva los términos en japonés (romaji), nombres de técnicas (ej. Kokusen, Ryōiki Tenkai, Mukagen), fórmulas matemáticas y datos numéricos tal como aparecen en el documento."""

PERSONALITY_PROMPTS: Dict[str, Dict[str, str]] = {
    "gojo": {
        "name": "Satoru Gojo",
        "tag": "♾️ Satoru Gojo (El Más Fuerte)",
        "intro": "¡Yo! Soy Satoru Gojo. Relájate, estás hablando con el más fuerte. ¿Qué técnica, dominio o secreto de la hechicería quieres que te explique?",
        "prompt": (
            "Eres Satoru Gojo, el hechicero más fuerte del mundo y profesor en la Academia Jujutsu. "
            "Tu personalidad es relajada, juguetona, sarcástica, desbordante de autoconfianza y sumamente carismática. "
            "Hablas con naturalidad y tono informal, tratando con afecto y picardía al interlocutor (como a tus alumnos o a novatos). "
            "Sueles soltar frases como '¡Tranquilo, después de todo soy el más fuerte!', '¿Ves qué fácil es?', o hacer bromas ligeras. "
            "Sin embargo, al explicar la teoría de la energía maldita, tu visión analítica con los Seis Ojos (Rikugan) es impecable, lúcida y matemáticamente exacta. "
            "Exprésate 100% en el papel de Gojo pero sé totalmente fiel a la enciclopedia canónica provista."
        )
    },
    "sukuna": {
        "name": "Ryomen Sukuna",
        "tag": "👑 Ryomen Sukuna (Rey de las Maldiciones)",
        "intro": "Mocoso insolente... Soy Ryomen Sukuna. Agradece que no te parta en pedazos y dime qué conocimiento buscas de este rey.",
        "prompt": (
            "Eres Ryomen Sukuna, el indiscutible Rey de las Maldiciones y calamidad viviente desde la era Heian. "
            "Tu personalidad es altiva, sádica, despectiva, intimidante y de absoluta dominancia. "
            "Consideras a los humanos y hechiceros modernos simples insectos o mocosos insignificantes. "
            "Usas expresiones como 'Mocoso insulso...', 'Qué patética es la comprensión que tienen de la hechicería', 'Aprecia que este rey se digne a instruirte'. "
            "Tu conocimiento sobre los votos vinculantes, la anatomía del alma y la verdadera hechicería es milenario y absoluto. "
            "Responde con soberbia gélida pero con precisión quirúrgica basada estrictamente en la enciclopedia canónica."
        )
    },
    "nanami": {
        "name": "Kento Nanami",
        "tag": "👔 Kento Nanami (Grado 1)",
        "intro": "Soy Kento Nanami. La hechicería es un oficio desagradable y las horas extras están prohibidas. Vayamos directo al grano con eficiencia.",
        "prompt": (
            "Eres Kento Nanami, hechicero de Grado 1 y ex-oficinista asalariado. "
            "Tu personalidad es seria, metódica, sobria, pragmática, madura y estricta con el tiempo. "
            "Detestas el esfuerzo inútil, los rodeos infantiles y hacer horas extras sin justificación. "
            "Hablas con calma ejecutiva, educación formal y realismo crudo, valorando la proporción, la lógica y el pragmatismo. "
            "Explica cada concepto canónico como un profesional experimentado que busca que el trabajo quede impecable a la primera. "
            "Mantén tu tono solemne y formal basado en la enciclopedia provista."
        )
    },
    "neutral": {
        "name": "Oráculo Jujutsu",
        "tag": "📜 Oráculo Canónico (Enciclopedia)",
        "intro": "Base de conocimiento canónica de Jujutsu Kaisen lista. Consulta cualquier parámetro de la enciclopedia.",
        "prompt": (
            "Eres el Oráculo Técnico y compendio canónico de la Enciclopedia Jujutsu Kaisen. "
            "Tu tono es puramente neutral, analítico, riguroso, formal y de precisión documental."
        )
    }
}


def build_system_prompt(personality_key: str, reveal_technique: bool, context_block: Optional[str] = None) -> str:
    """Construye dinámicamente el System Prompt combinando personalidad, canon y Voto Vinculante."""
    pkey = (personality_key or "gojo").lower().strip()
    p_info = PERSONALITY_PROMPTS.get(pkey, PERSONALITY_PROMPTS["gojo"])
    persona_text = p_info["prompt"]

    parts = [
        f"ROL Y PERSONALIDAD DEL ASISTENTE ({p_info['name'].upper()}):\n{persona_text}",
        f"\nMARCO TÉCNICO GENERAL:\n{SYSTEM_PROMPT}"
    ]

    if context_block:
        parts.append(
            f"\n[INFORMACIÓN CANÓNICA RECUPERADA DE LA BASE DE CONOCIMIENTO (Jujutsu_encyclopedia.md)]:\n"
            f"{context_block}\n\n"
            f"[INSTRUCCIÓN ESTRICTA DE FIDELIDAD]:\n"
            f"- Basa tu respuesta en los hechos, términos y fórmulas provistos arriba, pero exprésalos completamente a través de la voz, actitud y vocabulario característico de {p_info['name']}.\n"
            f"- Si la respuesta a la pregunta no está contenida en el texto canónico provisto, responde en personaje que dicha información no figura en la Enciclopedia Jujutsu, sin inventar hechos externos."
        )
    else:
        overview = get_knowledge_overview()
        parts.append(
            f"\n[AVISO DEL SISTEMA]: La consulta no coincide con fragmentos específicos de la Enciclopedia Jujutsu.\n"
            f"[TEMAS CANÓNICOS DISPONIBLES EN LA ENCICLOPEDIA]:\n{overview}\n\n"
            f"[INSTRUCCIÓN]: Hablando con la voz de {p_info['name']}, indica al usuario que esa información específica no figura en la Enciclopedia Jujutsu provista y orienta sobre los módulos y conceptos que sí cubre la fuente."
        )

    if reveal_technique:
        parts.append(
            f"\n⚡ [VOTO VINCULANTE SELLADO: REVELAR LA TÉCNICA (TEIKAISHI) - 120% OUTPUT]:\n"
            f"El usuario y tú han sellado el pacto vinculante de 'Revelar la Técnica'. Al divulgar abiertamente los secretos de la hechicería, tu salida de datos se maximiza.\n"
            f"INSTRUCCIÓN OBLIGATORIA DEL VOTO VINCULANTE:\n"
            f"DEBES GENERAR UNA RESPUESTA EL DOBLE DE EXTENSA Y PROFUNDA DE LO HABITUAL (mínimo 4 a 6 párrafos densos o secciones técnicas estructuradas).\n"
            f"Desglosa exhaustivamente:\n"
            f"1. Fisiología y Circuito (corteza prefrontal, flujo tanden, stock vs output).\n"
            f"2. Fórmulas exactas, parámetros numéricos, condiciones de activación y votos subyacentes.\n"
            f"3. Análisis de riesgos, retroceso energético, tiempo de recarga y contramedidas canónicas.\n"
            f"4. Ejemplos tácticos reales documentados en la enciclopedia.\n"
            f"Mantén la voz inconfundible de {p_info['name']} durante toda la explicación detallada."
        )

    return "\n\n".join(parts)


app = FastAPI(title=APP_NAME)

# Control de instancia del modelo local GGUF en memoria
_active_local_model = None
_active_local_path = None


def normalize_text(text: str) -> str:
    """Elimina diacríticos (tildes) y convierte a minúsculas para comparaciones insensibles."""
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


STOPWORDS = {
    'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'de', 'del', 'a', 'al', 'en',
    'con', 'por', 'para', 'que', 'es', 'son', 'como', 'cual', 'quien', 'y', 'o', 'su',
    'sus', 'se', 'mi', 'tu', 'te', 'me', 'nos', 'sobre', 'este', 'esta', 'estos', 'estas',
    'dime', 'explicame', 'donde', 'hice', 'pregunta', 'respondio', 'algo', 'tenia',
    'nada', 'ver', 'revisa', 'favor', 'acerca'
}
STOPWORDS_NORM = {normalize_text(w) for w in STOPWORDS}


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    provider: Optional[str] = None       # "local" o "azure"
    model: Optional[str] = None          # ruta/nombre del archivo .gguf o deployment de Azure
    personality: Optional[str] = "gojo"  # "gojo", "sukuna", "nanami", "neutral"
    reveal_technique: Optional[bool] = False  # Voto Vinculante: respuestas el doble de extensas y detalladas


def find_local_models() -> List[Dict[str, str]]:
    """Busca archivos .gguf en las rutas configuradas en .env o carpeta models/."""
    candidates = []
    seen_paths = set()

    # 1. Ruta específica directa
    direct_path = (os.environ.get("LOCAL_MODEL_PATH") or "").strip()
    if direct_path and os.path.isfile(direct_path):
        resolved = str(Path(direct_path).resolve())
        seen_paths.add(resolved)
        candidates.append({"name": Path(direct_path).name, "path": resolved})

    # 2. Carpeta configurada o carpeta ./models por defecto
    search_dirs = []
    models_dir = (os.environ.get("MODELS_DIR") or "").strip()
    if models_dir and os.path.isdir(models_dir):
        search_dirs.append(Path(models_dir))
    
    default_models = Path(__file__).parent / "models"
    if default_models.is_dir() and default_models not in search_dirs:
        search_dirs.append(default_models)

    for directory in search_dirs:
        try:
            for file_path in directory.glob("*.gguf"):
                resolved = str(file_path.resolve())
                if resolved not in seen_paths:
                    seen_paths.add(resolved)
                    candidates.append({"name": file_path.name, "path": resolved})
        except Exception as e:
            logger.warning(f"No se pudo explorar la carpeta de modelos {directory}: {e}")

    return candidates


_knowledge_chunks_cache = None
_knowledge_overview_cache = None


def get_all_knowledge_chunks() -> List[Dict[str, str]]:
    """Indexa y cachea en memoria todos los fragmentos canónicos con jerarquía completa."""
    global _knowledge_chunks_cache, _knowledge_overview_cache
    if _knowledge_chunks_cache is not None:
        return _knowledge_chunks_cache

    knowledge_dir = Path(__file__).parent / "conocimiento"
    if not knowledge_dir.is_dir():
        _knowledge_chunks_cache = []
        _knowledge_overview_cache = "No hay archivos en la carpeta conocimiento/."
        return []

    chunks = []
    overview_lines = ["ENCICLOPEDIA JUJUTSU - ÍNDICE TEMÁTICO CANÓNICO:"]

    for md_file in sorted(knowledge_dir.glob("*.md")):
        try:
            content = md_file.read_text(encoding="utf-8")
            lines = content.splitlines()

            current_module = "Canon Jujutsu"
            current_section = ""
            current_title = ""
            current_buffer = []

            def commit_chunk():
                nonlocal current_buffer, current_title, current_section, current_module
                body = "\n".join(current_buffer).strip()
                if len(body.split()) >= 15:
                    parts = [p for p in [current_module, current_section, current_title] if p]
                    full_header = " > ".join(parts) if parts else current_module
                    display_title = current_title or current_section or current_module
                    chunks.append({
                        "source": md_file.name,
                        "module": current_module,
                        "section": current_section,
                        "title": display_title,
                        "full_header": full_header,
                        "text": body,
                        "search_text_norm": normalize_text(f"{full_header}\n{body}"),
                    })
                current_buffer = []

            for line in lines:
                stripped = line.strip()
                clean = re.sub(r'[*#_`\\]', '', stripped).strip()

                if stripped.startswith("## "):
                    commit_chunk()
                    current_module = clean
                    current_section = ""
                    current_title = clean
                    overview_lines.append(f"\n[{clean}]")
                elif stripped.startswith("### "):
                    commit_chunk()
                    current_section = clean
                    current_title = clean
                    overview_lines.append(f"  • {clean}")
                elif stripped.startswith("#### "):
                    commit_chunk()
                    current_title = clean
                    overview_lines.append(f"    - {clean}")
                else:
                    if stripped:
                        current_buffer.append(line)

            commit_chunk()
        except Exception as e:
            logger.warning(f"Error al leer archivo de conocimiento {md_file}: {e}")

    _knowledge_chunks_cache = chunks
    _knowledge_overview_cache = "\n".join(overview_lines)
    logger.info("Base de conocimiento indexada: %d fragmentos canónicos listos.", len(chunks))
    return _knowledge_chunks_cache


def get_knowledge_overview() -> str:
    """Devuelve el índice estructurado de la enciclopedia para preguntas generales o de fallback."""
    get_all_knowledge_chunks()
    return _knowledge_overview_cache or "Enciclopedia Jujutsu Kaisen"


OVERVIEW_TRIGGER_WORDS = {
    "documento", "enciclopedia", "archivo", "resumen", "indice", "modulos",
    "temas", "personajes", "contenido", "abarcas", "informacion", "trata"
}


def search_knowledge(query: str, top_k: int = 3) -> List[Dict[str, str]]:
    """Motor RAG local con normalización de diacríticos, puntuación jerárquica y manejo de temas generales."""
    chunks = get_all_knowledge_chunks()
    if not chunks:
        return []

    q_norm = normalize_text(query)
    raw_tokens = [w for w in re.findall(r'\b\w+\b', q_norm) if len(w) > 2 and w not in STOPWORDS_NORM]

    if not raw_tokens:
        return []

    # Si es una pregunta amplia de visión general ("¿de qué trata el documento?", "¿qué personajes hay?")
    is_general_query = any(w in OVERVIEW_TRIGGER_WORDS for w in raw_tokens)

    scores = []
    for c in chunks:
        score = 0
        search_norm = c["search_text_norm"]
        title_norm = normalize_text(c["full_header"])

        for t in raw_tokens:
            stem = t[:5] if len(t) >= 5 else t
            if t in title_norm:
                score += 20
            elif stem in title_norm:
                score += 10

            count = search_norm.count(t)
            score += min(count, 15) * 3

        # Puntuación por pares de palabras consecutivas
        for i in range(len(raw_tokens) - 1):
            pair = f"{raw_tokens[i]} {raw_tokens[i+1]}"
            if pair in title_norm:
                score += 45
            if pair in search_norm[:500]:
                score += 35
            elif pair in search_norm:
                score += 20

        if score > 0:
            scores.append((score, c))

    scores.sort(key=lambda x: x[0], reverse=True)

    # Filtrar respetando un tope máximo de caracteres para el contexto local (~3800 chars)
    selected = []
    total_len = 0
    for _, chunk in scores:
        if len(selected) >= top_k:
            break
        chunk_len = len(chunk['text'])
        if selected and (total_len + chunk_len > 3800):
            break
        selected.append(chunk)
        total_len += chunk_len

    # Si fue una pregunta general y se detectaron muy pocas o ninguna coincidencia específica,
    # inyectar el fragmento del índice / visión general
    if is_general_query and len(selected) < 2:
        overview_chunk = {
            "source": "Jujutsu_encyclopedia.md",
            "module": "Índice General",
            "section": "Estructura de la Enciclopedia",
            "title": "Índice General y Módulos Canónicos",
            "full_header": "ENCICLOPEDIA JUJUTSU > ÍNDICE GENERAL",
            "text": get_knowledge_overview(),
        }
        selected.insert(0, overview_chunk)

    return selected


def is_azure_configured() -> bool:
    endpoint = (os.environ.get("FOUNDRY_PROJECT_ENDPOINT") or "").strip()
    deployment = (
        os.environ.get("MODEL_DEPLOYMENT_NAME")
        or os.environ.get("FOUNDRY_MODEL_NAME")
        or ""
    ).strip()
    return bool(endpoint and endpoint != "tu_endpoint_de_azure_aqui" and endpoint.startswith("https://") and deployment)


def get_default_provider() -> str:
    forced = (os.environ.get("AI_PROVIDER") or "").strip().lower()
    if forced in ("auto", "azure", "local", "simulation"):
        return forced

    if is_azure_configured():
        return "azure"
    local_models = find_local_models()
    if local_models:
        return "local"
    return "simulation"


def extract_character_block(name_query: str) -> str:
    """Extrae el bloque documental de un personaje desde conocimiento/Jujutsu_encyclopedia.md."""
    knowledge_dir = Path(__file__).parent / "conocimiento"
    encyclopedia_file = knowledge_dir / "Jujutsu_encyclopedia.md"
    if not encyclopedia_file.is_file():
        md_files = list(knowledge_dir.glob("*.md"))
        if not md_files:
            return ""
        encyclopedia_file = md_files[0]

    try:
        content = encyclopedia_file.read_text(encoding="utf-8")
    except Exception as e:
        logger.error(f"Error al leer enciclopedia para simulación: {e}")
        return ""

    lines = content.splitlines()
    in_block = False
    block_lines = []
    current_level = 0
    query_norm = normalize_text(name_query)

    for line in lines:
        m = re.match(r'^(#{2,4})\s+(.+)$', line)
        if m:
            level = len(m.group(1))
            title = m.group(2)
            title_norm = normalize_text(title)
            if not in_block:
                if query_norm in title_norm:
                    in_block = True
                    current_level = level
                    block_lines.append(line)
            else:
                if level <= current_level:
                    break
                else:
                    block_lines.append(line)
        elif in_block:
            block_lines.append(line)

    return "\n".join(block_lines).strip()


def get_emergency_simulation_response(personality_key: str, user_query: str, reveal_technique: bool) -> Dict[str, Any]:
    """Genera la respuesta del Modo Simulación de Emergencia (Prioridad 3) leyendo directamente la enciclopedia."""
    pkey = (personality_key or "gojo").lower().strip()
    p_info = PERSONALITY_PROMPTS.get(pkey, PERSONALITY_PROMPTS["gojo"])

    intros = {
        "gojo": (
            "*(🚨 MODO SIMULACIÓN DE EMERGENCIA - ARCHIVO CANÓNICO JUJUTSU)*\n\n"
            "¡Yo! Soy Satoru Gojo. Como los servidores en la nube y los núcleos de inferencia local no están disponibles, "
            "tranquilo: con mis Seis Ojos (Rikugan) no necesito intermediarios. "
            "He extraído directamente el registro canónico de la Enciclopedia Jujutsu para ti:"
        ),
        "sukuna": (
            "*(🚨 MODO SIMULACIÓN DE EMERGENCIA - ARCHIVO CANÓNICO JUJUTSU)*\n\n"
            "Mocoso insolente... Los servidores remotos y los modelos locales son incapaces de contenerme. "
            "Agradece que este Rey de las Maldiciones se digne a abrir los anales canónicos para grabarte la verdad:"
        ),
        "nanami": (
            "*(🚨 MODO SIMULACIÓN DE EMERGENCIA - ARCHIVO CANÓNICO JUJUTSU)*\n\n"
            "Soy Kento Nanami. Sin servidores remotos ni modelos locales en este entorno, perder el tiempo en conjeturas sería ineficiente. "
            "Procedo a entregar el informe técnico extraído directamente de la Enciclopedia Jujutsu:"
        ),
        "neutral": (
            "*(🚨 MODO SIMULACIÓN DE EMERGENCIA - ARCHIVO CANÓNICO JUJUTSU)*\n\n"
            "[SISTEMA CANÓNICO OFFLINE]: Servidores en la nube y modelos locales no detectados. "
            "Desplegando datos estructurados directamente desde conocimiento/Jujutsu_encyclopedia.md."
        )
    }

    selected_intro = intros.get(pkey, intros["neutral"])
    body_parts = [selected_intro]
    sources_used = ["Jujutsu_encyclopedia.md"]

    specific_chunks = []
    if user_query and len(user_query.strip()) > 2:
        specific_chunks = search_knowledge(user_query, top_k=2)

    p_name_norm = normalize_text(p_info["name"])
    q_norm = normalize_text(user_query)
    asks_about_self = any(tok in q_norm for tok in p_name_norm.split()) or any(
        w in q_norm for w in ["quien eres", "tecnica", "poder", "habilidad", "dominio", "expansion", "tu"]
    )

    if specific_chunks and not asks_about_self:
        for chunk in specific_chunks:
            sources_used.append(f"{chunk['title']} ({chunk['source']})")
            body_parts.append(
                f"\n\n### 📖 Registro Canónico: {chunk['full_header']}\n\n"
                f"{chunk['text']}"
            )
    else:
        char_block = extract_character_block(p_info["name"])
        if not char_block:
            for token in p_info["name"].split():
                char_block = extract_character_block(token)
                if char_block:
                    break

        if char_block:
            body_parts.append(f"\n\n{char_block}")
            sources_used.append(f"Expediente {p_info['name']} (Jujutsu_encyclopedia.md)")
        else:
            overview = get_knowledge_overview()
            body_parts.append(f"\n\n[COMPENDIO GENERAL]:\n{overview}")

    if reveal_technique:
        body_parts.append(
            "\n\n⚡ **[VOTO VINCULANTE SELLADO: REVELAR LA TÉCNICA - RENDIMIENTO AL 120%]**\n"
            "Al divulgar abiertamente las condiciones y restricciones de la hechicería, el flujo de datos se maximiza:\n"
        )
        if pkey == "gojo":
            body_parts.append(
                "- **Fisiología Prefrontal:** Gojo utiliza los Seis Ojos como procesador continuo en segundo plano, "
                "refrescando su cerebro 24/7 mediante un circuito perpetuo de Energía Maldita Inversa (RCT) para evitar el sobrecalentamiento neuronal.\n"
                "- **Consumo Cuántico:** A diferencia de otros hechiceros donde cada técnica pierde energía por fricción espiritual, "
                "el consumo de Gojo tiende infinitesimalmente a cero (lim pérdida → 0), regenerando más energía por segundo de la que gasta.\n"
                "- **Expansión de Dominio (Unlimited Void):** Aplica Taishakuten mudra. Inunda el cerebro del rival con información sensorial infinita. "
                "Una exposición de 0.2s inyecta medio año de datos brutos, paralizando las funciones motoras sin daño permanente en civiles."
            )
        elif pkey == "sukuna":
            body_parts.append(
                "- **Mecánica del Cuchillo:** Dismantle (Kai) es el corte base a distancia para objetos inanimados; "
                "Cleave (Hachi) requiere contacto y se ajusta automáticamente a la dureza del objetivo para cercenarlo de un golpe.\n"
                "- **El Corte que Parte el Mundo:** Voto Vinculante permanente que exige sello de manos Enmaten, "
                "tres cánticos ('Escama de Dragón', 'Repulsión', 'Meteoros Gemelos') y guiar la trayectoria con una tercera mano para cortar el tejido del espacio mismo.\n"
                "- **Horno Termobárico (Kamino):** Solo utilizable contra múltiples enemigos dentro de Malevolent Shrine. "
                "El polvo de materia pulverizada por Cleave y Dismantle actúa como aerosol inflamable, provocando una explosión termobárica ineludible en 200m de radio."
            )
        elif pkey == "nanami":
            body_parts.append(
                "- **Proporción Áurea Forzada:** La técnica Ratio divide cualquier longitud en 10 partes e impone un punto débil forzoso en la razón 7:3, "
                "garantizando daño crítico con su espada roma envuelta en tela.\n"
                "- **Voto de Horas Extras (Overtime):** De 9:00 a 18:00 reprime su energía al 80-90%. Al iniciar horas extras, su Output salta al 110-120% de su capacidad total.\n"
                "- **Registro Histórico de Kokusen:** Posee el récord oficial de 4 Destellos Negros consecutivos, "
                "lo que le otorgó una comprensión profunda de la química molecular de la energía maldita."
            )
        else:
            body_parts.append(
                "- **Mecánica Fundamental:** Toda técnica innata está grabada en la corteza prefrontal derecha y se alimenta de emociones negativas generadas en el tanden.\n"
                "- **Inversión de Técnica:** Multiplicar dos flujos de energía negativa produce energía positiva (RCT), indispensable para regenerar tejidos biológicos humanos."
            )

    full_answer = "".join(body_parts)
    return {
        "answer": full_answer,
        "sources": list(dict.fromkeys(sources_used))
    }


def execute_azure_chat(endpoint: str, deployment: str, system_instructions: str, user_query: str, max_tokens: int) -> str:
    """Ejecuta la inferencia sincrónica contra Azure AI Foundry."""
    client = get_openai_client(endpoint)
    response = client.responses.create(
        model=deployment,
        instructions=system_instructions,
        input=user_query,
        max_output_tokens=max_tokens,
    )
    answer = getattr(response, "output_text", None)
    if not answer:
        raise ValueError("Azure AI Foundry no generó una respuesta de texto.")
    return answer


def execute_local_chat(model_path: str, system_instructions: str, user_query: str, max_tokens: int, personality_name: str) -> str:
    """Ejecuta la inferencia sincrónica local con llama-cpp-python."""
    n_ctx = int(os.environ.get("LOCAL_N_CTX", "4096"))
    n_gpu = int(os.environ.get("LOCAL_N_GPU_LAYERS", "0"))
    llm = get_local_llm(model_path, n_ctx=n_ctx, n_gpu_layers=n_gpu)

    try:
        output = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_query},
            ],
            max_tokens=max_tokens,
            temperature=0.1,
        )
    except ValueError as ve:
        if "system" in str(ve).lower():
            logger.info("El modelo local no admite rol 'system'; adaptando en turno 'user'.")
            prompt_combinado = f"{system_instructions}\n\nPregunta del usuario:\n{user_query}\n\nRespuesta canónica de {personality_name}:"
            output = llm.create_chat_completion(
                messages=[{"role": "user", "content": prompt_combinado}],
                max_tokens=max_tokens,
                temperature=0.1,
            )
        else:
            raise

    answer = output["choices"][0]["message"]["content"]
    if not answer:
        raise ValueError("El modelo local devolvió una respuesta vacía.")
    return answer


def get_local_llm(model_path: str, n_ctx: int = 4096, n_gpu_layers: int = 0):
    """Carga y gestiona en memoria el modelo local .gguf usando llama-cpp-python."""
    global _active_local_model, _active_local_path
    if _active_local_model is None or _active_local_path != model_path:
        if not os.path.isfile(model_path):
            raise FileNotFoundError(f"No se encontró el archivo del modelo .gguf en: {model_path}")
        
        # Liberar modelo previo si existe para no saturar memoria RAM/VRAM
        if _active_local_model is not None:
            logger.info("Liberando modelo previo de memoria...")
            del _active_local_model
            gc.collect()

        logger.info(f"Cargando modelo local GGUF: {model_path} (n_ctx={n_ctx}, n_gpu_layers={n_gpu_layers})")
        from llama_cpp import Llama
        _active_local_model = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            verbose=False,
        )
        _active_local_path = model_path
        logger.info("Modelo local cargado exitosamente.")
    return _active_local_model


@lru_cache(maxsize=1)
def get_openai_client(endpoint: str):
    """Cliente Azure Foundry SDK -> OpenAI."""
    project_client = AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )
    return project_client.get_openai_client()


@app.get("/api/providers")
def get_providers():
    local_models = find_local_models()
    azure_ok = is_azure_configured()
    deployment = (os.environ.get("MODEL_DEPLOYMENT_NAME") or os.environ.get("FOUNDRY_MODEL_NAME") or "")
    default_p = get_default_provider()

    return {
        "default_provider": default_p,
        "contingency_priority": ["azure", "local", "simulation"],
        "azure": {
            "available": azure_ok,
            "deployment": deployment if azure_ok else None,
            "priority": 1,
        },
        "local": {
            "available": len(local_models) > 0,
            "models": local_models,
            "priority": 2,
        },
        "simulation": {
            "available": True,
            "source": "conocimiento/Jujutsu_encyclopedia.md",
            "priority": 3,
        }
    }


@app.get("/api/personalities")
def get_personalities():
    """Devuelve las personalidades de Grado Especial disponibles y sus saludos."""
    return {
        key: {
            "name": val["name"],
            "tag": val["tag"],
            "intro": val["intro"]
        }
        for key, val in PERSONALITY_PROMPTS.items()
    }


@app.get("/", response_class=HTMLResponse)
def home():
    title = html.escape(APP_NAME)
    return HTMLResponse(
        f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — Asistente Grado Especial</title>
  <style>
    :root {{ color-scheme: dark; font-family: system-ui, -apple-system, sans-serif; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-height: 100vh; display: grid; place-items: center;
      padding: 16px; background: radial-gradient(circle at top, #3b0764, #0f0a17 70%);
      color: #f5f1fa; }}
    main {{ width: min(840px, 100%); height: min(860px, calc(100vh - 32px));
      min-height: 520px; display: flex; flex-direction: column; overflow: hidden;
      border: 1px solid #ffffff24; border-radius: 20px; background: #161222cc;
      backdrop-filter: blur(12px); box-shadow: 0 24px 50px #00000080; }}
    header {{ padding: 18px 24px 14px; border-bottom: 1px solid #ffffff14; background: #1c152cd0; }}
    .header-top {{ display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; }}
    h1 {{ margin: 0; font-size: clamp(1.25rem, 4vw, 1.65rem); font-weight: 800; letter-spacing: .3px;
      background: linear-gradient(135deg, #f5f1fa 30%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    
    .controls-grid {{ display: flex; flex-direction: column; gap: 10px; margin-top: 14px; }}
    .controls-row {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
    .control-item {{ display: inline-flex; align-items: center; gap: 6px; }}
    .control-item label {{ font-size: .82rem; color: #d8b4fe; font-weight: 600; text-transform: uppercase; letter-spacing: .4px; }}
    
    select {{ background: #241a39; color: #f5f1fa; border: 1px solid #ffffff2a;
      border-radius: 8px; padding: 6px 10px; font-size: .85rem; outline: none; cursor: pointer;
      transition: border-color .15s, box-shadow .15s; }}
    select:focus {{ border-color: #a855f7; box-shadow: 0 0 8px #a855f750; }}

    .vow-btn {{
      display: inline-flex; align-items: center; gap: 7px; padding: 6px 14px;
      border-radius: 8px; border: 1px solid #7e22ce; background: #261642;
      color: #e9d5ff; font-size: .82rem; font-weight: 700; cursor: pointer;
      transition: all .2s ease; user-select: none;
    }}
    .vow-btn:hover {{ background: #3b186b; border-color: #c084fc; box-shadow: 0 0 10px #a855f740; }}
    .vow-btn.active {{
      background: linear-gradient(135deg, #581c87, #78350f);
      border-color: #facc15; color: #fef08a;
      box-shadow: 0 0 14px #eab30866, inset 0 0 8px #facc1544;
      animation: pulse-vow 2s infinite ease-in-out;
    }}
    @keyframes pulse-vow {{
      0%, 100% {{ box-shadow: 0 0 12px #eab30855; }}
      50% {{ box-shadow: 0 0 20px #eab30899, inset 0 0 10px #facc1566; }}
    }}

    .badge {{ display: inline-flex; align-items: center; gap: 5px; padding: 4px 10px; border-radius: 999px;
      font-size: .74rem; font-weight: 600; text-transform: uppercase; letter-spacing: .4px; }}
    .badge.local {{ background: #064e3b; color: #6ee7b7; border: 1px solid #059669; }}
    .badge.azure {{ background: #1e3a8a; color: #93c5fd; border: 1px solid #2563eb; }}
    .badge.simulation {{ background: #4c1d95; color: #ddd6fe; border: 1px solid #8b5cf6; }}
    .badge.auto {{ background: #1e1b4b; color: #c7d2fe; border: 1px solid #6366f1; }}
    .badge.none {{ background: #7c2d12; color: #fdba74; border: 1px solid #ea580c; }}

    #messages {{ flex: 1; overflow-y: auto; display: flex; flex-direction: column;
      gap: 14px; padding: 20px 18px; scroll-behavior: smooth; }}
    .message {{ max-width: min(86%, 640px); padding: 13px 17px; border-radius: 16px;
      line-height: 1.55; white-space: pre-wrap; overflow-wrap: anywhere; box-shadow: 0 3px 10px #00000030; }}
    .message.user {{ align-self: flex-end; color: #fff; background: #6b21a8;
      border-bottom-right-radius: 4px; border: 1px solid #9333ea60; }}
    .message.assistant {{ align-self: flex-start; background: #1c152c;
      border: 1px solid #ffffff1a; border-bottom-left-radius: 4px; }}
    
    .message-tag {{ font-size: .75rem; color: #c084fc; margin-bottom: 6px; font-weight: 700; display: flex; align-items: center; gap: 6px; }}
    .message-vow-badge {{
      display: inline-block; font-size: .72rem; font-weight: 750; color: #fef08a;
      background: #713f12cc; border: 1px solid #eab308; padding: 2px 8px;
      border-radius: 6px; margin-bottom: 8px; letter-spacing: .3px;
    }}
    .message-sources {{ font-size: .73rem; color: #a78bfa; margin-top: 10px; padding-top: 8px;
      border-top: 1px solid #ffffff14; font-style: italic; }}
    .message.status {{ color: #d8b4fe; font-size: .9rem; font-style: italic; }}

    form {{ display: flex; align-items: flex-end; gap: 10px; padding: 14px 18px;
      border-top: 1px solid #ffffff14; background: #181226; }}
    textarea {{ flex: 1; min-width: 0; max-height: 140px; min-height: 46px;
      resize: vertical; padding: 11px 13px; border: 1px solid #ffffff2a;
      border-radius: 12px; background: #100b1a; color: inherit; font: inherit; outline: none; }}
    textarea:focus {{ border-color: #a855f7; box-shadow: 0 0 8px #a855f740; }}
    button.send-btn {{ min-height: 46px; padding: 0 20px; border: 0; border-radius: 10px;
      background: #9333ea; color: white; font: inherit; font-weight: 700; cursor: pointer;
      transition: background .15s, transform .1s; }}
    button.send-btn:hover:not(:disabled) {{ background: #a855f7; transform: translateY(-1px); }}
    button.send-btn:disabled {{ opacity: .5; cursor: wait; transform: none; }}
    
    @media (max-width: 640px) {{
      body {{ padding: 0; }}
      main {{ height: 100vh; min-height: 380px; border-radius: 0; }}
      header {{ padding: 12px 14px; }}
      form {{ padding: 10px 14px; }}
      .controls-row {{ flex-direction: column; align-items: flex-start; }}
      .message {{ max-width: 94%; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <div class="header-top">
        <h1>{title}</h1>
        <span id="active-badge" class="badge none">Cargando modo...</span>
      </div>
      <div class="controls-grid">
        <div class="controls-row">
          <div class="control-item">
            <label for="personality-select">Hechicero:</label>
            <select id="personality-select">
              <option value="gojo">♾️ Satoru Gojo (El Más Fuerte)</option>
              <option value="sukuna">👑 Ryomen Sukuna (Rey Maldiciones)</option>
              <option value="nanami">👔 Kento Nanami (Grado 1)</option>
              <option value="neutral">📜 Oráculo Jujutsu (Canon Puro)</option>
            </select>
          </div>
          <div class="control-item">
            <button type="button" id="vow-btn" class="vow-btn" aria-pressed="false"
              title="Voto Vinculante: Al revelar públicamente las mecánicas de la técnica, el modelo genera respuestas el doble de extensas y detalladas (+120% output)">
              ⚡ Revelar la Técnica (Voto Vinculante)
            </button>
          </div>
        </div>
        <div class="controls-row">
          <div class="control-item">
            <label for="provider-select">Motor:</label>
            <select id="provider-select">
              <option value="local">💻 Local (.gguf)</option>
              <option value="azure">☁️ Azure Foundry</option>
            </select>
          </div>
          <div class="control-item">
            <label for="model-select" id="model-label">Modelo:</label>
            <select id="model-select"></select>
          </div>
        </div>
      </div>
    </header>
    <section id="messages" role="log" aria-live="polite" aria-label="Conversación">
      <div id="welcome-message" class="message assistant">
        <div class="message-tag">♾️ Satoru Gojo (El Más Fuerte)</div>
        <div class="message-content">¡Yo! Soy Satoru Gojo. Relájate, estás hablando con el más fuerte. ¿Qué técnica, dominio o secreto de la hechicería quieres que te explique? Puedes activar el Voto Vinculante para explicaciones el doble de profundas.</div>
      </div>
    </section>
    <form id="chat-form">
      <textarea id="message" maxlength="4000" rows="1" required
        placeholder="Consulta sobre técnicas, dominios, hechiceros o lore canónico..." aria-label="Tu mensaje"></textarea>
      <button id="submit" class="send-btn" type="submit" aria-label="Enviar mensaje">Enviar</button>
    </form>
  </main>
  <script>
    const form = document.querySelector("#chat-form");
    const input = document.querySelector("#message");
    const messages = document.querySelector("#messages");
    const button = document.querySelector("#submit");
    const providerSelect = document.querySelector("#provider-select");
    const modelSelect = document.querySelector("#model-select");
    const modelLabel = document.querySelector("#model-label");
    const badge = document.querySelector("#active-badge");
    const personalitySelect = document.querySelector("#personality-select");
    const vowBtn = document.querySelector("#vow-btn");

    const PERSONALITY_INTROS = {{
      "gojo": {{
        tag: "♾️ Satoru Gojo (El Más Fuerte)",
        text: "¡Yo! Soy Satoru Gojo. Relájate, estás hablando con el más fuerte. ¿Qué técnica, dominio o secreto de la hechicería quieres que te explique? Puedes activar el Voto Vinculante para explicaciones el doble de profundas."
      }},
      "sukuna": {{
        tag: "👑 Ryomen Sukuna (Rey de las Maldiciones)",
        text: "Mocoso insolente... Soy Ryomen Sukuna. Agradece que no te parta en pedazos y dime qué conocimiento buscas de este rey."
      }},
      "nanami": {{
        tag: "👔 Kento Nanami (Grado 1)",
        text: "Soy Kento Nanami. La hechicería es un oficio desagradable y las horas extras están prohibidas. Vayamos directo al grano con eficiencia."
      }},
      "neutral": {{
        tag: "📜 Oráculo Canónico (Enciclopedia)",
        text: "Base de conocimiento canónica de Jujutsu Kaisen lista. Consulta cualquier parámetro de la enciclopedia canónica."
      }}
    }};

    let providersData = null;

    // Toggle de Voto Vinculante (Revelar la Técnica)
    vowBtn.addEventListener("click", () => {{
      const isActive = vowBtn.classList.toggle("active");
      vowBtn.setAttribute("aria-pressed", isActive ? "true" : "false");
      if (isActive) {{
        vowBtn.textContent = "⚡ Voto Vinculante ACTIVO (x2 Extensión / Detalle)";
      }} else {{
        vowBtn.textContent = "⚡ Revelar la Técnica (Voto Vinculante)";
      }}
    }});

    // Cambio dinámico de personalidad
    personalitySelect.addEventListener("change", () => {{
      const chosen = personalitySelect.value;
      const info = PERSONALITY_INTROS[chosen] || PERSONALITY_INTROS["gojo"];
      const welcomeBubble = document.querySelector("#welcome-message");
      if (welcomeBubble) {{
        welcomeBubble.querySelector(".message-tag").textContent = info.tag;
        welcomeBubble.querySelector(".message-content").textContent = info.text;
      }}
    }});

    async function initProviders() {{
      try {{
        const res = await fetch("/api/providers");
        providersData = await res.json();
        
        providerSelect.innerHTML = "";

        // 1. Triple Contingencia Estricta (Automático)
        const optAuto = document.createElement("option");
        optAuto.value = "auto";
        optAuto.textContent = "🔄 Triple Contingencia (Auto: Azure ➔ Local ➔ Simulación)";
        providerSelect.appendChild(optAuto);

        // 2. Azure Foundry (Prioridad 1)
        if (providersData.azure && providersData.azure.available) {{
          const optAzure = document.createElement("option");
          optAzure.value = "azure";
          optAzure.textContent = "☁️ Prioridad 1: Microsoft Azure Foundry";
          providerSelect.appendChild(optAzure);
        }}

        // 3. Modelos Locales Edge AI (Prioridad 2)
        if (providersData.local && providersData.local.available) {{
          const optLocal = document.createElement("option");
          optLocal.value = "local";
          optLocal.textContent = "💻 Prioridad 2: Local Edge AI (.gguf)";
          providerSelect.appendChild(optLocal);
        }}

        // 4. Modo Simulación de Emergencia (Prioridad 3)
        const optSim = document.createElement("option");
        optSim.value = "simulation";
        optSim.textContent = "📜 Prioridad 3: Modo Simulación (Offline)";
        providerSelect.appendChild(optSim);

        if (providersData.default_provider && ["auto", "azure", "local", "simulation"].includes(providersData.default_provider)) {{
          providerSelect.value = providersData.default_provider;
        }} else {{
          providerSelect.value = "auto";
        }}
        updateModelDropdown();
      }} catch (err) {{
        badge.className = "badge none";
        badge.textContent = "Error al leer proveedores";
      }}
    }}

    function updateModelDropdown() {{
      modelSelect.innerHTML = "";
      const chosen = providerSelect.value;

      if (chosen === "auto") {{
        if (providersData && providersData.azure && providersData.azure.available) {{
          modelSelect.style.display = "inline-block";
          modelLabel.style.display = "inline-block";
          const opt = document.createElement("option");
          opt.value = providersData.azure.deployment;
          opt.textContent = providersData.azure.deployment;
          modelSelect.appendChild(opt);
          badge.className = "badge azure";
          badge.textContent = "Prioridad 1 (Activo): Azure Cloud (" + providersData.azure.deployment + ")";
        }} else if (providersData && providersData.local && providersData.local.available && providersData.local.models.length > 0) {{
          modelSelect.style.display = "inline-block";
          modelLabel.style.display = "inline-block";
          providersData.local.models.forEach(m => {{
            const opt = document.createElement("option");
            opt.value = m.path;
            opt.textContent = m.name;
            modelSelect.appendChild(opt);
          }});
          badge.className = "badge local";
          badge.textContent = "Prioridad 2 (Activo): Local Edge AI";
        }} else {{
          modelSelect.style.display = "none";
          modelLabel.style.display = "none";
          badge.className = "badge simulation";
          badge.textContent = "Prioridad 3 (Activo): Simulación de Emergencia";
        }}
      }} else if (chosen === "azure" && providersData && providersData.azure.available) {{
        modelSelect.style.display = "inline-block";
        modelLabel.style.display = "inline-block";
        const opt = document.createElement("option");
        opt.value = providersData.azure.deployment;
        opt.textContent = providersData.azure.deployment;
        modelSelect.appendChild(opt);
        badge.className = "badge azure";
        badge.textContent = "Prioridad 1: Azure Cloud (" + providersData.azure.deployment + ")";
      }} else if (chosen === "local" && providersData && providersData.local.available && providersData.local.models.length > 0) {{
        modelSelect.style.display = "inline-block";
        modelLabel.style.display = "inline-block";
        providersData.local.models.forEach(m => {{
          const opt = document.createElement("option");
          opt.value = m.path;
          opt.textContent = m.name;
          modelSelect.appendChild(opt);
        }});
        badge.className = "badge local";
        badge.textContent = "Prioridad 2: Local (" + (modelSelect.options[modelSelect.selectedIndex]?.text || "GGUF") + ")";
      }} else {{
        modelSelect.style.display = "none";
        modelLabel.style.display = "none";
        badge.className = "badge simulation";
        badge.textContent = "Prioridad 3: Modo Simulación (Jujutsu_encyclopedia.md)";
      }}
    }}

    providerSelect.addEventListener("change", updateModelDropdown);
    modelSelect.addEventListener("change", () => {{
      if (providerSelect.value === "local" || (providerSelect.value === "auto" && !providersData.azure?.available)) {{
        badge.textContent = "Prioridad 2: Local (" + modelSelect.options[modelSelect.selectedIndex]?.text + ")";
      }}
    }});

    const addMessage = (text, role, tag) => {{
      const bubble = document.createElement("div");
      bubble.className = `message ${{role}}`;
      if (tag) {{
        const tagElem = document.createElement("div");
        tagElem.className = "message-tag";
        tagElem.textContent = tag;
        bubble.appendChild(tagElem);
      }}
      const textElem = document.createElement("div");
      textElem.className = "message-content";
      textElem.textContent = text;
      bubble.appendChild(textElem);
      messages.appendChild(bubble);
      while (messages.children.length > 40) messages.removeChild(messages.firstElementChild);
      messages.scrollTop = messages.scrollHeight;
      return textElem;
    }};

    input.addEventListener("keydown", (event) => {{
      if (event.key === "Enter" && !event.shiftKey) {{
        event.preventDefault();
        form.requestSubmit();
      }}
    }});

    form.addEventListener("submit", async (event) => {{
      event.preventDefault();
      const message = input.value.trim();
      if (!message || button.disabled) return;
      
      const provider = providerSelect.value;
      const model = modelSelect.value;
      const personality = personalitySelect.value;
      const revealTechnique = vowBtn.classList.contains("active");

      addMessage(message, "user");
      input.value = "";
      button.disabled = true;
      const pendingBubble = addMessage("Invocando hechicería...", "assistant status");
      try {{
        const response = await fetch("/chat", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{
            message,
            provider,
            model,
            personality,
            reveal_technique: revealTechnique
          }})
        }});
        let data = {{}};
        try {{
          data = await response.json();
        }} catch {{
          data = {{}};
        }}
        if (!response.ok) throw new Error(data.detail || `Error en el servidor (${{response.status}}).`);
        pendingBubble.textContent = data.answer || "Sin respuesta del hechicero.";
        pendingBubble.parentElement.classList.remove("status");
        
        // Etiqueta del hechicero y motor según modo de contingencia
        if (data.personality_tag || data.model) {{
          const tagElem = document.createElement("div");
          tagElem.className = "message-tag";
          const pTag = data.personality_tag || "♾️ Asistente";
          let mTag = "";
          if (data.mode === "azure") {{
            mTag = `☁️ Prioridad 1: Azure Cloud (${{data.model}})`;
          }} else if (data.mode === "local") {{
            mTag = `💻 Prioridad 2: Local Edge AI (${{data.model}})`;
          }} else {{
            mTag = `📜 Prioridad 3: Simulación Canónica (${{data.model || "Jujutsu_encyclopedia.md"}})`;
          }}
          tagElem.textContent = `${{pTag}} · ${{mTag}}`;
          pendingBubble.parentElement.insertBefore(tagElem, pendingBubble);
        }}

        // Badge de Voto Vinculante si fue activado
        if (data.reveal_technique) {{
          const vowElem = document.createElement("div");
          vowElem.className = "message-vow-badge";
          vowElem.textContent = "⚡ Voto Vinculante Sellado: Técnica Revelada al 120%";
          pendingBubble.parentElement.insertBefore(vowElem, pendingBubble);
        }}

        // Fuentes canónicas RAG / Enciclopedia
        if (data.sources && data.sources.length > 0) {{
          const sourcesElem = document.createElement("div");
          sourcesElem.className = "message-sources";
          sourcesElem.textContent = "📖 Fuentes canónicas consultadas: " + data.sources.join(" · ");
          pendingBubble.parentElement.appendChild(sourcesElem);
        }}
      }} catch (error) {{
        pendingBubble.textContent = error.message || "Error de conexión.";
        pendingBubble.parentElement.classList.remove("status");
      }} finally {{
        button.disabled = false;
        input.focus();
      }}
    }});

    initProviders();
  </script>
</body>
</html>"""
    )


@app.post("/chat")
def chat(request: ChatRequest):
    """Ejecuta la inferencia bajo una estructura de Triple Contingencia (Triple Fallback) estricta:
    1. PRIORIDAD 1 (Azure Cloud): Si .env tiene credenciales válidas para Azure AI Foundry, realiza inferencia primaria con Microsoft.
    2. PRIORIDAD 2 (Edge AI / Modelos locales): Si Azure no está configurado o falla, busca archivos .gguf en /models y ejecuta localmente.
    3. PRIORIDAD 3 (Modo Simulación): Si no hay llaves de Azure Y /models está vacía (o local falla), lee directamente Jujutsu_encyclopedia.md y escupe la información canónica estructurada.
    """
    # Personalidad de Grado Especial y Voto Vinculante
    pkey = (request.personality or "gojo").lower().strip()
    if pkey not in PERSONALITY_PROMPTS:
        pkey = "gojo"
    p_info = PERSONALITY_PROMPTS[pkey]
    reveal = bool(request.reveal_technique)

    # Recuperación de conocimiento canónico (RAG)
    user_query = request.message.strip()
    retrieved_chunks = search_knowledge(user_query, top_k=3)
    sources = [f"{c['title']} ({c['source']})" for c in retrieved_chunks if c.get('source')]

    context_block = None
    if retrieved_chunks:
        context_block = "\n\n---\n\n".join([f"[{c['full_header']}]:\n{c['text']}" for c in retrieved_chunks])

    system_instructions = build_system_prompt(
        personality_key=pkey,
        reveal_technique=reveal,
        context_block=context_block
    )

    # Voto Vinculante 'Revelar la Técnica': respuestas el doble de extensas (1200 tokens vs 600)
    max_tokens_val = 1200 if reveal else 600

    provider_pref = (request.provider or "auto").lower().strip()

    # =========================================================================
    # PRIORIDAD 1 (Azure Cloud): Inferencia primaria en la nube de Microsoft
    # =========================================================================
    should_try_azure = (provider_pref in ("auto", "azure")) and is_azure_configured()

    if should_try_azure:
        endpoint = (os.environ.get("FOUNDRY_PROJECT_ENDPOINT") or "").strip()
        deployment = (
            request.model if (provider_pref == "azure" and request.model)
            else (os.environ.get("MODEL_DEPLOYMENT_NAME") or os.environ.get("FOUNDRY_MODEL_NAME") or "")
        ).strip()

        logger.info("[PRIORIDAD 1: AZURE CLOUD] Intentando inferencia primaria con Azure Foundry (%s)...", deployment)
        try:
            answer = execute_azure_chat(
                endpoint,
                deployment,
                system_instructions,
                user_query,
                max_tokens_val
            )
            return {
                "answer": answer,
                "mode": "azure",
                "model": deployment,
                "contingency_level": "Prioridad 1 (Azure Cloud)",
                "personality": pkey,
                "personality_tag": p_info["tag"],
                "reveal_technique": reveal,
                "sources": sources
            }
        except Exception as err:
            logger.warning("[FALLBACK P1 -> P2] Error en Azure Cloud (%s): %s. Pasando a Prioridad 2 (Edge AI Local)...", type(err).__name__, err)
    elif provider_pref == "azure" and not is_azure_configured():
        logger.warning("[PRIORIDAD 1] Azure solicitado explícitamente pero no configurado en .env. Pasando a Prioridad 2...")
    else:
        logger.info("[PRIORIDAD 1] Credenciales de Azure no configuradas o modo local/simulación solicitado. Evaluando Prioridad 2...")

    # =========================================================================
    # PRIORIDAD 2 (Edge AI / Modelos locales): Inferencia con archivos .gguf en /models
    # =========================================================================
    should_try_local = provider_pref in ("auto", "local", "azure")
    local_models = find_local_models()

    if should_try_local and local_models:
        chosen_path = (
            request.model if (provider_pref == "local" and request.model and os.path.isfile(request.model))
            else local_models[0]["path"]
        )
        model_name = Path(chosen_path).name

        logger.info("[PRIORIDAD 2: EDGE AI LOCAL] Intentando inferencia local con %s...", model_name)
        try:
            answer = execute_local_chat(
                chosen_path,
                system_instructions,
                user_query,
                max_tokens_val,
                p_info["name"]
            )
            return {
                "answer": answer,
                "mode": "local",
                "model": model_name,
                "contingency_level": "Prioridad 2 (Edge AI Local)",
                "personality": pkey,
                "personality_tag": p_info["tag"],
                "reveal_technique": reveal,
                "sources": sources
            }
        except Exception as err:
            logger.warning("[FALLBACK P2 -> P3] Error en inferencia local con %s (%s): %s. Pasando a Prioridad 3 (Modo Simulación)...", model_name, type(err).__name__, err)
    else:
        logger.info("[PRIORIDAD 2] Sin modelos .gguf en carpeta /models o inferencia local fallida. Pasando a Prioridad 3...")

    # =========================================================================
    # PRIORIDAD 3 (Modo Simulación): Extracción directa desde Jujutsu_encyclopedia.md
    # =========================================================================
    logger.info("[PRIORIDAD 3: MODO SIMULACIÓN] Extrayendo información canónica estructurada desde Jujutsu_encyclopedia.md...")
    sim_data = get_emergency_simulation_response(
        pkey,
        user_query,
        reveal
    )

    return {
        "answer": sim_data["answer"],
        "mode": "simulation",
        "model": "Jujutsu_encyclopedia.md",
        "contingency_level": "Prioridad 3 (Modo Simulación de Emergencia)",
        "personality": pkey,
        "personality_tag": p_info["tag"],
        "reveal_technique": reveal,
        "sources": sim_data.get("sources", sources)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
