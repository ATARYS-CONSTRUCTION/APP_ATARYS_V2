"""
Module 3 - Modèles SQLAlchemy - LISTE_CHANTIERS
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

# Modèles du module 3 - LISTE_CHANTIERS
# Ajouter ici les modèles du module 3 selon les besoins
