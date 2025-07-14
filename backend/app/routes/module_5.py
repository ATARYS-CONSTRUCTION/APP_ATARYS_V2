"""
Module 5 - Routes API Flask
Respecte les standards ATARYS V2 (voir .cursorrules et docs/02-architecture/ATARYS_MODULES.md)
- Utilise Blueprint
- Format de réponse {success, data, message}
- Validation Marshmallow obligatoire
"""
from flask import Blueprint, jsonify, request

module_5_bp = Blueprint('module_5', __name__)

# Routes du module 5 - DEVIS_FACTURATION
# Ajouter ici les routes du module 5 selon les besoins 

# Schéma et routes CRUD pour TestProfessionalTable
class TestProfessionalTableSchema(Schema):
    nom = fields.String()
    description = fields.String()
    montant = fields.Decimal()
    actif = fields.Boolean()

test_professional_table_schema = TestProfessionalTableSchema()
test_professional_table_schemas = TestProfessionalTableSchema(many=True)

@module_5_bp.route('/api/test_professional_table/', methods=['GET'])
def list_test_professional_table():
    try:
        items = TestProfessionalTable.query.all()
        return jsonify({
            'success': True,
            'data': test_professional_table_schemas.dump(items),
            'message': f'{len(items)} test_professional_table trouvés'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@module_5_bp.route('/api/test_professional_table/', methods=['POST'])
def create_test_professional_table():
    try:
        data = request.get_json()
        errors = test_professional_table_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        new_item = TestProfessionalTable(**data)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({
            'success': True,
            'data': test_professional_table_schema.dump(new_item),
            'message': 'TestProfessionalTable créé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@module_5_bp.route('/api/test_professional_table/<int:item_id>', methods=['PUT'])
def update_test_professional_table(item_id):
    try:
        item = TestProfessionalTable.query.get_or_404(item_id)
        data = request.get_json()
        errors = test_professional_table_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        return jsonify({
            'success': True,
            'data': test_professional_table_schema.dump(item),
            'message': 'TestProfessionalTable modifié avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@module_5_bp.route('/api/test_professional_table/<int:item_id>', methods=['DELETE'])
def delete_test_professional_table(item_id):
    try:
        item = TestProfessionalTable.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'TestProfessionalTable supprimé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400
