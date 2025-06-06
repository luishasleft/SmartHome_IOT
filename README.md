# 🏠 Smart Home Alarm System with micro:bit and Flask

## 📌 Project Overview

This project aims to build a **smart home automation system** using **micro:bit** boards that can detect and monitor essential environmental conditions for **home safety and comfort**.

The system consists of two micro:bit boards, various environmental sensors, and a **Flask web app** to display data in real-time.

## 🧠 Key Features

- 🌡️ Detects **ambient temperature**
- 💡 Monitors **room light intensity**
- 🚪 Detects **door status** (open/closed)
- 🚨 Detects **motion/presence**
- 🔊 Alarm control with states: `DISARM`, `ARM`, `SOS`
- 🌬️ Automatically activates **fan** when temperature is high
- 🌐 Web interface with **real-time updates**

## ⚙️ Hardware Components

- 2x **BBC micro:bit**
- **LM35** (Temperature sensor)
- **PIR Motion Sensor**
- **Hall Magnetic Sensor** (door detection)
- **RGB LED Module**
- **Fan**
- Jumper wires and breadboard

### 📌 Pin Configuration

| Component               | micro:bit Pins      |
|--------------------------|---------------------|
| LM35 Temp. Sensor        | S=3, V=3, G=3        |
| PIR Motion Sensor        | S=8, V=8, G=8        |
| RGB LED                  | R=S2, G=S1, B=S4, V=V1 |
| Hall Magnetic Sensor     | S=9, V=9, G=9        |
| Magnetic door            | Ina=S7, Inb=S10      |
| Fan                      | V=V2, GND=G10        |

## 🧪 System Architecture

1. **Sensor Micro:bit**:
   - Collects environmental data from sensors
   - Sends data via **radio** to the receiver micro:bit

2. **Receiver Micro:bit**:
   - Connected to **PC via USB**
   - Sends data via **serial** to the Flask web app

3. **Web App (Flask)**:
   - Reads data from serial port
   - Stores and manages state using **SQLite**
   - Displays data through a **simple dashboard** (HTML/CSS/JS)

## 🖥️ Technologies Used

- **MicroPython** (for micro:bit)
- **Python 3** + **Flask** (backend)
- **SQLite** (database)
- **HTML/CSS/JavaScript** (frontend)


## 🚀 How to Run

1. **Connect** the receiver micro:bit to your PC via USB.
2. Start the Flask server:
   ```bash
   python app_flask/app.py
   ```
3. Power on the sensor micro:bit: data transmission begins.
4. Visit the interface at `http://localhost:5000`.

## 🔧 Web Interface Controls

- **ARM**: Activate alarm
- **DISARM**: Deactivate alarm
- **SOS**: Emergency state
- Light control (toggle on/off + set intensity)

## 🧠 Technical Notes

- The project started using **Blazor**, but due to serial communication issues, it was migrated to **Flask**.
- Real-time updates are handled via **JavaScript** that refreshes the page upon state changes.

## 🙋‍♂️ Authors

- Luigi Gorgone - https://github.com/luishasleft
- Ludovica Gatti - https://github.com/G4tten
- Emanuele Marcello - https://github.com/MarcelloEmanuele
