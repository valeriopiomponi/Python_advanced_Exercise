# semmeta/visualizer_module.py

import json
import re
from pathlib import Path

import pandas as pd
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
    def __init__(self, imgs_dir: str = "imgs", output_dir: str = "output"):
        self.imgs_dir = Path(imgs_dir)
        self.output_dir = Path(output_dir)

    # ----------------- core API -----------------

    def run(self, image_stem: str):
        """
        image_stem: name without suffix, e.g. 'LIL_test_defect02' (or with .tif)
        """
        stem = Path(image_stem).stem
        cleaned_path = self.output_dir / f"{stem}_cleaned.json"
        tif_path = self.imgs_dir / f"{stem}.tif"

        data = self._load_json(cleaned_path)
        rows = self._extract_features(data, FEATURES)

        df = pd.DataFrame(rows, columns=["variable", "value", "unit"])
        print("\nExtracted features:\n")
        print(df.to_string(index=False))

        self._plot_image(tif_path, title=stem)

        return df

    # ----------------- helpers -----------------

    def _load_json(self, path: Path) -> dict:
        if not path.exists():
            raise FileNotFoundError(f"Cleaned JSON not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _extract_features(self, data: dict, keys):
        """
        Find target keys anywhere in the (possibly nested) dict.
        Returns list of (variable, value, unit)
        """
        out = []
        for k in keys:
            val = self._find_key_recursive(data, k)
            v, u = self._split_value_and_unit(val)
            out.append((k, v, u))
        return out

    def _find_key_recursive(self, obj, target):
        # depth-first search through dicts/lists to find the first occurrence of `target`
        if isinstance(obj, dict):
            if target in obj:
                return obj[target]
            for v in obj.values():
                found = self._find_key_recursive(v, target)
                if found is not None:
                    return found
        elif isinstance(obj, list):
            for item in obj:
                found = self._find_key_recursive(item, target)
                if found is not None:
                    return found
        return None

    def _split_value_and_unit(self, val):
        """
        Very simple parser:
        - if numeric -> (value, "")
        - if string like '10.2 mm' -> (10.2, 'mm')
        - otherwise -> (stringified, "")
        """
        if val is None:
            return None, ""
        if isinstance(val, (int, float)):
            return val, ""

        s = str(val).strip()
        # number + optional unit (letters, µ, %, °, /)
        m = re.match(r"^\s*([+-]?\d+(?:\.\d+)?)\s*([A-Za-zµμ/%°]+)?", s)
        if m:
            num = float(m.group(1))
            unit = m.group(2) or ""
            return num, unit
        return s, ""

    def _plot_image(self, tif_path: Path, title: str):
        if not tif_path.exists():
            print(f"Warning: image not found: {tif_path}")
            return
        with Image.open(tif_path) as im:
            plt.figure()
            plt.imshow(im, cmap="gray")
            plt.title(title)
            plt.axis("off")
            plt.show()



