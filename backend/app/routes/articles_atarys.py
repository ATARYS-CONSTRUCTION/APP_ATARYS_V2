from flask import Blueprint, request, jsonify
from app import db
from app.models.module_5_1 import articlesatarys
from marshmallow import Schema, fields, validate
from datetime import date, datetime


# Schéma Marshmallow conforme ATARYS
class ArticlesAtarysSchema(Schema):
    id = fields.Int(dump_only=True)
    reference = fields.Str(required=True, validate=validate.Length(max=100))
    libelle = fields.Str(required=True)
    prix_achat = fields.Decimal(as_string=True)
    coefficient = fields.Decimal(as_string=True)
    prix_unitaire = fields.Decimal(as_string=True)
    unite = fields.Str(validate=validate.Length(max=20))
    tva_pct = fields.Decimal(as_string=True)
    famille = fields.Str(validate=validate.Length(max=30))
    actif = fields.Bool()
    date_import = fields.Date()
    date_maj = fields.Date()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


articles_schema = ArticlesAtarysSchema(many=True)
article_schema = ArticlesAtarysSchema()

bp = Blueprint('articles_atarys', __name__, url_prefix='/api/articles-atarys')


# GET paginé
@bp.route('/', methods=['GET'])
def get_articles():
    page = int(request.args.get('page', 1))
    per_page = request.args.get('per_page', 'all')  # 'all' pour tout
    
    query = articlesatarys.query
    total = query.count()
    
    if per_page == 'all':
        # Récupérer toutes les données sans pagination
        items = query.order_by(articlesatarys.id.desc()).all()
        data = articles_schema.dump(items)
        return jsonify({
            'success': True,
            'data': data,
            'message': f'Liste complète des articles ATARYS ({total})',
            'pagination': {
                'page': 1,
                'per_page': total,
                'total': total,
                'has_next': False
            }
        })
    else:
        # Pagination normale
        per_page = int(per_page)
        items = query.order_by(articlesatarys.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        data = articles_schema.dump(items.items)
        return jsonify({
            'success': True,
            'data': data,
            'message': f'Liste des articles ATARYS (page {page})',
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'has_next': items.has_next
            }
        })


# POST (création ou mise à jour - logique upsert)
@bp.route('/', methods=['POST'])
def create_article():
    json_data = request.get_json()
    if not json_data:
        return jsonify({
            'success': False, 
            'data': [], 
            'message': 'Aucune donnée reçue'
        }), 400
    
    # Remplissage automatique des dates si absentes (AVANT validation)
    if 'date_import' not in json_data or not json_data['date_import']:
        json_data['date_import'] = date.today()
    elif isinstance(json_data['date_import'], str):
        json_data['date_import'] = date.fromisoformat(json_data['date_import'])
    if 'date_maj' not in json_data or not json_data['date_maj']:
        json_data['date_maj'] = date.today()
    elif isinstance(json_data['date_maj'], str):
        json_data['date_maj'] = date.fromisoformat(json_data['date_maj'])
    
    errors = article_schema.validate(json_data)
    if errors:
        return jsonify({'success': False, 'data': [], 'message': errors}), 400
    
    # Logique UPSERT : vérifier si la référence existe déjà
    reference = json_data.get('reference')
    existing_article = articlesatarys.query.filter_by(reference=reference).first()
    
    if existing_article:
        # Mise à jour de l'article existant
        for key, value in json_data.items():
            if key != 'id':  # Ne pas modifier l'ID
                setattr(existing_article, key, value)
        existing_article.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({
            'success': True, 
            'data': article_schema.dump(existing_article), 
            'message': f'Article mis à jour (référence: {reference})'
        })
    else:
        # Création d'un nouvel article
        article = articlesatarys(**json_data)
        db.session.add(article)
        db.session.commit()
        return jsonify({
            'success': True, 
            'data': article_schema.dump(article), 
            'message': f'Article créé (référence: {reference})'
        })


# PUT (modification)
@bp.route('/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    article = articlesatarys.query.get_or_404(article_id)
    json_data = request.get_json()
    if not json_data:
        return jsonify({
            'success': False, 
            'data': [], 
            'message': 'Aucune donnée reçue'
        }), 400
    errors = article_schema.validate(json_data)
    if errors:
        return jsonify({'success': False, 'data': [], 'message': errors}), 400
    for key, value in json_data.items():
        setattr(article, key, value)
    db.session.commit()
    return jsonify({
        'success': True, 
        'data': article_schema.dump(article), 
        'message': 'Article modifié'
    })


# DELETE
@bp.route('/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    article = articlesatarys.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return jsonify({'success': True, 'data': [], 'message': 'Article supprimé'}) 


# DELETE ALL (clear table)
@bp.route('/clear/', methods=['DELETE', 'OPTIONS'])
def clear_articles():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        num_deleted = db.session.query(articlesatarys).delete()
        db.session.commit()
        return jsonify({
            'success': True,
            'data': [],
            'message': f'{num_deleted} articles supprimés.'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'data': [],
            'message': f'Erreur lors de la suppression : {str(e)}'
        }), 500 