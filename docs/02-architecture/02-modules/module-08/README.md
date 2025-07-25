# 💰 Module 8 - COMPTABILITÉ

> **Gestion de la TVA et tableaux de bord comptables**  
> **État : STRUCTURE CRÉÉE** 📋 - Modèles à définir  
> Dernière mise à jour : 19/07/2025

---

## 🎯 Vue d'ensemble

Le module **8 - COMPTABILITÉ** gère les aspects comptables et financiers de l'entreprise ATARYS, incluant la gestion de la TVA et les tableaux de bord comptables.

### **Objectifs Principaux**
- Gestion de la TVA
- Tableaux de bord comptables
- Analyse financière
- Suivi des obligations fiscales

---

## 📊 Sous-modules

Selon `ATARYS_MODULES.md`, le module 8 comprend :

### **8.1 - TVA** ❌ **À IMPLÉMENTER**
- Gestion de la TVA
- Déclarations TVA
- Suivi des taux
- Calculs automatiques

### **8.2 - TABLEAU DE BORD** ❌ **À IMPLÉMENTER**
- Tableaux de bord comptables
- Analyse financière
- Indicateurs de performance
- Reporting comptable

---

## 🗄️ Structure de Données Proposée

### **Table Principale : TVA**
```python
class TVA(BaseModel):
    __tablename__ = 'tva'
    
    # Période
    periode = db.Column(db.String(7), nullable=False)  # YYYY-MM
    
    # TVA Collectée
    tva_collectee = db.Column(db.Numeric(10, 2))
    
    # TVA Déductible
    tva_deductible = db.Column(db.Numeric(10, 2))
    
    # TVA à payer/crédit
    tva_a_payer = db.Column(db.Numeric(10, 2))
    
    # Statut
    statut = db.Column(db.String(20), default='BROUILLON')
    date_declaration = db.Column(db.Date)
    
    # Notes
    notes = db.Column(db.Text)
```

---

## 🛣️ API Endpoints Proposées

### **Gestion TVA**
```http
GET    /api/module-8/tva                    # Données TVA
POST   /api/module-8/tva                    # Nouvelle période TVA
PUT    /api/module-8/tva/:id                # Modification
DELETE /api/module-8/tva/:id                # Suppression

GET    /api/module-8/tableaux-bord          # Tableaux de bord
```

---

## 🔗 Liens Utiles

- **[Modèles SQLAlchemy](./database-schema.md)** - Structure détaillée des tables
- **[API Endpoints](./api-endpoints.md)** - Spécifications REST complètes
- **[ATARYS_MODULES.md](../../00-overview/ATARYS_MODULES.md)** - Nomenclature officielle
