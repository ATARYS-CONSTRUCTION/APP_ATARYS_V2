"""
Module 12 - Schémas Marshmallow
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Validation obligatoire pour chaque endpoint
- Utiliser fields avec contraintes (String, Numeric, etc.)
"""

from marshmallow import Schema, fields


class TestAuditTableSchema(Schema):
    """Schéma pour la table TestAuditTable."""
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    nom = fields.String(required=True)
    prix = fields.Float(required=False, allow_none=True)
    actif = fields.Boolean(required=False, default=True)
    date_creation = fields.DateTime(required=True)


class NiveauQualificationSchema(Schema):
    """Schéma pour la table NiveauQualification."""
    id = fields.Integer(dump_only=True)
    niveau = fields.String(required=True)
    categorie = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class TestCle2Schema(Schema):
    """Schéma pour la table TestCle2 avec relation à NiveauQualification."""
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    libelle = fields.String(required=True)
    niveau_qualification_id = fields.Integer(
        required=False,
        allow_none=True,
        description="ID du niveau de qualification associé"
    )
    
    # Inclure les données du niveau_qualification dans la réponse
    niveau_qualification = fields.Nested(
        NiveauQualificationSchema,
        only=('id', 'niveau', 'categorie'),
        dump_only=True,
        description="Données du niveau de qualification associé"
    )
