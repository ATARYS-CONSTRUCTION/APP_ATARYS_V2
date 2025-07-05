# 📋 Logs ATARYS V2

## 📁 Fichiers de Log Locaux

### `sauvegarde.log`
- **Taille actuelle** : ~16 MB
- **Contenu** : Historique complet des sauvegardes
- **Rotation** : Automatique quand > 50 MB
- **Localisation** : Local uniquement (exclu de GitHub)

### Pourquoi les logs ne sont pas sur GitHub ?
- **Taille** : Fichiers volumineux (16+ MB)
- **Sécurité** : Chemins locaux et informations sensibles
- **Pollution** : Changements constants non pertinents
- **Bonnes pratiques** : Logs = données locales

## 🔍 Consultation des Logs

### Dernières entrées
```powershell
Get-Content logs\sauvegarde.log -Tail 20
```

### Recherche dans les logs
```powershell
Select-String "ERROR" logs\sauvegarde.log
Select-String "SUCCESS" logs\sauvegarde.log
```

### Statistiques
```powershell
# Nombre de sauvegardes réussies
(Select-String "SUCCESS" logs\sauvegarde.log).Count

# Dernière sauvegarde
Get-Content logs\sauvegarde.log -Tail 1
```

## 🧹 Nettoyage Automatique

Le système nettoie automatiquement les anciens logs :
- Rotation à 50 MB
- Archivage des anciens logs
- Suppression des logs > 90 jours 