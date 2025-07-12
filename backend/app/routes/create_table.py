from flask import Blueprint, request, jsonify
from app import db
import os
import re
from sqlalchemy import text
from app.utils.model_generator import (
    generate_sqlalchemy_model_code, 
    generate_marshmallow_schema_code
)

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
                'message': (
                    'Nom de table invalide (doit être en snake_case)'
                )
            }), 400
        
        # Vérifier que la table n'existe pas déjà
        try:
            # Vérifier si la table existe dans la base
            query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
            result = db.session.execute(text(query))
            if result.fetchone():
                return jsonify({
                    'success': False,
                    'message': (
                        f'La table "{table_name}" existe déjà'
                    )
                }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': (
                    f'Erreur lors de la vérification de la table: {str(e)}'
                )
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
            
            # Ajouter les colonnes created_at et updated_at automatiquement (BaseModel)
            sql_columns.append("created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
            sql_columns.append("updated_at DATETIME DEFAULT CURRENT_TIMESTAMP")
            
            # Créer la table
            columns_str = ",\n    ".join(sql_columns)
            create_sql = f"CREATE TABLE {table_name} (\n    {columns_str}\n)"
            
            db.session.execute(text(create_sql))
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': (
                    f'Table "{table_name}" créée avec succès'
                ),
                'data': {
                    'tableName': table_name,
                    'className': table_data['className'],
                    'columns': len(table_data.get('columns', [])) + 3  # +3 pour id, created_at, updated_at
                }
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': (
                    f'Erreur lors de la création de la table: {str(e)}'
                )
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': (
                f'Erreur serveur: {str(e)}'
            )
        }), 500


@bp.route('/generate-model', methods=['POST'])
def generate_model():
    """Génère le code d'un modèle SQLAlchemy et l'enregistre dans le bon fichier."""
    try:
        data = request.get_json()
        class_name = data.get('class_name')
        table_name = data.get('table_name')
        columns = data.get('columns', [])
        module_id = data.get('module_id', 12)
        if not class_name or not table_name or not columns:
            return jsonify({
                'success': False,
                'message': 'class_name, table_name et columns sont requis.'
            }), 400
        # Générer le code du modèle
        code = generate_sqlalchemy_model_code(class_name, table_name, columns, module_id)
        # Déterminer le fichier cible
        file_name = f"module_{module_id}_1.py"
        import os
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        os.makedirs(models_dir, exist_ok=True)
        file_path = os.path.join(models_dir, file_name)
        # Ajouter la classe à la fin du fichier si il existe, sinon créer
        if os.path.exists(file_path):
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\n\n' + code)
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
        return jsonify({
            'success': True,
            'message': f'Modèle généré et enregistré dans {file_path}',
            'model_code': code,
            'reminder': 'Redémarrez Flask-Admin pour voir la nouvelle table.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la génération du modèle : {str(e)}'
        }), 500


