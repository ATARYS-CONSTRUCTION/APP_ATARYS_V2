# 🏗️ Architecture ATARYS V2 - Synthèse Complète

> **Document de synthèse unique pour l'architecture ATARYS V2**  
> Stack technique, patterns, communication backend-frontend, métriques  
> **VERSION 2** : Architecture opérationnelle avec modules implémentés  
> Dernière mise à jour : 05/07/2025

---

## 🎯 **Vision et Objectifs ATARYS V2**

### **Objectifs Principaux**
- **Automatiser** les tâches informatiques récurrentes et indispensables
- **Remplacer** tous les fichiers Excel par une application qui archive, calcule et organise
- **Créer** des processus de travail efficaces et ludiques sur les tâches rébarbatives
- **Organiser** le travail du bureau en binôme
- **Renforcer** la protection juridique de l'entreprise
- **Réduire** le niveau de stress par une meilleure maîtrise des délais
- **Augmenter** le temps de présence sur les chantiers
- **Améliorer** la rentabilité par une meilleure organisation

### **Cible : Remplacer 17 Onglets Excel**
- **Fichier 1** : "Atarys 2025.xlsx" (10 onglets)
- **Fichier 2** : "📅 Module 8: Planning Atarys 2025 3.xlsm" (7 onglets)
- **Objectif** : Application web complète opérationnelle

---

## 🏗️ **Stack Technologique V2**

### **Backend - Python/Flask**
- **Framework** : Flask 3.x avec pattern Factory (`create_app()`)
- **ORM** : SQLAlchemy 2.0+ avec BaseModel pattern
- **Base de données** : SQLite avec BaseModel pattern
- **API** : REST avec format JSON standardisé `{success, data, message}`
- **API REST** : http://localhost:5000
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

## 📁 **Structure du Projet V2**

### **Architecture Modulaire Opérationnelle**
```
backend/
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

## 🗄️ **Base de Données V2**

### **Pattern BaseModel Standard**
```python
# backend/app/models/base.py
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

### **Modèles Implémentés**

#### **Module 5.1 - Articles ATARYS** (`articlesatarys`)
```python
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
```

**Données actuelles** : 176 lignes dans la table `articles_atarys`

---

## 🔌 **APIs REST V2**

### **Format Standardisé ATARYS**
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

### **Routes Implémentées**

