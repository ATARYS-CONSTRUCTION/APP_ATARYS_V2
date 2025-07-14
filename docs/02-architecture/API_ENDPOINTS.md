# 🛣️ API Endpoints ATARYS V2

> **Spécifications techniques des routes API REST**  
> **VERSION 2** : Backend Flask + SQLAlchemy opérationnel  
> Dernière mise à jour : 05/07/2025

---

## 📋 Vue d'ensemble

**Base URL :** `http://localhost:5000/api` (OPÉRATIONNEL)
**Format de réponse :** JSON standardisé `{success, data, message}`
**Stack Backend :** Flask 3.x + SQLAlchemy 2.0+ + SQLite
**Organisation :** APIs structurées par modules ATARYS prioritaires

---

## 🏗️ Stack Technique Backend

### **Framework et ORM**
```python
# Flask Factory Pattern - OPÉRATIONNEL
from flask import Flask
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

### **Pattern BaseModel Standard**
```python
# backend/app/models/base.py - OPÉRATIONNEL
class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
```

---

## ✅ **APIs Implémentées**

### **Module 5.1 - Articles ATARYS** (OPÉRATIONNEL)

#### **Base URL :** `/api/articles-atarys/`

#### **1. GET - Récupération des Articles**
```http
GET /api/articles-atarys/?per_page=all
```

**Réponse :**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "reference": "ART001",
      "libelle": "Article exemple",
      "prix_achat": "10.50",
      "coefficient": "1.20",
      "prix_unitaire": "12.60",
      "unite": "U",
      "tva_pct": "20.00",
      "famille": "Général",
      "actif": true,
      "date_import": "2025-07-05",
      "date_maj": "2025-07-05",
      "created_at": "2025-07-05T10:00:00Z",
      "updated_at": "2025-07-05T10:00:00Z"
    }
  ],
  "message": "Liste complète des articles ATARYS (176)",
  "pagination": {
    "page": 1,
    "per_page": 176,
    "total": 176,
    "has_next": false
  }
}
```

#### **2. POST - Création/Mise à jour (UPSERT)**
```http
POST /api/articles-atarys/
Content-Type: application/json

{
  "reference": "ART002",
  "libelle": "Nouvel article",
  "prix_achat": "15.00",
  "coefficient": "1.15",
  "prix_unitaire": "17.25",
  "unite": "U",
  "tva_pct": "20.00",
  "famille": "Général",
  "actif": true
}
```

**Logique UPSERT :**
- Si référence existe → Mise à jour
- Si référence n'existe pas → Création
- Dates automatiques si absentes

#### **3. PUT - Modification par ID**
```http
PUT /api/articles-atarys/1
Content-Type: application/json

{
  "libelle": "Article modifié",
  "prix_unitaire": "18.00"
}
```

#### **4. DELETE - Suppression par ID**
```http
DELETE /api/articles-atarys/1
```

#### **5. DELETE - Suppression de toutes les données**
```http
DELETE /api/articles-atarys/clear/
```

### **Module 12.1 - Création Dynamique de Tables** (OPÉRATIONNEL)

#### **Base URL :** `/api/create-table/`

#### **POST - Création de Table**
```http
POST /api/create-table/
Content-Type: application/json

{
  "tableData": {
    "moduleId": 12,
    "className": "ExampleModel",
    "tableName": "example_table",
    "columns": [
      {
        "name": "nom",
        "type": "String",
        "nullable": false,
        "maxLength": "100"
      },
      {
        "name": "prix_ht",
        "type": "Numeric",
        "nullable": true,
        "default": "0.00"
      }
    ]
  },
  "code": "from .base import BaseModel\nfrom app import db\n\nclass ExampleModel(BaseModel):\n    __tablename__ = 'example_table'\n    \n    id = db.Column(db.Integer, primary_key=True, autoincrement=True)\n    nom = db.Column(db.String(100), nullable=False)\n    prix_ht = db.Column(db.Numeric(10, 2), default=0.00)\n"
}
```

**Actions automatiques :**
1. Validation des données
2. Création du fichier modèle
3. Création de la table SQLite
4. Intégration dans l’API REST

---

## 🎯 **Modules Prioritaires à Implémenter**

### **Module 3.1 - LISTE CHANTIERS** (PRIORITÉ 1)
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

### **Module 9.1 - LISTE SALARIÉS** (PRIORITÉ 2)
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

### **Module 10.1 - CALCUL ARDOISES** (PRIORITÉ 3)
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

### **Validation Marshmallow** (OPÉRATIONNEL)
```python
# Exemple pour articles_atarys
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
```

### **Pagination Intelligente**
```python
# Support pour 'all' et pagination normale
per_page = request.args.get('per_page', 'all')

if per_page == 'all':
    # Récupérer toutes les données
    items = query.order_by(Model.id.desc()).all()
else:
    # Pagination normale
    per_page = int(per_page)
    items = query.paginate(page=page, per_page=per_page, error_out=False)
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

### **CORS Configuration**
```python
# Communication frontend-backend
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Autorise toutes les origines en développement
```

---

## 🚀 **Métriques et Performance**

### **APIs Opérationnelles**
- **Articles ATARYS** : 176 lignes, < 100ms response time
- **Création Tables** : Génération automatique, intégration immédiate
- **Validation** : Marshmallow pour intégrité des données
- **CORS** : Configuré pour communication frontend-backend

### **Standards de Performance**
- **Response time** : < 2s pour toutes les APIs
- **Validation** : Marshmallow pour intégrité
- **Rollback** : En cas d'erreur SQLAlchemy
- **Logging** : Logs structurés pour debugging

---

## 📚 **Documentation Associée**

### **Architecture**
- **[ATARYS_ARCHITECTURE.md](ATARYS_ARCHITECTURE.md)** - Architecture complète V2
- **[DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)** - Schéma base de données
- **[ATARYS_MODULES.md](ATARYS_MODULES.md)** - Organisation modulaire

### **Développement**
- **[WORKFLOWS.md](../03-regles-standards/WORKFLOWS.md)** - Processus de développement
- **[STANDARDS_DEV.md](../03-regles-standards/STANDARDS_DEV.md)** - Standards techniques

---

**✅ APIs ATARYS V2 - Backend opérationnel avec modules prioritaires en cours !** 