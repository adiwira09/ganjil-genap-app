import pandas as pd
import tkinter as tk
from tkinter import ttk

def load_excel_data(frame, file_path):
    try:
        data = pd.read_excel(file_path)
        tree = ttk.Treeview(frame, columns=list(data.columns), show="headings")

        column_widths = {
            "No": 50,
            "Frame": 80,
            "Text Plate": 200,
            "Keterangan": 150
        }

        for col in data.columns:
            tree.heading(col, text=col)
            tree.column(col, minwidth=50, width=column_widths.get(col, 100), anchor="center")

        for index, row in data.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(fill="both", expand=True)

    except Exception as e:
        error_label = tk.Label(frame, text=f"Error loading file: {e}", fg="red")
        error_label.pack()