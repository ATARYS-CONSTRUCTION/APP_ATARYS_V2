# 🏗️ Architecture ATARYS V2 - Synthèse Complète

> **Document de référence unique pour l'architecture ATARYS V2**  
> Stack technique, patterns, communication backend-frontend  
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
- **Admin** : API REST sur port 5000
- **CORS** : Configuré pour communication frontend-backend
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

### **🎯 STANDARDS D'INTERFACE UTILISATEUR**

#### **Tableaux Interactifs**
- **Simple clic** : Sélection de la ligne avec highlight visuel
- **Double clic** : Ouverture automatique du formulaire de modification
- **Boutons d'action** : Modifier, Supprimer, Actions spéciales par ligne
- **Feedback visuel** : Bordure colorée pour la ligne sélectionnée

#### **Structure Tableau Standard ATARYS**
```jsx
<tr
  key={item.id}
  onClick={() => handleRowClick(item)}
  onDoubleClick={() => handleEdit(item)}
  className={`hover:bg-gray-50 cursor-pointer ${
    selectedItem?.id === item.id ? 'bg-blue-50 border-l-4 border-blue-500' : ''
  }`}
>
```

#### **Gestion des Relations Many-to-Many**
- **Affichage des relations** : Utiliser `find()` pour récupérer les libellés
- **Exemple** : `niveauQualifications.find(q => q.id === salary.niveau_qualification_id)?.niveau`
- **Fallback obligatoire** : Toujours prévoir `|| '-'` pour les valeurs nulles
- **Sélection multiple** : Utiliser `multiple` et `size` pour les listes

#### **Formulaires de Modification**
- **Champs obligatoires** : Validation côté frontend ET backend
- **Instructions utilisateur** : Textes d'aide pour les interactions complexes
- **Sélection multiple** : Instructions claires (ex: "Ctrl+clic pour sélection multiple")
- **Compteur de sélections** : Affichage du nombre d'éléments sélectionnés

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

### **4. Déclencheurs Automatiques**
- **Configuration** : Interface admin pour définir les déclencheurs
- **Détection automatique** : Intégration dans les endpoints
- **Génération** : Service automatique de création des tâches
- **Suivi** : Interface de gestion des tâches

### **5. Règle d'Or - Nouveaux Déclencheurs**
> **⚠️ IMPORTANT :** Lors de la création de nouvelles commandes/endpoints dans l'application, TOUJOURS demander s'il faut ajouter un déclencheur automatique pour générer des tâches.
> 
> **Exemple :** Création d'un nouvel endpoint `/api/nouvelle-commande/` → Demander : "Faut-il un déclencheur automatique pour cette commande ?"

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
- **Déclencheurs automatiques** : Système complet de tâches automatiques

---

## 🚀 **Système de Déclencheurs Automatiques**

### **📋 Vue d'Ensemble**

ATARYS V2 intègre un système de déclencheurs automatiques qui génère des tâches en fonction d'événements métier. Cette approche permet une automatisation complète sans modification de code.

### **🎯 Architecture des Déclencheurs**

#### **1. Configuration (Base de Données)**
```python
# Table famille_tach - Configuration des déclencheurs
{
    "famille_tache": "chantier",
    "type_tache": "Chantier création",
    "declencheur": "chantier_creation",
    "auto_generee": True,
    "statut": "A faire",
    "date_echeance": "x jours après creation"
}
```

#### **2. Détection (Endpoints API)**
```python
# Intégration dans les endpoints existants
@chantier_bp.route('/api/chantiers/', methods=['POST'])
def create_chantier():
    # 1. Créer l'entité
    chantier = Chantier(**data)
    db.session.add(chantier)
    db.session.commit()
    
    # 2. DÉCLENCHEUR AUTOMATIQUE
    service = TacheAutomatiqueService()
    contexte = {'chantier_id': chantier.id}
    taches_creees = service.declencher_taches('chantier_creation', contexte)
    
    return jsonify({
        'success': True,
        'data': chantier_schema.dump(chantier),
        'taches_creees': len(taches_creees)
    })
```

#### **3. Génération (Service Automatique)**
```python
class TacheAutomatiqueService:
    def declencher_taches(self, evenement: str, contexte: dict):
        # 1. Chercher les tâches templates
        taches_templates = FamilleTach.query.filter_by(
            declencheur=evenement,
            auto_generee=True
        ).all()
        
        # 2. Créer les tâches selon le type (chantier ou administratif)
        taches_creees = []
        for template in taches_templates:
            if template.famille_tache == 'chantier' and contexte.get('chantier_id'):
                # Créer une tâche chantier
                nouvelle_tache = TachesChantiers(
                    titre=template.titre,
                    famille_tach=template.famille_tache,
                    type_tache=template.type_tache,
                    chantier_id=contexte.get('chantier_id'),
                    statut=template.statut,
                    auto_generee=True,
                    declencheur=evenement
                )
            else:
                # Créer une tâche administrative
                nouvelle_tache = TachesAdministratives(
                    titre=template.titre,
                    famille_tach=template.famille_tache,
                    type_tache=template.type_tache,
                    chantier_id=contexte.get('chantier_id'),  # Nullable
                    statut=template.statut,
                    auto_generee=True,
                    declencheur=evenement,
                    type_administratif=template.type_administratif or 'GENERAL'
                )
            
            db.session.add(nouvelle_tache)
            taches_creees.append(nouvelle_tache)
        
        db.session.commit()
        return taches_creees
```

### **🎯 Déclencheurs Configurés**

#### **Module 3 - Chantiers**
- `chantier_creation` : Création d'un nouveau chantier
- `chantier_signature` : Signature d'un chantier
- `chantier_en_cours` : Chantier en cours d'exécution
- `chantier_termine` : Fin d'un chantier

#### **Module 9 - Salariés**
- `insertion_salarié` : Création d'un nouveau salarié

#### **Module 1 - Planning**
- `modification_planning` : Modification du planning

### **📋 Avantages du Système**

#### **Flexibilité Maximale**
- ✅ **Configuration sans code** : L'admin peut tout configurer via l'interface
- ✅ **Ajout de déclencheurs** : Nouveaux événements sans redéploiement
- ✅ **Modification des règles** : Changement des logiques de calcul en temps réel

#### **Maintenance Réduite**
- ✅ **Pas de redéploiement** : Modifications via interface admin
- ✅ **Configuration centralisée** : Tous les déclencheurs dans une table
- ✅ **Auditabilité** : Historique des configurations

#### **Évolutivité**
- ✅ **Nouveaux événements** : Ajout facile de déclencheurs
- ✅ **Règles métier** : Configuration des logiques de calcul
- ✅ **Notifications** : Possibilité d'ajouter des alertes

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

**✅ Architecture ATARYS V2 - Système modulaire, extensible et performant avec déclencheurs automatiques !** 