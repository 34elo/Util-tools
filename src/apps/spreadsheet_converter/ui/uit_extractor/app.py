import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from processor.uit_extractor import parse_json_file, generate_xlsx


class Tab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding='20')
        
        self.json_path = None
        self.parsed_data = None
        
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
        
        self.type_label = ttk.Label(
            file_row, text='',
            foreground='blue'
        )
        self.type_label.pack(side='left', padx=10)
        
        preview_frame = ttk.LabelFrame(self, text='Предпросмотр', padding='10')
        preview_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        self.preview_frame = preview_frame
        self.count_label = ttk.Label(
            preview_frame, text='Записей: 0',
            font=('Segoe UI', 9, 'italic')
        )
        self.count_label.pack(anchor='e', pady=(5, 0))
        
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(pady=5)
    
    def select_file(self):
        path = filedialog.askopenfilename(
            title='Выберите .json файл',
            filetypes=[('JSON files', '*.json'), ('All files', '*.*')]
        )
        if path:
            self.json_path = path
            self.file_label.config(text=os.path.basename(path))
            
            try:
                self.parsed_data = parse_json_file(path)
                
                if self.parsed_data is None:
                    messagebox.showerror('Ошибка', 'Неизвестный формат JSON файла')
                    self.file_label.config(text='Неизвестный формат', foreground='red')
                    return
                
                self._setup_ui_for_type()
                
            except Exception as e:
                messagebox.showerror('Ошибка', f'Не удалось прочитать файл:\n{e}')
                self.file_label.config(text='Ошибка чтения', foreground='red')
    
    def _setup_ui_for_type(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        
        for widget in self.preview_frame.winfo_children():
            if widget != self.count_label:
                widget.destroy()
        
        data_type = self.parsed_data['type']
        
        if data_type == 'boxes_dm':
            self.type_label.config(text='Тип коробки и ДМ')
            
            columns = ('num', 'first', 'len1', 'second', 'len2')
            first_heading, second_heading = 'Коробки', 'ДМ'
            
            boxes = self.parsed_data['boxes']
            dm = self.parsed_data['dm']
            
            self._create_tree(columns, first_heading, second_heading)
            self._update_preview(boxes, dm)
            
            self.btn_boxes = ttk.Button(
                self.buttons_frame,
                text=f'Выгрузить коробки ({len(boxes)})',
                command=lambda: self.export_data(boxes, 'Коробки')
            )
            self.btn_boxes.pack(side='left', padx=5)
            
            self.btn_dm = ttk.Button(
                self.buttons_frame,
                text=f'Выгрузить ДМ ({len(dm)})',
                command=lambda: self.export_data(dm, 'ДМ')
            )
            self.btn_dm.pack(side='left', padx=5)
            
        elif data_type == 'pallets_kiga':
            self.type_label.config(text='Тип паллеты и кигу')
            
            columns = ('num', 'first', 'len1', 'second', 'len2')
            first_heading, second_heading = 'Паллеты', 'Кигу'
            
            pallets = self.parsed_data['pallets']
            kiga = self.parsed_data['kiga']
            
            self._create_tree(columns, first_heading, second_heading)
            self._update_preview(pallets, kiga)
            
            self.btn_pallets = ttk.Button(
                self.buttons_frame,
                text=f'Выгрузить паллеты ({len(pallets)})',
                command=lambda: self.export_data(pallets, 'Паллеты')
            )
            self.btn_pallets.pack(side='left', padx=5)
            
            self.btn_kiga = ttk.Button(
                self.buttons_frame,
                text=f'Выгрузить кигу ({len(kiga)})',
                command=lambda: self.export_data(kiga, 'Кигу')
            )
            self.btn_kiga.pack(side='left', padx=5)
    
    def _create_tree(self, columns, first_heading, second_heading):
        self.tree = ttk.Treeview(self.preview_frame, columns=columns, show='headings', height=15)
        
        self.tree.heading('num', text='#')
        self.tree.heading('first', text=first_heading)
        self.tree.heading('len1', text='Длина')
        self.tree.heading('second', text=second_heading)
        self.tree.heading('len2', text='Длина')
        
        self.tree.column('num', width=40, anchor='center')
        self.tree.column('first', width=250)
        self.tree.column('len1', width=60, anchor='center')
        self.tree.column('second', width=250)
        self.tree.column('len2', width=60, anchor='center')
        
        scrollbar = ttk.Scrollbar(self.preview_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def _update_preview(self, first_list, second_list):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        max_len = max(len(first_list), len(second_list))
        
        for i in range(max_len):
            first_val = first_list[i] if i < len(first_list) else ''
            first_len = len(first_list[i]) if i < len(first_list) else ''
            second_val = second_list[i] if i < len(second_list) else ''
            second_len = len(second_list[i]) if i < len(second_list) else ''
            
            self.tree.insert('', 'end', values=(i + 1, first_val, first_len, second_val, second_len))
        
        self.count_label.config(text=f'Записей: {max_len}')
    
    def export_data(self, data_list, data_type):
        if not data_list:
            messagebox.showerror('Ошибка', f'{data_type} отсутствуют')
            return
        
        output_path = filedialog.asksaveasfilename(
            title='Сохранить как',
            defaultextension='.xlsx',
            filetypes=[('Excel files', '*.xlsx'), ('All files', '*.*')]
        )
        if not output_path:
            return
        
        try:
            generate_xlsx(data_list, output_path)
            messagebox.showinfo('Готово', f'Файл сохранён.\n{data_type}: {len(data_list)}')
        
        except Exception as e:
            messagebox.showerror('Ошибка', str(e))
