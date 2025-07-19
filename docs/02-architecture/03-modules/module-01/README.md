# 📅 Module 1 - PLANNING

> **Gestion du planning des salariés et des chantiers**  
> **État : STRUCTURE CRÉÉE** 📋 - Modèles à définir  
> Dernière mise à jour : 19/07/2025

---

## 🎯 Vue d'ensemble

Le module **1 - PLANNING** gère l'organisation temporelle de l'entreprise ATARYS. Il permet de planifier les interventions des salariés sur les chantiers avec une vue calendaire complète.

### **Objectifs Principaux**
- Planning des chantiers
- Affectation des salariés
- Vue calendaire
- Gestion des interventions

---

## 📋 État d'Implémentation

### **✅ Implémenté**
- **Structure de fichier** : `module_1.py` créé
- **Pattern BaseModel** : Prêt pour les modèles

### **🔄 En Cours**
- **Modèles SQLAlchemy** : À définir selon besoins métier
- **API REST** : Endpoints à créer
- **Interface Frontend** : Composants React à développer

### **❌ À Implémenter**
- **Tables principales** : Planning, Affectations, Interventions
- **Relations** : Avec chantiers et salariés
- **Logique métier** : Calendrier et disponibilités

---

## 🏗️ Architecture Technique

### **Fichiers Concernés**
```
backend/app/models/module_1.py      # Modèles SQLAlchemy (structure créée)
backend/app/routes/module_1.py      # API REST (à créer)
backend/app/schemas/module_1.py     # Validation Marshmallow (à créer)
frontend/src/pages/Module1/         # Interface React (à créer)
```

### **Dépendances Critiques**
- **Module 3** : LISTE CHANTIERS (planning par chantier)
- **Module 9** : SOCIAL (affectation des salariés)
- **Module 4** : CHANTIERS (suivi détaillé)

---

## 📊 Sous-modules

Selon `ATARYS_MODULES.md`, le module 1 comprend :

### **1.1 - PLANNING SALARIÉS** ❌ **À IMPLÉMENTER**
- Planning des chantiers
- Affectation des salariés
- Vue calendaire
- Gestion des interventions

### **1.2 - PLANNING CHANTIER** ❌ **À IMPLÉMENTER**
- Planning spécifique par chantier
- Séquençage des tâches
- Suivi des délais
- Coordination des équipes

---

## 🗄️ Structure de Données Proposée

### **Table Principale : PlanningChantier**
```python
class PlanningChantier(BaseModel):
    __tablename__ = 'planning_chantier'
    
    # Relations
    chantier_id = db.Column(db.Integer, db.ForeignKey('chantiers.id'))
    salarie_id = db.Column(db.Integer, db.ForeignKey('salaries.id'))
    
    # Planification
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    heure_debut = db.Column(db.Time)
    heure_fin = db.Column(db.Time)
    
    # Description
    tache = db.Column(db.String(200))
    notes = db.Column(db.Text)
    statut = db.Column(db.String(20), default='PLANIFIE')
    
    # Relations
    chantier = db.relationship('Chantiers', backref='plannings')
    salarie = db.relationship('Salarie', backref='plannings')
```

### **Affectations Salariés**
```python
class AffectationSalarie(BaseModel):
    __tablename__ = 'affectation_salarie'
    
    salarie_id = db.Column(db.Integer, db.ForeignKey('salaries.id'))
    date_affectation = db.Column(db.Date, nullable=False)
    disponibilite = db.Column(db.String(20), default='DISPONIBLE')
    notes = db.Column(db.Text)
```

---

## 🛣️ API Endpoints Proposées

### **Gestion du Planning**
```http
GET    /api/module-1/planning              # Vue calendaire complète
POST   /api/module-1/planning              # Nouvelle planification
PUT    /api/module-1/planning/:id          # Modification planning
DELETE /api/module-1/planning/:id          # Suppression

GET    /api/module-1/planning/salarie/:id  # Planning d'un salarié
GET    /api/module-1/planning/chantier/:id # Planning d'un chantier
```

### **Disponibilités**
```http
GET    /api/module-1/disponibilites        # Disponibilités des salariés
PUT    /api/module-1/disponibilites/:id    # Mise à jour disponibilité
```

---

## 🎯 Priorités de Développement

### **Phase 1 : Base**
1. **Modèle PlanningChantier** : Table principale
2. **API CRUD** : Opérations de base
3. **Vue calendaire** : Interface simple

### **Phase 2 : Enrichissement**
1. **Relations** : Avec chantiers et salariés
2. **Disponibilités** : Gestion des congés et absences
3. **Notifications** : Alertes de planning

### **Phase 3 : Avancé**
1. **Optimisation** : Algorithmes d'affectation
2. **Intégration** : Avec autres modules
3. **Reporting** : Statistiques et analyses

---

## 🔗 Liens Utiles

- **[Modèles SQLAlchemy](./database-schema.md)** - Structure détaillée des tables
- **[API Endpoints](./api-endpoints.md)** - Spécifications REST complètes
- **[Règles Métier](./business-rules.md)** - Workflows et validations
- **[ATARYS_MODULES.md](../../00-overview/ATARYS_MODULES.md)** - Nomenclature officielle
