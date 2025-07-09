# import yaml
# import json

# def load_api_spec(path: str) -> dict:
#     if path.endswith('.yaml') or path.endswith('.yml'):
#         with open(path) as f:
#             return yaml.safe_load(f)
#     elif path.endswith('.json'):
#         with open(path) as f:
#             return json.load(f)
#     else:
#         raise ValueError("Unsupported file format: must be YAML or JSON")

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
