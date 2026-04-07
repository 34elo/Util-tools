import json


def detect_json_type(data):
    """Определяет тип JSON файла."""
    if 'products' in data:
        return 'boxes_dm'
    elif 'aggregationUnits' in data:
        return 'pallets_kiga'
    return None


def parse_json_file(file_path):
    """Парсит JSON файл и возвращает тип и данные."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    json_type = detect_json_type(data)

    if json_type == 'boxes_dm':
        return {
            'type': 'boxes_dm',
            'boxes': _extract_boxes(data),
            'dm': _extract_dm(data)
        }
    elif json_type == 'pallets_kiga':
        return {
            'type': 'pallets_kiga',
            'pallets': _extract_pallets(data),
            'kiga': _extract_kiga(data)
        }

    return None


def _extract_boxes(data):
    """Извлекает коробки (uit_code верхнего уровня)."""
    boxes = []
    products = data.get('products', [])
    for product in products:
        if 'uit_code' in product:
            boxes.append(product['uit_code'])
    return boxes


def _extract_dm(data):
    """Извлекает ДМ (uit_code из children)."""
    dm = []
    products = data.get('products', [])
    for product in products:
        children = product.get('children', [])
        for child in children:
            if 'uit_code' in child:
                dm.append(child['uit_code'])
    return dm


def _extract_pallets(data):
    """Извлекает паллеты (unitSerialNumber)."""
    pallets = []
    aggregation_units = data.get('aggregationUnits', [])
    for unit in aggregation_units:
        if 'unitSerialNumber' in unit:
            pallets.append(unit['unitSerialNumber'])
    return pallets


def _extract_kiga(data):
    """Извлекает киги (sntins)."""
    kiga = []
    aggregation_units = data.get('aggregationUnits', [])
    for unit in aggregation_units:
        sntins = unit.get('sntins', [])
        kiga.extend(sntins)
    return kiga
