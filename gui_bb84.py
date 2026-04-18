import tkinter as tk
from tkinter import messagebox
import winsound
import random

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from bb84_project import run_simulation

# ── Config ──────────────────────────────────────
MATRIX_CHARS = "01ｦｧｨｩｪｫABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&*"
FONT_SIZE = 13
COL_WIDTH = 14
DROP_SPEED = 40

# 🔥 UPDATED SIZE
W, H = 620, 660

# ── Matrix Rain ─────────────────────────────────
class MatrixRain:
    def __init__(self, canvas):
        self.c = canvas
        self.cols = W // COL_WIDTH
        self.drops = [random.randint(-60, 0) for _ in range(self.cols)]
        self.items = []

        for i in range(self.cols):
            item = canvas.create_text(
                i * COL_WIDTH + COL_WIDTH // 2, -20,
                text="", fill="#00ff41",
                font=("Courier", FONT_SIZE, "bold")
            )
            self.items.append(item)

        self._tick()

    def _tick(self):
        for i, y in enumerate(self.drops):
            ch = random.choice(MATRIX_CHARS)
            px = i * COL_WIDTH + COL_WIDTH // 2
            py = y * FONT_SIZE

            color = "#ffffff" if random.random() > 0.95 else "#00ff41"

            self.c.itemconfig(self.items[i], text=ch, fill=color)
            self.c.coords(self.items[i], px, py)

            if py > H and random.random() > 0.975:
                self.drops[i] = 0
            else:
                self.drops[i] += 1

        self.c.tag_raise("ui")
        self.c.after(DROP_SPEED, self._tick)

# ── Window ──────────────────────────────────────
root = tk.Tk()
root.title("Quantum Hacker Detection System")
root.geometry(f"{W}x{H}")
root.resizable(False, False)

canvas = tk.Canvas(root, width=W, height=H, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

MatrixRain(canvas)

# ── UI ──────────────────────────────────────────
title = tk.Label(root, text=">> QUANTUM SECURITY SYSTEM <<",
                 font=("Courier", 13, "bold"),
                 fg="#00ff41", bg="black")
canvas.create_window(W//2, 30, window=title, tags="ui")

# 🔥 BIGGER LOG BOX
output_text = tk.Text(root, height=14, width=60,
                      bg="#030d03", fg="#00ff41",
                      insertbackground="#00ff41",
                      font=("Courier", 10),
                      relief="flat",
                      highlightbackground="#00ff41",
                      highlightthickness=1)
canvas.create_window(W//2, 160, window=output_text, tags="ui")

# ── QBER Graph ──────────────────────────────────
graph_frame = tk.Frame(root, bg="black")

# 🔥 MOVED DOWN + BIGGER
canvas.create_window(W//2, 350, window=graph_frame,
                     width=500, height=190, tags="ui")

fig = Figure(figsize=(5, 2.2), dpi=80, facecolor="black")
ax = fig.add_subplot(111, facecolor="black")

ax.set_title("QBER Comparison", color="#00ff41", pad=12)
ax.set_facecolor("black")
ax.tick_params(colors="#00ff41")
for spine in ax.spines.values():
    spine.set_color("#00ff41")

ax.set_ylabel("QBER %", color="#00ff41")
ax.set_xticks([0, 1])
ax.set_xticklabels(["Without Hacker", "With Hacker"], color="#00ff41")
ax.grid(axis="y", color="#00ff41", alpha=0.2)

qber_values = [0.0, 0.0]
bars = ax.bar([0, 1], qber_values, color=["#00ff41", "#33ff33"], width=0.5)

canvas_graph = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_graph.draw()
canvas_graph.get_tk_widget().pack(fill="both", expand=True)

def update_qber_graph(without_hacker=None, with_hacker=None):
    if without_hacker is not None:
        qber_values[0] = without_hacker * 100
    if with_hacker is not None:
        qber_values[1] = with_hacker * 100

    max_value = max(10, max(qber_values) * 1.2)
    ax.set_ylim(0, max_value)

    for i, bar in enumerate(bars):
        bar.set_height(qber_values[i])

    canvas_graph.draw()

# ── Effects ─────────────────────────────────────
def typing_effect(text, delay=10):
    output_text.delete(1.0, tk.END)
    for char in text:
        output_text.insert(tk.END, char)
        output_text.update()
        root.after(delay)

def flash_red(duration=200):
    overlay = canvas.create_rectangle(0, 0, W, H, fill="red", tags="flash")
    canvas.tag_raise("flash")
    root.after(duration, lambda: canvas.delete(overlay))

# ── Functions ───────────────────────────────────
def run_clean():
    typing_effect("[SCANNING SYSTEM...]\n[CHECKING CHANNEL...]\n")

    def show():
        qber, _ = run_simulation("WITHOUT HACKER", False)
        output_text.insert(tk.END, "\n[SYSTEM SECURE]\n")
        output_text.insert(tk.END, f"QBER: {qber*100:.2f}%\n")
        update_qber_graph(without_hacker=qber)
    messagebox.showinfo("Result", "Secure Communication ✅")

    root.after(1500, show)
    

def run_hacker():
    typing_effect("[SCANNING SYSTEM...]\n[DETECTING INTRUSION...]\n")

    def show():
        qber, _ = run_simulation("WITH HACKER", True)

        flash_red()

        output_text.insert(tk.END, "\n[INTRUSION DETECTED]\n")
        output_text.insert(tk.END, f"QBER: {qber*100:.2f}%\n")
        update_qber_graph(with_hacker=qber)

        winsound.PlaySound("mixkit-facility-alarm-sound-999_CEfo3ago.wav",
                           winsound.SND_FILENAME)
    messagebox.showwarning("Alert", "Hacker Detected 🚨")

    root.after(1500, show)

def clear_output():
    output_text.delete(1.0, tk.END)

# ── Buttons ─────────────────────────────────────
btn1 = tk.Button(root, text="▶ Run Secure",
                 command=run_clean,
                 bg="#003300", fg="#00ff41",
                 font=("Courier", 10, "bold"),
                 width=22)
canvas.create_window(W//2, 460, window=btn1, tags="ui")

btn2 = tk.Button(root, text="☠ Run Attack",
                 command=run_hacker,
                 bg="#3d0000", fg="#ff3333",
                 font=("Courier", 10, "bold"),
                 width=22)
canvas.create_window(W//2, 510, window=btn2, tags="ui")

btn3 = tk.Button(root, text="✕ Clear",
                 command=clear_output,
                 bg="#1a1a1a", fg="#aaaaaa",
                 font=("Courier", 10),
                 width=22)
canvas.create_window(W//2, 560, window=btn3, tags="ui")

root.mainloop()