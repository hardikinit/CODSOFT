import tkinter as tk
from tkinter import messagebox
import random
import string
import platform

IS_MAC = platform.system() == "Darwin"

LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

BG = "#f5f4f0"
CARD = "#ffffff"
TEXT = "#1a1a2e"
ACCENT = "#3a86ff"
GREEN = "#38b000"
ORANGE = "#f48c06"
RED = "#d62828"
MUTED = "#8a8a8a"
BORDER = "#ddd"


def generate():
    length = int(slider.get())

    pool = ""
    required = []
    if var_lower.get():
        pool += LOWER
        required.append(random.choice(LOWER))
    if var_upper.get():
        pool += UPPER
        required.append(random.choice(UPPER))
    if var_digits.get():
        pool += DIGITS
        required.append(random.choice(DIGITS))
    if var_symbols.get():
        pool += SYMBOLS
        required.append(random.choice(SYMBOLS))

    if not pool:
        messagebox.showwarning("Oops", "Pick at least one character type.")
        return
    if length < len(required):
        messagebox.showwarning("Too short", "Increase the length to fit all selected types.")
        return

    rest = [random.choice(pool) for _ in range(length - len(required))]
    chars = required + rest
    random.shuffle(chars)
    pwd = "".join(chars)

    pwd_var.set(pwd)
    show_strength(pwd)


def show_strength(pwd):
    score = 0
    if any(c.islower() for c in pwd): score += 1
    if any(c.isupper() for c in pwd): score += 1
    if any(c.isdigit() for c in pwd): score += 1
    if any(c in SYMBOLS for c in pwd): score += 1
    if len(pwd) >= 12: score += 1
    if len(pwd) >= 16: score += 1

    bar_canvas.delete("all")
    w = bar_canvas.winfo_width()
    total = 6
    filled = score
    segment_w = (w - (total - 1) * 4) / total
    colors_map = {1: RED, 2: RED, 3: ORANGE, 4: ORANGE, 5: GREEN, 6: GREEN}
    fill_color = colors_map.get(filled, MUTED)

    for i in range(total):
        x = i * (segment_w + 4)
        c = fill_color if i < filled else "#e0e0e0"
        bar_canvas.create_rectangle(x, 0, x + segment_w, 10,
                                     fill=c, outline="", width=0)

    labels = {1: ("Weak", RED), 2: ("Weak", RED),
              3: ("Fair", ORANGE), 4: ("Fair", ORANGE),
              5: ("Strong", GREEN), 6: ("Strong", GREEN)}
    txt, col = labels.get(filled, ("–", MUTED))
    strength_lbl.config(text=f"Strength: {txt}", fg=col)


def copy_pwd():
    pwd = pwd_var.get()
    if not pwd:
        messagebox.showinfo("Nothing here", "Generate a password first.")
        return
    try:
        import pyperclip
        pyperclip.copy(pwd)
    except Exception:
        root.clipboard_clear()
        root.clipboard_append(pwd)
        root.update()
    messagebox.showinfo("Copied!", "Password copied to clipboard.")


def update_len_lbl(val):
    len_lbl.config(text=str(int(float(val))))


# ── window ──────────────────────────────────────────────────────
root = tk.Tk()
root.title("Password Generator")
root.geometry("420x470")
root.resizable(False, False)
root.configure(bg=BG)

tk.Label(root, text="Password Generator", font=("Georgia", 18, "bold"),
         bg=BG, fg=TEXT).pack(pady=(22, 2))
tk.Label(root, text="Make strong passwords in seconds",
         font=("Helvetica", 10), bg=BG, fg=MUTED).pack()

# length
len_frame = tk.Frame(root, bg=BG)
len_frame.pack(pady=18)
tk.Label(len_frame, text="Length:", font=("Helvetica", 12), bg=BG, fg=TEXT).grid(row=0, column=0, padx=6)
slider = tk.Scale(len_frame, from_=6, to=32, orient=tk.HORIZONTAL,
                  length=210, bg=BG, fg=TEXT,
                  highlightthickness=0, troughcolor="#d8d8d8",
                  activebackground=ACCENT, sliderrelief="flat",
                  command=update_len_lbl, showvalue=False, bd=0)
slider.set(16)
slider.grid(row=0, column=1, padx=6)
len_lbl = tk.Label(len_frame, text="16", font=("Helvetica", 13, "bold"),
                   width=3, bg=BG, fg=ACCENT)
len_lbl.grid(row=0, column=2)

# options box (drawn manually for cross-platform look)
opts_frame = tk.LabelFrame(root, text="  Include  ", font=("Helvetica", 10),
                            bg=BG, fg=MUTED, bd=1, relief="groove",
                            padx=18, pady=10)
opts_frame.pack(padx=30, pady=(0, 4))

var_lower = tk.IntVar(value=1)
var_upper = tk.IntVar(value=1)
var_digits = tk.IntVar(value=1)
var_symbols = tk.IntVar(value=0)

chk = {"bg": BG, "fg": TEXT, "font": ("Helvetica", 11),
       "activebackground": BG, "activeforeground": TEXT,
       "selectcolor": ACCENT if not IS_MAC else BG,
       "anchor": "w"}

tk.Checkbutton(opts_frame, text="Lowercase  (a–z)", variable=var_lower, **chk).grid(row=0, column=0, sticky="w")
tk.Checkbutton(opts_frame, text="Uppercase  (A–Z)", variable=var_upper, **chk).grid(row=0, column=1, sticky="w", padx=20)
tk.Checkbutton(opts_frame, text="Numbers    (0–9)", variable=var_digits, **chk).grid(row=1, column=0, sticky="w", pady=4)
tk.Checkbutton(opts_frame, text="Symbols    (!@#…)", variable=var_symbols, **chk).grid(row=1, column=1, sticky="w", padx=20, pady=4)

# generate button (uses Canvas for cross-platform color)
def make_btn(parent, text, bg, hover_bg, cmd):
    f = tk.Frame(parent, bg=bg, cursor="hand2")
    lbl = tk.Label(f, text=text, font=("Helvetica", 13, "bold"),
                   bg=bg, fg="white", padx=24, pady=8)
    lbl.pack()
    for w in (f, lbl):
        w.bind("<Enter>", lambda e: [f.config(bg=hover_bg), lbl.config(bg=hover_bg)])
        w.bind("<Leave>", lambda e: [f.config(bg=bg), lbl.config(bg=bg)])
        w.bind("<Button-1>", lambda e: cmd())
    return f

make_btn(root, "Generate Password", ACCENT, "#2476ee", generate).pack(pady=16)

# result
result_frame = tk.Frame(root, bg=BG)
result_frame.pack()

pwd_var = tk.StringVar()
pwd_entry = tk.Entry(result_frame, textvariable=pwd_var, font=("Courier", 13),
                     width=22, justify="center", bd=0,
                     highlightthickness=2, highlightbackground=BORDER,
                     highlightcolor=ACCENT, fg=TEXT, bg=CARD,
                     state="readonly", readonlybackground=CARD,
                     insertbackground=TEXT)
pwd_entry.pack(side=tk.LEFT, ipady=6, padx=(0, 6))

make_btn(result_frame, "Copy", GREEN, "#2e9900", copy_pwd).pack(side=tk.LEFT)

# strength bar
bar_canvas = tk.Canvas(root, height=12, bg=BG, bd=0, highlightthickness=0)
bar_canvas.pack(fill=tk.X, padx=60, pady=(12, 2))

strength_lbl = tk.Label(root, text="", font=("Helvetica", 10, "bold"), bg=BG, fg=MUTED)
strength_lbl.pack()

root.mainloop()