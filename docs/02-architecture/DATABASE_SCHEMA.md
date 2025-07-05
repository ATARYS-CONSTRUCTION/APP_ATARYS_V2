# 🗄️ Schéma Base de Données ATARYS

> **Structure technique complète des tables SQLite + Architecture SQLAlchemy + Flask-Admin**
> Dernière mise à jour : 03/07/2025

---

## 📋 Vue d'ensemble

Base de données SQLite : `data/atarys_data.db`
- **23 tables** principales
- **792+ enregistrements** de données
- **Relations** : Clés étrangères et contraintes
- **Index** : Optimisation des performances
- **ORM** : SQLAlchemy pour l'abstraction
- **Admin** : Flask-Admin pour la gestion

---

## 🔢 Types de Données Numériques

### **FLOAT vs NUMERIC - Recommandations ATARYS**

**Situation Actuelle :**
- Les modèles utilisent `db.Float` (REAL en SQLite)
- Script d'import utilise `NUMERIC` pour validation

**Problème Identifié :**
```python
# Exemple d'erreur de précision avec FLOAT
0.1 + 0.2  # = 0.30000000000000004 (incorrect)
```

**Recommandation :**
Pour les montants financiers, utiliser `NUMERIC` avec précision fixe :

```python
# Recommandé pour ATARYS
montant_ht = db.Column(db.Numeric(10, 2), nullable=True, default=0.00)
# 10 chiffres total, 2 décimales (ex: 12345678.90)
```

**Avantages NUMERIC :**
- ✅ Précision exacte pour les calculs financiers
- ✅ Pas d'erreurs d'arrondi
- ✅ Validation stricte des données
- ✅ Conformité comptable

**Migration Recommandée :**
1. Changer `db.Float` → `db.Numeric(10, 2)` pour les montants
2. Garder `db.Float` pour les mesures techniques (longueurs, angles)
3. Mettre à jour les validations

---

## 🏗️ Architecture Technique

### Stack Technologique
- **Base de données** : SQLite 3
- **ORM** : SQLAlchemy 2.x
- **Framework Web** : Flask 3.x
- **Interface Admin** : Flask-Admin
- **Frontend** : React + Vite
- **API** : RESTful avec blueprints

### Structure de l'Application
```
backend/
├── app/
│   ├── models/          # Modèles SQLAlchemy
│   ├── services/        # Logique métier
│   ├── routes/          # API endpoints
│   ├── middleware/      # Middleware (logging, errors)
│   └── config/          # Configuration
├── admin_atarys.py      # Interface Flask-Admin
└── run.py              # Serveur principal
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

## 🏗️ Tables Principales

### `chantiers`
Table principale des chantiers clients

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique du chantier |
| civilite | TEXT | NULL | Civilité du client (M., Mme, etc.) |
| nom | TEXT | NULL | Nom du client |
| prenom | TEXT | NULL | Prénom du client |
| email | TEXT | NULL | Email du client |
| telephone | TEXT | NULL | Téléphone du client |
| adresse | TEXT | NULL | Adresse du chantier |
| code_postal | TEXT | NULL | Code postal |
| ville | TEXT | NULL | Ville du chantier |
| description | TEXT | NULL | Description du chantier |
| reference_chantier | TEXT | UNIQUE | Référence unique du chantier |
| montant_ht_devis | REAL | DEFAULT 0.0 | Montant HT total (somme des devis) |
| nombre_heures_total | REAL | DEFAULT 0.0 | Nombre d'heures total (somme des devis) |
| famille_ouvrages | TEXT | NULL | JSON des familles d'ouvrages |
| dossier_onedrive | TEXT | NULL | Lien vers dossier OneDrive |
| etat_id | INTEGER | NOT NULL | Référence vers `etats_chantier` |
| actif | INTEGER | DEFAULT 1 | Chantier actif (1) ou archivé (0) |
| date_creation | TEXT | NOT NULL | Date de création (YYYY-MM-DD HH:MM:SS) |

**Modèle SQLAlchemy :**
```python
class Chantier(db.Model):
    __tablename__ = '🏗️ Module 3: Chantiers & Devis'
    
    id = db.Column(db.Integer, primary_key=True)
    civilite = db.Column(db.String(10))
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    email = db.Column(db.String(150))
    telephone = db.Column(db.String(20))
    adresse = db.Column(db.Text)
    code_postal = db.Column(db.String(10))
    ville = db.Column(db.String(100))
    description = db.Column(db.Text)
    reference_chantier = db.Column(db.String(50), unique=True)
    montant_ht_devis = db.Column(db.Float, default=0.0)
    nombre_heures_total = db.Column(db.Float, default=0.0)
    famille_ouvrages = db.Column(db.Text)
    dossier_onedrive = db.Column(db.Text)
    etat_id = db.Column(db.Integer, db.ForeignKey('🏗️ Module 3: Chantiers & Devis_chantier.id'), nullable=False)
    actif = db.Column(db.Integer, default=1)
    date_creation = db.Column(db.String(20), nullable=False)
    
    # Relations
    etat = db.relationship('EtatChantier', backref='🏗️ Module 3: Chantiers & Devis')
    devis = db.relationship('🏗️ Module 3: Chantiers & Devis', backref='🏗️ Module 3: Chantiers & Devis', lazy='dynamic')
