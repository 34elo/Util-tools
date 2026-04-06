import openpyxl


def generate_xlsx(uit_codes, output_path):
    """Генерирует XLSX файл с UIT кодами в одном столбце."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'UIT Codes'

    for code in uit_codes:
        ws.append([code])

    wb.save(output_path)
    wb.close()