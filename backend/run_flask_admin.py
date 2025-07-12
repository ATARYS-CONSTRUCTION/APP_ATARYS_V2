import os
import importlib
import sys
from app import create_app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = create_app('development')
admin = Admin(app, name='ATARYS Admin', template_mode='bootstrap4')

# Chemin absolu vers le dossier des modèles
MODELS_DIR = os.path.join(os.path.dirname(__file__), 'app', 'models')

print("🔍 Recherche des modèles ATARYS...")

# Parcourir tous les fichiers Python du dossier models
models_loaded = 0
for filename in os.listdir(MODELS_DIR):
    if filename.endswith('.py') and filename not in ('__init__.py', 'base.py'):
        module_name = f"app.models.{filename[:-3]}"
        try:
            module = importlib.import_module(module_name)
            
            # Parcourir tous les attributs du module
            for attr_name in dir(module):
                if attr_name.startswith('_'):
                    continue
                    
                obj = getattr(module, attr_name)
                
                # Vérifier si c'est une classe de modèle valide
                if (isinstance(obj, type) and 
                    hasattr(obj, '__tablename__') and 
                    obj.__module__ == module.__name__ and
                    obj.__name__ != "BaseModel" and 
                    not getattr(obj, '__abstract__', False)):
                    
                    try:
                        admin.add_view(ModelView(obj, db.session))
                        print(f"✅ Modèle ajouté : {obj.__name__} (table: {obj.__tablename__})")
                        models_loaded += 1
                    except Exception as view_error:
                        print(f"⚠️  Erreur ajout vue {obj.__name__} : {view_error}")
                        
        except ImportError as import_error:
            print(f"❌ Erreur import {module_name} : {import_error}")
        except Exception as e:
            print(f"❌ Erreur générale {module_name} : {e}")

print(f"\n🎉 Flask-Admin prêt avec {models_loaded} modèle(s)")
print(f"🌐 Interface disponible sur : http://localhost:5001/admin")

if __name__ == "__main__":
    if models_loaded == 0:
        print("\n⚠️  Aucun modèle trouvé. Vérifiez que :")
        print("   - Les tables existent dans atarys_data.db")
        print("   - Les modèles SQLAlchemy sont générés")
        print("   - Les fichiers sont dans app/models/")
        print("\n💡 Utilisez generate_complete_model.py pour générer les modèles")
    
    app.run(port=5001, debug=True) 