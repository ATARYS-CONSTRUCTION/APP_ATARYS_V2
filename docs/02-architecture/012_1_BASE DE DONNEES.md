# 🗄️ Module 12.1 - BASE DE DONNÉES ATARYS V2

> **Synthèse complète des fonctionnalités, architecture et workflow (juillet 2025)**

---

## 🚀 Fonctionnalités principales

- **Création dynamique de tables** depuis le frontend React (interface 12.1)
- **Génération automatique du modèle Python SQLAlchemy** côté backend (API Flask)
- **Ajout et suppression de tables** via l’interface (DROP TABLE)
- **Ajout de colonnes** à une table existante (ALTER TABLE ... ADD COLUMN ...)
- **Liste des tables** toujours à jour (chargement dynamique depuis la base SQLite)
- **Insertion, édition et suppression de données** dans toutes les tables créées
- **Synchronisation complète frontend/backend** via API REST

---

## 🏗️ Architecture technique

### **Frontend (React 18 + Vite)**
- Composant principal : `BaseDeDonnees.jsx`
- Création de table : `CreateTableForm.jsx`
- Ajout de colonne : mini-formulaire/modal intégré
- Suppression de table : bouton avec confirmation
- Liste des tables : chargée dynamiquement via `/api/create-table/list-tables`
- Appels API pour toutes les opérations (création, modification, suppression)

### **Backend (Flask 3 + SQLAlchemy 2)**
- Routes principales dans `backend/app/routes/create_table.py` :
  - `/api/create-table/` : création de table
  - `/api/create-table/generate-model` : génération du modèle Python
  - `/api/create-table/list-tables` : liste dynamique des tables
  - `/api/create-table/drop-table` : suppression de table
  - `/api/create-table/alter-table` : ajout de colonne
- Génération du code modèle via `utils/model_generator.py`
- Synchronisation automatique entre la structure SQLite et les modèles Python

---

## 🔄 Workflow utilisateur

1. **Créer une table**
   - L’utilisateur définit le nom, les colonnes, les types, etc. dans le frontend
   - Le backend crée la table dans SQLite et génère le modèle Python correspondant
   - La table apparaît instantanément dans la liste (12.1) et peut être utilisée pour l’insertion de données

2. **Ajouter une colonne**
   - L’utilisateur clique sur “Modifier la table”, saisit les infos de la colonne
   - Le backend exécute un ALTER TABLE ... ADD COLUMN ...
   - La colonne est ajoutée et utilisable immédiatement

3. **Supprimer une table**
   - L’utilisateur clique sur “Supprimer la table” (confirmation requise)
   - Le backend exécute un DROP TABLE
   - La table disparaît de la liste et de la base

4. **Insérer/éditer des données**
   - L’utilisateur peut saisir, coller ou éditer des données dans toutes les tables listées
   - Les opérations CRUD sont synchronisées avec le backend

---

## ⚙️ Points forts et bonnes pratiques

- **100% dynamique** : aucune modification de code nécessaire pour ajouter/supprimer des tables ou colonnes
- **Respect des standards ATARYS V2** : BaseModel, Numeric(10,2), architecture modulaire
- **API REST centralisée** : toutes les opérations passent par des endpoints documentés
- **Sécurité** : confirmation pour les actions destructives, validation des noms de tables/colonnes
- **Extensible** : possibilité d’ajouter d’autres opérations (renommer colonne/table, suppression colonne, etc.)

---

## 🔗 Lien avec la philosophie ATARYS V2

- **Modularité** : chaque table peut être rattachée à un module ATARYS (via moduleId)
- **Évolutivité** : architecture pensée pour accueillir de nouveaux modules/tables sans refonte
- **Transparence** : tout changement structurel est visible et traçable depuis l’interface
- **Automatisation** : génération de code, synchronisation, et gestion des modèles sans intervention manuelle

---

## 📝 Exemples de flux utilisateur

### **Créer une nouvelle table**
1. Cliquer sur “Créer une table”
2. Définir les colonnes, types, options
3. Valider : la table est créée, le modèle Python généré, la table apparaît dans la liste

### **Ajouter une colonne**
1. Sélectionner la table
2. Cliquer sur “Modifier la table”
3. Saisir le nom, type, options de la colonne
4. Valider : la colonne est ajoutée dynamiquement

### **Supprimer une table**
1. Sélectionner la table
2. Cliquer sur “Supprimer la table”
3. Confirmer : la table est supprimée de la base et de l’UI

---

## 🚦 Limites et points d’attention

- **Suppression de colonne** non encore implémentée (limite SQLite)
- **Modification du type d’une colonne** non supportée (nécessite migration)
- **Redémarrage de Flask-Admin** nécessaire pour voir la nouvelle table dans l’admin
- **Les modèles Python générés ne sont pas “hot-reload”** (nécessitent un reload du backend pour prise en compte complète)

---

**Le module 12.1 offre désormais une gestion de base de données dynamique, robuste et conforme à la philosophie ATARYS V2, accessible à tous les utilisateurs depuis l’interface web.** 