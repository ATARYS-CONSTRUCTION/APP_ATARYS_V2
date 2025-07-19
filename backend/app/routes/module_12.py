"""
Module 12 - Routes API Flask
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Utilise Blueprint
- Format de réponse {success, data, message}
- Validation Marshmallow obligatoire
"""
from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields
from app import db
from app.models.module_12 import TestAuditTable
from app.models.module_12 import TestCle2

module_12_bp = Blueprint('module_12', __name__)

# Routes du module 12 - PARAMÈTRES
# Ajouter ici les routes du module 12 selon les besoins 


# Schéma et routes CRUD pour TestAuditTable
class TestAuditTableSchema(Schema):
    nom = fields.String()
    prix = fields.Decimal()
    actif = fields.Boolean()
    date_creation = fields.DateTime()


test_audit_table_schema = TestAuditTableSchema()
test_audit_table_schemas = TestAuditTableSchema(many=True)

@module_12_bp.route('/api/test_audit_table/', methods=['GET'])
def list_test_audit_table():
    try:
        items = TestAuditTable.query.all()
        return jsonify({
            'success': True,
            'data': test_audit_table_schemas.dump(items),
            'message': f'{len(items)} test_audit_table trouvés'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@module_12_bp.route('/api/test_audit_table/', methods=['POST'])
def create_test_audit_table():
    try:
        data = request.get_json()
        errors = test_audit_table_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        new_item = TestAuditTable(**data)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({
            'success': True,
            'data': test_audit_table_schema.dump(new_item),
            'message': 'TestAuditTable créé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@module_12_bp.route('/api/test_audit_table/<int:item_id>', methods=['PUT'])
def update_test_audit_table(item_id):
    try:
        item = TestAuditTable.query.get_or_404(item_id)
        data = request.get_json()
        errors = test_audit_table_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        return jsonify({
            'success': True,
            'data': test_audit_table_schema.dump(item),
            'message': 'TestAuditTable modifié avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@module_12_bp.route('/api/test_audit_table/<int:item_id>', methods=['DELETE'])
def delete_test_audit_table(item_id):
    try:
        item = TestAuditTable.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'TestAuditTable supprimé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400





# Routes CRUD pour TestCle2
from app.schemas.module_12 import TestCle2Schema
test_cle2_schema = TestCle2Schema()
test_cle2_schemas = TestCle2Schema(many=True)

@module_12_bp.route('/api/test_cle2/', methods=['GET'])
def list_test_cle2():
    try:
        items = TestCle2.query.all()
        return jsonify({
            'success': True,
            'data': test_cle2_schemas.dump(items),
            'message': f'{len(items)} test_cle2 trouvés'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@module_12_bp.route('/api/test_cle2/', methods=['POST'])
def create_test_cle2():
    try:
        data = request.get_json()
        errors = test_cle2_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        new_item = TestCle2(**data)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({
            'success': True,
            'data': test_cle2_schema.dump(new_item),
            'message': 'TestCle2 créé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@module_12_bp.route('/api/test_cle2/<int:item_id>', methods=['PUT'])
def update_test_cle2(item_id):
    try:
        item = TestCle2.query.get_or_404(item_id)
        data = request.get_json()
        errors = test_cle2_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        return jsonify({
            'success': True,
            'data': test_cle2_schema.dump(item),
            'message': 'TestCle2 modifié avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@module_12_bp.route('/api/test_cle2/<int:item_id>', methods=['DELETE'])
def delete_test_cle2(item_id):
    try:
        item = TestCle2.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'TestCle2 supprimé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400
