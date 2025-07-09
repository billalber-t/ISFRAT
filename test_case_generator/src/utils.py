import yaml
import json

def load_api_spec(path: str) -> dict:
    if path.endswith('.yaml') or path.endswith('.yml'):
        with open(path) as f:
            return yaml.safe_load(f)
    elif path.endswith('.json'):
        with open(path) as f:
            return json.load(f)
    else:
        raise ValueError("Unsupported file format: must be YAML or JSON")

