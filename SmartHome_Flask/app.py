from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/log/<stato>', methods=['POST'])
def log_azione(stato):
    if stato not in ['ARM', 'DISARM', 'SOS']:
        return "Azione non valida", 400
    else:
        nuovo_evento = StoricoAllarme(stato=stato)
        db.session.add(nuovo_evento)
        db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
