# LED Matrix Editor & Player

A simple drag-and-draw editor and frame player for **MAX7219 LED dot matrix displays**.

This project helps create designs such as **robot eyes, shapes, symbols, and patterns** using an easy-to-use GUI.  
Frames can be saved and played back using a separate player with manual switching, automatic animation, and speed control.

---

## ✨ Features

- Drag-and-draw LED matrix editor (32×8)
- Live preview on MAX7219 LED matrix
- Save designs as frame files
- Frame player with:
  - Manual frame switching
  - Automatic animation mode
  - Adjustable animation speed
- Diff-based rendering for stable and efficient updates
- Supports ESP8266 / Arduino over serial

---

## 🧩 Project Structure

editor/ → LED matrix design tool
player/ → Frame player and animation tool
esp/ → ESP8266 / Arduino MAX7219 pixel server
examples/ → Sample frame files


---

## 🔧 Hardware Used

- MAX7219 LED Dot Matrix (8×32)
- ESP8266 / Arduino
- USB serial connection

---

## 🔗 ESP8266 – MAX7219 Connection

- VCC → 5V / VIN  
- GND → GND  
- DIN → D7 (GPIO13)  
- CLK → D5 (GPIO14)  
- CS / LOAD → D4 (GPIO2)

---

## 🚀 Usage (basic)

1. Upload the ESP firmware to your board.
2. Run the editor to draw and save frames.
3. Run the player to load frames and play animations.
4. Load all frames by selecting all frame files at once and opening.

---

## 📄 License

MIT License
