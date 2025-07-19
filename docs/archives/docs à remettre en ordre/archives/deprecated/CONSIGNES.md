# 📋 Consignes de Développement ATARYS

> **Guide complet des standards et évolutions du projet ATARYS**  
> Dernière mise à jour : 22/06/2025

---

## 🎯 **État Actuel du Projet**

### **✅ Fonctionnalités Opérationnelles**
- **Backend Flask** : Architecture SQLAlchemy moderne avec middleware
- **Frontend React** : Interface Vite + Tailwind CSS optimisée
- **Base de données** : SQLite avec 792 enregistrements sur 13 tables
- **APIs REST** : Format JSON standardisé avec gestion d'erreurs
- **Calcul Ardoises** : Workflow complet fonctionnel
- **Planning Salariés** : Interface tableau optimisée
- **Documentation** : Architecture complète et règles métier

### **🚀 Serveurs de Développement**
```bash
# Backend (Port 5000)
cd backend
python run.py

# Frontend (Port 3000)
cd frontend
npm run dev
```

---

## 🏗️ **Architecture Établie**

### **Structure Backend Moderne**
```
backend/app/
├── routes/              # Blueprints API organisés
├── models/              # Modèles SQLAlchemy
├── services/            # Logique métier séparée
├── middleware/          # Logging + gestion erreurs
└── utils/               # Utilitaires (sécurité, validation)
```

### **Standards APIs**
- **Format de réponse** : `{"success": bool, "data": [], "message": str}`
- **Gestion erreurs** : Middleware centralisé avec logging
- **Compatibilité** : APIs maintenues compatibles ancien format
- **Pagination** : Support `per_page`, `page` pour grandes listes

### **Frontend Optimisé**
- **Layout System** : Composants réutilisables avec variants
- **Padding standard** : 16px (p-4) pour confort visuel
- **Grille flexible** : Colonnes 8/4, 7/5, 6/6 selon besoins
- **Responsive** : Adaptation menu ouvert/fermé

---

## 📁 **NOMENCLATURE COMPLÈTE DES DOSSIERS**

### **🗂️ Structure Racine du Projet**
```
0 APP ATARYS/
├── .bat/                    # Scripts Windows (batch + PowerShell)
├── backend/                 # API Python Flask
├── frontend/                # Application React
├── docs/                    # Documentation complète
├── data/                    # Données de référence (JSON, CSV)
├── logs/                    # Fichiers de logs application
├── .git/                    # Contrôle de version Git
└── fichiers de config       # .cursorrules, package.json, README.md
```

### **🐍 Structure Backend Python**
```
backend/
├── app/                     # Application Flask principale
│   ├── models/              # Modèles SQLAlchemy (base de données)
│   ├── routes/              # Endpoints API (blueprints Flask)
│   ├── services/            # Logique métier séparée
│   ├── middleware/          # Gestion erreurs + logging
│   ├── utils/               # Utilitaires (sécurité, validation)
│   └── config/              # Configuration par environnement
├── scripts/                 # Scripts Python utilitaires
│   ├── extraction_devis.py  # Moteur extraction Excel/CSV (173KB)
│   ├── extraction_devis_wrapper.py  # Wrapper API extraction
│   ├── copier_dossier.py    # Gestion dossiers OneDrive
│   ├── create_*.py          # Scripts création tables/données
│   └── collecte_*.py        # Scripts collecte/maintenance
├── tests/                   # Tests unitaires et intégration
│   ├── routes/              # Tests endpoints API
│   ├── models/              # Tests modèles de données
│   └── services/            # Tests logique métier
├── utils/                   # Utilitaires business ATARYS
│   ├── auto_fill_chantier.py  # Auto-remplissage chantiers
│   └── chantier_calculations.py  # Calculs métier
├── legacy/                  # Archives et anciens fichiers
├── venv/                    # Environnement virtuel Python
├── requirements/            # Dépendances par environnement
├── migrations/              # Migrations base de données
├── static/                  # Fichiers statiques (images, CSS)
└── logs/                    # Logs spécifiques backend
```

