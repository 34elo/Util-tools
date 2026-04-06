import tkinter as tk
from tkinter import ttk

from ui.excel_xml.app import Tab as ExcelTab
from ui.uit_extractor.app import Tab as UitTab


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Spreadsheet Converter')
        self.root.geometry('1200x900')
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(True, True)
        
        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)
        
        self.excel_tab = ExcelTab(notebook)
        self.uit_tab = UitTab(notebook)
        
        notebook.add(self.excel_tab, text='Из Excel в XML')
        notebook.add(self.uit_tab, text='Извлечение UIT кодов')


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()