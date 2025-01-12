import unittest
from recherche import recherche_produit

class TestRecherche(unittest.TestCase):
    def test_recherche_produit(self):
        fichier_test = "data/test_inventaire.csv"
        result = recherche_produit("ProduitX", fichier_test)
        self.assertFalse(result.empty)
