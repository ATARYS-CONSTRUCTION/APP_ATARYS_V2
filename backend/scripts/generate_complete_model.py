#!/usr/bin/env python3
"""
ATARYS - GÉNÉRATEUR COMPLET DE MODÈLE
Script unifié pour générer automatiquement :
- Modèle SQLAlchemy
- Routes API
- Schéma Marshmallow
- Mise à jour Flask-Admin

Usage: python generate_complete_model.py nom_table
"""

import os
import sys
import sqlite3
from datetime import datetime

# Ajouter le dossier parent au sys.path pour pouvoir importer app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db


def analyze_table_structure(table_name):
    """Analyse la structure d'une table SQLite"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'atarys_data.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Récupérer les colonnes
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    conn.close()
    
    if not columns:
        raise ValueError(f"Table '{table_name}' non trouvée dans la base de données")
    
    return columns


def generate_model_class(table_name, columns):
    """Génère la classe SQLAlchemy"""
    class_name = ''.join(word.capitalize() for word in table_name.split('_'))
    
    model_content = f'''from .base import BaseModel
from app import db

class {class_name}(BaseModel):
    __tablename__ = '{table_name}'
    
'''
    
    for col in columns:
        col_name = col[1]
        col_type = col[2]
        is_primary = col[5] == 1
        not_null = col[3] == 1
        default_value = col[4]
        
        # Ignorer les colonnes BaseModel
        if col_name in ['id', 'created_at', 'updated_at']:
            continue
        
        # Convertir les types SQLite vers SQLAlchemy
        if col_type.upper() == 'INTEGER':
            sa_type = 'db.Integer'
        elif col_type.upper() == 'TEXT':
            sa_type = 'db.Text'
        elif col_type.upper() == 'REAL':
            sa_type = 'db.Float'
        elif col_type.upper().startswith('VARCHAR'):
            length = col_type.split('(')[1].split(')')[0] if '(' in col_type else '255'
            sa_type = f'db.String({length})'
        elif col_type.upper().startswith('NUMERIC'):
            sa_type = 'db.Numeric(10, 2)'
        elif col_type.upper() == 'BOOLEAN':
            sa_type = 'db.Boolean'
        elif col_type.upper() == 'DATE':
            sa_type = 'db.Date'
        elif col_type.upper() == 'DATETIME':
            sa_type = 'db.DateTime'
        else:
            sa_type = 'db.String(255)'  # Par défaut
        
        # Construire la définition de colonne
        col_def = f"    {col_name} = db.Column({sa_type}"
        
        if is_primary:
            col_def += ", primary_key=True"
        if not_null and not is_primary:
            col_def += ", nullable=False"
        if default_value and default_value != 'NULL':
            if col_type.upper() == 'TEXT' or col_type.upper().startswith('VARCHAR'):
                col_def += f", default='{default_value}'"
            else:
                col_def += f", default={default_value}"
        
        col_def += ")\n"
        model_content += col_def
    
    model_content += f'''
    def __repr__(self):
        return f'<{class_name} {{self.id}}>'
'''
    
    return class_name, model_content


def generate_routes(table_name, class_name, columns):
    """Génère les routes API"""
    endpoint_name = table_name.replace('_', '-')
    
    routes_content = f'''from flask import Blueprint, request, jsonify
from app import db
from app.models.{table_name}_model import {class_name}
from marshmallow import Schema, fields, validate
from datetime import date, datetime


# Schéma Marshmallow
class {class_name}Schema(Schema):
    id = fields.Int(dump_only=True)
'''
    
    # Ajouter les champs au schéma
    for col in columns:
        col_name = col[1]
        col_type = col[2]
        not_null = col[3] == 1
        
        if col_name in ['id', 'created_at', 'updated_at']:
            continue
        
        if col_type.upper() == 'INTEGER':
            field_type = 'fields.Int()'
        elif col_type.upper() == 'TEXT':
            field_type = 'fields.Str()'
        elif col_type.upper() == 'REAL':
            field_type = 'fields.Float()'
        elif col_type.upper().startswith('VARCHAR'):
            length = col_type.split('(')[1].split(')')[0] if '(' in col_type else '255'
            field_type = f'fields.Str(validate=validate.Length(max={length}))'
        elif col_type.upper().startswith('NUMERIC'):
            field_type = 'fields.Decimal(as_string=True)'
        elif col_type.upper() == 'BOOLEAN':
            field_type = 'fields.Bool()'
        elif col_type.upper() == 'DATE':
            field_type = 'fields.Date()'
        elif col_type.upper() == 'DATETIME':
            field_type = 'fields.DateTime()'
        else:
            field_type = 'fields.Str()'
        
        if not_null:
            field_type = field_type.replace('()', '(required=True)')
        
        routes_content += f'    {col_name} = {field_type}\n'
    
    routes_content += f'''    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


{table_name}_schema = {class_name}Schema(many=True)
{table_name}_single_schema = {class_name}Schema()

bp = Blueprint('{table_name}', __name__, url_prefix='/api/{endpoint_name}')


@bp.route('/', methods=['GET'])
def get_{table_name}():
    page = int(request.args.get('page', 1))
    per_page = request.args.get('per_page', 'all')
    
    query = {class_name}.query
    total = query.count()
    
    if per_page == 'all':
        items = query.order_by({class_name}.id.desc()).all()
        data = {table_name}_schema.dump(items)
        return jsonify({{
            'success': True,
            'data': data,
            'message': f'Liste complète ({total})',
            'pagination': {{
                'page': 1,
                'per_page': total,
                'total': total,
                'has_next': False
            }}
        }})
    else:
        per_page = int(per_page)
        items = query.order_by({class_name}.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        data = {table_name}_schema.dump(items.items)
        return jsonify({{
            'success': True,
            'data': data,
            'message': f'Liste (page {{page}})',
            'pagination': {{
                'page': page,
                'per_page': per_page,
                'total': total,
                'has_next': items.has_next
            }}
        }})


@bp.route('/', methods=['POST'])
def create_{table_name}():
    json_data = request.get_json()
    if not json_data:
        return jsonify({{'success': False, 'data': [], 'message': 'Aucune donnée reçue'}}), 400
    
    errors = {table_name}_single_schema.validate(json_data)
    if errors:
        return jsonify({{'success': False, 'data': [], 'message': errors}}), 400
    
    item = {class_name}(**json_data)
    db.session.add(item)
    db.session.commit()
    
    return jsonify({{
        'success': True,
        'data': {table_name}_single_schema.dump(item),
        'message': 'Élément créé'
    }})


@bp.route('/<int:item_id>', methods=['PUT'])
def update_{table_name}(item_id):
    item = {class_name}.query.get_or_404(item_id)
    json_data = request.get_json()
    
    if not json_data:
        return jsonify({{'success': False, 'data': [], 'message': 'Aucune donnée reçue'}}), 400
    
    errors = {table_name}_single_schema.validate(json_data)
    if errors:
        return jsonify({{'success': False, 'data': [], 'message': errors}}), 400
    
    for key, value in json_data.items():
        setattr(item, key, value)
    
    db.session.commit()
    
    return jsonify({{
        'success': True,
        'data': {table_name}_single_schema.dump(item),
        'message': 'Élément modifié'
    }})


@bp.route('/<int:item_id>', methods=['DELETE'])
def delete_{table_name}(item_id):
    item = {class_name}.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({{'success': True, 'data': [], 'message': 'Élément supprimé'}})


@bp.route('/clear/', methods=['DELETE', 'OPTIONS'])
def clear_{table_name}():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        num_deleted = db.session.query({class_name}).delete()
        db.session.commit()
        return jsonify({{
            'success': True,
            'data': [],
            'message': f'{{num_deleted}} éléments supprimés.'
        }})
    except Exception as e:
        db.session.rollback()
        return jsonify({{
            'success': False,
            'data': [],
            'message': f'Erreur lors de la suppression : {{str(e)}}'
        }}), 500
'''
    
    return routes_content


def update_app_init(table_name):
    """Met à jour le fichier __init__.py pour importer le nouveau blueprint"""
    init_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', '__init__.py')
    
    with open(init_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ajouter l'import du blueprint
    import_line = f"    from app.routes.{table_name} import bp as {table_name}_bp"
    register_line = f"    app.register_blueprint({table_name}_bp)"
    
    if import_line not in content:
        # Trouver la section des imports de blueprints
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'register_blueprint' in line:
                lines.insert(i-1, import_line)
                lines.insert(i+1, register_line)
                break
        
        content = '\n'.join(lines)
        
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(content)


def generate_complete_model(table_name):
    """Génère un modèle complet pour une table"""
    print(f"🔍 Analyse de la table '{table_name}'...")
    
    try:
        # Analyser la structure de la table
        columns = analyze_table_structure(table_name)
        print(f"✅ {len(columns)} colonnes trouvées")
        
        # Générer le modèle
        class_name, model_content = generate_model_class(table_name, columns)
        
        # Sauvegarder le modèle
        model_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'models', f'{table_name}_model.py')
        with open(model_file, 'w', encoding='utf-8') as f:
            f.write(model_content)
        print(f"✅ Modèle généré : {model_file}")
        
        # Générer les routes
        routes_content = generate_routes(table_name, class_name, columns)
        
        # Sauvegarder les routes
        routes_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'routes', f'{table_name}.py')
        with open(routes_file, 'w', encoding='utf-8') as f:
            f.write(routes_content)
        print(f"✅ Routes générées : {routes_file}")
        
        # Mettre à jour l'application
        update_app_init(table_name)
        print(f"✅ Application mise à jour")
        
        # Mettre à jour le fichier __init__.py des modèles
        models_init = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'models', '__init__.py')
        with open(models_init, 'a', encoding='utf-8') as f:
            f.write(f"\n# {table_name.upper()}\n")
            f.write(f"try:\n")
            f.write(f"    from .{table_name}_model import {class_name}\n")
            f.write(f"except ImportError:\n")
            f.write(f"    pass\n")
        
        print(f"🎉 Génération complète terminée pour '{table_name}'")
        print(f"📊 Classe générée : {class_name}")
        print(f"🌐 Endpoint API : /api/{table_name.replace('_', '-')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération : {str(e)}")
        return False


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python generate_complete_model.py nom_table")
        sys.exit(1)
    
    table_name = sys.argv[1]
    generate_complete_model(table_name) 