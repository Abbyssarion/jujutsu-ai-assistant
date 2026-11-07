"""Genera las figuras del tema 4 (generación de video con Sora). Solo matplotlib.
Precios de referencia: lista pública de OpenAI por segundo generado (sora-2 720p $0.10/s,
sora-2-pro 720p $0.30/s). Azure también cobra por segundo; revisa su página de precios."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path(__file__).resolve().parent

AZUL, MORADO, NARANJA, GRIS, VERDE = "#0F6CBD", "#5C2D91", "#F97316", "#8A8886", "#2EA44F"

# ---------- Figura A: costo por clip y costo de iterar ----------
dur = [4, 8, 12]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.2), dpi=160)
x = range(len(dur)); w = 0.38
b1 = a1.bar([i - w/2 for i in x], [d*0.10 for d in dur], w, color=AZUL, label="sora-2 · 720p · $0.10/s")
b2 = a1.bar([i + w/2 for i in x], [d*0.30 for d in dur], w, color=MORADO, label="sora-2-pro · 720p · $0.30/s")
for bars in (b1, b2):
    for b in bars:
        a1.text(b.get_x()+b.get_width()/2, b.get_height()+0.05, f"${b.get_height():.2f}", ha="center", fontsize=9)
a1.set_xticks(list(x)); a1.set_xticklabels([f"{d} s" for d in dur])
a1.set_ylabel("USD por clip (referencia)"); a1.set_title("Se cobra por segundo generado:\nel doble de duración = el doble de costo")
a1.legend(fontsize=9); a1.grid(axis="y", alpha=.3); a1.set_ylim(0, 4.2)

# Iterar directo en 12 s vs iterar en 4 s y solo el final en 12 s (6 intentos en total)
directo = [12*0.10]*6
inteligente = [4*0.10]*5 + [12*0.10]
a2.plot(range(1, 7), [sum(directo[:i]) for i in range(1, 7)], "o-", color=NARANJA, lw=2.4, label="6 intentos de 12 s")
a2.plot(range(1, 7), [sum(inteligente[:i]) for i in range(1, 7)], "s-", color=VERDE, lw=2.4, label="5 bocetos de 4 s + 1 final de 12 s")
a2.annotate(f"${sum(directo):.2f}", (6, sum(directo)), xytext=(5.55, sum(directo)+0.45), fontsize=10, color=NARANJA)
a2.annotate(f"${sum(inteligente):.2f}", (6, sum(inteligente)), xytext=(5.55, sum(inteligente)-0.75), fontsize=10, color=VERDE)
a2.set_xlabel("intento #"); a2.set_ylabel("USD acumulados (sora-2, 720p)")
a2.set_title("Costo de llegar al clip bueno:\nboceta corto, renderiza largo al final")
a2.legend(fontsize=9, loc="upper left"); a2.grid(alpha=.3); a2.set_ylim(0, 8.5)
plt.tight_layout(); plt.savefig(OUT / "video-costo-iteracion.png", facecolor="white"); plt.close()

# ---------- Figura B: tamaños soportados y regla de input_reference ----------
fig, (b1, b2) = plt.subplots(1, 2, figsize=(13, 5.6), dpi=160, gridspec_kw={"width_ratios": [1.15, 1]})
jobs = [(480,480),(854,480),(480,854),(720,720),(1080,1080),(1920,1080),(1080,1920)]
for wpx, hpx in jobs:
    b1.add_patch(Rectangle((0, 0), wpx, hpx, fill=False, ec=GRIS, ls=":", lw=1))
b1.add_patch(Rectangle((0, 0), 1280, 720, fc=AZUL, alpha=.25, ec=AZUL, lw=2.5))
b1.add_patch(Rectangle((0, 0), 720, 1280, fc=MORADO, alpha=.20, ec=MORADO, lw=2.5))
b1.text(1290, 690, "1280×720\nhorizontal (16:9)", color=AZUL, fontsize=10, va="top", weight="bold")
b1.text(20, 1300, "720×1280 vertical (9:16)\n← tamaño por defecto", color=MORADO, fontsize=10, weight="bold")
b1.text(1930, 1060, "punteado: tamaños de la\nAPI de jobs (preview):\n480p, 720p, 1080p\ncuadrado/vertical/horizontal", color="#555", fontsize=8.5, va="top")
b1.set_xlim(0, 2900); b1.set_ylim(0, 2000); b1.set_aspect("equal")
b1.set_xlabel("ancho (px)"); b1.set_ylabel("alto (px)")
b1.set_title("API v1 /videos (la de Learn): solo 2 tamaños", fontsize=11)

b2.axis("off"); b2.set_xlim(0, 10); b2.set_ylim(0, 10)
b2.add_patch(Rectangle((0.3, 4.2), 3.6, 3.6, fc="#DDE7F3", ec=GRIS, lw=1.5))
b2.text(2.1, 6.0, "foto\n1024×1024", ha="center", va="center", fontsize=10)
b2.add_patch(Rectangle((0.3, 5.0), 3.6, 2.0, fill=False, ec=NARANJA, lw=2, ls="--"))
b2.annotate("", xy=(5.4, 6.0), xytext=(4.2, 6.0), arrowprops=dict(arrowstyle="->", lw=2))
b2.text(4.8, 6.5, "ImageOps.fit", ha="center", fontsize=9)
b2.add_patch(Rectangle((5.6, 5.0), 4.2, 2.36, fc="#DDE7F3", ec=AZUL, lw=2.5))
b2.text(7.7, 6.18, "1280×720\n= size del video", ha="center", va="center", fontsize=10, color=AZUL, weight="bold")
b2.text(5, 3.3, "input_reference = primer cuadro del video.\nDebe medir EXACTAMENTE lo mismo que size\n(si no: error 400). Recorta al centro, no estires.", ha="center", fontsize=10)
b2.text(5, 1.4, "✗ Imágenes con rostros humanos: rechazadas\n✓ Paisajes, objetos, productos, personajes animados", ha="center", fontsize=9.5, color="#444")
b2.set_title("Imagen de referencia: ajústala antes de enviarla", fontsize=11)
plt.tight_layout(); plt.savefig(OUT / "video-tamanos-referencia.png", facecolor="white"); plt.close()
print("ok")
