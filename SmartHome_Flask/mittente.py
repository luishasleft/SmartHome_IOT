from microbit import *
import music
import radio

display.off()
autenticazione = False
start = False
on = 0
ventola_attiva = False
val = 500
pin6.write_analog(val)

# Variabile per controllare se la luce è forzatamente accesa/spenta da web
controllo_web_luce = False
luce_web_accesa = False
intensita_web = 500

# accensione della radio e creazione del gruppo
radio.on()
radio.config(group=1)

# Inizializza la comunicazione seriale
uart.init(baudrate=115200)

# Buffer per i dati seriali
buffer_seriale = ""

# Variabili per i dati ricevuti dalla seconda micro:bit
comando_ricevuto = ""
valore_ricevuto = 0
led_remoto_stato = 0


# Funzioni per controllare la ventola
def ventola_on():
    pin7.write_analog(550)  # INA - ON con potenza limitata
    pin10.write_digital(0)  # INB - OFF


def ventola_off():
    pin7.write_digital(0)
    pin10.write_digital(0)


# Funzione per processare i comandi luce da web
def processa_comando_luce(stato_luce, intensita):
    global controllo_web_luce, luce_web_accesa, intensita_web, val

    controllo_web_luce = True
    luce_web_accesa = bool(stato_luce)
    intensita_web = int(intensita)

    # Aggiorna anche val per mantenere coerenza
    val = intensita_web

    # Applica immediatamente il comando
    if luce_web_accesa:
        pin6.write_analog(intensita_web)
        uart.write("Luce accesa via web - Intensita: {}\n".format(intensita_web))
    else:
        pin6.write_digital(0)
        uart.write("Luce spenta via web\n")


# Funzione per processare i comandi web (ARM, DISARM, SOS)
def processa_comando_web(comando):
    global on, controllo_web_luce

    if comando == "ARM":
        # Imposta sistema in modalità ARM (spegnimento - LED rosso)
        if on % 2 == 1:  # Se è attualmente acceso (DISARM)
            on += 1  # Spegni il sistema
        # Disabilita controllo web quando si cambia modalità sistema
        controllo_web_luce = False
        uart.write("Sistema ARM attivato\n")

    elif comando == "DISARM":
        # Imposta sistema in modalità DISARM (accensione - LED verde)
        if on % 2 == 0:  # Se è attualmente spento (ARM)
            on += 1  # Accendi il sistema
        # Disabilita controllo web quando si cambia modalità sistema
        controllo_web_luce = False
        uart.write("Sistema DISARM attivato\n")

    elif comando == "SOS":
        # Attiva allarme SOS - forza il sistema in ARM e attiva suono
        if on % 2 == 1:  # Se è attualmente acceso
            on += 1  # Spegni il sistema per attivare ARM
        # Disabilita controllo web quando si attiva SOS
        controllo_web_luce = False
        # Suona l'allarme SOS
        for i in range(3):
            music.pitch(880, 200)  # Suono acuto
            sleep(100)
            music.pitch(440, 200)  # Suono grave
            sleep(100)
        uart.write("Allarme SOS attivato\n")


# Funzione per leggere e processare i dati seriali
def leggi_seriale():
    global buffer_seriale

    # Legge tutti i dati disponibili dalla seriale
    while uart.any():
        char = uart.read(1)
        if char:
            char = char.decode('utf-8')
            if char == '\n' or char == '\r':
                # Fine del comando, processa il buffer
                if buffer_seriale.strip():
                    try:
                        comando_pulito = buffer_seriale.strip()

                        # Controlla se è un comando web (ARM, DISARM, SOS)
                        if comando_pulito in ["ARM", "DISARM", "SOS"]:
                            processa_comando_web(comando_pulito)

                        # Controlla se è un comando LUCE
                        elif comando_pulito.startswith("LUCE|"):
                            parti = comando_pulito.split("|")
                            if len(parti) == 3:
                                stato_luce = int(parti[1])  # 0 o 1
                                intensita = int(parti[2])  # 0-1000
                                processa_comando_luce(stato_luce, intensita)
                                uart.write(
                                    "Comando luce ricevuto: stato={}, intensita={}\n".format(stato_luce, intensita))
                            else:
                                uart.write("Errore formato comando LUCE\n")

                        # Controlla se è un comando DATA dalla webapp
                        elif comando_pulito.startswith("DATA|"):
                            # Ignora i comandi DATA dalla webapp (sono solo per debug)
                            uart.write("Comando DATA ricevuto e ignorato\n")
                    except Exception as e:
                        uart.write("Errore nel processare comando seriale: {}\n".format(buffer_seriale))
                # Reset del buffer
                buffer_seriale = ""
            else:
                # Aggiungi il carattere al buffer
                buffer_seriale += char


