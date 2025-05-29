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
ventola_accesa = False  # Nuova variabile per lo stato della ventola
# Variabili per controllo locale
ultimo_button_a = False
ultimo_button_b = False
contatore_comandi = 0
# Variabili per controllo ventola (evitare spam)
ultimo_comando_ventola = ""


# Funzione per inviare comandi alla prima micro:bit
def invia_comando(comando, valore):
    messaggio = "{}|{}".format(comando, valore)
    radio.send(messaggio)
    print("Comando inviato: {}".format(messaggio))


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
                ventola_accesa = bool(int(dati[5]))  # Nuovo parametro per la ventola

                # Ogni 5 messaggi mostra i dati sul display a scorrimento
                contatore_comandi += 1
                if contatore_comandi % 5 == 0:
                    display.scroll("T:{} L:{} P:{} V:{}".format(
                        temperatura,
                        led_stato,
                        potenza_led,
                        "ON" if ventola_accesa else "OFF"
                    ), wait=False)
        else:
            # Per altri tipi di messaggi, mostra solo un punto
            display.show(Image.SQUARE_SMALL)
            sleep(50)
            display.clear()

    # Controllo dei pulsanti per inviare comandi al primo micro:bit
    button_a_pressed = button_a.is_pressed()
    button_b_pressed = button_b.is_pressed()

    # Rileva la pressione dei pulsanti
    if button_a_pressed and not ultimo_button_a:
        # Pulsante A premuto: aumenta intensità LED della prima micro:bit
        nuovo_valore = min(potenza_led + 100, 1000)
        invia_comando("LED_INTENSITY", nuovo_valore)
        display.show(Image.ARROW_N)
        sleep(200)

    if button_b_pressed and not ultimo_button_b:
        # Pulsante B premuto: diminuzione intensità LED della prima micro:bit
        nuovo_valore = max(potenza_led - 100, 0)
        invia_comando("LED_INTENSITY", nuovo_valore)
        display.show(Image.ARROW_S)
        sleep(200)

    # Aggiorna lo stato precedente dei pulsanti
    ultimo_button_a = button_a_pressed
    ultimo_button_b = button_b_pressed

    # Controllo combinazione pulsanti - entrambi i pulsanti premuti cambia stato del sistema
    if button_a.is_pressed() and button_b.is_pressed():
        invia_comando("TOGGLE_SYSTEM", 1)
        display.show(Image.DIAMOND)
        sleep(500)
        # Aspetta che i pulsanti vengano rilasciati
        while button_a.is_pressed() or button_b.is_pressed():
            sleep(50)

    # Controllo della temperatura per comandi automatici (solo al cambio di stato)
    if temperatura > 28:
        # Se la temperatura è molto alta, forza l'accensione della ventola
        if ultimo_comando_ventola != "VENTOLA_ON":
            invia_comando("VENTOLA_ON", 1)
            ultimo_comando_ventola = "VENTOLA_ON"
    elif temperatura < 24:
        # Se la temperatura è bassa, spegni la ventola
        if ultimo_comando_ventola != "VENTOLA_OFF":
            invia_comando("VENTOLA_OFF", 1)
            ultimo_comando_ventola = "VENTOLA_OFF"

    sleep(50)  # Piccola pausa per evitare spam di messaggi