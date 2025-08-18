import pytest
import pandas as pd
from recherche import recherche_produit, recherche_categorie, filtre_par_prix

# 1) Fichier introuvable -> couvre la branche d'erreur de lecture
def test_recherche_produit_fichier_introuvable():
    with pytest.raises(FileNotFoundError):
        recherche_produit("USB", "inexistant.csv")

# 2) Colonne 'Nom_du_produit' absente -> KeyError
def test_recherche_produit_colonne_absente(tmp_path):
    bad = tmp_path / "bad.csv"
    # on ne met PAS la colonne Nom_du_produit exprès
    pd.DataFrame(
        [["USB", 10, "Elec"]],
        columns=["AutreCol", "Quantité", "Categorie"],
    ).to_csv(bad, sep=";", index=False, encoding="utf-8")
    with pytest.raises(KeyError):
        recherche_produit("USB", str(bad))

# 3) Colonne 'Prix unitaire' absente -> KeyError
def test_filtre_par_prix_colonne_absente(tmp_path):
    bad = tmp_path / "bad.csv"
    pd.DataFrame(
        [["USB", 10, "Elec"]],
        columns=["Nom_du_produit", "Quantité", "Categorie"],  # manque Prix unitaire
    ).to_csv(bad, sep=";", index=False, encoding="utf-8")
    with pytest.raises(KeyError):
        filtre_par_prix(1, 10, str(bad))

# 4) Happy path complet (produit, catégorie, prix)
def test_recherche_happy_path(tmp_path):
    base = tmp_path / "base.csv"
    pd.DataFrame(
        [
            ["Clé USB 32GB", 150, 6.0, "Electronics"],
            ["Pâtes 500g", 200, 1.2, "Grocery"],
        ],
        columns=["Nom_du_produit", "Quantité", "Prix unitaire", "Categorie"],
    ).to_csv(base, sep=";", index=False, encoding="utf-8")

    # produit
    res_p = recherche_produit("usb", str(base))
    assert not res_p.empty
    assert res_p["Nom_du_produit"].str.contains("USB", case=False).all()

    # categorie
    res_c = recherche_categorie("grocery", str(base))
    assert not res_c.empty
    assert res_c["Categorie"].str.contains("grocery", case=False).all()

    # prix
    res_f = filtre_par_prix(1.0, 6.0, str(base))
    assert not res_f.empty
    assert res_f["Prix unitaire"].between(1.0, 6.0).all()
