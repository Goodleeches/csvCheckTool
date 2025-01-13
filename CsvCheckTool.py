import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import csv
import os
from PyInstaller.utils.hooks import collect_data_files
datas = collect_data_files('tkinterdnd2')

def check_csv(file_path):
    problem_lines = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for line_num, row in enumerate(reader, start=1):
            if all(cell == '' for cell in row):
                problem_lines.append(line_num)
    return problem_lines

def on_file_drop(event):
    file_paths = event.data
    file_paths = file_paths.replace("{", "").replace("}", "").split()  # Clean up and split file paths
    results = []
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        problem_lines = check_csv(file_path)
        if problem_lines:
            results.append(f"{file_name}:\n  Problematic lines: {problem_lines}")
        else:
            results.append(f"{file_name}:\n  Complete")
    messagebox.showinfo("Result", "\n\n".join(results))

def select_file():
    file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    if file_paths:
        results = []
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            problem_lines = check_csv(file_path)
            if problem_lines:
                results.append(f"{file_name}:\n  Problematic lines: {problem_lines}")
            else:
                results.append(f"{file_name}:\n  Complete")
        messagebox.showinfo("Result", "\n\n".join(results))

# GUI setup
root = TkinterDnD.Tk()
root.title("CSV Checker")

# Create a label
label = tk.Label(root, text="Drag and drop CSV files here or click to select", width=50, height=10, bg="lightgray")
label.pack(pady=20)

# Bind the drag and drop event
label.drop_target_register(DND_FILES)
label.dnd_bind('<<Drop>>', on_file_drop)

# Create a button to select file
button = tk.Button(root, text="Select Files", command=select_file)
button.pack(pady=10)

root.mainloop()
