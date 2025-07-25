# 🗄️ Schéma Base de Données ATARYS V2

> **Structure technique complète des tables SQLite organisée par Modules ATARYS**  
> Architecture SQLAlchemy + API REST + Organisation modulaire  
> **VERSION 2** : Base opérationnelle avec modèles implémentés  
> Dernière mise à jour : 19/07/2025

---

## 📋 Vue d'ensemble

Base de données SQLite V2 : `data/atarys_data.db` (OPÉRATIONNEL)
- **Structure modulaire** : Selon `ATARYS_MODULES.md`
- **Source données** : Fichier Excel propre et à jour
- **Approche V2** : Création propre, pas de migration V1
- **Relations** : Clés étrangères et contraintes implémentées
- **Index** : Optimisation des performances
- **ORM** : SQLAlchemy 2.0+ pour l'abstraction
- **Admin** : API REST organisé par modules

---

## 🏗️ Architecture Technique

### Stack Technologique
- **Base de données** : SQLite 3
- **ORM** : SQLAlchemy 2.0+
- **Framework Web** : Flask 3.x
- **Interface Admin** : API REST
- **Frontend** : React + Vite
- **API** : REST format `{success, data, message}`

### Structure de l'Application V2 (OPÉRATIONNEL)
```
backend/                 # OPÉRATIONNEL
├── app/
│   ├── models/          # Modèles SQLAlchemy selon modules ATARYS
│   │   ├── base.py      # Pattern BaseModel standard
│   │   ├── module_5.py  # Modèle FamilleOuvrages
│   │   ├── module_12.py # Modèles TestAuditTable, TestCle2
│   │   └── module_1.py à module_13.py # Structures créées
│   ├── routes/          # API endpoints par module
│   │   └── create_table.py   # API création dynamique
│   └── __init__.py      # Factory pattern Flask
├── app.py   # Point d'entrée API REST (port 5000)
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
# backend/app/models/module_5.py - OPÉRATIONNEL
from .base import BaseModel

class FamilleOuvrages(BaseModel):
    __tablename__ = 'famille_ouvrages'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num_bd_atarys = db.Column(db.String(10))
    libelle = db.Column(db.String(100), nullable=False)
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
- **Admin** : Interface API REST avec colonne ID visible

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

## 🎛️ API REST Configuration

### **Configuration Générale**
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

## 📊 Documentation des Tables

### Table `salaries`

**Description** : Table des salariés avec relation vers les villes.

**Colonnes** :
- `id` (INTEGER, PK) : Identifiant unique
- `nom` (VARCHAR(100)) : Nom du salarié
- `prenom` (VARCHAR(100)) : Prénom du salarié
- `salaire_brut_horaire` (NUMERIC(10, 2)) : Salaire horaire brut
- `nbre_heure_hebdo` (NUMERIC(10, 2)) : Nombre d'heures hebdomadaires
- `type_contrat` (VARCHAR(50)) : Type de contrat (CDI, CDD, etc.)
- `date_entree` (DATE) : Date d'entrée dans l'entreprise
- `date_sortie` (DATE) : Date de sortie (optionnel)
- `niveau_qualification_id` (INTEGER, FK) : Référence vers `niveau_qualification`
- `colonne_planning` (VARCHAR(100)) : Position dans le planning
- `email` (VARCHAR(200)) : Adresse email
- `num_telephone` (VARCHAR(20)) : Numéro de téléphone
- `adresse` (VARCHAR(200)) : Adresse postale
- `ville_id` (INTEGER, FK) : Référence vers `villes` (AJOUTÉ)
- `date_naissance` (DATE) : Date de naissance
- `num_securite_social` (VARCHAR(20)) : Numéro de sécurité sociale
- `ondrive_path` (VARCHAR(500)) : Chemin OneDrive
- `created_at` (DATETIME) : Date de création
- `updated_at` (DATETIME) : Date de mise à jour

**Relations** :
- `ville_id` → `villes.id` (ON DELETE SET NULL)
- `niveau_qualification_id` → `niveau_qualification.id` (ON DELETE SET NULL)

**Endpoints API** :
- `GET /api/salaries` : Liste tous les salariés
- `GET /api/salaries/<id>` : Récupère un salarié par son ID
- `POST /api/salaries` : Crée un nouveau salarié
- `PUT /api/salaries/<id>` : Met à jour un salarié
- `DELETE /api/salaries/<id>` : Supprime un salarié

### Table `villes`

**Description** : Table de référence pour toutes les villes françaises.

**Colonnes** :
- `id` (INTEGER, PK) : Identifiant unique
- `communes` (VARCHAR(100)) : Nom de la commune
- `code_postal` (INTEGER) : Code postal
- `code_insee` (INTEGER) : Code INSEE
- `departement` (INTEGER) : Numéro du département
- `latitude` (FLOAT) : Coordonnée GPS latitude
- `longitude` (FLOAT) : Coordonnée GPS longitude
- `zone_nv` (INTEGER) : Zone climatique (1, 2, ou 3)
- `distance_km_oiseau` (FLOAT) : Distance à vol d'oiseau
- `distance_km_routes` (FLOAT) : Distance par les routes
- `temps_route_min` (FLOAT) : Temps de trajet en minutes
- `created_at` (DATETIME) : Date de création
- `updated_at` (DATETIME) : Date de mise à jour

**Relations** :
- `salaries` (one-to-many) : Les salariés qui habitent dans cette ville

**Endpoints API** :
- `GET /api/villes` : Liste toutes les villes
- `GET /api/villes/search?code_postal=35000` : Recherche par code postal
- `GET /api/villes/search?ville=rennes` : Recherche par nom de ville
- `GET /api/villes/<id>` : Récupère une ville par son ID



### Table `niveau_qualification`

**Description** : Table de référence pour les niveaux de qualification.

**Colonnes** :
- `id` (INTEGER, PK) : Identifiant unique
- `niveau` (VARCHAR(100)) : Code du niveau (ex: N1P1)
- `categorie` (VARCHAR(100)) : Description du niveau
- `created_at` (DATETIME) : Date de création
- `updated_at` (DATETIME) : Date de mise à jour

**Relations** :
- Aucune relation active pour le moment

### **Phase 3 : Modules Additionnels (2-3 semaines)**
1. **Modules 1.1/1.2** : Planning
2. **Modules 7.1/7.2** : Gestion et tableaux de bord
3. **Modules 6.x** : Atelier
4. **Modules 8.x** : Comptabilité

---

## 🚨 **Règle d'Or - Déclencheurs Automatiques**

### **⚠️ IMPORTANT : Nouveaux Endpoints**
> Lors de la création de nouveaux endpoints/commandes dans l'application, TOUJOURS demander s'il faut ajouter un déclencheur automatique pour générer des tâches.

### **Exemples de Questions Obligatoires :**
- **Nouvel endpoint** `/api/nouvelle-commande/` → "Faut-il un déclencheur automatique ?"
- **Nouvelle table** `nouvelle_table` → "Cette table déclenche-t-elle des tâches automatiques ?"
- **Nouveau module** → "Ce module nécessite-t-il des déclencheurs automatiques ?"

### **Service Disponible :**
- **Fichier** : `backend/app/services/tache_automatique_service.py`
- **Statut** : ✅ **OPÉRATIONNEL**
- **Déclencheurs actuels** : 3 (chantier_creation, chantier_signature, insertion_salarié)
- **Extension** : Facile d'ajouter de nouveaux déclencheurs selon les besoins

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
- **Maintenance** : API REST pour gestion des données

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
- **Admin interface** : API REST opérationnel
- **API REST** : Format standardisé `{success, data, message}`

---

**✅ Base de données ATARYS V2 - Architecture modulaire opérationnelle !** 

### **Tables Module 2 - SYSTÈME TÂCHES AUTOMATIQUES** (STRUCTURE FINALE)

> **⚠️ NOUVELLE STRUCTURE** basée sur l'Excel de déclencheurs  
> **Architecture : 2 tables séparées + règles automatiques**  
> **Document détaillé** : `docs/02-architecture/02-modules/module-02/STRUCTURE_TACHES_AUTOMATIQUES.md`

#### **Table `taches_chantiers` - Tâches liées aux chantiers**

```sql
CREATE TABLE taches_chantiers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre VARCHAR(200) NOT NULL,
    description TEXT,
    utilisateur VARCHAR(50) NOT NULL,  -- YANN, JULIEN
    statut VARCHAR(20) DEFAULT 'A_FAIRE',
    priorite VARCHAR(10) DEFAULT 'NORMALE',
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_echeance DATETIME,
    date_completion DATETIME,
    temps_estime DECIMAL(5,2),
    temps_passe DECIMAL(5,2),
    notes TEXT,
    auto_generee BOOLEAN DEFAULT 0,
    declencheur VARCHAR(50),  -- Événement déclencheur
    famille_tach_id INTEGER,
    chantier_id INTEGER NOT NULL,  -- OBLIGATOIRE pour tâches chantiers
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (famille_tach_id) REFERENCES famille_tach(id),
    FOREIGN KEY (chantier_id) REFERENCES chantiers(id)
);
```

#### **Table `taches_administratives` - Tâches administratives générales**

```sql
CREATE TABLE taches_administratives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre VARCHAR(200) NOT NULL,
    description TEXT,
    utilisateur VARCHAR(50) NOT NULL,  -- YANN, JULIEN
    statut VARCHAR(20) DEFAULT 'A_FAIRE',
    priorite VARCHAR(10) DEFAULT 'NORMALE',
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_echeance DATETIME,
    date_completion DATETIME,
    temps_estime DECIMAL(5,2),
    temps_passe DECIMAL(5,2),
    notes TEXT,
    auto_generee BOOLEAN DEFAULT 0,
    declencheur VARCHAR(50),  -- Événement déclencheur
    famille_tach_id INTEGER,
    chantier_id INTEGER,  -- OPTIONNEL pour tâches administratives
    type_administratif VARCHAR(50),  -- FISCAL, RH, COMPTABLE, GENERAL
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (famille_tach_id) REFERENCES famille_tach(id),
    FOREIGN KEY (chantier_id) REFERENCES chantiers(id)
);
```

#### **Avantages de l'Approche Deux Tables**

✅ **Séparation claire** : Tâches chantiers vs administratives  
✅ **Contraintes adaptées** : `chantier_id` obligatoire pour tâches chantiers  
✅ **Requêtes optimisées** : Filtrage plus efficace par type  
✅ **Évolutivité** : Champs spécifiques par type (`type_administratif`)  
✅ **Maintenance** : Logique métier séparée et claire  

---

## ⚙️ Module 12.1 - BASE DE DONNÉES (PARAMÈTRES)

### **🎯 Objectif du Module 12.1**

Interface d'administration dynamique pour créer et gérer les tables SQLite selon les modules ATARYS, avec génération automatique des chemins backend et frontend.

### **🏗️ Architecture Proposée**

#### **1. Structure Backend Unifiée**
```
backend/app/
├── models/
│   ├── base.py                    # BaseModel standard
│   ├── module_12_1.py            # Modèles du module 12.1
│   └── __init__.py               # Imports automatiques
├── routes/
│   ├── module_12_1.py            # Routes du module 12.1
│   └── __init__.py               # Blueprint registration
└── services/
    └── table_generator.py        # Service de génération