```

**Règles Métier :**
- `reference_chantier` est obligatoire et unique
- `montant_ht_devis` et `nombre_heures_total` sont calculés automatiquement
- `famille_ouvrages` contient un JSON des types d'ouvrages
- `actif = 1` pour les chantiers en cours, `0` pour archivés

### `etats_chantier`
États des chantiers

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique de l'état |
| libelle | TEXT | NOT NULL | Libellé de l'état |
| couleur | TEXT | NULL | Couleur associée (hex) |
| ordre | INTEGER | DEFAULT 0 | Ordre d'affichage |

**Modèle SQLAlchemy :**
```python
class EtatChantier(db.Model):
    __tablename__ = '🏗️ Module 3: Chantiers & Devis_chantier'
    
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(50), nullable=False)
    couleur = db.Column(db.String(7))  # #RRGGBB
    ordre = db.Column(db.Integer, default=0)
```

**États Standards :**
- 1: "En cours"
- 2: "Terminé"
- 3: "En attente"
- 4: "Annulé"

### `devis`
Devis clients

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique du devis |
| chantier_id | INTEGER | NOT NULL | Référence vers `chantiers` |
| numero_devis | TEXT | UNIQUE | Numéro unique du devis |
| date_devis | TEXT | NOT NULL | Date du devis |
| montant_ht | REAL | DEFAULT 0.0 | Montant HT du devis |
| nombre_heures | REAL | DEFAULT 0.0 | Nombre d'heures estimé |
| description | TEXT | NULL | Description du devis |
| statut | TEXT | DEFAULT 'Brouillon' | Statut du devis |
| date_creation | TEXT | NOT NULL | Date de création |

**Modèle SQLAlchemy :**
```python
class Devis(db.Model):
    __tablename__ = '🏗️ Module 3: Chantiers & Devis'
    
    id = db.Column(db.Integer, primary_key=True)
    chantier_id = db.Column(db.Integer, db.ForeignKey('🏗️ Module 3: Chantiers & Devis.id'), nullable=False)
    numero_devis = db.Column(db.String(50), unique=True)
    date_devis = db.Column(db.String(10), nullable=False)
    montant_ht = db.Column(db.Float, default=0.0)
    nombre_heures = db.Column(db.Float, default=0.0)
    description = db.Column(db.Text)
    statut = db.Column(db.String(20), default='Brouillon')
    date_creation = db.Column(db.String(20), nullable=False)
```

### `villes`
Référentiel des villes

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique |
| nom | TEXT | NOT NULL | Nom de la ville |
| code_postal | TEXT | NOT NULL | Code postal |
| departement | TEXT | NULL | Département |
| region | TEXT | NULL | Région |

**Modèle SQLAlchemy :**
```python
class Ville(db.Model):
    __tablename__ = '🌍 Module 11: Géographie'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    code_postal = db.Column(db.String(10), nullable=False)
    departement = db.Column(db.String(50))
    region = db.Column(db.String(50))
```

### `salaries`
Salariés de l'entreprise

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique |
| nom | TEXT | NOT NULL | Nom du salarié |
| prenom | TEXT | NOT NULL | Prénom du salarié |
| poste | TEXT | NULL | Poste occupé |
| telephone | TEXT | NULL | Téléphone |
| email | TEXT | NULL | Email |
| actif | INTEGER | DEFAULT 1 | Salarié actif (1) ou inactif (0) |

**Modèle SQLAlchemy :**
```python
class Salarie(db.Model):
    __tablename__ = '👷 Module 9: Salariés'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    poste = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(150))
    actif = db.Column(db.Integer, default=1)
