# 🔧 Configuration Cursor pour ATARYS V2

> **Guide de configuration Cursor optimisé pour le projet ATARYS**  
> **Standards obligatoires** pour une productivité maximale  
> Dernière mise à jour : 19/07/2025

---

## 🎯 **Vue d'Ensemble**

Cette documentation définit la configuration optimale de Cursor pour le développement ATARYS V2, incluant les raccourcis, extensions et paramètres recommandés.

---

## ⚙️ **Configuration de Base**

### **Paramètres Cursor Recommandés**
```json
{
  "editor.quickSuggestions": {
    "other": true,
    "comments": true,
    "strings": true
  },
  "editor.suggest.insertMode": "replace",
  "editor.acceptSuggestionOnEnter": "on",
  "editor.wordBasedSuggestions": "on",
  "editor.parameterHints.enabled": true,
  "editor.hover.enabled": true,
  "editor.lightbulb.enabled": true,
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "workbench.editor.enablePreview": false,
  "explorer.confirmDelete": false,
  "explorer.confirmDragAndDrop": false
}
```

### **Configuration des Mentions @**
```json
{
  "editor.quickSuggestions": {
    "other": true,
    "comments": true,
    "strings": true
  },
  "editor.suggest.showWords": true,
  "editor.suggest.showFiles": true,
  "editor.suggest.showReferences": true,
  "editor.suggest.showSnippets": true
}
```

---

## 🚨 **PROBLÈME SPÉCIFIQUE : @ Affiche l'Autocomplétion mais Ne Trouve Pas les Fichiers**

### **Symptômes :**
- ✅ L'autocomplétion apparaît quand vous tapez `@`
- ❌ Les fichiers ne sont pas trouvés/sélectionnés
- ❌ Pas de liste de fichiers dans l'autocomplétion

### **CAUSE :** Configuration des chemins de fichiers manquante

### **SOLUTION COMPLÈTE :**

#### **Étape 1 : Ajouter les Paramètres de Recherche de Fichiers**
```json
{
  "search.include": {
    "**/*": true
  },
  "files.exclude": {
    "**/node_modules": true,
    "**/venv": true,
    "**/.git": true,
    "**/__pycache__": true
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/venv": true,
    "**/.git": true,
    "**/__pycache__": true
  },
  "files.watcherExclude": {
    "**/node_modules/**": true,
    "**/venv/**": true,
    "**/.git/**": true,
    "**/__pycache__/**": true
  },
  "editor.suggest.showFiles": true,
  "editor.suggest.showFolders": true,
  "editor.suggest.showSymbols": true,
  "editor.suggest.showWords": true,
  "editor.suggest.showSnippets": true,
  "editor.suggest.showUsers": true,
  "editor.suggest.showIssues": true,
  "editor.suggest.showCommands": true,
  "editor.suggest.showKeywords": true,
  "editor.suggest.showColors": true,
  "editor.suggest.showConstants": true,
  "editor.suggest.showEnums": true,
  "editor.suggest.showInterfaces": true,
  "editor.suggest.showModules": true,
  "editor.suggest.showProperties": true,
  "editor.suggest.showEvents": true,
  "editor.suggest.showOperators": true,
  "editor.suggest.showUnits": true,
  "editor.suggest.showValues": true,
  "editor.suggest.showTypeParameters": true,
  "editor.suggest.triggerCharacters": ["@", ".", ":", "#", "/", "\\"],
  "editor.suggest.insertMode": "replace",
  "editor.acceptSuggestionOnEnter": "on",
  "editor.wordBasedSuggestions": "on",
  "editor.inlineSuggest.enabled": true,
  "editor.suggest.preview": true,
  "editor.suggest.acceptSuggestionOnCommitCharacter": true,
  "editor.suggest.acceptSuggestionOnEnter": "on"
}
```

#### **Étape 2 : Configurer l'Indexation des Fichiers**
```json
{
  "files.associations": {
    "*.py": "python",
    "*.js": "javascript",
    "*.jsx": "javascriptreact",
    "*.ts": "typescript",
    "*.tsx": "typescriptreact",
    "*.md": "markdown",
    "*.json": "json",
    "*.html": "html",
    "*.css": "css"
  },
  "files.autoGuessEncoding": true,
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "files.eol": "\n",
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true
}
```

#### **Étape 3 : Activer la Recherche Globale**
```json
{
  "search.globalFindClipboard": true,
  "search.showLineNumbers": true,
  "search.showReplacePreview": true,
  "search.useGlobalIgnoreFiles": true,
  "search.useParentIgnoreFiles": true,
  "search.useIgnoreFiles": true,
  "search.followSymlinks": true,
  "search.smartCase": true,
  "search.useGlobalIgnoreFiles": true
}
```

#### **Étape 4 : Redémarrer Cursor et Recharger l'Index**
```bash
# 1. Fermer Cursor complètement
# 2. Redémarrer Cursor
# 3. Attendre que l'indexation se termine (barre de progression en bas)
# 4. Tester @ dans un nouveau fichier
```

#### **Étape 5 : Vérifier l'Indexation**
```bash
# Ouvrir la palette de commandes
Ctrl + Shift + P

# Taper : "Developer: Reload Window"
# Puis : "Developer: Rebuild and Reload Window"
```

---

## ⌨️ **Raccourcis Clavier ATARYS**