#### **1. Articles ATARYS** (`/api/articles-atarys/`)
- **GET** : Récupération paginée ou complète (`per_page=all`)
- **POST** : Création avec logique UPSERT
- **PUT** : Modification par ID
- **DELETE** : Suppression par ID
- **DELETE /clear/** : Suppression de toutes les données

#### **2. Création de Tables** (`/api/create-table/`)
- **POST** : Création dynamique de tables
- Génération automatique du code SQLAlchemy
- Création du fichier modèle
- Création de la table SQLite

### **Validation Marshmallow**
- Schémas de validation pour chaque ressource
- Validation des types et contraintes
- Gestion des erreurs 400 (Bad Request)

---

## 🎨 **Frontend V2**

### **Pages Implémentées**
- **Module 12.1** : `BaseDeDonnees.jsx` (Base de données - OPÉRATIONNEL)
- **Module 1.1** : `PlanningSalaries.jsx` (Planning salariés - OPÉRATIONNEL)
- **Module 10.1** : `CalculArdoises.jsx` (Calcul ardoises - EN COURS)

### **Composants Dynamiques**

#### **1. AddRowForm.jsx**
- Formulaire dynamique basé sur JSON Schema
- Validation en temps réel
- Conversion automatique des types
- Intégration avec l'API

#### **2. CreateTableForm.jsx**
- Interface multi-étapes pour création de tables
- Suggestions intelligentes selon le nom des colonnes
- Génération automatique du code SQLAlchemy
- Intégration avec l'API de création

### **Fonctionnalités Avancées**

#### **Gestion des Données**
- **Collage Excel** : Import direct depuis Excel
- **Validation** : Filtrage des lignes vides
- **Conversion types** : String → Number, Boolean
- **Logique UPSERT** : Création/mise à jour automatique

#### **Interface Utilisateur**
- **Compteur de lignes** : Affichage dynamique (176 lignes)
- **Boutons d'action** : Ajouter ligne, créer table
- **Gestion d'erreurs** : Messages explicites
- **Responsive** : Adaptation mobile/desktop

---

## 🔄 **Communication Backend-Frontend**

### **Flux de Données**

#### **1. Chargement des Données**
```
Frontend → GET /api/articles-atarys/?per_page=all
Backend → SQLAlchemy Query → JSON Response
Frontend → setData(result.data)
```

#### **2. Sauvegarde des Données**
```
Frontend → POST/PUT /api/articles-atarys/
Backend → Validation Marshmallow → SQLAlchemy
Backend → Response JSON → Frontend Update
```

#### **3. Création de Tables**
```
Frontend → POST /api/create-table/
Backend → Génération Code → Création Fichier → Création Table
Backend → Response JSON → Frontend Refresh
```

### **Gestion des Erreurs**
- **CORS** : Configuré dans Flask
- **Validation** : Côté frontend ET backend
- **Rollback** : En cas d'erreur SQLAlchemy
- **Messages** : Explicites pour l'utilisateur

---

## 🛠️ **Outils d'Administration**

### **API REST** (Port 5000)
- Interface d'administration des données
- Vue personnalisée pour afficher l'ID
- Organisation par modules ATARYS
- Gestion CRUD complète

### **Scripts Utilitaires**
- **Import Excel** : `import_articles_atarys.py`
- **Initialisation DB** : `init_database.py`
- **Scripts batch** : `.bat/fermer_atarys.bat`

---

## 📊 **Métriques et Performance**

### **Base de Données**
- **176 lignes** dans `articles_atarys`
- **Compteur dynamique** : Total + lignes avec données
- **Pagination** : 50 par défaut, `all` pour tout

### **API Performance**
- **Response time** : < 100ms pour les requêtes simples
- **Validation** : Marshmallow pour intégrité
- **Caching** : À implémenter pour les gros volumes

---

## 🚀 **Fonctionnalités Avancées**

### **1. Création Dynamique de Tables**
- Interface utilisateur intuitive
- Génération automatique du code
- Intégration immédiate dans l'admin

### **2. Import Excel Intelligent**
- Collage direct depuis Excel
- Validation et nettoyage automatique
- Gestion des types de données

### **3. Logique UPSERT**
- Création/mise à jour automatique
- Gestion des doublons
- Intégrité des données

---

## 📈 **Évolution et Roadmap**

### **Modules Prioritaires**
1. **Module 3.1** : Liste Chantiers (priorité 1)
2. **Module 9.1** : Liste Salariés (priorité 2)
3. **Module 10.1** : Calcul Ardoises (priorité 3)

### **Améliorations Prévues**
- **Authentification** : JWT
- **PostgreSQL** : Migration production
- **Tests unitaires** : Couverture complète
- **Documentation API** : Swagger/OpenAPI

---

## 🚀 **Environnement de Développement**

### **URLs et Ports**
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

## 📚 **Documentation Associée**

### **Architecture**
- **[ATARYS_ARCHITECTURE.md](ATARYS_ARCHITECTURE.md)** - Architecture complète V2
- **[API_ENDPOINTS.md](API_ENDPOINTS.md)** - APIs REST implémentées
- **[DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)** - Structure base de données
- **[ATARYS_MODULES.md](ATARYS_MODULES.md)** - Organisation modulaire

### **Développement**
- **[DEV_MASTER.md](../01-guides-principaux/DEV_MASTER.md)** - Document central
- **[WORKFLOWS.md](../03-regles-standards/WORKFLOWS.md)** - Processus de développement
- **[STANDARDS_DEV.md](../03-regles-standards/STANDARDS_DEV.md)** - Standards techniques

---

**✅ Architecture ATARYS V2 - Système modulaire, extensible et performant !** 