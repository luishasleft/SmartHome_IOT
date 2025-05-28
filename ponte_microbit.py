import serial
import requests
import time

FLASK_URL = 'http://127.0.0.1:5000/api/stato'  # endpoint Flask

# Apri la seriale
try:
    serial_microbit = serial.Serial('COM10', 115200, timeout=1)
    time.sleep(2)  # attendi connessione stabile
    print("[INFO] Porta seriale aperta su COM10")
except Exception as e:
    print(f"[ERRORE] Impossibile aprire la porta seriale: {e}")
    exit(1)

while True:
    try:
        linea = serial_microbit.readline().decode('utf-8').strip()
        if linea:
            print("[SERIALE] Messaggio ricevuto:", linea)

            if "|" in linea:
                try:
                    messaggio, temperatura, led_stato, potenza_led, colore, musica = linea.split("|")
                    dati = {
                        "messaggio": messaggio,
                        "temperatura": int(temperatura),
                        "led_stato": int(led_stato),
                        "potenza_led": int(potenza_led),
                        "colore": colore,
                        "musica": bool(int(musica))
                    }
                    print("[OK] Messaggio convertito:", dati)

                    try:
                        response = requests.post(FLASK_URL, json=dati)
                        print(f"[FLASK] Risposta: {response.status_code} - {response.text}")
                    except requests.RequestException as e:
                        print(f"[ERRORE] Impossibile inviare dati a Flask: {e}")

                except Exception as e:
                    print(f"[ERRORE] Parsing messaggio: {e}")
            else:
                print("[ERRORE] Formato messaggio non valido")

        time.sleep(0.1)  # evita di saturare la CPU

    except Exception as e:
        print(f"[ERRORE] Lettura seriale fallita: {e}")
        time.sleep(2)
