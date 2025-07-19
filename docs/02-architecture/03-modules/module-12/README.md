# ⚙️ Module 12 - PARAMÈTRES

> **Configuration système et gestion de la base de données**  
> **État : EN COURS** ⚡ - Tables de test et interface dynamique implémentées  
> Dernière mise à jour : 19/07/2025

---

## 🎯 Vue d'ensemble

Le module **12 - PARAMÈTRES** fournit l'interface d'administration et de configuration du système ATARYS. Il comprend principalement la gestion dynamique de la base de données, la configuration système et la personnalisation.

### **Objectifs Principaux**
- Gestion dynamique des tables SQLite (BASE DE DONNÉES)
- Configuration des paramètres système
- Interface d'administration complète
- Outils de maintenance et audit
- Personnalisation de l'interface

---

## 📋 État d'Implémentation

### **✅ Implémenté**
- **Tables de test** : `TestAuditTable`, `TestCle2` avec relations
- **Interface de gestion** : Création dynamique de tables
- **Service générateur** : `TableGeneratorService`
- **Relations BDD** : Clés étrangères avec module 9

### **🔄 En Cours**
- **API REST complète** : Endpoints de gestion
- **Interface Frontend** : Composants React avancés
- **Validation** : Schémas Marshmallow

### **❌ À Implémenter**
- **Paramètres système** : Configuration globale
- **Audit complet** : Logs et traçabilité
- **Sauvegarde/Restauration** : Outils de maintenance

---

## 🏗️ Architecture Technique

### **Fichiers Concernés**
```
backend/app/models/module_12.py      # Modèles SQLAlchemy ✅
backend/app/routes/create_table.py   # API création tables ✅
backend/app/services/table_generator.py # Service génération (à créer)
frontend/src/pages/Module12/         # Interface React (à créer)
```

### **Fonctionnalités Clés**
1. **Création dynamique de tables** ✅
2. **Modification de structure** 🔄
3. **Suppression sécurisée** 🔄
4. **Génération de code automatique** ✅

---

## 📊 Sous-modules

Selon `ATARYS_MODULES.md`, le module 12 comprend :

### **12.1 - BASE DE DONNÉES** ✅ **PARTIELLEMENT IMPLÉMENTÉ**
- Interface de gestion des tables SQLite
- Création dynamique de tables SQLite
- Modification de structure de tables existantes (ajout de colonnes)
- Gestion des colonnes et contraintes
- Interface d'administration des bases de données
- Tables de test opérationnelles (TestAuditTable, TestCle2)

### **Fonctionnalités Supplémentaires** ❌ **À IMPLÉMENTER**
- Configuration système
- Personnalisation de l'interface
- Paramètres utilisateur
- Gestion des préférences

---

## 🔗 Relations avec Autres Modules

### **Module 9 - LISTE_SALARIÉS**
```python
# Relation existante dans TestCle2
niveau_qualification_id → niveau_qualification.id
```

### **Tous les Modules**
- Génération automatique de modèles
- Création d'APIs REST standardisées
- Service de développement transversal

---

## 🛠️ Interface de Gestion

### **Fonctionnalités Disponibles**
1. **Créer une table** : Formulaire avec sélection module ATARYS
2. **Modifier une table** : Ajout/suppression de colonnes
3. **Supprimer une table** : Avec confirmation et nettoyage
4. **Générer le code** : Modèles, routes, schémas automatiques

### **Workflow Professionnel**
1. Définition de la structure
2. Génération du code backend
3. Exécution des migrations
4. Validation et tests

---

## 🔗 Liens Utiles

- **[Modèles SQLAlchemy](./database-schema.md)** - Structure des tables
- **[API Endpoints](./api-endpoints.md)** - Spécifications REST
- **[Service Generator](./table-generator.md)** - Documentation technique
- **[ATARYS_MODULES.md](../../00-overview/ATARYS_MODULES.md)** - Nomenclature officielle
