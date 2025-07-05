#  DEV_MASTER - Projet ATARYS 2025

> **FICHIER CENTRAL DE DÉVELOPPEMENT**  
> Centralise toute l'information projet pour un développement efficace  
> Objectif : Application opérationnelle pour septembre 2025  
> Dernière mise à jour : 30/06/2025

---

##  **ÉTAT ACTUEL DU PROJET - BILAN COMPLET**

### ** VISION GLOBALE & CONTEXTE ENTREPRISE**

**CONTEXTE ATARYS :**
Entreprise charpente-couverture-menuiserie de 10 personnes. Valeurs : technicité, polyvalence, qualité.
- **Julien (gérant)** : Diplômé master + charpentier, compétent mais submergé par le stress admin
- **Yann (conducteur de travaux)** : Grande expérience chantier, faible expérience informatique  
- **Équipe** : Apprécie l'ambiance et la qualité, mais inquiète de la désorganisation
- **Problèmes critiques** : Devis 3-6 mois de retard, chantiers mal organisés, pas de bénéfices

**OBJECTIF PRINCIPAL :**
**"Diminuer le stress du gérant par l'organisation automatisée"**

**Remplacer tous les fichiers Excel** par une application web qui :
- **PRIORITÉ 1** : Devis en 30min au lieu de 3h (extraction automatique)
- **PRIORITÉ 2** : Organisation chantiers automatisée (matériaux, suivi)
- **PRIORITÉ 3** : Interface ultra-simple pour Yann (novice informatique)
- **RÉSULTAT** : Équipe rassurée, gérant serein, rentabilité retrouvée

### ** TAUX DE COMPLETION GLOBAL : 65%**

#### ** MODULES 100% OPÉRATIONNELS**
- **Module 9.1** - Liste Salariés (197 lignes, 7.5KB)
- **Module 10.1** - Calcul Ardoises (373 lignes, 12KB) 
- **Architecture Backend** - Flask + SQLAlchemy + 13 tables
- **Base de données** - 792 enregistrements, 332 communes Bretagne

#### ** MODULES 80-95% OPÉRATIONNELS**
- **Module 3.1** - Liste Chantiers (1227 lignes, 49KB) - **ARCHITECTURE MIGREE, FONCTIONNALITÉS À TERMINER**
- **Module 1.1** - Planning Salariés (307 lignes, 10KB)
- **Module 1.2** - Planning Chantiers (328 lignes, 11KB)
- **Extraction Devis** - Excel → Base automatique (318 lignes)

---

##  **PROJET ATARYS - VISION 3 PHASES**

### **📍 PHASE 1 : REMPLACEMENT EXCEL** (Mi-octobre 2025)
**Objectif :** Remplacer totalement les 2 fichiers Excel de gestion

**OBJECTIFS DÉTAILLÉS PHASE 1 :**
- ✅ **Automatiser** des tâches informatiques récurrentes et indispensables
- ✅ **Remplacer** tous les fichiers Excel par une application qui archive, calcule et organise
- ✅ **Créer** des process de travail efficaces et ludiques sur les tâches rébarbatives (devis, facturation, planning, commandes, compta) pour se concentrer sur les tâches intéressantes (conception technique, organisation, formation, fabrication)
- ✅ **Organiser** le travail du bureau en binôme
- ✅ **Renforcer** la protection juridique de l'entreprise (process administratif mieux maîtrisés)
- ✅ **Réduire** le niveau de stress par une meilleure maîtrise des délais
- ✅ **Augmenter** le temps de présence sur les chantiers (ambitieux)
- ✅ **Augmenter** la rentabilité par une meilleure organisation

