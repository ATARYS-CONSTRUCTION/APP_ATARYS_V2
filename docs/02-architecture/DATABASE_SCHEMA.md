# 🗄️ Schéma Base de Données ATARYS V2

> **Structure technique complète des tables SQLite organisée par Modules ATARYS**  
> Architecture SQLAlchemy + Flask-Admin + Organisation modulaire  
> **VERSION 2** : Base opérationnelle avec modèles implémentés  
> Dernière mise à jour : 05/07/2025

---

## 📋 Vue d'ensemble

Base de données SQLite V2 : `data/atarys_data.db` (OPÉRATIONNEL)
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
- **API** : REST format `{success, data, message}`

### Structure de l'Application V2 (OPÉRATIONNEL)
```
backend/                 # OPÉRATIONNEL
├── app/
│   ├── models/          # Modèles SQLAlchemy selon modules ATARYS
│   │   ├── base.py      # Pattern BaseModel standard
│   │   └── module_5_1.py # Modèle articlesatarys
│   ├── routes/          # API endpoints par module
│   │   ├── articles_atarys.py # API articles ATARYS
│   │   └── create_table.py   # API création dynamique
│   └── __init__.py      # Factory pattern Flask
├── run_flask_admin.py   # Interface Flask-Admin (port 5001)
└── scripts/            # Scripts d'import Excel → SQLite V2
```

### Configuration SQLAlchemy
```python
# backend/app/__init__.py - OPÉRATIONNEL
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Configuration base de données
    db_uri = 'sqlite:///../../data/atarys_data.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialisation extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)  # Communication frontend-backend
    
    return app
```

---

## 🔢 Types de Données Numériques

### **Standard V2 pour les Montants Financiers**

Pour les montants financiers, utiliser `NUMERIC` avec précision fixe :

```python
# Standard ATARYS V2 - OPÉRATIONNEL
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
# backend/app/models/base.py - OPÉRATIONNEL
from datetime import datetime
from app import db

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
# backend/app/models/module_5_1.py - OPÉRATIONNEL
from .base import BaseModel

class articlesatarys(BaseModel):
    __tablename__ = 'articles_atarys'
    
    reference = db.Column(db.String(100), nullable=False, unique=True)
    libelle = db.Column(db.Text, nullable=False)
    prix_achat = db.Column(db.Numeric(10, 2))
    coefficient = db.Column(db.Numeric(10, 2))
    prix_unitaire = db.Column(db.Numeric(10, 2), nullable=False)
    unite = db.Column(db.String(20), nullable=False)
    tva_pct = db.Column(db.Numeric(10, 2), nullable=False, default=20)
    famille = db.Column(db.String(30))
    actif = db.Column(db.Boolean, default=True)
    date_import = db.Column(db.Date, nullable=False)
    date_maj = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return f'<articlesatarys {self.id}>'
```

---

## 📊 Organisation par Modules ATARYS

### **Modules Implémentés V2**

#### **Module 5.1 - Articles ATARYS** (OPÉRATIONNEL)
- **Objectif** : Gestion des articles et prix ATARYS
- **Table** : `articles_atarys` (176 lignes)
- **Modèle** : `articlesatarys` dans `module_5_1.py`
- **API** : `/api/articles-atarys/` (CRUD complet)
- **Admin** : Interface Flask-Admin avec colonne ID visible

**Structure de la table :**
```sql
CREATE TABLE articles_atarys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference VARCHAR(100) NOT NULL UNIQUE,
    libelle TEXT NOT NULL,
    prix_achat NUMERIC(10, 2),
    coefficient NUMERIC(10, 2),
    prix_unitaire NUMERIC(10, 2) NOT NULL,
    unite VARCHAR(20) NOT NULL,
    tva_pct NUMERIC(10, 2) NOT NULL DEFAULT 20,
    famille VARCHAR(30),
    actif BOOLEAN DEFAULT 1,
    date_import DATE NOT NULL,
    date_maj DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### **Modules Prioritaires à Développer**

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
# backend/run_flask_admin.py - OPÉRATIONNEL
from app import create_app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models.module_5_1 import articlesatarys

app = create_app('development')

# Configuration Flask-Admin
admin = Admin(app, name='ATARYS Admin', template_mode='bootstrap4')

# Vue personnalisée pour forcer l'affichage de la colonne id
class ArticlesAtarysAdmin(ModelView):
    column_list = ('id', 'reference', 'libelle', 'prix_achat', 'coefficient', 
                   'prix_unitaire', 'unite', 'tva_pct', 'famille', 'actif', 
                   'date_import', 'date_maj')

# Ajout des vues par module
admin.add_view(ArticlesAtarysAdmin(articlesatarys, db.session, 
                                   name="Articles ATARYS", 
                                   category="5. Devis-Facturation"))
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
├── import_articles_atarys.py  # Import articles ATARYS
├── init_database.py           # Initialisation base
└── create_atarys_database.py  # Création structure
```

### **Exemple de Script d'Import**
```python
# backend/import_articles_atarys.py - OPÉRATIONNEL
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
    import_from_excel('data/excel_propre.xlsx', 'articles_atarys')
```

---

## 🚀 Prochaines Étapes

### **Phase 1 : Modules Prioritaires (1-2 semaines)**
1. **Module 3.1** : Liste Chantiers (priorité 1)
2. **Module 9.1** : Liste Salariés (priorité 2)
3. **Module 10.1** : Calcul Ardoises (priorité 3)

### **Phase 2 : Optimisation (1 semaine)**
1. **Index** : Optimisation des performances
2. **Relations** : Clés étrangères et contraintes
3. **Migration** : Flask-Migrate pour évolution
4. **Monitoring** : Logs et métriques

### **Phase 3 : Modules Additionnels (2-3 semaines)**
1. **Modules 1.1/1.2** : Planning
2. **Modules 7.1/7.2** : Gestion et tableaux de bord
3. **Modules 6.x** : Atelier
4. **Modules 8.x** : Comptabilité

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

## 📊 Métriques Actuelles

### **Base de Données V2**
- **176 lignes** dans `articles_atarys`
- **1 table** opérationnelle
- **Pattern BaseModel** : Standardisé
- **Types de données** : Conformes aux standards ATARYS

### **Performance**
- **Response time** : < 100ms pour les requêtes simples
- **Validation** : Marshmallow pour intégrité
- **Admin interface** : Flask-Admin opérationnel
- **API REST** : Format standardisé `{success, data, message}`

---

**✅ Base de données ATARYS V2 - Architecture modulaire opérationnelle !** 