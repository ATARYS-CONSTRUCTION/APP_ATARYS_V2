"""
Module 3 - Schémas Marshmallow
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Validation obligatoire pour chaque endpoint
- Utiliser fields avec contraintes (String, Numeric, etc.)
"""
from marshmallow import Schema, fields, validate


class TestSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    test_atarys = fields.String()


class TestApiSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    test_api_field = fields.String()


class ClientsSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Champs de base
    civilite = fields.String(
        validate=validate.OneOf([
            'Mr ou Mme', 'Mr', 'Mme', 'SARL', 'SCI', 
            'Mr et Mr', 'Mme et Mme'
        ])
    )
    nom = fields.String(
        required=True, 
        validate=validate.Length(min=1, max=100)
    )
    prenom = fields.String(validate=validate.Length(max=100))
    
    # Contact
    email = fields.Email(allow_none=True)
    num_telephone = fields.String(validate=validate.Length(max=20))
    
    # Adresse
    adresse = fields.String(validate=validate.Length(max=200))
    code_postal = fields.String(validate=validate.Length(max=10))
    
    # Relations
    ville_id = fields.Integer(allow_none=True, validate=validate.Range(min=1))
    ville = fields.Nested('VillesSchema', dump_only=True)
    
    # Professionnel
    siret = fields.String(validate=validate.Length(max=14))
    id_contact_google = fields.String(validate=validate.Length(max=100))