**FICHIER "Atarys 2025.xlsx" (10 onglets) À REMPLACER :**
- 🔄 **LISTE DES TACHES** → Module 3.1 Liste Chantiers (95% fait - Architecture migrée)
- 🔄 **PrévisionneL** → Module 7.1 Tableaux de bord financiers
- 🔄 **Synthèse Prévisionnel** → Module 7.2 KPIs temps réel  
- 🔄 **Tableau de bord** → Dashboard principal
- 🔄 **Bilan chantier** → Reporting chantiers
- 🔄 **VENTE** → Suivi commercial intégré

**FICHIER "📅 Module 8: Planning Atarys 2025 3.xlsm" (7 onglets) À REMPLACER :**
- ✅ **Liste_Salariés** → Module 9.1 (FAIT 100%)
- 🔄 **Liste_Chantiers** → Module 3.1 (95% fait - Architecture migrée)
- 🔄 **Planning_2025** → Module 1.1/1.2 Planning équipes
- 🔄 **Fiche_Mensuelle** → Module 9.2 Suivi RH mensuel
- ✅ **Base_Villes** → Table villes (FAIT 100%)

### **📍 PHASE 2 : LOGICIEL DEVIS-FACTURATION COMPLET** (2026)
**Objectif :** Créer un logiciel de devis-facturation moderne pour remplacer BATAPPLI
**🎯 FOCUS :** Application métier complète avec fonctionnalités avancées

**OBJECTIFS DÉTAILLÉS PHASE 2 :**
- ✅ **Remplacer BATAPPLI** par application interne moderne (faciliter les connexions)
- ✅ **Faciliter l'élaboration** de devis complexes multi-corps d'état
- ✅ **Intégrer LISP AutoCAD** pour le calcul des métrés automatique depuis plans
- ✅ **Reprendre la base BATAPPLI** mais augmentée de fonctions intelligentes :
  - Comptabilité intégrée (fini les double-saisies)
  - Commandes de matériaux automatisées depuis devis
  - Planification chantiers automatique depuis devis  
- ✅ **Connexion totale Phase 1** : Devis ↔ Chantiers ↔ Planning synchronisés

**AVANTAGES vs BATAPPLI ACTUEL :**
- 🔗 **Intégration totale** : Connexion Phase 1 (chantiers ↔ devis ↔ planning)
- 🧮 **LISP AutoCAD** : Calculs métrés automatiques (fini les erreurs manuelles)
- 💰 **Comptabilité intégrée** : Fini les doubles saisies manuelles
- 📦 **Commandes intelligentes** : Matériaux commandés automatiquement depuis devis
- 📊 **Templates métier** : Devis complexes pré-configurés selon types de chantiers

**MODULES TECHNIQUES PHASE 2 :**
- Module 5.1 : Articles et ouvrages BATAPPLI (base de données complète)
- Module 5.2 : Fiche mètres + LISP AutoCAD (calculs automatiques)
- Module 5.3 : Devis MEXT avancés (90% fait - extraction Excel)
- Module 5.4 : Templates devis + devis complexes multi-corps d'état
- Module 5.5 : Connexions comptabilité (remplace saisies manuelles)
- Module 5.6 : Commandes matériaux automatiques (intégration fournisseurs)
- Module 6.x : Facturation complète intégrée (workflow complet)

### **📍 PHASE 3 : IA AUTOMATISATION** (2027)
**Objectif :** IA efficace avec accès au code
- Analyse données accumulées (Phases 1+2)
- Automatisation tâches définies par usage
- Auto-amélioration du système  
- Prédictions et optimisations métier

---

##  **PLAN IMMÉDIAT - PHASE 1**

### ** PRIORITÉ 1 : FINIR MODULE 3.1** (EN COURS)
**Remplace :** "LISTE DES TACHES" + "Liste_Chantiers"
- ✅ Workflow insertion devis (FAIT)
- ✅ Remplissage automatique (FAIT)
- ✅ Architecture SQLAlchemy unifiée (FAIT)
- 🔄 Finaliser toutes les fonctionnalités manquantes
- 🔄 Tests finaux et validation complète

