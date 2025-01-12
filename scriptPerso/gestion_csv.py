import pandas as pd
import glob

def consolider_fichiers_csv(dossier_csv, fichier_sortie):
    """Consolide les fichiers CSV dans un seul fichier."""
    fichiers_csv = glob.glob(f"{dossier_csv}/*.csv") # d'abord on cherche les fichiers csv grace au chemin passé par le user
    if not fichiers_csv:
        raise FileNotFoundError("Aucun fichier CSV trouvé dans le dossier.")
    
    dataframes = [pd.read_csv(fichier, sep=';', encoding='utf-8') for fichier in fichiers_csv]
    df_consolide = pd.concat(dataframes, ignore_index=True).drop_duplicates()
    df_consolide.to_csv(fichier_sortie, sep=';', index=False, encoding='utf-8')
    return fichier_sortie
