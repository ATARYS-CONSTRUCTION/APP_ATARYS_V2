# 🔧 Standards de Développement ATARYS V2

> **Standards techniques et conventions de développement**  
> **VERSION 2** : Standards opérationnels avec architecture moderne  
> Dernière mise à jour : 05/07/2025

---

## 🏗️ **Stack Technologique V2**

### **Backend - Python/Flask**
- **Framework** : Flask 3.x avec pattern Factory (`create_app()`)
- **ORM** : SQLAlchemy 2.0+ avec BaseModel pattern
- **Base de données** : SQLite avec BaseModel pattern
- **API** : REST avec format JSON standardisé `{success, data, message}`
- **Admin** : API REST sur port 5000
- **CORS** : Configuré pour communication frontend-backend
- **Validation** : Marshmallow pour intégrité des données
- **Dépendances clés** :
  ```python
  Flask + SQLAlchemy + Flask-CORS + Flask-Migrate + Marshmallow
  ```

### **Frontend - React/Vite**
- **Framework UI** : React 18.2.0 avec hooks modernes
- **Build Tool** : Vite 5.4.19 (Hot Module Replacement ultra-rapide)
- **Styling** : Tailwind CSS 3.4.1
- **HTTP Client** : Fetch API native
- **État global** : Context API + hooks personnalisés

---

## 📁 **Organisation des Fichiers**

### **Structure Opérationnelle**
```
backend/                 # OPÉRATIONNEL
├── app/
│   ├── models/          # SQLAlchemy ORM avec BaseModel
│   │   ├── base.py      # Pattern BaseModel standard
│   │   └── module_5_1.py # Modèle articlesatarys
│   ├── routes/          # Blueprints Flask (APIs REST)
│   │   ├── articles_atarys.py # API articles ATARYS
│   │   └── create_table.py   # API création dynamique
│   └── __init__.py      # Factory pattern Flask
├── run_flask_admin.py   # Interface admin (port 5001)
└── requirements/        # Dépendances par environnement

frontend/src/
├── pages/              # Pages selon modules ATARYS
│   ├── BaseDeDonnees.jsx    # Module 12.1 (opérationnel)
│   ├── PlanningSalaries.jsx # Module 1.1 (opérationnel)
│   └── CalculArdoises.jsx   # Module 10.1 (en cours)
├── components/         # Composants réutilisables
│   ├── AddRowForm.jsx       # Formulaire dynamique
│   ├── CreateTableForm.jsx  # Création tables
│   └── Layout.jsx           # Composants layout
└── api/               # Services API centralisés

data/
└── atarys_data.db     # Base SQLite V2 (176 lignes articles)
```

---

## 🗄️ **Standards Base de Données**

### **Pattern BaseModel Standard**
```python
# backend/app/models/base.py - OBLIGATOIRE
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

### **Types de Données Standards ATARYS**
- **Montants financiers** : `db.Numeric(10, 2)` OBLIGATOIRE
- **Textes courts** : `db.String(longueur_max)` avec limite
- **Textes longs** : `db.Text` pour descriptions
- **Dates** : `db.DateTime` avec `default=datetime.utcnow`
- **Booléens** : `db.Boolean` avec `default=True/False`

### **Exemple de Modèle Conforme**
```python
# backend/app/models/module_5_1.py
from .base import BaseModel
from app import db

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

## 🔌 **Standards API REST**

### **Format de Réponse Standardisé**
```json
{
  "success": true,
  "data": [...],
  "message": "Opération réussie",
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total": 100,
    "has_next": true
  }
}
```

### **Structure de Route Standard**
```python
# backend/app/routes/articles_atarys.py
from flask import Blueprint, request, jsonify
from app import db
from app.models.module_5_1 import articlesatarys
from marshmallow import Schema, fields, validate

# Schéma Marshmallow OBLIGATOIRE
class ArticlesAtarysSchema(Schema):
    id = fields.Int(dump_only=True)
    reference = fields.Str(required=True, validate=validate.Length(max=100))
    libelle = fields.Str(required=True)
    prix_achat = fields.Decimal(as_string=True)
    # ... autres champs

bp = Blueprint('articles_atarys', __name__, url_prefix='/api/articles-atarys')

@bp.route('/', methods=['GET'])
def get_articles():
    # Logique de récupération avec pagination
    pass

@bp.route('/', methods=['POST'])
def create_article():
    # Logique de création avec validation
    pass
```

### **Validation Marshmallow OBLIGATOIRE**
- **Schéma pour chaque ressource** : Validation des types et contraintes
- **Gestion des erreurs** : Messages explicites pour l'utilisateur
- **Conversion des types** : String → Number, Boolean automatique

---

## 🎨 **Standards Frontend**

### **Composants React Standards**
```jsx
// frontend/src/components/AddRowForm.jsx
import React, { useState, useEffect } from 'react';

export default function AddRowForm({ onAdd, onCancel }) {
  const [formData, setFormData] = useState({});
  const [errors, setErrors] = useState({});

  // Validation en temps réel
  const validateForm = () => {
    // Logique de validation
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      onAdd(formData);
    }
  };

  return (
    <div className="modal">
      {/* Interface utilisateur */}
    </div>
  );
}
```

