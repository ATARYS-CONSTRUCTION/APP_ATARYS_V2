# 💾 ATARYS V2 - Guide des Sauvegardes Automatiques

> **Système complet de sauvegarde pour protéger votre projet ATARYS V2**

---

## 🎯 **Solutions Disponibles**

### 1. **Sauvegarde Manuelle**
```powershell
# Sauvegarde immédiate
.\sauvegarde-auto.ps1 -Force
```
**Utilisation :** Sauvegarde immédiate quand vous le souhaitez

### 2. **Sauvegarde Automatique Planifiée (21h)**
```powershell
# Installation (pas besoin d'admin)
.\installer-tache-utilisateur.ps1
```
**Utilisation :** Sauvegarde automatique quotidienne à 21h

### 3. **Vérification du Système**
```powershell
# Vérifier l'état des sauvegardes
.\verifier-sauvegarde.ps1
```
**Utilisation :** Diagnostic et vérification du système

---

## 📁 **Fichiers Disponibles**

### **Scripts PowerShell :**
- `sauvegarde-auto.ps1` - Script principal de sauvegarde
- `installer-tache-utilisateur.ps1` - Installation tâche planifiée 21h
- `verifier-sauvegarde.ps1` - Vérification du système
- `README-SAUVEGARDES.md` - Cette documentation

---

## ⚙️ **Configuration Recommandée**

### **Étape 1 : Créer le dossier de sauvegarde locale**
```powershell
mkdir "C:\DEV\SAUVEGARDES\ATARYS_V2"
```

### **Étape 2 : Installer la tâche planifiée**
```powershell
# Pas besoin d'admin !
.\installer-tache-utilisateur.ps1
```

### **Étape 3 : Vérifier l'installation**
```powershell
.\verifier-sauvegarde.ps1
```

---

## 📅 **Planning des Sauvegardes Automatiques**

| **Déclencheur** | **Fréquence** | **Type** |
|----------------|---------------|----------|
| 🕘 **21h00** | Quotidien | GitHub + Local |

**Note :** Les sauvegardes toutes les 2h ont été supprimées pour éviter les interruptions.

---

## 🛠️ **Utilisation Quotidienne**

### **Sauvegarde Manuelle**
```powershell
# Sauvegarde avec message personnalisé
.\sauvegarde-auto.ps1 -Message "Fin de journée - nouvelles fonctionnalités"

# Forcer la sauvegarde même sans changements
.\sauvegarde-auto.ps1 -Force
```

### **Vérifier les Sauvegardes**
```powershell
# Vérifier l'état complet
.\verifier-sauvegarde.ps1

# Voir les logs
Get-Content "logs\sauvegarde.log" -Tail 20

# Voir l'historique Git
git log --oneline -10
```

---

## 📊 **Emplacements des Sauvegardes**

### **GitHub (Principal)**
- **URL :** https://github.com/ATARYS-CONSTRUCTION/APP_ATARYS_V2
- **Branche :** `main`
- **Accès :** En ligne, partageable, historique complet

### **Local (Sécurité)**
- **Dossier :** `C:\DEV\SAUVEGARDES\ATARYS_V2\`
- **Format :** `ATARYS_V2_YYYY-MM-DD_HH-mm-ss`
- **Contenu :** Fichiers projet (sans .git, node_modules)

### **Logs (Traçabilité)**
- **Sauvegarde :** `logs\sauvegarde.log`
- **Système :** `logs\atarys.log`

---

## 🚨 **Dépannage**

### **Problème : "Aucun changement détecté"**
```powershell
# Solution : Forcer la sauvegarde
.\sauvegarde-auto.ps1 -Force
```

### **Problème : Erreur de push GitHub**
```powershell
# Vérifier la connexion
git remote -v

# Re-authentifier si nécessaire
git push origin main
```

### **Problème : Tâche planifiée ne fonctionne pas**
```powershell
# Vérifier avec le script
.\verifier-sauvegarde.ps1

# Ou manuellement
Get-ScheduledTask -TaskName "ATARYS_V2_Sauvegarde_Auto"
```

---

## 🔧 **Personnalisation**

### **Modifier l'Heure**
Éditer `installer-tache-utilisateur.ps1` :
```powershell
# Changer l'heure quotidienne
$Trigger = New-ScheduledTaskTrigger -Daily -At "20:00"  # 20h au lieu de 21h
```

### **Ajouter des Exclusions**
Éditer `sauvegarde-auto.ps1` :
```powershell
# Modifier la commande robocopy
robocopy $ProjectPath $BackupFolder /E /XD .git node_modules .vite dist __pycache__ temp /XF *.log *.tmp *.cache
```

---

## 📈 **Statistiques et Monitoring**

### **Voir les Statistiques**
```powershell
# Utiliser le script de vérification
.\verifier-sauvegarde.ps1

# Nombre de commits
git rev-list --count HEAD

# Dernières sauvegardes
Get-ChildItem "C:\DEV\SAUVEGARDES\ATARYS_V2\" | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```

### **Nettoyage Automatique**
```powershell
# Supprimer les sauvegardes locales > 30 jours
Get-ChildItem "C:\DEV\SAUVEGARDES\ATARYS_V2\" | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item -Recurse -Force
```

---

## ✅ **Checklist de Mise en Place**

- [ ] Créer le dossier `C:\DEV\SAUVEGARDES\ATARYS_V2`
- [ ] Tester la sauvegarde manuelle : `.\sauvegarde-auto.ps1 -Force`
- [ ] Installer la tâche planifiée : `.\installer-tache-utilisateur.ps1`
- [ ] Vérifier l'installation : `.\verifier-sauvegarde.ps1`
- [ ] Attendre 21h pour la première sauvegarde automatique

---

## 🎯 **Résumé**

**Système simplifié et efficace :**
- ✅ **Sauvegarde quotidienne automatique à 21h**
- ✅ **Pas de sauvegardes intempestives toutes les 2h**
- ✅ **Installation sans droits administrateur**
- ✅ **Scripts de vérification et diagnostic**
- ✅ **Documentation complète**

**Prochaine sauvegarde automatique :** Aujourd'hui à 21h00 