# 👥 Module 9 - SOCIAL

> **Gestion des salariés, fiches mensuelles et calculs sociaux**  
> **État : STRUCTURE CRÉÉE** 📋 - Relations partielles avec module 12  
> Dernière mise à jour : 19/07/2025

---

## 🎯 Vue d'ensemble

Le module **9 - SOCIAL** gère l'ensemble de la gestion des ressources humaines de l'entreprise ATARYS, incluant les salariés, leurs fiches mensuelles et les calculs sociaux.

### **Objectifs Principaux**
- Gestion des salariés
- Fiches mensuelles
- Récapitulatifs et calculs sociaux
- Suivi des qualifications

---

## 📋 État d'Implémentation

### **✅ Implémenté**
- **Structure de fichier** : `module_9.py` créé
- **Pattern BaseModel** : Prêt pour les modèles
- **Relation existante** : `NiveauQualification` utilisé par module 12 (TestCle2)

### **❌ À Implémenter**
- **Tables principales** : Salaries, FichesMensuelles, Calculs
- **API REST** : Endpoints à créer
- **Interface Frontend** : Composants React à développer

---

## 📊 Sous-modules

Selon `ATARYS_MODULES.md`, le module 9 comprend :

### **9.1 - Liste_salaries** ❌ **À IMPLÉMENTER**
- Gestion des salariés
- Informations personnelles et professionnelles
- Qualifications et compétences
- Historique d'emploi

### **9.2 - Fiche mensuelle** ❌ **À IMPLÉMENTER**
- Fiches mensuelles des salariés
- Heures travaillées
- Congés et absences
- Évaluations

### **9.3 - Récap et calculs** ❌ **À IMPLÉMENTER**
- Récapitulatifs et calculs sociaux
- Charges sociales
- Bulletins de paie
- Déclarations sociales

---

## 🗄️ Structure de Données Proposée

### **Table Principale : Salaries**
```python
class Salaries(BaseModel):
    __tablename__ = 'salaries'
    
    # Identification
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    numero_employe = db.Column(db.String(20), unique=True)
    
    # Contact
    email = db.Column(db.String(200))
    telephone = db.Column(db.String(20))
    adresse = db.Column(db.Text)
    
    # Emploi
    poste = db.Column(db.String(100))
    date_embauche = db.Column(db.Date)
    date_fin_contrat = db.Column(db.Date)
    statut = db.Column(db.String(20), default='ACTIF')
    
    # Qualification
    niveau_qualification_id = db.Column(db.Integer, db.ForeignKey('niveau_qualification.id'))
    
    # Relations
    niveau_qualification = db.relationship('NiveauQualification', backref='salaries')
```

### **Relation existante : NiveauQualification**
```python
# Cette table existe déjà et est utilisée par module 12
class NiveauQualification(BaseModel):
    __tablename__ = 'niveau_qualification'
    
    code = db.Column(db.String(10), unique=True)
    libelle = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
```

---

## 🛣️ API Endpoints Proposées

### **Gestion des Salariés**
```http
GET    /api/module-9/salaries               # Liste des salariés
POST   /api/module-9/salaries               # Nouveau salarié
GET    /api/module-9/salaries/:id           # Détail d'un salarié
PUT    /api/module-9/salaries/:id           # Modification
DELETE /api/module-9/salaries/:id           # Suppression

GET    /api/module-9/qualifications         # Niveaux de qualification
```

---

## 🔗 Liens Utiles

- **[Modèles SQLAlchemy](./database-schema.md)** - Structure détaillée des tables
- **[API Endpoints](./api-endpoints.md)** - Spécifications REST complètes
- **[ATARYS_MODULES.md](../../00-overview/ATARYS_MODULES.md)** - Nomenclature officielle
