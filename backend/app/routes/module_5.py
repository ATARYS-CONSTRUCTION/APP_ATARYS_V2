"""
 Module 5 - Routes API Flask
 Respecte les standards ATARYS V2 (voir .cursorrules et
  docs/02-architecture/ATARYS_MODULES.md)
 - Utilise Blueprint
 - Format de réponse {success, data, message}
 - Validation Marshmallow obligatoire
 """


from flask import Blueprint, jsonify, request
from app import db
from app.models.module_5 import FamilleOuvrages
from app.schemas.module_5 import FamilleOuvragesSchema

module_5_bp = Blueprint('module_5', __name__)

# Schémas
famille_ouvrages_schema = FamilleOuvragesSchema()
famille_ouvrages_schemas = FamilleOuvragesSchema(many=True)

# ---------------------------------------------------------------------------
# Routes CRUD pour FamilleOuvrages
# ---------------------------------------------------------------------------

@module_5_bp.route('/api/famille_ouvrages/', methods=['GET'])
def list_famille_ouvrages():
    try:
        items = FamilleOuvrages.query.all()
        return jsonify({
            'success': True,
            'data': famille_ouvrages_schemas.dump(items),
            'message': f"{len(items)} famille_ouvrages trouvés"
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@module_5_bp.route('/api/famille_ouvrages/', methods=['POST'])
def create_famille_ouvrages():
    try:
        data = request.get_json()
        errors = famille_ouvrages_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        new_item = FamilleOuvrages(**data)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({
            'success': True,
            'data': famille_ouvrages_schema.dump(new_item),
            'message': 'FamilleOuvrages créé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


@module_5_bp.route('/api/famille_ouvrages/<int:item_id>', methods=['PUT'])
def update_famille_ouvrages(item_id):
    try:
        item = FamilleOuvrages.query.get_or_404(item_id)
        data = request.get_json()
        errors = famille_ouvrages_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        return jsonify({
            'success': True,
            'data': famille_ouvrages_schema.dump(item),
            'message': 'FamilleOuvrages modifié avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


@module_5_bp.route('/api/famille_ouvrages/<int:item_id>', methods=['DELETE'])
def delete_famille_ouvrages(item_id):
    try:
        item = FamilleOuvrages.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True, 'message': 'FamilleOuvrages supprimé avec succès'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400
