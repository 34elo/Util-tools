# Util-Tools

Набор утилит для работы с файлами.

## Приложения

### Spreadsheet Converter
Конвертер данных из Excel (xlsx) в XML формат + извлечение UIT кодов из JSON.

### XML Transform
Преобразование XML файлов из формата 1 в формат 2.

---

## Spreadsheet Converter

### Требования
- Python 3.8+
- openpyxl

### Установка
```bash
cd src/apps/spreadsheet_converter
pip install -r requirements.txt
```

### Запуск
```bash
cd src/apps/spreadsheet_converter
python main.py
```

### Сборка .exe
```bash
pip install pyinstaller
pyinstaller --onefile --windowed src/apps/spreadsheet_converter/main.py
```

### Функционал

#### Вкладка "Из Excel в XML"
Конвертация значений из xlsx файла в XML формат. Данные читаются из первого столбца.

#### Вкладка "Извлечение UIT кодов"
Парсинг JSON файла и извлечение всех значений `uit_code` с последующим экспортом в xlsx.

---

## XML Transform

### Требования
- Python 3.8+

### Запуск
```bash
cd src/apps/xml_transform
python main.py
```

### Сборка .exe
```bash
pip install pyinstaller
pyinstaller --onefile --windowed src/apps/xml_transform/main.py
```

---

## Структура проекта

```
util-tools/
├── .gitignore
├── README.md
└── src/
    └── apps/
        ├── spreadsheet_converter/
        │   ├── config.py
        │   ├── main.py
        │   ├── requirements.txt
        │   ├── processor/
        │   │   ├── __init__.py
        │   │   ├── excel_xml/
        │   │   │   ├── __init__.py
        │   │   │   ├── reader.py
        │   │   │   └── generator.py
        │   │   └── uit_extractor/
        │   │       ├── __init__.py
        │   │       ├── parser.py
        │   │       └── exporter.py
        │   └── ui/
        │       ├── excel_xml/
        │       │   └── app.py
        │       └── uit_extractor/
        │           └── app.py
        └── xml_transform/
            ├── config.py
            ├── main.py
            ├── requirements.txt
            ├── processor/
            │   ├── __init__.py
            │   └── xml_processor.py
            └── ui/
                └── app.py
```
