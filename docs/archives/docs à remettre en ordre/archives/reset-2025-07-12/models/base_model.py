"""
Fichier de compatibilité pour les imports de base_model.
Tous les modèles devraient être mis à jour pour importer depuis base.py directement.
"""
from .base import BaseModel

# Pour la rétrocompatibilité
__all__ = ['BaseModel']
