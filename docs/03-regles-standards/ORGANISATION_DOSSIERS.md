# 📁 Organisation des Dossiers ATARYS V2

> **Guide complet de l'organisation des dossiers et fichiers**  
> **Standards obligatoires** pour maintenir la cohérence du projet  
> Dernière mise à jour : 19/07/2025

---

## 🎯 **Vue d'Ensemble**

Cette documentation définit l'organisation stricte des dossiers dans ATARYS V2 pour maintenir la cohérence et faciliter la maintenance.

---

## 📁 **Structure Principale**

### **Racine du Projet** (`/`)
```
APP_ATARYS V2/
├── backend/           # Application Flask (Python)
├── frontend/          # Application React (JavaScript)
├── data/              # Base de données et données (PRINCIPAL)
├── docs/              # Documentation complète
├── logs/              # Fichiers de logs
├── scripts/           # Scripts utilitaires (racine)
└── .bat/              # Scripts batch Windows
```

---

## 🗄️ **Dossier `data/` - PRINCIPAL**

### **Emplacement** : `/data/` (racine du projet)
### **Usage** : Base de données et données de référence
### **Standard** : TOUJOURS utiliser ce dossier pour les données

#### **Contenu Standard**
```
data/
├── atarys_data.db           # Base SQLite principale ✅
├── atarys_data.db.backup    # Sauvegarde automatique ✅
├── import_csv/              # Données d'import CSV
│   ├── clients.csv
│   ├── chantiers.csv
│   └── ...
└── import_csv_interactive.py # Script d'import interactif
```

#### **Configuration Flask**
```python
# backend/app/__init__.py
db_uri = 'sqlite:///../../data/atarys_data.db'  # ✅ CORRECT
```

#### **Règles Strictes**
- ✅ **TOUJOURS** référencer `/data/` depuis la racine
- ✅ **TOUJOURS** utiliser ce dossier pour la base SQLite
- ✅ **JAMAIS** créer de base de données dans `/backend/`
- ✅ **JAMAIS** utiliser des chemins relatifs complexes

---

## 🔧 **Dossier `backend/` - Application Flask**

### **Emplacement** : `/backend/`
### **Usage** : Application backend Python/Flask

#### **Structure Standard**
```
backend/
├── app/                     # Application Flask
│   ├── models/             # Modèles SQLAlchemy
│   ├── routes/             # Routes API
│   ├── services/           # Services métier
│   ├── schemas/            # Validation Marshmallow
│   └── utils/              # Utilitaires
├── migrations/             # Migrations Alembic
├── requirements/           # Dépendances Python
├── scripts/               # Scripts backend
├── venv/                  # Environnement virtuel
├── instance/              # Configuration instance
├── app.py                 # Point d'entrée Flask
└── wsgi.py                # WSGI pour production
```

#### **Dossier `backend/data/` - À NETTOYER** ❌
```
backend/data/
└── onedrive_cache.json    # Cache temporaire (À DÉPLACER)
```

**Problème** : Ce dossier ne devrait pas exister selon les standards ATARYS
**Solution** : Déplacer vers `backend/cache/` ou supprimer

---

## 🎨 **Dossier `frontend/` - Application React**

### **Emplacement** : `/frontend/`
### **Usage** : Application frontend React/Vite

#### **Structure Standard**
```
frontend/
├── src/
│   ├── pages/             # Pages React (modules ATARYS)
│   ├── components/        # Composants réutilisables
│   ├── api/              # Services API
│   ├── contexts/         # Contextes React
│   ├── hooks/            # Hooks personnalisés
│   └── styles/           # Styles CSS
├── public/               # Assets statiques
├── package.json          # Dépendances Node.js
└── vite.config.js        # Configuration Vite
```

---

## 📚 **Dossier `docs/` - Documentation**

### **Emplacement** : `/docs/`
### **Usage** : Documentation complète du projet

#### **Structure Standard**
```
docs/
├── 01-guides-principaux/     # Guides principaux
├── 02-architecture/          # Architecture technique
├── 03-regles-standards/      # Standards et règles
├── 04-outils-templates/      # Outils et templates
├── 05-donnees-reference/     # Données de référence
└── README.md                 # Point d'entrée
```

---

## 📋 **Dossier `scripts/` - Utilitaires**

