import xml.etree.ElementTree as ET


def read(file_path):
    """Читает данные из XML файла."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    data = {
        'unit_pack_attrs': {},
        'document_attrs': {},
        'organisation': {},
        'pack_contents': []
    }
    
    unit_pack = root
    data['unit_pack_attrs'] = dict(unit_pack.attrib)
    
    document = unit_pack.find('Document')
    if document is not None:
        data['document_attrs'] = dict(document.attrib)
        
        organisation = document.find('organisation')
        if organisation is not None:
            id_info = organisation.find('id_info')
            if id_info is not None:
                lp_info = id_info.find('LP_info')
                if lp_info is not None:
                    data['organisation']['LP_info'] = dict(lp_info.attrib)
            
            address = organisation.find('Address')
            if address is not None:
                location = address.find('location_address')
                if location is not None:
                    data['organisation']['address'] = dict(location.attrib)
            
            contacts = organisation.find('contacts')
            if contacts is not None:
                data['organisation']['contacts'] = dict(contacts.attrib)
        
        pack_contents = document.findall('pack_content')
        for pack in pack_contents:
            pack_data = {}
            pack_code = pack.find('pack_code')
            if pack_code is not None and pack_code.text:
                pack_data['pack_code'] = pack_code.text
            
            cis_list = []
            for cis in pack.findall('cis'):
                if cis.text:
                    cis_list.append(cis.text)
            pack_data['cis'] = cis_list
            
            data['pack_contents'].append(pack_data)
    
    return data


def generate(data, unit_pack_attrs, document_attrs, organisation):
    """Генерирует XML из данных."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    
    unit_pack_attrs_str = ' '.join([f'{k}="{v}"' for k, v in unit_pack_attrs.items()])
    lines.append(f'<unit_pack {unit_pack_attrs_str}>')
    
    doc_attrs_str = ' '.join([f'{k}="{v}"' for k, v in document_attrs.items()])
    lines.append(f'    <Document {doc_attrs_str}>')
    lines.append('        <organisation>')
    lines.append('            <id_info>')
    
    lp_info = organisation.get('LP_info', {})
    lp_attrs = ' '.join([f'{k}="{v}"' for k, v in lp_info.items()])
    lines.append(f'                <LP_info {lp_attrs} />')
    lines.append('            </id_info>')
    
    address = organisation.get('address', {})
    if address:
        addr_attrs = ' '.join([f'{k}="{v}"' for k, v in address.items()])
        lines.append('            <Address>')
        lines.append(f'                <location_address {addr_attrs} />')
        lines.append('            </Address>')
    
    contacts = organisation.get('contacts', {})
    if contacts:
        contact_attrs = ' '.join([f'{k}="{v}"' for k, v in contacts.items()])
        lines.append(f'            <contacts {contact_attrs} />')
    
    lines.append('        </organisation>')
    
    for pack in data.get('pack_contents', []):
        lines.append('        <pack_content>')
        pack_code = pack.get('pack_code', '')
        lines.append(f'            <pack_code><![CDATA[{pack_code}]]></pack_code>')
        for cis in pack.get('cis', []):
            lines.append(f'            <cis><![CDATA[{cis}]]></cis>')
        lines.append('        </pack_content>')
    
    lines.append('    </Document>')
    lines.append('</unit_pack>')
    
    return '\n'.join(lines)
