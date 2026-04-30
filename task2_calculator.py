import tkinter as tk
from tkinter import messagebox
import platform

IS_MAC = platform.system() == "Darwin"

# Colors
BG = "#1c1c28"
DISPLAY_BG = "#13131f"
BTN_NUM = "#2a2a3e"
BTN_OP = "#e8a838"
BTN_EQ = "#5c6fe0"
BTN_CLR = "#d14f4f"
BTN_HOVER_NUM = "#3a3a55"
BTN_HOVER_OP = "#f0b848"
BTN_HOVER_EQ = "#7080f0"
BTN_HOVER_CLR = "#e06060"
FG = "#ffffff"
DISPLAY_FG = "#e8e8f0"

expression = ""
just_evaluated = False


def update_display(text):
    display_canvas.delete("all")
    display_canvas.create_text(
        display_canvas.winfo_width() - 16, 45,
        text=text if text else "0",
        fill=DISPLAY_FG,
        font=("Courier", 28, "bold"),
        anchor="e"
    )


def btn_press(val):
    global expression, just_evaluated
    if just_evaluated:
        if val in "0123456789.":
            expression = ""
        just_evaluated = False
    expression += str(val)
    update_display(expression)


def do_clear():
    global expression, just_evaluated
    expression = ""
    just_evaluated = False
    update_display("")


def do_backspace():
    global expression, just_evaluated
    just_evaluated = False
    expression = expression[:-1]
    update_display(expression)


def do_equals():
    global expression, just_evaluated
    if not expression:
        return
    try:
        result = eval(expression)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        expression = str(result)
        just_evaluated = True
        update_display(expression)
    except ZeroDivisionError:
        update_display("Div/0 Error")
        expression = ""
        just_evaluated = False
    except Exception:
        update_display("Error")
        expression = ""
        just_evaluated = False


def make_button(parent, text, row, col, bg, hover_bg, cmd, colspan=1):
    frame = tk.Frame(parent, bg=bg, cursor="hand2")
    frame.grid(row=row, column=col, columnspan=colspan,
               padx=4, pady=4, sticky="nsew")

    lbl = tk.Label(frame, text=text, font=("Helvetica", 17, "bold"),
                   bg=bg, fg=FG)
    lbl.pack(expand=True, fill=tk.BOTH, ipady=13)

    def on_enter(e):
        frame.config(bg=hover_bg)
        lbl.config(bg=hover_bg)

    def on_leave(e):
        frame.config(bg=bg)
        lbl.config(bg=bg)

    def on_click(e):
        cmd()

    frame.bind("<Enter>", on_enter)
    frame.bind("<Leave>", on_leave)
    frame.bind("<Button-1>", on_click)
    lbl.bind("<Enter>", on_enter)
    lbl.bind("<Leave>", on_leave)
    lbl.bind("<Button-1>", on_click)

    return frame


# ── window ──────────────────────────────────────────────────────
root = tk.Tk()
root.title("Calculator")
root.geometry("340x500")
root.resizable(False, False)
root.configure(bg=BG)

# display
display_canvas = tk.Canvas(root, bg=DISPLAY_BG, height=80,
                            bd=0, highlightthickness=0)
display_canvas.pack(fill=tk.X, padx=12, pady=(14, 8))
display_canvas.bind("<Configure>", lambda e: update_display(expression or ""))

# grid
grid = tk.Frame(root, bg=BG)
grid.pack(padx=12, pady=(0, 12), fill=tk.BOTH, expand=True)
for c in range(4):
    grid.columnconfigure(c, weight=1)
for r in range(5):
    grid.rowconfigure(r, weight=1)

layout = [
    [("C", BTN_CLR, BTN_HOVER_CLR, do_clear),
     ("←", BTN_CLR, BTN_HOVER_CLR, do_backspace),
     ("%", BTN_OP, BTN_HOVER_OP, lambda: btn_press("%")),
     ("÷", BTN_OP, BTN_HOVER_OP, lambda: btn_press("/"))],

    [("7", BTN_NUM, BTN_HOVER_NUM, lambda: btn_press("7")),
     ("8", BTN_NUM, BTN_HOVER_NUM, lambda: btn_press("8")),
     ("9", BTN_NUM, BTN_HOVER_NUM, lambda: btn_press("9")),
     ("×", BTN_OP, BTN_HOVER_OP, lambda: btn_press("*"))],

    [("4", BTN_NUM, BTN_HOVER_NUM, lambda: btn_press("4")),
     ("5", BTN_NUM, BTN_HOVER_NUM, lambda: btn_press("5")),
     ("6", BTN_NUM, BTN_HOVER_NUM, lambda: btn_press("6")),
     ("−", BTN_OP, BTN_HOVER_OP, lambda: btn_press("-"))],

    [("1", BTN_NUM, BTN_HOVER_NUM, lambda: btn_press("1")),
     ("2", BTN_NUM, BTN_HOVER_NUM, lambda: btn_press("2")),
     ("3", BTN_NUM, BTN_HOVER_NUM, lambda: btn_press("3")),
     ("+", BTN_OP, BTN_HOVER_OP, lambda: btn_press("+"))],

    [("0", BTN_NUM, BTN_HOVER_NUM, lambda: btn_press("0")),
     ("00", BTN_NUM, BTN_HOVER_NUM, lambda: btn_press("00")),
     (".", BTN_NUM, BTN_HOVER_NUM, lambda: btn_press(".")),
     ("=", BTN_EQ, BTN_HOVER_EQ, do_equals)],
]

for r, row in enumerate(layout):
    for c, (txt, bg, hbg, cmd) in enumerate(row):
        make_button(grid, txt, r, c, bg, hbg, cmd)


def key_press(event):
    key = event.char
    if key in "0123456789.+-*/%":
        btn_press(key)
    elif key in ("=", "\r"):
        do_equals()
    elif key == "\x08":
        do_backspace()
    elif key.lower() == "c":
        do_clear()


root.bind("<Key>", key_press)
root.after(50, lambda: update_display(""))
root.mainloop()