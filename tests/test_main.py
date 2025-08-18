# tests/test_main_cli.py
import builtins
import os
import pandas as pd
import main

# Helper pour simuler une séquence d'inputs utilisateur
def _seq(*answers):
    it = iter(answers)
    return lambda _: next(it)

# ------------------ utilitaires ------------------

def test_project_path_rel_et_abs(tmp_path):
    # Chemin absolu -> renvoyé tel quel
    abs_path = str((tmp_path / "x").resolve())
    assert main.project_path(abs_path) == abs_path

    # Chemin relatif -> résolu sous BASE_DIR
    rel = "data/output/sub"
    assert main.project_path(rel).endswith(rel.replace("/", os.sep))

def test_afficher_menu_affiche_titre(capsys):
    main.afficher_menu()
    out = capsys.readouterr().out
    assert "MENU INVENTAIRE" in out

def test_menu_quitter(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", _seq("0"))
    main.main()
    out = capsys.readouterr().out
    assert "Au revoir" in out

# ------------------ option 1 : consolider ------------------

def test_menu_option_1_consolider_succes(monkeypatch, capsys, tmp_path):
    in_dir = tmp_path / "in"
    out_file = tmp_path / "out" / "base.csv"
    in_dir.mkdir(parents=True, exist_ok=True)

    called = {}
    def fake_consolider_fichiers_csv(dossier, fichier):
        called["dossier"] = dossier
        called["fichier"] = fichier

    monkeypatch.setattr("main.consolider_fichiers_csv", fake_consolider_fichiers_csv)
    monkeypatch.setattr(builtins, "input", _seq("1", str(in_dir), str(out_file), "0"))

    main.main()
    out = capsys.readouterr().out
    assert "Fichier consolidé dans" in out
    assert called["dossier"] == str(in_dir)
    assert called["fichier"] == str(out_file)

def test_menu_option_1_consolider_erreur(monkeypatch, capsys, tmp_path):
    in_dir = tmp_path / "in"
    out_file = tmp_path / "out" / "base.csv"
    in_dir.mkdir(parents=True, exist_ok=True)

    def boom(*args, **kwargs):
        raise RuntimeError("kaboom")

    monkeypatch.setattr("main.consolider_fichiers_csv", lambda *a, **k: boom())
    monkeypatch.setattr(builtins, "input", _seq("1", str(in_dir), str(out_file), "0"))

    main.main()
    out = capsys.readouterr().out
    assert "Erreur :" in out and "kaboom" in out

# ------------------ option 2 : rechercher produit ------------------

def test_menu_option_2_rechercher_produit_introuvable(monkeypatch, capsys, tmp_path):
    # Mock : renvoie DataFrame vide
    monkeypatch.setattr("main.recherche_produit", lambda nom, f: pd.DataFrame())

    csvfile = tmp_path / "base.csv"
    csvfile.write_text("Nom_du_produit;Categorie;Quantite;Prix unitaire\n", encoding="utf-8")

    monkeypatch.setattr(builtins, "input", _seq("2", str(csvfile), "ProduitInexistant123", "0"))
    main.main()
    out = capsys.readouterr().out.lower()
    assert "introuvable" in out

def test_menu_option_2_rechercher_produit_trouve(monkeypatch, capsys, tmp_path):
    df = pd.DataFrame([{"Nom_du_produit": "USB-C Cable", "Categorie": "Elec", "Quantite": 1, "Prix unitaire": 9.9}])
    monkeypatch.setattr("main.recherche_produit", lambda nom, f: df)

    csvfile = tmp_path / "base.csv"
    csvfile.write_text("Nom_du_produit;Categorie;Quantite;Prix unitaire\n", encoding="utf-8")

    monkeypatch.setattr(builtins, "input", _seq("2", str(csvfile), "usb", "0"))
    main.main()
    out = capsys.readouterr().out
    assert "USB-C Cable" in out

def test_menu_option_2_rechercher_produit_exception(monkeypatch, capsys, tmp_path):
    def boom(*args, **kwargs):
        raise RuntimeError("erreur simulée")
    monkeypatch.setattr("main.recherche_produit", boom)

    csvfile = tmp_path / "base.csv"
    csvfile.write_text("Nom_du_produit;Categorie;Quantite;Prix unitaire\n", encoding="utf-8")

    monkeypatch.setattr(builtins, "input", _seq("2", str(csvfile), "usb", "0"))
    main.main()
    out = capsys.readouterr().out
    assert "Erreur :" in out and "erreur simulée" in out

# ------------------ option 3 : rechercher catégorie ------------------

def test_menu_option_3_rechercher_categorie_trouve(monkeypatch, capsys, tmp_path):
    df = pd.DataFrame([{"Nom_du_produit": "Pâtes", "Categorie": "Epicerie", "Quantite": 2, "Prix unitaire": 1.2}])
    monkeypatch.setattr("main.recherche_categorie", lambda nom, f: df)

    csvfile = tmp_path / "base.csv"
    csvfile.write_text("Nom_du_produit;Categorie;Quantite;Prix unitaire\n", encoding="utf-8")

    monkeypatch.setattr(builtins, "input", _seq("3", str(csvfile), "epicerie", "0"))
    main.main()
    out = capsys.readouterr().out
    assert "Pâtes" in out

def test_menu_option_3_rechercher_categorie_aucun(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr("main.recherche_categorie", lambda nom, f: pd.DataFrame())

    csvfile = tmp_path / "base.csv"
    csvfile.write_text("Nom_du_produit;Categorie;Quantite;Prix unitaire\n", encoding="utf-8")

    monkeypatch.setattr(builtins, "input", _seq("3", str(csvfile), "epicerie", "0"))
    main.main()
    out = capsys.readouterr().out.lower()
    assert "aucun produit" in out

def test_menu_option_3_rechercher_categorie_exception(monkeypatch, capsys, tmp_path):
    def boom(*args, **kwargs):
        raise ValueError("boom cat")
    monkeypatch.setattr("main.recherche_categorie", boom)

    csvfile = tmp_path / "base.csv"
    csvfile.write_text("Nom_du_produit;Categorie;Quantite;Prix unitaire\n", encoding="utf-8")

    monkeypatch.setattr(builtins, "input", _seq("3", str(csvfile), "cat", "0"))
    main.main()
    out = capsys.readouterr().out
    assert "Erreur :" in out and "boom cat" in out

# ------------------ option 4 : filtrer par prix ------------------

def test_menu_option_4_filtrer_prix(monkeypatch, capsys, tmp_path):
    csvfile = tmp_path / "base.csv"
    pd.DataFrame(
        [
            ["ProdA", "Cat", 1, 5.0],
            ["ProdB", "Cat", 1, 10.0],
            ["ProdC", "Cat", 1, 15.0],
        ],
        columns=["Nom_du_produit", "Categorie", "Quantite", "Prix unitaire"]
    ).to_csv(csvfile, sep=";", index=False, encoding="utf-8")

    monkeypatch.setattr(builtins, "input", _seq("4", str(csvfile), "5", "10", "0"))
    main.main()
    out = capsys.readouterr().out
    assert "ProdA" in out and "ProdB" in out and "ProdC" not in out

def test_menu_option_4_filtrer_prix_aucun(monkeypatch, capsys, tmp_path):
    csvfile = tmp_path / "base.csv"
    pd.DataFrame(
        [["Unique", "Cat", 1, 5.0]],
        columns=["Nom_du_produit", "Categorie", "Quantite", "Prix unitaire"]
    ).to_csv(csvfile, sep=";", index=False, encoding="utf-8")

    monkeypatch.setattr(builtins, "input", _seq("4", str(csvfile), "6", "10", "0"))
    main.main()
    out = capsys.readouterr().out
    assert "Aucun produit entre 6.0 et 10.0" in out

def test_menu_option_4_filtrer_prix_exception(monkeypatch, capsys, tmp_path):
    def boom(*args, **kwargs):
        raise KeyError("err prix")
    monkeypatch.setattr("main.filtre_par_prix", boom)

    csvfile = tmp_path / "base.csv"
    csvfile.write_text("Nom_du_produit;Categorie;Quantite;Prix unitaire\n", encoding="utf-8")

    monkeypatch.setattr(builtins, "input", _seq("4", str(csvfile), "1", "2", "0"))
    main.main()
    out = capsys.readouterr().out
    assert "Erreur :" in out and "err prix" in out

# ------------------ option 5 : générer rapport ------------------

def test_menu_option_5_generer_rapport_succes(monkeypatch, capsys, tmp_path):
    fake_report = {
        "quantite_par_categorie": {"Electronique": 10, "Epicerie": 5},
        "valeur_totale": 123.45,
        "produit_cher": {
            "Nom_du_produit": "Laptop Pro",
            "Categorie": "Electronique",
            "Prix unitaire": 1999.0,
            "Quantite": 1,
            "Valeur totale": 1999.0,
        },
    }
    monkeypatch.setattr("main.generer_rapport", lambda _: fake_report)

    csv_in = tmp_path / "base.csv"     # pas réellement utilisé (on mocke)
    report_out = tmp_path / "out" / "rapport.txt"

    monkeypatch.setattr(builtins, "input", _seq("5", str(csv_in), str(report_out), "0"))
    main.main()
    out = capsys.readouterr().out

    assert "RAPPORT INVENTAIRE" in out
    assert "Valeur totale du stock : 123.45" in out
    assert "Laptop Pro" in out

    content = report_out.read_text(encoding="utf-8")
    assert "Laptop Pro" in content and "123.45" in content

def test_menu_option_5_generer_rapport_exception(monkeypatch, capsys, tmp_path):
    def boom(*args, **kwargs):
        raise ValueError("raté")
    monkeypatch.setattr("main.generer_rapport", boom)

    csv_in = tmp_path / "base.csv"
    report_out = tmp_path / "out" / "rapport.txt"

    monkeypatch.setattr(builtins, "input", _seq("5", str(csv_in), str(report_out), "0"))
    main.main()
    out = capsys.readouterr().out
    assert "Erreur :" in out and "raté" in out
