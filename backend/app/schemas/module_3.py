"""
Module 3 - Schémas Marshmallow
Respecte les standards ATARYS V2 (voir .cursorrules et docs/02-architecture/ATARYS_MODULES.md)
- Validation obligatoire pour chaque endpoint
- Utiliser fields avec contraintes (String, Numeric, etc.)
"""
from marshmallow import Schema, fields, validate

# Schémas du module 3 - LISTE_CHANTIERS
# Ajouter ici les schémas du module 3 selon les besoins 
# Schéma généré automatiquement - test

from marshmallow import Schema, fields

class TestSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    test_atarys = fields.String()


# Schéma généré automatiquement - test_api

from marshmallow import Schema, fields

class TestApiSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    test_api_field = fields.String()

