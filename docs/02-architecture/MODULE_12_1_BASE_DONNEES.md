# 📊 Module 12.1 - BASE DE DONNÉES

> **Gestion dynamique des tables SQLite ATARYS**  
> **Interface d'administration complète**  
> Dernière mise à jour : 05/07/2025

---

## 🎯 Vue d'ensemble

Le module **12.1 Base de Données** fournit une interface complète pour gérer dynamiquement les tables SQLite du système ATARYS. Il comprend deux fonctionnalités principales intégrées dans un seul composant React.

---

## 🏗️ Fonctionnalités Principales

### **12.1.1 - CRÉER UNE TABLE**
- **Interface** : Formulaire `CreateTableForm` dans `BaseDeDonnees.jsx`
- **Fonctionnalités** :
  - Création de tables avec nom personnalisé
  - Définition de colonnes avec types SQLAlchemy
  - Gestion des contraintes (nullable, unique, default)
  - Génération automatique de code backend (modèle, schéma, routes)
  - Validation et écriture des fichiers après confirmation utilisateur

### **12.1.2 - MODIFIER UNE TABLE**
- **Interface** : Modal d'ajout de colonne dans `BaseDeDonnees.jsx`
- **Fonctionnalités** :
  - Ajout de nouvelles colonnes aux tables existantes
  - Support de tous les types SQLAlchemy (String, Text, Integer, Numeric, REAL, Boolean, Date, DateTime)
  - Configuration des contraintes (nullable, unique, default)
  - Mise à jour automatique de la structure

---

## 🔧 Architecture Technique

### **Composant Frontend**
```jsx
// frontend/src/pages/BaseDeDonnees.jsx
- Interface unifiée pour les deux fonctionnalités
- Gestion d'état avec useState pour les formulaires
- Intégration avec les APIs backend
- Validation et gestion d'erreurs
```

### **APIs Backend**
```python
# backend/app/routes/create_table.py
- /api/create-table/create-table (POST)
- /api/create-table/list-tables (GET)
- /api/create-table/drop-table (POST)
- /api/create-table/alter-table (POST)
- /api/create-table/generate-code (POST)
- /api/create-table/write-code (POST)
```

### **Types de Données Supportés**
- **String** : Texte court avec longueur max configurable
- **Text** : Texte long sans limite
- **Integer** : Nombre entier
- **Numeric** : Montant financier (10,2) - Standard ATARYS
- **REAL** : Nombre décimal pour mesures techniques
- **Boolean** : Vrai/Faux
- **Date** : Date simple
- **DateTime** : Date avec heure

---

## 🎨 Interface Utilisateur

### **Boutons d'Action**
```jsx
// Boutons principaux dans l'interface
- 🏗️ "Créer une table" → Ouvre CreateTableForm
- 🛠️ "Modifier la table" → Ouvre modal d'ajout de colonne
- 🗑️ "Supprimer la table" → Suppression avec confirmation
- ➕ "Ajouter une ligne" → Ajout manuel de données
```

### **Formulaires**
```jsx
// CreateTableForm
- Nom de la table
- Liste dynamique des colonnes
- Types SQLAlchemy avec validation
- Boutons d'ajout/suppression de colonnes

// Modal d'ajout de colonne
- Nom de la colonne
- Sélection du type
- Configuration des contraintes
- Valeur par défaut
```

---

## 🔄 Workflow de Création de Table

### **Étape 1 : Interface Utilisateur**
1. Utilisateur clique sur "Créer une table"
2. Formulaire `CreateTableForm` s'ouvre
3. Saisie du nom et des colonnes
4. Validation côté frontend

### **Étape 2 : Génération Backend**
1. Envoi des données à `/api/create-table/generate-code`
2. Génération automatique du code :
   - Modèle SQLAlchemy (backend/app/models/)
   - Schéma Marshmallow (backend/app/schemas/)
   - Routes API (backend/app/routes/)
3. Retour du code généré au frontend

### **Étape 3 : Validation et Écriture**
1. Affichage du code généré pour validation
2. Confirmation utilisateur
3. Envoi à `/api/create-table/write-code`
4. Écriture des fichiers dans le backend
5. Création de la table dans SQLite

### **Étape 4 : Intégration**
1. Mise à jour de la liste des tables
2. Affichage dans l'interface
3. Possibilité d'ajouter des données

---

## 🔄 Workflow de Modification de Table

