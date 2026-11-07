"""Figura del tema 5 del módulo 7: qué bloquea cada nivel de bloqueo de los guardrails
(nomenclatura nueva) y su equivalente en la nomenclatura clásica de filtros de contenido."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

OUT = Path(__file__).resolve().parent

niveles = ["Off", "Low", "Medium\n(DefaultV2)", "High"]
clasico = ["No filters /\nAnnotate only", "High", "Medium, high", "Low, medium,\nhigh"]
restr = ["nada", "menos restrictivo", "equilibrado", "más restrictivo"]
sev = ["Safe", "Low", "Medium", "High"]
# 1 = bloqueado, 0 = pasa (con anotación)
M = np.array([
    [0, 0, 0, 0],   # Safe
    [0, 0, 0, 1],   # Low
    [0, 0, 1, 1],   # Medium
    [0, 1, 1, 1],   # High
])
fig, ax = plt.subplots(figsize=(11.5, 6.6), dpi=160)
ax.imshow(M, cmap=ListedColormap(["#DFF3E4", "#F8D7DA"]), vmin=0, vmax=1, aspect="auto")
for i in range(4):
    for j in range(4):
        ax.text(j, i, "BLOQUEA" if M[i, j] else "pasa\n(se anota)", ha="center", va="center",
                fontsize=10, weight="bold" if M[i, j] else "normal", color="#842029" if M[i, j] else "#1E5631")
ax.set_xticks(range(4)); ax.set_xticklabels([f"{n}\n{r}" for n, r in zip(niveles, restr)], fontsize=10)
ax.set_yticks(range(4)); ax.set_yticklabels([f"severidad {s}" for s in sev], fontsize=10)
ax.xaxis.tick_top()
for j, c in enumerate(clasico):
    ax.text(j, 3.78, f"clásico: «{c}»", ha="center", va="top", fontsize=8.5, color="#605E5C")
ax.set_ylim(4.35, -0.5)
ax.set_xticks(np.arange(-.5, 4), minor=True); ax.set_yticks(np.arange(-.5, 4), minor=True)
ax.grid(which="minor", color="white", lw=3); ax.tick_params(which="minor", length=0)
ax.set_title("Nivel de bloqueo de un guardrail (odio, sexual, violencia, autolesiones)\n"
             "El nivel dice QUÉ TAN ESTRICTO eres, no desde qué severidad empiezas", fontsize=12, pad=58)
plt.tight_layout(); plt.savefig(OUT / "guardrails-niveles-bloqueo.png", facecolor="white"); plt.close()
print("ok")
