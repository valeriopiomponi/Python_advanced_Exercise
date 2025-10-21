# semmeta/json_cleaner_module.py

import json
from pathlib import Path

class JSONCleaner:
    """
    Reads output/<name>_raw.json, removes entries whose values are None or "null",
    and writes output/<name>_cleaned.json.
    """

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _resolve_raw_path(self, raw_json_name: str) -> Path:
        p = Path(raw_json_name)
        if not p.suffix:
            p = Path(f"{raw_json_name}_raw.json")
        if not p.name.endswith("_raw.json"):
            p = p.with_name(p.stem + "_raw.json")
        if not p.is_absolute():
            p = self.output_dir / p.name
        return p

    def _clean_value(self, value):
        """
        Recursively remove values that are None or the string 'null' (case-insensitive).
        Keeps containers; only prunes offending entries.
        """
        # drop if None or "null"
        if value is None:
            return None  # marker for drop
        if isinstance(value, str) and value.strip().lower() == "null":
            return None  # marker for drop

        if isinstance(value, dict):
            cleaned = {}
            for k, v in value.items():
                cv = self._clean_value(v)
                if cv is not None:
                    cleaned[k] = cv
            return cleaned

        if isinstance(value, list):
            cleaned_list = []
            for item in value:
                ci = self._clean_value(item)
                if ci is not None:
                    cleaned_list.append(ci)
            return cleaned_list

        # leave as-is
        return value

    def run(self, raw_json_name: str) -> Path:
        """
        Main entry point. Returns path to the cleaned JSON file.
        """
        raw_path = self._resolve_raw_path(raw_json_name)
        if not raw_path.exists():
            raise FileNotFoundError(f"Raw JSON not found: {raw_path}")

        with open(raw_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        cleaned = self._clean_value(data)

        cleaned_path = self.output_dir / raw_path.name.replace("_raw.json", "_cleaned.json")
        with open(cleaned_path, "w", encoding="utf-8") as f:
            json.dump(cleaned, f, indent=2, ensure_ascii=False)

        return cleaned_path

