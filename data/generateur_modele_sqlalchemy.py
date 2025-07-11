#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - GÉNÉRATEUR DE MODÈLES SQLALCHEMY INTERACTIF
Script pédagogique pour générer du code de modèles SQLAlchemy conformes ATARYS

Auteur: ATARYS Team
Date: 2025
"""

import sys
import re
import datetime
from pathlib import Path

MODULES_ATARYS = {
    1: "PLANNING",
    2: "LISTE_DES_TACHES", 
    3: "LISTE_CHANTIERS",
    4: "CHANTIERS",
    5: "DEVIS_FACTURATION",
    6: "ATELIER",
    7: "GESTION",
    8: "COMPTABILITE",
    9: "SOCIAL",
    10: "OUTILS",
    11: "ARCHIVES",
    12: "PARAMETRES",
    13: "AIDE"
}

TYPES = [
    ("Integer", "Nombre entier (Integer)", "db.Integer"),
    ("String", "Texte court (String)", "db.String"),
    ("Text", "Texte long (Text)", "db.Text"),
    ("Numeric", "Montant financier (Numeric(10,2))", "db.Numeric(10, 2)"),
    ("Float", "Nombre décimal (Float)", "db.Float"),
    ("Boolean", "Vrai/Faux (Boolean)", "db.Boolean"),
    ("Date", "Date seulement (Date)", "db.Date"),
    ("DateTime", "Date/Heure (DateTime)", "db.DateTime"),
    ("Time", "Heure seulement (Time)", "db.Time"),
    ("Timestamp", "Horodatage (Timestamp)", "db.Timestamp"),
    ("JSON", "Données JSON (JSON)", "db.JSON"),
    ("LargeBinary", "Données binaires (LargeBinary)", "db.LargeBinary"),
    ("Enum", "Liste de valeurs (Enum)", "db.Enum")
]

def ask(prompt, default=None):
    val = input(prompt)
    if not val and default is not None:
        return default
    return val

def pascal_to_snake(pascal_case):
    """Convertir PascalCase en snake_case"""
    # Ajouter un underscore avant chaque majuscule, sauf la première
    snake_case = re.sub(r'(?<!^)(?=[A-Z])', '_', pascal_case)
    # Convertir en minuscules
    return snake_case.lower()

def main():
    print("="*60)
    print(" ATARYS - GÉNÉRATEUR DE MODÈLES SQLALCHEMY INTERACTIF")
    print("="*60)
    print()
    print("Modules ATARYS disponibles :")
    for k, v in MODULES_ATARYS.items():
        print(f" {k}. {v}")
    while True:
        try:
            module_id = int(ask("\nVotre choix de module (1-13) : "))
            if module_id in MODULES_ATARYS:
                break
            else:
                print("❌ Choix invalide")
        except ValueError:
            print("❌ Entrez un nombre")
    module_name = MODULES_ATARYS[module_id]
    file_name = f"module_{module_id}_1.py"
    print(f"\nNom du fichier généré : backend/app/models/{file_name}")
    classes = []
    while True:
        print("\n--- Nouvelle table à créer ---")
        class_name = ask("Nom de la classe (PascalCase) : ")
        # Générer automatiquement le nom de table
        table_name = pascal_to_snake(class_name)
        print(f"✅ Nom de table généré : {table_name}")
        
        # Option pour modifier le nom de table si besoin
        custom_table = ask("Modifier le nom de table ? (laisser vide pour garder) : ")
        if custom_table:
            table_name = custom_table
            print(f"✅ Nom de table modifié : {table_name}")
        
        columns = []
        
        # Ajouter automatiquement la colonne id en clé primaire
        print("\n✅ Colonne 'id' ajoutée automatiquement (clé primaire auto-incrémentée)")
        id_column = "    id = db.Column(db.Integer, primary_key=True, autoincrement=True)"
        columns.append(id_column)
        
        while True:
            print("\nAjout d'une colonne :")
            col_name = ask("- Nom de la colonne : ")
            
            # Validation : empêcher la création d'une colonne 'id' manuelle
            if col_name.lower() == 'id':
                print("❌ La colonne 'id' est déjà créée automatiquement (clé primaire)")
                continue
            print("- Type :")
            for i, (t, desc, _) in enumerate(TYPES, 1):
                print(f"  {i}. {desc}")
            while True:
                try:
                    t_idx = int(ask(f"  Votre choix (1-{len(TYPES)}) : "))
                    if 1 <= t_idx <= len(TYPES):
                        break
                    else:
                        print("❌ Choix invalide")
                except ValueError:
                    print("❌ Entrez un nombre")
            t_name, _, t_sql = TYPES[t_idx-1]
            args = ""
            is_fk = ask("  Cette colonne est-elle une clé étrangère ? (y/n) : ", "n").lower() == "y"
            fk_target = None
            if is_fk:
                fk_target = ask("    Table cible (snake_case) : ")
                fk_col = ask("    Colonne cible (par défaut 'id') : ", "id")
                fk_str = f"db.ForeignKey('{fk_target}.{fk_col}')"
                t_sql = f"db.Integer, {fk_str}"
            if t_name == "String" and not is_fk:
                maxlen = ask("  Longueur max (ex: 100) : ", "100")
                t_sql = f"db.String({maxlen})"
            elif t_name == "Integer" and not is_fk:
                # Integer peut avoir des contraintes spécifiques (mais pas auto-incrément car id existe déjà)
                print("  ℹ️ Auto-incrément géré par la colonne 'id' (clé primaire)")
            elif t_name in ["Date", "DateTime", "Timestamp"] and not is_fk:
                # Types temporels peuvent avoir des valeurs par défaut
                default_now = ask("  Valeur par défaut 'now' ? (y/n) : ", "n").lower() == "y"
                if default_now:
                    if t_name == "Date":
                        t_sql += ", default=datetime.date.today"
                    elif t_name == "DateTime":
                        t_sql += ", default=datetime.datetime.utcnow"
                    elif t_name == "Timestamp":
                        t_sql += ", default=datetime.datetime.utcnow"
            elif t_name == "Enum" and not is_fk:
                # Configuration des ENUM
                print("  Configuration ENUM :")
                enum_name = ask("    Nom de l'enum (ex: StatutChantier) : ")
                print("    Valeurs possibles (une par ligne, ligne vide pour terminer) :")
                enum_values = []
                while True:
                    value = ask("      Valeur : ").strip()
                    if not value:
                        break
                    enum_values.append(value)
                
                if enum_values:
                    # Configurer la colonne
                    t_sql = f"db.Enum({enum_name})"
                    
                    # Stocker les infos ENUM pour génération plus tard
                    enum_config = {
                        "name": enum_name,
                        "values": enum_values
                    }
                    # On ajoutera la classe Enum lors de la génération finale
                else:
                    print("    ⚠️ Aucune valeur ENUM définie, utilisation de String")
                    t_sql = "db.String(50)"
                    enum_config = None
            nullable = ask("  Obligatoire ? (y/n) : ", "y").lower() == "n"
            unique = ask("  Unique ? (y/n) : ", "n").lower() == "y"
            default = ask("  Valeur par défaut (laisser vide si aucune) : ")
            col_def = f"    {col_name} = db.Column({t_sql}"
            if not nullable:
                col_def += ", nullable=False"
            if unique:
                col_def += ", unique=True"
            if default:
                if t_name == "String":
                    col_def += f', default="{default}"'
                elif t_name == "Boolean":
                    col_def += f', default={default.lower() in ["true", "1", "y", "yes"]}'
                elif t_name in ["Integer", "Float", "Numeric"]:
                    col_def += f', default={default}'
                else:
                    col_def += f', default="{default}"'
            col_def += ")"
            columns.append(col_def)
            # Many-to-Many
            is_m2m = ask("  Veux-tu créer une relation Many-to-Many avec une autre table ? (y/n) : ", "n").lower() == "y"
            if is_m2m:
                m2m_target = ask("    Table cible (snake_case) : ")
                m2m_assoc = f"{table_name}_{m2m_target}" if table_name < m2m_target else f"{m2m_target}_{table_name}"
                # Table d'association
                assoc_code = f"{m2m_assoc} = db.Table(\n    '{m2m_assoc}',\n    db.Column('{table_name}_id', db.Integer, db.ForeignKey('{table_name}.id')),"
                assoc_code += f"\n    db.Column('{m2m_target}_id', db.Integer, db.ForeignKey('{m2m_target}.id'))\n)"
                # Relation dans le modèle courant
                rel_name = ask(f"    Nom de la relation Python (ex: {m2m_target}) : ", m2m_target)
                rel_class = ask(f"    Classe cible (ex: {m2m_target[:-1].capitalize()}) : ", m2m_target[:-1].capitalize())
                rel_def = f"    {rel_name} = db.relationship('{rel_class}', secondary={m2m_assoc}, back_populates='{table_name}')"
                columns.append(f"# --- Many-to-Many association table ---\n{assoc_code}\n# --- End association table ---")
                columns.append(rel_def)
                columns.append(f"# ⚠️ Ajoute la relation symétrique dans le modèle {rel_class} :\n#    {table_name} = db.relationship('{class_name}', secondary={m2m_assoc}, back_populates='{rel_name}')\n")
            # Proposer la relation Python si ForeignKey
            if is_fk:
                rel_name = ask(f"  Nom de la relation Python (ex: {fk_target[:-1]}) : ", fk_target[:-1])
                rel_class = ask(f"  Classe cible (ex: {fk_target[:-1].capitalize()}) : ", fk_target[:-1].capitalize())
                rel_def = f"    {rel_name} = db.relationship('{rel_class}')"
                columns.append(rel_def)
            more = ask("Ajouter une autre colonne ? (y/n) : ", "n").lower()
            if more != "y":
                break
        classes.append((class_name, table_name, columns))
        more_table = ask("Voulez-vous ajouter une autre table à ce module ? (y/n) : ", "n").lower()
        if more_table != "y":
            break
    # Génération du code
    code = ["from .base import BaseModel", "from app import db", ""]
    
    # Collecter tous les ENUMs utilisés
    enums_used = set()
    for class_name, table_name, columns in classes:
        for col in columns:
            if "db.Enum(" in col:
                # Extraire le nom de l'ENUM
                enum_name = col.split("db.Enum(")[1].split(")")[0]
                enums_used.add(enum_name)
    
    # Ajouter l'import enum si nécessaire
    if enums_used:
        code.insert(0, "import enum")
        code.insert(1, "")
    
    # Générer les classes ENUM
    for enum_name in enums_used:
        # Pour l'instant, on génère des ENUMs basiques
        # Dans une version future, on pourrait stocker les valeurs
        enum_code = f"class {enum_name}(enum.Enum):\n"
        enum_code += f"    # TODO: Ajouter les valeurs spécifiques\n"
        enum_code += f"    pass\n\n"
        code.append(enum_code)
    
    for class_name, table_name, columns in classes:
        code.append(f"class {class_name}(BaseModel):")
        code.append(f"    __tablename__ = '{table_name}'")
        code.extend(columns)
        code.append("")
        code.append(f"    def __repr__(self):")
        code.append(f"        return f'<{class_name} {{{{self.id}}}}>'")
        code.append("")
    code_str = "\n".join(code)
    print("\n--- CODE GÉNÉRÉ ---\n")
    print(code_str)
    save = ask(f"\nVoulez-vous sauvegarder dans backend/app/models/{file_name} ? (y/n) : ", "y").lower()
    if save == "y":
        models_dir = Path(__file__).parent.parent / "backend" / "app" / "models"
        models_dir.mkdir(parents=True, exist_ok=True)
        with open(models_dir / file_name, "w", encoding="utf-8") as f:
            f.write(code_str)
        print(f"✅ Fichier sauvegardé : {models_dir / file_name}")
    print("\n🎉 Génération terminée !")

if __name__ == "__main__":
    main() 