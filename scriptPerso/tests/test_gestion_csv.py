# tests/test_gestion_csv_edges.py
from pathlib import Path
import csv
import pytest

from gestion_csv import consolider_fichiers_csv


def test_consolider_aucun_csv(tmp_path: Path):
    """Dossier vide -> doit lever FileNotFoundError (couvre la condition ligne 8)."""
    d = tmp_path / "vide"
    d.mkdir()
    out = tmp_path / "base.csv"
    with pytest.raises(FileNotFoundError):
        consolider_fichiers_csv(d, out)


def test_consolider_tous_csv_vides_declenche_valueerror(tmp_path: Path):
    """Tous les CSV ne contiennent que l'entête -> ValueError (couvre la condition 'not dataframes')."""
    d = tmp_path / "in"
    d.mkdir()

    headers = ["Nom_du_produit", "Categorie", "Quantite", "Prix_unitaire"]
    for i in range(2):
        p = d / f"empty{i}.csv"
        with p.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(headers)  # entête seule -> df.empty == True

    out = tmp_path / "base.csv"
    with pytest.raises(ValueError):
        consolider_fichiers_csv(d, out)


def test_consolider_avec_un_fichier_vide_affiche_warning_et_ecrit_out(tmp_path: Path, capsys):
    """Un CSV vide est ignoré (warning), un CSV valide est conservé et le fichier de sortie est créé."""
    d = tmp_path / "in"
    d.mkdir()

    headers = ["Nom_du_produit", "Categorie", "Quantite", "Prix_unitaire"]

    # CSV vide (entête seulement) -> doit afficher un avertissement
    p_empty = d / "empty.csv"
    with p_empty.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(headers)

    # CSV valide (1 ligne)
    p_ok = d / "ok.csv"
    with p_ok.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(headers)
        w.writerow(["USB-C Cable", "Electronique", 10, 9.9])

    out = tmp_path / "base.csv"
    consolider_fichiers_csv(d, out)

    # Vérifie le warning
    captured = capsys.readouterr()
    assert "sera ignoré" in captured.out

    # Vérifie que le fichier de sortie existe et n'est pas vide
    assert out.exists() and out.stat().st_size > 0

    # Vérifie que la ligne valide est bien dedans (optionnel)
    content = out.read_text(encoding="utf-8")
    assert "USB-C Cable" in content


def test_consolider_permission_error(tmp_path: Path, monkeypatch):
    """Simule une PermissionError sur l'écriture du CSV de sortie."""
    import pandas as pd  # import local pour monkeypatcher proprement

    d = tmp_path / "in"
    d.mkdir()
    # CSV minimal valide
    (d / "data.csv").write_text(
        "Nom_du_produit;Categorie;Quantite;Prix_unitaire\nA;X;1;1.0\n", encoding="utf-8"
    )
    out = tmp_path / "base.csv"

    # Monkeypatch DataFrame.to_csv pour forcer une PermissionError
    original_to_csv = pd.DataFrame.to_csv

    def boom(*args, **kwargs):
        raise PermissionError("simulé")

    monkeypatch.setattr(pd.DataFrame, "to_csv", boom)
    try:
        with pytest.raises(PermissionError):
            consolider_fichiers_csv(d, out)
    finally:
        # Restaure pour ne pas impacter les autres tests
        monkeypatch.setattr(pd.DataFrame, "to_csv", original_to_csv)
