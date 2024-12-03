import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# --- Étape 1 : Charger les données ---
df = pd.read_csv("synthetic_visitors_data.csv")

# --- Étape 2 : Ajouter les labels (classification basée sur règles) ---
def classify_persona(row):
    if row['PagesVisitées'] > 15 and row['TempsTotal (sec)'] > 800 and row['AjoutWishlist'] > 0:
        return 'Découvreur'
    elif row['AjoutPanier'] > 1 and row['TempsTotal (sec)'] < 600 and row['PagesVisitées'] < 10:
        return 'Précipité'
    elif row['PromosConsultées'] > 0 and row['DélaiEntreVisites (jours)'] > 10:
        return 'Chercheur des bonnes affaires'
    else:
        return 'Autres'

df['Persona'] = df.apply(classify_persona, axis=1)

# --- Étape 3 : Préparer les features (X) et labels (y) ---
# Encoder la colonne catégorique 'SourceTrafic'
label_encoder = LabelEncoder()
df['SourceTrafic'] = label_encoder.fit_transform(df['SourceTrafic'])

# Features sélectionnées
features = ['PagesVisitées', 'TempsTotal (sec)', 'AjoutPanier', 
            'AjoutWishlist', 'ProduitsConsultés', 'ProduitsAchetés', 
            'PromosConsultées', 'DélaiEntreVisites (jours)', 'SourceTrafic']

X = df[features]

# Labels (Persona)
y = df['Persona']

# Standardiser les features numériques pour le modèle
scaler = StandardScaler()
X = scaler.fit_transform(X)

# --- Étape 4 : Diviser les données en jeu d'entraînement et de test ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Étape 5 : Entraîner le modèle Random Forest ---
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# --- Étape 6 : Faire des prédictions ---
y_pred = model.predict(X_test)

# --- Étape 7 : Évaluer les performances ---
print("Rapport de classification :\n", classification_report(y_test, y_pred))
print("Matrice de confusion :\n", confusion_matrix(y_test, y_pred))

# --- Visualisation de la matrice de confusion ---
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
plt.title("Matrice de confusion")
plt.xlabel("Prédictions")
plt.ylabel("Vrais labels")
plt.show()

# --- Étape 8 : Sauvegarder le modèle pour usage futur ---
import joblib
joblib.dump(model, "persona_model.pkl")
print("Modèle sauvegardé sous le nom 'persona_model.pkl'")
