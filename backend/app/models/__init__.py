# Import des modèles ATARYS
# Ce fichier permet d'importer tous les modèles créés

# Module 5.1 - DEVIS-FACTURATION
try:
    from .module_5_1 import articlesatarys
except ImportError:
    pass

# Ajouter ici les autres modules au fur et à mesure du développement
# from .module_3_1 import *
# from .module_9_1 import *
# etc. 