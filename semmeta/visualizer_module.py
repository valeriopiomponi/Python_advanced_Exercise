#write a python class for extraction and visualization
import json
import re
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image

FEATURES = [
    "AP_WD",
    "AP_BEAM_TIME",
    "AP_IMAGE_PIXEL_SIZE",
    "AP_HOLDER_HEIGHT",
    "AP_BEAM_CURRENT",
    "AP_HOLDER_DIAMETER",
]

class Visualizer:
    def __init__(self, imgs_dir="imgs", output_dir="output"):
        self.imgs_dir = Path(imgs_dir)
        self.output_dir = Path(output_dir)

    def run(self, image_stem):
        stem = Path(image_stem).stem
        cleaned_path = self.output_dir / f"{stem}_cleaned.json"
        tif_path = self.imgs_dir / f"{stem}.tif"

        with open(cleaned_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        rows = []
        for key in FEATURES:
            val = self._find(data, key)
            v, u = self._split(val)
            rows.append((key, v, u))

        # print simple table
        print("\nvariable              value            unit")
        print("---------------------------------------------")
        for k, v, u in rows:
            print(f"{k:<20} {str(v):<16} {u}")

        # show image
        if tif_path.exists():
            with Image.open(tif_path) as im:
                plt.figure()
                plt.imshow(im, cmap="gray")
                plt.title(stem)
                plt.axis("off")
                plt.show()
        else:
            print(f"Image not found: {tif_path}")

        return rows

    def _find(self, obj, target):
        if isinstance(obj, dict):
            if target in obj:
                return obj[target]
            for v in obj.values():
                r = self._find(v, target)
                if r is not None: return r
        elif isinstance(obj, list):
            for it in obj:
                r = self._find(it, target)
                if r is not None: return r
        return None

    def _split(self, val):
        if val is None: return None, ""
        if isinstance(val, (int, float)): return val, ""
        s = str(val).strip()
        m = re.match(r"^\s*([+-]?\d+(?:\.\d+)?)\s*([A-Za-zµμ/%°]+)?", s)
        if m: return float(m.group(1)), (m.group(2) or "")
        return s, ""
