import pandas as pd
from tkinter import ttk

def load_csv_data(frame, file_path, interval=1000):
    # Inisialisasi Treeview
    columns = ["Track ID", "Text Plate", "Date", "Keterangan"]
    tree = ttk.Treeview(frame, columns=columns, show="headings")

    # Set heading dan lebar kolom
    column_widths = {
        "Track ID": 50,
        "Text Plate": 80,
        "Date": 70,
        "Keterangan": 300
    }
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, minwidth=50, width=column_widths.get(col, 100), anchor="center")

    tree.pack(fill="both", expand=True)

    def update_csv_data():
        """Membaca ulang data dari file CSV dan memperbarui Treeview."""
        try:
            data = pd.read_csv(file_path)

            # Hapus data lama di Treeview
            for item in tree.get_children():
                tree.delete(item)

            # Tambahkan data baru dari CSV
            for index, row in data.iterrows():
                tree.insert("", "end", values=list(row[columns]))

        except Exception as e:
            print(f"Error updating Treeview: {e}")

        # Jadwalkan pembaruan berikutnya
        frame.after(interval, update_csv_data)

    # Jalankan pembaruan pertama kali
    update_csv_data()