import json
import re

class JsonCleaner:
    def __init__(self, cleaned_data={}):                       
        self.cleaned_data = cleaned_data

    def load_json(self, jsfile):
        with open(jsfile, 'r') as f:
            return json.load(f)

    def clean_value(self, value):
        """
        Extracts numeric value and unit from strings like 'Liner Tube =  8.00 kV'
        """
        match = re.search(r'([\d.]+)\s*([a-zA-Zμ]+)', value)
        if match:
            return match.group(1) + ' ' + match.group(2)
        return value

    def clean_dict(self, data):
        cleaned = {}
        for key, value in data.items():
            if value is None:
                continue
            if isinstance(value, str):
                cleaned[key] = self.clean_value(value)
            else:
                cleaned[key] = value
        return cleaned

    def process(self, jsfile):
        raw_data = self.load_json(jsfile)
        self.cleaned_data = self.clean_dict(raw_data)
        return self.cleaned_data

    def save_cleaned(self, output_path):
        with open(output_path, 'w') as f:
            json.dump(self.cleaned_data, f, indent=2)

