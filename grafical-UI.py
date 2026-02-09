import tkinter as tk
from tkinter import ttk
import os
import sys
import subprocess

APP_FOLDER = "app"

def summarize_text(text) -> str :
     input_path = os.path.join(APP_FOLDER, "input.txt")
     summary_path = os.path.join(APP_FOLDER, "summary.txt")

     #craete input.txt file
     with open(input_path, "w", encoding="utf-8") as f:
          f.write(text)

     # remove old files of Embedding
     for file_name in ["sentences.json", "embedded.npy"]:
          path = os.path.join(APP_FOLDER, file_name)
          if os.path.exists(path):
               os.remove(path)

     # remove old summary.txt file
     if os.path.exists(summary_path):
          os.remove(summary_path)


     VENV_python = sys.executable

     # run embed_sentences.py and main.py
     subprocess.run([VENV_python, os.path.join(APP_FOLDER, "embed_sentences.py"), input_path], check=True)
     subprocess.run([VENV_python, os.path.join(APP_FOLDER, "main.py"), input_path], check = True)

     # read new summary.txt
     with open(summary_path, "r", encoding="utf-8") as f:
          summary = f.read()

     return summary





# ====== GUI LOGIC ======
def on_summarize():
    input_text = input_textbox.get("1.0", tk.END).strip()

    if not input_text:
        output_textbox.delete("1.0", tk.END)
        output_textbox.insert(tk.END, "⚠️ Please enter some text to summarize.")
        return

    summary = summarize_text(input_text)

    output_textbox.delete("1.0", tk.END)
    output_textbox.insert(tk.END, summary)


# ====== MAIN WINDOW ======
root = tk.Tk()
root.title("Text Summarizer")
root.geometry("900x600")
root.resizable(False, False)

# ====== STYLE ======
style = ttk.Style()
style.theme_use("clam")

# ====== INPUT LABEL ======
input_label = ttk.Label(root, text="Input Text", font=("Segoe UI", 11, "bold"))
input_label.pack(anchor="w", padx=20, pady=(15, 5))

# ====== INPUT TEXT AREA ======
input_frame = ttk.Frame(root)
input_frame.pack(fill="both", expand=True, padx=20)

input_scroll = ttk.Scrollbar(input_frame)
input_scroll.pack(side="right", fill="y")

input_textbox = tk.Text(
    input_frame,
    height=10,
    font=("Segoe UI", 10),
    wrap="word",
    yscrollcommand=input_scroll.set
)
input_textbox.pack(fill="both", expand=True)

input_scroll.config(command=input_textbox.yview)

# ====== BUTTON ======
summarize_btn = ttk.Button(
    root,
    text="Summarize It",
    command=on_summarize
)
summarize_btn.pack(pady=15)

# ====== OUTPUT LABEL ======
output_label = ttk.Label(root, text="Summary", font=("Segoe UI", 11, "bold"))
output_label.pack(anchor="w", padx=20, pady=(5, 5))

# ====== OUTPUT TEXT AREA ======
output_frame = ttk.Frame(root)
output_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

output_scroll = ttk.Scrollbar(output_frame)
output_scroll.pack(side="right", fill="y")

output_textbox = tk.Text(
    output_frame,
    height=8,
    font=("Segoe UI", 10),
    wrap="word",
    bg="#f5f5f5",
    state="normal",
    yscrollcommand=output_scroll.set
)
output_textbox.pack(fill="both", expand=True)

output_scroll.config(command=output_textbox.yview)

# ====== START APP ======
root.mainloop()
