# ATARYS - Architecture Technique Complète

> **Document de référence unique pour toute l'architecture ATARYS**  
> Fusion architecture technique + standards + vision globale  
> Dernière mise à jour : 02/07/2025

---

## 🎯 **Vision et Objectifs ATARYS**

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

## 🏗️ **Stack Technologique**

### **Backend - Python/Flask**
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

### **Frontend - React/Vite**
- **Framework UI** : React 18.2.0 avec hooks modernes
- **Build Tool** : Vite 5.1.0 (Hot Module Replacement ultra-rapide)
- **Routing** : React Router DOM 6.22.0
- **Styling** : Tailwind CSS 3.4.1 + @tailwindcss/forms
- **HTTP Client** : Axios 1.6.7
- **État global** : Context API + hooks personnalisés

---

## 📁 **Structure du Projet**

### **Architecture Modulaire**
```
0 APP ATARYS/
├── backend/app/
│   ├── models/          # SQLAlchemy ORM (13 tables)
│   ├── services/        # Logique métier séparée  
│   ├── routes/          # Blueprints Flask (APIs REST)
│   ├── middleware/      # Gestion erreurs + logging centralisé
│   ├── utils/           # Utilitaires (sécurité, validation)
│   └── config/          # Configuration par environnement
├── frontend/src/
│   ├── pages/           # Pages selon nomenclature ATARYS (1.1, 3.1, etc.)
│   ├── components/      # Composants réutilisables (Layout, Grid, Card)
│   ├── contexts/        # Context API (MenuContext, etc.)
│   ├── hooks/           # Hooks personnalisés (useApi)
│   └── api/             # Services API centralisés
└── docs/                # Documentation restructurée par thème
```

---

## 📋 **Architecture Fonctionnelle - 13 Modules ATARYS**

### **✅ Modules 100% Opérationnels**
- **Module 9.1** - Liste Salariés (API + Interface complète)
- **Module 10.1** - Calcul Ardoises (Workflow complet fonctionnel)
- **Architecture Backend** - Flask + SQLAlchemy + 13 tables

### **🔄 Modules 80-95% Opérationnels**
- **Module 3.1** - Liste Chantiers (95% - PRIORITÉ 1)
- **Module 1.1** - Planning Salariés (90%)
- **Module 1.2** - Planning Chantiers (90%)
- **Module 5.3** - Devis MEXT (90% - Extraction Excel)

### **📋 Nomenclature Complète**
```
1. PLANNING          → 1.1 Salariés, 1.2 Chantiers
2. LISTE DES TÂCHES  → 2.1 Yann, 2.2 Julien
3. LISTE CHANTIERS   → 3.1 Liste, 3.2 Projets, 3.3 Signés, 3.4 En cours, 3.5 Archives
4. CHANTIERS         → 4.1 Suivi, 4.2 Notes, 4.3 Commandes, 4.4 Documents
5. DEVIS-FACTURATION → 5.1 BATAPPLI, 5.2 Fiche Mètres, 5.3 MEXT, 5.4 Type
6. ATELIER           → 6.1-6.5 Quincaillerie, Consommables, Camion, Matériel, Échafaudage
7. GESTION           → 7.1-7.3 Prévisionnel, Synthèse, Bilans
8. COMPTABILITÉ      → 8.1-8.2 TVA, Tableau de bord
9. SOCIAL            → 9.1-9.3 Salariés, Fiche mensuelle, Récap
10. OUTILS           → 10.1-10.5 Ardoises, Structures, Staravina, Domaine, Documents
11. ARCHIVES         → Archivage automatique
12. PARAMÈTRES       → Configuration système
13. AIDE             → Nomenclature + Documentation
```

---

## 🗄️ **Base de Données SQLAlchemy**

### **13 Tables Principales**
- **`chantiers`** : Projets chantier (19 colonnes)
- **`devis`** : Devis clients (17 colonnes)
- **`liste_salaries`** : Employés (10 entrées)
- **`villes`** : Communes Bretagne (332 entrées)
- **`calcul_modele_ardoises`** : Calculs ardoises (194 entrées)
- **`planning`** : Planning général (5 entrées)
- **`etats_chantier`** : États workflow
- **`familles_ouvrages`** : Classification travaux
- **`niveaux_qualification`** : Grille salariale
- **Et 4 autres tables** support

### **Architecture Base Model**
```python
class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
```

---

## 🔧 **Standards de Développement**

### **Layout System Frontend**
- **PageLayout** : Conteneur principal avec variants
- **Card** : Composant de base avec padding standard (16px)
- **GridLayout** : Grille 12 colonnes (8/4, 7/5, 6/6)
- **FormLayout** : Formulaires 2 colonnes responsive

### **Format API Standard**
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

### **Conventions Nommage**
- **Modules** : Numérotation 1-13 selon nomenclature
- **Sous-modules** : X.Y (ex: 1.1, 1.2)
- **Composants** : PascalCase (`CalculArdoises.jsx`)
- **Fichiers** : snake_case pour backend, camelCase pour frontend
- **APIs** : kebab-case (`/api/calcul-ardoises`)

---

## 🚀 **Environnement de Développement**

### **URLs et Ports**
- **Frontend React** : http://localhost:3001
- **Backend Flask** : http://localhost:5000
- **Proxy API** : `/api/*` → `localhost:5000`

### **Commandes de Lancement**
```powershell
# Backend (Terminal 1)
cd backend; python run.py

# Frontend (Terminal 2)  
cd frontend; npm run dev
```

### **Vérification APIs**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/chantiers"
Invoke-RestMethod -Uri "http://localhost:5000/api/villes?per_page=5"
Invoke-RestMethod -Uri "http://localhost:5000/health"
```

---

## 📊 **Métriques et Performance**

### **État Actuel (02/07/2025)**
- **Base de données** : 792 enregistrements sur 13 tables
- **Code Backend** : ~15 000 lignes Python
- **Code Frontend** : ~8 000 lignes React
- **Documentation** : Restructurée en 5 thèmes

### **Objectifs Performance**
- **< 2s** temps de réponse toutes APIs
- **Concurrent users** : Julien + Yann sans conflits
- **100% compatibilité** développement ↔ production

---

## 🔄 **Évolution et Migration**

### **Phase 1 - Remplacement Excel** (Mi-octobre 2025)
- **Objectif** : 17 onglets Excel → 0
- **7 modules critiques** à terminer
- **Application web complète** opérationnelle

### **Phase 2 - Logiciel Métier** (2026)
- **Migration** SQLite → PostgreSQL
- **Intégration** BATAPPLI + LISP AutoCAD
- **Authentification** multi-utilisateur

### **Phase 3 - IA Automatisation** (2027)
- **IA efficace** avec accès code
- **Prédictions** et optimisations métier
- **Auto-amélioration** système

---

## 📚 **Documentation Associée**

### **APIs et Données**
- **[API_ENDPOINTS.md](API_ENDPOINTS.md)** - 30+ endpoints documentés
- **[DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)** - Schéma SQLAlchemy complet

### **Guides Techniques**
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production et staging
- **[Standards Dev](../03-regles-standards/STANDARDS_DEV.md)** - Règles développement

### **Projet Global**
- **[DEV_MASTER](../01-guides-principaux/DEV_MASTER.md)** - Document central
- **[QUICK_START](../01-guides-principaux/QUICK_START.md)** - Lancement 2 minutes

---

*Architecture maintenue par l'équipe ATARYS - Fondations solides pour 3 phases* 