```

#### **2. Frontend Conservé (Interface Existante)**
```
frontend/src/
├── components/
│   ├── CreateTableForm.jsx       # Formulaire création table
│   ├── AddRowForm.jsx            # Formulaire ajout lignes
│   └── Layout.jsx                # Layout standard
├── pages/
│   └── BaseDeDonnees.jsx         # Page module 12.1
└── App.jsx                       # Route /base-donnees
```

### **🚨 Erreurs Commises et Solutions**

#### **❌ Erreur 1 : Architecture Contradictoire**
**Problème :** Mélange d'approches manuelle (`module_X_Y.py`) et automatique (`table_name_model.py`)
```python
# ❌ AVANT - Conflits SQLAlchemy
class ArticlesAtarys(BaseModel):  # module_5_1.py
class articlesatarys(BaseModel):   # articles_atarys_model.py
# → "Table 'articles_atarys' is already defined"
```

**✅ Solution :** Approche unifiée par module
```python
# ✅ APRÈS - Architecture cohérente
# backend/app/models/module_12_1.py
class TableDefinition(BaseModel):
    __tablename__ = 'table_definitions'
    # Structure pour stocker les définitions de tables

class GeneratedTable(BaseModel):
    __tablename__ = 'generated_tables'
    # Structure pour les tables générées