### **Standards UI/UX**
- **Padding** : 16px standard
- **Gap** : gap-3 pour les espacements
- **Responsive** : Adaptation mobile/desktop
- **Couleurs** : Palette Tailwind CSS
- **Messages d'erreur** : Explicites et contextuels

---

## 🔄 **Standards Communication Backend-Frontend**

### **Configuration CORS**
```python
# backend/app/__init__.py
from flask_cors import CORS

def create_app(config_name='development'):
    app = Flask(__name__)
    # ... configuration
    CORS(app)  # Communication frontend-backend
    return app
```

### **Gestion des Erreurs**
```javascript
// Frontend - Gestion d'erreurs standardisée
try {
  const response = await fetch('/api/articles-atarys/');
  const result = await response.json();
  
  if (result.success) {
    setData(result.data);
  } else {
    setError(result.message);
  }
} catch (err) {
  setError(`Erreur de connexion: ${err.message}`);
}
```

---

## 🛠️ **Standards Outils d'Administration**

### **API REST Configuration**
```python
# backend/run_flask_admin.py
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

class ArticlesAtarysAdmin(ModelView):
    column_list = ('id', 'reference', 'libelle', 'prix_achat', 
                   'coefficient', 'prix_unitaire', 'unite', 'tva_pct', 
                   'famille', 'actif', 'date_import', 'date_maj')

admin = Admin(app, name='ATARYS Admin', template_mode='bootstrap4')
admin.add_view(ArticlesAtarysAdmin(articlesatarys, db.session, 
                                   name="Articles ATARYS", 
                                   category="5. Devis-Facturation"))
```

---

## 📊 **Standards Performance**

### **Métriques de Performance**
- **Response time** : < 100ms pour les requêtes simples
- **Pagination** : 50 par défaut, `all` pour tout
- **Validation** : Marshmallow pour intégrité
- **Caching** : À implémenter pour les gros volumes

### **Optimisations**
- **Index** sur les colonnes clés
- **Requêtes optimisées** avec SQLAlchemy
- **Validation côté client ET serveur**
- **Gestion d'erreurs** avec rollback

---

## 🚀 **Standards Fonctionnalités Avancées**

### **Création Dynamique de Tables**
- **Interface multi-étapes** : Sélection module → Classe → Colonnes
- **Suggestions intelligentes** : Types selon nom de colonne
- **Génération automatique** : Code SQLAlchemy + Table SQLite
- **Intégration immédiate** : API REST automatique

### **Import Excel Intelligent**
- **Collage direct** : Ctrl+V depuis Excel
- **Nettoyage automatique** : Guillemets, espaces, types
- **Validation** : Filtrage des lignes vides
- **Logique UPSERT** : Création/mise à jour automatique

### **Logique UPSERT**
```python
# Vérification de l'existence avant insertion
existing_item = Model.query.filter_by(unique_field=value).first()

if existing_item:
    # Mise à jour
    for key, value in data.items():
        setattr(existing_item, key, value)
else:
    # Création
    new_item = Model(**data)
    db.session.add(new_item)

db.session.commit()
```

---

## 📚 **Standards Documentation**

### **Documentation Obligatoire**
- **Architecture** : `docs/02-architecture/`
- **APIs** : `docs/02-architecture/API_ENDPOINTS.md`
- **Base de données** : `docs/02-architecture/DATABASE_SCHEMA.md`
- **Workflows** : `docs/03-regles-standards/WORKFLOWS.md`

### **Commentaires de Code**
```python
# Standards pour les commentaires
def create_article():
    """
    Créer un nouvel article avec logique UPSERT
    
    Returns:
        JSON: Format standardisé {success, data, message}
    """
    pass
```

---

## ⚠️ **Interdictions Absolues**

### **❌ JAMAIS**
- **Créer de modèles sans BaseModel** : Héritage obligatoire
- **Utiliser Float pour les montants** : Toujours Numeric(10, 2)
- **Oublier la validation Marshmallow** : Intégrité obligatoire
- **Créer des APIs sans format standardisé** : {success, data, message}
- **Oublier CORS** : Communication frontend-backend obligatoire
- **Créer des String sans longueur max** : Limites obligatoires
- **Inventer des tables sans demande** : Consentement utilisateur obligatoire

### **✅ TOUJOURS**
- **Utiliser BaseModel** : Pattern standard obligatoire
- **Valider les données** : Marshmallow + validation frontend
- **Gérer les erreurs** : Messages explicites pour l'utilisateur
- **Documenter les APIs** : Spécifications complètes
- **Tester avant intégration** : Validation côté backend d'abord
- **Respecter les types** : Standards ATARYS obligatoires

---

## 🚀 **Environnement de Développement**

### **URLs et Ports Standards**
- **Frontend React** : http://localhost:3000
- **Backend Flask** : http://localhost:5000
- **Flask-Admin** : http://localhost:5001
- **Proxy API** : `/api/*` → `localhost:5000`

### **Commandes de Lancement**
```powershell
# Frontend (Terminal 1) - OPÉRATIONNEL
cd frontend; npm run dev

# API REST (Terminal 2) - OPÉRATIONNEL
cd backend; python run.py

# Flask-Admin (Terminal 3) - OPÉRATIONNEL
cd backend; python run_flask_admin.py
```

---

**✅ Standards ATARYS V2 - Architecture moderne avec fonctionnalités avancées !**
