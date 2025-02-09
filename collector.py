import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk

def gather_directory_content(root_dir):
    """Walks through a directory and returns its contents."""
    output = ""
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root_dir)  # Get relative path

            output += f"Relative Path: {rel_path}\n"

            try:
                with open(filepath, "r") as infile:
                    content = infile.read()
                    output += f"Content:\n{content}\n\n"  # Add separator
            except (UnicodeDecodeError, PermissionError):
                output += "Content: (Binary or inaccessible file)\n\n"
    
    return output

def select_directory():
    global selected_directory
    directory = filedialog.askdirectory()
    if directory:
        selected_directory = directory  # Save the selected directory globally
        update_output()

def update_output():
    global selected_directory
    if selected_directory:
        result = gather_directory_content(selected_directory)
        text_output.delete(1.0, tk.END)  # Clear previous content
        text_output.insert(tk.END, result)

def copy_to_clipboard():
    content = text_output.get(1.0, tk.END)
    root.clipboard_clear()
    root.clipboard_append(content)

def save_to_file():
    content = text_output.get(1.0, tk.END)
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if save_path:
        with open(save_path, "w") as outfile:
            outfile.write(content)

# Set up the GUI
root = tk.Tk()
root.title("Directory Content Collector")

# Global variable to store selected directory
selected_directory = None

# Configure the style
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 14))
style.configure("TFrame", padding=20)

frame = ttk.Frame(root)
frame.pack(padx=20, pady=20)

label = ttk.Label(frame, text="Select a directory to display its contents:")
label.pack(pady=10)

text_output = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20, font=("Helvetica", 10))
text_output.pack(pady=10)

# Create the menu bar
menu_bar = tk.Menu(root)

# Create the file menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Select Directory", command=select_directory)
file_menu.add_command(label="Update", command=update_output)
file_menu.add_separator()
file_menu.add_command(label="Copy to Clipboard", command=copy_to_clipboard)
file_menu.add_command(label="Save to File", command=save_to_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Add the file menu to the menu bar
menu_bar.add_cascade(label="File", menu=file_menu)

# Configure the root window to display the menu bar
root.config(menu=menu_bar)

root.mainloop()
