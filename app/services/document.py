import tkinter as tk
from tkinter import filedialog


class Document:
    @staticmethod
    def select(how_many: int = 1) -> list[str]:
        new_existing_file_count = how_many
        existing_file_paths = []

        root = tk.Tk()
        root.withdraw()
        while new_existing_file_count > 0:
            existing_file_path = filedialog.askopenfilename()
            existing_file_paths.append(existing_file_path)
            new_existing_file_count -= 1
    
        return existing_file_paths