### ** PRIORITÉ 2 : DÉVELOPPER LES 10 CHAPITRES ATARYS** (Long terme)
**Objectif :** Construire les fondations complètes de l'application
- **Modules 1-2** : Planning et Listes de tâches  
- **Modules 3-4** : Chantiers (3.2 à 3.5 + 4.1 à 4.4)
- **Modules 6-8** : Atelier, Gestion, Comptabilité
- **Modules 11-12** : Archives et Paramètres

### ** PRIORITÉ 3 : TABLEAUX DE BORD ET SYNTHÈSES** (3-4 semaines)
**Remplace :** "Synthèse Prévisionnel" + "Tableau de bord"
- KPIs temps réel
- Graphiques évolution  
- Alertes automatiques
- Interfaces de pilotage

**💡 REMARQUE SECONDAIRE :** Interface simplifiée pour Yann (gros boutons, workflow guidé) sera intégrée naturellement dans chaque module développé.

---

##  **MÉTRIQUES PROGRESSION 3 PHASES**

### **📊 PHASE 1 - REMPLACEMENT EXCEL (Mi-octobre 2025)**
**Objectif :** 17 onglets Excel → 0 (100% remplacés)

**MODULES PHASE 1 :**
- [x] **9.1** Liste Salariés → Remplace "Liste_Salariés" ✅
- [x] **10.1** Calcul Ardoises → Outils techniques ✅  
- [x] **Base Villes** → Remplace "Base_Villes" ✅
- [ ] **3.1** Liste Chantiers → Remplace "LISTE DES TACHES" + "Liste_Chantiers" (95%)
- [ ] **1.1/1.2** Planning → Remplace "📅 Module 8: Planning_2025" (90%)
- [ ] **7.1/7.2** Tableaux de bord → Remplace "Synthèse" + "Tableau de bord" (0%)
- [ ] **Mode Yann** → Interface simplifiée pour conducteur (0%)

**PROGRESSION PHASE 1 : 3/7 = 43%**

### **📊 PHASE 2 - LOGICIEL DEVIS-FACTURATION COMPLET (2026)**  
**Objectif :** Créer un logiciel de devis-facturation moderne pour remplacer BATAPPLI
**🎯 FOCUS :** Application métier complète avec fonctionnalités avancées

