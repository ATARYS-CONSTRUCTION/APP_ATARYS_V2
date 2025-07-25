# 📁 Module 11 - ARCHIVES

> **Archivage des chantiers, devis et factures avec conservation légale**  
> **État : STRUCTURE CRÉÉE** 📋 - Modèles à définir  
> Dernière mise à jour : 19/07/2025

---

## 🎯 Vue d'ensemble

Le module **11 - ARCHIVES** gère l'archivage et la conservation légale de tous les documents et données de l'entreprise ATARYS, assurant la traçabilité et le respect des obligations légales.

### **Objectifs Principaux**
- Archivage des chantiers
- Archivage des devis
- Archivage des factures
- Conservation légale

---

## 📋 État d'Implémentation

### **✅ Implémenté**
- **Structure de fichier** : `module_11.py` créé
- **Pattern BaseModel** : Prêt pour les modèles

### **❌ À Implémenter**
- **Tables principales** : Archives, Documents, Conservation
- **API REST** : Endpoints à créer
- **Interface Frontend** : Composants React à développer
- **Logique métier** : Règles de conservation

---

## 📊 Fonctionnalités

Selon `ATARYS_MODULES.md`, le module 11 comprend :

### **Archivage Automatique** ❌ **À IMPLÉMENTER**
- Archivage des chantiers terminés
- Archivage des devis expirés ou refusés
- Archivage des factures payées
- Sauvegarde automatique des documents

### **Conservation Légale** ❌ **À IMPLÉMENTER**
- Respect des durées de conservation légales
- Classification par type de document
- Gestion des dates de destruction
- Audit et traçabilité

---

## 🗄️ Structure de Données Proposée

### **Table Principale : Archives**
```python
class Archives(BaseModel):
    __tablename__ = 'archives'
    
    # Document source
    type_document = db.Column(db.String(50), nullable=False)
    # CHANTIER, DEVIS, FACTURE, CONTRAT, CORRESPONDANCE
    
    document_id = db.Column(db.Integer, nullable=False)
    document_reference = db.Column(db.String(100))
    
    # Archivage
    date_archivage = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    motif_archivage = db.Column(db.String(100))
    
    # Conservation légale
    duree_conservation_annees = db.Column(db.Integer)
    date_destruction_prevue = db.Column(db.Date)
    statut_conservation = db.Column(db.String(20), default='ACTIVE')
    # ACTIVE, A_DETRUIRE, DETRUITE, CONSERVATION_PERMANENTE
    
    # Métadonnées
    taille_fichier = db.Column(db.BigInteger)  # En octets
    chemin_stockage = db.Column(db.String(500))
    checksum = db.Column(db.String(64))  # Pour vérifier l'intégrité
    
    # Indexation
    mots_cles = db.Column(db.Text)
    description = db.Column(db.Text)
    
    # Audit
    archive_par = db.Column(db.String(100))
    derniere_verification = db.Column(db.Date)
```

### **Règles de Conservation**
```python
class ReglesConservation(BaseModel):
    __tablename__ = 'regles_conservation'
    
    type_document = db.Column(db.String(50), nullable=False, unique=True)
    duree_conservation_annees = db.Column(db.Integer, nullable=False)
    
    # Règles spéciales
    conservation_permanente = db.Column(db.Boolean, default=False)
    destruction_automatique = db.Column(db.Boolean, default=True)
    
    # Références légales
    base_legale = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    # Métadonnées
    derniere_mise_a_jour = db.Column(db.Date)
    mise_a_jour_par = db.Column(db.String(100))
```

---

## 🛣️ API Endpoints Proposées

### **Gestion des Archives**
```http
GET    /api/module-11/archives              # Liste des archives
POST   /api/module-11/archives              # Archiver un document
GET    /api/module-11/archives/:id          # Détail archive
PUT    /api/module-11/archives/:id          # Modification métadonnées
DELETE /api/module-11/archives/:id          # Destruction définitive

GET    /api/module-11/archives/search       # Recherche dans les archives
GET    /api/module-11/archives/a-detruire   # Documents à détruire
```

### **Règles de Conservation**
```http
GET    /api/module-11/regles-conservation   # Règles de conservation
PUT    /api/module-11/regles-conservation/:type # Modification règle
```

### **Maintenance**
```http
POST   /api/module-11/maintenance/verification # Vérification intégrité
POST   /api/module-11/maintenance/nettoyage    # Nettoyage automatique
GET    /api/module-11/stats                    # Statistiques d'archivage
```

---

## 📏 Règles de Conservation Légales

### **Durées de Conservation Standard**
```
- Chantiers : 10 ans (garantie décennale)
- Devis : 5 ans
- Factures : 10 ans (obligations comptables)
- Contrats : 5 ans après fin de contrat
- Correspondances : 5 ans
- Documents sociaux : 50 ans
- Documents comptables : 10 ans
```

### **Processus d'Archivage**
1. **Déclenchement automatique** : Selon statut du document
2. **Classification** : Application des règles de conservation
3. **Stockage sécurisé** : Avec checksum d'intégrité
4. **Indexation** : Mots-clés et métadonnées
5. **Planification destruction** : Selon durées légales

---

## 🎯 Priorités de Développement

### **Phase 1 : Base**
1. **Modèle Archives** : Structure principale
2. **Règles conservation** : Configuration légale
3. **API archivage** : Fonctions de base

### **Phase 2 : Automatisation**
1. **Archivage automatique** : Déclencheurs
2. **Vérification intégrité** : Contrôles périodiques
3. **Interface recherche** : Consultation archives

### **Phase 3 : Conformité**
1. **Audit complet** : Traçabilité
2. **Destruction automatique** : Respect des délais
3. **Reporting légal** : Conformité réglementaire

---

## 🔗 Liens Utiles

- **[Modèles SQLAlchemy](./database-schema.md)** - Structure détaillée des tables
- **[API Endpoints](./api-endpoints.md)** - Spécifications REST complètes
- **[Règles Légales](./conservation-legale.md)** - Obligations et durées
- **[ATARYS_MODULES.md](../../00-overview/ATARYS_MODULES.md)** - Nomenclature officielle