@bp.route('/generate-model-and-api', methods=['POST'])
def generate_model_and_api():
    """
    Génère le code du modèle SQLAlchemy, du schéma Marshmallow et de la route Flask CRUD pour une table donnée.
    Reçoit : class_name, table_name, columns, module_id
    Retourne : code généré (modèle, schéma, route)
    """
    try:
        data = request.get_json()
        class_name = data.get('class_name')
        table_name = data.get('table_name')
        columns = data.get('columns', [])
        module_id = data.get('module_id', 12)
        if not class_name or not table_name or not columns:
            msg = 'class_name, table_name et columns sont requis.'
            return jsonify({'success': False, 'message': msg}), 400
        # Générer le modèle SQLAlchemy
        model_code = generate_sqlalchemy_model_code(class_name, table_name, columns, module_id)
        # Générer le schéma Marshmallow
        schema_code = generate_marshmallow_schema_code(class_name, columns)
        # Générer la route Flask CRUD (template simplifié)
        route_code = f"""
from flask import Blueprint, request, jsonify
from app import db
from app.models.module_{module_id}_1 import {class_name}
from app.schemas.{table_name}_schema import {class_name}Schema

bp = Blueprint('{table_name}', __name__, url_prefix='/api/{table_name}')

schema = {class_name}Schema()
schemas = {class_name}Schema(many=True)

@bp.route('/', methods=['GET'])
def get_all():
    items = {class_name}.query.all()
    return jsonify({{'success': True, 'data': schemas.dump(items), 'message': 'Liste'}})

@bp.route('/', methods=['POST'])
def create():
    json_data = request.get_json()
    errors = schema.validate(json_data)
    if errors:
        return jsonify({{'success': False, 'data': [], 'message': errors}}), 400
    item = {class_name}(**json_data)
    db.session.add(item)
    db.session.commit()
    return jsonify({{'success': True, 'data': schema.dump(item), 'message': 'Créé'}})

@bp.route('/<int:item_id>', methods=['PUT'])
def update(item_id):
    item = {class_name}.query.get_or_404(item_id)
    json_data = request.get_json()
    errors = schema.validate(json_data)
    if errors:
        return jsonify({{'success': False, 'data': [], 'message': errors}}), 400
    for key, value in json_data.items():
        setattr(item, key, value)
    db.session.commit()
    return jsonify({{'success': True, 'data': schema.dump(item), 'message': 'Modifié'}})

@bp.route('/<int:item_id>', methods=['DELETE'])
def delete(item_id):
    item = {class_name}.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({{'success': True, 'data': [], 'message': 'Supprimé'}})
"""
        return jsonify({
            'success': True,
            'model_code': model_code,
            'schema_code': schema_code,
            'route_code': route_code,
            'message': 'Code généré. À valider avant écriture.'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erreur : {str(e)}'}), 500

@bp.route('/list-tables', methods=['GET'])
def list_tables():
    """Retourne la liste des tables SQLite (hors tables système)."""
    try:
        result = db.session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
        )
        tables = [row[0] for row in result.fetchall()]
        return jsonify({
            'success': True,
            'tables': tables,
            'message': f'{len(tables)} tables trouvées.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'tables': [],
            'message': f'Erreur lors de la récupération des tables : {str(e)}'
        }), 500 

@bp.route('/drop-table', methods=['POST'])
def drop_table():
    """
    Supprime une table de la base SQLite.
    Reçoit : { "table_name": "nom_table" }
    """
    try:
        data = request.get_json()
        table_name = data.get('table_name')
        if not table_name:
            return jsonify({'success': False, 'message': 'Nom de table requis.'}), 400
        db.session.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
        db.session.commit()
        return jsonify({'success': True, 'message': f'Table {table_name} supprimée.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Erreur : {str(e)}'}), 500

@bp.route('/alter-table', methods=['POST'])
def alter_table():
    """
    Ajoute une colonne à une table existante.
    Reçoit : {
      "table_name": "nom_table",
      "column": {
        "name": "nouvelle_colonne",
        "type": "String", // ou Integer, Numeric, etc.
        "nullable": true,
        "unique": false,
        "default": null,
        "max_length": 100 // optionnel
      }
    }
    """
    try:
        data = request.get_json()
        table_name = data.get('table_name')
        col = data.get('column')
        if not table_name or not col:
            return jsonify({'success': False, 'message': 'table_name et column requis.'}), 400
        type_mapping = {
            'Integer': 'INTEGER',
            'String': f"TEXT{f'({col.get('max_length', 100)})' if col.get('max_length') else ''}",
            'Text': 'TEXT',
            'Numeric': 'REAL',
            'REAL': 'REAL',
            'Boolean': 'INTEGER',
            'Date': 'TEXT',
            'DateTime': 'TEXT',
            'Time': 'TEXT',
            'Timestamp': 'TEXT',
            'JSON': 'TEXT',
            'LargeBinary': 'BLOB',
            'Enum': 'TEXT'
        }
        sql_type = type_mapping.get(col['type'], 'TEXT')
        col_def = f"{col['name']} {sql_type}"
        if not col.get('nullable', True):
            col_def += " NOT NULL"
        if col.get('unique', False):
            col_def += " UNIQUE"
        if col.get('default') not in [None, '']:
            default_val = col['default']
            if col['type'] == 'Boolean':
                default_val = '1' if default_val else '0'
            elif col['type'] == 'String':
                default_val = f"'{default_val}'"
            col_def += f" DEFAULT {default_val}"
        db.session.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {col_def}"))
        db.session.commit()
        return jsonify({'success': True, 'message': f'Colonne {col['name']} ajoutée à {table_name}.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Erreur : {str(e)}'}), 500 

def get_all_tables():
    """Récupère toutes les tables de la base de données"""
    try:
        result = db.session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT IN ('alembic_version') ORDER BY name;")
        )
        return [row[0] for row in result.fetchall()]
    except Exception:
        return []


@bp.route('/sync-flask-admin', methods=['POST'])
def sync_flask_admin():
    """Synchronise toutes les tables avec Flask-Admin"""
    try:
        # Lister toutes les tables
        tables = get_all_tables()
        
        if not tables:
            return jsonify({
                'success': False,
                'message': 'Aucune table trouvée dans la base de données'
            })
        
        # Importer le script de génération
        import sys
        import subprocess
        
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts', 'simple_model_generator.py')
        
        generated_tables = []
        errors = []
        
        for table_name in tables:
            # Ignorer les tables système
            if table_name.startswith('sqlite_') or table_name in ['alembic_version']:
                continue
                
            try:
                # Exécuter le script de génération pour chaque table
                result = subprocess.run([
                    sys.executable, script_path, table_name
                ], capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
                
                if result.returncode == 0:
                    generated_tables.append(table_name)
                    print(f"✅ {table_name} généré avec succès")
                else:
                    error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
                    errors.append(f"{table_name}: {error_msg}")
                    print(f"❌ Erreur pour {table_name}: {error_msg}")
                    
            except Exception as e:
                errors.append(f"{table_name}: {str(e)}")
                print(f"❌ Exception pour {table_name}: {str(e)}")
        
        # Préparer le message de réponse
        message_parts = []
        
        if generated_tables:
            message_parts.append(f"✅ {len(generated_tables)} table(s) synchronisée(s) :")
            for table in generated_tables:
                message_parts.append(f"  • {table}")
        
        if errors:
            message_parts.append(f"\n❌ {len(errors)} erreur(s) :")
            for error in errors[:5]:  # Limiter à 5 erreurs pour l'affichage
                message_parts.append(f"  • {error}")
            if len(errors) > 5:
                message_parts.append(f"  • ... et {len(errors) - 5} autres erreurs")
        
        message_parts.append("\n🔄 Redémarrez Flask-Admin pour voir les changements")
        
        return jsonify({
            'success': len(generated_tables) > 0,
            'message': '\n'.join(message_parts),
            'generated_tables': generated_tables,
            'errors': errors
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la synchronisation : {str(e)}'
        }), 500 