```

#### **❌ Erreur 2 : Imports Circulaires**
**Problème :** Tentatives d'import de modules inexistants
```python
# ❌ AVANT - Import incorrect
from app.models.base_model import BaseModel  # Fichier inexistant
```

**✅ Solution :** Imports standardisés
```python
# ✅ APRÈS - Import correct
from app.models.base import BaseModel  # Fichier existant
```

#### **❌ Erreur 3 : Encodage Unicode Windows**
**Problème :** Emojis dans les scripts causant des crashes
```python
# ❌ AVANT - Emojis Unicode
print(f"🔍 Analyse de la table '{table_name}'...")
# → UnicodeEncodeError: 'charmap' codec can't encode character
```

**✅ Solution :** Texte simple
```python
# ✅ APRÈS - Texte simple
print(f"[INFO] Analyse de la table '{table_name}'...")
```

#### **❌ Erreur 4 : Chemins de Scripts Incorrects**
**Problème :** Scripts cherchés dans le mauvais répertoire
```python
# ❌ AVANT - Chemin incorrect
subprocess.run(['python', 'scripts/simple_model_generator.py'], cwd='app/')
```

**✅ Solution :** Chemins absolus
```python
# ✅ APRÈS - Chemin correct
script_path = os.path.join(os.getcwd(), 'backend', 'scripts', 'table_generator.py')
subprocess.run(['python', script_path], cwd=os.path.join(os.getcwd(), 'backend'))
```

### **🎯 Nouvelle Architecture Module 12.1**

#### **1. Interface Utilisateur (Frontend)**
- **Page** : `/base-donnees` → `BaseDeDonnees.jsx`
- **Fonctionnalités** :
  - Sélection du module ATARYS (1-13)
  - Définition de la table (nom, colonnes, types)
  - Génération automatique du modèle SQLAlchemy
  - Création des routes API REST
  - Interface d'administration API REST

#### **2. Backend Unifié (Module 12.1)**
```python
# backend/app/models/module_12_1.py
class TableDefinition(BaseModel):
    __tablename__ = 'table_definitions'
    
    module_id = db.Column(db.Integer, nullable=False)  # Module ATARYS (1-13)
    table_name = db.Column(db.String(100), nullable=False, unique=True)
    class_name = db.Column(db.String(100), nullable=False)
    columns_definition = db.Column(db.JSON, nullable=False)  # Structure des colonnes
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<TableDefinition {self.table_name}>'

