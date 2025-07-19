#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - ROUTES UNIFIÉES POUR LA GESTION DE BASE DE DONNÉES
API centralisée pour toutes les opérations sur les tables et relations

Auteur: ATARYS Team
Date: 2025
Version: 2.0 - Architecture unifiée
"""

from flask import Blueprint, request, jsonify
from app.services.database_manager import database_manager
from sqlalchemy import inspect
from app import db

# Blueprint pour l'API unifiée de base de données
database_api_bp = Blueprint('database_api', __name__)


# ============================================================================
# ROUTES POUR LES TABLES
# ============================================================================

@database_api_bp.route('/api/database/tables', methods=['GET'])
def list_tables():
    """Lister toutes les tables de la base de données"""
    try:
        result = database_manager.list_tables()
        return jsonify(result), 200 if result['success'] else 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur serveur : {str(e)}'
        }), 500


@database_api_bp.route('/api/database/tables/<table_name>', methods=['GET'])
def get_table_info(table_name):
    """Récupérer les informations détaillées d'une table"""
    try:
        result = database_manager.get_table_info(table_name)
        return jsonify(result), 200 if result['success'] else 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur serveur : {str(e)}'
        }), 500


@database_api_bp.route('/api/database/tables', methods=['POST'])
def create_table():
    """Créer une nouvelle table avec modèle et routes"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Données JSON requises'
            }), 400
        
        # Validation des données requises
        required_fields = ['table_name', 'columns']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Champ requis manquant : {field}'
                }), 400
        
        # Gestion du module_id
        if 'module_id' not in data and 'module' not in data:
            return jsonify({
                'success': False,
                'message': 'Champ requis manquant : module_id ou module'
            }), 400
        
        # Si module est fourni, le convertir en module_id
        if 'module' in data and 'module_id' not in data:
            module_str = data['module']
            # Convertir "12.1" en "12_1"
            module_id = module_str.replace('.', '_')
            data['module_id'] = module_id
        
        # Création de la table via le service
        result = database_manager.create_table(data)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur serveur : {str(e)}'
        }), 500


@database_api_bp.route('/api/database/tables/<table_name>', methods=['DELETE'])
def delete_table(table_name):
    """Supprimer une table complètement (base + fichiers générés)"""
    try:
        result = database_manager.delete_table(table_name)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur serveur : {str(e)}'
        }), 500


@database_api_bp.route('/api/database/tables/<table_name>/bulk-insert', methods=['POST'])
def bulk_insert_data(table_name):
    """Insérer des données en masse dans une table dynamique"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Données JSON requises'
            }), 400
        
        # Validation des données
        if 'data' not in data or not isinstance(data['data'], list):
            return jsonify({
                'success': False,
                'message': 'Champ "data" requis avec une liste de données'
            }), 400
        
        # Insertion via le service
        result = database_manager.bulk_insert(table_name, data['data'])
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur serveur : {str(e)}'
        }), 500


# ============================================================================
# ROUTES POUR LES RELATIONS
# ============================================================================

@database_api_bp.route('/api/database/relations', methods=['GET'])
def list_relations():
    """Lister toutes les relations existantes"""
    try:
        result = database_manager.list_relations()
        return jsonify(result), 200 if result['success'] else 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur serveur : {str(e)}'
        }), 500


@database_api_bp.route('/api/database/relations', methods=['POST'])
def create_relation():
    """Créer une nouvelle relation entre tables"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Données JSON requises'
            }), 400
        
        # Validation des données requises
        required_fields = ['source_table', 'target_table']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Champ requis manquant : {field}'
                }), 400
        
        # Création de la relation via le service
        result = database_manager.create_relation(data)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur serveur : {str(e)}'
        }), 500


@database_api_bp.route('/api/database/relations/validate', methods=['POST'])
def validate_foreign_key():
    """Valider si une clé étrangère est possible"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Données JSON requises'
            }), 400
        
        # Validation des données requises
        required_fields = ['source_table', 'source_column', 'target_table', 'target_column']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Champ requis manquant : {field}'
                }), 400
        
        # Validation via le service
        result = database_manager.validate_foreign_key(
            data['source_table'], data['source_column'],
            data['target_table'], data['target_column']
        )
        
        return jsonify(result), 200 if result['success'] else 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur serveur : {str(e)}'
        }), 500


# ============================================================================
# ROUTES POUR LA GÉNÉRATION DE CODE
# ============================================================================

@database_api_bp.route('/api/database/generate/table', methods=['POST'])
def generate_table_code():
    """Générer le code pour une table"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Données JSON requises'
            }), 400
        
        # Validation des données requises
        required_fields = ['table_name', 'class_name', 'module_id', 'columns']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Champ requis manquant : {field}'
                }), 400
        
        # Génération via le service
        result = database_manager.generate_table_code(data)
        
        return jsonify(result), 200 if result['success'] else 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur serveur : {str(e)}'
        }), 500


@database_api_bp.route('/api/database/generate/relation', methods=['POST'])
def generate_relation_code():
    """Générer le code pour une relation"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Données JSON requises'
            }), 400
        
        # Validation des données requises
        required_fields = ['source_table', 'target_table']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Champ requis manquant : {field}'
                }), 400
        
        # Génération via le service
        result = database_manager.generate_relation_code(data)
        
        return jsonify(result), 200 if result['success'] else 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur serveur : {str(e)}'
        }), 500


# ============================================================================
# ROUTES DE TEST ET DIAGNOSTIC
# ============================================================================

@database_api_bp.route('/api/database/test', methods=['GET'])
def test_route():
    """Route de test pour vérifier que l'API fonctionne"""
    return jsonify({
        'success': True,
        'message': 'API Database unifiée fonctionne !',
        'data': {
            'service': 'DatabaseManager',
            'version': '2.0',
            'endpoints': [
                'GET /api/database/tables',
                'POST /api/database/tables',
                'DELETE /api/database/tables/<table_name>',
                'POST /api/database/tables/<table_name>/bulk-insert',
                'GET /api/database/relations',
                'POST /api/database/relations',
                'POST /api/database/relations/validate',
                'POST /api/database/generate/table',
                'POST /api/database/generate/relation'
            ]
        }
    }), 200


@database_api_bp.route('/api/database/status', methods=['GET'])
def get_database_status():
    """Obtenir le statut de la base de données"""
    try:
        # Lister les tables pour vérifier la connexion
        tables_result = database_manager.list_tables()
        
        if tables_result['success']:
            return jsonify({
                'success': True,
                'message': 'Base de données accessible',
                'data': {
                    'tables_count': len(tables_result['data']),
                    'tables': tables_result['data'][:10],  # Limiter à 10 pour l'affichage
                    'db_path': database_manager.db_path
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Problème d\'accès à la base de données',
                'error': tables_result['message']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la vérification du statut : {str(e)}'
        }), 500 