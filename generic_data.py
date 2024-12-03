import pandas as pd
import numpy as np
import random
from faker import Faker

# Initialisation de Faker avec localisation en français
fake = Faker('fr_FR')

# Génération des données synthétiques
def generate_realistic_data(n=250):
    data = []
    for user_id in range(1, n + 1):
        # Données comportementales
        pages_visited = int(np.random.normal(loc=10, scale=5))  # Distribution normale pour les pages visitées
        pages_visited = max(1, pages_visited)  # Minimum 1 page

        total_time = int(np.random.normal(loc=600, scale=300))  # Temps passé en secondes
        total_time = max(100, total_time)  # Minimum 100 secondes

        add_to_cart = random.randint(0, min(5, pages_visited // 2))  # Ajouts au panier liés aux pages visitées
        add_to_wishlist = random.randint(0, 2) if pages_visited > 10 else 0  # Wishlist si beaucoup d'exploration
        products_viewed = random.randint(pages_visited // 2, pages_visited)  # Produits vus proportionnels
        products_bought = random.randint(0, add_to_cart)  # Achats ≤ Ajouts au panier
        promos_viewed = random.randint(0, 5) if pages_visited > 5 else 0  # Promotions consultées
        days_since_last_visit = random.randint(0, 30)  # Temps écoulé depuis la dernière visite
        traffic_source = random.choice(['Direct', 'Publicité', 'Recherche Organique', 'Réseaux Sociaux'])

        # Données utilisateur avec Faker
        full_name = fake.name()
        email = fake.email()
        country = fake.country()
        language = fake.language_name()
        registration_date = fake.date_this_year(before_today=True, after_today=False)

        # Ajouter une ligne de données
        data.append({
            "UserID": user_id,
            "NomComplet": full_name,
            "Email": email,
            "Pays": country,
            "Langue": language,
            "DateInscription": registration_date,
            "PagesVisitées": pages_visited,
            "TempsTotal (sec)": total_time,
            "AjoutPanier": add_to_cart,
            "AjoutWishlist": add_to_wishlist,
            "ProduitsConsultés": products_viewed,
            "ProduitsAchetés": products_bought,
            "PromosConsultées": promos_viewed,
            "DélaiEntreVisites (jours)": days_since_last_visit,
            "SourceTrafic": traffic_source
        })
    return pd.DataFrame(data)

# Générer et sauvegarder
df = generate_realistic_data(1000)
df.to_csv("realistic_visitors_data_enriched.csv", index=False)
print("Données enrichies sauvegardées dans 'realistic_visitors_data_enriched.csv'")
