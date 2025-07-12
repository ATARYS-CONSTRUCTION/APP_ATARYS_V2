# Import des modèles ATARYS
# Ce fichier permet d'importer tous les modèles créés

# Module 5.1 - DEVIS-FACTURATION
try:
    from .module_5_1 import ArticlesAtarys
except ImportError:
    pass

# MODELE_ARDOISES (généré automatiquement)
try:
    from .modele_ardoises_model import ModeleArdoises
except ImportError:
    pass

# Ajouter ici les autres modules au fur et à mesure du développement
# from .module_3_1 import *
# from .module_9_1 import *
# etc.

# ARTICLES_ATARYS
try:
    from .articles_atarys_model import ArticlesAtarys
except ImportError:
    pass

# MODELE_ARDOISES
try:
    from .modele_ardoises_model import ModeleArdoises
except ImportError:
    pass
