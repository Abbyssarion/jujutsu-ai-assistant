"""Genera las gráficas del Tema 1 (Parte 2, Módulo 3). Ejecutar: python _generar_graficas.py
Los precios son de lista (oct-2026, región global estándar, USD) y sirven como orden de magnitud.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent
AZUL, NARANJA, AQUA, AMARILLO, GRIS = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#8a8a85"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#b8b8b3", "axes.labelcolor": "#444", "xtick.color": "#444",
                     "ytick.color": "#444", "figure.dpi": 160})

# ---------- 1) Costo por 1 millón de textos (500 caracteres, 3 análisis) ----------
N = 1_000_000
chars = 500
tokens_texto = chars / 3.6          # ~3.6 caracteres por token en español
tokens_prompt = 120                 # instrucciones del sistema
tokens_salida = 100                 # JSON con idioma, PII y sentimiento
def costo_llm(p_in, p_out):
    return N * ((tokens_texto + tokens_prompt) * p_in + tokens_salida * p_out) / 1e6
# Azure Language: 1 registro = 1,000 caracteres (se redondea hacia arriba). 3 funciones = 3 registros por texto.
registros = N * 3
def costo_language_escalonado(r):
    # Niveles S: 0-0.5M $1.00 | 0.5-2.5M $0.75 | 2.5-10M $0.30 | 10M+ $0.25 (por 1,000 registros)
    niveles = [(500_000, 1.00), (2_000_000, 0.75), (7_500_000, 0.30), (float("inf"), 0.25)]
    total, rest = 0.0, r
    for tam, precio in niveles:
        usa = min(rest, tam); total += usa / 1000 * precio; rest -= usa
        if rest <= 0: break
    return total
opciones = [
    ("Azure Language (3 funciones,\nnivel 0–0.5M: \\$1 / 1K registros)", registros / 1000 * 1.00, AQUA),
    ("Azure Language (3 funciones,\ncon niveles de volumen)", costo_language_escalonado(registros), AQUA),
    ("LLM frontier\n(\\$2.50 in / \\$10 out por 1M tokens)", costo_llm(2.50, 10.0), NARANJA),
    ("LLM grande (gpt-4.1)\n(\\$2 in / \\$8 out por 1M tokens)", costo_llm(2.0, 8.0), NARANJA),
    ("LLM mini (gpt-4.1-mini)\n(\\$0.40 in / \\$1.60 out por 1M tokens)", costo_llm(0.40, 1.60), NARANJA),
]
fig, ax = plt.subplots(figsize=(9, 4.6))
y = np.arange(len(opciones))
vals = [o[1] for o in opciones]
ax.barh(y, vals, color=[o[2] for o in opciones], height=0.55)
for i, v in enumerate(vals):
    ax.text(v + max(vals) * 0.01, i, f"\\${v:,.0f}", va="center", color="#333")
ax.set_yticks(y); ax.set_yticklabels([o[0] for o in opciones])
ax.set_xlabel("USD por 1,000,000 de textos (500 caracteres c/u; detectar idioma + PII + sentimiento)")
ax.set_title("Costo de lista: Azure Language vs. LLM — el servicio especializado NO siempre es más barato", loc="left", fontsize=11)
ax.grid(axis="x", color="#e6e6e2"); ax.set_axisbelow(True)
ax.invert_yaxis()
fig.text(0.01, -0.02, "Supuestos: ~140 tokens por texto + 120 de instrucciones y 100 de salida; 1 registro de Language = 1,000 caracteres y cada función se cobra aparte. Precios de lista oct-2026, aproximados.",
         fontsize=7.5, color="#666")
fig.tight_layout(); fig.savefig(OUT / "costo-1m-textos.png", bbox_inches="tight"); plt.close(fig)

# ---------- 2) Latencia ilustrativa por llamada ----------
rng = np.random.default_rng(7)
lat = {
    "Azure Language\n(detect_language / PII)": rng.lognormal(np.log(0.18), 0.25, 300),
    "LLM mini\n(JSON corto)": rng.lognormal(np.log(1.3), 0.35, 300),
    "LLM grande / razonamiento": rng.lognormal(np.log(3.5), 0.4, 300),
}
fig, ax = plt.subplots(figsize=(9, 3.8))
colores = [AQUA, NARANJA, NARANJA]
for i, (k, v) in enumerate(lat.items()):
    x = rng.normal(i, 0.06, len(v))
    ax.scatter(x, v, s=9, color=colores[i], alpha=0.35, linewidths=0)
    p50, p95 = np.percentile(v, [50, 95])
    ax.hlines(p50, i - 0.25, i + 0.25, color="#222", lw=2)
    ax.text(i + 0.28, p50, f"p50 ≈ {p50:.2f} s", va="center", fontsize=9, color="#222")
    ax.text(i + 0.28, p95, f"p95 ≈ {p95:.1f} s", va="center", fontsize=8, color="#666")
ax.set_xticks(range(len(lat))); ax.set_xticklabels(lat.keys())
ax.set_yscale("log"); ax.set_ylabel("segundos por llamada (escala log)")
ax.set_yticks([0.1, 0.3, 1, 3, 10]); ax.set_yticklabels(["0.1", "0.3", "1", "3", "10"])
ax.set_title("Latencia típica por llamada (ilustrativa): un servicio especializado responde ~10× más rápido", loc="left", fontsize=11)
ax.grid(axis="y", color="#e6e6e2"); ax.set_axisbelow(True)
fig.text(0.01, -0.03, "Valores simulados a partir de rangos típicos; mide los tuyos con el script de la práctica (variable `t`).", fontsize=7.5, color="#666")
fig.tight_layout(); fig.savefig(OUT / "latencia-ilustrativa.png", bbox_inches="tight"); plt.close(fig)

# ---------- 3) Unidades de cobro: registros vs tokens ----------
fig, ax = plt.subplots(figsize=(9, 2.6))
texto_chars = 2_300
ax.barh(1, texto_chars, color="#e6e6e2", height=0.5)
for i in range(3):
    ax.add_patch(plt.Rectangle((i * 1000, 0.75), 1000 - 8, 0.5, fill=False, edgecolor=AQUA, lw=2))
    ax.text(i * 1000 + 500, 1.42, f"registro {i+1}", ha="center", color=AQUA, fontsize=9)
ax.text(3000 + 30, 1, "← Azure Language cobra 3 registros\n   (2,300 caracteres → se redondea a 3 × 1,000)", va="center", fontsize=9, color="#333")
tok = int(texto_chars / 3.6)
for i in range(0, texto_chars, int(3.6 * 10)):
    ax.vlines(i, 0.25, 0.65, color=NARANJA, lw=0.6, alpha=0.8)
ax.text(3000 + 30, 0.45, f"← Un LLM cobra ≈ {tok} tokens de entrada (+ prompt + salida)", va="center", fontsize=9, color="#333")
ax.text(0, 0.1, "0", fontsize=8, color="#666"); ax.text(texto_chars, 0.1, f"{texto_chars:,} caracteres", fontsize=8, color="#666", ha="center")
ax.set_xlim(0, 5600); ax.set_ylim(0, 1.7); ax.axis("off")
ax.set_title("Dos formas de cobrar el mismo texto", loc="left", fontsize=11)
fig.tight_layout(); fig.savefig(OUT / "registros-vs-tokens.png", bbox_inches="tight"); plt.close(fig)
print("OK:", [p.name for p in OUT.glob('*.png')])
