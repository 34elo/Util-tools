import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from processor import read, generate
from config import DEFAULTS


class App:
    """Главное окно приложения."""
    
    def __init__(self, root):
        self.root = root
        self.root.title('Spreadsheet Converter')
        self.root.geometry('1200x800')
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(True, True)

        self.xlsx_path = None
        self.values = []

        main_frame = ttk.Frame(root, padding='20')
        main_frame.pack(fill='both', expand=True)

        file_frame = ttk.LabelFrame(
            main_frame,
            text='Выберите .xlsx файл (данные должны быть в первом столбце)',
            padding='10'
        )
        file_frame.pack(fill='x', pady=(0, 15))

        file_row = ttk.Frame(file_frame)
        file_row.pack(fill='x')

        self.file_btn = ttk.Button(
            file_row, text='Выбрать файл',
            command=self.select_file, width=20
        )
        self.file_btn.pack(side='left')

        self.file_label = ttk.Label(
            file_row, text='Файл не выбран',
            foreground='gray'
        )
        self.file_label.pack(side='left', padx=15, fill='x', expand=True)

        preview_frame = ttk.LabelFrame(main_frame, text='Предпросмотр', padding='10')
        preview_frame.pack(fill='both', expand=True, pady=(0, 15))

        columns = ('#', 'Значение', 'Длина')
        self.tree = ttk.Treeview(preview_frame, columns=columns, show='headings', height=8)

        self.tree.heading('#', text='#')
        self.tree.heading('Значение', text='Значение')
        self.tree.heading('Длина', text='Длина')

        self.tree.column('#', width=50, anchor='center')
        self.tree.column('Значение', width=350)
        self.tree.column('Длина', width=80, anchor='center')

        scrollbar = ttk.Scrollbar(preview_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.count_label = ttk.Label(
            preview_frame, text='Записей: 0',
            font=('Segoe UI', 9, 'italic')
        )
        self.count_label.pack(anchor='e', pady=(5, 0))

        params_frame = ttk.LabelFrame(main_frame, text='Параметры XML', padding='10')
        params_frame.pack(fill='x', pady=(0, 15))

        self.entries = {}
        for label, default in DEFAULTS.items():
            row = ttk.Frame(params_frame)
            row.pack(fill='x', pady=3)
            ttk.Label(row, text=f'{label}:', width=15).pack(side='left')
            entry = ttk.Entry(row, width=30)
            entry.insert(0, default)
            entry.pack(side='left', padx=5, fill='x', expand=True)
            self.entries[label] = entry

        self.save_btn = ttk.Button(
            main_frame, text='Сохранить как .xml',
            command=self.save_file
        )
        self.save_btn.pack(pady=5)

    def select_file(self):
        """Выбор xlsx файла."""
        path = filedialog.askopenfilename(
            title='Выберите .xlsx файл',
            filetypes=[('Excel files', '*.xlsx'), ('All files', '*.*')]
        )
        if path:
            self.xlsx_path = path
            self.file_label.config(text=os.path.basename(path))

            try:
                self.values = read(path)
                self.update_preview()
            except Exception as e:
                messagebox.showerror('Ошибка', f'Не удалось прочитать файл:\n{e}')
                self.file_label.config(text='Ошибка чтения', foreground='red')

    def update_preview(self):
        """Обновление таблицы предпросмотра."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, value in enumerate(self.values, 1):
            self.tree.insert('', 'end', values=(i, value, len(value)))

        self.count_label.config(text=f'Записей: {len(self.values)}')

    def save_file(self):
        """Сохранение данных в XML файл."""
        if not self.xlsx_path:
            messagebox.showerror('Ошибка', 'Сначала выберите .xlsx файл')
            return

        if not self.values:
            messagebox.showerror('Ошибка', 'Файл не содержит данных для экспорта')
            return

        output_path = filedialog.asksaveasfilename(
            title='Сохранить как',
            defaultextension='.xml',
            filetypes=[('XML files', '*.xml'), ('All files', '*.*')]
        )
        if not output_path:
            return

        try:
            action_id = self.entries['action_id'].get()
            version = self.entries['version'].get()
            inn = self.entries['inn'].get()

            count = generate(self.values, action_id, version, inn, output_path)
            messagebox.showinfo('Готово', f'Файл сохранён.\nЗаписей: {count}')

        except Exception as e:
            messagebox.showerror('Ошибка', str(e))
