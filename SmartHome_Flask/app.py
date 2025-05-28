from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'smarthomedb.db')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/smarthomedb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class StoricoAllarme(db.Model):
    __tablename__ = 'StoricoAllarme'

    id = db.Column(db.Integer, primary_key=True)
    data_ora = db.Column(db.DateTime, nullable=False, default=datetime.now)
    stato = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Allarme {self.stato} @ {self.timestamp}>'

@app.route('/')
def index():
    return render_template('index.html')

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
    try:
        dati= request.get_json()

        #Controlla che tutti i campi necessari siano presenti
        richiesti= ['messaggio', 'temperatura', 'led_stato', 'potenza_led', 'colore', 'musica']
        if not all(k in dati for k in richiesti):
            return jsonify({"errore": "Campi mancanti"}), 400

        #Logica per decidere lo stato dell'allarme
        stato_corrente = None

        if dati['colore'] == 'verde':
            stato_corrente = 'DISARM'
        elif dati['colore'] == 'rosso' and dati['musica']:
            stato_corrente = 'SOS'
        elif dati['colore'] == 'rosso' and not dati['musica']:
            stato_corrente = 'ARM'

        if stato_corrente:
            #salva nel DB
            nuovo_evento = StoricoAllarme(stato=stato_corrente)
            db.session.add(nuovo_evento)
            db.session.commit()
            print(f"[FLASK] Stato allarme registrato: {stato_corrente}"), 200
            return jsonify({"successo": True, "stato": stato_corrente}), 200
        else:
            return jsonify({"errore": "Stato non riconosciuto"}), 400

    except Exception as e:
        print("[FLASK] Errore", str(e))
        return jsonify({"errore": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
