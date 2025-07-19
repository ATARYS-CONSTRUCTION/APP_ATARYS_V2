"""
Routes pour le générateur de relations étape par étape
"""
from flask import Blueprint, jsonify, request
from app.services.relation_generator import relation_generator

relation_generator_bp = Blueprint('relation_generator', __name__)


@relation_generator_bp.route('/api/relation-generator/list-tables', methods=['GET'])
def list_tables():
    """Lister toutes les tables disponibles pour les relations"""
    try:
        tables = relation_generator.get_all_tables()
        return jsonify({
            'success': True,
            'data': tables,
            'message': f'{len(tables)} tables disponibles'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur listing tables : {str(e)}'
        }), 500


@relation_generator_bp.route('/api/relation-generator/get-table-info/<table_name>', methods=['GET'])
def get_table_info(table_name):
    """Récupérer les informations d'une table spécifique"""
    try:
        table_info = relation_generator.get_table_info(table_name)
        if table_info:
            return jsonify({
                'success': True,
                'data': table_info,
                'message': f'Informations de {table_name} récupérées'
            })
        else:
            return jsonify({
                'success': False,
                'message': f'Table {table_name} non trouvée'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur récupération info table : {str(e)}'
        }), 500


@relation_generator_bp.route('/api/relation-generator/generate-relation', methods=['POST'])
def generate_relation():
    """Générer le code de relation étape par étape"""
    try:
        data = request.get_json()
        
        source_table = data.get('source_table')
        target_table = data.get('target_table')
        relation_type = data.get('relation_type', 'many-to-one')
        cascade = data.get('cascade', '')
        lazy = data.get('lazy', 'select')
        
        if not source_table or not target_table:
            return jsonify({
                'success': False,
                'message': 'Tables source et cible requises'
            }), 400
        
        if source_table == target_table:
            return jsonify({
                'success': False,
                'message': 'Les tables source et cible doivent être différentes'
            }), 400
        
        # Générer le code de relation
        relation_code = relation_generator.generate_relation_code(
            source_table, target_table, relation_type, cascade, lazy
        )
        
        if relation_code:
            return jsonify({
                'success': True,
                'data': relation_code,
                'message': 'Code de relation généré avec succès'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Erreur lors de la génération du code'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur génération relation : {str(e)}'
        }), 500


@relation_generator_bp.route('/api/relation-generator/validate-relation', methods=['POST'])
def validate_relation():
    """Valider une relation avant génération"""
    try:
        data = request.get_json()
        
        source_table = data.get('source_table')
        target_table = data.get('target_table')
        
        if not source_table or not target_table:
            return jsonify({
                'success': False,
                'message': 'Tables source et cible requises'
            }), 400
        
        # Vérifier l'existence des tables
        source_info = relation_generator.get_table_info(source_table)
        target_info = relation_generator.get_table_info(target_table)
        
        if not source_info:
            return jsonify({
                'success': False,
                'message': f'Table source {source_table} non trouvée'
            }), 404
        
        if not target_info:
            return jsonify({
                'success': False,
                'message': f'Table cible {target_table} non trouvée'
            }), 404
        
        # Vérifier si la clé étrangère existe déjà
        foreign_key_name = f"{target_table}_id"
        source_columns = [col['name'] for col in source_info['columns']]
        
        if foreign_key_name in source_columns:
            return jsonify({
                'success': False,
                'message': f'La clé étrangère {foreign_key_name} existe déjà dans {source_table}'
            }), 400
        
        return jsonify({
            'success': True,
            'data': {
                'source_info': source_info,
                'target_info': target_info,
                'foreign_key_name': foreign_key_name,
                'is_valid': True
            },
            'message': 'Relation valide'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur validation relation : {str(e)}'
        }), 500 