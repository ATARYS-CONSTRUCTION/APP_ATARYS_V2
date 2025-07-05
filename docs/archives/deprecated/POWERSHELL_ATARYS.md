# GUIDE POWERSHELL ATARYS - RÉFÉRENCE RAPIDE

> **Guide de référence pour éviter les erreurs PowerShell récurrentes**  
> Environnement : Windows PowerShell sur projet ATARYS  
> Dernière mise à jour : 02/07/2025

---

## 🚨 ERREURS RÉCURRENTES IDENTIFIÉES

### ❌ **ERREUR #1 : Séparateur de commandes**
```powershell
# ❌ FAUX (ne fonctionne pas en PowerShell)
cd backend && python run.py
cd frontend && npm run dev

# ✅ CORRECT
cd backend; python run.py
cd frontend; npm run dev
```

### ❌ **ERREUR #2 : Chemins relatifs incorrects**
```powershell
# ❌ FAUX (chemins incorrects ATARYS)
python run.py           # fichier dans backend/, pas racine
cd ../frontend          # dossier est ./frontend

# ✅ CORRECT
cd backend; python run.py
cd frontend; npm run dev
```

### ❌ **ERREUR #3 : Commandes Unix/Linux**
```powershell
# ❌ FAUX (commandes Unix)
curl -s http://localhost:5000/api/test
ls -la

# ✅ CORRECT (commandes PowerShell)
Invoke-RestMethod -Uri "http://localhost:5000/api/test"
Get-ChildItem
```

---

## ✅ COMMANDES ATARYS CORRECTES

### **🚀 DÉMARRAGE DÉVELOPPEMENT**
```powershell
# Backend Flask (Port 5000)
cd backend; python run.py

# Frontend Vite (Port 3000) - Nouvelle fenêtre PowerShell
cd frontend; npm run dev
```

### **🧪 TESTS API STANDARD**
```powershell
# API Chantiers (Module 3.1)
Invoke-RestMethod -Uri "http://localhost:5000/api/chantiers" -Method GET

# API Villes (avec pagination)
Invoke-RestMethod -Uri "http://localhost:5000/api/villes?per_page=5" -Method GET

# API Salariés (Module 9.1)
Invoke-RestMethod -Uri "http://localhost:5000/api/salaries" -Method GET

# Statut Frontend
Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing
```

### **🔧 DIAGNOSTICS TECHNIQUES**
```powershell
# Test modèles SQLAlchemy
cd backend; python -c "from app import create_app; from app.models import Chantier, Devis, EtatChantier; app=create_app(); app.app_context().push(); print(f'🏗️ Module 3: Chantiers & Devis: {Chantier.query.count()}, Devis: {Devis.query.count()}, États: {EtatChantier.query.count()}')"

# Vérification base de données
cd backend; python -c "from app.services.database_service import DatabaseService; from app import create_app; app=create_app(); app.app_context().push(); print('Tables:', DatabaseService.get_all_tables())"

# Analyse logs
Get-Content "logs\atarys.log" -Tail 20
```

### **📁 NAVIGATION DOSSIERS ATARYS**
```powershell
# Structure projet depuis C:\DEV\0 APP ATARYS
cd backend              # → backend/
cd frontend             # → frontend/
cd docs                 # → docs/
cd data                 # → data/
cd logs                 # → logs/

# Retour racine
cd ..                   # ou Set-Location "C:\DEV\0 APP ATARYS"
```

---

## 📋 ÉQUIVALENCES BASH ↔ POWERSHELL

| Fonction | Bash/Linux | PowerShell Windows |
|----------|------------|-------------------|
| **Séparateur** | `&&` | `;` |
| **HTTP Request** | `curl` | `Invoke-RestMethod` |
| **Lister fichiers** | `ls` | `Get-ChildItem` |
| **Lire fichier** | `cat file.txt` | `Get-Content file.txt` |
| **Rechercher** | `grep` | `Select-String` |
| **Navigation** | `cd dir` | `cd dir` (identique) |

---

## 🎯 RÈGLES D'APPLICATION IMMÉDIATE

### **POUR CURSOR/IA :**
1. ❌ **JAMAIS proposer `&&` en PowerShell** → Toujours `;`
2. ❌ **JAMAIS proposer `curl` en PowerShell** → Toujours `Invoke-RestMethod`
3. ✅ **TOUJOURS vérifier chemins ATARYS** → `backend/`, `frontend/`, `docs/`
4. ✅ **TESTER commandes PowerShell** avant proposition
5. ✅ **CORRIGER immédiatement** si erreur détectée

### **POUR DÉVELOPPEUR :**
1. **Ouvrir 2 fenêtres PowerShell** pour backend + frontend
2. **Utiliser uniquement `;`** pour enchaîner commandes
3. **Copier-coller commandes** depuis ce guide
4. **Signaler erreurs** pour mise à jour du guide

---

## 🔍 RÉSOLUTION PROBLÈMES COURANTS

### **Erreur : "Le jeton '&&' n'est pas un séparateur..."**
```powershell
# Solution : Remplacer && par ;
cd backend; python run.py
```

### **Erreur : "can't open file 'run.py'"**
```powershell
# Solution : Le fichier est dans backend/
cd backend; python run.py
```

### **Erreur : "Impossible de trouver le chemin '../frontend'"**
```powershell
# Solution : Le dossier est ./frontend depuis racine
cd frontend; npm run dev
```

### **Erreur : "Invoke-WebRequest : Argument manquant"**
```powershell
# curl n'existe pas nativement, utiliser :
Invoke-RestMethod -Uri "http://localhost:5000/api/test"
```

---

## ✅ VALIDATION ENVIRONNEMENT

### **Test rapide fonctionnement :**
```powershell
# Vérifier répertoire courant
Get-Location

# Doit afficher : C:\DEV\0 APP ATARYS

# Test structure dossiers
Get-ChildItem -Name

# Doit montrer : backend, frontend, docs, data, logs, etc.
```

---

**🎯 OBJECTIF : Éliminer 100% des erreurs PowerShell récurrentes dans ATARYS** 