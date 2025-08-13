import pandas as pd

def recherche_produit(nom_produit, fichier_csv):
    df = pd.read_csv(fichier_csv, sep=';', encoding='utf-8')
    return df[df['Nom_du_produit'].str.contains(nom_produit, case=False, na=False)]

def recherche_categorie(nom_categorie, fichier_csv):
    df = pd.read_csv(fichier_csv, sep=';', encoding='utf-8')
    return df[df['Categorie'].str.contains(nom_categorie, case=False, na=False)]

def filtre_par_prix(prix_min, prix_max, fichier_csv):
    """
    Filtre les produits selon un intervalle de prix 

    Pré :
    - le fichier_csv existe
    - 0 <= prix_min <= prix_max
    - Colonne 'Prix unitaire' est présente

    Post : 
    - Toutes les lignes retournées ont un prix compris entre [prix_min, prix_max]
    """
    df = pd.read_csv(fichier_csv, sep=';', encoding='utf-8')
    return df[(df['Prix unitaire'] >= prix_min) & (df['Prix unitaire'] <= prix_max)]
