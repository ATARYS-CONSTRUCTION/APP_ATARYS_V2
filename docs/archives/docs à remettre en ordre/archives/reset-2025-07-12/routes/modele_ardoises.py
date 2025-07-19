from flask import Blueprint, request, jsonify
from app import db
from app.models.modele_ardoises_model import ModeleArdoises

bp = Blueprint('modele_ardoises', __name__, url_prefix='/api/modele-ardoises')

@bp.route('/', methods=['GET'])
def get_all():
    page = int(request.args.get('page', 1))
    per_page = request.args.get('per_page', 'all')
    
    query = ModeleArdoises.query
    total = query.count()
    
    if per_page == 'all':
        items = query.order_by(ModeleArdoises.id.desc()).all()
        data = [{
            'id': item.id,
            **{k: v for k, v in item.__dict__.items() if not k.startswith('_')}
        } for item in items]
        return jsonify({
            'success': True,
            'data': data,
            'message': f'Liste complète ({total})',
            'pagination': {
                'page': 1,
                'per_page': total,
                'total': total,
                'has_next': False
            }
        })
    else:
        per_page = int(per_page)
        items = query.order_by(ModeleArdoises.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        data = [{
            'id': item.id,
            **{k: v for k, v in item.__dict__.items() if not k.startswith('_')}
        } for item in items.items]
        return jsonify({
            'success': True,
            'data': data,
            'message': f'Liste (page {page})',
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'has_next': items.has_next
            }
        })

@bp.route('/', methods=['POST'])
def create():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'success': False, 'data': [], 'message': 'Aucune donnée reçue'}), 400
    
    item = ModeleArdoises(**json_data)
    db.session.add(item)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': {'id': item.id, **{k: v for k, v in item.__dict__.items() if not k.startswith('_')}},
        'message': 'Élément créé'
    })

@bp.route('/<int:item_id>', methods=['DELETE'])
def delete(item_id):
    item = ModeleArdoises.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({'success': True, 'data': [], 'message': 'Élément supprimé'})

@bp.route('/clear/', methods=['DELETE'])
def clear_all():
    try:
        num_deleted = db.session.query(ModeleArdoises).delete()
        db.session.commit()
        return jsonify({
            'success': True,
            'data': [],
            'message': f'{num_deleted} éléments supprimés.'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'data': [],
            'message': f'Erreur lors de la suppression : {str(e)}'
        }), 500
