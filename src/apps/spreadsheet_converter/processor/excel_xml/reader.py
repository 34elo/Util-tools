import openpyxl


def read(file_path):
    """Читает значения из первого столбца xlsx файла."""
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active
    values = []
    
    for row in ws.iter_rows(min_col=1, max_col=1, values_only=True):
        value = row[0]
        if value is not None and str(value).strip():
            values.append(str(value).strip())
    
    wb.close()
    return values