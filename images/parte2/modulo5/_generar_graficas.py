"""Genera las figuras del tema 1 (modelos multimodales). Solo numpy/matplotlib/Pillow."""
import math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent

# ---------- 1) Fórmulas de tokens ----------
def tokens_tiles(w, h, base=85, tile=170, detail="high"):
    """Modelos por mosaicos (gpt-4o, gpt-4.1): base + 170 por cada mosaico de 512 px."""
    if detail == "low":
        return base
    s = min(1.0, 2048 / max(w, h)); w, h = w * s, h * s        # 1) cabe en 2048x2048
    s = min(1.0, 768 / min(w, h));  w, h = w * s, h * s        # 2) lado corto a 768
    n = math.ceil(w / 512) * math.ceil(h / 512)                # 3) mosaicos de 512
    return base + n * tile

def tokens_patches(w, h, mult=1.62, max_dim=2048, budget=1536):
    """Modelos por parches (gpt-4.1-mini/nano, gpt-5-mini): parches de 32 px × multiplicador."""
    s = min(1.0, max_dim / max(w, h)); w, h = int(w * s), int(h * s)
    n = math.ceil(w / 32) * math.ceil(h / 32)
    if n > budget:                                              # presupuesto de parches
        s = math.sqrt(budget / n); w, h = int(w * s), int(h * s)
        n = math.ceil(w / 32) * math.ceil(h / 32)
    return math.ceil(n * mult)

# ---------- Figura A: tokens vs resolución ----------
lados = [256, 512, 768, 1024, 1536, 2048, 3000, 4000]
fig, ax = plt.subplots(figsize=(11, 5.5), dpi=160)
ax.plot(lados, [tokens_tiles(l, l) for l in lados], "o-", lw=2.2, label="gpt-4.1 / gpt-4o  (detail=high)  85 + 170·mosaicos")
ax.plot(lados, [tokens_tiles(l, l, detail='low') for l in lados], "s--", lw=2, label="gpt-4.1 / gpt-4o  (detail=low)  85 fijos")
ax.plot(lados, [tokens_patches(l, l, 1.62) for l in lados], "^-", lw=2.2, label="gpt-4.1-mini  parches de 32 px × 1.62")
ax.plot(lados, [tokens_patches(l, l, 2.46) for l in lados], "v-", lw=2.2, label="gpt-4.1-nano  parches de 32 px × 2.46")
ax.plot(lados, [tokens_patches(l, l, 1.2) for l in lados], "d-", lw=2.2, label="gpt-5-mini  parches de 32 px × 1.2")
ax.set_xlabel("lado de una imagen cuadrada (px)"); ax.set_ylabel("tokens de entrada que cuesta la imagen")
ax.set_title("¿Cuántos tokens cuesta una imagen? Depende del modelo, la resolución y el nivel de detalle")
ax.grid(alpha=.3); ax.legend(fontsize=9)
for l in (768, 1536):
    ax.axvline(l, color="gray", ls=":", lw=1)
ax.annotate("tope: el lado corto se\nreduce a 768 px → 4 mosaicos", xy=(1024, tokens_tiles(1024,1024)), xytext=(2100, 1150),
            arrowprops=dict(arrowstyle="->", color="gray"), fontsize=8.5, color="#444")
plt.tight_layout(); plt.savefig(OUT / "tokens-por-resolucion.png", facecolor="white"); plt.close()

# ---------- Figura B: mosaicos vs parches sobre un "documento" sintético ----------
W, H = 1024, 768
doc = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(doc)
try:
    f_t = ImageFont.truetype("DejaVuSans-Bold.ttf", 40); f_b = ImageFont.truetype("DejaVuSans.ttf", 22); f_s = ImageFont.truetype("DejaVuSans.ttf", 12)
except Exception:
    f_t = f_b = f_s = ImageFont.load_default()
