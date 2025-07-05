# 📚 Modules ATARYS - Nomenclature Officielle

> **Référence unique : organisation par chapitres ATARYS**
> Dernière mise à jour : 03/07/2025

---

## 📋 Vue d'ensemble

- **13 chapitres principaux** : Numérotés de 1 à 13
- **Sous-chapitres** : Format X.Y (ex: 1.1, 1.2, 3.1, etc.)
- **Organisation hiérarchique** : Structure claire et logique
- **Cohérence avec l'architecture** : Alignement sur les modèles et routes existants

---

## 📅 1. PLANNING

### Sous-chapitres
- 1.1 PLANNING SALARIÉS
- 1.2 PLANNING CHANTIER

### Tables Concernées
- `planning` - Planning des interventions

### Fonctionnalités
- Planning des chantiers
- Affectation des salariés
- Vue calendaire
- Gestion des interventions

### Routes API
- `/api/planning` - CRUD planning

---

## 📋 2. LISTE DES TACHES

### Sous-chapitres
- 2.1 YANN
- 2.2 JULIEN

### Tables Concernées
- `liste_taches` - Tâches personnalisées par utilisateur

### Fonctionnalités
- Liste de tâches personnalisées
- Suivi par utilisateur
- Priorisation des tâches

---

## 🏗️ 3. LISTE CHANTIERS

### Sous-chapitres
- 3.1 LISTE CHANTIERS
- 3.2 CHANTIERS PROJETS
- 3.3 CHANTIERS SIGNES
- 3.4 CHANTIERS EN COURS
- 3.5 CHANTIERS ARCHIVES

### Tables Concernées
- `chantiers` - Chantiers clients
- `etats_chantier` - États des chantiers

### Fonctionnalités
- Gestion des chantiers clients
- Suivi des états (Projet, Signé, En cours, Terminé, Annulé)
- Pipeline commercial complet
- Vue par statut

### Routes API
- `/api/chantiers` - CRUD chantiers

---

## 🏠 4. CHANTIERS

### Sous-chapitres
- 4.1 FICHE CHANTIER
- 4.2 PHOTOS CHANTIER
- 4.3 NOTES CHANTIER
- 4.4 DOCUMENTS CHANTIER

### Tables Concernées
- `chantiers` - Détails des chantiers
- `photos_chantier` - Photos des chantiers
- `notes_chantier` - Notes et commentaires
- `documents_chantier` - Documents associés

### Fonctionnalités
- Fiches détaillées des chantiers
- Gestion des photos
- Notes et commentaires
- Documents associés

---

## 📄 5. DEVIS-FACTURATION

### Sous-chapitres
- 5.1 DEVIS
- 5.2 FACTURES
- 5.3 RECOUVREMENTS

### Tables Concernées
- `devis` - Devis clients
- `factures` - Factures émises
- `recouvrements` - Suivi des paiements

### Fonctionnalités
- Création et gestion des devis
- Émission des factures
- Suivi des recouvrements
- Calculs automatiques

### Routes API
- `/api/devis` - CRUD devis
- `/api/factures` - CRUD factures

---

## 🔧 6. ATELIER

### Sous-chapitres
- 6.1 STOCK MATERIAUX
- 6.2 COMMANDES FOURNISSEURS
- 6.3 LIVRAISONS
- 6.4 INVENTAIRES
- 6.5 OUTILLAGE

### Tables Concernées
- `materiaux` - Stock des matériaux
- `commandes` - Commandes fournisseurs
- `livraisons` - Livraisons reçues
- `inventaires` - Inventaires de stock
- `outillage` - Gestion de l'outillage

### Fonctionnalités
- Gestion du stock
- Commandes fournisseurs
- Suivi des livraisons
- Inventaires
- Gestion de l'outillage

---

## 📊 7. GESTION

### Sous-chapitres
- 7.1 TABLEAUX DE BORD
- 7.2 RAPPORTS
- 7.3 STATISTIQUES

### Tables Concernées
- `statistiques` - Données statistiques
- `rapports` - Rapports générés
- `indicateurs` - Indicateurs de performance

### Fonctionnalités
- Tableaux de bord
- Rapports personnalisés
- Statistiques de performance
- Indicateurs clés

---

## 💰 8. COMPTABILITE

### Sous-chapitres
- 8.1 COMPTE RESULTAT
- 8.2 BILAN

### Tables Concernées
- `compte_resultat` - Compte de résultat
- `bilan` - Bilan comptable

### Fonctionnalités
- Compte de résultat
- Bilan comptable
- Analyse financière

---

## 👥 9. SOCIAL

### Sous-chapitres
- 9.1 SALARIES
- 9.2 CONGES
- 9.3 FORMATIONS

### Tables Concernées
- `salaries` - Salariés de l'entreprise
- `conges` - Gestion des congés
- `formations` - Formations suivies

### Fonctionnalités
- Gestion des salariés
- Planning des congés
- Suivi des formations

### Routes API
- `/api/salaries` - CRUD salariés

---

## 🛠️ 10. OUTILS

### Sous-chapitres
- 10.1 CALCULS ARDOISES
- 10.2 CALCULS ZINGUERIE
- 10.3 CALCULS COUVERTURE

### Tables Concernées
- `ardoise` - Calculs ardoises
- `ardoise_complet` - Calculs complets
- `pente` - Calculs de pente
- `surface` - Calculs de surface
- `materiau_ardoise` - Matériaux ardoises
- `calcul_ardoise` - Résultats calculs

### Fonctionnalités
- Calculs automatiques ardoises
- Calculs zinguerie
- Calculs couverture
- Outils de dimensionnement

### Routes API
- `/api/ardoises` - Calculs ardoises

---

## 📁 11. ARCHIVES

### Sous-chapitres
- 11.1 ARCHIVES CHANTIERS
- 11.2 ARCHIVES DEVIS
- 11.3 ARCHIVES FACTURES

### Tables Concernées
- `archives` - Archives générales

### Fonctionnalités
- Archivage des chantiers
- Archivage des devis
- Archivage des factures
- Conservation légale

---

## ⚙️ 12. PARAMETRES

### Sous-chapitres
- 12.1 PARAMETRES GENERAUX
- 12.2 CONFIGURATION

### Tables Concernées
- `parametres` - Paramètres système
- `configuration` - Configuration application

### Fonctionnalités
- Paramètres généraux
- Configuration système
- Personnalisation

---

## ❓ 13. AIDE

### Sous-chapitres
- 13.1 GUIDE UTILISATEUR
- 13.2 FAQ

### Tables Concernées
- `aide` - Contenu d'aide
- `faq` - Questions fréquentes

### Fonctionnalités
- Guide utilisateur
- FAQ interactive
- Support utilisateur

---

## 📊 Statistiques

- **1. PLANNING** : 1 table
- **2. LISTE DES TACHES** : 1 table
- **3. LISTE CHANTIERS** : 2 tables
- **4. CHANTIERS** : 4 tables
- **5. DEVIS-FACTURATION** : 3 tables
- **6. ATELIER** : 5 tables
- **7. GESTION** : 3 tables
- **8. COMPTABILITE** : 2 tables
- **9. SOCIAL** : 3 tables
- **10. OUTILS** : 6 tables
- **11. ARCHIVES** : 1 table
- **12. PARAMETRES** : 2 tables
- **13. AIDE** : 2 tables

**Total** : 35 tables organisées en 13 chapitres

---

**✅ Nomenclature officielle ATARYS - 13 chapitres organisés !** 