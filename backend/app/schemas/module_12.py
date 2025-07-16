"""
Module 12 - Schémas Marshmallow
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Validation obligatoire pour chaque endpoint
- Utiliser fields avec contraintes (String, Numeric, etc.)
"""

# Schémas du module 12 - PARAMÈTRES
# Ajouter ici les schémas du module 12 selon les besoins


from marshmallow import Schema, fields

class TestAuditTableSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    nom = fields.String()
    prix = fields.Decimal()
    actif = fields.Boolean()
    date_creation = fields.DateTime()
