import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import subprocess
import threading

def launch_game():
    def run():
        status_var.set("Running game...")

        black = black_var.get()
        white = white_var.get()
        time_limit = time_var.get()
        dup = dup_var.get()
        level_b = level_b_var.get()
        level_w = level_w_var.get()

        cmd = [
            "python", "othello.py",
            black, white,
            "-t", str(time_limit),
            "-lB", str(level_b),
            "-lW", str(level_w)
        ]

        if ab_b_var.get():
            cmd.append("-aB")
        if ab_w_var.get():
            cmd.append("-aW")
        if verbose_var.get():
            cmd.append("-v")
        if dup > 1:
            cmd.extend(["-dup", str(dup)])

        try:
            subprocess.Popen(cmd)
        except Exception as e:
            status_var.set(f"Error: {e}")
        else:
            status_var.set("Game launched.")

    threading.Thread(target=run, daemon=True).start()

# === GUI using ttkbootstrap ===
root = tb.Window(themename="darkly")
root.title("Othello Game Launcher")
root.geometry("460x540")

TITLE_FONT = ("Courier New", 20, "bold")
frame = tb.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

label = tb.Label(frame, text="Othello Game Launcher", font=TITLE_FONT, bootstyle="info")
label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

engines = ["human", "minimax", "alpha", "random", "new_alpha"]
black_var = tb.StringVar(value="human")
white_var = tb.StringVar(value="minimax")

tb.Label(frame, text="Black Engine:").grid(row=1, column=0, sticky="w", pady=6)
tb.Combobox(frame, textvariable=black_var, values=engines, state="readonly").grid(row=1, column=1, sticky="ew", pady=6)

tb.Label(frame, text="White Engine:").grid(row=2, column=0, sticky="w", pady=6)
tb.Combobox(frame, textvariable=white_var, values=engines, state="readonly").grid(row=2, column=1, sticky="ew", pady=6)

ab_b_var = tb.BooleanVar()
ab_w_var = tb.BooleanVar()
tb.Checkbutton(frame, text="Black Alpha-Beta", variable=ab_b_var).grid(row=3, column=0, sticky="w", pady=6)
tb.Checkbutton(frame, text="White Alpha-Beta", variable=ab_w_var).grid(row=3, column=1, sticky="w", pady=6)

verbose_var = tb.BooleanVar()
tb.Checkbutton(frame, text="Verbose Output", variable=verbose_var).grid(row=4, column=0, sticky="w", pady=6)

time_var = tb.IntVar(value=300)
tb.Label(frame, text="Time Limit (s):").grid(row=5, column=0, sticky="w", pady=6)
tb.Entry(frame, textvariable=time_var).grid(row=5, column=1, sticky="ew", pady=6)

level_b_var = tb.IntVar(value=4)
level_w_var = tb.IntVar(value=4)
tb.Label(frame, text="Black Level:").grid(row=6, column=0, sticky="w", pady=6)
tb.Entry(frame, textvariable=level_b_var).grid(row=6, column=1, sticky="ew", pady=6)
tb.Label(frame, text="White Level:").grid(row=7, column=0, sticky="w", pady=6)
tb.Entry(frame, textvariable=level_w_var).grid(row=7, column=1, sticky="ew", pady=6)

dup_var = tb.IntVar(value=1)
tb.Label(frame, text="Repeat Count:").grid(row=8, column=0, sticky="w", pady=6)
tb.Entry(frame, textvariable=dup_var).grid(row=8, column=1, sticky="ew", pady=6)

status_var = tb.StringVar(value="Idle")
tb.Label(frame, textvariable=status_var, bootstyle="secondary").grid(
    row=9, column=0, columnspan=2, pady=(12, 4))

tb.Button(frame, text="▶ Play Game", command=launch_game, bootstyle="primary").grid(
    row=10, column=0, columnspan=2, pady=14, ipadx=10, ipady=4)

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

root.mainloop()
