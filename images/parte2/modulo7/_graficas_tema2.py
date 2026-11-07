"""Figuras del tema 2 del módulo 7 (prompt vs RAG vs fine-tuning). Solo numpy + matplotlib.
Los números de costo son ILUSTRATIVOS (supuestos indicados en el tema); verifica precios vigentes."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent

AZUL, MORADO, NARANJA, VERDE, GRIS = "#0F6CBD", "#5C2D91", "#F97316", "#2EA44F", "#8A8886"

# ---------- Figura A: los dos ejes ----------
fig, ax = plt.subplots(figsize=(10, 8), dpi=160)
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.axhline(5, color=GRIS, lw=1); ax.axvline(5, color=GRIS, lw=1)
ax.set_xlabel("¿Qué tanto debe CAMBIAR SU COMPORTAMIENTO el modelo?\n(formato, tono, habilidad, uso de herramientas)  →", fontsize=11)
ax.set_ylabel("¿Qué tanto CONOCIMIENTO le falta al modelo?\n(datos privados, recientes, específicos)  →", fontsize=11)
ax.set_xticks([]); ax.set_yticks([])
box = dict(boxstyle="round,pad=0.6", lw=2)
ax.text(2.5, 2.5, "① PROMPT ENGINEERING\nsystem prompt + few-shot\n+ salidas estructuradas\n\nsiempre se empieza aquí", ha="center", va="center", fontsize=11, bbox={**box, "fc": "#E8F1FB", "ec": AZUL})
ax.text(2.5, 7.5, "② + RAG\nFoundry IQ / File Search /\nAzure AI Search\n\n\"le falta saber\"", ha="center", va="center", fontsize=11, bbox={**box, "fc": "#EFE8F7", "ec": MORADO})
ax.text(7.5, 2.5, "③ + FINE-TUNING\nSFT / DPO / RFT\n\n\"le falta saber HACER\"\n(de forma consistente y barata)", ha="center", va="center", fontsize=11, bbox={**box, "fc": "#FFF1E6", "ec": NARANJA})
ax.text(7.5, 7.5, "④ RAG + FINE-TUNING\nmodelo ajustado para usar\nbien el contexto recuperado\n\nlo más potente… y lo más caro", ha="center", va="center", fontsize=11, bbox={**box, "fc": "#E9F6EC", "ec": VERDE})
ax.annotate("", xy=(2.5, 5.9), xytext=(2.5, 4.1), arrowprops=dict(arrowstyle="->", lw=2.5, color=MORADO))
ax.annotate("", xy=(5.9, 2.5), xytext=(4.1, 2.5), arrowprops=dict(arrowstyle="->", lw=2.5, color=NARANJA))
ax.annotate("", xy=(6.0, 6.0), xytext=(4.0, 4.0), arrowprops=dict(arrowstyle="->", lw=2.5, color=VERDE, ls="--"))
ax.set_title("Dos preguntas distintas → palancas distintas", fontsize=14, weight="bold")
plt.tight_layout(); plt.savefig(OUT / "palancas-dos-ejes.png", facecolor="white"); plt.close()

# ---------- Figura B: punto de equilibrio de costo ----------
llamadas = np.linspace(0, 2_000_000, 400)          # llamadas por mes
def costo(ent_tok, sal_tok, p_ent, p_sal, fijo=0):
    return fijo + llamadas * (ent_tok * p_ent + sal_tok * p_sal) / 1e6
A = costo(4000, 200, 2.00, 8.00)                    # gpt-4.1 base, prompt largo con few-shot
B = costo(4000, 200, 0.40, 1.60)                    # gpt-4.1-mini base, mismo prompt largo
C = costo(500, 200, 0.80, 3.20, fijo=1.70 * 730)    # gpt-4.1-mini ajustado, prompt corto + hospedaje 24/7
fig, ax = plt.subplots(figsize=(11, 5.8), dpi=160)
ax.plot(llamadas/1000, A, color=MORADO, lw=2.4, label="A · gpt-4.1 base, prompt de 4,000 tokens (few-shot)")
ax.plot(llamadas/1000, B, color=AZUL, lw=2.4, label="B · gpt-4.1-mini base, prompt de 4,000 tokens")
ax.plot(llamadas/1000, C, color=NARANJA, lw=2.4, label="C · gpt-4.1-mini AJUSTADO, prompt de 500 tokens + hospedaje 24/7")
for otro, nombre, col in ((A, "A", MORADO), (B, "B", AZUL)):
    i = np.argmax(C < otro)
    if C[i] < otro[i] and i > 0:
        ax.plot(llamadas[i]/1000, C[i], "o", color=col, ms=9)
        ax.annotate(f"C empieza a ser más barato que {nombre}\n≈ {llamadas[i]/1000:,.0f} mil llamadas/mes",
                    (llamadas[i]/1000, C[i]), xytext=(llamadas[i]/1000 + (185 if nombre == 'A' else 120), C[i] + (870 if nombre == 'A' else -900)),
                    arrowprops=dict(arrowstyle="->", color=col), fontsize=9, color=col)
ax.set_xlabel("miles de llamadas por mes (200 tokens de salida cada una)")
ax.set_ylabel("USD por mes")
ax.set_title("¿Cuándo se paga solo el fine-tuning?  (supuestos ilustrativos)", fontsize=12)
ax.grid(alpha=.3); ax.legend(fontsize=9, loc="upper left"); ax.set_ylim(0, 6000); ax.set_xlim(0, 2000)
plt.tight_layout(); plt.savefig(OUT / "costo-equilibrio-finetuning.png", facecolor="white"); plt.close()

# ---------- Figura C: curvas de pérdida, sano vs sobreajuste ----------
rng = np.random.default_rng(7)
pasos = np.arange(0, 300)
tr_ok = 1.6*np.exp(-pasos/70) + .35 + rng.normal(0, .03, pasos.size)
va_ok = 1.6*np.exp(-pasos/80) + .42 + rng.normal(0, .01, pasos.size)
tr_bad = 1.6*np.exp(-pasos/45) + .05 + rng.normal(0, .025, pasos.size)
va_bad = 1.6*np.exp(-pasos/60) + .45 + np.clip(pasos-110, 0, None)*.0035 + rng.normal(0, .01, pasos.size)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4.8), dpi=160, sharey=True)
a1.plot(pasos, tr_ok, color=AZUL, lw=1.6, label="train_loss"); a1.plot(pasos, va_ok, color=NARANJA, lw=2.4, label="full_valid_loss")
a1.set_title("Sano: ambas bajan y se estabilizan juntas"); a1.legend(); a1.grid(alpha=.3); a1.set_xlabel("pasos de entrenamiento"); a1.set_ylabel("pérdida (loss)")
a2.plot(pasos, tr_bad, color=AZUL, lw=1.6, label="train_loss"); a2.plot(pasos, va_bad, color=NARANJA, lw=2.4, label="full_valid_loss")
m = int(np.argmin(va_bad)); a2.axvline(m, color=VERDE, ls="--"); a2.text(m+4, 1.5, f"mejor checkpoint\n(paso ~{m})", color=VERDE, fontsize=9)
a2.set_title("Sobreajuste: train sigue bajando, validación sube"); a2.legend(); a2.grid(alpha=.3); a2.set_xlabel("pasos de entrenamiento")
fig.suptitle("Cómo leer las métricas de un job de fine-tuning (curvas ilustrativas)", fontsize=12)
plt.tight_layout(); plt.savefig(OUT / "curvas-loss-finetuning.png", facecolor="white"); plt.close()
print("ok")
