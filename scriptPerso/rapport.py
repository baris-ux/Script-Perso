import pandas as pd

def generer_rapport(fichier_csv):
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
