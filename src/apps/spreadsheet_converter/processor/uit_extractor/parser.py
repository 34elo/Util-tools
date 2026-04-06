import json


def parse_json_uit_codes(file_path):
    """Парсит JSON файл и извлекает все значения uit_code."""
    uit_codes = []

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    _extract_uit_codes(data, uit_codes)

    return uit_codes


def _extract_uit_codes(obj, uit_codes):
    """Рекурсивно извлекает uit_code из объекта."""
    if isinstance(obj, dict):
        if 'uit_code' in obj:
            uit_codes.append(obj['uit_code'])
        for value in obj.values():
            _extract_uit_codes(value, uit_codes)
    elif isinstance(obj, list):
        for item in obj:
            _extract_uit_codes(item, uit_codes)