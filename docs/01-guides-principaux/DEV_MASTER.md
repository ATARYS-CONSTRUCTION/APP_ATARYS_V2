# 🚀 DEV_MASTER - Projet ATARYS V2

> **FICHIER CENTRAL DE DÉVELOPPEMENT**  
> Centralise toute l'information projet pour un développement efficace  
> **VERSION 2** : Architecture opérationnelle avec modules implémentés  
> Dernière mise à jour : 05/07/2025

---

## 📊 **ÉTAT ACTUEL DU PROJET V2 - BILAN COMPLET**

### **🎯 VISION GLOBALE & CONTEXTE ENTREPRISE**

**CONTEXTE ATARYS :**
Entreprise charpente-couverture-menuiserie de 10 personnes. Valeurs : technicité, polyvalence, qualité.
- **Julien (gérant)** : Diplômé master + charpentier, compétent mais submergé par le stress admin
- **Yann (conducteur de travaux)** : Grande expérience chantier, faible expérience informatique  
- **Équipe** : Apprécie l'ambiance et la qualité, mais inquiète de la désorganisation
- **Problèmes critiques** : Devis 3-6 mois de retard, chantiers mal organisés, pas de bénéfices

**OBJECTIF PRINCIPAL :**
**"Diminuer le stress du gérant par l'organisation automatisée"**

**Remplacer tous les fichiers Excel** par une application web moderne et structurée

### **🏗️ PROJET ATARYS V2 - ARCHITECTURE OPÉRATIONNELLE**

**✅ POURQUOI UNE V2 ?**
- **V1 "0 APP ATARYS"** : Développement erratique, architecture instable
- **Problèmes V1** : Code non structuré, pas de standards, développement chaotique
- **Décision** : Recommencer à zéro avec méthodologie rigoureuse
- **V2 "APP_ATARYS V2"** : Architecture solide, nomenclature officielle, standards stricts

**✅ AVANTAGES V2 :**
- **Architecture cohérente** : 13 modules ATARYS organisés
- **Standards de développement** : Méthodologie Cursor stricte
- **Documentation complète** : Chaque aspect documenté
- **Base solide** : Frontend React + Backend Flask structurés
- **Nomenclature officielle** : Modules 1.1 à 13.1 définis

### **📈 TAUX DE COMPLETION GLOBAL V2 : 45%**

**🚀 ÉTAT ACTUEL V2 (05/07/2025) :**

#### **✅ ÉLÉMENTS 100% OPÉRATIONNELS V2**
- **Frontend React** - Structure complète fonctionnelle (port 3000)
- **Backend Flask** - API REST opérationnelle (port 5000)
- **Base de données** - SQLite V2 avec 13 modèles SQLAlchemy créés
- **API REST** - Interface d'administration (port 5000)
- **Documentation** - Architecture complète et cohérente
- **Nomenclature** - 13 modules ATARYS avec sous-modules définis
- **Standards** - Méthodologie Cursor stricte + spécifications techniques
- **APIs REST** - Format standardisé `{success, data, message}`
- **Pattern BaseModel** - SQLAlchemy 2.0+ avec types standards

#### **✅ MODULES PARTIELLEMENT IMPLÉMENTÉS V2**
- **Module 5** - DEVIS_FACTURATION (EN COURS)
  - Modèle `FamilleOuvrages` créé
  - Structure SQLAlchemy définie
  - API à implémenter

- **Module 12** - PARAMÈTRES (EN COURS)
  - Tables de test : `TestAuditTable`, `TestCle2`
  - Relations avec clés étrangères
  - Interface de gestion des données
  - Service de création dynamique de tables

#### **🔄 MODULES EN COURS V2**
- **Module 1** - PLANNING (STRUCTURE CRÉÉE)
- **Module 10** - CALCULS (STRUCTURE CRÉÉE)
- **Modules 2-4, 6-9, 11, 13** - STRUCTURES CRÉÉES, MODÈLES À DÉFINIR

#### **📋 RÉFÉRENCE TECHNIQUE V1 CONSERVÉE**
- **Dossiers V1** - `0 APP ATARYS/` et `0 APP ATARYS - Copie/` pour référence
- **Scripts d'import** - Logique d'extraction Excel/CSV à adapter
- **Structure BDD** - Modèles SQLAlchemy comme base de réflexion
- **Configuration** - Paramètres techniques à reprendre

#### **🎯 À DÉVELOPPER EN V2**
- **Module 3.1** - LISTE CHANTIERS (priorité 1)