```

### `planning`
Planning des interventions

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique |
| chantier_id | INTEGER | NULL | Référence vers `chantiers` |
| salarie_id | INTEGER | NULL | Référence vers `salaries` |
| date_debut | TEXT | NOT NULL | Date de début |
| date_fin | TEXT | NULL | Date de fin |
| description | TEXT | NULL | Description de l'intervention |
| statut | TEXT | DEFAULT 'Planifié' | Statut de l'intervention |

**Modèle SQLAlchemy :**
```python
class Planning(db.Model):
    __tablename__ = '📅 Module 8: Planning'
    
    id = db.Column(db.Integer, primary_key=True)
    chantier_id = db.Column(db.Integer, db.ForeignKey('🏗️ Module 3: Chantiers & Devis.id'))
    salarie_id = db.Column(db.Integer, db.ForeignKey('👷 Module 9: Salariés.id'))
    date_debut = db.Column(db.String(10), nullable=False)
    date_fin = db.Column(db.String(10))
    description = db.Column(db.Text)
    statut = db.Column(db.String(20), default='Planifié')
    
    # Relations
    chantier = db.relationship('🏗️ Module 3: Chantiers & Devis', backref='📅 Module 8: Planning')
    salarie = db.relationship('👷 Module 9: Salariés', backref='📅 Module 8: Planning')
```

---

## 🛠️ Tables Techniques (Calculs Ardoises)

### `ardoise`
Calculs ardoises de base

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique |
| longueur | REAL | NOT NULL | Longueur en mètres |
| largeur | REAL | NOT NULL | Largeur en mètres |
| surface | REAL | NOT NULL | Surface calculée |
| pente | REAL | NULL | Pente en degrés |
| type_ardoise | TEXT | NULL | Type d'📐 Module 10: Outils Ardoises |

### `ardoise_complet`
Calculs ardoises complets

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique |
| chantier_id | INTEGER | NULL | Référence vers `chantiers` |
| surface_totale | REAL | NOT NULL | Surface totale |
| nombre_ardoises | INTEGER | NOT NULL | Nombre d'📐 Module 10: Outils Ardoises calculé |
| marge_securite | REAL | DEFAULT 0.1 | Marge de sécurité (10%) |
| prix_unitaire | REAL | NULL | Prix unitaire |
| prix_total | REAL | NULL | Prix total calculé |

### `pente`
Calculs de pente

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique |
| hauteur | REAL | NOT NULL | Hauteur en mètres |
| longueur | REAL | NOT NULL | Longueur en mètres |
| angle_degres | REAL | NOT NULL | Angle en degrés |
| pourcentage | REAL | NOT NULL | Pente en pourcentage |

### `surface`
Calculs de surface

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique |
| longueur | REAL | NOT NULL | Longueur en mètres |
| largeur | REAL | NOT NULL | Largeur en mètres |
| surface_brute | REAL | NOT NULL | Surface brute |
| surface_nette | REAL | NOT NULL | Surface nette (avec déductions) |

### `materiau_ardoise`
Matériaux ardoises

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique |
| nom | TEXT | NOT NULL | Nom du matériau |
| type | TEXT | NOT NULL | Type d'📐 Module 10: Outils Ardoises |
| prix_unitaire | REAL | NOT NULL | Prix unitaire |
| unite | TEXT | DEFAULT 'm²' | Unité de mesure |

### `calcul_ardoise`
Résultats des calculs

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique |
| chantier_id | INTEGER | NULL | Référence vers `chantiers` |
| surface_totale | REAL | NOT NULL | Surface totale calculée |
| nombre_ardoises | INTEGER | NOT NULL | Nombre d'📐 Module 10: Outils Ardoises |
| prix_total | REAL | NOT NULL | Prix total |
| date_calcul | TEXT | NOT NULL | Date du calcul |

---

## 🔗 Relations et Contraintes

### Clés Étrangères
- `chantiers.etat_id` → `etats_chantier.id`
- `devis.chantier_id` → `chantiers.id`
- `planning.chantier_id` → `chantiers.id`
- `planning.salarie_id` → `salaries.id`
- `ardoise_complet.chantier_id` → `chantiers.id`
- `calcul_ardoise.chantier_id` → `chantiers.id`

### Index Recommandés
```sql
CREATE INDEX idx_chantiers_etat ON chantiers(etat_id);
CREATE INDEX idx_chantiers_reference ON chantiers(reference_chantier);
CREATE INDEX idx_devis_chantier ON devis(chantier_id);
CREATE INDEX idx_planning_chantier ON planning(chantier_id);
CREATE INDEX idx_planning_salarie ON planning(salarie_id);
CREATE INDEX idx_villes_code_postal ON villes(code_postal);
```

---

## 🎛️ Interface Flask-Admin

### Configuration
```python
# backend/admin_atarys.py
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app, name='ATARYS Admin', template_mode='bootstrap3')