### **Étape 1 : Sélection**
1. Utilisateur sélectionne une table existante
2. Clic sur "Modifier la table"
3. Ouverture du modal d'ajout de colonne

### **Étape 2 : Configuration**
1. Saisie du nom de la nouvelle colonne
2. Sélection du type de données
3. Configuration des contraintes (nullable, unique, default)
4. Validation des paramètres

### **Étape 3 : Application**
1. Envoi à `/api/create-table/alter-table`
2. Génération de la commande ALTER TABLE
3. Exécution dans SQLite
4. Mise à jour de l'interface

---

## 🛡️ Sécurité et Validation

### **Validation Frontend**
```javascript
// Validation des noms de tables
- Caractères autorisés uniquement
- Pas de mots-clés SQL réservés
- Longueur minimale/maximale

// Validation des colonnes
- Types de données valides
- Contraintes cohérentes
- Valeurs par défaut appropriées
```

### **Validation Backend**
```python
# Validation SQLAlchemy
- Types de données supportés
- Contraintes SQLite valides
- Gestion des erreurs de syntaxe

# Sécurité
- Protection contre l'injection SQL
- Validation des noms de tables
- Rollback en cas d'erreur
```

---

## 📊 Gestion des Données

### **Chargement Dynamique**
```javascript
// Chargement des tables disponibles
fetch('/api/create-table/list-tables')
  .then(res => res.json())
  .then(result => setAvailableTables(result.tables));
```

### **Manipulation des Données**
```javascript
// Collage Excel
- Support du format tabulation
- Nettoyage automatique des données
- Validation des types

// Édition en ligne
- Modification directe dans le tableau
- Sauvegarde automatique
- Gestion des erreurs
```

---

## 🔧 Configuration et Personnalisation

### **Types de Données Standards ATARYS**
```python
# Montants financiers (OBLIGATOIRE)
montant_ht = db.Column(db.Numeric(10, 2), default=0.00)

# Textes avec longueur max
nom = db.Column(db.String(100), nullable=False)

# Mesures techniques
longueur = db.Column(db.REAL, nullable=True)
```

### **Contraintes par Défaut**
```python
# Colonnes obligatoires
- id : Primary key automatique
- created_at : Timestamp automatique
- updated_at : Timestamp automatique

# Contraintes ATARYS
- Montants en Numeric(10, 2)
- Textes avec longueur max définie
- Validation Marshmallow obligatoire
```

---

## 🚨 Gestion d'Erreurs

### **Erreurs Fréquentes**
```javascript
// Erreurs de création de table
- Nom de table déjà existant
- Syntaxe SQL invalide
- Types de données non supportés

// Erreurs de modification
- Colonne déjà existante
- Contraintes incompatibles
- Erreurs de migration SQLite
```

### **Solutions Automatiques**
```python
# Nettoyage des noms
- Remplacement des caractères spéciaux
- Conversion en snake_case
- Validation des mots-clés SQL

# Gestion des conflits
- Ajout de suffixe numérique
- Rollback automatique
- Messages d'erreur explicites
```

---

## 📈 Évolutions Futures

### **Fonctionnalités Prévues**
- **Suppression de colonnes** : ALTER TABLE DROP COLUMN
- **Modification de colonnes** : ALTER TABLE MODIFY
- **Index automatiques** : Création d'index sur les clés
- **Relations** : Gestion des clés étrangères
- **Migrations** : Système de migrations SQLAlchemy

### **Améliorations Interface**
- **Drag & Drop** : Réorganisation des colonnes
- **Prévisualisation** : Aperçu de la structure
- **Templates** : Modèles de tables prédéfinis
- **Import/Export** : Sauvegarde des structures

---

## 📚 Documentation Associée

### **Fichiers Techniques**
- `frontend/src/pages/BaseDeDonnees.jsx` : Composant principal
- `frontend/src/components/CreateTableForm.jsx` : Formulaire de création
- `backend/app/routes/create_table.py` : APIs backend
- `backend/app/models/` : Modèles générés

### **Documentation ATARYS**
- `docs/02-architecture/ATARYS_ARCHITECTURE.md` : Architecture générale
- `docs/02-architecture/API_ENDPOINTS.md` : APIs disponibles
- `docs/03-regles-standards/REGLES METIERS.md` : Règles business

---

**✅ Module 12.1 Base de Données - Interface complète pour la gestion dynamique des tables SQLite ATARYS !** 