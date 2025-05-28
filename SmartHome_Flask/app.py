import sqlite3

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'smarthomedb.db')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/smarthomedb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Variabile per tenere traccia dell'ultimo stato registrato e della temperatura
ultimo_stato = None
ultima_temperatura = None

class StoricoAllarme(db.Model):
    __tablename__ = 'StoricoAllarme'

    id = db.Column(db.Integer, primary_key=True)
    data_ora = db.Column(db.DateTime, nullable=False, default=datetime.now)
    stato = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Allarme {self.stato} @ {self.timestamp}>'

@app.route('/')
def index():
    ultimo = get_ultimo_stato()
    try:
        return render_template('index.html',ultimo=ultimo, temperatura=ultima_temperatura)
    except Exception as e:
        return f"Errore nel caricamento dello storico: {str(e)}", 500

#@app.route('/log/<stato>', methods=['POST'])
#def log_azione(stato):
#    if stato not in ['ARM', 'DISARM', 'SOS']:
#        return "Azione non valida", 400
#    else:
#        nuovo_evento = StoricoAllarme(stato=stato)
#        db.session.add(nuovo_evento)
#        db.session.commit()
#
#    return redirect(url_for('index'))

@app.route('/api/stato', methods=['POST'])
def ricevi_stato_microbit():
    global ultimo_stato  # ci serve per confrontare i cambiamenti
    global ultima_temperatura
    try:
        dati = request.get_json()


        richiesti = ['messaggio', 'temperatura', 'led_stato', 'potenza_led', 'colore', 'musica']
        if not all(k in dati for k in richiesti):
            return jsonify({"errore": "Campi mancanti"}), 400

        ultima_temperatura = dati['temperatura']

        stato_corrente = None
        if dati['colore'] == 'verde':
            stato_corrente = 'DISARM'
        elif dati['colore'] == 'rosso' and dati['musica']:
            stato_corrente = 'SOS'
        elif dati['colore'] == 'rosso' and not dati['musica']:
            stato_corrente = 'ARM'

        if stato_corrente is None:
            return jsonify({"errore": "Stato non riconosciuto"}), 400

        if stato_corrente != ultimo_stato:
            nuovo_evento = StoricoAllarme(stato=stato_corrente)
            db.session.add(nuovo_evento)
            db.session.commit()
            print(f"[FLASK] Cambio stato registrato: {stato_corrente}")
            ultimo_stato = stato_corrente  # aggiorna ultimo stato
        else:
            print(f"[FLASK] Stato invariato: {stato_corrente} (ignorato)")

        return jsonify({"successo": True, "stato": stato_corrente}), 200


    except Exception as e:
        db.session.rollback()  # buona pratica in caso di errore
        print("[FLASK] Errore", str(e))
        return jsonify({"errore": str(e)}), 500


def get_allarmi():
    return StoricoAllarme.query.order_by(StoricoAllarme.data_ora.desc()).all()

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


if __name__ == '__main__':
    app.run(debug=True)
