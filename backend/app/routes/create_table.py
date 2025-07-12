from flask import Blueprint, request, jsonify
from app import db
import os
import re

bp = Blueprint('create_table', __name__, url_prefix='/api/create-table')

@bp.route('/', methods=['POST'])
def create_table():
    """Créer une nouvelle table selon les spécifications"""
    
    try:
        data = request.get_json()
        table_data = data.get('tableData')
        code = data.get('code')
        
        if not table_data or not code:
            return jsonify({
                'success': False,
                'message': 'Données manquantes'
            }), 400
        
        # Valider les données
        if not table_data.get('className') or not table_data.get('tableName'):
            return jsonify({
                'success': False,
                'message': 'Nom de classe et table requis'
            }), 400
        
        # Vérifier que le nom de table est valide
        table_name = table_data['tableName']
        if not re.match(r'^[a-z][a-z0-9_]*$', table_name):
            return jsonify({
                'success': False,
                'message': 'Nom de table invalide (doit être en snake_case)'
            }), 400
        
        # Vérifier que la table n'existe pas déjà
        try:
            # Vérifier si la table existe dans la base
            result = db.session.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            if result.fetchone():
                return jsonify({
                    'success': False,
                    'message': f'La table "{table_name}" existe déjà'
                }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erreur lors de la vérification de la table: {str(e)}'
            }), 500
        
        # Créer le fichier de modèle
        module_id = table_data.get('moduleId', 12)
        file_name = f"module_{module_id}_1.py"
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        
        # Créer le répertoire models s'il n'existe pas
        os.makedirs(models_dir, exist_ok=True)
        
        file_path = os.path.join(models_dir, file_name)
        
        # Vérifier si le fichier existe déjà
        if os.path.exists(file_path):
            # Ajouter la nouvelle classe au fichier existant
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            # Ajouter la nouvelle classe à la fin
            new_content = existing_content + '\n\n' + code
        else:
            # Créer un nouveau fichier
            new_content = code
        
        # Écrire le fichier
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        # Créer la table dans la base de données
        try:
            # Générer la requête SQL CREATE TABLE
            sql_columns = []
            for col in table_data.get('columns', []):
                col_name = col['name']
                col_type = col['type']
                
                # Mapper les types SQLAlchemy vers SQLite
                type_mapping = {
                    'Integer': 'INTEGER',
                    'String': 'TEXT',
                    'Text': 'TEXT',
                    'Numeric': 'REAL',
                    'Float': 'REAL',
                    'Boolean': 'INTEGER',
                    'Date': 'TEXT',
                    'DateTime': 'TEXT',
                    'Time': 'TEXT',
                    'Timestamp': 'TEXT',
                    'JSON': 'TEXT',
                    'LargeBinary': 'BLOB',
                    'Enum': 'TEXT'
                }
                
                sql_type = type_mapping.get(col_type, 'TEXT')
                
                # Construire la définition de colonne
                col_def = f"{col_name} {sql_type}"
                
                if not col.get('nullable', True):
                    col_def += " NOT NULL"
                
                if col.get('unique', False):
                    col_def += " UNIQUE"
                
                if col.get('default'):
                    default_val = col['default']
                    if col_type == 'Boolean':
                        default_val = '1' if default_val else '0'
                    elif col_type == 'String':
                        default_val = f"'{default_val}'"
                    col_def += f" DEFAULT {default_val}"
                
                sql_columns.append(col_def)
            
            # Ajouter la colonne id automatiquement
            sql_columns.insert(0, "id INTEGER PRIMARY KEY AUTOINCREMENT")
            
            # Créer la table
            create_sql = f"CREATE TABLE {table_name} (\n    " + ",\n    ".join(sql_columns) + "\n)"
            
            db.session.execute(create_sql)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Table "{table_name}" créée avec succès',
                'data': {
                    'tableName': table_name,
                    'className': table_data['className'],
                    'columns': len(table_data.get('columns', [])) + 1  # +1 pour l'id
                }
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Erreur lors de la création de la table: {str(e)}'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur serveur: {str(e)}'
        }), 500 