# 🎛️ ATARYS V2 - Scripts de lancement

> **Scripts batch pour lancer ATARYS V2**  
> Backend Flask + Frontend React + API REST  
> Dernière mise à jour : 2025 - Version 2.0

---

## 📋 Vue d'ensemble

ATARYS V2 utilise une architecture moderne :
- **Backend Flask** : API REST avec SQLAlchemy
- **Frontend React** : Interface utilisateur avec Vite
- **Base de données** : SQLite dans `/data/`
- **Génération automatique** : Tables via Module 12.1

---

## 🚀 Scripts disponibles

### 1. Installation des dépendances
```batch
# Installation complète du backend
.bat\installer-backend.bat
```

### 2. Lancement du backend
```batch
# Lancement du serveur Flask API REST
.bat\lancer-backend.bat
```

### 3. Lancement du frontend
```batch
# Lancement du serveur React
.bat\lancer-frontend.bat
```

### 4. Lancement complet
```batch
# Lancement backend + frontend simultanément
.bat\lancer-atarys-complet.bat
```

### 5. Fermeture des serveurs
```batch
# Fermeture des serveurs (ports 3000 et 5000)
.bat\fermer_atarys.bat
```

### 6. Test de configuration
```batch
# Test de la configuration complète
.bat\test-atarys-v2.bat
```

---

## 🏗️ Architecture ATARYS V2

### Structure des fichiers
```
backend/
├── app.py                    # Point d'entrée Flask
├── wsgi.py                   # Point d'entrée WSGI
├── app/
│   ├── __init__.py           # Factory pattern
│   ├── models/               # Modèles SQLAlchemy
│   ├── routes/               # Routes API REST
│   ├── services/             # Services métier
│   └── utils/                # Utilitaires
└── requirements/
    ├── development.txt       # Dépendances dev
    └── production.txt        # Dépendances prod

frontend/
├── src/
│   ├── pages/               # Pages React
│   ├── components/          # Composants
│   └── api/                # Services API
└── package.json            # Dépendances Node.js
```

### URLs et ports
- **Backend API** : http://localhost:5000
- **Frontend** : http://localhost:3000
- **Health check** : http://localhost:5000/health
- **API Table Generator** : http://localhost:5000/api/table-generator/

---

## 📊 Modules ATARYS supportés

### **Modules Prioritaires V2**
- **Module 3.1** : LISTE CHANTIERS (priorité 1)
- **Module 9.1** : LISTE SALARIÉS (priorité 2)  
- **Module 10.1** : CALCUL ARDOISES (priorité 3)
- **Module 12.1** : BASE DE DONNÉES (génération tables)

### **Modules Phase 1**
- **Modules 1.1/1.2** : Planning
- **Modules 2.1/2.2** : Listes de tâches
- **Modules 7.1/7.2** : Gestion et tableaux de bord

---

## 🔧 Fonctionnalités

### **Backend Flask**
- ✅ API REST standardisée
- ✅ Base de données SQLite
- ✅ Génération automatique de tables
- ✅ Validation Marshmallow
- ✅ CORS activé

### **Frontend React**
- ✅ Interface moderne avec Tailwind CSS
- ✅ Navigation par modules ATARYS
- ✅ Intégration API REST
- ✅ Gestion d'état avec Context

### **Génération de tables**
- ✅ Création dynamique via Module 12.1
- ✅ Génération automatique de modèles
- ✅ Génération automatique de routes
- ✅ Génération automatique de schémas

---

## ⚠️ Notes importantes

### **Sécurité**
- Interface de développement
- Authentification à implémenter
- Validation des données côté serveur

### **Performance**
- Pagination automatique (50 éléments)
- Index sur les colonnes fréquentes
- Cache pour les requêtes lourdes

### **Maintenance**
- Logs structurés dans `/logs/`
- Sauvegarde automatique de la base
- Tests des fonctionnalités

---

## 🎯 Prochaines étapes

1. **Tester les scripts batch** avec l'architecture V2
2. **Implémenter l'authentification** si nécessaire
3. **Optimiser les performances** selon usage
4. **Ajouter des tests automatisés**

---

**✅ Scripts batch prêts pour ATARYS V2 !** 