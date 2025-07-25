"""
Module 3 - Routes API Flask
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Utilise Blueprint
- Format de réponse {success, data, message}
- Validation Marshmallow obligatoire
"""
from flask import Blueprint, request, jsonify
from app.models.module_3 import Clients
from app.schemas.module_3 import ClientsSchema
from app import db

module_3_bp = Blueprint('module_3', __name__)

# Routes du module 3 - LISTE_CHANTIERS
# Ajouter ici les routes du module 3 selon les besoins

# Routes CRUD pour Clients
clients_schema = ClientsSchema()
clients_schemas = ClientsSchema(many=True)


@module_3_bp.route('/api/clients/', methods=['GET'])
def list_clients():
    """Récupérer tous les clients avec leurs villes"""
    try:
        clients = Clients.query.all()
        return jsonify({
            'success': True,
            'data': clients_schemas.dump(clients),
            'message': f'{len(clients)} clients trouvés'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@module_3_bp.route('/api/clients/', methods=['POST'])
def create_client():
    """Créer un nouveau client"""
    try:
        data = request.get_json()
        errors = clients_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        
        new_client = Clients(**data)
        db.session.add(new_client)
        db.session.commit()
        
        # TODO: DÉCLENCHEUR AUTOMATIQUE - À IMPLÉMENTER
        # Lors de la création d'un client, déclencher les tâches automatiques
        # service = TacheAutomatiqueService()
        # contexte = {'client_id': new_client.id}
        # taches_creees = service.declencher_taches(
        #     'client_creation', contexte
        # )
        
        return jsonify({
            'success': True,
            'data': clients_schema.dump(new_client),
            'message': 'Client créé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


@module_3_bp.route('/api/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    """Modifier un client existant"""
    try:
        client = Clients.query.get_or_404(client_id)
        data = request.get_json()
        errors = clients_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        
        for key, value in data.items():
            setattr(client, key, value)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': clients_schema.dump(client),
            'message': 'Client modifié avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


@module_3_bp.route('/api/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    """Supprimer un client"""
    try:
        client = Clients.query.get_or_404(client_id)
        db.session.delete(client)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Client supprimé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400
