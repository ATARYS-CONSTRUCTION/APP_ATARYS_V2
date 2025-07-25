# 🛣️ API Endpoints ATARYS V2

> **Spécifications techniques des routes API REST**  
> **VERSION 2** : Backend Flask + SQLAlchemy opérationnel  
> Dernière mise à jour : 19/07/2025

---

## 📋 Vue d'ensemble

**Base URL :** `http://localhost:5000/api` (OPÉRATIONNEL)
**Format de réponse :** JSON standardisé `{success, data, message}`
**Stack Backend :** Flask 3.x + SQLAlchemy 2.0+ + SQLite
**Organisation :** APIs structurées par modules ATARYS

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

### **Module 12 - Gestion Dynamique des Tables** (OPÉRATIONNEL)

#### **Base URL :** `/api/module-12/`

#### **1. POST - Création de Table**
```http
POST /api/module-12/create-table
```

**Payload :**
```json
{
  "module_atarys": 3,
  "nom_table": "chantiers",
  "colonnes": [
    {
      "nom": "nom_chantier",
      "type": "String",
      "longueur": 200,
      "nullable": false
    },
    {
      "nom": "budget",
      "type": "Numeric",
      "precision": "10,2"
    }
  ]
}
```

**Réponse :**
```json
{
  "success": true,
  "message": "✅ Code généré pour 'chantiers'. Lancez maintenant les migrations :",
  "data": {
    "table_name": "chantiers",
    "module": 3,
    "files_generated": [
      "backend/app/models/module_3.py",
      "backend/app/routes/module_3.py"
    ],
    "migration_commands": [
      "flask db migrate -m 'Add chantiers table'",
      "flask db upgrade"
    ]
  }
}
```

---

## 🔄 **APIs en Développement**

### **Module 5 - DEVIS_FACTURATION** (EN COURS)

#### **Base URL :** `/api/module-5/`

#### **1. GET - Familles d'Ouvrages**
```http
GET /api/module-5/familles-ouvrages
```

**Réponse (à implémenter) :**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "num_bd_atarys": "FAM001",
      "libelle": "Charpente",
      "created_at": "2025-07-19T12:00:00Z",
      "updated_at": "2025-07-19T12:00:00Z"
    }
  ],
  "message": "Familles d'ouvrages récupérées avec succès"
}
```

#### **2. POST - Création Famille d'Ouvrages**
```http
POST /api/module-5/familles-ouvrages
```

**Payload (à implémenter) :**
```json
{
  "num_bd_atarys": "FAM002",
  "libelle": "Couverture"
}
```

---

## 📋 **APIs à Implémenter par Module**

### **Module 1 - PLANNING**
```http
GET    /api/module-1/planning-salaries     # Planning des salariés
POST   /api/module-1/planning-salaries     # Création planning
PUT    /api/module-1/planning-salaries/:id # Modification
DELETE /api/module-1/planning-salaries/:id # Suppression
```

### **Module 3 - LISTE CHANTIERS**
```http
GET    /api/module-3/chantiers              # Liste paginée
POST   /api/module-3/chantiers              # Création chantier
PUT    /api/module-3/chantiers/:id          # Modification
DELETE /api/module-3/chantiers/:id          # Suppression
GET    /api/module-3/chantiers/:id/devis    # Devis du chantier
```

### **Module 6 - CLIENTS**
```http
GET    /api/module-6/clients                # Liste clients
POST   /api/module-6/clients                # Création client
PUT    /api/module-6/clients/:id            # Modification
DELETE /api/module-6/clients/:id            # Suppression
GET    /api/module-6/clients/:id/chantiers  # Chantiers du client
```

### **Module 9 - LISTE_SALARIÉS**
```http
GET    /api/module-9/salaries               # Liste salariés
POST   /api/module-9/salaries               # Création salarié
PUT    /api/module-9/salaries/:id           # Modification
DELETE /api/module-9/salaries/:id           # Suppression
GET    /api/module-9/qualifications         # Niveaux qualification

# Villes (relation avec salaries)
GET    /api/villes/                         # Liste complète des villes
GET    /api/villes/search?code_postal=35000 # Recherche par code postal
GET    /api/villes/search?ville=rennes      # Recherche par nom de ville
GET    /api/villes/1                        # Détails d'une ville
```

---

## 🎯 **Standards API REST**

### **Format de Réponse Standardisé**
```json
{
  "success": boolean,
  "data": object|array|null,
  "message": string,
  "pagination": {
    "page": number,
    "per_page": number,
    "total": number,
    "pages": number
  }
}
```

### **Codes de Statut HTTP**
- **200** : Succès (GET, PUT)
- **201** : Créé (POST)
- **204** : Supprimé (DELETE)
- **400** : Erreur de validation
- **404** : Ressource non trouvée
- **500** : Erreur serveur

### **Pagination**
```http
GET /api/module-X/resource?page=1&per_page=20&sort=created_at&order=desc
```

### **Filtrage**
```http
GET /api/module-3/chantiers?statut=EN_COURS&client_id=5
```

---

## 🔒 **Sécurité et Validation**

### **Validation Marshmallow**
```python
# Exemple de schéma de validation
class FamilleOuvragesSchema(ma.Schema):
    class Meta:
        model = FamilleOuvrages
        load_instance = True
    
    num_bd_atarys = fields.Str(required=False, validate=Length(max=10))
    libelle = fields.Str(required=True, validate=Length(min=1, max=100))
```

### **Gestion des Erreurs**
```python
# Format d'erreur standardisé
{
  "success": false,
  "data": null,
  "message": "Erreur de validation",
  "errors": {
    "libelle": ["Ce champ est obligatoire"]
  }
}
```

---

## 🔗 **Documentation Complémentaire**

- **[DATABASE_SCHEMA.md](../01-database/DATABASE_SCHEMA.md)** - Structure des tables
- **[STANDARDS_DEV.md](../../03-regles-standards/STANDARDS_DEV.md)** - Standards techniques
- **[Modules Documentation](../03-modules/)** - Documentation par module
