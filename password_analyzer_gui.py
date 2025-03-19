import re
import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Function to check password length
def check_length(password):
    return len(password) >= 8

# Function to check password complexity
def check_complexity(password):
    return (re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'[0-9]', password) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

# Function to check against common passwords
def check_common_passwords(password):
    common_passwords = ["123456", "password", "qwerty", "admin"]
    return password not in common_passwords

# Function to calculate entropy
def calculate_entropy(password):
    charset_size = 94  # Total possible characters (letters, numbers, symbols)
    length = len(password)
    return length * math.log2(charset_size)

# Function to analyze password strength
def analyze_password_strength(password):
    if not password:
        return "Please enter a password.", 0, "black"

    if not check_length(password):
        return "Password is too short. Use at least 8 characters.", 25, "red"
    if not check_complexity(password):
        return "Password is weak. Include uppercase, lowercase, numbers, and special characters.", 50, "orange"
    if not check_common_passwords(password):
        return "Password is too common. Choose a more unique password.", 50, "orange"

    entropy = calculate_entropy(password)
    if entropy < 50:
        return f"Password is moderate. Entropy: {entropy:.2f} bits", 75, "orange"
    else:
        return f"Password is strong! Entropy: {entropy:.2f} bits", 100, "green"

# Function to handle button click
def on_analyze_click():
    password = password_entry.get()
    result, strength, color = analyze_password_strength(password)
    result_label.config(text=result, fg=color)
    progress_bar["value"] = strength
    root.update_idletasks()

# Function to save results to a file
def save_results():
    result = result_label.cget("text")
    if not result:
        messagebox.showwarning("Save Error", "No results to save.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(result)
        messagebox.showinfo("Save Successful", f"Results saved to {file_path}")

# Create the main window
root = tk.Tk()
root.title("Password Strength Analyzer")

# Create and place widgets
tk.Label(root, text="Enter your password:").pack(pady=5)
password_entry = tk.Entry(root, show="*", width=40)
password_entry.pack(pady=5)

analyze_button = tk.Button(root, text="Analyze Password", command=on_analyze_click)
analyze_button.pack(pady=10)

# Progress bar to indicate password strength
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=5)

# Label to display result
result_label = tk.Label(root, text="", fg="black")
result_label.pack(pady=10)

# Button to save results
save_button = tk.Button(root, text="Save Results", command=save_results)
save_button.pack(pady=10)

# Run the application
root.mainloop()