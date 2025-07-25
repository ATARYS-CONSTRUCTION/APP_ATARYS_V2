"""
Module 10 - Schémas Marshmallow
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Validation obligatoire pour chaque endpoint
- Utiliser fields avec contraintes (String, Numeric, etc.)
"""
from marshmallow import Schema, fields, validate

# Schémas du module 10 - OUTILS
# Ajouter ici les schémas du module 10 selon les besoins 



from marshmallow import Schema, fields

class ModeleArdoisesSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    modele_ardoises = fields.String()



from marshmallow import Schema, fields

class VillesSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    communes = fields.String()
    code_postal = fields.Integer()
    code_insee = fields.Integer()
    departement = fields.Integer()
    latitude = fields.String()
    longitude = fields.String()
    zone_nv = fields.Integer()
    distance_km_oiseau = fields.String()
    distance_km_routes = fields.String()
    temps_route_min = fields.String()
