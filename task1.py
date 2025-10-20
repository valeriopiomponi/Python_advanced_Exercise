# image_to_json.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import numpy as np
from PIL import Image, TiffImagePlugin


class ImageToJson:
    """
    Read a .tif image, convert image data + metadata to JSON,
    filter out null/None-like features, and save to disk.
    """

    def __init__(self, image_path: str | Path) -> None:
        self.image_path = Path(image_path)

        if not self.image_path.exists():
            raise FileNotFoundError(f"Image not found: {self.image_path}")
        if self.image_path.suffix.lower() not in {".tif", ".tiff"}:
            raise ValueError("Expected a .tif/.tiff image")

    # --------- public API ---------
    def process(self, out_path: str | Path = "data.json") -> Path:
        """
        End-to-end: load image, build JSON payload, filter nulls, save.
        Returns the output path.
        """
        img, np_data = self._load_image()
        payload = {
            "source_path": str(self.image_path),
            "image": {
                "format": img.format,
                "mode": img.mode,
                "size": {"width": img.width, "height": img.height},
                "dtype": str(np_data.dtype),
                # Note: this can be large; for assignments we include full data.
                "data": np_data.tolist(),
            },
            "metadata": self._extract_metadata(img),
        }

        cleaned = self._filter_null_like(payload)
        out_path = Path(out_path)
        self._save_json(cleaned, out_path)
        return out_path

    # --------- internals ---------
    def _load_image(self) -> tuple[Image.Image, np.ndarray]:
        """
        Opens the image and returns (PIL_image, numpy_array).
        """
        with Image.open(self.image_path) as img:
            # Ensure we load the pixels before the file handle closes
            pil_img = img.copy()

        # Convert to a sensible NumPy array (no dtype surprises)
        np_data = np.array(pil_img)

        return pil_img, np_data

    def _extract_metadata(self, img: Image.Image) -> Dict[str, Any]:
        """
        Extracts common metadata from Pillow.
        For TIFFs we also read the tag dictionary (when available).
        """
        meta: Dict[str, Any] = {}

        # Basic info dict (non-standard, depends on encoder)
        if img.info:
            # Convert any non-JSON-serializable values to strings
            meta["info"] = {k: self._jsonify_scalar(v) for k, v in img.info.items()}

        # TIFF tag dictionary (more structured)
        if isinstance(img, TiffImagePlugin.TiffImageFile):
            try:
                # tag_v2 is a mapping {tag_id: value}; convert ids to names when possible
                tag_dict = {}
                for tag_id, value in img.tag_v2.items():
                    name = TiffImagePlugin.TAGS_V2.get(tag_id, f"Tag{tag_id}")
                    tag_dict[str(name)] = self._jsonify_scalar(value)
                if tag_dict:
                    meta["tiff_tags"] = tag_dict
            except Exception:
                # Be robust—metadata varies a lot across TIFFs
                pass

        return meta

    def _jsonify_scalar(self, value: Any) -> Any:
        """
        Convert values to JSON-serializable Python types.
        - NumPy scalars/arrays -> Python types / lists
        - Bytes -> hex string
        - Everything else left as-is if JSON can handle it
        """
        if isinstance(value, np.ndarray):
            return value.tolist()
        if isinstance(value, (np.generic,)):
            return value.item()
        if isinstance(value, (bytes, bytearray)):
            # safer than raw bytes in JSON
            return value.hex()
        # Some TIFF values are tuples of mixed types (convert inner scalars)
        if isinstance(value, (tuple, list)):
            return [self._jsonify_scalar(v) for v in value]
        if isinstance(value, dict):
            return {str(k): self._jsonify_scalar(v) for k, v in value.items()}
        return value

    def _filter_null_like(self, obj: Any) -> Any:
        """
        Recursively remove keys whose values are:
        - None
        - the literal string "null" (case-insensitive)
        - empty containers ([], {}, "")
        """
        # Remove string "null" (any case) and empty strings
        if isinstance(obj, str):
            s = obj.strip()
            if s == "" or s.lower() == "null":
                return None
            return obj

        # Walk lists
        if isinstance(obj, list):
            filtered_list = [self._filter_null_like(v) for v in obj]
            filtered_list = [v for v in filtered_list if v is not None]
            return filtered_list

        # Walk dicts
        if isinstance(obj, dict):
            filtered_dict = {}
            for k, v in obj.items():
                fv = self._filter_null_like(v)
                # drop if None or empty container
                if fv is None:
                    continue
                if isinstance(fv, (list, dict)) and len(fv) == 0:
                    continue
                filtered_dict[k] = fv
            return filtered_dict

        # Plain scalars
        if obj is None:
            return None

        return obj

    def _save_json(self, payload: Dict[str, Any], out_path: Path) -> None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # Example usage:
    #   python image_to_json.py path/to/image.tif data.json
    import sys

    if len(sys.argv) not in (2, 3):
        print("Usage: python image_to_json.py <image.tif> [out.json]")
        sys.exit(1)

    image_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) == 3 else "data.json"

    converter = ImageToJson(image_path)
    output = converter.process(out_path)
    print(f"Saved JSON to: {output}")
