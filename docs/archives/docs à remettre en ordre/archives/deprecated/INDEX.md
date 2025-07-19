# 📚 Index Documentation IA - ATARYS

> **Guide central pour toute la documentation du projet ATARYS selon Nomenclature**  
> Organisation en 13 modules fonctionnels avec documentation technique complète

---

## 🎯 **Documentation Principale**

### **Architecture & Nomenclature**
- **[ATARYS_ARCHITECTURE.md](ATARYS_ARCHITECTURE.md)** - Architecture complète selon nomenclature
  - Vision et objectifs ATARYS
  - 13 modules fonctionnels (1. PLANNING → 13. AIDE)
  - Stack technologique (Flask + React + SQLite)
  - État d'avancement par module
  - Standards de développement et conventions

### **Nomenclature Officielle**
- **[NOMENCLATURE.txt](NOMENCLATURE.txt)** - Structure officielle des modules
  - 13 chapitres principaux avec sous-modules
  - Organisation hiérarchique (X.Y)
  - Définition des domaines fonctionnels

---

## 📋 **Architecture Fonctionnelle - 13 Modules ATARYS**

### **✅ Modules Implémentés**

#### **1 PLANNING**
- **1.1 PLANNING SALARIES**
- **1.2 PLANNING CHANTIER**

#### **2 LISTE DES TACHES**
- **2.2 JULIEN**
- **2.1 YANN**

#### **3 LISTE CHANTIERS**
- **3.1 LISTE CHANTIERS**
- **3.2 CHANTIERS PROJETS**
- **3.3 CHANTIERS SIGNES**
- **3.4 CHANTIERS EN COURS**
- **3.5 CHANTIERS ARCHIVES**

#### **4 CHANTIERS**
- **4.1 SUIVI DE CHANTIER**
- **4.2 NOTES DE CHANTIER**
- **4.3 COMMANDES**
- **4.4 DOCUMENTS**

#### **5 DEVIS-FACTURATION**
- **5.1 Ouvrages et articles BATAPPLI**
- **5.2 FICHE METRES**
- **5.3 DEVIS MEXT**
- **5.4 DEVIS TYPE**

#### **6 ATELIER**
- **6.1 QUINCAILLERIE**
- **6.2 CONSOMMABLES**
- **6.3 CAMION**
- **6.4 MATERIEL**
- **6.5 ECHAFAUDAGE**

#### **7 GESTION**
- **7.1 PREVISIONNEL**
- **7.2 SYNTHESE PREVISIONNELLE**
- **7.3 BILANS**

#### **8 COMPTABILITE**
- **8.1 TVA**
- **8.2 TABLEAU DE BORD**

#### **9 SOCIAL**
- **9.1 Liste_salaries**
- **9.2 Fiche mensuelle**
- **9.3 Récap et calculs**

#### **10 OUTILS**
- **10.1 CALCUL_ARDOISES**
- **10.2 Calcul_structures**
- **10.3 Staravina (base de données avec mots-clés de la documentation)**
- **10.4 Documents types**

#### **11 ARCHIVES**

#### **12 PARAMETRES**

#### **13 AIDE**
- **NOMENCLATURE**

### **🚧 Modules en Développement**

#### **Module 2 - LISTE DES TÂCHES**
- **2.1 Yann** - Tâches personnalisées
- **2.2 Julien** - Tâches personnalisées

#### **Module 3 - LISTE CHANTIERS** 🎯 *Priorité Haute*
- **3.1 Liste Chantiers** - Vue générale
- **3.2 Chantiers à Deviser** - Pipeline commercial
- **3.3 Chantiers Signés** - Commandes confirmées
- **3.4 Chantiers à Finir** - Suivi réalisation
- **3.5 Chantiers Archives** - Historique

#### **Module 4 - CHANTIERS**
- **4.1 Suivi de Chantier** - Avancement travaux
- **4.2 Liste des Tâches** - Détail par chantier
- **4.3 Commandes** - Gestion approvisionnements
- **4.4 Documents** - Dossier technique

#### **Module 5 - DEVIS-FACTURATION** 🎯 *Impact Business*
- **5.1 Ouvrages et Articles BATAPPLI** - Référentiel
- **5.2 Fiche Mètres** - Métrés détaillés
- **5.3 Demande de Devis MEXT** - Fournisseurs
- **5.4 Estimatif** - Calculs prévisionnels

