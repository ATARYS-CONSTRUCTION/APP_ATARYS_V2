"""
Routes pour la synchronisation des tables SQLite avec le backend
"""
from flask import Blueprint, jsonify
from app.services.table_sync import table_sync

table_sync_bp = Blueprint('table_sync', __name__)

@table_sync_bp.route('/api/table-sync/sync-all', methods=['POST'])
def sync_all_tables():
    """Synchroniser toutes les tables SQLite avec le backend"""
    try:
        result = table_sync.sync_all_tables()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur synchronisation : {str(e)}'
        }), 500

@table_sync_bp.route('/api/table-sync/sync-table/<table_name>', methods=['POST'])
def sync_single_table(table_name):
    """Synchroniser une table spécifique"""
    try:
        result = table_sync.sync_single_table(table_name)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur synchronisation {table_name} : {str(e)}'
        }), 500

@table_sync_bp.route('/api/table-sync/list-tables', methods=['GET'])
def list_tables_for_sync():
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