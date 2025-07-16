"""
Module 2 - Modèles SQLAlchemy - LISTE_DES_TACHES
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Hérite toujours de BaseModel
- Utilise db.Numeric(10, 2) pour montants financiers
- Strings avec longueur max obligatoire
- __repr__ explicite
"""
from app.models.base import BaseModel
from app import db
from datetime import datetime

# Modèles du module 2 - LISTE_DES_TACHES
# Ajouter ici les modèles du module 2 selon les besoins