#### **Module 6 - ATELIER**
- **6.1 Quincaillerie** - Stock fixations
- **6.2 Consommables** - Matériaux courants
- **6.3 Camion** - Gestion véhicules
- **6.4 Matériel** - Outillage
- **6.5 Échafaudage** - Équipements sécurité

#### **Module 7 - GESTION** 🎯 *Tableaux de Bord*
- **7.1 Prévisionnel** - Budget prévisionnel
- **7.2 Synthèse Prévisionnelle** - Tableaux de bord
- **7.3 Bilans** - Analyses financières

#### **Module 8 - COMPTABILITÉ**
- **8.1 TVA** - Déclarations fiscales

#### **Module 11 - ARCHIVES**
- Gestion documentaire

#### **Module 12 - PARAMÈTRES**
- Configuration système

---

## 🔧 **Documentation Technique Complète**

### **APIs & Endpoints**
- **[API_ENDPOINTS.md](API_ENDPOINTS.md)** ✅ **Complet** - Documentation des APIs REST
  - 30+ endpoints avec paramètres et réponses
  - Exemples JavaScript et cURL par module
  - Codes d'erreur et format standardisé
  - Pagination et filtrage

### **Base de Données**
- **[DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)** ✅ **Complet** - Schéma SQLite détaillé
  - 13 tables avec 792 enregistrements
  - Relations et contraintes par module
  - Workflow calcul ardoises (Module 10.1)
  - Index et optimisations recommandées

### **Tests & Qualité**
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** ✅ **Complet** - Stratégie de tests
  - Pyramide de tests (80% unitaires, 15% intégration, 5% E2E)
  - Configuration pytest + Jest + Playwright
  - Tests par module avec exemples
  - Performance et monitoring

### **Déploiement**
- **[DEPLOYMENT.md](DEPLOYMENT.md)** ✅ **Complet** - Guide déploiement
  - 3 environnements (dev, staging, production)
  - Configuration Nginx + Gunicorn + PostgreSQL
  - CI/CD GitHub Actions par module
  - Sécurité et monitoring

---

## 📋 **Guides de Développement**

### **Consignes & Standards**
- **[CONSIGNES.md](CONSIGNES.md)** ✅ **Mis à jour** - Guide développement ATARYS
  - Architecture établie selon nomenclature
  - Standards APIs et UI/UX par module
  - Workflow git avec références modules
  - Évolutions récentes et prochaines étapes

- **[CHECKLIST_DEVELOPPEMENT.md](CHECKLIST_DEVELOPPEMENT.md)** ✅ **Nouveau** - Processus obligatoire
  - Consultation documentation AVANT tout code
  - Workflow en 3 phases (Doc → Dev → Validation)
  - Questions obligatoires à se poser
  - Règles d'or pour cohérence ATARYS

### **Règles Globales**
- **[regles.md](regles.md)** - Règles globales du projet
  - Règles générales à respecter
  - Contraintes et limitations par module

---

## 📊 **Documentation Fonctionnelle**

### **Synthèse Projet**
- **[SYNTHESE.md](SYNTHESE.md)** - Synthèse générale du projet
  - Vue d'ensemble du système ATARYS
  - Fonctionnalités par module
  - État actuel et roadmap selon nomenclature

---

## 🚀 **Guides Utilisateur (À Créer)**

### **Manuel Utilisateur par Module**
- **[USER_MANUAL.md](USER_MANUAL.md)** *(À créer)*
  - Guide d'utilisation par module (1-13)
  - Workflows et cas d'usage spécifiques
  - FAQ par domaine fonctionnel

### **Guide d'Installation**
- **[INSTALLATION.md](INSTALLATION.md)** *(À créer)*
  - Prérequis système
  - Installation pas à pas
  - Configuration initiale des modules

---

## 📝 **Documentation de Maintenance**

### **Changelog par Module**
- **[CHANGELOG.md](CHANGELOG.md)** *(À créer)*
  - Historique des versions par module
  - Nouvelles fonctionnalités selon nomenclature
  - Corrections de bugs référencées

### **Roadmap selon Nomenclature**
- **[ROADMAP.md](ROADMAP.md)** *(À créer)*
  - Prochaines étapes par module
  - Priorités : Module 3 → Module 5 → Module 7
  - Planning de développement

### **Troubleshooting par Module**
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** *(À créer)*
  - Problèmes courants par module
  - Diagnostic et débogage spécifique
  - Logs et monitoring par domaine

---

