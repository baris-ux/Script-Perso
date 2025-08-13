import pandas as pd

def generer_rapport(fichier_csv):
    """
    Préconditions :
    - fichier_csv existe et est lisible
    - Le fichier contient au minimum les colonnes :
      'Categorie', 'Quantite', 'Prix unitaire'

    Postconditions :
    - Le dictionnaire retourné contient :
        {
            "quantite_par_categorie": pandas.Series,
            "valeur_totale": float,
            "produit_cher": pandas.Series
        }

    Invariant :
    - Le fichier source reste inchangé

    Exceptions :
    - FileNotFoundError : fichier introuvable
    - KeyError : colonnes attendues manquantes
    """
    df = pd.read_csv(fichier_csv, sep=';', encoding='utf-8')
    quantite_par_categorie = df.groupby("Categorie")["Quantite"].sum()
    df['Valeur totale'] = df['Quantite'] * df['Prix unitaire']
    valeur_totale = df['Valeur totale'].sum()
    produit_cher = df.loc[df['Prix unitaire'].idxmax()]
    return {
        "quantite_par_categorie": quantite_par_categorie,
        "valeur_totale": valeur_totale,
        "produit_cher": produit_cher
    }
