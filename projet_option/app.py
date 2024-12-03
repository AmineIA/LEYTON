from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import uuid
from user_agents import parse
from functools import wraps
import time
import logging  # Ajout du logging

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'votre_clé_secrète'

navigation_data = {}

def track_navigation():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                session['user_id'] = str(uuid.uuid4())
                session['start_time'] = time.time()
                session['page_history'] = []

            user_agent = parse(request.headers.get('User-Agent'))
            navigation_info = {
                'timestamp': datetime.now().isoformat(),
                'url': request.url,
                'referrer': request.referrer,
                'user_id': session['user_id'],
                'device': {
                    'type': 'mobile' if user_agent.is_mobile else 'tablet' if user_agent.is_tablet else 'desktop',
                    'browser': user_agent.browser.family,
                    'os': user_agent.os.family
                },
                'screen_resolution': request.headers.get('Sec-CH-UA-Platform-Version', 'unknown'),
                'session_duration': time.time() - session['start_time']
            }

            session['page_history'].append(request.url)
            navigation_info['bounce_rate'] = len(session['page_history']) == 1

            if session['user_id'] not in navigation_data:
                navigation_data[session['user_id']] = []
            navigation_data[session['user_id']].append(navigation_info)
            
            # Log pour déboguer
            logger.debug(f"Données stockées pour l'utilisateur {session['user_id']}")
            logger.debug(f"Navigation data actuelle: {navigation_data}")

            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route("/export-csv")
def export_csv():
    """Route pour exporter les données en CSV"""
    logger.debug("Tentative d'export CSV")
    logger.debug(f"Données à exporter: {navigation_data}")
    
    if not navigation_data:
        logger.warning("Aucune donnée à exporter!")
        return jsonify({"error": "Aucune donnée disponible"})
    
    try:
        from data_utils import export_to_csv
        result = export_to_csv(navigation_data)
        logger.info(f"Export réussi: {result}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Erreur lors de l'export: {str(e)}")
        return jsonify({"error": str(e)})

@app.route("/")
@track_navigation()
def home():
    return render_template("index.html", title="Accueil")

@app.route("/stats")
def get_stats():
    logger.debug(f"Données de stats demandées: {navigation_data}")
    return jsonify(navigation_data)

if __name__ == '__main__':
    # Assurez-vous que le dossier data existe
    import os
    if not os.path.exists('data'):
        os.makedirs('data')
        logger.info("Dossier 'data' créé")
    
    app.run(debug=True)





    