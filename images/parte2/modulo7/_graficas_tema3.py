"""Figura del tema 3 del módulo 7: cómo trocea File Search (800 tokens, traslape de 400)
y cuánto contexto puede inyectar. Solo matplotlib. Supuesto: ~500 tokens por página."""
import math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path(__file__).resolve().parent

AZUL, MORADO, NARANJA, GRIS = "#0F6CBD", "#5C2D91", "#F97316", "#8A8886"
CH, OV = 800, 400
paso = CH - OV

fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 5.4), dpi=160, gridspec_kw={"width_ratios": [1.25, 1]})
# Panel 1: ventanas deslizantes sobre un documento de 3,200 tokens
doc = 3200
a1.add_patch(Rectangle((0, 0), doc, 0.6, fc="#EDEBE9", ec=GRIS))
a1.text(doc/2, 0.3, "documento: 3,200 tokens (~6 páginas)", ha="center", va="center", fontsize=10)
cols = [AZUL, MORADO, NARANJA]
i, ini = 0, 0
while ini < doc - OV:
    fin = min(ini + CH, doc)
    y = 1.0 + (i % 3) * 0.75
    a1.add_patch(Rectangle((ini, y), fin - ini, 0.55, fc=cols[i % 3], alpha=.35, ec=cols[i % 3], lw=1.8))
    a1.text((ini + fin)/2, y + 0.27, f"chunk {i+1}\n{ini}–{fin}", ha="center", va="center", fontsize=8)
    ini += paso; i += 1
a1.annotate("", xy=(800, 3.45), xytext=(400, 3.45), arrowprops=dict(arrowstyle="<->", color="black"))
a1.text(600, 3.6, "traslape 400", ha="center", fontsize=9)
a1.annotate("", xy=(800, 3.95), xytext=(0, 3.95), arrowprops=dict(arrowstyle="<->", color="black"))
a1.text(400, 4.1, "chunk 800", ha="center", fontsize=9)
a1.set_xlim(-50, doc + 50); a1.set_ylim(-0.2, 4.5); a1.set_yticks([])
a1.set_xlabel("posición en el documento (tokens)")
a1.set_title(f"File Search trocea con ventanas de {CH} tokens que avanzan {paso}:\ncada idea queda en ~2 chunks (no se corta a la mitad)", fontsize=11)

# Panel 2: chunks generados según páginas y contexto máximo por respuesta
paginas = list(range(1, 401))
chunks = [max(1, math.ceil((p*500 - OV) / paso)) for p in paginas]
a2.plot(paginas, chunks, color=AZUL, lw=2.4, label="chunks generados (≈ 500 tokens/página)")
a2.set_xlabel("páginas del documento"); a2.set_ylabel("número de chunks", color=AZUL)
a2.grid(alpha=.3)
for p in (10, 100, 400):
    c = max(1, math.ceil((p*500 - OV) / paso))
    a2.plot(p, c, "o", color=AZUL); a2.annotate(f"{p} págs → {c} chunks", (p, c), xytext={10: (30, 75), 100: (115, 95), 400: (255, 470)}[p], fontsize=8.5, arrowprops=dict(arrowstyle="->", color=GRIS))
a2.axhline(20, color=NARANJA, ls="--", lw=2)
a2.text(150, 32, "máx. 20 chunks llegan al modelo por búsqueda\n= hasta ~16,000 tokens de contexto que pagas", color=NARANJA, fontsize=9)
a2.set_title("Un documento grande genera cientos de chunks;\nsolo los 20 mejores llegan a la respuesta", fontsize=11)
a2.set_ylim(0, 520)
plt.tight_layout(); plt.savefig(OUT / "filesearch-chunking.png", facecolor="white"); plt.close()
print("ok")
