import yaml
import json
from pathlib import Path

def load_api_spec(path: Path) -> dict:
    path_str = str(path)  # convert Path to string
    if path_str.endswith('.yaml') or path_str.endswith('.yml'):
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    elif path_str.endswith('.json'):
        with open(path, 'r') as f:
            return json.load(f)
    else:
        raise ValueError("Unsupported file format: must be YAML or JSON")