**MODULES PHASE 2 :**
- [ ] **5.1** Base données BATAPPLI (articles/ouvrages) → 0%
- [ ] **5.2** FICHE METRES + LISP AutoCAD (calculs métrés automatiques) → 0%
- [x] **5.3** DEVIS MEXT (extraction Excel) → 90% ✅
- [ ] **5.4** DEVIS COMPLEXES (templates avancés, multi-corps d'état) → 0%
- [ ] **5.5** CONNEXIONS COMPTABILITÉ (intégration comptable) → 0%
- [ ] **5.6** COMMANDES MATÉRIAUX (automatisation fournisseurs) → 0%
- [ ] **6.x** FACTURATION INTÉGRÉE (gestion complète) → 0%

**AVANTAGES vs BATAPPLI ACTUEL :**
- 🔗 **Intégration totale** : Connexion Phase 1 (chantiers ↔ devis ↔ planning)
- 🧮 **LISP AutoCAD** : Calculs métrés automatiques depuis plans
- 💰 **Comptabilité native** : Fini les double-saisies
- 📦 **Commandes intelligentes** : Matériaux commandés automatiquement
- 🎨 **Templates métier** : Devis complexes pré-configurés

**PROGRESSION PHASE 2 : 1/7 modules = 14%**

### **📊 PHASE 3 - IA AUTOMATISATION (2027)**
**Objectif :** IA efficace avec accès code
**PROGRESSION PHASE 3 : 0/X = 0%** (Phase future)

---

### **🎯 CRITÈRES DE RÉUSSITE PHASE 1 (Mi-octobre)**
- ✅ **Excel fermés définitivement** : 17 onglets → 0
- ✅ **Gérant serein** : Stress admin réduit de 50%  
- ✅ **Interface Yann** : Novice informatique autonome
- ✅ **Équipe rassurée** : Organisation professionnelle visible

**ÉTAT GLOBAL PROJET : 3/7 modules = 43%**  
**OBJECTIF MI-OCTOBRE : 7/7 modules = 100%** (Phase 1 terminée)

---

## 📋 **NOMENCLATURE COMPLÈTE ATARYS - 13 MODULES**

### **1. PLANNING**
- **1.1** PLANNING SALARIÉS → ✅ 90% (Interface opérationnelle)
- **1.2** PLANNING CHANTIER → ✅ 90% (Gestion projets par dates)

### **2. LISTE DES TACHES**
- **2.1** YANN → 🔄 En développement (Liste personnalisée)
- **2.2** JULIEN → 🔄 En développement (Liste personnalisée)

### **3. LISTE CHANTIERS** ⭐ PRIORITÉ 1

**CONSTAT :**
Aujourd'hui, batappli ne permet pas de vision clair des ventes, du nombre d'heures à faire, du planning. Les chantiers sont organisés individuellement un fichier excel nommés Notes de chantiers.xls. Il est présent dans chaque dossier (voir modèle dans docs/fichiers excel). "C:\DEV\0 APP ATARYS\docs\Fichiers excel\NOTES DE CHANTIER1.xlsx". Il faut centraliser manuellement en calculant le nombre d'heures depuis batappli (exprimé en jours), rentrer le déboursé et ensuite intégrer toutes les factures fournisseurs, les factures d'acompte, factures d'avancement et factures. Il y a souvent des oublis. Pour calculer le nombre d'heures réelles on se fie à un nomenclature calculé sur le planning. Il a été récemment amélioré avec chatgpt mais est très rébarbatif et sujet aux oublis ou erreur de calcul. Il faut changer par exemple à chaque fois le nombre d'heures.

**OBJECTIF :**
Le chapitre LISTE_CHANTIERS permet de visualiser les chantiers. Il sert à créer et mettre à jour les chantiers à partir de toutes les données s'y référant: devis, factures, commandes de matériaux, temps de travail, informations, liens, description, calcul détaillé par familles d'ouvrage. Il est constitué de 5 pages , la première 3.1 est généraliste et présente l'ensemble des chantiers en projet ou signés. Il permet d'afficher et de tenir à jour les informations essentielles du chantier.

**ACTION :**
Créer 5 pages avec la même interface mais qui affiche différentes données. Se référer aux bases de données existantes et à la nomenclature, demander des précisions sur l'objectif de chaque pages

**RÉSULTAT :**
Une interface facile à maintenir qui reçoit des informations de l'ensemble des pages (planning pour calculer les heures réelles, social pour intégrer les salaires payés, liste des taches pour avoir un suivi) et envoie des informations vers les autres pages

---

#### **3.1 LISTE CHANTIERS** ⭐ PRIORITÉ IMMÉDIATE

**CONSTAT MODULE 3.1 :**
Fiche récap avec bilan de chantier et liste des tâches en visuel. Il contient les infos essentielles, la page actuelle est quasi correcte mais il y a des modifs à faire.

**FINIR LA PAGE LISTECHANTIERS.JSX :**

**🔗 MISE EN COHÉRENCE BASE DE DONNÉES**
- Mise en cohérence de la base de données entre devis et chantiers

**🧮 CALCUL (Montant HT total)**
- Pour le montant Ht total de la chantiers, appliquer la même logique que pour le nombre d'heures
- Chaque ligne dans la table devis a un montant Ht (colonne 16). Dans le frontend, le montant HT d'un chantier est l'addition de un ou plusieurs devis, elle peut aussi être rentrée manuellement


**📝 DESCRIPTION (Extraction devis)**
- La description affiche dans par défaut le ou les numéros du devis et leur titres
- Affiner la description: il faut améliorer les scripts sur extraction devis et rechercher un titre du devis qui se trouve au dessus de la ligne des devis contenant référence, libellé,... Attention cette ligne n'est pas fixe
- Il faut créer une colonne titre du devis dans la table devis. Fais un premier test pour voir ce que tu peux trouver dans les devis de C:\Users\Dell15\OneDrive\Organisation ATARYS\1 APP ATARYS\3 LISTE CHANTIERS\Devis_DB.

**🏷️ STATUT/ÉTAT (Gestion des états)**
- Remplacer la colonne statut par État et afficher une liste déroulante sur les etat_chantier. Cette liste est modifiable dans le tableau principal de la page listechantiers.jsx

**👁️ AFFICHAGE (Interface utilisateur)**
- Réduire la taille de la colonne date de création
- Les cases à cocher doivent être conservées pour sélection multiple mais il faut changer le mode de sélection
- Affichage de l'ordre des chantiers, possibilité de choisir par nom ou référence (alphabétique), par date de création, par état. Par défaut, les chantiers sont affichés par état

**➕ CRÉER (Workflow création)**
- Supprimer le bouton créer à partir d'un devis dans la fenêtre créer un devis
- IL FAUT d'abord créer le chantier puis y insérer un devis. Cela sera beaucoup plus clair
- Ne modifie pas de scripts qui auraient des effets sur insertion devis qui doit rester en place

**✏️ MODIFIER (Fonctionnalités)**
- Dans le frontend, liste_chantiers, si on double clic sur une ligne corerspondant à un chantier, la fenêtre modifier un chantier s'ouvre
- Modifier le bouton Modifier (ne pas ajouter insérer un devis)
- Modifier le déclenchement de la fonction insérer un devis, on ouvre le fichier, on execute le script et les données sont insérées dans la fenêtre. Le bouton du bas mettre à jour chantier valide l'ensemble.

**📁 ONEDRIVE (Intégration dossiers)**
- Dans listechantiers.jsx, il faut ajouter une colonne dans le tableau qui est lien onedrive. Créer une route
- Cette colonne est liée à la colonne 14 de la base de données table chantier. Se référer à la documentation
- Dans la fenetre de création d'un chantier, ajouter deux boutons en dessous de l'item onedrive (des petits boutons ou clic). Le premier permet d'assigner un dossier onedrive existant (ouverture d'une fenetre windows), Le deuxième permet de créer un dossier grace au script copier_dossier.py. Le dossier s'intitulera AAAA-MM (automatique selon la date de création du dossier) puis espace puis la référence du chantier (selon base de données ou l'item Référence qui devra être rempli préalablement sans validation)