---

## 🌐 **Migration Hostinger 2025 (EXPÉRIMENTAL - En évaluation)**

### **📊 Changement Architectural Majeur :**
- **Stockage centralisé** : Fichiers entreprise sur serveur applicatif
- **Redirection automatique** : Liens OneDrive → Hostinger File Manager
- **Synchronisation continue** : rclone OneDrive → Serveur Linux

### **🎯 Impact Développement :**
- **Nouveau service** : `hostinger_path_mapper.py`
- **Endpoint modifié** : `/api/open-explorer` avec redirection intelligente
- **Fallback automatique** : OneDrive local si Hostinger indisponible
- **Tests requis** : Vérifier mapping caractères spéciaux

### **📋 À surveiller en développement :**
```python
# Vérifier mapping correct
./OneDrive/Comptabilité 2025 → /home/atarys/Comptabilite_2025
./OneDrive/Stavařina → /home/atarys/Stavarina

# Tester redirection
Clic "OneDrive" → Hostinger File Manager (navigateur)
Fallback → OneDrive local (explorateur)

# Monitoring synchronisation
rclone sync status quotidien
Logs erreurs dans backend
```

### **⚠️ Phase d'évaluation :**
- **Durée** : 3-6 mois (2025)
- **Rollback possible** : Retour OneDrive exclusif si échec
- **Documentation** : Retours d'expérience obligatoires
- **Module 9.1** - Liste Salariés (priorité 2)
- **Module 10.1** - Calcul Ardoises (priorité 3)
- **Modules additionnels** - Selon roadmap Phase 1-3

#### **🏗️ INFRASTRUCTURE V2 OPÉRATIONNELLE**
- **Architecture modulaire** : 13 modules définis avec sous-modules
- **Standards de code** : Règles Cursor appliquées
- **Documentation technique** : Architecture complète dans `docs/02-architecture/`
- **Spécifications** : API_ENDPOINTS.md, DATABASE_SCHEMA.md, ATARYS_MODULES.md
- **Environnement dev** : Frontend + Backend + Admin opérationnels

---

## 🏗️ **ARCHITECTURE V2 OPÉRATIONNELLE**

