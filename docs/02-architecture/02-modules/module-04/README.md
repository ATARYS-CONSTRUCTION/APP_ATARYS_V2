# 🏠 Module 4 - CHANTIERS

> **Suivi détaillé des chantiers, notes et gestion des commandes**  
> **État : STRUCTURE CRÉÉE** 📋 - Modèles à définir  
> Dernière mise à jour : 19/07/2025

---

## 🎯 Vue d'ensemble

Le module **4 - CHANTIERS** gère le suivi détaillé des chantiers en cours, incluant les notes de chantier, la gestion des commandes et les documents associés.

### **Objectifs Principaux**
- Suivi détaillé des chantiers
- Gestion des notes
- Gestion des commandes
- Documents associés

---

## 📋 État d'Implémentation

### **✅ Implémenté**
- **Structure de fichier** : `module_4.py` créé
- **Pattern BaseModel** : Prêt pour les modèles

### **❌ À Implémenter**
- **Tables principales** : SuiviChantier, NotesChantier, Commandes
- **API REST** : Endpoints à créer
- **Interface Frontend** : Composants React à développer
- **Logique métier** : Workflow de suivi

---

## 🏗️ Architecture Technique

### **Fichiers Concernés**
```
backend/app/models/module_4.py      # Modèles SQLAlchemy (structure créée)
backend/app/routes/module_4.py      # API REST (à créer)
backend/app/schemas/module_4.py     # Validation Marshmallow (à créer)
frontend/src/pages/Module4/         # Interface React (à créer)
```

### **Dépendances Critiques**
- **Module 3** : LISTE CHANTIERS (relation chantier parent)
- **Module 1** : PLANNING (planification détaillée)
- **Module 9** : SOCIAL (intervenants)

---

## 📊 Sous-modules

Selon `ATARYS_MODULES.md`, le module 4 comprend :

### **4.1 - SUIVI DE CHANTIER** ❌ **À IMPLÉMENTER**
- Suivi détaillé des chantiers
- Avancement des travaux
- Contrôle qualité
- Reporting d'activité

### **4.2 - NOTES DE CHANTIER** ❌ **À IMPLÉMENTER**
- Gestion des notes
- Observations quotidiennes
- Incidents et problèmes
- Historique des interventions

### **4.3 - COMMANDES** ❌ **À IMPLÉMENTER**
- Gestion des commandes matériaux
- Suivi des livraisons
- Validation des réceptions
- Gestion des stocks chantier

### **4.4 - DOCUMENTS** ❌ **À IMPLÉMENTER**
- Documents associés au chantier
- Photos et rapports
- Plans et schémas
- Certificats et validations

---

## 🗄️ Structure de Données Proposée

### **Table Principale : SuiviChantier**
```python
class SuiviChantier(BaseModel):
    __tablename__ = 'suivi_chantier'
    
    # Relations
    chantier_id = db.Column(db.Integer, db.ForeignKey('chantiers.id'))
    
    # Suivi
    date_suivi = db.Column(db.Date, nullable=False)
    avancement_pct = db.Column(db.Numeric(5, 2))
    
    # Météo et conditions
    meteo = db.Column(db.String(50))
    temperature = db.Column(db.Integer)
    conditions_travail = db.Column(db.String(100))
    
    # Équipe présente
    nb_ouvriers = db.Column(db.Integer)
    heures_travaillees = db.Column(db.Numeric(5, 2))
    
    # Observations
    travaux_realises = db.Column(db.Text)
    problemes_rencontres = db.Column(db.Text)
    notes_generales = db.Column(db.Text)
    
    # Relations
    chantier = db.relationship('Chantiers', backref='suivis')
```

### **Notes de Chantier**
```python
class NotesChantier(BaseModel):
    __tablename__ = 'notes_chantier'
    
    chantier_id = db.Column(db.Integer, db.ForeignKey('chantiers.id'))
    
    date_note = db.Column(db.Date, nullable=False)
    type_note = db.Column(db.String(50))  # OBSERVATION, INCIDENT, QUALITE
    
    titre = db.Column(db.String(200))
    contenu = db.Column(db.Text, nullable=False)
    
    auteur = db.Column(db.String(100))
    priorite = db.Column(db.String(10), default='NORMALE')
    statut = db.Column(db.String(20), default='OUVERTE')
    
    # Relations
    chantier = db.relationship('Chantiers', backref='notes')
```

### **Commandes Chantier**
```python
class CommandesChantier(BaseModel):
    __tablename__ = 'commandes_chantier'
    
    chantier_id = db.Column(db.Integer, db.ForeignKey('chantiers.id'))
    
    numero_commande = db.Column(db.String(50), unique=True)
    fournisseur = db.Column(db.String(200))
    
    date_commande = db.Column(db.Date, nullable=False)
    date_livraison_prevue = db.Column(db.Date)
    date_livraison_reelle = db.Column(db.Date)
    
    montant_ht = db.Column(db.Numeric(10, 2))
    statut = db.Column(db.String(20), default='COMMANDEE')
    # COMMANDEE, LIVREE, RECUE, FACTUREE
    
    description = db.Column(db.Text)
    notes = db.Column(db.Text)
```

---

## 🛣️ API Endpoints Proposées

### **Suivi de Chantier**
```http
GET    /api/module-4/suivi/:chantier_id     # Suivi d'un chantier
POST   /api/module-4/suivi                  # Nouveau suivi
PUT    /api/module-4/suivi/:id              # Modification suivi
DELETE /api/module-4/suivi/:id              # Suppression suivi
```

### **Notes de Chantier**
```http
GET    /api/module-4/notes/:chantier_id     # Notes d'un chantier
POST   /api/module-4/notes                  # Nouvelle note
PUT    /api/module-4/notes/:id              # Modification note
DELETE /api/module-4/notes/:id              # Suppression note
```

### **Commandes**
```http
GET    /api/module-4/commandes/:chantier_id # Commandes d'un chantier
POST   /api/module-4/commandes              # Nouvelle commande
PUT    /api/module-4/commandes/:id          # Modification commande
PUT    /api/module-4/commandes/:id/statut   # Changement statut
```

---

## 🎯 Priorités de Développement

### **Phase 1 : Base**
1. **Modèle SuiviChantier** : Table principale
2. **NotesChantier** : Système de notes
3. **API CRUD** : Opérations de base

### **Phase 2 : Enrichissement**
1. **Commandes** : Gestion des achats
2. **Documents** : Gestion des fichiers
3. **Reporting** : Tableaux de bord

### **Phase 3 : Intégration**
1. **Relations** : Avec autres modules
2. **Workflow** : Automatisation
3. **Mobile** : Application terrain

---

## 🔗 Liens Utiles

- **[Modèles SQLAlchemy](./database-schema.md)** - Structure détaillée des tables
- **[API Endpoints](./api-endpoints.md)** - Spécifications REST complètes
- **[Règles Métier](./business-rules.md)** - Workflows et validations
- **[ATARYS_MODULES.md](../../00-overview/ATARYS_MODULES.md)** - Nomenclature officielle
