"""
Module 10 - Routes API Flask
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Utilise Blueprint
- Format de réponse {success, data, message}
- Validation Marshmallow obligatoire
"""
from flask import Blueprint, jsonify, request
from app.models.module_10 import ModeleArdoises 
from app.models.module_10 import Villes
from app import db
from marshmallow import Schema, fields


module_10_bp = Blueprint('module_10', __name__)

# Routes du module 10 - OUTILS
# Ajouter ici les routes du module 10 selon les besoins 



# Routes CRUD pour ModeleArdoises
from app.schemas.module_10 import ModeleArdoisesSchema
modele_ardoises_schema = ModeleArdoisesSchema()
modele_ardoises_schemas = ModeleArdoisesSchema(many=True)

@module_10_bp.route('/api/modele_ardoises/', methods=['GET'])
def list_modele_ardoises():
    try:
        items = ModeleArdoises.query.all()
        return jsonify({
            'success': True,
            'data': modele_ardoises_schemas.dump(items),
            'message': f'{len(items)} modele_ardoises trouvés'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@module_10_bp.route('/api/modele_ardoises/', methods=['POST'])
def create_modele_ardoises():
    try:
        data = request.get_json()
        errors = modele_ardoises_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        new_item = ModeleArdoises(**data)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({
            'success': True,
            'data': modele_ardoises_schema.dump(new_item),
            'message': 'ModeleArdoises créé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@module_10_bp.route('/api/modele_ardoises/<int:item_id>', methods=['PUT'])
def update_modele_ardoises(item_id):
    try:
        item = ModeleArdoises.query.get_or_404(item_id)
        data = request.get_json()
        errors = modele_ardoises_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        return jsonify({
            'success': True,
            'data': modele_ardoises_schema.dump(item),
            'message': 'ModeleArdoises modifié avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@module_10_bp.route('/api/modele_ardoises/<int:item_id>', methods=['DELETE'])
def delete_modele_ardoises(item_id):
    try:
        item = ModeleArdoises.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'ModeleArdoises supprimé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400




# Routes CRUD pour Villes
from app.schemas.module_10 import VillesSchema
villes_schema = VillesSchema()
villes_schemas = VillesSchema(many=True)

@module_10_bp.route('/api/villes/', methods=['GET'])
def list_villes():
    try:
        items = Villes.query.all()
        return jsonify({
            'success': True,
            'data': villes_schemas.dump(items),
            'message': f'{len(items)} villes trouvés'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@module_10_bp.route('/api/villes/', methods=['POST'])
def create_villes():
    try:
        data = request.get_json()
        errors = villes_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        new_item = Villes(**data)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({
            'success': True,
            'data': villes_schema.dump(new_item),
            'message': 'Villes créé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@module_10_bp.route('/api/villes/<int:item_id>', methods=['PUT'])
def update_villes(item_id):
    try:
        item = Villes.query.get_or_404(item_id)
        data = request.get_json()
        errors = villes_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        return jsonify({
            'success': True,
            'data': villes_schema.dump(item),
            'message': 'Villes modifié avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@module_10_bp.route('/api/villes/<int:item_id>', methods=['DELETE'])
def delete_villes(item_id):
    try:
        item = Villes.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Villes supprimé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400
