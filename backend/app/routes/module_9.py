"""
Module 9 - Routes API Flask
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Utilise Blueprint
- Format de réponse {success, data, message}
- Validation Marshmallow obligatoire
"""
import os
import subprocess
from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields
from app import db
from app.models.module_9 import NiveauQualification, Salaries
from app.schemas.module_9 import NiveauQualificationSchema, SalariesSchema
from app.utils.onedrive_detector import onedrive_detector

module_9_bp = Blueprint('module_9', __name__)

# Routes du module 9 - SOCIAL
# Ajouter ici les routes du module 9 selon les besoins

# Initialisation des schémas
niveau_qualification_schema = NiveauQualificationSchema()
niveau_qualification_schemas = NiveauQualificationSchema(many=True)
salaries_schema = SalariesSchema()
salaries_schemas = SalariesSchema(many=True)

# Routes CRUD pour NiveauQualification
@module_9_bp.route('/api/niveau_qualification/', methods=['GET'])
def list_niveau_qualification():
    try:
        items = NiveauQualification.query.all()
        return jsonify({
            'success': True,
            'data': niveau_qualification_schemas.dump(items),
            'message': f'{len(items)} niveau_qualification trouvés'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@module_9_bp.route('/api/niveau_qualification/', methods=['POST'])
def create_niveau_qualification():
    try:
        data = request.get_json()
        errors = niveau_qualification_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        new_item = NiveauQualification(**data)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({
            'success': True,
            'data': niveau_qualification_schema.dump(new_item),
            'message': 'NiveauQualification créé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@module_9_bp.route('/api/niveau_qualification/<int:item_id>', methods=['PUT'])
def update_niveau_qualification(item_id):
    try:
        item = NiveauQualification.query.get_or_404(item_id)
        data = request.get_json()
        errors = niveau_qualification_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        return jsonify({
            'success': True,
            'data': niveau_qualification_schema.dump(item),
            'message': 'NiveauQualification modifié avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@module_9_bp.route('/api/niveau_qualification/<int:item_id>', methods=['DELETE'])
def delete_niveau_qualification(item_id):
    try:
        item = NiveauQualification.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'NiveauQualification supprimé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


# Routes CRUD pour Salaries
@module_9_bp.route('/api/salaries/', methods=['GET'])
def list_salaries():
    try:
        # Récupérer le paramètre actif depuis la requête
        actif = request.args.get('actif', type=str)
        
        if actif == 'true':
            # Filtrer les salariés actifs (sans date de sortie ou date de sortie dans le futur)
            from datetime import date
            today = date.today()
            items = Salaries.query.filter(
                (Salaries.date_sortie.is_(None)) | 
                (Salaries.date_sortie > today)
            ).all()
        else:
            # Retourner tous les salariés
            items = Salaries.query.all()
        
        return jsonify({
            'success': True,
            'data': salaries_schemas.dump(items),
            'message': f'{len(items)} salaries trouvés'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@module_9_bp.route('/api/salaries/', methods=['POST'])
def create_salaries():
    try:
        data = request.get_json()
        errors = salaries_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        
        # Conversion des chaînes de dates en objets date Python
        from datetime import datetime
        
        # Convertir date_naissance si présente
        if data.get('date_naissance') and isinstance(data['date_naissance'], str):
            try:
                data['date_naissance'] = datetime.strptime(data['date_naissance'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'success': False, 'message': 'Format de date invalide pour date_naissance'}), 400
        
        # Convertir date_entree si présente
        if data.get('date_entree') and isinstance(data['date_entree'], str):
            try:
                data['date_entree'] = datetime.strptime(data['date_entree'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'success': False, 'message': 'Format de date invalide pour date_entree'}), 400
        
        # Convertir date_sortie si présente
        if data.get('date_sortie') and isinstance(data['date_sortie'], str):
            try:
                data['date_sortie'] = datetime.strptime(data['date_sortie'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'success': False, 'message': 'Format de date invalide pour date_sortie'}), 400
        
        # Gestion des familles d'ouvrages (relation many-to-many)
        famille_ouvrages_ids = data.pop('famille_ouvrages_ids', [])
        
        new_item = Salaries(**data)
        db.session.add(new_item)
        db.session.flush()  # Pour obtenir l'ID du nouveau salarié
        
        # Ajouter les familles d'ouvrages
        if famille_ouvrages_ids:
            from app.models.module_5 import FamilleOuvrages
            for famille_id in famille_ouvrages_ids:
                famille = FamilleOuvrages.query.get(famille_id)
                if famille:
                    new_item.famille_ouvrages.append(famille)
        
        db.session.commit()
        return jsonify({
            'success': True,
            'data': salaries_schema.dump(new_item),
            'message': 'Salaries créé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@module_9_bp.route('/api/salaries/<int:item_id>', methods=['PUT'])
def update_salaries(item_id):
    try:
        item = Salaries.query.get_or_404(item_id)
        data = request.get_json()
        errors = salaries_schema.validate(data)
        if errors:
            return jsonify({'success': False, 'message': errors}), 400
        
        # Conversion des chaînes de dates en objets date Python
        from datetime import datetime
        
        # Convertir date_naissance si présente
        if data.get('date_naissance') and isinstance(data['date_naissance'], str):
            try:
                data['date_naissance'] = datetime.strptime(data['date_naissance'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'success': False, 'message': 'Format de date invalide pour date_naissance'}), 400
        
        # Convertir date_entree si présente
        if data.get('date_entree') and isinstance(data['date_entree'], str):
            try:
                data['date_entree'] = datetime.strptime(data['date_entree'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'success': False, 'message': 'Format de date invalide pour date_entree'}), 400
        
        # Convertir date_sortie si présente
        if data.get('date_sortie') and isinstance(data['date_sortie'], str):
            try:
                data['date_sortie'] = datetime.strptime(data['date_sortie'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'success': False, 'message': 'Format de date invalide pour date_sortie'}), 400
        
        # Gestion des familles d'ouvrages (relation many-to-many)
        famille_ouvrages_ids = data.pop('famille_ouvrages_ids', [])
        
        # Mettre à jour les champs du salarié
        for key, value in data.items():
            setattr(item, key, value)
        
        # Mettre à jour les familles d'ouvrages
        item.famille_ouvrages.clear()  # Supprimer toutes les relations existantes
        if famille_ouvrages_ids:
            from app.models.module_5 import FamilleOuvrages
            for famille_id in famille_ouvrages_ids:
                famille = FamilleOuvrages.query.get(famille_id)
                if famille:
                    item.famille_ouvrages.append(famille)
        
        db.session.commit()
        return jsonify({
            'success': True,
            'data': salaries_schema.dump(item),
            'message': 'Salaries modifié avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@module_9_bp.route('/api/salaries/<int:item_id>', methods=['DELETE'])
def delete_salaries(item_id):
    try:
        item = Salaries.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Salaries supprimé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@module_9_bp.route('/api/open-explorer', methods=['POST'])
def open_explorer():
    try:
        data = request.get_json()
        relative_path = data.get('path')
        
        if not relative_path:
            return jsonify({
                'success': False, 
                'message': 'Chemin relatif manquant'
            }), 400
        
        # Utiliser le détecteur OneDrive pour résoudre le chemin
        resolved_path = onedrive_detector.resolve_relative_path(relative_path)
        
        if not resolved_path:
            return jsonify({
                'success': False, 
                'message': 'OneDrive non trouvé sur le système'
            }), 404
        
        # Vérifier que le dossier existe
        if not os.path.exists(resolved_path):
            return jsonify({
                'success': False, 
                'message': f'Le dossier n\'existe pas: {resolved_path}'
            }), 404
        
        # Ouvrir l'explorateur Windows
        try:
            os.startfile(resolved_path)
            return jsonify({
                'success': True, 
                'message': f'Explorateur ouvert: {resolved_path}',
                'resolved_path': resolved_path,
                'relative_path': relative_path
            })
        except Exception as e:
            # Fallback avec subprocess
            subprocess.run(['explorer', resolved_path], check=True)
            return jsonify({
                'success': True, 
                'message': f'Explorateur ouvert: {resolved_path}',
                'resolved_path': resolved_path,
                'relative_path': relative_path
            })
            
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Erreur lors de l\'ouverture: {str(e)}'
        }), 500

@module_9_bp.route('/api/test-onedrive-path', methods=['POST'])
def test_onedrive_path():
    """Teste un chemin relatif OneDrive"""
    try:
        data = request.get_json()
        relative_path = data.get('path')
        
        if not relative_path:
            return jsonify({
                'success': False, 
                'message': 'Chemin relatif manquant'
            }), 400
        
        # Tester le chemin avec le détecteur
        result = onedrive_detector.test_path(relative_path)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Erreur lors du test: {str(e)}'
        }), 500

@module_9_bp.route('/api/onedrive-info', methods=['GET'])
def get_onedrive_info():
    """Retourne les informations OneDrive"""
    try:
        info = onedrive_detector.get_detection_info()
        return jsonify({
            'success': True,
            'data': info
        })
        
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Erreur lors de la récupération des infos: {str(e)}'
        }), 500