### **⚛️ Structure Frontend React**
```
frontend/
├── src/                     # Code source React
│   ├── pages/               # Pages selon modules ATARYS (1.1, 3.1, etc.)
│   │   ├── ListeChantiers.jsx    # Module 3.1 (95% fait)
│   │   ├── CalculArdoises.jsx    # Module 10.1 (100% fait)
│   │   ├── PlanningSalaries.jsx  # Module 1.1 (90% fait)
│   │   └── PlanningChantiers.jsx # Module 1.2 (90% fait)
│   ├── components/          # Composants réutilisables
│   │   ├── Layout.jsx       # Layout principal avec sidebar
│   │   ├── FormComponents.jsx  # Inputs, boutons standardisés
│   │   ├── Menu.jsx         # Menu navigation ATARYS
│   │   └── CSSGrid.jsx      # Système de grille responsive
│   ├── contexts/            # Context API React
│   │   └── MenuContext.jsx  # État global menu sidebar
│   ├── hooks/               # Hooks React personnalisés
│   │   └── useApi.js        # Hook pour appels API
│   ├── api/                 # Services API centralisés
│   │   ├── apiService.js    # Client HTTP Axios configuré
│   │   └── config.js        # Configuration URLs API
│   ├── assets/              # Images, logos, ressources
│   │   └── ATARYS_logo_BLACK.jpg
│   ├── data/                # Données statiques (backup)
│   │   └── villes.json      # Communes Bretagne (backup)
│   ├── styles/              # Styles CSS globaux
│   │   └── index.css        # Styles Tailwind + custom
│   └── services/            # Services métier (vide - à développer)
├── public/                  # Fichiers publics (favicon, manifest)
└── dist/                    # Build production (généré)
```

### **📚 Structure Documentation**
```
docs/
├── **Guides principaux**
│   ├── INDEX.md             # Navigation centrale documentation
│   ├── DEV_MASTER.md        # Document central - Vision globale
│   ├── CONSIGNES.md         # Standards et workflow (ce fichier)
│   └── CHECKLIST_DEVELOPPEMENT.md  # Checklist avant développement
├── **Architecture**
│   ├── ATARYS_ARCHITECTURE.md  # Architecture technique complète
│   ├── API_ENDPOINTS.md     # Documentation APIs REST
│   └── DATABASE_SCHEMA.md   # Structure base de données
├── **Métier**
│   ├── REGLES METIERS.md    # Règles business ATARYS
│   ├── NOMENCLATURE.txt     # Modules ATARYS (1.1 à 13.x)
│   └── WORKFLOWS.md         # Processus métier
├── **Technique**
│   ├── TESTING_GUIDE.md     # Guide tests unitaires
│   ├── DEPLOYMENT.md        # Guide déploiement
│   └── TEMPLATE_NOUVELLE_PAGE.md  # Template création pages
├── **Données de référence**
│   ├── Devis_DB/            # Exemples devis clients (26 fichiers)
│   ├── Fichiers excel/      # Fichiers Excel de référence
│   └── temp-docs/           # Documentation temporaire
└── **Archives**
    └── regles.md            # Anciennes règles (deprecated)
```

### **⚙️ Structure Scripts et Utilitaires**
```
.bat/                        # Scripts Windows (automatisation)
├── start_dev.bat            # Démarrage serveurs dev (backend + frontend)
├── stop_dev.bat             # Arrêt serveurs
├── restart_dev.bat          # Redémarrage serveurs
├── debug_dev.bat            # Mode debug développement
├── test_api.bat             # Tests endpoints API
├── notification_sound.ps1   # Notifications PowerShell
└── cleanup_copies.ps1       # Nettoyage fichiers temporaires

data/                        # Données de référence JSON
├── liste_salaries.json      # Données salariés (référence)
├── products.json            # Produits/matériaux
└── users.json               # Utilisateurs système

logs/                        # Logs application
├── atarys.log               # Log principal application
├── api.log                  # Logs spécifiques API
└── error.log                # Logs erreurs uniquement
```

### **🚨 Règles d'Organisation STRICTES**

