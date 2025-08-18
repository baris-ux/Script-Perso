# src/main.py
from gestion_csv import consolider_fichiers_csv
from recherche import recherche_produit, recherche_categorie, filtre_par_prix
from rapport import generer_rapport
import os
from pathlib import Path

# Répertoire racine du projet (là où se trouve main.py)
BASE_DIR = Path(__file__).resolve().parent.parent  # "Script-Perso"

# Dossier de sortie
OUTPUT_DIR = BASE_DIR / "data" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def project_path(path: str) -> str:
    """Retourne un chemin absolu basé sur la racine du projet."""
    return str(path) if os.path.isabs(path) else str((BASE_DIR / path).resolve())

def consolider():
    dossier = input("Chemin du dossier contenant les CSV : ") or "data/input"
    fichier = input("Nom du fichier de sortie (défaut: data/output/base_inventaire.csv) : ") or "data/output/base_inventaire.csv"

    dossier = project_path(dossier)
    fichier = project_path(fichier)

    try:
        os.makedirs(os.path.dirname(fichier), exist_ok=True)
        consolider_fichiers_csv(dossier, fichier)
        print(f"Fichier consolidé dans : {fichier}")
    except Exception as e:
        print(f"Erreur : {e}")


def rechercher_produit_menu():
    fichier = project_path(input("Chemin du fichier consolidé : ") or "data/output/base_inventaire.csv")
    nom = input("Nom du produit à rechercher : ")
    try:
        res = recherche_produit(nom, fichier)
        print(res if not res.empty else f"Produit '{nom}' introuvable.")
    except Exception as e:
        print(f"Erreur : {e}")


def rechercher_categorie_menu():
    fichier = project_path(input("Chemin du fichier consolidé : ") or "data/output/base_inventaire.csv")
    nom = input("Nom de la catégorie : ")
    try:
        res = recherche_categorie(nom, fichier)
        print(res if not res.empty else f"Aucun produit trouvé dans '{nom}'.")
    except Exception as e:
        print(f"Erreur : {e}")


def filtrer_prix_menu():
    fichier = project_path(input("Chemin du fichier consolidé : ") or "data/output/base_inventaire.csv")
    try:
        prix_min = float(input("Prix minimum : "))
        prix_max = float(input("Prix maximum : "))
        res = filtre_par_prix(prix_min, prix_max, fichier)
        print(res if not res.empty else f"Aucun produit entre {prix_min} et {prix_max}.")
    except Exception as e:
        print(f"Erreur : {e}")


def generer():
    fichier = project_path(input("Chemin du fichier consolidé : ") or "data/output/base_inventaire.csv")
    try:
        rapport = generer_rapport(fichier)
        print("\n=== 📊 RAPPORT INVENTAIRE ===")

        # Quantité par catégorie
        print("\n🔹 Quantité par catégorie :")
        for cat, qte in rapport["quantite_par_categorie"].items():
            print(f"   - {cat} : {qte}")

        # Valeur totale
        print(f"\n💰 Valeur totale du stock : {rapport['valeur_totale']} €")

        # Produit le plus cher
        produit = rapport["produit_cher"]
        print("\n🏆 Produit le plus cher :")
        print(f"   Nom        : {produit['Nom_du_produit']}")
        print(f"   Catégorie  : {produit['Categorie']}")
        print(f"   Prix       : {produit['Prix unitaire']} €")
        print(f"   Quantité   : {produit['Quantite']}")
        print(f"   Valeur tot : {produit['Valeur totale']} €")

        print("\n✅ Rapport généré avec succès\n")


         # === Export fichier (texte) ===
        chemin_rapport = project_path(
            input("Chemin du fichier rapport (défaut: data/output/rapport_inventaire.txt) : ")
            or "data/output/rapport_inventaire.txt"
        )
        os.makedirs(os.path.dirname(chemin_rapport), exist_ok=True)

        with open(chemin_rapport, "w", encoding="utf-8") as f:
            f.write("=== RAPPORT INVENTAIRE ===\n")
            f.write("\nQuantité par catégorie :\n")
            for cat, qte in rapport["quantite_par_categorie"].items():
                f.write(f"- {cat} : {qte}\n")

            f.write(f"\nValeur totale du stock : {rapport['valeur_totale']} €\n")

            produit = rapport["produit_cher"]
            f.write("\nProduit le plus cher :\n")
            f.write(f"- Nom        : {produit['Nom_du_produit']}\n")
            f.write(f"- Catégorie  : {produit['Categorie']}\n")
            f.write(f"- Prix       : {produit['Prix unitaire']} €\n")
            f.write(f"- Quantité   : {produit['Quantite']}\n")
            f.write(f"- Valeur tot : {produit['Valeur totale']} €\n")

        print(f"📝 Rapport exporté dans : {chemin_rapport}")

    except Exception as e:
        print(f"Erreur : {e}")



def afficher_menu():
    print("\n=== MENU INVENTAIRE ===")
    print("1. Consolider les fichiers CSV")
    print("2. Rechercher un produit")
    print("3. Rechercher une catégorie")
    print("4. Filtrer par prix")
    print("5. Générer un rapport")
    print("0. Quitter")


def main():
    while True:
        afficher_menu()
        choix = input("Choisissez une option : ")

        if choix == "1":
            consolider()
        elif choix == "2":
            rechercher_produit_menu()
        elif choix == "3":
            rechercher_categorie_menu()
        elif choix == "4":
            filtrer_prix_menu()
        elif choix == "5":
            generer()
        elif choix == "0":
            print("Au revoir")
            break
        else:
            print("Choix invalide, réessayez.")


if __name__ == "__main__":
    main()
