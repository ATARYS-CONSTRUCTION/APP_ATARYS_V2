# 🏗️ Module 3 - LISTE CHANTIERS

> **Gestion des chantiers clients avec pipeline commercial complet**  
> **État : STRUCTURE CRÉÉE** 📋 - Modèles à définir  
> Dernière mise à jour : 19/07/2025

---

## 🎯 Vue d'ensemble

Le module **3 - LISTE CHANTIERS** gère l'ensemble du pipeline commercial des chantiers ATARYS, depuis les projets en prospection jusqu'aux chantiers archivés.

### **Objectifs Principaux**
- Gestion des chantiers clients
- Suivi des états (Projet, Signé, En cours, Terminé, Annulé)
- Pipeline commercial complet
- Vue par statut

---

## 📋 État d'Implémentation

### **✅ Implémenté**
- **Structure de fichier** : `module_3.py` créé
- **Pattern BaseModel** : Prêt pour les modèles

### **🔄 En Cours**
- **Modèles SQLAlchemy** : À définir selon besoins métier
- **API REST** : Endpoints à créer
- **Interface Frontend** : Composants React à développer

### **❌ À Implémenter**
- **Tables principales** : Chantiers, États, Pipeline
- **Relations** : Avec clients et devis
- **Logique métier** : Workflows commerciaux

---

## 🏗️ Architecture Technique

### **Fichiers Concernés**
```
backend/app/models/module_3.py      # Modèles SQLAlchemy (structure créée)
backend/app/routes/module_3.py      # API REST (à créer)
backend/app/schemas/module_3.py     # Validation Marshmallow (à créer)
frontend/src/pages/Module3/         # Interface React (à créer)
```

### **Dépendances Critiques**
- **Module 5** : DEVIS-FACTURATION (relation chantier → devis)
- **Module 1** : PLANNING (planification chantiers)
- **Module 4** : CHANTIERS (suivi détaillé)

---

## 📊 Sous-modules

Selon `ATARYS_MODULES.md`, le module 3 comprend :

### **3.1 - LISTE CHANTIERS** ❌ **À IMPLÉMENTER**
- Vue d'ensemble de tous les chantiers
- Filtrage par état, client, période
- Recherche avancée
- Tableau de bord commercial

### **3.2 - CHANTIERS PROJETS** ❌ **À IMPLÉMENTER**
- Chantiers en phase de prospection
- Suivi des opportunités
- Conversion en chantiers signés
- Pipeline commercial

### **3.3 - CHANTIERS SIGNÉS** ❌ **À IMPLÉMENTER**
- Chantiers confirmés et contractualisés
- Préparation et planification
- Transition vers "En cours"
- Gestion administrative

### **3.4 - CHANTIERS EN COURS** ❌ **À IMPLÉMENTER**
- Chantiers actifs en réalisation
- Suivi d'avancement
- Gestion des interventions
- Reporting temps réel

### **3.5 - CHANTIERS ARCHIVES** ❌ **À IMPLÉMENTER**
- Chantiers terminés ou annulés
- Conservation des données
- Historique et références
- Analyses post-projet

---

## 🗄️ Structure de Données Proposée

### **Table Principale : Chantiers**
```python
class Chantiers(BaseModel):
    __tablename__ = 'chantiers'
    
    # Identification
    numero_chantier = db.Column(db.String(50), nullable=False, unique=True)
    nom_chantier = db.Column(db.String(200), nullable=False)
    
    # Localisation
    adresse = db.Column(db.Text)
    ville = db.Column(db.String(100))
    code_postal = db.Column(db.String(10))
    
    # Relations (à définir selon autres modules)
    client_id = db.Column(db.Integer)  # Relation future avec module clients
    
    # États et workflow
    statut = db.Column(db.String(30), default='PROJET')
    # PROJET, SIGNE, EN_COURS, TERMINE, ANNULE, ARCHIVE
    
    # Dates
    date_creation = db.Column(db.Date, default=datetime.utcnow)
    date_signature = db.Column(db.Date)
    date_debut_prevue = db.Column(db.Date)
    date_fin_prevue = db.Column(db.Date)
    date_debut_reelle = db.Column(db.Date)
    date_fin_reelle = db.Column(db.Date)
    
    # Financier
    montant_estime = db.Column(db.Numeric(10, 2))
    montant_signe = db.Column(db.Numeric(10, 2))
    
    # Suivi
    avancement_pct = db.Column(db.Numeric(5, 2), default=0.00)
    notes = db.Column(db.Text)
    priorite = db.Column(db.String(10), default='NORMALE')
```

### **États des Chantiers**
```python
class EtatChantier(BaseModel):
    __tablename__ = 'etat_chantier'
    
    code = db.Column(db.String(20), nullable=False, unique=True)
    libelle = db.Column(db.String(100), nullable=False)
    couleur = db.Column(db.String(7))  # Code couleur hex
    ordre = db.Column(db.Integer)  # Ordre dans le pipeline
    actif = db.Column(db.Boolean, default=True)
```

---

## 🛣️ API Endpoints Proposées

### **Gestion des Chantiers**
```http
GET    /api/module-3/chantiers              # Liste avec filtres et pagination
POST   /api/module-3/chantiers              # Création nouveau chantier
GET    /api/module-3/chantiers/:id          # Détail d'un chantier
PUT    /api/module-3/chantiers/:id          # Modification chantier
DELETE /api/module-3/chantiers/:id          # Suppression (soft delete)
```

### **Pipeline Commercial**
```http
GET    /api/module-3/chantiers/projets      # Chantiers en prospection
GET    /api/module-3/chantiers/signes       # Chantiers signés
GET    /api/module-3/chantiers/en-cours     # Chantiers actifs
GET    /api/module-3/chantiers/archives     # Chantiers archivés
```

### **Gestion des États**
```http
GET    /api/module-3/etats                  # Liste des états disponibles
PUT    /api/module-3/chantiers/:id/etat     # Changement d'état
```

### **Statistiques et Reporting**
```http
GET    /api/module-3/stats/pipeline         # Statistiques du pipeline
GET    /api/module-3/stats/chiffre-affaires # CA par période et statut
GET    /api/module-3/stats/conversion       # Taux de conversion
```

---

## 🎯 Priorités de Développement

### **Phase 1 : Base (Priorité 1)**
1. **Modèle Chantiers** : Table principale avec statuts
2. **API CRUD** : Opérations de base
3. **États simples** : PROJET, SIGNE, EN_COURS, TERMINE

### **Phase 2 : Pipeline (Priorité 2)**
1. **Workflow** : Transitions d'états automatisées
2. **Vues par statut** : Interfaces spécialisées
3. **Filtrage avancé** : Recherche multi-critères

### **Phase 3 : Intégration (Priorité 3)**
1. **Relations** : Avec clients, devis, planning
2. **Reporting** : Tableaux de bord et KPI
3. **Automatisation** : Notifications et alertes

---

## 🔗 Liens Utiles

- **[Modèles SQLAlchemy](./database-schema.md)** - Structure détaillée des tables
- **[API Endpoints](./api-endpoints.md)** - Spécifications REST complètes
- **[Règles Métier](./business-rules.md)** - Workflows et validations
- **[ATARYS_MODULES.md](../../00-overview/ATARYS_MODULES.md)** - Nomenclature officielle
