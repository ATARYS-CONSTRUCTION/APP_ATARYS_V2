# Architecture ATARYS V2

## Vue d'ensemble

Cette section documente l'architecture technique complète d'ATARYS V2, incluant la structure de la base de données, les modules fonctionnels, et les standards de développement.

## Structure des dossiers

### 00-overview/
- **ATARYS_ARCHITECTURE.md** : Architecture technique générale
- **ATARYS_MODULES.md** : Vue d'ensemble des modules fonctionnels
- **DEPLOYMENT.md** : Guide de déploiement

### 01-database/
- **DATABASE_SCHEMA.md** : Schéma complet de la base de données
- **API_ENDPOINTS.md** : Documentation des APIs REST

### 02-modules/
- **README_MODULES.md** : Guide des modules
- **module_01_planning.md** : Module 1 - Planning
- **module_03_chantiers.md** : Module 3 - Chantiers
- **module_05_devis_facturation.md** : Module 5 - Devis et Facturation
- **module_09_social.md** : Module 9 - Social
- **module_10_calcul_ardoises.md** : Module 10 - Calcul Ardoises
- **module_12_base_donnees.md** : Module 12 - Base de Données

### 03-deployment/
- **DEPLOYMENT.md** : Guide de déploiement
- **CONFIGURATION.md** : Configuration serveur

## Standards techniques

### Backend
- **Framework** : Flask 3.0+
- **ORM** : SQLAlchemy 2.0+
- **Base de données** : SQLite
- **Architecture** : Factory pattern

### Frontend
- **Framework** : React 18.2.0
- **Build tool** : Vite 5.4.19
- **CSS** : Tailwind CSS 3.4.1
- **Architecture** : Component-based

### APIs
- **Format** : REST JSON
- **Structure** : `{success, data, message}`
- **Validation** : Marshmallow schemas
- **Authentification** : Session-based

## Modules fonctionnels

### Module 1 - Planning
Gestion du planning des chantiers et des équipes.

### Module 2 - Clients
Gestion des clients et prospects.

### Module 3 - Chantiers
Suivi complet des chantiers de couverture.

### Module 4 - Stock
Gestion des matériaux et fournitures.

### Module 5 - Devis et Facturation
Génération de devis et facturation.

### Module 6 - Comptabilité
Gestion comptable complète.

### Module 7 - Maintenance
Maintenance et support technique.

### Module 8 - Rapports
Génération de rapports et analyses.

### Module 9 - Social
Gestion des salariés et ressources humaines.

### Module 10 - Calcul Ardoises
Calculs techniques pour les ardoises.

### Module 11 - Qualité
Contrôle qualité et certifications.

### Module 12 - Base de Données
Gestion et maintenance de la base de données.

### Module 13 - Administration
Administration système et utilisateurs.

## Conventions

### Nommage
- **Fichiers Python** : snake_case
- **Classes** : PascalCase
- **Variables** : snake_case
- **Constantes** : UPPER_SNAKE_CASE

### Base de données
- **Tables** : snake_case
- **Colonnes** : snake_case
- **Clés étrangères** : `table_id`
- **Contraintes** : `fk_table_column`

### APIs
- **Endpoints** : kebab-case
- **Paramètres** : snake_case
- **Réponses** : camelCase

## Développement

### Workflow
1. **Modèles** : Définir les modèles SQLAlchemy
2. **Services** : Implémenter la logique métier
3. **Routes** : Créer les endpoints API
4. **Frontend** : Développer les composants React
5. **Tests** : Écrire les tests unitaires et d'intégration

### Standards
- **Documentation** : Toujours à jour
- **Tests** : Couverture minimale 80%
- **Code** : PEP 8 pour Python, ESLint pour JavaScript
- **Git** : Commits conventionnels

## Maintenance

### Sauvegarde
- **Base de données** : Quotidienne
- **Code** : Versioning Git
- **Configuration** : Environnements séparés

### Monitoring
- **Logs** : Centralisés
- **Performance** : Métriques temps réel
- **Erreurs** : Alertes automatiques

## Évolutions

### Court terme
- Amélioration des performances
- Correction des bugs
- Ajout de fonctionnalités mineures

### Moyen terme
- Refactoring du code
- Optimisation de la base de données
- Amélioration de l'UX

### Long terme
- Migration vers microservices
- Intégration IA/ML
- Déploiement cloud 