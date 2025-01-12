from gestion_csv import consolider_fichiers_csv
from recherche import recherche_produit, recherche_categorie, filtre_par_prix
from rapport import generer_rapport

def menu():
    fichier_consolide = "base_inventaire.csv"
    fichier_rapport = "rapport_inventaire.csv"
    while True:
        print("\n=== Menu Gestion d'Inventaire ===")
        print("1. Consolider les fichiers CSV")
        print("2. Rechercher un produit")
        print("3. Rechercher par catégorie")
        print("4. Filtrer les produits par prix")
        print("5. Générer un rapport d'inventaire")
        print("6. Quitter")
        
        choix = input("Choisissez une option : ")
        try:
            if choix == "1":
                dossier = input("Entrez le chemin du dossier contenant les fichiers CSV : ")
                consolider_fichiers_csv(dossier, fichier_consolide)
                print(f"Fichier consolidé dans : {fichier_consolide}")
            elif choix == "2":
                nom_produit = input("Entrez le nom du produit : ")
                print(recherche_produit(nom_produit, fichier_consolide))
            elif choix == "3":
                nom_categorie = input("Entrez le nom de la catégorie : ")
                print(recherche_categorie(nom_categorie, fichier_consolide))
            elif choix == "4":
                prix_min = float(input("Prix minimum : "))
                prix_max = float(input("Prix maximum : "))
                print(filtre_par_prix(prix_min, prix_max, fichier_consolide))
            elif choix == "5":
                rapport = generer_rapport(fichier_consolide)
                print(rapport)
            elif choix == "6":
                break
            else:
                print("Option invalide.")
        except Exception as e:
            print(f"Erreur : {e}")

if __name__ == "__main__":
    menu()
