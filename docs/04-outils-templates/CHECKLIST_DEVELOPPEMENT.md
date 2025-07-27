# ✅ CHECKLIST DÉVELOPPEMENT ATARYS

> **Processus obligatoire à suivre AVANT tout développement**  
> Référence systématique à la documentation existante

---

## 🔍 **PHASE 1 : CONSULTATION DOCUMENTATION OBLIGATOIRE**

### **Documents à consulter AVANT de coder :**
- [ ] `docs/01-guides-principaux/DEV_MASTER.md` - Document central (Vision globale)
- [ ] `docs/03-regles-standards/WORKFLOWS.md` - Standards et workflow
- [ ] `docs/03-regles-standards/REGLES METIERS.md` - Règles business
- [ ] `docs/02-architecture/00-overview/API_ENDPOINTS.md` - APIs existantes
- [ ] `docs/02-architecture/01-database/DATABASE_SCHEMA.md` - Structure BDD
- [ ] `docs/02-architecture/00-overview/ATARYS_ARCHITECTURE.md` - Architecture technique

### **Questions à se poser OBLIGATOIREMENT :**
- [ ] Cette fonctionnalité existe-t-elle déjà ?
- [ ] Y a-t-il des standards ATARYS à respecter ?
- [ ] Quel module ATARYS (1.1 à 13.x) est concerné ?
- [ ] Y a-t-il des règles métier spécifiques ?
- [ ] L'architecture actuelle couvre-t-elle ce besoin ?

---

## 🏗️ **PHASE 2 : DÉVELOPPEMENT SELON STANDARDS**

### **Backend - Ordre obligatoire :**
1. [ ] **Modèle** : `backend/app/models/` selon structure SQLite
2. [ ] **Service** : `backend/app/services/` pour logique métier
3. [ ] **Routes** : `backend/app/routes/` avec blueprint
4. [ ] **Tests** : `backend/tests/` selon template existant
5. [ ] **Documentation** : Mettre à jour docs concernées

### **Frontend - Standards ATARYS :**
- [ ] **Layout** : Utiliser `PageLayout` et `GridLayout`
- [ ] **Nomenclature** : Nommage selon module (ex: `Module3_1.jsx`)
- [ ] **UI/UX** : Padding 16px, gap-3, responsive
- [ ] **API** : Format standardisé `{success, data, message}`

---

## 🔧 **PHASE 3 : VALIDATION ET COHÉRENCE**

### **Tests obligatoires :**
- [ ] **APIs** : Tester avec `.bat/test_api.bat`
- [ ] **Logs** : Vérifier `logs/atarys.log`
- [ ] **Base** : Analyser avec `analyze_real_db.py`
- [ ] **Frontend** : Valider dans navigateur

### **Documentation à mettre à jour :**
- [ ] `docs/README.md` si nouveau module
- [ ] `docs/02-architecture/00-overview/API_ENDPOINTS.md` si nouvelle API
- [ ] `docs/02-architecture/01-database/DATABASE_SCHEMA.md` si nouveau modèle
- [ ] `README.md` du module concerné

---

## 🎯 **EXEMPLES D'APPLICATION**

### **Problème : Erreur "Unexpected token"**
```
❌ AVANT : Corriger directement le code
✅ MAINTENANT : 
1. Consulter docs/WORKFLOWS.md
2. Vérifier docs/API_ENDPOINTS.md  
3. Analyser logs/atarys.log
4. Appliquer solution selon standards
```

### **Nouvelle fonctionnalité**
```
❌ AVANT : Coder directement
✅ MAINTENANT :
1. Identifier module concerné (ex: 3.1 Liste Chantiers)
2. Consulter docs/REGLES METIERS.md
3. Vérifier docs/ATARYS_ARCHITECTURE.md
4. Suivre workflow backend → frontend → tests
```

---

## 🚨 **RÈGLES D'OR**

1. **JAMAIS de code sans avoir lu la doc pertinente**
2. **TOUJOURS vérifier si ça existe déjà**  
3. **RESPECTER l'architecture et nomenclature ATARYS**
4. **METTRE À JOUR la documentation après développement**

---

## 📚 **RACCOURCIS DOCUMENTATION**

```bash
# Consultation rapide
docs/INDEX.md           # Vue d'ensemble
docs/CONSIGNES.md       # Workflow et standards
docs/DEV_MASTER.md      # Document central
docs/REGLES METIERS.md  # Règles business

# Technique
docs/API_ENDPOINTS.md   # Toutes les APIs
docs/DATABASE_SCHEMA.md # Structure complète
docs/TESTING_GUIDE.md   # Stratégie tests
```

**Cette checklist doit être consultée AVANT tout développement !** 