def generate_sqlalchemy_model_code(class_name, table_name, columns, module_id=12):
    """
    Génère le code Python d'un modèle SQLAlchemy ATARYS.
    - class_name : Nom de la classe Python (PascalCase)
    - table_name : Nom de la table (snake_case)
    - columns : liste de dicts :
        [
            {
                "name": "reference",
                "type": "String",
                "nullable": False,
                "unique": True,
                "default": None,
                "max_length": 100,      # optionnel pour String
                "is_foreign_key": False,
                "foreign_key_target": "", # si clé étrangère
                "foreign_key_column": "id" # si clé étrangère
            },
            ...
        ]
    - module_id : pour le nom du fichier cible (optionnel)
    Retourne : code Python (str)
    """
    code = ["from .base import BaseModel", "from app import db", "import datetime", ""]
    code.append(f"class {class_name}(BaseModel):")
    code.append(f"    __tablename__ = '{table_name}'")
    # Colonne id automatique
    code.append("    id = db.Column(db.Integer, primary_key=True, autoincrement=True)")
    for col in columns:
        # Gestion du type SQLAlchemy
        t = col["type"]
        args = ""
        if t == "String":
            maxlen = col.get("max_length", 100)
            args = f"db.String({maxlen})"
        elif t == "Numeric":
            args = "db.Numeric(10, 2)"
        elif t == "REAL":
            args = "db.Float"
        elif t == "Boolean":
            args = "db.Boolean"
        elif t == "Text":
            args = "db.Text"
        elif t == "Integer":
            args = "db.Integer"
        elif t == "Date":
            args = "db.Date"
        elif t == "DateTime":
            args = "db.DateTime"
        elif t == "Time":
            args = "db.Time"
        elif t == "Timestamp":
            args = "db.DateTime"
        elif t == "JSON":
            args = "db.JSON"
        elif t == "LargeBinary":
            args = "db.LargeBinary"
        elif t == "Enum":
            args = f"db.Enum({col.get('enum_name', 'EnumType')})"
        else:
            args = "db.String(100)"
        # ForeignKey
        if col.get("is_foreign_key"):
            fk_target = col.get("foreign_key_target", "")
            fk_col = col.get("foreign_key_column", "id")
            args += f", db.ForeignKey('{fk_target}.{fk_col}')"
        # Attributs supplémentaires
        attr = []
        if not col.get("nullable", True):
            attr.append("nullable=False")
        if col.get("unique", False):
            attr.append("unique=True")
        if col.get("default") not in [None, ""]:
            default = col["default"]
            if t == "String":
                attr.append(f'default="{default}"')
            elif t == "Boolean":
                attr.append(f'default={str(default).lower()}')
            elif t in ["Integer", "REAL", "Numeric"]:
                attr.append(f'default={default}')
            elif t in ["Date", "DateTime", "Timestamp"] and default in ["datetime.date.today", "datetime.datetime.utcnow"]:
                attr.append(f'default={default}')
            else:
                attr.append(f'default="{default}"')
        attr_str = ", " + ", ".join(attr) if attr else ""
        code.append(f"    {col['name']} = db.Column({args}{attr_str})")
    code.append("")
    code.append(f"    def __repr__(self):")
    code.append(f"        return f'<{class_name} {{{{self.id}}}}>'")
    code.append("")
    return "\n".join(code)

def generate_marshmallow_schema_code(class_name, columns):
    """
    Génère le code Python d'un schéma Marshmallow pour la classe donnée.
    - class_name : Nom de la classe (PascalCase)
    - columns : liste de dicts (name, type, nullable, unique, default, max_length...)
    Retourne : code Python (str)
    """
    code = ["from marshmallow import Schema, fields, validate", ""]
    schema_name = f"{class_name}Schema"
    code.append(f"class {schema_name}(Schema):")
    code.append("    id = fields.Int(dump_only=True)")
    for col in columns:
        name = col['name']
        t = col['type']
        field = None
        opts = []
        if t == "String":
            field = "fields.Str"
            if col.get("max_length"):
                opts.append(f"validate=validate.Length(max={col['max_length']})")
        elif t == "Text":
            field = "fields.Str"
        elif t == "Integer":
            field = "fields.Int"
        elif t in ["Numeric", "REAL"]:
            field = "fields.Decimal"
            opts.append("as_string=True")
        elif t == "Boolean":
            field = "fields.Bool"
        elif t == "Date":
            field = "fields.Date"
        elif t in ["DateTime", "Timestamp"]:
            field = "fields.DateTime"
        else:
            field = "fields.Raw"
        if not col.get("nullable", True):
            opts.append("required=True")
        opts_str = ", ".join(opts)
        code.append(f"    {name} = {field}({opts_str})" if opts_str else f"    {name} = {field}()")
    code.append("    created_at = fields.DateTime(dump_only=True)")
    code.append("    updated_at = fields.DateTime(dump_only=True)")
    code.append("")
    return "\n".join(code) 