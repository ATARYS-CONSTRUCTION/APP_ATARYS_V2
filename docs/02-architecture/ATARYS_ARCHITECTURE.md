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

### **✅ Éléments 100% Opérationnels V2**
- **Frontend React** - Structure complète fonctionnelle (port 3000)
- **Documentation** - Architecture complète et cohérente
- **Nomenclature** - 13 modules ATARYS avec sous-modules définis
- **Standards** - Méthodologie Cursor stricte appliquée

### **📋 Référence Technique V1 Conservée**
- **Dossiers V1** - `0 APP ATARYS/` et `0 APP ATARYS - Copie/` pour référence
- **Scripts d'import** - Logique d'extraction Excel/CSV à adapter
- **Structure BDD** - Modèles SQLAlchemy comme base de réflexion

### **🔄 À Créer Entièrement en V2**
- **Backend Flask** - API REST structurée selon modules ATARYS (PRIORITÉ 1)
- **Base de données** - SQLite V2 propre à partir d'Excel à jour (PRIORITÉ 3)
- **Module 3.1** - LISTE CHANTIERS (interface + API)
- **Module 9.1** - Liste_salaries (interface + API)
- **Module 10.1** - CALCUL_ARDOISES (interface + API)

### **📋 Nomenclature Complète**
```
1. PLANNING          → 1.1 Planning Salariés, 1.2 Planning Chantier
2. LISTE DES TÂCHES  → 2.1 Yann, 2.2 Julien
3. LISTE CHANTIERS   → 3.1 Liste Chantiers, 3.2 Chantiers Projets, 3.3 Chantiers Signés, 3.4 Chantiers En Cours, 3.5 Chantiers Archives
4. CHANTIERS         → 4.1 Suivi de Chantier, 4.2 Notes de Chantier, 4.3 Commandes, 4.4 Documents
5. DEVIS-FACTURATION → 5.1 Ouvrages et articles BATAPPLI, 5.2 Fiche Mètres, 5.3 Devis MEXT, 5.4 Devis Type
6. ATELIER           → 6.1 Quincaillerie, 6.2 Consommables, 6.3 Camions, 6.4 Matériel, 6.5 Échafaudage
7. GESTION           → 7.1 Prévisionnel, 7.2 Synthèse Prévisionnelle, 7.3 Bilans
8. COMPTABILITÉ      → 8.1 TVA, 8.2 Tableau de Bord
9. SOCIAL            → 9.1 Liste_salaries, 9.2 Fiche mensuelle, 9.3 Récap et calculs
10. OUTILS           → 10.1 Calcul_Ardoises, 10.2 Calcul_structures, 10.3 Staravina, 10.4 Documents types
11. ARCHIVES         → Archivage automatique
12. PARAMÈTRES       → 12.1 Base de Données
13. AIDE             → 13.1 Documentation
```

---

## 🗄️ **Base de Données SQLAlchemy**

### **Structure Base de Données V2**
- **Organisation modulaire** : Selon nomenclature officielle `ATARYS_MODULES.md`
- **Source données** : Fichier Excel propre et à jour (à importer)
- **Base SQLite V2** : À créer entièrement selon standards V2
- **Migration** : Pas de migration V1, création propre depuis Excel
- **Standards** : SQLAlchemy 2.0+ avec BaseModel pattern

**Modules prioritaires à développer :**
- **Module 3.1** : LISTE CHANTIERS (priorité 1)
- **Module 9.1** : Liste_salaries (priorité 2)
- **Module 10.1** : CALCUL_ARDOISES (priorité 3)
- **Autres modules** : À développer selon roadmap Phase 1-3

### **🏗️ Workflow États Chantiers**
**9 États Définis :**
1. **Projet** → 2. **Modification** → 3. **En cours de signature** → 4. **Signature** → 5. **En cours** → 6. **À finir** → 7. **Terminé** ⇄ 8. **SAV** | 9. **Non abouti** (réactivable)

**Automatisation Tâches :**
- **Changement d'état** → **Génération automatique** des tâches `CHANTIER_RECURRENT`
- **Service Python** : `backend/app/services/etat_chantier_service.py` (à créer)
- **Types de tâches** : Administrative, Technique, Commerciale
- **Liaison** : Table `etats_taches_recurrentes` pour mapping automatique

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
- **Frontend React** : http://localhost:3000
- **Backend Flask** : http://localhost:5000 (à créer)
- **Proxy API** : `/api/*` → `localhost:5000`

### **Commandes de Lancement**
```powershell
# Frontend (Terminal 1) - OPÉRATIONNEL
cd frontend; npm run dev

# Backend (Terminal 2) - À CRÉER
cd backend; python run.py
```

### **Vérification APIs**
```powershell
# APIs à créer - exemples pour tests futurs
# Invoke-RestMethod -Uri "http://localhost:5000/api/health"
# Invoke-RestMethod -Uri "http://localhost:5000/api/status"

# Backend à créer en priorité 1
echo "Backend Flask à créer selon API_ENDPOINTS.md"
```

---

## 📊 **Métriques et Performance**

### **État Actuel V2 (05/07/2025)**
- **Frontend React** : Structure complète opérationnelle (port 3000)
- **Documentation** : Architecture complète et cohérente
- **Nomenclature** : 13 modules ATARYS définis avec sous-modules
- **Standards** : Méthodologie Cursor stricte appliquée

### **À Créer V2**
- **Backend Flask** : Structure complète (priorité 1)
- **Base SQLite V2** : Import depuis Excel propre (priorité 2)
- **APIs REST** : Selon spécifications modules prioritaires
- **Interfaces** : Modules 3.1, 9.1, 10.1

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
- **[ETATS_CHANTIERS_COMPLETS.md](ETATS_CHANTIERS_COMPLETS.md)** - Workflow détaillé des états

### **Guides Techniques**
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production et staging
- **[Standards Dev](../03-regles-standards/STANDARDS_DEV.md)** - Règles développement

### **Projet Global**
- **[DEV_MASTER](../01-guides-principaux/DEV_MASTER.md)** - Document central
- **[QUICK_START](../01-guides-principaux/QUICK_START.md)** - Lancement 2 minutes

---

*Architecture maintenue par l'équipe ATARYS - Fondations solides pour 3 phases* 