from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50), nullable=False)
    time_spent = db.Column(db.Float, nullable=True)
    product = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.String(50), nullable=True)

# Créer les tables si elles n'existent pas
with app.app_context():
    db.create_all()

# Routes pour les pages
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/track-event', methods=['POST'])
def track_event():
    data = request.json
    print(f"Event received: {data}")

    # Ajouter un nouvel événement dans la base de données
    event_name = data.get('event', 'unknown_event')
    time_spent = data.get('timeSpent', None)
    product = data.get('product', 'N/A')
    price = data.get('price', None)
    timestamp = data.get('timestamp', None)

    new_event = Event(
        event_name=event_name,
        time_spent=time_spent,
        product=product,
        price=price,
        timestamp=timestamp
    )
    db.session.add(new_event)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Event saved!'})

@app.route('/view-events')
def view_events():
    # Récupérer tous les événements dans la base de données
    events = Event.query.all()

    # Générer une liste de dictionnaires à partir des objets Event
    event_list = [
        {'id': event.id, 'event_name': event.event_name, 'time_spent': event.time_spent}
        for event in events
    ]

    # Retourner les données à une page HTML
    return render_template('view_events.html', events=event_list)


import csv
from flask import Response

@app.route('/export-events', methods=['GET'])
def export_events():
    # Récupérer tous les événements de la base de données
    events = Event.query.all()

    # Créer un fichier CSV en mémoire
    def generate_csv():
        # Définir l'en-tête
        yield 'ID,Event Name,Time Spent\n'

        # Ajouter les données
        for event in events:
            yield f'{event.id},{event.event_name},{event.time_spent or "N/A"}\n'

    # Retourner le fichier CSV comme une réponse HTTP
    return Response(
        generate_csv(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=events.csv'
        }
    )

if __name__ == '__main__':
    app.run(debug=True)
