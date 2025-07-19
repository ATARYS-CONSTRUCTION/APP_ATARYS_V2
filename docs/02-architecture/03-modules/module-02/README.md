# 📋 Module 2 - LISTE DES TÂCHES

> **Gestion des listes de tâches personnalisées par utilisateur**  
> **État : STRUCTURE CRÉÉE** 📋 - Modèles à définir  
> Dernière mise à jour : 19/07/2025

---

## 🎯 Vue d'ensemble

Le module **2 - LISTE DES TÂCHES** gère les listes de tâches personnalisées pour chaque utilisateur du système ATARYS, permettant un suivi individuel et une priorisation des activités.

### **Objectifs Principaux**
- Liste de tâches personnalisées
- Suivi par utilisateur
- Priorisation des tâches
- Organisation du travail individuel

---

## 📋 État d'Implémentation

### **✅ Implémenté**
- **Structure de fichier** : `module_2.py` créé
- **Pattern BaseModel** : Prêt pour les modèles

### **❌ À Implémenter**
- **Tables principales** : Tâches, Utilisateurs, Priorités
- **API REST** : Endpoints à créer
- **Interface Frontend** : Composants React à développer
- **Logique métier** : Gestion des priorités et statuts

---

## 🏗️ Architecture Technique

### **Fichiers Concernés**
```
backend/app/models/module_2.py      # Modèles SQLAlchemy (structure créée)
backend/app/routes/module_2.py      # API REST (à créer)
backend/app/schemas/module_2.py     # Validation Marshmallow (à créer)
frontend/src/pages/Module2/         # Interface React (à créer)
```

---

## 📊 Sous-modules

Selon `ATARYS_MODULES.md`, le module 2 comprend :

### **2.1 - YANN** ❌ **À IMPLÉMENTER**
- Liste de tâches personnalisées pour Yann
- Suivi des activités spécifiques
- Priorisation individuelle

### **2.2 - JULIEN** ❌ **À IMPLÉMENTER**
- Liste de tâches personnalisées pour Julien
- Gestion des responsabilités de gérant
- Suivi des tâches administratives

---

## 🗄️ Structure de Données Proposée

### **Table Principale : Taches**
```python
class Taches(BaseModel):
    __tablename__ = 'taches'
    
    # Identification
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Assignation
    utilisateur = db.Column(db.String(50), nullable=False)  # YANN, JULIEN
    
    # Gestion
    statut = db.Column(db.String(20), default='A_FAIRE')
    # A_FAIRE, EN_COURS, TERMINE, REPORTE, ANNULE
    
    priorite = db.Column(db.String(10), default='NORMALE')
    # HAUTE, NORMALE, BASSE
    
    # Dates
    date_creation = db.Column(db.Date, default=datetime.utcnow)
    date_echeance = db.Column(db.Date)
    date_completion = db.Column(db.Date)
    
    # Suivi
    temps_estime = db.Column(db.Numeric(5, 2))  # En heures
    temps_passe = db.Column(db.Numeric(5, 2))   # En heures
    notes = db.Column(db.Text)
```

---

## 🛣️ API Endpoints Proposées

### **Gestion des Tâches**
```http
GET    /api/module-2/taches                 # Liste des tâches avec filtres
POST   /api/module-2/taches                 # Création nouvelle tâche
GET    /api/module-2/taches/:id             # Détail d'une tâche
PUT    /api/module-2/taches/:id             # Modification tâche
DELETE /api/module-2/taches/:id             # Suppression tâche

GET    /api/module-2/taches/yann            # Tâches de Yann
GET    /api/module-2/taches/julien          # Tâches de Julien
```

### **Gestion des Statuts**
```http
PUT    /api/module-2/taches/:id/statut      # Changement de statut
PUT    /api/module-2/taches/:id/priorite    # Changement de priorité
```

---

## 🎯 Priorités de Développement

### **Phase 1 : Base**
1. **Modèle Taches** : Table principale avec utilisateurs
2. **API CRUD** : Opérations de base
3. **Interface simple** : Liste et création

### **Phase 2 : Fonctionnalités**
1. **Filtrage** : Par utilisateur, statut, priorité
2. **Notifications** : Rappels d'échéances
3. **Statistiques** : Suivi de productivité

---

## 🔗 Liens Utiles

- **[Modèles SQLAlchemy](./database-schema.md)** - Structure détaillée des tables
- **[API Endpoints](./api-endpoints.md)** - Spécifications REST complètes
- **[ATARYS_MODULES.md](../../00-overview/ATARYS_MODULES.md)** - Nomenclature officielle