## 🎨 **Documentation Design**

### **UI/UX Guidelines par Module**
- **[DESIGN_SYSTEM.md](DESIGN_SYSTEM.md)** *(À créer)*
  - Système de design selon nomenclature
  - Composants UI par module
  - Guidelines d'interface cohérentes

### **Wireframes par Module**
- **[WIREFRAMES.md](WIREFRAMES.md)** *(À créer)*
  - Maquettes des interfaces par module
  - Flux utilisateur selon nomenclature
  - Spécifications visuelles

---

## 🛠️ **Templates de Développement**

### **Template Nouvelle Page**
- **[TEMPLATE_NOUVELLE_PAGE.md](TEMPLATE_NOUVELLE_PAGE.md)** ✅ **Créé** - Guide complet pour créer une nouvelle page
  - Identification du module selon nomenclature
  - Structure backend complète (Modèle, Service, Routes)
  - Page frontend avec hooks et composants
  - Intégration et tests
  - Documentation et standards ATARYS
  - Checklist complète et exemples pratiques

---

## 📚 **Comment Utiliser Cette Documentation**

### **Pour les Développeurs**
1. **Commencez par** : `ATARYS_ARCHITECTURE.md` pour comprendre les 13 modules
2. **Consultez** : `NOMENCLATURE.txt` pour la structure officielle
3. **Référez-vous** : `consignes.md` pour les standards par module
4. **Utilisez** : Format commit "Module X.Y: Description"

### **Pour l'IA Assistant**
- **Référencez les modules** : "Module 10.1 (Calcul Ardoises)"
- **Mentionnez la nomenclature** : "Selon la nomenclature ATARYS..."
- **Organisez par modules** : Structurez les réponses selon les 13 modules
- **Mettez à jour** : Maintenez la cohérence avec la nomenclature

### **Pour la Maintenance**
- **Organisez par modules** : Classez les évolutions selon la nomenclature
- **Tenez à jour** : Maintenez la cohérence des 13 modules
- **Référencez** : Utilisez toujours la numérotation officielle

---

## 🔄 **Statut des Fichiers selon Nomenclature**

| Fichier | Statut | Modules Couverts | Dernière MAJ | Description |
|---------|--------|------------------|--------------|-------------|
| `ATARYS_ARCHITECTURE.md` | ✅ Complet | 1-13 | 22/06/2025 | Architecture par modules |
| `NOMENCLATURE.txt` | ✅ Référence | 1-13 | 22/06/2025 | Structure officielle |
| `consignes.md` | ✅ Mis à jour | 1, 9, 10, 13 | 22/06/2025 | Guide développement |
| `INDEX.md` | ✅ Restructuré | 1-13 | 22/06/2025 | Navigation par modules |
| `API_ENDPOINTS.md` | ✅ Complet | 1, 9, 10 | 22/06/2025 | APIs par modules |
| `DATABASE_SCHEMA.md` | ✅ Complet | 1, 9, 10 | 22/06/2025 | Tables par modules |
| `TESTING_GUIDE.md` | ✅ Complet | Global | 22/06/2025 | Tests par modules |
| `DEPLOYMENT.md` | ✅ Complet | Global | 22/06/2025 | Déploiement global |
| `TEMPLATE_NOUVELLE_PAGE.md` | ✅ Créé | Guide | 22/06/2025 | Template développement complet |
| `regles.md` | ✅ Existant | Global | - | Règles globales |
| `SYNTHESE.md` | ✅ Existant | Global | - | Synthèse projet |

---

## 🎯 **Prochaines Étapes selon Nomenclature**

### **Priorité 1 - Module 3 (LISTE CHANTIERS)**
- Créer les APIs pour les 5 sous-modules (3.1 à 3.5)
- Développer l'interface de gestion des chantiers
- Implémenter le pipeline commercial

### **Priorité 2 - Module 5 (DEVIS-FACTURATION)**
- Intégration BATAPPLI (5.1)
- Système de métrés (5.2)
- Gestion fournisseurs (5.3)
- Calculs prévisionnels (5.4)

### **Priorité 3 - Module 7 (GESTION)**
- Tableaux de bord (7.2)
- Analyses prévisionnelles (7.1)
- Bilans financiers (7.3)

---

*Dernière mise à jour de l'index : 22/06/2025 - Restructuration selon Nomenclature ATARYS*  
*Organisation : 13 modules fonctionnels avec documentation technique complète* 