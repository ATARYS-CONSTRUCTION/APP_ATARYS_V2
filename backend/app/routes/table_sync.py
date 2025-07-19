"""
Routes pour la synchronisation des tables SQLite avec le backend
"""
from flask import Blueprint, jsonify
from app.services.table_sync import table_sync

table_sync_bp = Blueprint('table_sync', __name__)


@table_sync_bp.route('/api/table-sync/list-tables', methods=['GET'])
def list_tables():
    """Lister toutes les tables SQLite disponibles"""
    try:
        tables = table_sync._get_all_tables()
        return jsonify({
            'success': True,
            'data': [t for t in tables if not t.startswith('sqlite_')],
            'message': f'{len(tables)} tables trouvées'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur listing tables : {str(e)}'
        }), 500


@table_sync_bp.route('/api/table-sync/list-columns/<table_name>', 
                     methods=['GET'])
def list_columns(table_name):
    """Lister les colonnes d'une table spécifique"""
    try:
        columns = table_sync._get_table_columns(table_name)
        return jsonify({
            'success': True,
            'data': columns,
            'message': f'Colonnes de {table_name} récupérées'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur listing colonnes : {str(e)}'
        }), 500


@table_sync_bp.route('/api/table-sync/generate-relation', methods=['POST'])
def generate_relation():
    """Générer le code de relation Python"""
    try:
        from flask import request
        data = request.get_json()
        
        source_table = data.get('source_table')
        source_column = data.get('source_column')
        target_table = data.get('target_table')
        target_column = data.get('target_column')
        relation_name = data.get('relation_name')
        
        required_params = [source_table, source_column, target_table,
                          target_column, relation_name]
        if not all(required_params):
            return jsonify({
                'success': False,
                'message': 'Tous les paramètres sont requis'
            }), 400
        
        relation_code = table_sync.generate_relation_code(
            source_table, source_column, target_table, target_column, 
            relation_name
        )
        
        return jsonify({
            'success': True,
            'data': {
                'relation_code': relation_code,
                'instructions': 'Copiez ce code dans votre modèle Python'
            },
            'message': 'Code de relation généré'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur génération relation : {str(e)}'
        }), 500


@table_sync_bp.route('/api/table-sync/validate-foreign-key', methods=['POST'])
def validate_foreign_key():
    """Valider une clé étrangère"""
    try:
        from flask import request
        data = request.get_json()
        
        source_table = data.get('source_table')
        source_column = data.get('source_column')
        target_table = data.get('target_table')
        target_column = data.get('target_column')
        
        if not all([source_table, source_column, target_table, target_column]):
            return jsonify({
                'success': False,
                'message': 'Tous les paramètres sont requis'
            }), 400
        
        is_valid = table_sync.validate_foreign_key(
            source_table, source_column, target_table, target_column
        )
        
        valid_msg = ('Clé étrangère valide' if is_valid 
                    else 'Clé étrangère invalide')
        return jsonify({
            'success': True,
            'data': {
                'is_valid': is_valid,
                'message': valid_msg
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur validation : {str(e)}'
        }), 500 