class GeneratedTable(BaseModel):
    __tablename__ = 'generated_tables'
    
    table_name = db.Column(db.String(100), nullable=False, unique=True)
    module_id = db.Column(db.Integer, nullable=False)
    model_file = db.Column(db.String(200))  # Chemin vers le fichier modèle
    route_file = db.Column(db.String(200))  # Chemin vers le fichier route
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<GeneratedTable {self.table_name}>'
```

#### **3. Service de Génération**
```python
# backend/app/services/table_generator.py
class TableGeneratorService:
    """Service pour générer automatiquement les modèles et routes"""
    
    def __init__(self):
        self.modules_atarys = {
            1: "PLANNING", 2: "LISTE_DES_TACHES", 3: "LISTE_CHANTIERS",
            4: "CHANTIERS", 5: "DEVIS_FACTURATION", 6: "ATELIER",
            7: "GESTION", 8: "COMPTABILITE", 9: "SOCIAL",
            10: "OUTILS", 11: "ARCHIVES", 12: "PARAMETRES", 13: "AIDE"
        }
    
    def generate_table(self, module_id, table_name, columns_definition):
        """Générer une table complète avec modèle et routes"""
        # 1. Créer le modèle SQLAlchemy
        model_code = self._generate_model_code(table_name, columns_definition)
        
        # 2. Créer les routes API
        route_code = self._generate_route_code(table_name, module_id)
        
        # 3. Enregistrer dans la base
        self._save_table_definition(module_id, table_name, columns_definition)
        
        # 4. Générer les fichiers
        self._write_model_file(table_name, model_code)
        self._write_route_file(table_name, route_code)
        
        return {"success": True, "message": f"Table {table_name} générée avec succès"}
    
    def _generate_model_code(self, table_name, columns):
        """Générer le code du modèle SQLAlchemy"""
        # Logique de génération selon les standards ATARYS
        pass
    
    def _generate_route_code(self, table_name, module_id):
        """Générer le code des routes API"""
        # Logique de génération selon les standards ATARYS
        pass
```

#### **4. Routes API Module 12.1**
```python
# backend/app/routes/module_12_1.py
from flask import Blueprint, request, jsonify
from app.models.module_12_1 import TableDefinition, GeneratedTable
from app.services.table_generator import TableGeneratorService

module_12_1 = Blueprint('module_12_1', __name__)
table_generator = TableGeneratorService()

