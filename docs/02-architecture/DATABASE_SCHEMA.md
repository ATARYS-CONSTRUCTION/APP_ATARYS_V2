# 🗄️ Schéma Base de Données ATARYS V2

> **Structure technique complète des tables SQLite organisée par Modules ATARYS**  
> Architecture SQLAlchemy + Flask-Admin + Organisation modulaire  
> **VERSION 2** : Base propre créée depuis Excel à jour  
> Dernière mise à jour : 05/07/2025

---

## 📋 Vue d'ensemble

Base de données SQLite V2 : `data/atarys_v2.db` (à créer)
- **Structure modulaire** : Selon `ATARYS_MODULES.md`
- **Source données** : Fichier Excel propre et à jour
- **Approche V2** : Création propre, pas de migration V1
- **Relations** : Clés étrangères et contraintes à définir
- **Index** : Optimisation des performances
- **ORM** : SQLAlchemy 2.0+ pour l'abstraction
- **Admin** : Flask-Admin organisé par modules

---

## 🏗️ Architecture Technique

### Stack Technologique
- **Base de données** : SQLite 3
- **ORM** : SQLAlchemy 2.0+
- **Framework Web** : Flask 3.x
- **Interface Admin** : Flask-Admin
- **Frontend** : React + Vite
- **API** : RESTful avec blueprints

### Structure de l'Application V2 (à créer)
```
backend/                 # À CRÉER
├── app/
│   ├── models/          # Modèles SQLAlchemy selon modules ATARYS
│   ├── services/        # Logique métier par module
│   ├── routes/          # API endpoints par module
│   ├── middleware/      # Middleware (logging, errors)
│   └── config/          # Configuration
├── admin_atarys.py      # Interface Flask-Admin
├── run.py              # Serveur principal
├── migrations/          # Flask-Migrate
└── scripts/            # Scripts d'import Excel → SQLite V2
```

### Configuration SQLAlchemy
```python
# backend/app/__init__.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    return app
```

---

## 🔢 Types de Données Numériques

### **Standard V2 pour les Montants Financiers**

Pour les montants financiers, utiliser `NUMERIC` avec précision fixe :

```python
# Standard ATARYS V2
montant_ht = db.Column(db.Numeric(10, 2), nullable=True, default=0.00)
# 10 chiffres total, 2 décimales (ex: 12345678.90)
```

**Avantages NUMERIC :**
- ✅ Précision exacte pour les calculs financiers
- ✅ Pas d'erreurs d'arrondi
- ✅ Validation stricte des données
- ✅ Conformité comptable

**Implémentation V2 :**
1. Utiliser `db.Numeric(10, 2)` pour tous les montants dès la création
2. Garder `db.Float` pour les mesures techniques (longueurs, angles)
3. Appliquer les validations dès la conception

---

## 🏗️ Pattern BaseModel Standard

### **Modèle de Base pour Tous les Modèles**

```python
# backend/app/models/base.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        """Sauvegarder l'objet en base"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Supprimer l'objet de la base"""
        db.session.delete(self)
        db.session.commit()
        return self
    
    def to_dict(self):
        """Convertir l'objet en dictionnaire"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"
```

### **Utilisation dans les Modèles**

```python
# backend/app/models/module_3_1.py
from .base import BaseModel

class ExampleModel(BaseModel):
    __tablename__ = 'example_table'
    
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    montant_ht = db.Column(db.Numeric(10, 2), default=0.00)
    
    def __repr__(self):
        return f"<ExampleModel {self.nom}>"
```

---

## 📊 Organisation par Modules ATARYS

### **Modules Prioritaires V2**

#### **Module 3.1 - LISTE CHANTIERS** (PRIORITÉ 1)
- **Objectif** : Remplacer "LISTE DES TACHES" + "Liste_Chantiers" Excel
- **Tables** : À créer selon besoins métier
- **Modèles** : À développer avec BaseModel

