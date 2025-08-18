import unittest
from rapport import generer_rapport

class TestRapport(unittest.TestCase):
    def test_generer_rapport(self):
        fichier_test = "data/test_inventaire.csv"
        rapport = generer_rapport(fichier_test)
        self.assertIn("quantite_par_categorie", rapport)
        self.assertIn("valeur_totale", rapport)