#### **✅ AUTORISÉ**
- **Scripts Python** → `backend/scripts/` uniquement
- **Composants React** → `frontend/src/components/`
- **Pages React** → `frontend/src/pages/`
- **Documentation** → `docs/` (tous les .md)
- **Tests** → `backend/tests/` ou `frontend/tests/`
- **Config** → Racine (package.json, .cursorrules, etc.)

#### **❌ STRICTEMENT INTERDIT**
- **Fichiers Python dans frontend/** (contamination croisée)
- **Fichiers React dans backend/** (violation séparation)
- **Scripts à la racine** (pollution namespace)
- **Mélange backend/frontend** dans même dossier
- **Documentation éparpillée** (centraliser dans docs/)
- **Fichiers temporaires permanents** (nettoyage obligatoire)

#### **🎯 Workflow Création Fichiers**
1. **Identifier le type** : Script ? Composant ? Documentation ?
2. **Localiser le dossier** : Selon nomenclature ci-dessus
3. **Vérifier l'existant** : Éviter les doublons
4. **Respecter le nommage** : snake_case (Python), PascalCase (React)
5. **Mettre à jour docs** : INDEX.md si nécessaire

---

## 🎨 **Standards UI/UX Appliqués**

### **Layout Optimisé**
```jsx
// Utilisation pleine largeur
<PageLayout variant="full">
  <GridLayout columns="8-4" gap="standard">
    <GridColumn span={8}>
      <Card padding="standard">
        {/* Contenu principal */}
      </Card>
    </GridColumn>
  </GridLayout>