**💾 DONNÉES EXISTANTES**
- Insérer les données existatnes dans la base de données. Vérifier l'extraction de devis

---

**MODULES RESTANTS :**
- **3.2** CHANTIERS PROJETS → 🔄 À créer (Filtrage état "🏗️ Module 3: Chantiers & Devis")
- **3.3** CHANTIERS SIGNÉS → 🔄 À créer (Filtrage état "Signé")
- **3.4** CHANTIERS EN COURS → 🔄 À créer (Filtrage état "En cours")
- **3.5** CHANTIERS ARCHIVES → 🔄 À créer (Filtrage état "Terminé")

### **4. CHANTIERS**
- **4.1** SUIVI DE CHANTIER → 🔄 Backend prêt, Frontend à créer
- **4.2** NOTES DE CHANTIER → 🔄 Concept défini
- **4.3** COMMANDES → 🔄 En réflexion
- **4.4** DOCUMENTS → 🔄 Intégration OneDrive prévue

### **5. DEVIS-FACTURATION** ⭐ PRIORITÉ 2
- **5.1** Ouvrages et articles BATAPPLI → 🔄 Structure prête
- **5.2** FICHE METRES → 🔄 + LISP AutoCAD (calculs métrés)
- **5.3** DEVIS MEXT → ✅ 90% (Extraction Excel opérationnelle)
- **5.4** DEVIS TYPE → 🔄 Templates et devis complexes

