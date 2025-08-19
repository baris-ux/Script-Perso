# Script-Perso

ScriptPerso est un outil de gestion d'inventaire basé sur des fichiers CSV.  
Il permet de consolider les fichiers de données, de rechercher des produits ou des catégories, de filtrer les articles par prix, et de générer des rapports d'inventaire exportables.

---

## vidéo de démo

https://www.youtube.com/watch?v=gFHMQWQO1-M

## Fonctionnalités

- **Consolidation des fichiers CSV** : fusionne plusieurs fichiers CSV en un seul fichier, avec suppression des doublons.  
- **Recherche** :
  - par produit (nom partiel ou complet)
  - par catégorie
- **Filtrage par prix** : affiche les produits compris dans une plage de prix donnée (prix min / prix max).  
- **Rapports** :
  - Quantité totale par catégorie
  - Valeur totale des stocks
  - Produit le plus cher

---

## Prérequis

- **Python 3.x**
- Bibliothèques Python :
  - `pandas`
- (optionnel) `pytest` pour exécuter les tests unitaires

---

## 🛠️ Installation

```bash
git clone https://github.com/baris-ux/Script-Perso
cd Script-Perso
pip install -r requirements.txt```

## 🚀 Utilisation
Depuis la racine du projet :
```bash
cd src
python main.py
