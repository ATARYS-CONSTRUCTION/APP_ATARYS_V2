"""
Module 5 - Schémas Marshmallow
Respecte les standards ATARYS V2 (voir .cursorrules et docs/02-architecture/ATARYS_MODULES.md)
- Validation obligatoire pour chaque endpoint
- Utiliser fields avec contraintes (String, Numeric, etc.)
"""
from marshmallow import Schema, fields, validate

# Schémas du module 5 - DEVIS_FACTURATION
# Ajouter ici les schémas du module 5 selon les besoins 

from marshmallow import Schema, fields

class TestProfessionalTableSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    nom = fields.String()
    description = fields.String()
    montant = fields.Decimal()
    actif = fields.Boolean()


from marshmallow import Schema, fields

class FamilleOuvragesSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    num_bd_atarys = fields.String()
    libelle = fields.String()
