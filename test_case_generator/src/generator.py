import random
import string


def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))


def random_email():
    return f"{random_string(5)}@example.com"


def generate_valid_value(param_spec):
    if 'enum' in param_spec:
        return random.choice(param_spec['enum'])

    if param_spec['type'] == 'string':
        fmt = param_spec.get('format', '')
        if fmt == 'email':
            return random_email()
        return random_string()

    if param_spec['type'] == 'integer':
        return random.randint(1, 100)

    if param_spec['type'] == 'number':
        return round(random.uniform(1.0, 100.0), 2)

    if param_spec['type'] == 'boolean':
        return random.choice([True, False])

    return None  # fallback


def generate_invalid_value(param_spec):
    if param_spec['type'] == 'string':
        return 12345  # wrong type

    if param_spec['type'] == 'integer':
        return "invalid"  # wrong type

    if param_spec['type'] == 'number':
        return "not_a_number"  # wrong type

    if param_spec['type'] == 'boolean':
        return "notabool"  # wrong type

    return None  # fallback


def build_test_case(endpoint, method, parameters):
    test_cases = []
    valid_payload = {}
    invalid_payload = {}

    for param in parameters:
        name = param['name']
        schema = param['schema']

        valid_payload[name] = generate_valid_value(schema)
        invalid_payload[name] = generate_invalid_value(schema)

    test_cases.append({"type": "valid", "payload": valid_payload})
    test_cases.append({"type": "invalid", "payload": invalid_payload})

    return test_cases
