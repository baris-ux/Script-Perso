# src/main.py
from gestion_csv import consolider_fichiers_csv
from recherche import recherche_produit, recherche_categorie, filtre_par_prix
from rapport import generer_rapport


def consolider():
    dossier = input("Chemin du dossier contenant les CSV : ")
    fichier = input("Nom du fichier de sortie (défaut: base_inventaire.csv) : ") or "base_inventaire.csv"
    try:
        consolider_fichiers_csv(dossier, fichier)
        print(f"Fichier consolidé dans : {fichier}")
    except Exception as e:
        print(f"Erreur : {e}")


def rechercher_produit_menu():
    fichier = input("Chemin du fichier consolidé : ") or "base_inventaire.csv"
    nom = input("Nom du produit à rechercher : ")
    try:
        res = recherche_produit(nom, fichier)
        print(res if not res.empty else f"Produit '{nom}' introuvable.")
    except Exception as e:
        print(f"Erreur : {e}")


def rechercher_categorie_menu():
    fichier = input("Chemin du fichier consolidé : ") or "base_inventaire.csv"
    nom = input("Nom de la catégorie : ")
    try:
        res = recherche_categorie(nom, fichier)
        print(res if not res.empty else f"Aucun produit trouvé dans '{nom}'.")
    except Exception as e:
        print(f"Erreur : {e}")


def filtrer_prix_menu():
    fichier = input("Chemin du fichier consolidé : ") or "base_inventaire.csv"
    try:
        prix_min = float(input("Prix minimum : "))
        prix_max = float(input("Prix maximum : "))
        res = filtre_par_prix(prix_min, prix_max, fichier)
        print(res if not res.empty else f"Aucun produit entre {prix_min} et {prix_max}.")
    except Exception as e:
        print(f"Erreur : {e}")


def generer():
    fichier = input("Chemin du fichier consolidé : ") or "base_inventaire.csv"
    try:
        rapport = generer_rapport(fichier)
        print("Rapport généré :")
        print(rapport)
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
