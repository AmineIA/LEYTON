import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

# Load the clustered data
df = pd.read_csv("clustered_visitors_data.csv")

# --- Scatter plot of two features ---
plt.figure(figsize=(8, 6))
sns.scatterplot(
    x="PagesVisitées", 
    y="TempsTotal (sec)", 
    hue="Persona", 
    data=df, 
    palette="Set2",
    s=100
)
plt.title("Clustered Personas: Pages Visited vs. Total Time", fontsize=16)
plt.xlabel("Pages Visited")
plt.ylabel("Total Time (sec)")
plt.legend(title="Persona")
plt.show()

# --- Feature importance (box plots for each persona) ---
features = ["PagesVisitées", "AjoutPanier", "ProduitsAchetés", "PromosConsultées"]

for feature in features:
    plt.figure(figsize=(8, 6))
    sns.boxplot(x="Persona", y=feature, data=df, palette="Set3")
    plt.title(f"Distribution of {feature} Across Personas", fontsize=16)
    plt.xlabel("Persona")
    plt.ylabel(feature)
    plt.show()

# --- PCA for dimensionality reduction (optional) ---
# Select numerical features for clustering
features = ['PagesVisitées', 'TempsTotal (sec)', 'AjoutPanier', 
            'AjoutWishlist', 'ProduitsConsultés', 'ProduitsAchetés', 
            'PromosConsultées', 'DélaiEntreVisites (jours)']

X = df[features]

# Normalize the features
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Reduce to 2D using PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Add PCA components to the DataFrame
df['PCA1'] = X_pca[:, 0]
df['PCA2'] = X_pca[:, 1]

# Plot PCA results
plt.figure(figsize=(8, 6))
sns.scatterplot(
    x="PCA1", 
    y="PCA2", 
    hue="Persona", 
    data=df, 
    palette="Set2", 
    s=100
)
plt.title("Clustered Personas in PCA Space", fontsize=16)
plt.xlabel("PCA1")
plt.ylabel("PCA2")
plt.legend(title="Persona")
plt.show()
