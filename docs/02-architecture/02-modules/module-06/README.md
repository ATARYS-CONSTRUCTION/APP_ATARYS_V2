# 🔧 Module 6 - ATELIER

> **Gestion de la quincaillerie, consommables, camions et matériel**  
> **État : STRUCTURE CRÉÉE** 📋 - Modèles à définir  
> Dernière mise à jour : 19/07/2025

---

## 🎯 Vue d'ensemble

Le module **6 - ATELIER** gère l'ensemble des ressources matérielles de l'entreprise ATARYS, incluant la quincaillerie, les consommables, les camions, le matériel et l'échafaudage.

### **Objectifs Principaux**
- Gestion de la quincaillerie
- Suivi des consommables
- Gestion des camions
- Matériel d'atelier
- Gestion de l'échafaudage

---

## 📊 Sous-modules

Selon `ATARYS_MODULES.md`, le module 6 comprend :

### **6.1 - QUINCAILLERIE** ❌ **À IMPLÉMENTER**
- Gestion de la quincaillerie
- Stock et inventaire
- Commandes et réapprovisionnement

### **6.2 - CONSOMMABLES** ❌ **À IMPLÉMENTER**
- Suivi des consommables
- Gestion des stocks
- Contrôle des coûts

### **6.3 - CAMIONS** ❌ **À IMPLÉMENTER**
- Gestion des camions
- Maintenance et contrôles
- Planification d'utilisation

### **6.4 - MATÉRIEL** ❌ **À IMPLÉMENTER**
- Matériel d'atelier
- Outils et équipements
- Maintenance préventive

### **6.5 - ÉCHAFAUDAGE** ❌ **À IMPLÉMENTER**
- Gestion de l'échafaudage
- Location et propriété
- Montage et démontage

---

## 🗄️ Structure de Données Proposée

### **Table Principale : Materiel**
```python
class Materiel(BaseModel):
    __tablename__ = 'materiel'
    
    # Identification
    reference = db.Column(db.String(50), nullable=False, unique=True)
    nom = db.Column(db.String(200), nullable=False)
    type_materiel = db.Column(db.String(50))  # QUINCAILLERIE, CONSOMMABLE, CAMION, OUTIL, ECHAFAUDAGE
    
    # Caractéristiques
    marque = db.Column(db.String(100))
    modele = db.Column(db.String(100))
    description = db.Column(db.Text)
    
    # Gestion
    statut = db.Column(db.String(20), default='DISPONIBLE')
    localisation = db.Column(db.String(100))
    
    # Financier
    prix_achat = db.Column(db.Numeric(10, 2))
    date_achat = db.Column(db.Date)
    amortissement = db.Column(db.Numeric(10, 2))
    
    # Stock (pour consommables/quincaillerie)
    stock_actuel = db.Column(db.Integer)
    stock_minimum = db.Column(db.Integer)
    unite = db.Column(db.String(10))
```

---

## 🛣️ API Endpoints Proposées

### **Gestion du Matériel**
```http
GET    /api/module-6/materiel               # Liste du matériel
POST   /api/module-6/materiel               # Nouveau matériel
PUT    /api/module-6/materiel/:id           # Modification
DELETE /api/module-6/materiel/:id           # Suppression

GET    /api/module-6/materiel/quincaillerie # Quincaillerie uniquement
GET    /api/module-6/materiel/camions       # Camions uniquement
GET    /api/module-6/materiel/echafaudage   # Échafaudage uniquement
```

---

## 🔗 Liens Utiles

- **[Modèles SQLAlchemy](./database-schema.md)** - Structure détaillée des tables
- **[API Endpoints](./api-endpoints.md)** - Spécifications REST complètes
- **[ATARYS_MODULES.md](../../00-overview/ATARYS_MODULES.md)** - Nomenclature officielle
