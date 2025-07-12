from app import create_app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models.module_5_1 import articlesatarys
# Exemple d'import d'un autre module (à adapter selon les modèles réels)
# from app.models.module_3_1 import chantier

app = create_app('development')

# Configuration Flask-Admin
admin = Admin(app, name='ATARYS Admin', template_mode='bootstrap4')

# Dictionnaire pour forcer l'ordre des modules (clé = numéro, valeur = nom complet)
MODULES_ORDER = [
    (3, "3. Liste Chantiers"),
    (5, "5. Devis-Facturation"),
    # Ajouter ici les autres modules dans l'ordre souhaité
]

# Vue personnalisée pour forcer l'affichage de la colonne id
class ArticlesAtarysAdmin(ModelView):
    column_list = ('id', 'reference', 'libelle', 'prix_achat', 'coefficient', 'prix_unitaire', 'unite', 'tva_pct', 'famille', 'actif', 'date_import', 'date_maj')

# Ajout des vues par module (exemple)
# admin.add_view(ModelView(chantier, db.session, name="Chantiers", category="3. Liste Chantiers"))
admin.add_view(ArticlesAtarysAdmin(articlesatarys, db.session, name="Articles ATARYS", category="5. Devis-Facturation"))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 