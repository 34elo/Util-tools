import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from processor import read, generate
from config import DEFAULTS


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('XML Transform')
        self.root.geometry('1200x900')
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(True, True)

        self.xml_path = None
        self.data = None
        self.input_values = []

        main_frame = ttk.Frame(root, padding='20')
        main_frame.pack(fill='both', expand=True)

        file_frame = ttk.LabelFrame(
            main_frame,
            text='Выберите .xml файл',
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

        columns = ('#', 'pack_code', 'cis_count')
        self.tree = ttk.Treeview(preview_frame, columns=columns, show='headings', height=8)

        self.tree.heading('#', text='#')
        self.tree.heading('pack_code', text='Pack Code')
        self.tree.heading('cis_count', text='Кол-во CIS')

        self.tree.column('#', width=50, anchor='center')
        self.tree.column('pack_code', width=300)
        self.tree.column('cis_count', width=100, anchor='center')

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
        
        unit_pack_frame = ttk.LabelFrame(params_frame, text='Unit Pack', padding='5')
        unit_pack_frame.pack(fill='x', pady=3)
        
        for label in ['document_id', 'VerForm', 'file_date_time', 'VerProg']:
            row = ttk.Frame(unit_pack_frame)
            row.pack(fill='x', pady=2)
            ttk.Label(row, text=f'{label}:', width=18).pack(side='left')
            entry = ttk.Entry(row, width=40)
            entry.insert(0, DEFAULTS.get(label, ''))
            entry.pack(side='left', padx=5, fill='x', expand=True)
            self.entries[label] = entry

        document_frame = ttk.LabelFrame(params_frame, text='Document', padding='5')
        document_frame.pack(fill='x', pady=3)
        
        for label in ['operation_date_time', 'document_number']:
            row = ttk.Frame(document_frame)
            row.pack(fill='x', pady=2)
            ttk.Label(row, text=f'{label}:', width=18).pack(side='left')
            entry = ttk.Entry(row, width=40)
            entry.insert(0, DEFAULTS.get(label, ''))
            entry.pack(side='left', padx=5, fill='x', expand=True)
            self.entries[label] = entry

        organisation_frame = ttk.LabelFrame(params_frame, text='Organisation', padding='5')
        organisation_frame.pack(fill='x', pady=3)
        
        for label in ['org_name', 'LP_TIN', 'RRC', 'country_code', 'text_address', 'phone_number', 'email']:
            row = ttk.Frame(organisation_frame)
            row.pack(fill='x', pady=2)
            ttk.Label(row, text=f'{label}:', width=18).pack(side='left')
            entry = ttk.Entry(row, width=40)
            entry.insert(0, DEFAULTS.get(label, ''))
            entry.pack(side='left', padx=5, fill='x', expand=True)
            self.entries[label] = entry

        self.save_btn = ttk.Button(
            main_frame, text='Сохранить как .xml',
            command=self.save_file
        )
        self.save_btn.pack(pady=5)

    def select_file(self):
        path = filedialog.askopenfilename(
            title='Выберите .xml файл',
            filetypes=[('XML files', '*.xml'), ('All files', '*.*')]
        )
        if path:
            self.xml_path = path
            self.file_label.config(text=os.path.basename(path))

            try:
                self.data = read(path)
                self.update_preview()
            except Exception as e:
                messagebox.showerror('Ошибка', f'Не удалось прочитать файл:\n{e}')
                self.file_label.config(text='Ошибка чтения', foreground='red')

    def update_preview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, pack in enumerate(self.data.get('pack_contents', []), 1):
            pack_code = pack.get('pack_code', '')
            cis_count = len(pack.get('cis', []))
            self.tree.insert('', 'end', values=(i, pack_code, cis_count))

        self.count_label.config(text=f'Записей: {len(self.data.get("pack_contents", []))}')

    def save_file(self):
        if not self.xml_path:
            messagebox.showerror('Ошибка', 'Сначала выберите .xml файл')
            return

        if not self.data:
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
            unit_pack_attrs = {
                'document_id': self.entries['document_id'].get(),
                'VerForm': self.entries['VerForm'].get(),
                'file_date_time': self.entries['file_date_time'].get(),
                'VerProg': self.entries['VerProg'].get(),
            }
            
            document_attrs = {
                'operation_date_time': self.entries['operation_date_time'].get(),
                'document_number': self.entries['document_number'].get(),
            }
            
            organisation = {
                'LP_info': {
                    'org_name': self.entries['org_name'].get(),
                    'LP_TIN': self.entries['LP_TIN'].get(),
                    'RRC': self.entries['RRC'].get(),
                },
                'address': {
                    'country_code': self.entries['country_code'].get(),
                    'text_address': self.entries['text_address'].get(),
                },
                'contacts': {
                    'phone_number': self.entries['phone_number'].get(),
                    'email': self.entries['email'].get(),
                },
            }

            content = generate(self.data, unit_pack_attrs, document_attrs, organisation)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            messagebox.showinfo('Готово', f'Файл сохранён.\nЗаписей: {len(self.data.get("pack_contents", []))}')

        except Exception as e:
            messagebox.showerror('Ошибка', str(e))