</PageLayout>
```

### **Améliorations Interface**
- **Planning Salariés** : Tableau agrandi (+20px hauteur, police plus lisible)
- **Calcul Ardoises** : Marges supprimées, utilisation maximale écran
- **Cards** : Padding confortable (16px), hover effects
- **Espacement** : Gap optimisé (gap-3) pour interface compacte

---

## 🔧 **Règles de Développement**

### **1. Respect de l'Architecture**
- **Nouveaux modules** : Suivre pattern Modèle → Service → Routes → Blueprint
- **Tests** : Utiliser template `backend/tests/routes/test_example_routes.py`
- **Documentation** : Maintenir `docs/INDEX.md` à jour

### **2. OneDrive et Stockage Cloud**
- **⚠️ CRITIQUES : Liens OneDrive RELATIFS uniquement**
- **Contexte** : Application en ligne multi-appareils (ordinateurs, tablettes)
- **OneDrive** : Base de stockage fichiers (PDF, AutoCAD, documents, photos)
- **Base de données** : Hébergée sur serveur (pas dans OneDrive)
- **Chemin interdits** : `C:\Users\`, chemins absolus Windows
- **Format requis** : Chemins relatifs compatibles multi-OS

### **3. Nettoyage Obligatoire**
- **Files de test** : Suppression automatique après usage
- **Files temporaires** : Nettoyage systématique des `test_*.py`, `debug_*.py`
- **Files inutiles** : Suppression scripts ponctuels après validation
- **Règle d'or** : Garder uniquement les fichiers nécessaires à l'application

### **4. Gestion Requirements**
- **⚠️ OBLIGATOIRE** : À chaque `pip install` pendant le développement
- **Mettre à jour** `backend/requirements/base.txt` immédiatement
- **Tester** l'installation depuis requirements avant commit
- **Versionner** les dépendances critiques (ex: `pandas>=1.5.0`)
- **Documenter** les nouvelles dépendances (commentaires dans requirements)

### **4. Standards de Code**
```python
# Backend - Nommage
- Fichiers : snake_case
- Classes : PascalCase  
- Variables : snake_case
- APIs : kebab-case (/api/calcul-ardoises)
```

```jsx
// Frontend - Nommage
- Composants : PascalCase (CalculArdoises.jsx)
- Fichiers : camelCase
- Variables : camelCase
```

### **3. Gestion Base de Données**
- **Modèles** : Correspondance exacte structure SQLite existante
- **Migrations** : Éviter modifications destructives
- **Requêtes** : Optimisation avec pagination

---

## 📊 **Fonctionnalités Métier**

### **Calcul des Ardoises**
- **Workflow** : Ville → Zone → Pente → Recouvrement → Modèles → Résultats
- **Conversion** : Pente automatique °/% bidirectionnelle
- **Validation** : Contrôles métier selon `docs/BUSINESS_RULES.md`

### **Planning Salariés**
- **Interface** : Tableau optimisé pleine largeur
- **Données** : Salariés actifs (date_sortie IS NULL)
- **Colonnes** : Dynamiques selon nombre salariés

### **APIs Opérationnelles**
- `/api/salaries` - Liste salariés (format array compatible)
- `/api/villes` - Communes Bretagne avec zones
- `/api/ardoises/*` - Workflow calcul complet
- `/api/planning` - Données planning

---

## 🛡️ **Sécurité & Qualité**

### **Outils Créés**
- **`backend/app/utils/security.py`** : Authentification, validation, rate limiting
- **Décorateurs** : `@require_api_key`, `@rate_limit`
- **Middleware** : Gestion centralisée erreurs + logging

### **Logging**
- **Fichier** : `logs/atarys.log`
- **Niveaux** : DEBUG en développement
- **Format** : Structuré avec timestamps et contexte

---

## 🚀 **Évolutions Récentes**

### **Optimisations Layout (22/06/2025)**
1. **Padding Cards** : Passage à 16px standard
2. **Grilles** : Nouveau système 8/4 colonnes
3. **Marges** : Suppression pour utilisation maximale écran
4. **Responsive** : Adaptation menu sidebar

### **Architecture Backend (22/06/2025)**
1. **Migration SQLAlchemy** : Remplacement ancien serveur
2. **Middleware** : Logging et gestion erreurs centralisés
3. **Services** : Séparation logique métier
4. **Tests** : Framework établi

### **Documentation (22/06/2025)**
1. **`docs/INDEX.md`** : Navigation centralisée
2. **`docs/ATARYS_ARCHITECTURE.md`** : Architecture complète
3. **`docs/BUSINESS_RULES.md`** : Règles métier détaillées

---

## 📝 **Workflow de Développement**

### **Ajout Nouvelle Fonctionnalité**
1. **Consulter** `docs/BUSINESS_RULES.md` pour règles métier
2. **Créer modèle** dans `backend/app/models/`
3. **Développer service** dans `backend/app/services/`
4. **Implémenter routes** dans `backend/app/routes/`
5. **Créer tests** dans `backend/tests/`
6. **Développer frontend** selon layout system
7. **Mettre à jour documentation**

### **Résolution Problèmes**
1. **Logs** : Consulter `logs/atarys.log`
2. **Base données** : Vérifier structure avec `analyze_real_db.py`
3. **APIs** : Tester endpoints avec format JSON standard
4. **Frontend** : Vérifier proxy Vite vers backend

---

## 🎯 **Prochaines Étapes Suggérées**

### **Documentation à Créer**
- [ ] `API_ENDPOINTS.md` - Documentation complète APIs
- [ ] `DATABASE_SCHEMA.md` - Schéma base de données
- [ ] `TESTING_GUIDE.md` - Stratégie de tests
- [ ] `DEPLOYMENT.md` - Guide déploiement

### **Améliorations Techniques**
- [ ] Tests unitaires complets
- [ ] CI/CD pipeline
- [ ] Monitoring production
- [ ] Optimisation performances

### **Fonctionnalités Métier**
- [ ] Gestion chantiers avancée
- [ ] Exports PDF/Excel
- [ ] Notifications système
- [ ] Historique modifications

---

## ⚠️ **Points d'Attention**

### **Compatibilité**
- **Maintenir** format APIs existant
- **Tester** rétrocompatibilité après modifications
- **Documenter** breaking changes

### **Performance**
- **Pagination** obligatoire pour listes > 100 items
- **Optimisation** requêtes SQLite
- **Cache** données statiques (villes, modèles)

### **Maintenance**
- **Backup** base données avant modifications
- **Logs** rotation automatique
- **Documentation** synchronisée avec code

---

*Ce fichier doit être mis à jour à chaque évolution majeure du projet.*