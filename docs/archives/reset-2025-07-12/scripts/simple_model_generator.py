#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de génération de modèles SQLAlchemy simples
Génère un modèle et des routes API pour une table existante
"""

import sys
import os
import sqlite3
from datetime import datetime

# Ajouter le répertoire parent au path pour importer les modules app
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import db, create_app

def analyze_table_structure(table_name):
    """Analyse la structure d'une table SQLite"""
    app = create_app()
    with app.app_context():
        result = db.session.execute(db.text(f"PRAGMA table_info({table_name})"))
        columns = result.fetchall()
        return columns

def generate_model_class(table_name, columns):
    """Génère le code d'une classe SQLAlchemy"""
    
    # Convertir le nom de table en nom de classe (PascalCase)
    class_name = ''.join(word.capitalize() for word in table_name.split('_'))
    
    # Générer le contenu du modèle
    model_content = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
Modèle SQLAlchemy pour la table {table_name}
Généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
\"\"\"

from app import db
from app.models.base import BaseModel

class {class_name}(BaseModel):
    __tablename__ = '{table_name}'
    
"""
    
    # Ajouter les colonnes (sauf id, created_at, updated_at qui sont dans BaseModel)
    for col in columns:
        col_name = col[1]  # Nom de la colonne
        col_type = col[2]  # Type de la colonne
        not_null = col[3]  # NOT NULL
        default_value = col[4]  # Valeur par défaut
        is_primary = col[5]  # PRIMARY KEY
        
        # Ignorer les colonnes de BaseModel
        if col_name in ['id', 'created_at', 'updated_at']:
            continue
        
        # Convertir le type SQLite en type SQLAlchemy
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


def generate_simple_routes(table_name, class_name):
    """Génère des routes API simples"""
    endpoint_name = table_name.replace('_', '-')
    
    routes_content = f'''from flask import Blueprint, request, jsonify
from app import db
from app.models.{table_name}_model import {class_name}

bp = Blueprint('{table_name}', __name__, url_prefix='/api/{endpoint_name}')

@bp.route('/', methods=['GET'])
def get_all():
    page = int(request.args.get('page', 1))
    per_page = request.args.get('per_page', 'all')
    
    query = {class_name}.query
    total = query.count()
    
    if per_page == 'all':
        items = query.order_by({class_name}.id.desc()).all()
        data = [{{
            'id': item.id,
            **{{k: v for k, v in item.__dict__.items() if not k.startswith('_')}}
        }} for item in items]
        return jsonify({{
            'success': True,
            'data': data,
            'message': f'Liste complète ({{total}})',
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
        data = [{{
            'id': item.id,
            **{{k: v for k, v in item.__dict__.items() if not k.startswith('_')}}
        }} for item in items.items]
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
def create():
    json_data = request.get_json()
    if not json_data:
        return jsonify({{'success': False, 'data': [], 'message': 'Aucune donnée reçue'}}), 400
    
    item = {class_name}(**json_data)
    db.session.add(item)
    db.session.commit()
    
    return jsonify({{
        'success': True,
        'data': {{'id': item.id, **{{k: v for k, v in item.__dict__.items() if not k.startswith('_')}}}},
        'message': 'Élément créé'
    }})

@bp.route('/<int:item_id>', methods=['DELETE'])
def delete(item_id):
    item = {class_name}.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({{'success': True, 'data': [], 'message': 'Élément supprimé'}})

@bp.route('/clear/', methods=['DELETE'])
def clear_all():
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


def generate_simple_model(table_name):
    """Génère un modèle simple pour une table"""
    print(f"[INFO] Analyse de la table '{table_name}'...")
    
    try:
        # Analyser la structure de la table
        columns = analyze_table_structure(table_name)
        print(f"[SUCCESS] {len(columns)} colonnes trouvées")
        
        # Générer le modèle
        class_name, model_content = generate_model_class(table_name, columns)
        
        # Sauvegarder le modèle
        model_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'models', f'{table_name}_model.py')
        with open(model_file, 'w', encoding='utf-8') as f:
            f.write(model_content)
        print(f"[SUCCESS] Modèle généré : {model_file}")
        
        # Générer les routes
        routes_content = generate_simple_routes(table_name, class_name)
        
        # Sauvegarder les routes
        routes_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'routes', f'{table_name}.py')
        with open(routes_file, 'w', encoding='utf-8') as f:
            f.write(routes_content)
        print(f"[SUCCESS] Routes générées : {routes_file}")
        
        # Mettre à jour le fichier __init__.py des modèles
        models_init = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'models', '__init__.py')
        with open(models_init, 'a', encoding='utf-8') as f:
            f.write(f"\n# {table_name.upper()}\n")
            f.write(f"try:\n")
            f.write(f"    from .{table_name}_model import {class_name}\n")
            f.write(f"except ImportError:\n")
            f.write(f"    pass\n")
        
        print(f"[SUCCESS] Génération terminée pour '{table_name}'")
        print(f"[INFO] Classe générée : {class_name}")
        print(f"[INFO] Endpoint API : /api/{table_name.replace('_', '-')}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Erreur lors de la génération : {str(e)}")
        return False


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python simple_model_generator.py nom_table")
        sys.exit(1)
    
    table_name = sys.argv[1]
    generate_simple_model(table_name) 