### **Emplacement** : `/scripts/` (racine)
### **Usage** : Scripts utilitaires généraux

#### **Contenu Standard**
```
scripts/
├── analyse_devis_historique.py    # Analyse des devis
├── requirements_analyse.txt        # Dépendances analyse
└── ...
```

---

## 🗂️ **Dossier `logs/` - Logs**

### **Emplacement** : `/logs/`
### **Usage** : Fichiers de logs de l'application

#### **Contenu Standard**
```
logs/
├── atarys.log              # Log principal
├── errors.log              # Log d'erreurs
└── access.log              # Log d'accès
```

---

## ⚠️ **Règles d'Or - Organisation**

### **✅ TOUJOURS FAIRE**

#### **1. Base de Données**
- ✅ **Utiliser** `/data/atarys_data.db` pour la base principale
- ✅ **Configurer** Flask avec `sqlite:///../../data/atarys_data.db`
- ✅ **Sauvegarder** dans `/data/` avec `.backup` extension

#### **2. Scripts Python**
- ✅ **Backend** → `backend/scripts/` (services, migrations)
- ✅ **Utilitaires** → `scripts/` (racine) (analyse, maintenance)
- ✅ **Tests** → `backend/tests/` ou `frontend/tests/`

#### **3. Documentation**
- ✅ **Tout document** → `docs/` avec structure appropriée
- ✅ **Standards** → `docs/03-regles-standards/`
- ✅ **Architecture** → `docs/02-architecture/`

#### **4. Services Backend**
- ✅ **Services métier** → `backend/app/services/`
- ✅ **Modèles** → `backend/app/models/`
- ✅ **Routes** → `backend/app/routes/`

### **❌ JAMAIS FAIRE**

#### **1. Base de Données**
- ❌ **Créer** des bases dans `/backend/`
- ❌ **Utiliser** des chemins relatifs complexes
- ❌ **Mélanger** bases de données et code

#### **2. Scripts**
- ❌ **Mettre** des scripts Python dans `/frontend/`
- ❌ **Mettre** des fichiers React dans `/backend/`
- ❌ **Créer** des fichiers à la racine (sauf configuration)

#### **3. Organisation**
- ❌ **Mélanger** backend et frontend dans le même dossier
- ❌ **Inventer** des structures non documentées
- ❌ **Ignorer** les standards ATARYS

---

## 🔧 **Corrections à Apporter**

### **1. Nettoyer `backend/data/`**
```bash
# Déplacer le cache vers un dossier approprié
mkdir backend/cache
mv backend/data/onedrive_cache.json backend/cache/
rmdir backend/data
```

### **2. Vérifier les Références**
```python
# Vérifier que toutes les références pointent vers /data/
# backend/app/__init__.py
db_uri = 'sqlite:///../../data/atarys_data.db'  # ✅ CORRECT
```

### **3. Standardiser les Scripts**
```bash
# Scripts backend → backend/scripts/
# Scripts utilitaires → scripts/ (racine)
# Scripts batch → .bat/
```

---

## 📊 **Vérification de Conformité**

### **Script de Vérification**
```python
# scripts/verifier_organisation.py
import os

def verifier_structure():
    """Vérifier la conformité de l'organisation"""
    
    # Vérifications obligatoires
    checks = [
        ("data/atarys_data.db", "Base de données principale"),
        ("backend/app/", "Application Flask"),
        ("frontend/src/", "Application React"),
        ("docs/", "Documentation"),
        ("logs/", "Logs"),
    ]
    
    for path, description in checks:
        if os.path.exists(path):
            print(f"✅ {description}: {path}")
        else:
            print(f"❌ {description}: {path} MANQUANT")
```

---

## 🎯 **Avantages de cette Organisation**

### **1. Cohérence**
- ✅ **Structure claire** et prévisible
- ✅ **Séparation** backend/frontend/données
- ✅ **Standards** uniformes

### **2. Maintenance**
- ✅ **Localisation facile** des fichiers
- ✅ **Backup simple** de `/data/`
- ✅ **Déploiement propre**

### **3. Évolutivité**
- ✅ **Ajout facile** de nouveaux modules
- ✅ **Intégration** de nouveaux services
- ✅ **Documentation** organisée

---

**✅ Organisation ATARYS V2 - Structure claire et maintenable !** 