# 🎛️ ATARYS V2 - Scripts Batch

> **Scripts organisés pour lancer et gérer ATARYS V2**  
> Dernière mise à jour : 2025 - Version 2.0 (Nettoyée)

---

## 📁 Structure du dossier `.bat`

### **Scripts Batch (.bat) - Lancement**
- `lancer-atarys-complet.bat` - **Script principal** (Backend + Frontend)
- `lancer-backend.bat` - Backend API REST seul
- `lancer-frontend.bat` - Frontend React seul
- `fermer_atarys.bat` - Fermeture des serveurs (ports 3000/5000)
- `installer-backend.bat` - Installation des dépendances backend
- `test-atarys-v2.bat` - Test de configuration complète

### **Scripts PowerShell (.ps1) - Sauvegarde**
- `sauvegarde-securisee.ps1` - Sauvegarde GitHub + Local
- `verifier-sauvegarde.ps1` - Vérification du système de sauvegarde
- `installer-tache-utilisateur.ps1` - Installation tâche planifiée 21h

### **Documentation**
- `README-SCRIPTS-BATCH.md` - Guide des scripts de lancement
- `README-SAUVEGARDES.md` - Guide des sauvegardes automatiques

---

## 🚀 Utilisation rapide

### **Première installation**
```batch
# 1. Installer les dépendances backend
.bat\installer-backend.bat

# 2. Tester la configuration
.bat\test-atarys-v2.bat
```

### **Lancement quotidien**
```batch
# Option 1 : Lancement complet (recommandé)
.bat\lancer-atarys-complet.bat

# Option 2 : Lancement séparé
.bat\lancer-backend.bat
.bat\lancer-frontend.bat
```

### **Fermeture**
```batch
# Fermer tous les serveurs
.bat\fermer_atarys.bat
```

---

## 📊 URLs ATARYS V2

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:5000
- **Health Check** : http://localhost:5000/health
- **API Table Generator** : http://localhost:5000/api/table-generator/

---

## 💾 Sauvegarde automatique

### **Installation**
```powershell
# Installer la sauvegarde quotidienne à 21h
.bat\installer-tache-utilisateur.ps1
```

### **Vérification**
```powershell
# Vérifier l'état des sauvegardes
.bat\verifier-sauvegarde.ps1
```

### **Sauvegarde manuelle**
```powershell
# Sauvegarde immédiate
.bat\sauvegarde-securisee.ps1 -Force
```

---

## ✅ Nettoyage effectué

### **Supprimé**
- ❌ `lancer_atarys.bat` (redondant avec `lancer-atarys-complet.bat`)

### **Renommé**
- 🔄 `ouvrir-flask-admin.bat` → `lancer-backend.bat`
- 🔄 `installer-flask-admin.bat` → `installer-backend.bat`

### **Mis à jour**
- ✅ En-têtes des scripts pour refléter "API REST" au lieu de "Flask-Admin"
- ✅ Documentation mise à jour avec les nouveaux noms
- ✅ Références corrigées dans les README

---

## 🎯 Scripts recommandés

### **Pour le développement**
1. `lancer-atarys-complet.bat` - Lancement complet
2. `test-atarys-v2.bat` - Test de configuration
3. `fermer_atarys.bat` - Fermeture propre

### **Pour la maintenance**
1. `installer-backend.bat` - Installation dépendances
2. `sauvegarde-securisee.ps1` - Sauvegarde manuelle
3. `verifier-sauvegarde.ps1` - Diagnostic sauvegarde

---

**✅ Dossier `.bat` nettoyé et organisé !** 