import serial
import time
import tkinter as tk
from tkinter import filedialog

# -------- CONFIG --------
PORT = "COM8"
BAUD = 115200
PIXEL = 20
W, H = 32, 8

# MUST MATCH PLAYER ORIENTATION
FLIP_X = True
FLIP_Y = False

SEND_DELAY = 0.001  # 🔑 prevents parseInt corruption

ser = serial.Serial(PORT, BAUD, timeout=1)

# -------- DATA --------
pixels = [[0]*W for _ in range(H)]
mouse_down = False
paint_value = 1
mirror_on = False

# -------- GUI --------
root = tk.Tk()
root.title("LED Editor (Mirror Corrected)")

canvas = tk.Canvas(root, width=W*PIXEL, height=H*PIXEL, bg="gray")
canvas.pack()

rects = [[None]*W for _ in range(H)]

# -------- MAPPING --------
def MAP_X(x):
    return W - 1 - x if FLIP_X else x

def MAP_Y(y):
    return H - 1 - y if FLIP_Y else y

# -------- CORE --------
def send(x, y, v):
    ser.write(f"{x} {y} {v}\n".encode())
    time.sleep(SEND_DELAY)

def draw_single(x, y, v):
    if pixels[y][x] != v:
        pixels[y][x] = v
        canvas.itemconfig(rects[y][x], fill="red" if v else "black")

        px = MAP_X(x)
        py = MAP_Y(y)
        send(px, py, v)

def draw_pixel(x, y, v):
    # main pixel
    draw_single(x, y, v)

    # mirrored pixel
    if mirror_on:
        mx = W - 1 - x
        draw_single(mx, y, v)

# -------- INPUT --------
def mouse_press(event):
    global mouse_down, paint_value
    mouse_down = True
    x = event.x // PIXEL
    y = event.y // PIXEL
    if 0 <= x < W and 0 <= y < H:
        paint_value = 0 if pixels[y][x] else 1
        draw_pixel(x, y, paint_value)

def mouse_release(event):
    global mouse_down
    mouse_down = False

def handle_paint(event):
    if not mouse_down:
        return
    x = event.x // PIXEL
    y = event.y // PIXEL
    if 0 <= x < W and 0 <= y < H:
        draw_pixel(x, y, paint_value)

canvas.bind("<ButtonPress-1>", mouse_press)
canvas.bind("<ButtonRelease-1>", mouse_release)
canvas.bind("<B1-Motion>", handle_paint)

# -------- GRID --------
for y in range(H):
    for x in range(W):
        rects[y][x] = canvas.create_rectangle(
            x*PIXEL, y*PIXEL,
            (x+1)*PIXEL, (y+1)*PIXEL,
            fill="black",
            outline="white"
        )

# -------- MIRROR TOGGLE --------
def toggle_mirror():
    global mirror_on
    mirror_on = not mirror_on
    mirror_btn.config(text=f"Mirror: {'ON' if mirror_on else 'OFF'}")

mirror_btn = tk.Button(root, text="Mirror: OFF", command=toggle_mirror)
mirror_btn.pack(pady=4)

# -------- SAVE --------
def save_file():
    file = filedialog.asksaveasfilename(defaultextension=".txt")
    if not file:
        return
    with open(file, "w") as f:
        for y in range(H):
            f.write("".join("1" if pixels[y][x] else "0" for x in range(W)) + "\n")

tk.Button(root, text="Save Frame (.txt)", command=save_file).pack(pady=6)

root.mainloop()
