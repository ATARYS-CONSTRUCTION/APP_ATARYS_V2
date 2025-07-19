# 🗄️ Module 5 - Schéma Base de Données

> **Modèles SQLAlchemy pour DEVIS_FACTURATION**  
> **État : EN COURS** ⚡ - FamilleOuvrages implémenté  
> Dernière mise à jour : 19/07/2025

---

## 📋 Tables Implémentées

### **FamilleOuvrages** ✅ OPÉRATIONNEL

```python
# backend/app/models/module_5.py
class FamilleOuvrages(BaseModel):
    __tablename__ = 'famille_ouvrages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num_bd_atarys = db.Column(db.String(10))
    libelle = db.Column(db.String(100), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<FamilleOuvrages {self.id}>"
```

**Description :**
- Gestion des familles d'ouvrages pour la facturation
- Référence ATARYS avec numérotation interne
- Libellé descriptif obligatoire
- Timestamps automatiques via BaseModel

---

## 📊 Tables à Implémenter

### **Articles** ❌ À CRÉER

```python
# Proposition de structure
class Articles(BaseModel):
    __tablename__ = 'articles'
    
    reference = db.Column(db.String(100), nullable=False, unique=True)
    libelle = db.Column(db.Text, nullable=False)
    prix_achat = db.Column(db.Numeric(10, 2))
    coefficient = db.Column(db.Numeric(10, 2))
    prix_unitaire = db.Column(db.Numeric(10, 2), nullable=False)
    unite = db.Column(db.String(10))
    tva_pct = db.Column(db.Numeric(5, 2), default=20.00)
    famille_id = db.Column(db.Integer, db.ForeignKey('famille_ouvrages.id'))
    actif = db.Column(db.Boolean, default=True)
    
    # Relations
    famille = db.relationship('FamilleOuvrages', backref='articles')
```

### **Devis** ❌ À CRÉER

```python
# Proposition de structure
class Devis(BaseModel):
    __tablename__ = 'devis'
    
    numero = db.Column(db.String(50), nullable=False, unique=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    date_creation = db.Column(db.Date, nullable=False)
    date_validite = db.Column(db.Date)
    montant_ht = db.Column(db.Numeric(10, 2))
    montant_ttc = db.Column(db.Numeric(10, 2))
    statut = db.Column(db.String(20), default='BROUILLON')
    
    # Relations
    client = db.relationship('Client', backref='devis')
    lignes = db.relationship('LigneDevis', backref='devis')
```

### **LigneDevis** ❌ À CRÉER

```python
# Proposition de structure
class LigneDevis(BaseModel):
    __tablename__ = 'ligne_devis'
    
    devis_id = db.Column(db.Integer, db.ForeignKey('devis.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    quantite = db.Column(db.Numeric(10, 3))
    prix_unitaire = db.Column(db.Numeric(10, 2))
    montant_ht = db.Column(db.Numeric(10, 2))
    
    # Relations
    article = db.relationship('Articles', backref='lignes_devis')
```

---

## 🔗 Relations avec Autres Modules

### **Module 6 - CLIENTS**
```python
# Relation ForeignKey
devis.client_id → clients.id
```

### **Module 7 - FOURNISSEURS**
```python
# Relation pour les achats
articles.fournisseur_id → fournisseurs.id
```

### **Module 12 - PARAMÈTRES**
```python
# Configuration TVA, coefficients
parametres.tva_defaut → articles.tva_pct
```

---

## 📏 Standards Techniques

### **Types de Données**
- **Montants financiers** : `db.Numeric(10, 2)` (précision exacte)
- **Pourcentages** : `db.Numeric(5, 2)` (ex: 20.00%)
- **Quantités** : `db.Numeric(10, 3)` (3 décimales)
- **Références** : `db.String(100)` avec contrainte unique
- **Descriptions** : `db.Text` pour contenu long

### **Contraintes**
- **Clés primaires** : Auto-increment obligatoire
- **Clés étrangères** : Avec `ondelete='SET NULL'`
- **Valeurs par défaut** : Définies au niveau SQLAlchemy
- **Index** : Sur les colonnes de recherche fréquente

### **Validation**
- **Montants positifs** : Contraintes CHECK à ajouter
- **Dates cohérentes** : date_validite > date_creation
- **Statuts** : Enum pour les valeurs autorisées
