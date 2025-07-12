from marshmallow import Schema, fields, validate

class ArticlesAtarysSchema(Schema):
    id = fields.Int(dump_only=True)
    reference = fields.Str(required=True)
    libelle = fields.Str(required=True)
    prix_achat = fields.Str()
    coefficient = fields.Str()
    prix_unitaire = fields.Str(required=True)
    unite = fields.Str(required=True)
    tva_pct = fields.Str(required=True)
    famille = fields.Str()
    actif = fields.Bool()
    date_import = fields.Str(required=True)
    date_maj = fields.Str(required=True)
    created_at = fields.Str()
    updated_at = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
