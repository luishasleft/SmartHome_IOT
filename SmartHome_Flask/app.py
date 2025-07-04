import sqlite3
import serial
import time

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'smarthomedb.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ultimo_stato = None
ultima_temperatura = None
stato_luce = False
intensita_luce = 500  # default a metà

class StoricoAllarme(db.Model):
    __tablename__ = 'StoricoAllarme'
    id = db.Column(db.Integer, primary_key=True)
    data_ora = db.Column(db.DateTime, nullable=False, default=datetime.now)
    stato = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Allarme {self.stato} @ {self.data_ora}>'


def invia_comando_seriale(comando, porta='COM12', baudrate=115200):
    try:
        with serial.Serial(porta, baudrate, timeout=1) as ser:
            time.sleep(2)  # attesa porta pronta

            # Invia direttamente il comando (ARM, DISARM, SOS)
            msg = comando

            ser.write((msg + '\n').encode())
            print(f"[SERIALE] Comando inviato: {msg}")
            return True
    except Exception as e:
        print(f"[ERRORE SERIALE] {e}")
        return False

@app.route('/')
def index():
    ultimo = get_ultimo_stato()
    try:
        return render_template('index.html', ultimo=ultimo, temperatura=ultima_temperatura, stato_luce=stato_luce)
    except Exception as e:
        return f"Errore nel caricamento dello storico: {str(e)}", 500

@app.route('/api/stato', methods=['POST'])
def ricevi_stato_microbit():
    global ultimo_stato, ultima_temperatura, stato_luce, intensita_luce
    try:
        dati = request.get_json()
        richiesti = ['messaggio', 'temperatura', 'led_stato', 'potenza_led', 'colore', 'musica', 'ventola']
        if not all(k in dati for k in richiesti):
            return jsonify({"errore": "Campi mancanti"}), 400

        ultima_temperatura = dati['temperatura']
        stato_luce = bool(int(dati['led_stato']))
        intensita_luce = int(dati['potenza_led'])

        stato_corrente = None
        if dati['colore'] == 'verde':
            stato_corrente = 'DISARM'
        elif dati['colore'] == 'rosso' and dati['musica']:
            stato_corrente = 'SOS'
            stato_luce = False
        elif dati['colore'] == 'rosso' and not dati['musica']:
            stato_corrente = 'ARM'
            stato_luce = False

        if stato_corrente is None:
            return jsonify({"errore": "Stato non riconosciuto"}), 400

        if stato_corrente != ultimo_stato:
            nuovo_evento = StoricoAllarme(stato=stato_corrente)
            db.session.add(nuovo_evento)
            db.session.commit()
            print(f"[FLASK] Cambio stato registrato: {stato_corrente}")
            ultimo_stato = stato_corrente
        else:
            print(f"[FLASK] Stato invariato: {stato_corrente} (ignorato)")

        return jsonify({"successo": True, "stato": stato_corrente}), 200

    except Exception as e:
        db.session.rollback()
        print("[FLASK] Errore", str(e))
        return jsonify({"errore": str(e)}), 500

def get_allarmi():
    return StoricoAllarme.query.order_by(StoricoAllarme.data_ora.desc()).all()

@app.route('/api/stato_luce', methods=['GET'])
def stato_luce_corrente():
    return jsonify({
        "luce_accesa": stato_luce,
        "intensita": intensita_luce
    })


@app.route('/storico')
def storico():
    try:
        allarmi = get_allarmi()
        return render_template('Storico.html', allarmi=allarmi)
    except Exception as e:
        return f"Errore nel caricamento dello storico: {str(e)}", 500

def get_ultimo_stato():
    ultimo = StoricoAllarme.query.order_by(StoricoAllarme.data_ora.desc()).first()
    return ultimo.stato if ultimo else None

@app.route('/api/comando_web', methods=['POST'])
def comando_web():
    global ultimo_stato
    if not request.json or 'comando' not in request.json:
        return jsonify({"errore": "Comando mancante"}), 400

    comando = request.json['comando'].upper()
    if comando not in ['ARM', 'DISARM', 'SOS']:
        return jsonify({"errore": "Comando non valido"}), 400

    try:
        if comando != ultimo_stato:
            nuovo_evento = StoricoAllarme(stato=comando)
            db.session.add(nuovo_evento)
            db.session.commit()
            ultimo_stato = comando
            print(f"[FLASK] Comando '{comando}' registrato nel DB")

        # Invio diretto seriale del comando
        successo = invia_comando_seriale(comando)
        if not successo:
            return jsonify({"errore": "Impossibile inviare il comando alla microbit"}), 500

        return jsonify({"successo": True, "stato": comando})

    except Exception as e:
        db.session.rollback()
        return jsonify({"errore": str(e)}), 500

@app.route('/api/comando_luce', methods=['POST'])
def comando_luce():
    if not request.json or 'luce_accesa' not in request.json or 'intensita' not in request.json:
        return jsonify({"errore": "Dati luce mancanti"}), 400

    luce = request.json['luce_accesa']
    intensita = request.json['intensita']

    comando = f"LUCE|{int(luce)}|{int(intensita)}"
    successo = invia_comando_seriale(comando)

    if not successo:
        return jsonify({"errore": "Invio comando fallito"}), 500

    return jsonify({"successo": True})


if __name__ == '__main__':
    app.run(debug=True)
