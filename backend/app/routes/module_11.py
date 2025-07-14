"""
Module 11 - Routes API Flask
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Utilise Blueprint
- Format de réponse {success, data, message}
- Validation Marshmallow obligatoire
"""
from flask import Blueprint

module_11_bp = Blueprint('module_11', __name__)

# Routes du module 11 - ARCHIVES
# Ajouter ici les routes du module 11 selon les besoins 