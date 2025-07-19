# 🗄️ Module 12 - Schéma Base de Données

> **Modèles SQLAlchemy pour PARAMÈTRES**  
> **État : EN COURS** ⚡ - Tables de test implémentées avec relations  
> Dernière mise à jour : 19/07/2025

---

## 📋 Tables Implémentées

### **TestAuditTable** ✅ OPÉRATIONNEL

```python
# backend/app/models/module_12.py
class TestAuditTable(BaseModel):
    __tablename__ = 'test_audit_table'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100))
    prix = db.Column(db.Float)
    actif = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TestAuditTable {self.id}>'
```

**Description :**
- Table de test pour l'audit et les fonctionnalités de base
- Champs de test avec différents types de données
- Timestamps automatiques
- Pattern BaseModel respecté

### **TestCle2** ✅ OPÉRATIONNEL

```python
# backend/app/models/module_12.py
class TestCle2(BaseModel):
    __tablename__ = 'test_cle2'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle = db.Column(db.String(30))
    
    # Clé étrangère avec contrainte
    niveau_qualification_id = db.Column(
        db.Integer,
        db.ForeignKey('niveau_qualification.id', ondelete='SET NULL'),
        nullable=True
    )
    
    # Relation avec NiveauQualification (Module 9)
    niveau_qualification = db.relationship(
        'NiveauQualification',
        backref=db.backref('test_cles', lazy=True)
    )
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<TestCle2 {self.id}>'
```

**Description :**
- Table de test avec relation vers Module 9 (LISTE_SALARIÉS)
- Clé étrangère avec contrainte `SET NULL`
- Relation bidirectionnelle avec backref
- Exemple de relation inter-modules

---

## 📊 Tables à Implémenter

### **ParametresSysteme** ❌ À CRÉER

```python
# Proposition de structure
class ParametresSysteme(BaseModel):
    __tablename__ = 'parametres_systeme'
    
    cle = db.Column(db.String(100), nullable=False, unique=True)
    valeur = db.Column(db.Text)
    type_valeur = db.Column(db.String(20), default='STRING')  # STRING, INTEGER, BOOLEAN, JSON
    description = db.Column(db.Text)
    module_id = db.Column(db.Integer)  # Module ATARYS concerné
    actif = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<ParametresSysteme {self.cle}>'
```

### **LogsAudit** ❌ À CRÉER

```python
# Proposition de structure
class LogsAudit(BaseModel):
    __tablename__ = 'logs_audit'
    
    action = db.Column(db.String(50), nullable=False)  # CREATE, UPDATE, DELETE
    table_name = db.Column(db.String(100), nullable=False)
    record_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)  # Utilisateur responsable
    donnees_avant = db.Column(db.JSON)  # État avant modification
    donnees_apres = db.Column(db.JSON)  # État après modification
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LogsAudit {self.action} {self.table_name}>'
```

### **TableDefinitions** ❌ À CRÉER

```python
# Proposition de structure pour le service de génération
class TableDefinitions(BaseModel):
    __tablename__ = 'table_definitions'
    
    nom_table = db.Column(db.String(100), nullable=False, unique=True)
    module_atarys = db.Column(db.Integer, nullable=False)  # 1-13
    schema_json = db.Column(db.JSON)  # Définition complète de la table
    statut = db.Column(db.String(20), default='ACTIVE')  # ACTIVE, DEPRECATED
    version = db.Column(db.Integer, default=1)
    
    def __repr__(self):
        return f'<TableDefinitions {self.nom_table}>'
```

---

## 🔗 Relations avec Autres Modules

### **Module 9 - LISTE_SALARIÉS** ✅ IMPLÉMENTÉ
```python
# Relation existante
TestCle2.niveau_qualification_id → NiveauQualification.id
```

### **Tous les Modules** (Service de Génération)
```python
# Relations dynamiques créées par le service
TableDefinitions.module_atarys → Modules ATARYS (1-13)
LogsAudit.table_name → Toutes les tables générées
```

---

## 🛠️ Service de Génération de Tables

### **TableGeneratorService** 🔄 EN COURS

Le service de génération automatique permet de créer dynamiquement :

1. **Modèles SQLAlchemy** : Classes avec BaseModel
2. **Routes API REST** : Endpoints CRUD standardisés
3. **Schémas Marshmallow** : Validation des données
4. **Migrations** : Scripts Flask-Migrate

### **Workflow de Génération**
```python
# Exemple de génération automatique
{
    "module_atarys": 3,
    "nom_table": "chantiers",
    "colonnes": [
        {"nom": "nom_chantier", "type": "String", "longueur": 200},
        {"nom": "adresse", "type": "Text"},
        {"nom": "budget", "type": "Numeric", "precision": "10,2"}
    ]
}
```

---

## 📏 Standards Techniques

### **Types de Données**
- **Configuration** : `db.Text` pour valeurs JSON
- **Clés système** : `db.String(100)` avec unique=True
- **Logs** : `db.JSON` pour données structurées
- **Timestamps** : `db.DateTime` avec default=utcnow

### **Contraintes**
- **Paramètres uniques** : Une seule valeur par clé système
- **Relations sécurisées** : `ondelete='SET NULL'` pour éviter les cascades
- **Validation JSON** : Schémas pour les données structurées

### **Index de Performance**
```sql
-- Index recommandés
CREATE INDEX idx_parametres_cle ON parametres_systeme(cle);
CREATE INDEX idx_logs_table ON logs_audit(table_name, timestamp);
CREATE INDEX idx_definitions_module ON table_definitions(module_atarys);
```
