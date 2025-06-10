import tkinter as tk
from tkinter import ttk
import re

common_passwords = ['123456', 'password', 'qwerty', 'admin', 'letmein', 'abc123', 'iloveyou']

# --- ANALYZE PASSWORD ---
def analyze_password(password):
    score = 0
    suggestions = []

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        suggestions.append("❌ Use at least 12 characters.")

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        suggestions.append("❌ Add uppercase letters.")
    
    if re.search(r'[a-z]', password):
        score += 1
    else:
        suggestions.append("❌ Add lowercase letters.")
    
    if re.search(r'[0-9]', password):
        score += 1
    else:
        suggestions.append("❌ Include numbers.")
    
    if re.search(r'[^A-Za-z0-9]', password):
        score += 1
    else:
        suggestions.append("❌ Include special characters.")

    if password.lower() in common_passwords:
        suggestions.append("❌ Avoid common passwords like '123456', 'qwerty'.")
        score = 1

    if score >= 6:
        return "✅ Strong", suggestions, "#28a745", 100
    elif score >= 4:
        return "⚠️ Moderate", suggestions, "#ffc107", 60
    else:
        return "❌ Weak", suggestions, "#dc3545", 30

# --- ON PASSWORD CHANGE ---
def on_password_change(event=None):
    password = entry.get()
    strength, tips, color, percent = analyze_password(password)

    result_label.config(text=strength, fg=color)
    style.configure("green.Horizontal.TProgressbar", foreground=color, background=color)
    strength_bar["value"] = percent

    suggestions_text.config(state='normal')
    suggestions_text.delete("1.0", tk.END)
    if tips:
        for tip in tips:
            suggestions_text.insert(tk.END, f"{tip}\n")
    else:
        suggestions_text.insert(tk.END, "✅ Your password is strong.")
    suggestions_text.config(state='disabled')

# --- TOGGLE PASSWORD VISIBILITY ---
def toggle_password():
    if entry.cget('show') == '':
        entry.config(show='*')
        toggle_btn.config(text="👁 Show")
    else:
        entry.config(show='')
        toggle_btn.config(text="🙈 Hide")

# --- GUI SETUP ---
root = tk.Tk()
root.title("💡 Password Analyzer Pro")
root.geometry("550x500")
root.config(bg="#1a1c2c")
root.resizable(False, False)

# --- Fonts and Styles ---
style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", background="#1a1c2c", foreground="white", font=('Segoe UI', 12))
style.configure("TButton", font=('Segoe UI', 10))
style.configure("green.Horizontal.TProgressbar", troughcolor='#2e2f3e', bordercolor='#2e2f3e', background='#28a745', lightcolor='#28a745', darkcolor='#28a745')

# --- UI ELEMENTS ---
title = tk.Label(root, text="🔐 Password Strength Analyzer", font=('Segoe UI Semibold', 16), bg="#1a1c2c", fg="white")
title.pack(pady=(20, 10))

frame = tk.Frame(root, bg="#1a1c2c")
frame.pack()

entry = tk.Entry(frame, width=30, font=('Consolas', 12), show='*', relief="solid", bd=2, bg="#e7e7e7")
entry.pack(side="left", padx=10)
entry.bind("<KeyRelease>", on_password_change)

toggle_btn = tk.Button(frame, text="👁 Show", command=toggle_password, font=('Segoe UI', 9), bg="#3a3a4f", fg="white", relief="flat")
toggle_btn.pack(side="left")

result_label = tk.Label(root, text="", font=('Segoe UI Bold', 14), bg="#1a1c2c")
result_label.pack(pady=(15, 5))

strength_bar = ttk.Progressbar(root, style="green.Horizontal.TProgressbar", length=300, mode='determinate')
strength_bar.pack(pady=(0, 15))

tk.Label(root, text="💡 Suggestions:", font=('Segoe UI Semibold', 12), bg="#1a1c2c", fg="white").pack(pady=(10, 0))

suggestions_text = tk.Text(root, height=6, width=60, font=('Segoe UI', 10), bg="#2c2e3e", fg="white", relief="flat", state='disabled', wrap='word')
suggestions_text.pack(pady=10)

footer = tk.Label(root, text="Tip: Use a mix of 3+ character types & avoid names, dates, or patterns", font=('Segoe UI', 9), fg="#aaa", bg="#1a1c2c")
footer.pack(pady=(10, 0))

root.mainloop()
