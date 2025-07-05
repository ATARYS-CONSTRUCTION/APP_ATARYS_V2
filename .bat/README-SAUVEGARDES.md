# 💾 ATARYS V2 - Guide des Sauvegardes Automatiques

> **Système complet de sauvegarde pour protéger votre projet ATARYS V2**

---

## 🎯 **Solutions Disponibles**

### 1. **Sauvegarde Manuelle Rapide**
```powershell
# Double-clic sur le fichier
.\sauvegarde-rapide.bat
```
**Utilisation :** Sauvegarde immédiate quand vous le souhaitez

### 2. **Sauvegarde Automatique Planifiée**
```powershell
# Exécuter en tant qu'administrateur
.\configurer-tache-planifiee.ps1
```
**Utilisation :** Sauvegardes automatiques selon planning

### 3. **Git Hooks Automatiques**
```powershell
# Installation unique
.\installer-git-hooks.ps1
```
**Utilisation :** Sauvegardes déclenchées par vos actions Git

---

## ⚙️ **Configuration Recommandée**

### **Étape 1 : Créer le dossier de sauvegarde locale**
```powershell
mkdir "C:\DEV\SAUVEGARDES\ATARYS_V2"
```

### **Étape 2 : Installer la tâche planifiée**
1. **Clic droit** sur `configurer-tache-planifiee.ps1`
2. **"Exécuter avec PowerShell"** (en tant qu'administrateur)
3. Confirmer l'installation

### **Étape 3 : Installer les Git Hooks**
```powershell
.\installer-git-hooks.ps1
```

---

## 📅 **Planning des Sauvegardes Automatiques**

| **Déclencheur** | **Fréquence** | **Type** |
|----------------|---------------|----------|
| 🕕 **18h00** | Quotidien | GitHub + Local |
| 🚪 **Fermeture session** | À chaque fois | GitHub uniquement |
| ⏰ **Toutes les 2h** | 8h-18h | GitHub (si changements) |
| 📝 **Commit important** | Automatique | GitHub + Local |
| 🔄 **Git push** | À chaque fois | Validation + Log |

---

## 🛠️ **Utilisation Quotidienne**

### **Sauvegarde Rapide**
```powershell
# Méthode 1 : Double-clic
.\sauvegarde-rapide.bat

# Méthode 2 : PowerShell avec message personnalisé
.\sauvegarde-auto.ps1 -Message "Fin de journée - nouvelles fonctionnalités"

# Méthode 3 : Forcer la sauvegarde même sans changements
.\sauvegarde-auto.ps1 -Force
```

### **Vérifier les Sauvegardes**
```powershell
# Voir les logs
Get-Content "logs\sauvegarde.log" -Tail 20

# Voir l'historique Git
git log --oneline -10

# Vérifier la tâche planifiée
Get-ScheduledTask -TaskName "ATARYS_V2_Sauvegarde_Auto"
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
- **Commits :** `logs\commits.log`
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
1. Ouvrir **Gestionnaire des tâches**
2. Aller dans **Bibliothèque du Planificateur de tâches**
3. Chercher `ATARYS_V2_Sauvegarde_Auto`
4. Vérifier les **Conditions** et **Paramètres**

### **Problème : Hooks Git ne s'exécutent pas**
```powershell
# Vérifier les permissions
ls -la .git/hooks/

# Réinstaller les hooks
.\installer-git-hooks.ps1
```

---

## 🔧 **Personnalisation**

### **Modifier la Fréquence**
Éditer `configurer-tache-planifiee.ps1` :
```powershell
# Changer l'heure quotidienne
$Triggers += New-ScheduledTaskTrigger -Daily -At "20:00"

# Changer l'intervalle
$Triggers += New-ScheduledTaskTrigger -Once -At "08:00" -RepetitionInterval (New-TimeSpan -Hours 1)
```

### **Ajouter des Exclusions**
Éditer `sauvegarde-auto.ps1` :
```powershell
# Modifier la commande robocopy
robocopy $ProjectPath $BackupFolder /E /XD .git node_modules .vite dist __pycache__ temp /XF *.log *.tmp *.cache
```

### **Notifications**
Ajouter dans `sauvegarde-auto.ps1` :
```powershell
# Notification Windows
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show("Sauvegarde ATARYS V2 terminée !", "Succès")
```

---

## 📈 **Statistiques et Monitoring**

### **Voir les Statistiques**
```powershell
# Nombre de commits
git rev-list --count HEAD

# Taille du dépôt
git count-objects -vH

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
- [ ] Tester la sauvegarde manuelle : `.\sauvegarde-rapide.bat`
- [ ] Installer la tâche planifiée (admin requis)
- [ ] Installer les Git hooks
- [ ] Vérifier les logs : `logs\sauvegarde.log`
- [ ] Tester un commit pour vérifier les hooks
- [ ] Configurer les notifications (optionnel)

---

**🎯 Avec ce système, votre projet ATARYS V2 est protégé automatiquement !** 