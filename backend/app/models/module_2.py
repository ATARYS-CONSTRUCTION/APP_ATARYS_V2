"""
Module 2 - Modèles SQLAlchemy - ÉCHÉANCES
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Hérite toujours de BaseModel
- Utilise db.Numeric(10, 2) pour montants financiers
- Strings avec longueur max obligatoire
- __repr__ explicite
"""

from datetime import datetime

from app import db
from app.models.base import BaseModel


# Les modèles seront créés selon vos besoins spécifiques
# et uniquement après validation explicite
