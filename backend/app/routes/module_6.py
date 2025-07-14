"""
Module 6 - Routes API Flask
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Utilise Blueprint
- Format de réponse {success, data, message}
- Validation Marshmallow obligatoire
"""
from flask import Blueprint

module_6_bp = Blueprint('module_6', __name__)

# Routes du module 6 - ATELIER
# Ajouter ici les routes du module 6 selon les besoins 