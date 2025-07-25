"""
Module 9 - Schémas Marshmallow
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Schéma Marshmallow obligatoire pour chaque ressource
- Validation stricte
"""

from marshmallow import Schema, fields
from .module_5 import FamilleOuvragesSchema

class NiveauQualificationSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    niveau = fields.String()
    categorie = fields.String()


class SalariesSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Informations de base (selon l'image)
    nom = fields.String(required=True)
    prenom = fields.String(required=True)
    
    # Rémunération et heures (selon l'image)
    salaire_brut_horaire = fields.Decimal(places=2, allow_none=True)
    nbre_heure_hebdo = fields.Decimal(places=2, allow_none=True)
    
    # Contrat
    type_contrat = fields.String(allow_none=True)
    date_entree = fields.String(required=True)  # Changé en String pour éviter les erreurs de format
    date_sortie = fields.String(allow_none=True)  # Changé en String
    
    # Qualifications
    niveau_qualification_id = fields.Integer(allow_none=True)
    
    # Planning
    colonne_planning = fields.String(allow_none=True)
    
    # Contact
    email = fields.String(allow_none=True)
    num_telephone = fields.String(allow_none=True)
    
    # Adresse
    adresse = fields.String(allow_none=True)
    ville_id = fields.Integer(allow_none=True)
    
    # Informations personnelles
    date_naissance = fields.String(allow_none=True)  # Changé en String
    num_securite_social = fields.String(allow_none=True)
    
    # OneDrive
    ondrive_path = fields.String(allow_none=True)
    
    # Familles d'ouvrages (relation many-to-many)
    famille_ouvrages = fields.Nested('FamilleOuvragesSchema', many=True, dump_only=True)
    famille_ouvrages_ids = fields.List(fields.Integer(), load_only=True, allow_none=True)
    
    # Relation ville
    ville = fields.Nested('VilleSchema', dump_only=True)


class VilleSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Informations de base
    communes = fields.String(required=True)
    code_postal = fields.Integer(required=True)
    code_insee = fields.Integer(allow_none=True)
    departement = fields.Integer(allow_none=True)
    
    # Coordonnées géographiques (gestion des virgules françaises)
    latitude = fields.String(allow_none=True)  # Changé en String pour éviter les erreurs de conversion
    longitude = fields.String(allow_none=True)  # Changé en String pour éviter les erreurs de conversion
    
    # Zone climatique
    zone_nv = fields.Integer(allow_none=True)
    
    # Distances et temps (gestion des virgules françaises)
    distance_km_oiseau = fields.String(allow_none=True)  # Changé en String
    distance_km_routes = fields.String(allow_none=True)   # Changé en String
    temps_route_min = fields.String(allow_none=True)      # Changé en String
