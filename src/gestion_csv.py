import pandas as pd
import glob

def consolider_fichiers_csv(dossier_csv, fichier_sortie):
    """Consolide les fichiers CSV dans un seul fichier.

    Préconditions:
    - dossier_csv existe et contient au moins un fichier csv lisible
    - Les fichiers CSV sont encodés en UTF-8 et séparés par ';'

    Post :
    - fichier_sortie est créé 
    - Les lignes dupliquées ont été **supprimées** (dédoublonnage).
    - fichier_sortie est créé en UTF-8, séparé par ';'
    - L'ordre des colonnes est conservé en sorti ;

    Exceptions:
    - FileNotFoundError : aucun fichier *.csv trouvé dans `dossier_csv`.
    - ValueError        : tous les *.csv trouvés sont vides.
    - PermissionError   : écriture impossible dans `fichier_sortie`.
    
    
    """
    fichiers_csv = glob.glob(f"{dossier_csv}/*.csv")
    if not fichiers_csv:
        raise FileNotFoundError("Aucun fichier CSV trouvé dans le dossier spécifié.")
    
    try:
        dataframes = []
        for fichier in fichiers_csv:
            df = pd.read_csv(fichier, sep=';', encoding='utf-8')
            if df.empty:
                print(f"Attention : Le fichier '{fichier}' est vide et sera ignoré.")
            else:
                dataframes.append(df)
        
        if not dataframes:
            raise ValueError("Tous les fichiers CSV dans le dossier sont vides.")
        
        df_consolide = pd.concat(dataframes, ignore_index=True).drop_duplicates()
        df_consolide.to_csv(fichier_sortie, sep=';', index=False, encoding='utf-8')
        return fichier_sortie
    except PermissionError:
        raise PermissionError(f"Impossible d'écrire dans le fichier de sortie : {fichier_sortie}. Vérifiez les permissions.")
