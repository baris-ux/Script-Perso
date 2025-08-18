import pandas as pd

def recherche_produit(nom_produit, fichier_csv):
    """
    Recherche les produits par nom dans un fichier CSV

    Préconditions : 
    - fichier_csv existe et est lisible
    - Le fichier contient la colonne 'Nom_du_produit'
    - nom_produit est une chaine non vide
    
    Postconditions : 
    - Le type de retour est un pandas.DataFrame (même si vide)
    - Le DataFrame retourné contient uniquement des lignes avec 'Nom_du_produit' correspondant au filtre

    Exceptions :
    - FileNotFoundError : fichier introuvable
    - KeyError : colonne 'Nom_du_produit' manquante
    
    """
    df = pd.read_csv(fichier_csv, sep=';', encoding='utf-8')
    return df[df['Nom_du_produit'].str.contains(nom_produit, case=False, na=False)]

def recherche_categorie(nom_categorie, fichier_csv):
    """
    Préconditions :
    - fichier_csv existe et est lisible
    - Le fichier contient la colonne 'Categorie'
    - nom_categorie est une chaîne non vide

    Postconditions :
    - Retourne un pandas.DataFrame (même si vide)
    - Le DataFrame retourné contient uniquement des lignes dont 'Categorie'
      correspond au filtre (recherche insensible à la casse)

      
    Exceptions :
    - FileNotFoundError : si le fichier CSV est introuvable
    - KeyError : si la colonne 'Categorie' est absente
    """
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