@module_12_1.route('/api/module-12-1/create-table', methods=['POST'])
def create_table():
    """Créer une nouvelle table avec génération automatique"""
    data = request.get_json()
    
    try:
        result = table_generator.generate_table(
            module_id=data['module_id'],
            table_name=data['table_name'],
            columns_definition=data['columns']
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@module_12_1.route('/api/module-12-1/list-tables', methods=['GET'])
def list_tables():
    """Lister toutes les tables générées"""
    tables = TableDefinition.query.filter_by(is_active=True).all()
    return jsonify({
        "success": True,
        "data": [table.to_dict() for table in tables]
    })
```

### **🎯 Workflow Module 12.1**

#### **Étape 1 : Interface Utilisateur**
1. Utilisateur accède à `/base-donnees`
2. Sélectionne le module ATARYS (1-13)
3. Définit le nom de la table et les colonnes
4. Valide la création

#### **Étape 2 : Génération Backend**
1. Service `TableGeneratorService` traite la demande
2. Génère le modèle SQLAlchemy selon standards ATARYS
3. Génère les routes API REST
4. Crée les fichiers dans la structure appropriée

#### **Étape 3 : Intégration**
1. Enregistrement dans `table_definitions`
2. Mise à jour des imports automatiques
3. Redémarrage du serveur Flask
4. Interface API REST mise à jour

### **✅ Avantages de cette Architecture**

#### **Simplicité**
- **Interface unique** : Un seul formulaire pour créer toutes les tables
- **Standards automatiques** : Respect automatique des conventions ATARYS
- **Pas de scripts multiples** : Un seul service de génération

#### **Cohérence**
- **Architecture unifiée** : Toutes les tables suivent le même pattern
- **Imports standardisés** : Plus de conflits d'imports
- **Nomenclature cohérente** : Respect des conventions ATARYS

#### **Maintenabilité**
- **Code centralisé** : Toute la logique dans le module 12.1
- **Documentation intégrée** : Chaque table documentée automatiquement
- **Évolutivité** : Facile d'ajouter de nouveaux types de colonnes

### **🚀 Prochaines Étapes**

1. **Implémentation du service** `TableGeneratorService`
2. **Création des modèles** `TableDefinition` et `GeneratedTable`
3. **Développement des routes** API module 12.1
4. **Intégration frontend** avec l'interface existante
5. **Tests complets** de la génération automatique

---

**✅ Module 12.1 - Architecture unifiée et simplifiée pour la génération automatique de tables !** 

---

## 🗑️ Suppression complète d’une table (workflow professionnel)

> Utiliser cette procédure lorsque vous voulez **retirer définitivement** une table du projet : modèle, routes, schéma, base SQLite **et** historique Alembic.

1. **Nettoyage du code**
   1. Supprimer ou commenter la classe modèle dans `backend/app/models/module_X.py`.
   2. Supprimer les routes CRUD correspondantes dans `backend/app/routes/module_X.py`.
   3. Supprimer le schéma Marshmallow dans `backend/app/schemas/module_X.py`.
   4. Vérifier qu’aucun import (`from app.models…`) ne référence encore la classe.

2. **Rollback de la dernière révision (si elle créait la table)**
   ```powershell
   flask db downgrade <revision_précédente>
   ```
   *Astuce : `flask db history -v` pour lister les révisions et identifier le hash.*

3. **Supprimer la révision Alembic devenue inutile**
   • Effacer le fichier `.py` dans `backend/migrations/versions/` qui contenait la création ou la modification de la table.

4. **Générer une nouvelle révision « drop table »** (sécurisé)
   ```powershell
   flask db migrate -m "Drop table <nom_table>"
   ```
   – Le fichier généré est souvent vide en SQLite ; remplace alors le contenu de `upgrade()` par :
   ```python
   from alembic import op

   def upgrade():
       op.drop_table('<nom_table>')

   def downgrade():
       pass  # (réimplémentation éventuelle)
   ```

5. **Appliquer la migration**
   ```powershell
   flask db upgrade
   ```

6. **Vérification finale**
   ```python
   from sqlalchemy import inspect
   from app import db
   assert '<nom_table>' not in inspect(db.engine).get_table_names()
   ```

**💡 Pourquoi ?**
• Garantit la cohérence entre le code et la base de données.  
• Évite les commandes `ALTER TABLE` non supportées par SQLite.  
• Conserve un historique clair dans Alembic.

--- 