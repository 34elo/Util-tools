import openpyxl


def generate_xlsx(data_list, output_path):
    """Генерирует XLSX файл с данными в одном столбце."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Data'

    for item in data_list:
        ws.append([item])

    wb.save(output_path)
    wb.close()
