from microbit import *
import radio

radio.on()
radio.config(group=1)

# Variabili per salvare i dati ricevuti
temperatura = 0
led_stato = 0
potenza_led = 0
colore_attivo = ""
musica_suonando = False
ventola_accesa = False
contatore_comandi = 0

while True:
    # Controllo continuo della ricezione di messaggi
    messaggio = radio.receive()
    if messaggio:
        # Stampa TUTTO quello che riceve sulla porta seriale (per la web app)
        print(messaggio)

        # Controlla se è un messaggio di dati (inizia con "DATA|")
        if messaggio.startswith("DATA|"):
            # Feedback visivo per i dati ricevuti
            display.show(Image.HAPPY)
            sleep(100)
            display.clear()

            # Rimuovi il prefisso "DATA|" e processa i dati
            dati_puliti = messaggio[5:]
            dati = dati_puliti.split("|")

            # Salva tutti i dati nelle variabili (ora sono 6 parametri)
            if len(dati) == 6:
                temperatura = int(dati[0])
                led_stato = int(dati[1])
                potenza_led = int(dati[2])
                colore_attivo = dati[3]
                musica_suonando = bool(int(dati[4]))
                ventola_accesa = bool(int(dati[5]))

    sleep(50)  # Piccola pausa per evitare spam di messaggi