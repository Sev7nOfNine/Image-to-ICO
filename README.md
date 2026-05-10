# Image to ICO

Petite app Windows (Tkinter) pour convertir n'importe quelle image en `.ico` :
- Drag & drop ou clic pour choisir
- Suppression automatique du fond ([rembg](https://github.com/danielgatis/rembg) / u2net)
- Generation `.ico` multi-tailles (16, 32, 48, 64, 128, 256) avec encodage PNG pour preserver la transparence dans la barre des taches
- Deux modes : image complete ou crop auto sur le sujet

## Installation

Pre-requis : **Python 3.10+** ([python.org](https://www.python.org/downloads/), cocher "Add to PATH" a l'install).

1. Cloner ou telecharger ce repo
2. Double-cliquer sur `install.bat`
3. Attendre que les dependances s'installent (1-2 min)

## Utilisation

| Fichier | Mode | Sortie |
|---|---|---|
| `Image_to_ICO.vbs` | Image complete (pad transparent en carre) | `mon_image.ico` |
| `Image_to_ICO_ZOOM.vbs` | Crop auto sur le sujet + 5% de marge | `mon_image_zoom.ico` |

Double-clic sur le `.vbs` -> une fenetre s'ouvre -> drag & drop ton image dedans.

Le tout premier run telecharge le modele u2net (~170 Mo, une seule fois). Les suivants sont rapides.

## Debug

Si quelque chose plante, lance `Image_to_ICO_DEBUG.bat` : la console reste ouverte avec le detail de l'erreur.

## Stack

- [Pillow](https://python-pillow.org/) pour la generation `.ico`
- [rembg](https://github.com/danielgatis/rembg) pour la suppression de fond
- [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2) pour le drag & drop


---

By Mel & Ada ♡