#### **Module 9.1 - LISTE SALARIÉS** (PRIORITÉ 2)
- **Objectif** : Gestion des salariés de l'entreprise
- **Tables** : À créer selon besoins RH
- **Modèles** : À développer avec BaseModel

#### **Module 10.1 - CALCUL ARDOISES** (PRIORITÉ 3)
- **Objectif** : Calculateur d'ardoises selon zones climatiques
- **Tables** : À créer selon besoins techniques
- **Modèles** : À développer avec BaseModel

---

## 🎛️ Flask-Admin Configuration

### **Configuration Générale**
```python
# backend/admin_atarys.py
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

def create_admin(app, db):
    admin = Admin(app, name='ATARYS Admin V2', template_mode='bootstrap4')
    
    # Les vues seront ajoutées au fur et à mesure du développement
    # selon les modules ATARYS créés
    
    return admin
```

### **Avantages de cette approche :**
- **Navigation intuitive** par module
- **Cohérence** avec l'architecture ATARYS
- **Maintenance facilitée** des données
- **Formation utilisateur** simplifiée

---

## 🔧 Scripts d'Import Excel → SQLite V2

### **Structure des Scripts**
```
backend/scripts/
├── import_excel_v2.py      # Script principal d'import
├── validators.py           # Validation des données
├── transformers.py         # Transformation des données
└── utils.py               # Utilitaires communs
```

### **Exemple de Script d'Import**
```python
# backend/scripts/import_excel_v2.py
import pandas as pd
from sqlalchemy import create_engine
from app import create_app, db

def import_from_excel(excel_file_path, table_name):
    """
    Importer des données Excel vers SQLite V2
    
    Args:
        excel_file_path (str): Chemin vers le fichier Excel
        table_name (str): Nom de la table de destination
    """
    app = create_app('development')
    
    with app.app_context():
        # Lecture du fichier Excel
        df = pd.read_excel(excel_file_path)
        
        # Validation des données
        # À implémenter selon les besoins
        
        # Import vers SQLite
        df.to_sql(table_name, db.engine, if_exists='append', index=False)
        
        print(f"Import terminé : {len(df)} enregistrements dans {table_name}")

if __name__ == '__main__':
    # Exemple d'utilisation
    import_from_excel('data/excel_propre.xlsx', 'example_table')
```

---

## 🚀 Prochaines Étapes

### **Phase 1 : Création Backend (1-2 semaines)**
1. **Structure Flask** : Factory pattern + configuration
2. **BaseModel** : Modèle de base avec méthodes communes
3. **Modèles prioritaires** : Modules 3.1, 9.1, 10.1
4. **Flask-Admin** : Interface d'administration
5. **Scripts d'import** : Excel → SQLite V2

### **Phase 2 : Intégration (1 semaine)**
1. **APIs REST** : Endpoints selon modules
2. **Validation** : Marshmallow + contraintes SQLAlchemy
3. **Tests** : Tests unitaires des modèles
4. **Documentation** : Mise à jour selon développement

### **Phase 3 : Optimisation (1 semaine)**
1. **Index** : Optimisation des performances
2. **Relations** : Clés étrangères et contraintes
3. **Migration** : Flask-Migrate pour évolution
4. **Monitoring** : Logs et métriques

---

## ⚠️ Notes Importantes

### **Cohérence avec V1**
- **Référence technique** : `0 APP ATARYS/` conservé pour logique métier
- **Pas de migration** : Création propre V2 depuis Excel à jour
- **Standards V2** : SQLAlchemy 2.0 + `db.Numeric(10, 2)` pour montants

### **Évolutivité**
- **PostgreSQL** : Migration prévue pour production
- **Authentification** : JWT à implémenter
- **Scaling** : Architecture modulaire extensible
- **Maintenance** : Flask-Admin pour gestion des données

---

**✅ Base de données ATARYS V2 - Architecture modulaire prête pour le développement !** 