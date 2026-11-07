"""Genera la figura del tema 1 del módulo 7: qué IQ cubre qué tipo de dato. Solo matplotlib.
Basado en la documentación de Microsoft Learn (octubre de 2026)."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

OUT = Path(__file__).resolve().parent

cols = ["Work IQ", "Foundry IQ", "Fabric IQ", "Web IQ"]
filas = [
    ("Correos, calendario y chats de Teams",        [2, 1, 0, 0], ["", "fuente Work IQ\n(preview)", "", ""]),
    ("Personas, organigrama, colaboración",          [2, 1, 0, 0], ["", "fuente Work IQ\n(preview)", "", ""]),
    ("Documentos de SharePoint / OneDrive",          [2, 2, 0, 0], ["del usuario", "curados por dominio", "", ""]),
    ("PDFs y archivos en Blob Storage",              [0, 2, 0, 0], ["", "", "", ""]),
    ("Tablas de Azure SQL",                          [0, 1, 1, 0], ["", "preview", "vía OneLake", ""]),
    ("Lakehouse en OneLake",                         [0, 1, 2, 0], ["", "", "", ""]),
    ("Métricas y KPI de negocio (modelo semántico)", [0, 1, 2, 0], ["", "fuente Fabric\n(preview)", "", ""]),
    ("Entidades y reglas de negocio (ontología)",    [0, 1, 2, 0], ["", "fuente Fabric\n(preview)", "", ""]),
    ("Dynamics 365 / Power Platform",                [1, 0, 0, 0], ["Context", "", "", ""]),
    ("Web pública y noticias",                       [0, 1, 0, 2], ["", "fuente Web\n(Bing)", "", ""]),
]
import numpy as np
M = np.array([f[1] for f in filas])
cmap = ListedColormap(["#F3F2F1", "#9CC3E8", "#0F6CBD"])
fig, ax = plt.subplots(figsize=(11.5, 7.2), dpi=160)
ax.imshow(M, cmap=cmap, vmin=0, vmax=2, aspect="auto")
ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols, fontsize=11, weight="bold")
ax.xaxis.tick_top()
ax.set_yticks(range(len(filas))); ax.set_yticklabels([f[0] for f in filas], fontsize=10)
sim = {0: "—", 1: "puede\nconsultarlo", 2: "su\nespecialidad"}
for i, f in enumerate(filas):
    for j, v in enumerate(f[1]):
        txt = f[2][j] if f[2][j] else sim[v]
        if v and f[2][j]:
            txt = ("★ " if v == 2 else "") + f[2][j]
        elif v == 2:
            txt = "★ su especialidad"
        ax.text(j, i, txt, ha="center", va="center", fontsize=8.2,
                color="white" if v == 2 else ("#1B1A19" if v == 1 else "#A19F9D"))
ax.set_xticks(np.arange(-.5, len(cols)), minor=True); ax.set_yticks(np.arange(-.5, len(filas)), minor=True)
ax.grid(which="minor", color="white", lw=2); ax.tick_params(which="minor", length=0)
ax.set_title("¿Qué IQ conoce qué dato?  (★ = su especialidad · azul claro = lo puede consultar)", fontsize=12, pad=38)
plt.tight_layout(); plt.savefig(OUT / "iq-cobertura-datos.png", facecolor="white"); plt.close()
print("ok")