### **6. ATELIER**
- **6.1** QUINCAILLERIE → 🔄 Base de données à créer
- **6.2** CONSOMMABLES → 🔄 Gestion stocks
- **6.3** CAMION → 🔄 Suivi véhicules
- **6.4** MATERIEL → 🔄 Inventaire
- **6.5** ECHAFAUDAGE → 🔄 Sécurité équipements

### **7. GESTION** ⭐ PRIORITÉ 3
- **7.1** PREVISIONNEL → 🔄 Budgets et forecasts
- **7.2** SYNTHESE PREVISIONNELLE → 🔄 Tableaux de bord
- **7.3** BILANS → 🔄 Analyses financières

### **8. COMPTABILITE**
- **8.1** TVA → 🔄 Déclarations fiscales
- **8.2** TABLEAU DE BORD → 🔄 KPIs temps réel
- **Script LCR** → ✅ 80% (Extraction PDF automatique OneDrive)

### **9. SOCIAL**
- **9.1** Liste_salaries → ✅ 100% (API + Interface terminées)
- **9.2** Fiche mensuelle → ✅ 90% (Suivi individuel)
- **9.3** Récap et calculs → 🔄 Paie et charges

### **10. OUTILS**
- **10.1** CALCUL_ARDOISES → ✅ 100% (Workflow complet opérationnel)
- **10.2** Calcul_structures → 🔄 En développement
- **10.3** Staravina → 🔄 Base documentaire avec mots-clés
- **10.4** Documents types → 🔄 Templates

### **11. ARCHIVES**
- **11.x** Module futur → 🔄 Archivage automatique

### **12. PARAMETRES**
- **12.x** Configuration système → 🔄 Administration application

### **13. AIDE**
- **13.x** NOMENCLATURE → ✅ 100% (Documentation complète)

---

## 📊 **RÉCAPITULATIF GLOBAL - 13 MODULES**

### **MODULES TERMINÉS (100%)**
- ✅ **9.1** Liste Salariés
- ✅ **10.1** Calcul Ardoises
- ✅ **13.x** Nomenclature/Documentation

### **MODULES QUASI-TERMINÉS (80-95%)**
- 🔄 **3.1** Liste Chantiers (95%)
- 🔄 **1.1** Planning Salariés (90%)
- 🔄 **1.2** Planning Chantiers (90%)
- 🔄 **5.3** Devis MEXT (90%)
- 🔄 **9.2** Fiche Mensuelle (90%)

### **MODULES EN DÉVELOPPEMENT (50-80%)**
- 🔄 **Script LCR** Comptabilité (80%)

### **MODULES À CRÉER (0-50%)**
- 🔄 **Tous les autres modules** (27 modules restants)

**PROGRESSION TOTALE : 8/35 modules détaillés = 23%**

---

## 🏗️ **ARCHITECTURE TECHNIQUE COMPLÈTE**

### **🎯 STACK TECHNOLOGIQUE CHOISIE**

#### **Backend - Python/Flask**
- **Framework** : Flask 2.3+ avec pattern Factory (`create_app()`)
- **ORM** : SQLAlchemy 2.0+ avec modèles déclaratifs  
- **Base de données** : SQLite (dev) → PostgreSQL (production)
- **API** : REST avec format JSON standardisé
- **Dépendances clés** :
  ```python
  Flask + SQLAlchemy + Flask-CORS + Flask-Migrate
  pandas>=1.5.0      # Traitement Excel/CSV
  openpyxl>=3.0.0    # Lecture fichiers Excel
  pytest>=7.0.0      # Framework de tests
  ```

#### **Frontend - React/Vite**
- **Framework UI** : React 18.2.0 avec hooks modernes
- **Build Tool** : Vite 5.1.0 (Hot Module Replacement ultra-rapide)
- **Routing** : React Router DOM 6.22.0
- **Styling** : Tailwind CSS 3.4.1 + @tailwindcss/forms
- **HTTP Client** : Axios 1.6.7
- **État global** : Context API + hooks personnalisés

