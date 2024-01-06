import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk, scrolledtext

def new_file(window, text_edit, status):
    text_edit.delete("1.0", tk.END)
    window.title("New File")
    status.config(text="Current file: None")

def open_file(window, text_edit, status):
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not filepath:
        return
    text_edit.delete("1.0", tk.END)
    with open(filepath, "r") as f:
        content = f.read()
        text_edit.insert(tk.END, content)
    window.title(f"Open File: {filepath}")
    status.config(text=f"Current file: {filepath}")

def save_file(window, text_edit, status):
    filepath = asksaveasfilename(filetypes=[("Text Files", "*.txt")])
    if not filepath:
        return
    with open(filepath, "w") as f:
        content = text_edit.get(1.0, tk.END)
        f.write(content)
    window.title(f"Open File:{filepath}")
    status.config(text=f"Current file: {filepath}")

def find_text(window, text_edit):
    find_string = tk.simpledialog.askstring("Find...", "Enter text")
    text_edit.tag_remove('found', '1.0', tk.END)
    if find_string:
        idx = '1.0'
        while True:
            idx = text_edit.search(find_string, idx, nocase=1, stopindex=tk.END)
            if not idx: break
            lastidx = '%s+%dc' % (idx, len(find_string))
            text_edit.tag_add('found', idx, lastidx)
            idx = lastidx
        text_edit.tag_config('found', foreground='red')

def main():
    window = tk.Tk()
    window.title("Text Editor")
    window.rowconfigure(0, minsize=400, weight=1)
    window.columnconfigure(1, minsize=800, weight=1)

    frame = tk.Frame(window, relief=tk.RAISED, bd = 2)
    frame.grid(row = 0, column=0, sticky="ns")

    text_edit = scrolledtext.ScrolledText(window, font = "Calibri 18 bold italic", wrap = tk.WORD)
    text_edit.grid(row = 0, column=1, sticky="nsew", padx=5, pady=5)

    new_button = ttk.Button(frame, text="New", command=lambda: new_file(window, text_edit, status))
    new_button.grid(row=0, column=0, padx=7, pady=7, sticky="ew")

    open_button = ttk.Button(frame, text="Open", command=lambda: open_file(window, text_edit, status))
    open_button.grid(row=1, column=0, padx=7, pady=7, sticky="ew")

    save_button = ttk.Button(frame, text="Save", command=lambda: save_file(window, text_edit, status))
    save_button.grid(row=2, column=0, padx=7, pady=7, sticky="ew")

    find_button = ttk.Button(frame, text="Find", command=lambda: find_text(window, text_edit))
    find_button.grid(row=3, column=0, padx=7, pady=7, sticky="ew")

    status = tk.Label(window, text = "Current file: None", bd = 1, relief = tk.SUNKEN, anchor = tk.W)
    status.grid(row = 1, column = 0, columnspan = 2, sticky = "we")

    window.bind("<Control-n>", lambda event: new_file(window, text_edit, status))
    window.bind("<Control-o>", lambda event: open_file(window, text_edit, status))
    window.bind("<Control-s>", lambda event: save_file(window, text_edit, status))
    window.bind("<Control-f>", lambda event: find_text(window, text_edit))

    window.mainloop()   

main()