### **Stack Technologique**
- **Backend** : Flask 3.x + SQLAlchemy 2.0+ + Factory pattern
- **Frontend** : React 18.2.0 + Vite 5.4.19 + Tailwind CSS 3.4.1
- **Base de données** : SQLite avec BaseModel pattern
- **API** : REST format `{success, data, message}`
- **Admin** : API REST sur port 5000
- **Validation** : Marshmallow pour intégrité des données

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
└── atarys_data.db     # Base SQLite V2 (structure complète)
```

### **Fonctionnalités Avancées Implémentées**
- **Création Dynamique de Tables** : Interface utilisateur intuitive
- **Import Excel Intelligent** : Collage direct depuis Excel
- **Logique UPSERT** : Création/mise à jour automatique
- **Compteur de Lignes** : Affichage dynamique en temps réel
- **Validation Marshmallow** : Intégrité des données
- **Communication CORS** : Frontend-backend configuré

---

## 📋 **PROJET ATARYS - VISION 3 PHASES**

### **📍 PHASE 1 : REMPLACEMENT EXCEL** (Mi-octobre 2025)
**Objectif :** Remplacer totalement les 2 fichiers Excel de gestion

**OBJECTIFS DÉTAILLÉS PHASE 1 :**
- ✅ **Automatiser** des tâches informatiques récurrentes et indispensables
- ✅ **Remplacer** tous les fichiers Excel par une application qui archive, calcule et organise
- ✅ **Créer** des process de travail efficaces et ludiques sur les tâches rébarbatives
- ✅ **Organiser** le travail du bureau en binôme
- ✅ **Renforcer** la protection juridique de l'entreprise
- ✅ **Réduire** le niveau de stress par une meilleure maîtrise des délais
- ✅ **Augmenter** le temps de présence sur les chantiers
- ✅ **Augmenter** la rentabilité par une meilleure organisation

**FICHIER "Atarys 2025.xlsx" (10 onglets) À REMPLACER :**
- 🔄 **Articles ATARYS** → Module 5.1 (STRUCTURE CRÉÉE - données à importer)
- 🔄 **LISTE DES TACHES** → Module 3.1 Liste Chantiers (EN COURS)
- 🔄 **PrévisionneL** → Module 7.1 Tableaux de bord financiers
- 🔄 **Synthèse Prévisionnel** → Module 7.2 KPIs temps réel  
- 🔄 **Tableau de bord** → Dashboard principal
- 🔄 **Bilan chantier** → Reporting chantiers
- 🔄 **VENTE** → Suivi commercial intégré

**FICHIER "📅 Module 8: Planning Atarys 2025 3.xlsm" (7 onglets) À REMPLACER :**
- ✅ **Liste_Salariés** → Module 9.1 (EN COURS)
- 🔄 **Liste_Chantiers** → Module 3.1 (EN COURS)
- 🔄 **Planning_2025** → Module 1.1/1.2 Planning équipes
- 🔄 **Fiche_Mensuelle** → Module 9.2 Suivi RH mensuel
- ✅ **Base_Villes** → Table villes (FAIT 100%)

### **📍 PHASE 2 : LOGICIEL DEVIS-FACTURATION COMPLET** (2026)
**Objectif :** Créer un logiciel de devis-facturation moderne pour remplacer BATAPPLI
**🎯 FOCUS :** Application métier complète avec fonctionnalités avancées

**OBJECTIFS DÉTAILLÉS PHASE 2 :**
- ✅ **Remplacer BATAPPLI** par application interne moderne
- ✅ **Faciliter l'élaboration** de devis complexes multi-corps d'état
- ✅ **Intégrer LISP AutoCAD** pour le calcul des métrés automatique
- ✅ **Reprendre la base BATAPPLI** mais augmentée de fonctions intelligentes

**AVANTAGES vs BATAPPLI ACTUEL :**
- 🔗 **Intégration totale** : Connexion Phase 1 (chantiers ↔ devis ↔ planning)
- 🧮 **LISP AutoCAD** : Calculs métrés automatiques
- 💰 **Comptabilité intégrée** : Fini les doubles saisies manuelles
- 📦 **Commandes intelligentes** : Matériaux commandés automatiquement
- 📊 **Templates métier** : Devis complexes pré-configurés

### **📍 PHASE 3 : IA AUTOMATISATION** (2027)
**Objectif :** IA efficace avec accès au code
- Analyse données accumulées (Phases 1+2)
- Automatisation tâches définies par usage
- Auto-amélioration du système  
- Prédictions et optimisations métier

---

## 🚀 **PLAN IMMÉDIAT - PHASE 1**

### **✅ PRIORITÉ 1 : BACKEND V2** (TERMINÉ)
**Objectif :** Créer l'API REST Flask selon spécifications d'architecture
- ✅ Architecture V2 définie (FAIT)
- ✅ Standards de développement (FAIT - SQLAlchemy 2.0+ + BaseModel pattern)
- ✅ Spécifications techniques (FAIT)
- ✅ Structure backend Flask avec Factory pattern (FAIT)
- ✅ Implémenter BaseModel et configuration SQLAlchemy (FAIT)
- ✅ APIs REST pour modules prioritaires (FAIT - Module 5.1)

### **✅ PRIORITÉ 2 : BASE DE DONNÉES V2** (TERMINÉ)
**Objectif :** Créer une base de données propre à partir de fichiers Excel à jour
- ✅ Approche : Repartir à zéro avec données propres et à jour (FAIT)
- ✅ Source : Fichier Excel propre préparé par l'utilisateur (FAIT)
- ✅ Standards V2 : SQLAlchemy 2.0+ avec `db.Numeric(10, 2)` pour montants (FAIT)
- ✅ Scripts d'import : Créer outils d'import Excel → SQLite V2 (FAIT)
- ✅ Base SQLite V2 selon modules ATARYS prioritaires (FAIT - structure complète)

### **🔄 PRIORITÉ 3 : DÉVELOPPER MODULE 3.1** (EN COURS)
**Remplace :** "LISTE DES TACHES" + "Liste_Chantiers"
- ✅ Référence V1 pour logique métier (FAIT)
- 🔄 Modèles SQLAlchemy avec BaseModel pattern (EN COURS)
- 🔄 Interface utilisateur React selon standards (EN COURS)
- 🔄 Connexion API frontend ↔ backend (EN COURS)
- 🔄 Tests et validation complète (À FAIRE)

### **🔄 PRIORITÉ 4 : MODULES ADDITIONNELS V2** (EN COURS)
**Objectif :** Développer les modules selon roadmap Phase 1-3
- **Module 9.1** : Liste Salariés (EN COURS)
- **Module 10.1** : Calcul Ardoises (EN COURS)
- **Modules 1.1/1.2** : Planning (À FAIRE)
- **Modules 7.1/7.2** : Gestion (À FAIRE)
- **Organisation** : Selon nomenclature officielle `ATARYS_MODULES.md`

### **📊 PRIORITÉ 5 : TABLEAUX DE BORD ET SYNTHÈSES** (3-4 semaines)
**Remplace :** "Synthèse Prévisionnel" + "Tableau de bord"
- KPIs temps réel
- Graphiques évolution  
- Alertes automatiques
- Interfaces de pilotage

---

## 🔄 **BILAN V1 → V2 : SUCCÈS DE LA MIGRATION**

### **🚨 PROBLÈMES V1 "0 APP ATARYS"**
- **Développement erratique** : Code écrit sans méthodologie
- **Architecture instable** : Pas de standards, refactoring constant
- **Documentation inexistante** : Difficile de s'y retrouver
- **Nommage incohérent** : Pas de nomenclature officielle
- **Code spaghetti** : Mélange frontend/backend, pas de séparation
- **Stress développement** : Régressions constantes, bugs récurrents

### **✅ AVANTAGES V2 "APP_ATARYS V2"**
- **Méthodologie Cursor** : Règles strictes appliquées systématiquement
- **Architecture cohérente** : Frontend + Backend + Admin opérationnels
- **Documentation complète** : Chaque aspect documenté
- **Standards techniques** : BaseModel, SQLAlchemy 2.0+, Factory pattern
- **Fonctionnalités avancées** : Création dynamique, import Excel, UPSERT
- **Performance** : < 100ms response time, architecture optimisée

---

## 📚 **DOCUMENTATION TECHNIQUE V2**

### **Architecture**
- **[ATARYS_ARCHITECTURE.md](../02-architecture/ATARYS_ARCHITECTURE.md)** - Architecture complète V2
- **[ARCHITECTURE_SYNTHESE_V2.md](../02-architecture/ARCHITECTURE_SYNTHESE_V2.md)** - Synthèse complète
- **[API_ENDPOINTS.md](../02-architecture/API_ENDPOINTS.md)** - APIs REST implémentées
- **[DATABASE_SCHEMA.md](../02-architecture/DATABASE_SCHEMA.md)** - Structure base de données
- **[ATARYS_MODULES.md](../02-architecture/ATARYS_MODULES.md)** - Organisation modulaire

### **Développement**
- **[WORKFLOWS.md](../03-regles-standards/WORKFLOWS.md)** - Processus de développement
- **[STANDARDS_DEV.md](../03-regles-standards/STANDARDS_DEV.md)** - Standards techniques
- **[ERREURS_IMPLANTATION_DONNEES.md](../03-regles-standards/ERREURS_IMPLANTATION_DONNEES.md)** - Gestion d'erreurs

### **Guides**
- **[QUICK_START.md](QUICK_START.md)** - Guide de démarrage rapide
- **[CHECKLIST_DEVELOPPEMENT.md](../04-outils-templates/CHECKLIST_DEVELOPPEMENT.md)** - Checklist développement

---

## 🚀 **ENVIRONNEMENT DE DÉVELOPPEMENT**

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

**✅ PROJET ATARYS V2 - Architecture opérationnelle, développement efficace !**

### **🎨 Frontend V2**

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
- **Compteur de lignes** : Affichage dynamique en temps réel
- **Boutons d'action** : Ajouter ligne, créer table
- **Gestion d'erreurs** : Messages explicites
- **Responsive** : Adaptation mobile/desktop

### **🎯 BONNES PRATIQUES TABLEAUX ATARYS**

#### **Interactions Utilisateur**
- **Simple clic** : Sélection de la ligne (highlight)
- **Double clic** : Ouverture du formulaire de modification
- **Boutons d'action** : Modifier, Supprimer, Actions spéciales
- **Feedback visuel** : Ligne sélectionnée avec bordure colorée

#### **Structure Tableau Standard**
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

#### **Gestion des Relations**
- **Affichage des relations** : Utiliser `find()` pour récupérer les libellés
- **Exemple** : `niveauQualifications.find(q => q.id === salary.niveau_qualification_id)?.niveau`
- **Fallback** : Toujours prévoir un fallback `|| '-'` pour les valeurs nulles

#### **Formulaires de Modification**
- **Champs obligatoires** : Validation côté frontend ET backend
- **Sélection multiple** : Utiliser `multiple` et `size` pour les listes
- **Instructions utilisateur** : Textes d'aide pour les interactions complexes
