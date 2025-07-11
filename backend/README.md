# 🏗️ Backend ATARYS - Structure Flask

> **Application Flask avec Factory pattern pour ATARYS V2**  
> Architecture modulaire selon les règles ATARYS  
> Dernière mise à jour : 2025

---

## 📁 Structure actuelle

```
backend/
└── app/
    └── __init__.py   # Factory pattern Flask minimal
```

---

## 🔧 Configuration

### **Factory Pattern**
- `create_app()` : Fonction de création de l'application Flask
- Configuration SQLAlchemy pour la base `data/atarys_data.db`
- Extensions : Flask-SQLAlchemy, Flask-Migrate

### **Base de données**
- **URI** : `sqlite:///data/atarys_data.db`
- **ORM** : SQLAlchemy 2.0+
- **Migrations** : Flask-Migrate

---

## 🚀 Utilisation

### **Démarrage de l'application**
```python
from app import create_app

app = create_app('development')
app.run(debug=True)
```

### **Test de santé**
```bash
curl http://localhost:5000/health
```

---

## 📋 Prochaines étapes

### **Phase 1 : Structure de base**
- [ ] Créer les modèles SQLAlchemy selon modules ATARYS
- [ ] Configurer Flask-Admin pour la visualisation
- [ ] Ajouter les services par module

### **Phase 2 : Développement modulaire**
- [ ] Module 3.1 : LISTE CHANTIERS (priorité 1)
- [ ] Module 9.1 : LISTE SALARIÉS (priorité 2)
- [ ] Module 10.1 : CALCUL ARDOISES (priorité 3)

---

## ⚠️ Règles importantes

### **Standards ATARYS V2**
- **Factory pattern** obligatoire
- **BaseModel** pour tous les modèles
- **Numeric(10,2)** pour les montants financiers
- **Modules 1.1 à 13.x** selon nomenclature officielle

### **Interdictions**
- ❌ Aucune invention de table sans consentement
- ❌ Aucun modèle sans BaseModel
- ❌ Aucun montant en Float (toujours Numeric)

---

**✅ Backend minimal prêt pour le développement ATARYS !** 