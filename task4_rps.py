import tkinter as tk
import random
import platform

IS_MAC = platform.system() == "Darwin"

BG = "#ffffff"
TEXT = "#1a1a2e"
MUTED = "#9b9b9b"
WIN_COLOR = "#38b000"
LOSE_COLOR = "#d62828"
TIE_COLOR = "#f48c06"
SCORE_COLOR = "#3a86ff"
PANEL = "#f0f0f5"
BORDER = "#e0e0ea"

CHOICES = ["Rock", "Paper", "Scissors"]
EMOJI = {"Rock": "🪨", "Paper": "📄", "Scissors": "✂️"}
BEATS = {"Rock": "Scissors", "Scissors": "Paper", "Paper": "Rock"}
BTN_COLORS = {"Rock": "#8b5cf6", "Paper": "#3b82f6", "Scissors": "#ef4444"}
BTN_HOVER = {"Rock": "#7c3aed", "Paper": "#2563eb", "Scissors": "#dc2626"}

player_score = 0
computer_score = 0
ties = 0


def play(choice):
    global player_score, computer_score, ties

    comp = random.choice(CHOICES)

    player_icon.config(text=EMOJI[choice])
    comp_icon.config(text=EMOJI[comp])
    player_name_lbl.config(text=f"You chose {choice}")
    comp_name_lbl.config(text=f"PC chose {comp}")

    if choice == comp:
        ties += 1
        msg, color = "It's a Tie!", TIE_COLOR
    elif BEATS[choice] == comp:
        player_score += 1
        msg, color = "You Win! 🎉", WIN_COLOR
    else:
        computer_score += 1
        msg, color = "You Lose!", LOSE_COLOR

    result_lbl.config(text=msg, fg=color)
    score_lbl.config(text=f"You  {player_score}  –  {computer_score}  PC     Ties: {ties}")


def reset():
    global player_score, computer_score, ties
    player_score = computer_score = ties = 0
    result_lbl.config(text="Make your move!", fg=MUTED)
    player_icon.config(text="❓")
    comp_icon.config(text="❓")
    player_name_lbl.config(text="You")
    comp_name_lbl.config(text="Computer")
    score_lbl.config(text="You  0  –  0  PC     Ties: 0")


def make_choice_btn(parent, choice):
    bg = BTN_COLORS[choice]
    hbg = BTN_HOVER[choice]
    f = tk.Frame(parent, bg=bg, cursor="hand2", width=110, height=90)
    f.pack_propagate(False)

    emoji_lbl = tk.Label(f, text=EMOJI[choice], font=("Helvetica", 26),
                         bg=bg, fg="white")
    emoji_lbl.pack(pady=(10, 2))
    text_lbl = tk.Label(f, text=choice, font=("Helvetica", 11, "bold"),
                        bg=bg, fg="white")
    text_lbl.pack()

    for w in (f, emoji_lbl, text_lbl):
        w.bind("<Enter>", lambda e, b=bg, h=hbg: _hover(f, [emoji_lbl, text_lbl], h))
        w.bind("<Leave>", lambda e, b=bg: _hover(f, [emoji_lbl, text_lbl], b))
        w.bind("<Button-1>", lambda e, c=choice: play(c))

    return f


def _hover(frame, labels, color):
    frame.config(bg=color)
    for lbl in labels:
        lbl.config(bg=color)


# ── window ──────────────────────────────────────────────────────
root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("440x530")
root.resizable(False, False)
root.configure(bg=BG)

tk.Label(root, text="Rock  Paper  Scissors", font=("Georgia", 20, "bold"),
         bg=BG, fg=TEXT).pack(pady=(22, 2))
tk.Label(root, text="Choose your move",
         font=("Helvetica", 10), bg=BG, fg=MUTED).pack()

score_lbl = tk.Label(root, text="You  0  –  0  PC     Ties: 0",
                     font=("Helvetica", 12, "bold"), bg=BG, fg=SCORE_COLOR)
score_lbl.pack(pady=10)

# arena
arena = tk.Frame(root, bg=BG)
arena.pack(pady=6)

# player panel
left = tk.Frame(arena, bg=PANEL, padx=22, pady=14, bd=1, relief="flat",
                highlightthickness=1, highlightbackground=BORDER,
                highlightcolor=BORDER)
left.grid(row=0, column=0, padx=14)
tk.Label(left, text="YOU", font=("Helvetica", 10, "bold"), bg=PANEL, fg="#3b82f6").pack()
player_icon = tk.Label(left, text="❓", font=("Helvetica", 40), bg=PANEL)
player_icon.pack()
player_name_lbl = tk.Label(left, text="You", font=("Helvetica", 9), bg=PANEL, fg=MUTED)
player_name_lbl.pack()

tk.Label(arena, text="VS", font=("Georgia", 16, "bold"),
         bg=BG, fg="#d0d0d8").grid(row=0, column=1, padx=10)

# computer panel
right = tk.Frame(arena, bg=PANEL, padx=22, pady=14, bd=1, relief="flat",
                 highlightthickness=1, highlightbackground=BORDER,
                 highlightcolor=BORDER)
right.grid(row=0, column=2, padx=14)
tk.Label(right, text="COMPUTER", font=("Helvetica", 10, "bold"), bg=PANEL, fg="#ef4444").pack()
comp_icon = tk.Label(right, text="❓", font=("Helvetica", 40), bg=PANEL)
comp_icon.pack()
comp_name_lbl = tk.Label(right, text="Computer", font=("Helvetica", 9), bg=PANEL, fg=MUTED)
comp_name_lbl.pack()

result_lbl = tk.Label(root, text="Make your move!", font=("Georgia", 17, "bold"),
                      bg=BG, fg=MUTED)
result_lbl.pack(pady=16)

# choice buttons
btn_row = tk.Frame(root, bg=BG)
btn_row.pack()
for c in CHOICES:
    b = make_choice_btn(btn_row, c)
    b.pack(side=tk.LEFT, padx=8)

# reset
reset_frame = tk.Frame(root, bg="#1a1a2e", cursor="hand2")
reset_lbl = tk.Label(reset_frame, text="Reset Scores", font=("Helvetica", 10),
                     bg="#1a1a2e", fg="white", padx=14, pady=6)
reset_lbl.pack()
for w in (reset_frame, reset_lbl):
    w.bind("<Enter>", lambda e: [reset_frame.config(bg="#2a2a4e"), reset_lbl.config(bg="#2a2a4e")])
    w.bind("<Leave>", lambda e: [reset_frame.config(bg="#1a1a2e"), reset_lbl.config(bg="#1a1a2e")])
    w.bind("<Button-1>", lambda e: reset())
reset_frame.pack(pady=18)

root.mainloop()