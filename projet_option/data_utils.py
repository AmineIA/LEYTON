import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def export_to_csv(navigation_data):
    """Exporte les données de navigation en CSV"""
    if not navigation_data:
        return {"error": "Aucune donnée disponible"}

    # Préparer les données pour le CSV
    csv_data = []
    for user_id, visits in navigation_data.items():
        for visit in visits:
            row = {
                'user_id': visit['user_id'],
                'timestamp': visit['timestamp'],
                'url': visit['url'],
                'referrer': visit['referrer'],
                'device_type': visit['device']['type'],
                'browser': visit['device']['browser'],
                'os': visit['device']['os'],
                'screen_resolution': visit['screen_resolution'],
                'session_duration': visit['session_duration'],
                'bounce_rate': visit['bounce_rate']
            }
            csv_data.append(row)

    # Créer un DataFrame pandas
    df = pd.DataFrame(csv_data)
    
    # Générer un nom de fichier unique avec la date
    filename = f"navigation_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    # Sauvegarder en CSV
    df.to_csv(f'data/{filename}', index=False)
    
    return {
        "status": "success",
        "message": f"Données exportées dans {filename}",
        "filename": filename
    }

def prepare_data_for_ml(filename):
    """Prépare les données pour le machine learning"""
    df = pd.read_csv(f'data/{filename}')
    
    le = LabelEncoder()
    df['device_type_encoded'] = le.fit_transform(df['device_type'])
    df['browser_encoded'] = le.fit_transform(df['browser'])
    df['os_encoded'] = le.fit_transform(df['os'])
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    
    features = ['device_type_encoded', 'browser_encoded', 'os_encoded', 
                'session_duration', 'hour', 'day_of_week']
    
    X = df[features]
    y = df['bounce_rate']
    
    return train_test_split(X, y, test_size=0.2) 