#### **Architecture Modulaire**
```
backend/app/
├── models/          # SQLAlchemy ORM (13 tables)
├── services/        # Logique métier séparée  
├── routes/          # Blueprints Flask (APIs REST)
├── middleware/      # Gestion erreurs + logging centralisé
├── utils/           # Utilitaires (sécurité, validation)
└── config/          # Configuration par environnement

frontend/src/
├── pages/           # Pages selon nomenclature ATARYS (1.1, 3.1, etc.)
├── components/      # Composants réutilisables (Layout, Grid, Card)
├── contexts/        # Context API (MenuContext, etc.)
├── hooks/           # Hooks personnalisés (useApi)
└── api/             # Services API centralisés
```

### **🗄️ GESTION DES DONNÉES - SQLALCHEMY**

#### **Modèles de Données (13 Tables)**
- **792 enregistrements** au total
- **332 communes bretonnes** avec zones climatiques
- **Relations normalisées** avec clés étrangères
- **Base Model** commune avec `created_at`, `updated_at`, `to_dict()`

#### **Architecture Base de Données**
```python
# Pattern BaseModel pour tous les modèles
class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

# Modèles métier avec relations
class Chantier(BaseModel):
    __tablename__ = '🏗️ Module 3: Chantiers & Devis'
    # 19 colonnes avec relations vers devis, etats_chantier
    
class Salarie(BaseModel):
    __tablename__ = 'liste_salaries'
    # Relations avec planning, niveaux_qualification
```

### **⚠️ DÉFIS TECHNIQUES IDENTIFIÉS**

#### **1. Architecture Hybride Actuelle (PROBLÉMATIQUE)**
```
AUDIT CRITIQUE :
├── SQLAlchemy ORM (Moderne) : 7 fichiers app/
├── SQLite Direct (Legacy) : 25+ fichiers backend/
├── Conflits potentiels : Transactions simultanées
└── Maintenance complexe : Deux façons de faire

IMPACT IMMÉDIAT :
❌ Module 3.1 (95% fait) utilise architecture hybride
❌ Extraction devis critique avec sqlite3.connect()
❌ Risque Julien + Yann accès simultanés
```

#### **2. Scalabilité SQLite**
```
DONNÉES ACTUELLES (2025) :
- 2 chantiers + 2 devis
- 792 enregistrements total  
- Base : ~104 KB

PROJECTION 2027 :
- 100 chantiers + 300 devis
- 2000 factures/commandes  
- 10 000+ planning entries
- Base : 500 MB - 1 GB

LIMITES SQLITE :
❌ 1 seul écrivain simultané
❌ Pas d'authentification native
❌ Limite pratique : 2-3 utilisateurs
```

#### **3. Défis Déploiement Serveur**
```
ENVIRONNEMENT ACTUEL :
- Développement Windows (python run.py + npm run dev)
- Fichiers Excel locaux (26 devis clients)
- Chemins absolus OneDrive

DÉFIS PRODUCTION :
❌ Architecture monolithique (point de défaillance unique)
❌ Stockage fichiers (Excel → Cloud Storage)
❌ Concurrence utilisateurs (SQLite → PostgreSQL)
❌ Sécurité multi-tenant (authentification centralisée)
```

### **🎯 PLAN DE MIGRATION TECHNIQUE**

#### **🔥 PRIORITÉ 1 : Nettoyer Architecture Hybride (1-2 jours)**
```
ROUTES CRITIQUES À MIGRER :
├── app/routes/chantiers.py     # Module 3.1 (95%)
├── app/routes/devis.py         # Extraction automatique
├── app/routes/villes.py        # API géographique
├── extraction_devis_wrapper.py # Cœur métier ATARYS
└── server.py                   # Serveur principal

SCRIPTS UTILITAIRES (Reporter) :
├── create_*.py, check_*.py     # Maintenance ponctuelle
├── test_*.py, debug_*.py       # Outils développeur
└── clean_*.py, analyze_*.py    # Scripts administration
```

