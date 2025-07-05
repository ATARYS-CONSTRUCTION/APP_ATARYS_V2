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

**Remplacer tous les fichiers Excel** par une application web moderne et structurée

### ** PROJET ATARYS V2 - NOUVEAU DÉPART**

**🔄 POURQUOI UNE V2 ?**
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

### ** TAUX DE COMPLETION GLOBAL V2 : 33%**

**🚀 ÉTAT ACTUEL V2 (05/07/2025) :**

#### ** ÉLÉMENTS 100% OPÉRATIONNELS V2**
- **Frontend React** - Structure complète fonctionnelle (port 3000)
- **Documentation** - Architecture complète et cohérente (4 fichiers d'architecture)
- **Nomenclature** - 13 modules ATARYS avec sous-modules définis
- **Standards** - Méthodologie Cursor stricte + spécifications techniques
- **Spécifications** - BaseModel pattern, SQLAlchemy 2.0+, Factory Flask

#### ** RÉFÉRENCE TECHNIQUE V1 CONSERVÉE**
- **Dossiers V1** - `0 APP ATARYS/` et `0 APP ATARYS - Copie/` pour référence
- **Scripts d'import** - Logique d'extraction Excel/CSV à adapter
- **Structure BDD** - Modèles SQLAlchemy comme base de réflexion
- **Configuration** - Paramètres techniques à reprendre

#### ** À CRÉER ENTIÈREMENT EN V2**
- **Backend Flask** - API REST structurée selon modules ATARYS
- **Base de données** - SQLite V2 propre à partir d'Excel à jour
- **Scripts d'import** - Nouveaux outils Excel → SQLite V2
- **Module 3.1** - LISTE CHANTIERS (interface + API)
- **Module 9.1** - Liste_salaries (interface + API)
- **Module 10.1** - CALCUL_ARDOISES (interface + API)

#### ** INFRASTRUCTURE V2 DÉFINIE**
- **Architecture modulaire** : 13 modules définis avec sous-modules
- **Standards de code** : Règles Cursor appliquées
- **Documentation technique** : Architecture complète dans `docs/02-architecture/`
- **Spécifications** : API_ENDPOINTS.md, DATABASE_SCHEMA.md, ATARYS_MODULES.md
- **Environnement dev** : Frontend opérationnel, backend à créer

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

### ** PRIORITÉ 1 : CRÉER BACKEND V2** (URGENT)
**Objectif :** Créer l'API REST Flask selon spécifications d'architecture
- ✅ Architecture V2 définie (FAIT - voir `docs/02-architecture/`)
- ✅ Standards de développement (FAIT - SQLAlchemy 2.0+ + BaseModel pattern)
- ✅ Spécifications techniques (FAIT - voir `API_ENDPOINTS.md`)
- 🔄 Créer structure backend Flask avec Factory pattern
- 🔄 Implémenter BaseModel et configuration SQLAlchemy
- 🔄 Créer APIs REST pour modules prioritaires (3.1, 9.1, 10.1)

### ** PRIORITÉ 2 : CRÉATION BASE DE DONNÉES V2** (CRITIQUE)
**Objectif :** Créer une base de données propre à partir de fichiers Excel à jour
- **Approche** : Repartir à zéro avec données propres et à jour
- **Source** : Fichier Excel propre préparé par l'utilisateur
- **Standards V2** : SQLAlchemy 2.0+ avec `db.Numeric(10, 2)` pour montants
- **Scripts d'import** : Créer outils d'import Excel → SQLite V2
- **Action** : Base SQLite V2 selon modules ATARYS prioritaires

### ** PRIORITÉ 3 : DÉVELOPPER MODULE 3.1** (APRÈS BACKEND + BDD)
**Remplace :** "LISTE DES TACHES" + "Liste_Chantiers"
- ✅ Référence V1 pour logique métier (FAIT)
- 🔄 Modèles SQLAlchemy avec BaseModel pattern
- 🔄 Interface utilisateur React selon standards
- 🔄 Connexion API frontend ↔ backend
- 🔄 Tests et validation complète

### ** PRIORITÉ 4 : MODULES ADDITIONNELS V2** (Long terme)
**Objectif :** Développer les modules selon roadmap Phase 1-3
- **Phase 1** : Modules 9.1 (Salariés) et 10.1 (Calcul Ardoises)
- **Phase 2** : Modules 1.1/1.2 (Planning) et 7.1/7.2 (Gestion)
- **Phase 3** : Modules restants selon besoins métier
- **Organisation** : Selon nomenclature officielle `ATARYS_MODULES.md`

### ** PRIORITÉ 5 : TABLEAUX DE BORD ET SYNTHÈSES** (3-4 semaines)
**Remplace :** "Synthèse Prévisionnel" + "Tableau de bord"
- KPIs temps réel
- Graphiques évolution  
- Alertes automatiques
- Interfaces de pilotage

**💡 REMARQUE V2 :** Interface simplifiée pour Yann (gros boutons, workflow guidé) sera intégrée naturellement dans chaque module développé selon les standards V2.

---

## 🔄 **BILAN V1 → V2 : NOUVEAU DÉPART JUSTIFIÉ**

### **🚨 PROBLÈMES V1 "0 APP ATARYS"**
- **Développement erratique** : Code écrit sans méthodologie
- **Architecture instable** : Pas de standards, refactoring constant
- **Documentation inexistante** : Difficile de s'y retrouver
- **Nommage incohérent** : Pas de nomenclature officielle
- **Code spaghetti** : Mélange frontend/backend, pas de séparation
- **Stress développement** : Régressions constantes, bugs récurrents

### **✅ AVANTAGES V2 "APP_ATARYS V2"**
- **Méthodologie Cursor** : Règles strictes appliquées systématiquement
- **Architecture solide** : Frontend React + Backend Flask séparés
- **Documentation complète** : Chaque aspect documenté et cohérent
- **Nomenclature officielle** : 13 modules avec sous-modules définis
- **Standards de code** : Qualité professionnelle assurée
- **Développement serein** : Base solide pour accélération future

### **📊 COMPARAISON OBJECTIVE**
| Aspect | V1 "0 APP ATARYS" | V2 "APP_ATARYS V2" |
|--------|------------------|-------------------|
| **Architecture** | ❌ Chaotique | ✅ Structurée |
| **Documentation** | ❌ Inexistante | ✅ Complète |
| **Standards** | ❌ Aucun | ✅ Stricts |
| **Maintenance** | ❌ Impossible | ✅ Facilitée |
| **Évolutivité** | ❌ Bloquée | ✅ Assurée |
| **Progression** | ❌ 43% instable | ✅ 33% solide |

### **🎯 STRATÉGIE V2 : INVESTIR POUR ACCÉLÉRER**
- **Principe** : Prendre le temps de bien faire pour aller plus vite ensuite
- **Résultat** : Base solide qui permettra un développement rapide des modules
- **Objectif** : Rattraper et dépasser la V1 d'ici fin 2025

---

##  **MÉTRIQUES PROGRESSION 3 PHASES**

### **📊 PHASE 1 - REMPLACEMENT EXCEL (Mi-octobre 2025)**
**Objectif :** 17 onglets Excel → 0 (100% remplacés)

**MODULES PHASE 1 V2 :**
- [x] **Frontend** → Structure React + Tailwind + Vite ✅
- [x] **Documentation** → Architecture complète et cohérente ✅
- [x] **Standards** → Méthodologie Cursor + Nomenclature officielle ✅
- [x] **Référence V1** → Conservée dans `0 APP ATARYS/` pour technique ✅
- [ ] **Backend** → API REST Flask à créer (0%)
- [ ] **Base de données** → SQLite V2 propre à partir d'Excel à jour (0%)
- [ ] **3.1** Liste Chantiers → Interface + API (0%)
- [ ] **9.1** Liste_salaries → Interface + API (0%)
- [ ] **10.1** CALCUL_ARDOISES → Interface + API (0%)
- [ ] **1.1/1.2** Planning → Interface + API (0%)
- [ ] **7.1/7.2** Tableaux de bord → Interface + API (0%)
- [ ] **Mode Yann** → Interface simplifiée pour conducteur (0%)

**PROGRESSION PHASE 1 V2 : 4/12 = 33%**

**🎯 DIFFÉRENCE V1 vs V2 :**
- **V1** : Développement chaotique, 43% mais instable
- **V2** : Base solide, 33% mais architecture pérenne
- **Avantage V2** : Fondations solides pour développement rapide

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

**ÉTAT GLOBAL PROJET V2 : 4/12 modules = 33%**  
**OBJECTIF MI-OCTOBRE : 12/12 modules = 100%** (Phase 1 V2 terminée)

**🔄 LEÇONS APPRISES V1 → V2 :**
- **V1** : Développement rapide mais chaotique → instabilité
- **V2** : Développement méthodique → base solide pour accélération
- **Stratégie V2** : Investir dans l'architecture pour gagner en vitesse ensuite

---

## 📋 **NOMENCLATURE COMPLÈTE ATARYS - 13 MODULES**

> **Référence** : Selon `docs/02-architecture/ATARYS_MODULES.md`

### **1. PLANNING**
- 1.1 PLANNING SALARIÉS
- 1.2 PLANNING CHANTIER

### **2. LISTE DES TÂCHES**
- 2.1 YANN
- 2.2 JULIEN

### **3. LISTE CHANTIERS**
- 3.1 LISTE CHANTIERS
- 3.2 CHANTIERS PROJETS
- 3.3 CHANTIERS SIGNÉS
- 3.4 CHANTIERS EN COURS
- 3.5 CHANTIERS ARCHIVES

### **4. CHANTIERS**
- 4.1 SUIVI DE CHANTIER
- 4.2 NOTES DE CHANTIER
- 4.3 COMMANDES
- 4.4 DOCUMENTS

### **5. DEVIS-FACTURATION**
- 5.1 Ouvrages et articles BATAPPLI
- 5.2 FICHE MÈTRES
- 5.3 DEVIS MEXT
- 5.4 DEVIS TYPE

### **6. ATELIER**
- 6.1 QUINCAILLERIE
- 6.2 CONSOMMABLES
- 6.3 CAMIONS
- 6.4 MATÉRIEL
- 6.5 ÉCHAFAUDAGE

### **7. GESTION**
- 7.1 PRÉVISIONNEL
- 7.2 SYNTHÈSE PRÉVISIONNELLE
- 7.3 BILANS

### **8. COMPTABILITÉ**
- 8.1 TVA
- 8.2 TABLEAU DE BORD

### **9. SOCIAL**
- 9.1 Liste_salaries
- 9.2 Fiche mensuelle
- 9.3 Récap et calculs

### **10. OUTILS**
- 10.1 CALCUL_ARDOISES
- 10.2 Calcul_structures
- 10.3 Staravina (base de données avec mots-clés de la documentation)
- 10.4 Documents types

### **11. ARCHIVES**
- (Pas de sous-modules définis)

### **12. PARAMÈTRES**
- 12.1 BASE DE DONNÉES

### **13. AIDE**
- 13.1 DOCUMENTATION

---

## 🎯 **DÉVELOPPEMENT ORGANISÉ PAR MODULES**

### **MODULES PRIORITAIRES PHASE 1**
- **3.1** LISTE CHANTIERS → 🔄 **PRIORITÉ 1** (Remplace Excel "LISTE DES TACHES")
- **9.1** Liste Salariés → ✅ **100%** (API + Interface terminées)
- **10.1** CALCUL ARDOISES → ✅ **100%** (Workflow complet opérationnel)

### **MODULES PHASE 2**
- **1.1** PLANNING SALARIÉS → 🔄 À créer après backend
- **1.2** PLANNING CHANTIER → 🔄 À créer après backend
- **7.1** PRÉVISIONNEL → 🔄 Tableaux de bord financiers
- **7.2** SYNTHÈSE PRÉVISIONNELLE → 🔄 KPIs temps réel

### **MODULES PHASE 3**
- **5.1-5.4** DEVIS-FACTURATION → 🔄 Remplacer BATAPPLI
- **8.1-8.2** COMPTABILITÉ → 🔄 Intégration fiscale
- **Modules restants** → 🔄 Selon besoins métier

### **ÉTAT GLOBAL DES MODULES**
- **Modules terminés** : 2/13 (15%)
- **Modules en cours** : 1/13 (8%)
- **Modules à créer** : 10/13 (77%)

**🎯 OBJECTIF PHASE 1 :** 5 modules opérationnels (38%) pour remplacer Excel

---

## 🏗️ **ARCHITECTURE TECHNIQUE V2**

### **STACK TECHNOLOGIQUE**
- **Frontend** : React 18.2.0 + Vite 5.4.19 + Tailwind CSS 3.4.1
- **Backend** : Flask 3.0+ + SQLAlchemy 2.0+ + Factory pattern
- **Base de données** : SQLite avec BaseModel pattern
- **Standards** : API REST, `db.Numeric(10, 2)` pour montants

### **ORGANISATION FICHIERS**
```
APP_ATARYS V2/
├── frontend/src/          # React + Vite (port 3000)
├── backend/app/           # Flask + SQLAlchemy (port 5000)
├── docs/02-architecture/  # Spécifications techniques
├── data/                  # Données de référence
└── .bat/                  # Scripts PowerShell
```

### **FLUX DE DONNÉES**
- **Frontend → Backend** : API REST format `{success, data, message}`
- **Backend → SQLite** : SQLAlchemy 2.0+ avec BaseModel
- **Excel → SQLite** : Scripts d'import dans `backend/scripts/`

---

## 📋 **MÉTRIQUES DÉVELOPPEMENT**

### **LIGNES DE CODE ESTIMÉES**
- **Frontend** : ~5 000 lignes (React + composants)
- **Backend** : ~3 000 lignes (Flask + API)
- **Documentation** : ~2 000 lignes (Architecture + guides)
- **Total projet** : ~10 000 lignes

### **TEMPS DE DÉVELOPPEMENT ESTIMÉ**
- **Phase 1** : 6-8 semaines (5 modules prioritaires)
- **Phase 2** : 12-16 semaines (logiciel complet)
- **Phase 3** : 8-12 semaines (IA et optimisations)

### **COMPLEXITÉ TECHNIQUE**
- **Module 3.1** : ⭐⭐⭐ (CRUD + états + workflow)
- **Module 9.1** : ⭐ (CRUD simple)
- **Module 10.1** : ⭐⭐ (Calculs + PDF)
- **Modules 5.x** : ⭐⭐⭐⭐⭐ (Devis-facturation complexe)

---

### **🎯 CRITÈRES DE RÉUSSITE PHASE 1 (Mi-octobre)**
- ✅ **Excel fermés définitivement** : 17 onglets → 0
- ✅ **Gérant serein** : Stress admin réduit de 50%  
- ✅ **Interface Yann** : Novice informatique autonome
- ✅ **Équipe rassurée** : Organisation professionnelle visible

**ÉTAT GLOBAL PROJET V2 : 4/12 modules = 33%**  
**OBJECTIF MI-OCTOBRE : 12/12 modules = 100%** (Phase 1 V2 terminée)

**🔄 LEÇONS APPRISES V1 → V2 :**
- **V1** : Développement rapide mais chaotique → instabilité
- **V2** : Développement méthodique → base solide pour accélération
- **Stratégie V2** : Investir dans l'architecture pour gagner en vitesse ensuite

---

## 📋 **NOMENCLATURE COMPLÈTE ATARYS - 13 MODULES**

> **Référence** : Selon `docs/02-architecture/ATARYS_MODULES.md`

### **1. PLANNING**
- 1.1 PLANNING SALARIÉS
- 1.2 PLANNING CHANTIER

### **2. LISTE DES TÂCHES**
- 2.1 YANN
- 2.2 JULIEN

### **3. LISTE CHANTIERS**
- 3.1 LISTE CHANTIERS
- 3.2 CHANTIERS PROJETS
- 3.3 CHANTIERS SIGNÉS
- 3.4 CHANTIERS EN COURS
- 3.5 CHANTIERS ARCHIVES

### **4. CHANTIERS**
- 4.1 SUIVI DE CHANTIER
- 4.2 NOTES DE CHANTIER
- 4.3 COMMANDES
- 4.4 DOCUMENTS

### **5. DEVIS-FACTURATION**
- 5.1 Ouvrages et articles BATAPPLI
- 5.2 FICHE MÈTRES
- 5.3 DEVIS MEXT
- 5.4 DEVIS TYPE

### **6. ATELIER**
- 6.1 QUINCAILLERIE
- 6.2 CONSOMMABLES
- 6.3 CAMIONS
- 6.4 MATÉRIEL
- 6.5 ÉCHAFAUDAGE

### **7. GESTION**
- 7.1 PRÉVISIONNEL
- 7.2 SYNTHÈSE PRÉVISIONNELLE
- 7.3 BILANS

### **8. COMPTABILITÉ**
- 8.1 TVA
- 8.2 TABLEAU DE BORD

### **9. SOCIAL**
- 9.1 Liste_salaries
- 9.2 Fiche mensuelle
- 9.3 Récap et calculs

### **10. OUTILS**
- 10.1 CALCUL_ARDOISES
- 10.2 Calcul_structures
- 10.3 Staravina (base de données avec mots-clés de la documentation)
- 10.4 Documents types

### **11. ARCHIVES**
- (Pas de sous-modules définis)

### **12. PARAMÈTRES**
- 12.1 BASE DE DONNÉES

### **13. AIDE**
- 13.1 DOCUMENTATION

---

## 🚀 **ACTIONS IMMÉDIATES - ROADMAP**

### **SEMAINE 1-2 : BACKEND + BASE DE DONNÉES**
1. **Créer structure backend Flask** selon spécifications
2. **Implémenter BaseModel** et configuration SQLAlchemy 2.0+
3. **Créer base SQLite V2** avec modules prioritaires
4. **Scripts d'import Excel** → SQLite V2

### **SEMAINE 3-4 : MODULE 3.1**
1. **Modèles SQLAlchemy** pour chantiers/devis/états
2. **API REST** pour CRUD chantiers
3. **Interface React** selon standards ATARYS
4. **Tests et validation** complète

### **SEMAINE 5-6 : MODULES 9.1 & 10.1**
1. **Finaliser module 9.1** (Salariés) avec backend
2. **Finaliser module 10.1** (Calcul Ardoises) avec backend
3. **Intégration complète** frontend ↔ backend
4. **Tests utilisateur** avec Yann

### **SEMAINE 7-8 : FINALISATION PHASE 1**
1. **Tableaux de bord** et synthèses
2. **Optimisations** et corrections
3. **Documentation utilisateur**
4. **Déploiement** et formation équipe

**🎯 OBJECTIF : Application V2 opérationnelle mi-octobre 2025**

---

## 📞 **CONTACTS & RESSOURCES**

### **ÉQUIPE PROJET**
- **Julien** (Gérant) : Vision métier, validation fonctionnelle
- **Yann** (Conducteur) : Tests utilisateur, feedback terrain
- **Développeur** : Architecture technique, implémentation

### **RESSOURCES TECHNIQUES**
- **Documentation** : `docs/02-architecture/`
- **Référence V1** : `0 APP ATARYS/` (technique uniquement)
- **Données** : Excel à jour préparé par utilisateur
- **Standards** : `.cursorrules` (méthodologie Cursor)

### **OUTILS DÉVELOPPEMENT**
- **IDE** : Cursor avec règles strictes
- **Frontend** : React + Vite (port 3000)
- **Backend** : Flask + SQLAlchemy (port 5000)
- **Base** : SQLite + scripts d'import

---

**🎯 SUCCÈS ATARYS V2 = Gérant serein + Excel fermés + Équipe rassurée**
