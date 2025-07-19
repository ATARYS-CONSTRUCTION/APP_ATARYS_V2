# ❓ Module 13 - AIDE

> **Documentation système et support utilisateur**  
> **État : STRUCTURE CRÉÉE** 📋 - Modèles à définir  
> Dernière mise à jour : 19/07/2025

---

## 🎯 Vue d'ensemble

Le module **13 - AIDE** fournit l'ensemble de la documentation système et du support utilisateur pour l'application ATARYS, incluant les guides, la documentation technique et le support.

### **Objectifs Principaux**
- Documentation système
- Guide utilisateur
- Support utilisateur
- Formation et assistance

---

## 📋 État d'Implémentation

### **✅ Implémenté**
- **Structure de fichier** : `module_13.py` créé
- **Pattern BaseModel** : Prêt pour les modèles

### **❌ À Implémenter**
- **Tables principales** : Documentation, Guides, Support
- **API REST** : Endpoints à créer
- **Interface Frontend** : Composants React à développer
- **Logique métier** : Système d'aide contextuelle

---

## 📊 Sous-modules

Selon `ATARYS_MODULES.md`, le module 13 comprend :

### **13.1 - DOCUMENTATION** ❌ **À IMPLÉMENTER**
- Documentation système
- Guides techniques
- Procédures d'utilisation
- FAQ et résolution de problèmes

---

## 🗄️ Structure de Données Proposée

### **Table Principale : Documentation**
```python
class Documentation(BaseModel):
    __tablename__ = 'documentation'
    
    # Document
    titre = db.Column(db.String(200), nullable=False)
    type_document = db.Column(db.String(50))
    # GUIDE, FAQ, PROCEDURE, TUTORIEL, REFERENCE
    
    # Contenu
    contenu = db.Column(db.Text, nullable=False)
    resume = db.Column(db.Text)
    
    # Organisation
    categorie = db.Column(db.String(100))
    module_concerne = db.Column(db.String(50))  # Module ATARYS concerné
    niveau = db.Column(db.String(20), default='DEBUTANT')
    # DEBUTANT, INTERMEDIAIRE, AVANCE
    
    # Métadonnées
    auteur = db.Column(db.String(100))
    version = db.Column(db.String(10), default='1.0')
    statut = db.Column(db.String(20), default='BROUILLON')
    # BROUILLON, PUBLIE, ARCHIVE
    
    # Utilisation
    nb_vues = db.Column(db.Integer, default=0)
    note_moyenne = db.Column(db.Numeric(3, 2))
    derniere_consultation = db.Column(db.DateTime)
    
    # Recherche
    mots_cles = db.Column(db.Text)
    tags = db.Column(db.Text)
```

### **Support et FAQ**
```python
class FAQ(BaseModel):
    __tablename__ = 'faq'
    
    # Question
    question = db.Column(db.Text, nullable=False)
    reponse = db.Column(db.Text, nullable=False)
    
    # Classification
    categorie = db.Column(db.String(100))
    module_concerne = db.Column(db.String(50))
    
    # Popularité
    nb_consultations = db.Column(db.Integer, default=0)
    utile_oui = db.Column(db.Integer, default=0)
    utile_non = db.Column(db.Integer, default=0)
    
    # Gestion
    statut = db.Column(db.String(20), default='ACTIVE')
    ordre_affichage = db.Column(db.Integer)
```

---

## 🛣️ API Endpoints Proposées

### **Documentation**
```http
GET    /api/module-13/documentation         # Liste documentation
POST   /api/module-13/documentation         # Nouveau document
GET    /api/module-13/documentation/:id     # Détail document
PUT    /api/module-13/documentation/:id     # Modification
DELETE /api/module-13/documentation/:id     # Suppression

GET    /api/module-13/documentation/search  # Recherche dans la doc
GET    /api/module-13/documentation/module/:module # Doc par module
```

### **FAQ et Support**
```http
GET    /api/module-13/faq                   # Liste FAQ
POST   /api/module-13/faq                   # Nouvelle FAQ
GET    /api/module-13/faq/:id               # Détail FAQ
PUT    /api/module-13/faq/:id               # Modification
DELETE /api/module-13/faq/:id               # Suppression

POST   /api/module-13/faq/:id/utile         # Marquer comme utile
GET    /api/module-13/faq/populaires        # FAQ les plus consultées
```

### **Aide Contextuelle**
```http
GET    /api/module-13/aide/:module          # Aide pour un module
GET    /api/module-13/aide/recherche        # Recherche d'aide
POST   /api/module-13/feedback              # Feedback utilisateur
```

---

## 🎯 Priorités de Développement

### **Phase 1 : Base**
1. **Modèle Documentation** : Structure principale
2. **FAQ** : Questions fréquentes
3. **API consultation** : Lecture de la documentation

### **Phase 2 : Fonctionnalités**
1. **Recherche** : Moteur de recherche dans la doc
2. **Aide contextuelle** : Aide par module
3. **Feedback** : Retours utilisateurs

### **Phase 3 : Avancé**
1. **Versioning** : Gestion des versions
2. **Statistiques** : Analytics d'utilisation
3. **Génération automatique** : Doc depuis le code

---

## 📚 Contenu de Documentation Proposé

### **Guides Utilisateur**
- Guide de démarrage rapide
- Manuel utilisateur par module
- Procédures métier ATARYS
- Bonnes pratiques

### **Documentation Technique**
- Architecture système
- API Reference
- Guide développeur
- Troubleshooting

### **FAQ par Module**
- Questions fréquentes par module
- Résolution de problèmes courants
- Astuces et conseils
- Cas d'usage types

---

## 🔗 Liens Utiles

- **[Modèles SQLAlchemy](./database-schema.md)** - Structure détaillée des tables
- **[API Endpoints](./api-endpoints.md)** - Spécifications REST complètes
- **[Guide Rédaction](./guide-redaction.md)** - Standards de documentation
- **[ATARYS_MODULES.md](../../00-overview/ATARYS_MODULES.md)** - Nomenclature officielle
