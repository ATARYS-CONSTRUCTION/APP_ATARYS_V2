# 🎛️ Flask-Admin ATARYS - Guide d'utilisation

> **Interface d'administration pour la base de données ATARYS**  
> Compatible SQLAlchemy + Architecture modulaire ATARYS  
> Dernière mise à jour : 2025

---

## 📋 Vue d'ensemble

Flask-Admin fournit une interface web pour :
- **Visualiser** les données de la base SQLite
- **Gérer** les enregistrements (CRUD)
- **Naviguer** par modules ATARYS
- **Exporter** les données
- **Valider** les contraintes SQLAlchemy

---

## 🚀 Installation et démarrage

### 1. Installation
```batch
# Depuis la racine du projet ATARYS
.bat\installer-flask-admin.bat
```

### 2. Ouverture
```batch
# Depuis la racine du projet ATARYS
.bat\ouvrir-flask-admin.bat
```

### 3. Accès
- **URL** : http://localhost:5000/admin
- **Port** : 5000 (configurable)
- **Arrêt** : Ctrl+C dans le terminal

---

## 🏗️ Architecture Flask-Admin

### Structure des fichiers
```
backend/
├── admin_atarys.py          # Configuration Flask-Admin
├── app/
│   ├── models/              # Modèles SQLAlchemy
│   │   ├── base.py          # BaseModel
│   │   ├── module_3_1.py   # Module 3.1 - LISTE CHANTIERS
│   │   ├── module_9_1.py   # Module 9.1 - LISTE SALARIÉS
│   │   └── module_10_1.py  # Module 10.1 - CALCUL ARDOISES
│   └── __init__.py          # Factory pattern
└── run.py                   # Serveur principal
```

### Configuration Flask-Admin
```python
# backend/admin_atarys.py
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

def create_admin(app, db):
    admin = Admin(app, name='ATARYS Admin', template_mode='bootstrap4')
    
    # Ajouter les vues par module ATARYS
    # admin.add_view(ModelView(Chantier, db.session, name='Chantiers'))
    
    return admin
```

---

## 📊 Modules ATARYS supportés

### **Modules Prioritaires V2**
- **Module 3.1** : LISTE CHANTIERS (priorité 1)
- **Module 9.1** : LISTE SALARIÉS (priorité 2)  
- **Module 10.1** : CALCUL ARDOISES (priorité 3)

### **Modules Phase 1**
- **Modules 1.1/1.2** : Planning
- **Modules 2.1/2.2** : Listes de tâches
- **Modules 7.1/7.2** : Gestion et tableaux de bord

---

## 🔧 Fonctionnalités

### **Visualisation des données**
- ✅ Tables SQLAlchemy avec relations
- ✅ Filtres et recherche
- ✅ Pagination automatique
- ✅ Tri par colonnes

### **Gestion des données**
- ✅ Création d'enregistrements
- ✅ Modification en ligne
- ✅ Suppression avec confirmation
- ✅ Validation des contraintes

### **Export et import**
- ✅ Export CSV/JSON
- ✅ Import de données
- ✅ Sauvegarde des configurations

---

## ⚠️ Notes importantes

### **Sécurité**
- Interface d'administration (pas de production)
- Authentification à implémenter
- Validation des permissions

### **Performance**
- Pagination automatique (50 éléments)
- Index sur les colonnes fréquentes
- Cache pour les requêtes lourdes

### **Maintenance**
- Logs des actions d'administration
- Sauvegarde avant modifications
- Tests des fonctionnalités

---

## 🎯 Prochaines étapes

1. **Créer les modèles SQLAlchemy** selon modules ATARYS
2. **Configurer les vues Flask-Admin** par module
3. **Tester l'interface** avec des données
4. **Optimiser les performances** selon usage

---

**✅ Flask-Admin prêt pour la gestion des données ATARYS !** 