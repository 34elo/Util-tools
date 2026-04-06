import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from processor.uit_extractor import parse_json_uit_codes, generate_xlsx


class Tab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding='20')
        
        self.json_path = None
        self.uit_codes = []
        
        self._init_ui()
    
    def _init_ui(self):
        file_frame = ttk.LabelFrame(
            self,
            text='Выберите .json файл',
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
        
        preview_frame = ttk.LabelFrame(self, text='Предпросмотр UIT кодов', padding='10')
        preview_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        columns = ('#', 'UIT Code', 'Длина')
        self.tree = ttk.Treeview(preview_frame, columns=columns, show='headings', height=15)
        
        self.tree.heading('#', text='#')
        self.tree.heading('UIT Code', text='UIT Code')
        self.tree.heading('Длина', text='Длина')
        
        self.tree.column('#', width=50, anchor='center')
        self.tree.column('UIT Code', width=450)
        self.tree.column('Длина', width=80, anchor='center')
        
        scrollbar = ttk.Scrollbar(preview_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.count_label = ttk.Label(
            preview_frame, text='Кодов: 0',
            font=('Segoe UI', 9, 'italic')
        )
        self.count_label.pack(anchor='e', pady=(5, 0))
        
        self.save_btn = ttk.Button(
            self, text='Сохранить как .xlsx',
            command=self.save_file
        )
        self.save_btn.pack(pady=5)
    
    def select_file(self):
        path = filedialog.askopenfilename(
            title='Выберите .json файл',
            filetypes=[('JSON files', '*.json'), ('All files', '*.*')]
        )
        if path:
            self.json_path = path
            self.file_label.config(text=os.path.basename(path))
            
            try:
                self.uit_codes = parse_json_uit_codes(path)
                self.update_preview()
            except Exception as e:
                messagebox.showerror('Ошибка', f'Не удалось прочитать файл:\n{e}')
                self.file_label.config(text='Ошибка чтения', foreground='red')
    
    def update_preview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for i, code in enumerate(self.uit_codes, 1):
            self.tree.insert('', 'end', values=(i, code, len(code)))
        
        self.count_label.config(text=f'Кодов: {len(self.uit_codes)}')
    
    def save_file(self):
        if not self.json_path:
            messagebox.showerror('Ошибка', 'Сначала выберите .json файл')
            return
        
        if not self.uit_codes:
            messagebox.showerror('Ошибка', 'Файл не содержит кодов для экспорта')
            return
        
        output_path = filedialog.asksaveasfilename(
            title='Сохранить как',
            defaultextension='.xlsx',
            filetypes=[('Excel files', '*.xlsx'), ('All files', '*.*')]
        )
        if not output_path:
            return
        
        try:
            generate_xlsx(self.uit_codes, output_path)
            messagebox.showinfo('Готово', f'Файл сохранён.\nКодов: {len(self.uit_codes)}')
        
        except Exception as e:
            messagebox.showerror('Ошибка', str(e))