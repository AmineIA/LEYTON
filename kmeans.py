from sklearn.cluster import KMeans
import pandas as pd
import pandas as pd  # Manipulation des données
from sklearn.cluster import KMeans  # Algorithme de clustering K-Means
from sklearn.preprocessing import StandardScaler  # Normalisation des données


# Charger les données
df = pd.read_csv("realistic_visitors_data.csv")

# Préparer les features (sans 'SourceTrafic' pour simplifier le clustering)
features = ['PagesVisitées', 'TempsTotal (sec)', 'AjoutPanier', 
            'AjoutWishlist', 'ProduitsConsultés', 'ProduitsAchetés', 
            'PromosConsultées', 'DélaiEntreVisites (jours)']

X = df[features]

# Normaliser les données
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Appliquer K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Assigner des labels basés sur l'analyse des clusters
cluster_labels = {
    0: "Découvreur",
    1: "Précipité",
    2: "Chercheur des bonnes affaires"
}
df['Persona'] = df['Cluster'].map(cluster_labels)

# Sauvegarder les résultats
df.to_csv("clustered_visitors_data.csv", index=False)
print("Données segmentées sauvegardées dans 'clustered_visitors_data.csv'")
