from data_utils import prepare_data_for_ml
from sklearn.ensemble import RandomForestClassifier

def analyze_navigation_data(filename):
    # Préparer les données
    X_train, X_test, y_train, y_test = prepare_data_for_ml(filename)
    
    # Exemple d'utilisation avec Random Forest
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    
    # Évaluer le modèle
    score = model.score(X_test, y_test)
    print(f"Précision du modèle : {score:.2f}")

if __name__ == "__main__":
    # Remplacez par votre fichier CSV le plus récent
    analyze_navigation_data("navigation_data_20240101_120000.csv") 