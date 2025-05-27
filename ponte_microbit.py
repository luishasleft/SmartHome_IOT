import serial
import requests
import time

FLASK_URL = 'http://127.0.0.1:5000/api/stato'  # sarà il tuo endpoint Flask

# Apri la seriale
serial_microbit = serial.Serial('COM10', 115200, timeout=1)
time.sleep(2)  # tempo per avviare la connessione

while True:
    linea = serial_microbit.readline().decode('utf-8').strip()
    if linea:
        print("[SERIALE] Messaggio ricevuto:", linea)

        # Prova a interpretare il messaggio come stringa separata da "|"
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

                # Invia a Flask
                response = requests.post(FLASK_URL, json=dati)
                print("[FLASK] Risposta:", response.status_code)

            except Exception as e:
                print(f"[ERRORE] Errore nel parsing: {e}")
        else:
            print("[ERRORE] Formato messaggio non valido")
