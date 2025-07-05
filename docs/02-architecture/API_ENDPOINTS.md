# 🛣️ API Endpoints ATARYS V2

> **Spécifications techniques des routes API REST**  
> **VERSION 2** : Backend Flask + SQLAlchemy à créer  
> Dernière mise à jour : 05/07/2025

---

## 📋 Vue d'ensemble

**Base URL :** `http://localhost:5000/api` (à créer)
**Format de réponse :** JSON standardisé `{success, data, message}`
**Stack Backend :** Flask 2.3+ + SQLAlchemy 2.0+ + SQLite
**Organisation :** APIs structurées par modules ATARYS prioritaires

---

## 🏗️ Stack Technique Backend

### **Framework et ORM**
```python
# Flask Factory Pattern
from flask import Flask
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

### **Modèles SQLAlchemy**
```python
# Pattern BaseModel pour tous les modèles
class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
```

### **Configuration Base de Données**
```python
# backend/app/config/config.py
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # postgresql://user:pass@host:5432/atarys_v2
```

---

## 🎯 Modules Prioritaires V2

### **🔄 À CRÉER EN PRIORITÉ**

#### **Module 3.1 - LISTE CHANTIERS** (PRIORITÉ 1)
**Objectif :** Remplacer "LISTE DES TACHES" + "Liste_Chantiers" Excel
**Modèles :** À créer selon `DATABASE_SCHEMA.md`
**Relations :** À définir lors de la création des modèles

```python
# Endpoints Module 3.1 (à créer)
GET    /api/chantiers                 # Liste paginée
POST   /api/chantiers                 # Créer chantier
GET    /api/chantiers/<id>            # Détails chantier
PUT    /api/chantiers/<id>            # Modifier chantier
DELETE /api/chantiers/<id>            # Supprimer chantier
GET    /api/chantiers/search          # Recherche textuelle
```

#### **Module 9.1 - LISTE SALARIÉS** (PRIORITÉ 2)
**Objectif :** Gestion des salariés de l'entreprise
**Modèles :** À créer selon `DATABASE_SCHEMA.md`
**Relations :** À définir lors de la création des modèles

```python
# Endpoints Module 9.1 (à créer)
GET    /api/salaries          # Liste des salariés
POST   /api/salaries          # Créer salarié
GET    /api/salaries/<id>     # Détails salarié
PUT    /api/salaries/<id>     # Modifier salarié
DELETE /api/salaries/<id>     # Supprimer salarié
```

#### **Module 10.1 - CALCUL ARDOISES** (PRIORITÉ 3)
**Objectif :** Calculateur d'ardoises selon zones climatiques
**Modèles :** À créer selon `DATABASE_SCHEMA.md`
**Relations :** À définir lors de la création des modèles

```python
# Endpoints Module 10.1 (à créer)
GET    /api/ardoises/modeles           # Modèles d'ardoises
GET    /api/ardoises/modeles/<id>      # Détails modèle
POST   /api/ardoises/calcul            # Calculer besoins
GET    /api/ardoises/zones             # Zones climatiques
```

---

## 📊 Format de Réponse Standard

### **Succès avec données**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nom": "Exemple d'enregistrement",
      "description": "Description de l'élément",
      "created_at": "2025-07-05T10:00:00Z",
      "updated_at": "2025-07-05T10:00:00Z"
    }
  ],
  "message": "Données récupérées avec succès",
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total": 25,
    "pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

### **Erreur**
```json
{
  "success": false,
  "error": "Ressource non trouvée",
  "code": 404
}
```

---

## 🔧 Spécifications Techniques

### **Pagination Obligatoire**
```python
# Implémentation standard
@lru_cache(maxsize=128)
def get_paginated_results(query, page=1, per_page=50):
    return query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
```

### **Validation des Données**
```python
# Validation automatique avec SQLAlchemy
from marshmallow import Schema, fields, validate

class ExampleSchema(Schema):
    nom = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(allow_none=True)
    # Autres champs selon les modèles créés
```

### **Gestion des Erreurs**
```python
# Middleware centralisé
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Ressource non trouvée",
        "code": 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({
        "success": False,
        "error": "Erreur interne du serveur",
        "code": 500
    }), 500
```

---

## 🚀 Structure Backend à Créer

### **Organisation des Fichiers**
```
backend/
├── app/
│   ├── __init__.py              # Factory Flask
│   ├── models/
│   │   ├── __init__.py
│   │   ├── module_3_1.py        # Modèles Module 3.1 (à créer)
│   │   ├── module_9_1.py        # Modèles Module 9.1 (à créer)
│   │   └── module_10_1.py       # Modèles Module 10.1 (à créer)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── chantiers.py         # Blueprint Module 3.1
│   │   ├── salaries.py          # Blueprint Module 9.1
│   │   └── ardoises.py          # Blueprint Module 10.1
│   ├── services/
│   │   ├── chantier_service.py  # Logique métier Module 3.1
│   │   ├── salarie_service.py   # Logique métier Module 9.1
│   │   └── ardoise_service.py   # Logique métier Module 10.1
│   └── config/
│       └── config.py            # Configuration par environnement
├── migrations/                  # Flask-Migrate
├── scripts/                     # Import Excel → SQLite V2
├── requirements.txt             # Dépendances Python
└── run.py                       # Serveur principal
```

### **Dépendances Python**
```python
# requirements.txt
Flask>=2.3.0
SQLAlchemy>=2.0.0
Flask-SQLAlchemy>=3.0.0
Flask-Migrate>=4.0.0
Flask-CORS>=4.0.0
marshmallow>=3.19.0
pandas>=1.5.0
openpyxl>=3.0.0
pytest>=7.0.0
```

---

## 🎯 Prochaines Étapes

### **Phase 1 : Créer Backend (1-2 semaines)**
1. **Structure Flask** : Factory pattern + configuration
2. **Modèles SQLAlchemy** : 3 modules prioritaires
3. **APIs REST** : Endpoints selon spécifications
4. **Base SQLite V2** : Import depuis Excel propre
5. **Tests unitaires** : Validation des APIs

### **Phase 2 : Intégration Frontend (1 semaine)**
1. **Services API** : Connexion React ↔ Flask
2. **Interfaces utilisateur** : Modules 3.1, 9.1, 10.1
3. **Tests d'intégration** : Workflow complet
4. **Optimisation** : Performance et UX

### **Phase 3 : Modules Additionnels (2-3 semaines)**
1. **Module 1.1/1.2** : Planning
2. **Module 5.3** : Devis MEXT
3. **Module 7.1/7.2** : Tableaux de bord
4. **Modules restants** : Selon priorités métier

---

## ⚠️ Notes Importantes

### **Cohérence avec V1**
- **Référence technique** : `0 APP ATARYS/` conservé pour logique métier
- **Pas de migration** : Création propre V2 depuis Excel à jour
- **Standards V2** : SQLAlchemy 2.0 + `db.Numeric(10, 2)` pour montants

### **Optimisations Prévues**
- **Index BDD** : Sur colonnes critiques (référence, état, dates)
- **Cache** : Données statiques (villes, états, modèles)
- **Pagination** : Obligatoire pour toutes les listes
- **Validation** : Marshmallow + contraintes SQLAlchemy

### **Évolutivité**
- **PostgreSQL** : Migration prévue pour production
- **Authentification** : JWT à implémenter
- **Monitoring** : Logs centralisés + métriques
- **Scaling** : Architecture modulaire extensible 