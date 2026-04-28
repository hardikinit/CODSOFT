import tkinter as tk
from tkinter import messagebox

# I tried doing this with just labels first but buttons felt better

expression = ""

def button_click(value):
    global expression
    expression += str(value)
    display_var.set(expression)

def clear_all():
    global expression
    expression = ""
    display_var.set("")

def backspace():
    global expression
    expression = expression[:-1]
    display_var.set(expression)

def calculate():
    global expression
    if not expression:
        return
    try:
        # eval is fine for a simple calculator like this
        result = eval(expression)
        # if result is a whole number, don't show .0
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        display_var.set(str(result))
        expression = str(result)
    except ZeroDivisionError:
        messagebox.showerror("Error", "Can't divide by zero!")
        clear_all()
    except Exception:
        messagebox.showerror("Error", "Invalid expression")
        clear_all()


root = tk.Tk()
root.title("Calculator")
root.geometry("340x480")
root.resizable(False, False)
root.configure(bg="#1e1e2e")

display_var = tk.StringVar()

# display screen
display_frame = tk.Frame(root, bg="#1e1e2e", pady=15)
display_frame.pack(fill=tk.X, padx=15)

tk.Entry(display_frame, textvariable=display_var, font=("Consolas", 24),
         bd=0, relief="flat", bg="#2a2a3e", fg="black", justify="right",
         state="readonly", readonlybackground="#2a2a3e",
         insertbackground="black").pack(fill=tk.X, ipady=12, padx=5)

# button layout
buttons = [
    ["C", "←", "%", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["00", "0", ".", "="],
]

btn_frame = tk.Frame(root, bg="#1e1e2e")
btn_frame.pack(padx=15, pady=10)

for row_idx, row in enumerate(buttons):
    for col_idx, btn_text in enumerate(row):
        # pick colors based on type
        if btn_text == "=":
            bg_color = "#5e60ce"
            fg_color = "black"
        elif btn_text in ("C", "←"):
            bg_color = "#e74c3c"
            fg_color = "black"
        elif btn_text in ("/", "*", "-", "+", "%"):
            bg_color = "#f39c12"
            fg_color = "black"
        else:
            bg_color = "#2d2d44"
            fg_color = "black"

        def make_cmd(val):
            if val == "=":
                return calculate
            elif val == "C":
                return clear_all
            elif val == "←":
                return backspace
            else:
                return lambda v=val: button_click(v)

        tk.Button(btn_frame, text=btn_text, font=("Helvetica", 16, "bold"),
                  bg=bg_color, fg=fg_color, relief="flat",
                  width=5, height=2, bd=0, cursor="hand2",
                  activebackground="#444466", activeforeground="black",
                  command=make_cmd(btn_text)).grid(row=row_idx, column=col_idx,
                                                   padx=4, pady=4)

# keyboard support
def key_press(event):
    key = event.char
    if key in "0123456789.+-*/%" :
        button_click(key)
    elif key == "\r":
        calculate()
    elif key == "\x08":
        backspace()

root.bind("<Key>", key_press)

root.mainloop()
