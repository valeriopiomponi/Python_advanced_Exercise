#write a python class that read a json file and clean it
import json
from pathlib import Path

class JSONCleaner:
    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _resolve_raw(self, name_or_path):
        p = Path(name_or_path)
        if not p.suffix:
            p = Path(f"{p.stem}_raw.json")
        if not p.name.endswith("_raw.json"):
            p = p.with_name(p.stem + "_raw.json")
        if not p.is_absolute():
            p = self.output_dir / p.name
        return p

    def _clean(self, value):
        if value is None:
            return None
        if isinstance(value, str) and value.strip().lower() == "null":
            return None

        if isinstance(value, dict):
            cleaned = {}
            for k, v in value.items():
                cv = self._clean(v)
                if cv is not None:
                    cleaned[k] = cv
            return cleaned

        if isinstance(value, list):
            cleaned_list = []
            for item in value:
                ci = self._clean(item)
                if ci is not None:
                    cleaned_list.append(ci)
            return cleaned_list

        return value

    def run(self, name_or_path):
        raw = self._resolve_raw(name_or_path)
        if not raw.exists():
            raise FileNotFoundError(raw)
        with open(raw, "r", encoding="utf-8") as f:
            data = json.load(f)
        cleaned = self._clean(data)
        out = self.output_dir / raw.name.replace("_raw.json", "_cleaned.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(cleaned, f, indent=2, ensure_ascii=False)
        return out