# Vues par module
admin.add_view(ChantierView(name='🏗️ Module 3: Chantiers & Devis', endpoint='⚙️ Module 12: Paramètres_chantiers', category='🏗️ Module 3: Chantiers'))
admin.add_view(DevisView(name='🏗️ Module 3: Chantiers & Devis', endpoint='⚙️ Module 12: Paramètres_devis', category='🏗️ Module 3: Chantiers'))
admin.add_view(SalarieView(name='Salariés', endpoint='⚙️ Module 12: Paramètres_salaries', category='👥 Module 9: Salariés'))
admin.add_view(PlanningView(name='📅 Module 8: Planning', endpoint='⚙️ Module 12: Paramètres_planning', category='📅 Module 8: Planning'))
admin.add_view(VilleView(name='🌍 Module 11: Géographie', endpoint='⚙️ Module 12: Paramètres_villes', category='🌍 Module 11: Géographie'))
```

### Modules Disponibles dans Flask-Admin
- **🏗️ Module 3: Chantiers** - Chantiers, États, Devis
- **📅 Module 8: Planning** - Planning des interventions
- **👥 Module 9: Salariés** - Gestion des salariés
- **📐 Module 10: Outils** - Calculs ardoises (6 tables)
- **🌍 Module 11: Géographie** - Référentiel villes

### URL d'Accès
- **Interface Admin** : `http://localhost:5001/admin/`
- **Port** : 5001 (différent du serveur principal)
- **Mode** : Développement avec debug activé

---

## 📊 Statistiques Base de Données

- **Tables principales** : 23
- **Enregistrements** : 792+
- **Relations** : 6 clés étrangères
- **Index** : 6 index recommandés
- **Taille** : ~2.5 MB

---

## 📚 Organisation en Modules ATARYS

> **Note importante** : La base de données `atarys_data.db` est organisée selon la nomenclature officielle ATARYS en **13 modules principaux** (chapitres 1 à 13).

### Structure Modulaire
- **Chaque module** correspond à un chapitre de l'application ATARYS
- **Sous-modules** : Format X.Y (ex: 3.1, 3.2, etc.)
- **Tables groupées** par fonctionnalité métier
- **Cohérence** avec l'interface utilisateur et les workflows

### Modules Principaux
1. **PLANNING** - Planning et interventions
2. **LISTE DES TACHES** - Tâches personnalisées
3. **LISTE CHANTIERS** - Gestion des chantiers clients
4. **CHANTIERS** - Détails et documents chantiers
5. **DEVIS-FACTURATION** - Devis, factures, recouvrements
6. **ATELIER** - Stock, commandes, outillage
7. **GESTION** - Tableaux de bord et rapports
8. **COMPTABILITE** - Comptabilité et bilan
9. **SOCIAL** - Salariés, congés, formations
10. **OUTILS** - Calculs techniques (ardoises, etc.)
11. **ARCHIVES** - Archivage légal
12. **PARAMETRES** - Configuration système
13. **AIDE** - Documentation et support

### Avantages de cette Organisation
- **Navigation intuitive** dans l'interface
- **Séparation claire** des responsabilités
- **Évolutivité** : ajout facile de nouveaux modules
- **Maintenance** : isolation des problèmes par module
- **Formation** : apprentissage progressif par chapitre

> **Voir** `docs/02-architecture/ATARYS_MODULES.md` pour la nomenclature détaillée des modules.

---

**✅ Schéma technique complet de la base de données ATARYS avec architecture SQLAlchemy et Flask-Admin !** 