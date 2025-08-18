import argparse
from gestion_csv import consolider_fichiers_csv
from recherche import recherche_produit, recherche_categorie, filtre_par_prix
from rapport import generer_rapport

def consolider(dossier, fichier_consolide):
    consolider_fichiers_csv(dossier, fichier_consolide)
    print(f"Fichier consolidé dans : {fichier_consolide}")

def rechercher_produit(nom_produit, fichier_consolide):
    try:
        resultat = recherche_produit(nom_produit, fichier_consolide)
        if resultat.empty:
            print(f"Produit '{nom_produit}' introuvable.")
        else:
            print(resultat)
    except FileNotFoundError:
        print(f"Fichier '{fichier_consolide}' introuvable. Veuillez d'abord consolider les fichiers CSV.")
    except KeyError:
        print("La colonne 'Nom_du_produit' est absente du fichier. Vérifiez la structure du fichier CSV.")

def rechercher_categorie(nom_categorie, fichier_consolide):
    resultat = recherche_categorie(nom_categorie, fichier_consolide)
    if resultat.empty:
        print(f"Aucun produit trouvé dans la catégorie '{nom_categorie}'.")
    else:
        print(resultat)

def filtrer_prix(prix_min, prix_max, fichier_consolide):
    if prix_min > prix_max:
        raise ValueError("Le prix minimum ne peut pas être supérieur au prix maximum.")
    resultat = filtre_par_prix(prix_min, prix_max, fichier_consolide)
    if resultat.empty:
        print(f"Aucun produit trouvé entre {prix_min} et {prix_max}.")
    else:
        print(resultat)

def generer(fichier_consolide):
    try:
        rapport = generer_rapport(fichier_consolide)
        print("Rapport généré avec succès :")
        print(rapport)
    except FileNotFoundError:
        print("Fichier consolidé introuvable. Veuillez d'abord consolider les fichiers CSV.")

def main():
    parser = argparse.ArgumentParser(description="Gestion d'inventaire en ligne de commande.")
    parser.add_argument("action", choices=["consolider", "rechercher_produit", "rechercher_categorie", "filtrer_prix", "generer"],
                        help="Action à effectuer.")
    parser.add_argument("--dossier", help="Chemin du dossier contenant les fichiers CSV (pour 'consolider').")
    parser.add_argument("--fichier_consolide", default="base_inventaire.csv", help="Chemin du fichier consolidé (par défaut : 'base_inventaire.csv').")
    parser.add_argument("--nom_produit", help="Nom du produit à rechercher (pour 'rechercher_produit').")
    parser.add_argument("--nom_categorie", help="Nom de la catégorie à rechercher (pour 'rechercher_categorie').")
    parser.add_argument("--prix_min", type=float, help="Prix minimum (pour 'filtrer_prix').")
    parser.add_argument("--prix_max", type=float, help="Prix maximum (pour 'filtrer_prix').")

    args = parser.parse_args()

    try:
        if args.action == "consolider":
            if not args.dossier:
                raise ValueError("L'argument '--dossier' est requis pour 'consolider'.")
            consolider(args.dossier, args.fichier_consolide)

        elif args.action == "rechercher_produit":
            if not args.nom_produit:
                raise ValueError("L'argument '--nom_produit' est requis pour 'rechercher_produit'.")
            rechercher_produit(args.nom_produit, args.fichier_consolide)

        elif args.action == "rechercher_categorie":
            if not args.nom_categorie:
                raise ValueError("L'argument '--nom_categorie' est requis pour 'rechercher_categorie'.")
            rechercher_categorie(args.nom_categorie, args.fichier_consolide)

        elif args.action == "filtrer_prix":
            if args.prix_min is None or args.prix_max is None:
                raise ValueError("Les arguments '--prix_min' et '--prix_max' sont requis pour 'filtrer_prix'.")
            filtrer_prix(args.prix_min, args.prix_max, args.fichier_consolide)

        elif args.action == "generer":
            generer(args.fichier_consolide)

    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    main()
