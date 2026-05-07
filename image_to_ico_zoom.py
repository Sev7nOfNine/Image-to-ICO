"""Mini app Tkinter pour convertir une image en .ico - VERSION ZOOM
- Drag & drop ou clic pour selectionner
- Retire le fond avec rembg
- Crop auto sur le sujet (bbox alpha) puis pad en carre avec marge 5%
  -> le sujet remplit le canvas, ideal pour barre des taches
- Genere un .ico multi-tailles a cote du fichier source (suffixe _zoom)
"""

import os
import sys
import threading
from pathlib import Path

# pythonw.exe met stdout/stderr a None -> rembg/tqdm crashent en ecrivant dedans.
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")
from tkinter import Tk, Label, Button, filedialog, StringVar
from tkinter import ttk

from PIL import Image
from tkinterdnd2 import DND_FILES, TkinterDnD

ICO_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
MARGIN_RATIO = 0.05  # 5% de marge autour du sujet


def crop_to_subject(img: Image.Image) -> Image.Image:
    """Crop sur la bbox de l'alpha pour virer la zone transparente autour du sujet."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    alpha = img.split()[-1]
    bbox = alpha.getbbox()
    if bbox:
        return img.crop(bbox)
    return img


def pad_to_square_with_margin(img: Image.Image, margin_ratio: float = MARGIN_RATIO) -> Image.Image:
    """Pad transparent en carre avec une petite marge pour respirer."""
    w, h = img.size
    side = max(w, h)
    canvas_side = int(side * (1 + 2 * margin_ratio))
    canvas = Image.new("RGBA", (canvas_side, canvas_side), (0, 0, 0, 0))
    canvas.paste(img, ((canvas_side - w) // 2, (canvas_side - h) // 2), img)
    return canvas


def convert(path: str, status_var: StringVar, progress: ttk.Progressbar):
    try:
        from rembg import remove

        src = Path(path)
        if not src.is_file():
            status_var.set(f"[X] Fichier introuvable : {src.name}")
            return

        status_var.set(f"[...] Lecture de {src.name}")
        progress.start(10)

        with open(src, "rb") as f:
            input_bytes = f.read()

        status_var.set("[...] Suppression du fond (peut prendre quelques secondes)")
        output_bytes = remove(input_bytes)

        status_var.set("[...] Crop sur le sujet et generation du .ico")
        from io import BytesIO
        img = Image.open(BytesIO(output_bytes)).convert("RGBA")

        cropped = crop_to_subject(img)
        squared = pad_to_square_with_margin(cropped)

        out_path = src.with_name(f"{src.stem}_zoom.ico")
        squared.save(out_path, format="ICO", sizes=ICO_SIZES, bitmap_format="png")

        progress.stop()
        status_var.set(f"[OK] Cree : {out_path.name}")
    except Exception as e:
        progress.stop()
        status_var.set(f"[X] Erreur : {e}")


def on_drop(event, status_var, progress):
    raw = event.data.strip()
    if raw.startswith("{") and raw.endswith("}"):
        raw = raw[1:-1]
    paths = [p for p in raw.split("} {") if p]
    if not paths:
        return
    threading.Thread(
        target=process_batch,
        args=(paths, status_var, progress),
        daemon=True,
    ).start()


def process_batch(paths, status_var, progress):
    for i, p in enumerate(paths, 1):
        status_var.set(f"[{i}/{len(paths)}] Traitement...")
        convert(p, status_var, progress)


def on_click(status_var, progress):
    paths = filedialog.askopenfilenames(
        title="Choisir une ou plusieurs images",
        filetypes=[
            ("Images", "*.png *.jpg *.jpeg *.bmp *.webp *.tiff"),
            ("Tous les fichiers", "*.*"),
        ],
    )
    if not paths:
        return
    threading.Thread(
        target=process_batch,
        args=(list(paths), status_var, progress),
        daemon=True,
    ).start()


def main():
    root = TkinterDnD.Tk()
    root.title("Image -> ICO (Zoom)")
    root.geometry("480x280")
    root.configure(bg="#1e1e2e")

    title = Label(
        root,
        text="Image -> ICO  [ZOOM]",
        font=("Segoe UI", 16, "bold"),
        bg="#1e1e2e",
        fg="#f9e2af",
    )
    title.pack(pady=(18, 6))

    drop_zone = Label(
        root,
        text="Glisse une image ici\n(ou clique pour choisir)\n\nVersion crop sur le sujet",
        font=("Segoe UI", 11),
        bg="#313244",
        fg="#a6adc8",
        width=44,
        height=7,
        relief="ridge",
        bd=2,
    )
    drop_zone.pack(padx=20, pady=10, fill="x")

    status_var = StringVar(value="Pret. Sortie suffixee _zoom.ico")
    status = Label(
        root,
        textvariable=status_var,
        font=("Segoe UI", 9),
        bg="#1e1e2e",
        fg="#f9e2af",
        wraplength=440,
    )
    status.pack(pady=(4, 4))

    progress = ttk.Progressbar(root, mode="indeterminate", length=300)
    progress.pack(pady=(0, 10))

    drop_zone.drop_target_register(DND_FILES)
    drop_zone.dnd_bind("<<Drop>>", lambda e: on_drop(e, status_var, progress))
    drop_zone.bind("<Button-1>", lambda e: on_click(status_var, progress))

    root.mainloop()


if __name__ == "__main__":
    main()
