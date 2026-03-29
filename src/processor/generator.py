def generate_xml(values, action_id, version, inn, output_path):
    """Генерирует XML файл из списка значений."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<disaggregation action_id="{action_id}" version="{version}">')
    lines.append(f'    <trade_participant_inn>{inn}</trade_participant_inn>')
    lines.append('    <packings_list>')

    for value in values:
        lines.append('        <packing>')
        lines.append('            <kitu><![CDATA[{value}]]></kitu>'.replace('{value}', value))
        lines.append('        </packing>')

    lines.append('    </packings_list>')
    lines.append('</disaggregation>')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return len(values)
