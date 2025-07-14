"""
Module 10 - Routes API Flask
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Utilise Blueprint
- Format de réponse {success, data, message}
- Validation Marshmallow obligatoire
"""
from flask import Blueprint

module_10_bp = Blueprint('module_10', __name__)

# Routes du module 10 - OUTILS
# Ajouter ici les routes du module 10 selon les besoins 