#### **📅 PRIORITÉ 2 : Optimisation SQLite (1 semaine)**
```python
# Index sur colonnes critiques
CREATE INDEX idx_chantier_etat ON chantiers(etat_id);
CREATE INDEX idx_chantier_ref ON chantiers(reference_chantier);
CREATE INDEX idx_devis_chantier ON devis(chantier_id);

# Pagination obligatoire
@lru_cache(maxsize=128)
def get_chantiers(page=1, per_page=50):
    return query.offset((page-1)*per_page).limit(per_page)

# Cache données statiques
@lru_cache(maxsize=32)
def get_villes_by_zone(zone_id):
    return VilleService.get_by_zone(zone_id)
```

#### **📅 PRIORITÉ 3 : Migration PostgreSQL (1 mois)**
```python
# Configuration par environnement
class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # postgresql://user:pass@host:5432/atarys
    
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    # Compatibilité développement
```

### **🚀 ARCHITECTURE DÉPLOIEMENT**

#### **Environnements Prévus**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  DÉVELOPPEMENT  │    │     STAGING     │    │   PRODUCTION    │
│ Flask Dev       │    │ Flask + Gunicorn│    │ Flask + Gunicorn│
│ Vite Dev        │    │ Nginx + Build   │    │ Nginx + Build   │
│ SQLAlchemy +    │    │ SQLAlchemy +    │    │ SQLAlchemy +    │
│ SQLite Local    │    │ PostgreSQL      │    │ PostgreSQL      │
│ Port 5000/3000  │    │ Port 80/443     │    │ Port 80/443     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### **Standards API**
```json
// Format standardisé toutes les APIs
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

### **✅ JUSTIFICATION DES CHOIX TECHNIQUES**

#### **Points Forts Architecture**
- **✅ Séparation Backend/Frontend** : APIs réutilisables, frontend optimisé
- **✅ Technologies Éprouvées** : Flask + React (communautés larges)
- **✅ Automatisation Métier** : Excel → API (3h → 30min de gain)
- **✅ Évolutivité Progressive** : SQLite → PostgreSQL transparente

#### **Cohérence Objectifs ATARYS**
- **✅ Remplacer Excel** : Architecture API permet migration 17 onglets
- **✅ Interface Simple** : React + Tailwind pour Yann (novice)
- **✅ Gain Temps** : Extraction devis automatisée validée
- **✅ Croissance** : 13 modules selon nomenclature métier

---

## 🔧 **ACTIONS TECHNIQUES IMMÉDIATES**

### **🎯 Avant Architecture Globale (Cette Semaine)**
1. **Migrer 5 routes critiques** vers SQLAlchemy (app/routes/)
2. **Tester extraction devis** avec architecture propre
3. **Valider Module 3.1** sans conflits de données
4. **Optimiser index** sur colonnes recherchées

### **🎯 Phase 1 Finalisée (Mi-Octobre)**
- **Architecture unifiée** : 100% SQLAlchemy ORM
- **Performance optimisée** : Index + pagination + cache
- **Déploiement prêt** : Configuration multi-environnement
- **Excel remplacé** : 17 onglets → Application web complète

### **🎯 Indicateurs Techniques de Réussite**
- **0 fichier** avec `sqlite3.connect()` dans app/
- **< 2s** temps de réponse toutes APIs
- **100% compatibilité** développement ↔ production
- **Concurrent users** : Julien + Yann sans conflits

**ARCHITECTURE TECHNIQUE : FONDATIONS SOLIDES POUR 3 PHASES ATARYS**

---

** MI-OCTOBRE 2025 : PHASE 1 TERMINÉE - EXCEL REMPLACÉ !**
