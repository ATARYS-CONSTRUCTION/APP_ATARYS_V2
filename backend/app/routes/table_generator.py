#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - ROUTES POUR GÉNÉRATEUR DE TABLES
API pour le module 12.1 Base de Données

Auteur: ATARYS Team
Date: 2025
Version: 2.0
"""

from flask import Blueprint, request, jsonify
from app.services.table_generator import TableGeneratorService


# Blueprint pour le générateur de tables
table_generator_bp = Blueprint('table_generator', __name__, 
                              url_prefix='/api/table-generator')


@table_generator_bp.route('/test', methods=['GET'])
def test_route():
    """Route de test pour vérifier que le blueprint fonctionne"""
    return jsonify({
        'success': True,
        'message': 'Blueprint table_generator fonctionne !'
    }), 200


@table_generator_bp.route('/create-table', methods=['POST'])
def create_table():
    """
    Créer une nouvelle table avec modèle et routes
    
    POST /api/table-generator/create-table
    """
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
                    'message': f'Champ requis manquant: {field}'
                }), 400
        
        # Gestion du module_id
        if 'module_id' not in data and 'module' not in data:
            return jsonify({
                'success': False,
                'message': 'Champ requis manquant: module_id ou module'
            }), 400
        
        # Si module est fourni, le convertir en module_id
        if 'module' in data and 'module_id' not in data:
            module_str = data['module']
            # Convertir "12.1" en "12_1"
            module_id = module_str.replace('.', '_')
            data['module_id'] = module_id
        
        # Création de la table via le service
        generator = TableGeneratorService()
        result = generator.create_table(table_data=data)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': f'Table {data["table_name"]} créée avec succès dans le module {data["module_id"]}',
                'data': result['data']
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur serveur: {str(e)}'
        }), 500


@table_generator_bp.route('/list-tables', methods=['GET'])
def list_tables():
    """
    Lister toutes les tables générées
    
    GET /api/table-generator/list-tables
    """
    try:
        generator = TableGeneratorService()
        tables = generator.list_tables()
        
        return jsonify({
            'success': True,
            'data': tables
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur serveur: {str(e)}'
        }), 500 


@table_generator_bp.route('/delete-table', methods=['DELETE'])
def delete_table():
    """
    Supprimer une table complètement (base + fichiers générés)
    
    DELETE /api/table-generator/delete-table
    Body: {"table_name": "nom_table"}
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Données JSON requises'
            }), 400
        
        # Validation du nom de table
        if 'table_name' not in data:
            return jsonify({
                'success': False,
                'message': 'Champ requis manquant: table_name'
            }), 400
        
        table_name = data['table_name']
        
        # Suppression via le service
        generator = TableGeneratorService()
        result = generator.delete_table_by_name(table_name)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': f'Table {table_name} supprimée avec succès'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur serveur: {str(e)}'
        }), 500 

@table_generator_bp.route('/check-migrations', methods=['GET'])
def check_migrations():
    """Vérifier l'état des migrations Flask-Migrate"""
    try:
        generator = TableGeneratorService()
        result = generator.check_migration_status()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur vérification migrations : {str(e)}'
        }), 500


@table_generator_bp.route('/migration-help', methods=['GET'])
def get_migration_help():
    """Obtenir l'aide pour les migrations Flask-Migrate"""
    try:
        generator = TableGeneratorService()
        result = generator.get_migration_help()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur aide migrations : {str(e)}'
        }), 500 