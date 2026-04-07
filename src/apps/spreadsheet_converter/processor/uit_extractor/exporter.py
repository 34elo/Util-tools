import openpyxl


def generate_xlsx(data_list, output_path):
    """Генерирует XLSX файл с данными в одном столбце."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Data'

<<<<<<< HEAD
    for code in uit_codes:
        ws.append([code])
=======
    for item in data_list:
        ws.append([item])
>>>>>>> 8c19220 (feature: update spreadsheet_converter)

    wb.save(output_path)
    wb.close()