### **Navigation Rapide**
```bash
# Recherche de fichiers
Ctrl + P                    # Recherche rapide de fichiers
Ctrl + Shift + P           # Palette de commandes
Ctrl + G                   # Aller à une ligne spécifique

# Navigation dans l'explorateur
Ctrl + Shift + E           # Ouvrir l'explorateur de fichiers
Ctrl + B                   # Basculer la barre latérale

# Recherche dans le code
Ctrl + Shift + F           # Recherche globale
Ctrl + F                   # Recherche dans le fichier actuel

# Sélection de fichiers pour prompts
Ctrl + Shift + P + "Insert File Reference"  # Alternative à @
Ctrl + K + Ctrl + F        # Insérer une référence de fichier
```

### **Raccourcis Spécifiques ATARYS**
```bash
# Navigation vers les dossiers principaux
Ctrl + P + "backend/"      # Aller dans le backend
Ctrl + P + "frontend/"     # Aller dans le frontend  
Ctrl + P + "docs/"         # Aller dans la documentation
Ctrl + P + "data/"         # Aller dans les données

# Recherche de modules spécifiques
Ctrl + P + "module_3"      # Rechercher les fichiers du module 3
Ctrl + P + "Module3"       # Rechercher les composants React du module 3
```

---

## 🔧 **Résolution du Problème @**

### **Problème : Mentions @ ne fonctionnent pas**
**Symptômes :**
- `@` ne déclenche pas la sélection de fichiers
- Pas d'autocomplétion avec `@`
- Comportement différent de l'habituel

### **Solutions par Ordre de Priorité**

#### **Solution 1 : Vérifier les paramètres**
```bash
# 1. Ouvrir les paramètres
Ctrl + ,

# 2. Rechercher "quickSuggestions"
# 3. Vérifier que "other" est activé
# 4. Vérifier que "comments" est activé
# 5. Vérifier que "strings" est activé
```

#### **Solution 2 : Réinitialiser la configuration**
```json
// Dans settings.json
{
  "editor.quickSuggestions": {
    "other": true,
    "comments": true,
    "strings": true
  },
  "editor.suggest.insertMode": "replace",
  "editor.acceptSuggestionOnEnter": "on",
  "editor.wordBasedSuggestions": "on"
}
```

#### **Solution 3 : Alternatives temporaires**
```bash
# Au lieu de @, utilisez :
Ctrl + Shift + P  # Puis tapez "Insert File Reference"
# Ou
Ctrl + K + Ctrl + F  # Insérer une référence de fichier
# Ou
Ctrl + P  # Puis copier le chemin du fichier
```

#### **Solution 4 : Redémarrer Cursor**
```bash
# 1. Fermer Cursor complètement
# 2. Redémarrer Cursor
# 3. Tester @ dans un nouveau fichier
```

---

## 📁 **Workflow ATARYS Optimisé**

### **Méthode Recommandée pour les Prompts**
```bash
# 1. Utiliser Ctrl + P pour trouver le fichier
# 2. Copier le chemin relatif
# 3. Coller dans le prompt avec le contexte

# Exemple :
"Peux-tu analyser le fichier backend/app/models/module_3.py 
et me dire s'il respecte les standards ATARYS ?"
```

### **Raccourcis pour Documentation ATARYS**
```bash
# Documentation principale
Ctrl + P + "DEV_MASTER.md"           # Document central
Ctrl + P + "WORKFLOWS.md"            # Workflows et standards
Ctrl + P + "REGLES METIERS.md"       # Règles business
Ctrl + P + "API_ENDPOINTS.md"        # APIs existantes

# Architecture
Ctrl + P + "DATABASE_SCHEMA.md"      # Structure BDD
Ctrl + P + "ATARYS_ARCHITECTURE.md"  # Architecture technique
```

---

## 🚨 **Dépannage Avancé**

### **Si @ ne fonctionne toujours pas :**

1. **Vérifier les extensions** :
   ```bash
   # Désactiver temporairement les extensions
   Ctrl + Shift + P + "Extensions: Disable All"
   # Tester @
   # Réactiver une par une pour identifier le conflit
   ```

2. **Vérifier la version Cursor** :
   ```bash
   # Help > About
   # Mettre à jour si nécessaire
   ```

3. **Réinitialiser les paramètres** :
   ```bash
   # File > Preferences > Settings
   # Cliquer sur l'icône de réinitialisation
   ```

4. **Utiliser les alternatives** :
   ```bash
   # Méthode manuelle
   Ctrl + P  # Trouver le fichier
   Ctrl + C  # Copier le nom
   # Coller dans le prompt
   ```

---

## ✅ **Validation de la Configuration**

### **Test de Fonctionnement**
```bash
# 1. Ouvrir un nouveau fichier
# 2. Taper @
# 3. Vérifier que l'autocomplétion apparaît
# 4. Tester la sélection de fichiers

# Si ça ne marche pas :
# Utiliser Ctrl + P comme alternative
```

### **Standards ATARYS Respectés**
- ✅ Navigation rapide vers les fichiers
- ✅ Accès facile à la documentation
- ✅ Workflow optimisé pour le développement
- ✅ Respect des conventions de nommage

---

## 📚 **Ressources Complémentaires**

- `docs/03-regles-standards/WORKFLOWS.md` - Workflows de développement
- `docs/03-regles-standards/STANDARDS_DEV.md` - Standards techniques
- `docs/04-outils-templates/CHECKLIST_DEVELOPPEMENT.md` - Checklist développement

**Cette configuration garantit une productivité optimale pour le développement ATARYS V2 !** 