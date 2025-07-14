"""
Module 8 - Routes API Flask
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Utilise Blueprint
- Format de réponse {success, data, message}
- Validation Marshmallow obligatoire
"""
from flask import Blueprint

module_8_bp = Blueprint('module_8', __name__)

# Routes du module 8 - COMPTABILITÉ
# Ajouter ici les routes du module 8 selon les besoins 