while True:
    # Leggi e processa comandi seriali
    leggi_seriale()

    signal = pin9.read_digital()

    # Se il sensore NON rileva un campo magnetico
    if signal == 1:
        autenticazione = False
    # Se il sensore RILEVA un campo magnetico
    else:
        autenticazione = True
        sleep(100)
        on += 1

    # Controllo dell'accensione e dell'intensità della luce
    movimento = pin8.read_digital()

    # Calcolo dello stato del LED
    led_acceso = 0
    potenza_led = val

    # Se il controllo web è attivo, usa le impostazioni web
    if controllo_web_luce:
        led_acceso = 1 if luce_web_accesa else 0
        potenza_led = intensita_web

        if luce_web_accesa:
            pin6.write_analog(intensita_web)
        else:
            pin6.write_digital(0)
    else:
        # Controllo normale basato sullo stato del sistema
        # Il LED è acceso se il sistema è in modalità "acceso" (on % 2 == 1) - VERDE
        if on % 2 == 1:
            led_acceso = 1
            # Accendi il LED con l'intensità corrente
            pin6.write_analog(val)
            potenza_led = val
        else:
            # Sistema in modalità spenta (ROSSO) - LED spento
            led_acceso = 0
            pin6.write_digital(0)
            potenza_led = val

            # Variabile per tracciare se sta suonando la musica
    musica_attiva = 0

    # Controllo dell'allarme quando c'è movimento ma sistema è spento (ROSSO)
    if movimento == 1 and on % 2 == 0:
        music.pitch(440, 100)
        music.pitch(220, 100)
        musica_attiva = 1
    # Suono per cambio stato "Sbloccato/Bloccato"
    if autenticazione != start:
        start = autenticazione
        music.pitch(440, 100)
        music.pitch(220, 100)
        musica_attiva = 1

    # Controllo del LED di "sblocco" rosso/verde
    colore_led = ""
    if on % 2 == 1:
        pin1.write_analog(0)  # Rosso spento
        pin2.write_analog(1023)  # Verde acceso
        colore_led = "verde"
        sleep(100)
    else:
        pin1.write_analog(1023)  # Rosso acceso
        pin2.write_analog(0)  # Verde spento
        colore_led = "rosso"
        sleep(100)

    # Lettura e conversione della temperatura dal sensore (P3)
    Temp = (300 * pin3.read_analog()) // 1023

    # Stato della ventola (1 se accesa, 0 se spenta)
    stato_ventola = 1 if ventola_attiva else 0

    # Invio di tutti i dati separati da "|"
    # Aggiungiamo "DATA|" per distinguere dai comandi
    dati_da_inviare = "DATA|{}|{}|{}|{}|{}|{}".format(
        Temp, led_acceso, potenza_led, colore_led, musica_attiva, stato_ventola
    )
    radio.send(dati_da_inviare)

    # Mostra la temperatura sul display
    display.show(str(Temp))
    uart.write("Temp(C): {}\n".format(Temp))

    # Controllo della ventola
    if Temp >= 30 and not ventola_attiva:
        ventola_on()
        ventola_attiva = True
    elif Temp <= 26 and ventola_attiva:
        ventola_off()
        ventola_attiva = False