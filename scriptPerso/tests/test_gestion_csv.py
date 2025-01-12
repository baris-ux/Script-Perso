import unittest
import os
from gestion_csv import consolider_fichiers_csv

class TestGestionCSV(unittest.TestCase):
    def test_consolider_fichiers_csv(self):
        dossier_test = "data/"
        fichier_sortie = "fichier_consolide.csv"
        consolider_fichiers_csv(dossier_test, fichier_sortie)
        self.assertTrue(os.path.exists(fichier_sortie))
