# 📄 Module 5 - DEVIS-FACTURATION

> **Gestion des ouvrages BATAPPLI, métrés et devis**  
> **État : EN COURS** ⚡ - Modèles partiellement implémentés  
> Dernière mise à jour : 19/07/2025

---

## 🎯 Vue d'ensemble

Le module **5 - DEVIS-FACTURATION** gère l'ensemble du processus de création de devis basé sur les ouvrages BATAPPLI et les fiches de métrés. Il remplace les onglets Excel correspondants par une interface web moderne et structurée.

### **Objectifs Principaux**
- Gestion des ouvrages et articles BATAPPLI
- Création et gestion des fiches métrés
- Génération des devis MEXT
- Modèles de devis types
- Calculs automatiques

---

## 📋 État d'Implémentation

### **✅ Implémenté**
- **Modèle SQLAlchemy** : `FamilleOuvrages` créé
- **Structure de base** : Pattern BaseModel respecté
- **Standards V2** : SQLAlchemy 2.0+ avec types appropriés

### **🔄 En Cours**
- **API REST** : Endpoints à créer
- **Interface Frontend** : Composants React à développer
- **Relations BDD** : Liens avec autres modules

### **❌ À Implémenter**
- **Modèles complets** : Articles, Devis, Factures
- **Logique métier** : Calculs, validations
- **Import/Export** : Intégration Excel

---

## 🏗️ Architecture Technique

### **Fichiers Concernés**
```
backend/app/models/module_5.py    # Modèles SQLAlchemy
backend/app/routes/module_5.py    # API REST (à créer)
backend/app/schemas/module_5.py   # Validation Marshmallow (à créer)
frontend/src/pages/Module5/       # Interface React (à créer)
```

### **Dépendances**
- **Module 6** : CLIENTS (pour les devis)
- **Module 7** : FOURNISSEURS (pour les achats)
- **Module 12** : PARAMÈTRES (pour la configuration)

---

## 📊 Sous-modules

Selon `ATARYS_MODULES.md`, le module 5 comprend :

### **5.1 - Ouvrages et articles BATAPPLI** ✅ **PARTIELLEMENT IMPLÉMENTÉ**
- Gestion des familles d'ouvrages (FamilleOuvrages créé)
- Catalogue des ouvrages BATAPPLI
- Articles et références

### **5.2 - FICHE MÈTRES** ❌ **À IMPLÉMENTER**
- Création des fiches de métrés
- Calculs de quantités
- Validation des mesures

### **5.3 - DEVIS MEXT** ❌ **À IMPLÉMENTER**
- Génération des devis MEXT
- Format standardisé
- Export et impression

### **5.4 - DEVIS TYPE** ❌ **À IMPLÉMENTER**
- Modèles de devis prédéfinis
- Templates réutilisables
- Personnalisation

---

## 🔗 Liens Utiles

- **[Modèles SQLAlchemy](./database-schema.md)** - Structure des tables
- **[API Endpoints](./api-endpoints.md)** - Spécifications REST
- **[Règles Métier](./business-rules.md)** - Logique fonctionnelle
- **[ATARYS_MODULES.md](../../00-overview/ATARYS_MODULES.md)** - Nomenclature officielle
