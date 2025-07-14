"""
Module 13 - Routes API Flask
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Utilise Blueprint
- Format de réponse {success, data, message}
- Validation Marshmallow obligatoire
"""
from flask import Blueprint

module_13_bp = Blueprint('module_13', __name__)

# Routes du module 13 - AIDE
# Ajouter ici les routes du module 13 selon les besoins 