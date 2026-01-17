import serial
import time
import tkinter as tk
from tkinter import filedialog

# ---------- CONFIG ----------
PORT = "COM8"
BAUD = 115200
WIDTH = 32
HEIGHT = 8

FLIP_X = True
FLIP_Y = False

DRAW_DELAY = 0.001     # per pixel delay
LOOP_DELAY = 200       # redraw interval

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

frames = []
current_index = 0
running = False
auto_mode = False
last_frame = None

# ---------- CORE ----------
def draw_diff(frame):
    global last_frame

    if last_frame is None:
        for y in range(HEIGHT):
            for x in range(WIDTH):
                ser.write(f"{x} {y} 0\n".encode())
                time.sleep(DRAW_DELAY)

        for y in range(HEIGHT):
            for x in range(WIDTH):
                if frame[y][x] == "1":
                    px = WIDTH - 1 - x if FLIP_X else x
                    py = HEIGHT - 1 - y if FLIP_Y else y
                    ser.write(f"{px} {py} 1\n".encode())
                    time.sleep(DRAW_DELAY)

        last_frame = [row[:] for row in frame]
        return

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if frame[y][x] != last_frame[y][x]:
                px = WIDTH - 1 - x if FLIP_X else x
                py = HEIGHT - 1 - y if FLIP_Y else y
                ser.write(f"{px} {py} {frame[y][x]}\n".encode())
                time.sleep(DRAW_DELAY)

    last_frame = [row[:] for row in frame]

def draw_current_frame():
    if not running or not frames:
        return
    draw_diff(frames[current_index])
    root.after(LOOP_DELAY, draw_current_frame)

# ---------- AUTO SWITCH ----------
def auto_step():
    global current_index
    if not running or not auto_mode or not frames:
        return
    current_index = (current_index + 1) % len(frames)
    draw_diff(frames[current_index])

    # use speed slider value
    root.after(speed_var.get(), auto_step)

# ---------- FILE ----------
def load_frames():
    global frames, current_index, last_frame
    files = filedialog.askopenfilenames(
        filetypes=[("Frame Files", "*.txt")]
    )
    if not files:
        return

    frames = []
    for file in files:
        with open(file) as f:
            lines = [line.strip() for line in f.readlines()]
        if len(lines) == HEIGHT and all(len(line) == WIDTH for line in lines):
            frames.append(lines)

    current_index = 0
    last_frame = None
    print(f"{len(frames)} frame(s) loaded")

# ---------- CONTROLS ----------
def start():
    global running
    if not frames:
        return
    running = True
    draw_current_frame()
    if auto_mode:
        auto_step()

def stop():
    global running
    running = False

def switch_frame():
    global current_index
    if not frames:
        return
    current_index = (current_index + 1) % len(frames)
    if not running:
        draw_diff(frames[current_index])

def toggle_auto():
    global auto_mode
    auto_mode = not auto_mode
    auto_btn.config(text=f"Auto: {'ON' if auto_mode else 'OFF'}")
    if auto_mode and running:
        auto_step()

# ---------- GUI ----------
root = tk.Tk()
root.title("LED Matrix Player")

tk.Button(root, text="Load Frame(s)", command=load_frames).pack(fill="x", padx=10, pady=5)
tk.Button(root, text="Start", command=start).pack(fill="x", padx=10, pady=5)
tk.Button(root, text="Switch", command=switch_frame).pack(fill="x", padx=10, pady=5)

auto_btn = tk.Button(root, text="Auto: OFF", command=toggle_auto)
auto_btn.pack(fill="x", padx=10, pady=5)

# ---------- SPEED SLIDER ----------
speed_var = tk.IntVar(value=800)  # default ms

tk.Label(root, text="Frame Speed (ms)").pack()
tk.Scale(
    root,
    from_=100, to=2000,        # fast → slow
    orient=tk.HORIZONTAL,
    variable=speed_var
).pack(fill="x", padx=10, pady=5)

root.mainloop()
