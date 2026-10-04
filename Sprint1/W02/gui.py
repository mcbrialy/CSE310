"""A simple graphical user interface using Tkinter."""

import tkinter as tk
from tkinter import messagebox


def greet_user():
    """Display a personalized greeting using the form values."""
    name = name_entry.get().strip()
    age_text = age_entry.get().strip()

    if not name:
        messagebox.showerror("Input Error", "Please enter your name.")
        return

    try:
        age = int(age_text)
        if age < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Input Error", "Please enter a whole number for your age."
        )
        return

    result_label.config(text=f"Hello, {name}! You are {age} years old.")


window = tk.Tk()
window.title("Prompt GUI")
window.geometry("350x220")
window.resizable(False, False)

title_label = tk.Label(window, text="Welcome to the GUI prompt program!", pady=10)
title_label.pack()

form_frame = tk.Frame(window)
form_frame.pack(pady=5)

tk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
name_entry = tk.Entry(form_frame, width=25)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Age:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
age_entry = tk.Entry(form_frame, width=25)
age_entry.grid(row=1, column=1, padx=5, pady=5)

greet_button = tk.Button(window, text="Submit", command=greet_user)
greet_button.pack(pady=8)

result_label = tk.Label(window, text="", wraplength=300)
result_label.pack(pady=5)

name_entry.focus()
window.mainloop()