d.rectangle([0, 0, W, 90], fill="#0F6CBD"); d.text((30, 22), "FACTURA  A-2026-0417", fill="white", font=f_t)
d.text((30, 120), "Cliente: Taquería El Brujo S.A. de C.V.", fill="black", font=f_b)
d.text((30, 155), "RFC: TEB260101XYZ      Fecha: 26/10/2026", fill="black", font=f_b)
y = 230
for c, cant, pu in [("Barra de sonido HT-S20RC", 2, 4599.00), ("Cable HDMI 2.1 (2 m)", 4, 349.00), ("Instalación", 1, 1200.00)]:
    d.text((30, y), f"{c:<30}", fill="black", font=f_b); d.text((520, y), f"{cant:>3}", fill="black", font=f_b)
    d.text((640, y), f"${pu:>9,.2f}", fill="black", font=f_b); d.text((820, y), f"${cant*pu:>10,.2f}", fill="black", font=f_b); y += 40
d.line([30, y+5, W-30, y+5], fill="black", width=2)
d.text((640, y+20), "TOTAL:", fill="black", font=f_b); d.text((820, y+20), "$11,794.00", fill="black", font=f_b)
d.text((30, H-60), "Nota en letra pequeña: el IVA ya está incluido. Pago a 30 días. Folio fiscal 7F3A-19C2-88B1.", fill="#444", font=f_s)
doc.save(OUT / "doc-ejemplo.png")

fig, axes = plt.subplots(1, 3, figsize=(15, 5.2), dpi=150)
# low: 512x512
low = doc.resize((512, 384), Image.LANCZOS)
axes[0].imshow(low); axes[0].set_title("detail=low → 1 vista de 512 px\n85 tokens (gpt-4.1): la letra pequeña se pierde", fontsize=10)
# high: 768 short side → 1024x768 ; tiles
hi = doc  # ya cabe: lado corto 768
axes[1].imshow(hi)
for x in range(0, W, 512):
    for yy in range(0, H, 512):
        axes[1].add_patch(Rectangle((x, yy), 512, 512, fill=False, ec="#E4002B", lw=2))
axes[1].set_title(f"detail=high → mosaicos de 512 px\n{tokens_tiles(W,H)} tokens (gpt-4.1): 85 + 170 × {math.ceil(W/512)*math.ceil(H/512)}", fontsize=10)
# patches
axes[2].imshow(hi)
for x in range(0, W, 32): axes[2].axvline(x, color="#2EA44F", lw=.4, alpha=.8)
for yy in range(0, H, 32): axes[2].axhline(yy, color="#2EA44F", lw=.4, alpha=.8)
n = math.ceil(W/32)*math.ceil(H/32)
axes[2].set_title(f"gpt-4.1-mini → parches de 32 px\n{n} parches × 1.62 = {math.ceil(n*1.62)} tokens", fontsize=10)
for a in axes: a.axis("off")
plt.suptitle("La misma factura de 1024×768 px: cómo la 've' el modelo según el nivel de detalle y la familia", fontsize=12)
plt.tight_layout(); plt.savefig(OUT / "detalle-low-high-parches.png", facecolor="white"); plt.close()

# ---------- Figura C: costo relativo al redimensionar antes de enviar ----------
casos = [("Foto de celular\n4000×3000", 4000, 3000), ("Reducida a\n2048×1536", 2048, 1536), ("Reducida a\n1024×768", 1024, 768), ("Reducida a\n512×384", 512, 384)]
fig, ax = plt.subplots(figsize=(10, 5), dpi=160)
x = np.arange(len(casos)); wdt = .38
t41 = [tokens_tiles(w, h) for _, w, h in casos]; tmini = [tokens_patches(w, h, 1.62) for _, w, h in casos]
b1 = ax.bar(x - wdt/2, t41, wdt, label="gpt-4.1 (mosaicos, high)", color="#0969DA")
b2 = ax.bar(x + wdt/2, tmini, wdt, label="gpt-4.1-mini (parches)", color="#8250DF")
ax.bar_label(b1, fontsize=9); ax.bar_label(b2, fontsize=9)
ax.set_xticks(x, [c[0] for c in casos]); ax.set_ylabel("tokens de la imagen"); ax.legend()
ax.set_title("Redimensionar ANTES de enviar: los modelos por mosaicos topan en 768 px; los de parches siguen cobrando por píxel")
ax.grid(axis="y", alpha=.3); plt.tight_layout(); plt.savefig(OUT / "redimensionar-ahorra.png", facecolor="white"); plt.close()
print("ok", t41, tmini)
