# 🔧 Extensions VS Code pour ATARYS

> **Guide d'installation des extensions recommandées**  
> SQLAlchemy, Python, React, Base de données

---

## 🚀 **Installation Automatique**

### **Méthode 1 : Extensions Essentielles (1 clic)**
```powershell
# Copier-coller dans le terminal VS Code
code --install-extension ms-python.python
code --install-extension qwtel.sqlite-viewer
code --install-extension alexcvzz.vscode-sqlite
code --install-extension mtxr.sqltools
code --install-extension mtxr.sqltools-driver-sqlite
code --install-extension ms-python.black-formatter
```

### **Méthode 2 : Pack Complet ATARYS**
```powershell
# Extensions complètes pour développement ATARYS
code --install-extension ms-python.python
code --install-extension ms-python.flake8
code --install-extension ms-python.black-formatter
code --install-extension ms-python.debugpy
code --install-extension qwtel.sqlite-viewer
code --install-extension alexcvzz.vscode-sqlite
code --install-extension mtxr.sqltools
code --install-extension mtxr.sqltools-driver-sqlite
code --install-extension bradlc.vscode-tailwindcss
code --install-extension esbenp.prettier-vscode
code --install-extension ms-vscode.powershell
code --install-extension christian-kohler.path-intellisense
```

---

## 🗄️ **Extensions Base de Données**

### **✅ SQLite Viewer** 
- **Extension** : `qwtel.sqlite-viewer`
- **Utilité** : Visualiser le contenu de `data/atarys.db` directement dans VS Code
- **Usage** : Clic droit sur `.db` → "Open with SQLite Viewer"

### **✅ SQLite Tools**
- **Extension** : `alexcvzz.vscode-sqlite`
- **Utilité** : Exécuter des requêtes SQL sur votre base ATARYS
- **Usage** : `Ctrl+Shift+P` → "SQLite: Open Database"

### **✅ SQLTools**
- **Extension** : `mtxr.sqltools` + `mtxr.sqltools-driver-sqlite`
- **Utilité** : Interface complète de gestion base de données
- **Avantage** : Comprend les relations SQLAlchemy !

---

## 🐍 **Extensions Python/SQLAlchemy**

### **✅ Python** 
- **Extension** : `ms-python.python`
- **Utilité** : IntelliSense pour vos modèles SQLAlchemy
- **Fonctionnalités** :
  - Auto-complétion sur `Chantier.query.filter_by()`
  - Détection erreurs relations FK
  - Debug SQLAlchemy avec breakpoints

### **✅ Black Formatter**
- **Extension** : `ms-python.black-formatter`
- **Utilité** : Formatage automatique du code Python
- **Configuration** : Déjà configuré selon standards ATARYS

---

## 🌐 **Extensions Frontend**

### **✅ Tailwind CSS**
- **Extension** : `bradlc.vscode-tailwindcss`
- **Utilité** : Auto-complétion classes Tailwind dans vos composants React
- **Essentiel** : Pour le frontend ATARYS

### **✅ Prettier**
- **Extension** : `esbenp.prettier-vscode`
- **Utilité** : Formatage automatique JSX/JavaScript

---

## 🔧 **Configuration Recommandée**

### **Settings VS Code pour ATARYS**
```json
{
    // Python/SQLAlchemy
    "python.defaultInterpreterPath": "./backend/venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    
    // Base de données
    "sqltools.connections": [
        {
            "driver": "SQLite",
            "name": "ATARYS Database",
            "database": "./data/atarys.db"
        }
    ],
    
    // Formatage
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    
    // Tailwind
    "tailwindCSS.includeLanguages": {
        "javascript": "javascript",
        "html": "HTML"
    }
}
```

---

## 🎯 **Utilisation Pratique**

### **Inspecter Modèles SQLAlchemy**
1. Ouvrir `backend/app/models/chantier.py`
2. `Ctrl+Clic` sur `ForeignKey('🏗️ Module 3: Chantiers & Devis_chantier.id')` 
3. **VS Code navigue automatiquement** vers la définition !

### **Visualiser Base ATARYS**
1. Ouvrir `data/atarys.db` avec SQLite Viewer
2. Voir toutes les tables avec données en temps réel
3. **Mais ATTENTION** : Modification directe = risques !

### **Debug SQLAlchemy**
1. Placer breakpoint dans `backend/app/services/chantier_service.py`
2. `F5` pour debug
3. Inspecter `chantier.etat.libelle` en mode debug

---

## ⚡ **Installation Rapide (30 secondes)**

```powershell
# Dans le terminal VS Code - Extensions critiques seulement
code --install-extension ms-python.python
code --install-extension qwtel.sqlite-viewer  
code --install-extension mtxr.sqltools
code --install-extension mtxr.sqltools-driver-sqlite
```

**Résultat** : IntelliSense SQLAlchemy + Visualisation base ATARYS !

---

## 🚀 **Comparaison Outils**

| Outil | Relations FK | Sécurité | IntelliSense | Modules ATARYS |
|-------|--------------|----------|--------------|----------------|
| **API REST** | ✅ Auto | ✅ ORM | ✅ Complet | ✅ Organisés |
| **VS Code SQLite** | ❌ Manuel | ⚠️ Direct | ✅ Python | ❌ Aucune |
| **SQLite Studio** | ❌ Aucune | ❌ Risqué | ❌ Aucun | ❌ Aucune |

**Recommandation** : **API REST** pour administration + **VS Code** pour développement !

---

*Guide mis à jour - Compatible with ATARYS development workflow* 