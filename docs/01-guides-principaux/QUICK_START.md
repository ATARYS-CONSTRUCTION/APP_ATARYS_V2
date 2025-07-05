# 🚀 Démarrage Rapide ATARYS

> **Lancer l'application ATARYS en 2 minutes**  
> Guide minimal pour développeurs

---

## ⚡ **Lancement Immédiat (RECOMMANDÉ)**

### **🎯 Option 1 : Scripts Automatisés** 
```powershell
# Démarrage automatique Backend + Frontend
.bat/start_dev.bat

# Redémarrage complet
.bat/restart_dev.bat

# Arrêt des serveurs
.bat/stop_dev.bat

# Test de toutes les APIs
.bat/test_api.bat
```
**Résultat :** ✅ Backend (port 5000) + Frontend (port 3000) démarrés automatiquement

### **🔧 Option 2 : Commandes Manuelles**

#### **1. Backend Flask** (Terminal 1)
```powershell
cd backend
python run.py
```
**Résultat :** ✅ Serveur Flask sur http://localhost:5000

#### **2. Frontend React** (Terminal 2)  
```powershell
cd frontend
npm run dev
```
**Résultat :** ✅ Interface React sur http://localhost:3001

### **3. Vérification APIs**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/chantiers"
Invoke-RestMethod -Uri "http://localhost:5000/api/villes?per_page=5"  
```

---

## 🔧 **Environnement Requis**

### **Prérequis**
- **Python 3.9+** avec Flask installé
- **Node.js 18+** avec npm
- **PowerShell** (Windows)

### **Vérification Rapide**
```powershell
# Vérifier Python + dépendances
cd backend; python -c "import flask, sqlalchemy; print('Backend OK')"

# Vérifier Node + React
cd frontend; npm --version
```

---

## 📋 **Premiers Pas Développeur**

### **Étapes Obligatoires**
1. **[Lire DEV_MASTER](DEV_MASTER.md)** - Vision complète du projet
2. **[Consulter CHECKLIST](../04-outils-templates/CHECKLIST_DEVELOPPEMENT.md)** - Avant tout développement
3. **[Suivre STANDARDS](../03-regles-standards/STANDARDS_DEV.md)** - Règles de code

### **Structure Projet**
```
0 APP ATARYS/
├── .bat/        # Scripts démarrage/test automatisés
├── backend/     # Flask + SQLAlchemy
├── frontend/    # React + Vite  
├── docs/        # Documentation complète
└── data/        # Base SQLite + références
```

---

## 🚨 **Règles PowerShell Windows**

### **✅ Syntaxe CORRECTE**
```powershell
cd backend; python run.py              # ✅ Utiliser ;
Invoke-RestMethod -Uri "http://..."     # ✅ Pas curl
.bat/start_dev.bat                      # ✅ Scripts automatisés
```

### **❌ Syntaxe INTERDITE**  
```bash
cd backend && python run.py            # ❌ && invalide PowerShell
curl http://localhost:5000              # ❌ curl n'existe pas
```

---

## 🎯 **Modules ATARYS Prioritaires**

### **✅ Modules Opérationnels**
- **Module 9.1** - Liste Salariés (http://localhost:3001/salaries)
- **Module 10.1** - Calcul Ardoises (http://localhost:3001/calcul-ardoises)

### **🔄 Module en Développement**  
- **Module 3.1** - Liste Chantiers (http://localhost:3001/chantiers) - PRIORITÉ 1

---

## 🔍 **Diagnostic Rapide**

### **Scripts de Debug Disponibles**
```powershell
.bat/debug_dev.bat      # Debug avec logs détaillés
.bat/test_api.bat       # Test complet des APIs
```

### **Problèmes Fréquents**
```powershell
# Base de données vide ?
cd backend; python -c "from app.models import Chantier; print(f'🏗️ Module 3: Chantiers & Devis: {len(list(Chantier.query.all()))}')"

# APIs non fonctionnelles ?
Invoke-RestMethod -Uri "http://localhost:5000/health"

# Frontend ne charge pas ?
cd frontend; npm run dev --host
```

---

## 📚 **Pour Aller Plus Loin**

- **[DEV_MASTER](DEV_MASTER.md)** - Document central complet
- **[ARCHITECTURE](../02-architecture/ARCHITECTURE.md)** - Vue d'ensemble technique  
- **[API_ENDPOINTS](../02-architecture/API_ENDPOINTS.md)** - Toutes les APIs

---

*Temps de lecture : 2 minutes | Temps de lancement : 30 secondes* 