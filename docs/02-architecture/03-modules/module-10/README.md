# 🛠️ Module 10 - OUTILS

> **Calculs automatiques, structures et base de données Staravina**  
> **État : STRUCTURE CRÉÉE** 📋 - Modèles à définir  
> Dernière mise à jour : 19/07/2025

---

## 🎯 Vue d'ensemble

Le module **10 - OUTILS** fournit l'ensemble des outils de calcul et de référence de l'entreprise ATARYS, incluant les calculs d'ardoises, de structures, la base Staravina et les documents types.

### **Objectifs Principaux**
- Calculs automatiques ardoises
- Calculs de structures
- Base de données Staravina avec mots-clés
- Gestion des documents types

---

## 📊 Sous-modules

Selon `ATARYS_MODULES.md`, le module 10 comprend :

### **10.1 - CALCUL_ARDOISES** ❌ **À IMPLÉMENTER**
- Calculs automatiques ardoises
- Formules de calcul spécialisées
- Optimisation des quantités
- Devis automatisés

### **10.2 - Calcul_structures** ❌ **À IMPLÉMENTER**
- Calculs de structures
- Dimensionnement
- Résistance des matériaux
- Normes de construction

### **10.3 - Staravina (base de données avec mots-clés de la documentation)** ❌ **À IMPLÉMENTER**
- Base de données Staravina avec mots-clés
- Documentation technique
- Recherche par mots-clés
- Base de connaissances

### **10.4 - Documents types** ❌ **À IMPLÉMENTER**
- Gestion des documents types
- Templates et modèles
- Bibliothèque de documents
- Personnalisation

---

## 🗄️ Structure de Données Proposée

### **Table Principale : CalculsArdoises**
```python
class CalculsArdoises(BaseModel):
    __tablename__ = 'calculs_ardoises'
    
    # Projet
    nom_projet = db.Column(db.String(200), nullable=False)
    chantier_id = db.Column(db.Integer, db.ForeignKey('chantiers.id'))
    
    # Dimensions
    longueur = db.Column(db.Numeric(8, 2))
    largeur = db.Column(db.Numeric(8, 2))
    surface = db.Column(db.Numeric(10, 2))
    
    # Paramètres
    type_ardoise = db.Column(db.String(100))
    format_ardoise = db.Column(db.String(50))
    pureau = db.Column(db.Numeric(6, 2))
    
    # Résultats
    nb_ardoises = db.Column(db.Integer)
    nb_crochets = db.Column(db.Integer)
    poids_total = db.Column(db.Numeric(8, 2))
    
    # Coûts
    cout_materiel = db.Column(db.Numeric(10, 2))
    cout_main_oeuvre = db.Column(db.Numeric(10, 2))
    cout_total = db.Column(db.Numeric(10, 2))
```

### **Base Staravina**
```python
class Staravina(BaseModel):
    __tablename__ = 'staravina'
    
    # Document
    titre = db.Column(db.String(200), nullable=False)
    type_document = db.Column(db.String(50))
    categorie = db.Column(db.String(100))
    
    # Contenu
    contenu = db.Column(db.Text)
    mots_cles = db.Column(db.Text)  # Séparés par virgules
    
    # Métadonnées
    auteur = db.Column(db.String(100))
    date_creation = db.Column(db.Date)
    version = db.Column(db.String(10))
    
    # Recherche
    tags = db.Column(db.Text)
    popularite = db.Column(db.Integer, default=0)
```

---

## 🛣️ API Endpoints Proposées

### **Calculs Ardoises**
```http
GET    /api/module-10/calculs-ardoises      # Liste des calculs
POST   /api/module-10/calculs-ardoises      # Nouveau calcul
GET    /api/module-10/calculs-ardoises/:id  # Détail calcul
PUT    /api/module-10/calculs-ardoises/:id  # Modification
DELETE /api/module-10/calculs-ardoises/:id  # Suppression

POST   /api/module-10/calculs-ardoises/compute # Calcul automatique
```

### **Base Staravina**
```http
GET    /api/module-10/staravina             # Recherche dans la base
POST   /api/module-10/staravina             # Nouveau document
GET    /api/module-10/staravina/:id         # Détail document
PUT    /api/module-10/staravina/:id         # Modification
DELETE /api/module-10/staravina/:id         # Suppression

GET    /api/module-10/staravina/search      # Recherche par mots-clés
```

---

## 🎯 Priorités de Développement

### **Phase 1 : Calculs (Priorité 3 selon DEV_MASTER.md)**
1. **Calculs ardoises** : Algorithmes de base
2. **Interface calcul** : Saisie des paramètres
3. **Résultats** : Affichage et export

### **Phase 2 : Base Staravina**
1. **Structure** : Base de données documentaire
2. **Recherche** : Moteur de recherche par mots-clés
3. **Interface** : Consultation et ajout

### **Phase 3 : Intégration**
1. **Calculs structures** : Algorithmes avancés
2. **Documents types** : Bibliothèque complète
3. **Export** : Intégration avec devis

---

## 🔗 Liens Utiles

- **[Modèles SQLAlchemy](./database-schema.md)** - Structure détaillée des tables
- **[API Endpoints](./api-endpoints.md)** - Spécifications REST complètes
- **[Algorithmes de Calcul](./calculs-ardoises.md)** - Formules et méthodes
- **[ATARYS_MODULES.md](../../00-overview/ATARYS_MODULES.md)** - Nomenclature officielle
