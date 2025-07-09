import random

def generate_valid_value(param_spec):
    if 'enum' in param_spec:
        return random.choice(param_spec['enum'])
    if param_spec['type'] == 'string':
        return 'example'
    if param_spec['type'] == 'integer':
        return random.randint(1, 100)
    if param_spec['type'] == 'boolean':
        return random.choice([True, False])
    return None

def generate_invalid_value(param_spec):
    if param_spec['type'] == 'string':
        return 12345  # Wrong type
    if param_spec['type'] == 'integer':
        return 'invalid'
    if param_spec['type'] == 'boolean':
        return 'notabool'
    return None

def build_test_case(endpoint, method, parameters):
    test_cases = []
    valid_payload = {}
    invalid_payload = {}

    for param in parameters:
        name = param['name']
        valid_payload[name] = generate_valid_value(param['schema'])
        invalid_payload[name] = generate_invalid_value(param['schema'])

    test_cases.append({"type": "valid", "payload": valid_payload})
    test_cases.append({"type": "invalid", "payload": invalid_payload})
    return test_cases
