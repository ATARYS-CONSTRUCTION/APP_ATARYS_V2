# 📄 Guide Utilisateur - Extraction Intelligente de Documents

> **Guide complet pour l'extraction automatique et la ventilation IA des factures/LCR**  
> **Module 8.1 - Traitement intelligent des documents fournisseurs**  
> Dernière mise à jour : 20/01/2025

---

## 🎯 Objectif du Guide

Ce guide vous explique comment utiliser le système d'extraction automatique ATARYS pour traiter vos factures et LCR fournisseurs avec l'aide de l'intelligence artificielle.

**Ce que fait le système :**
- ✅ Lit automatiquement vos PDF de factures
- ✅ Extrait tous les bons de livraison
- ✅ Propose une ventilation intelligente par chantier
- ✅ Vous permet de valider et corriger facilement

**Gain de temps estimé :** 85% de temps gagné sur la saisie comptable !

---

## 🚀 Démarrage Rapide (2 minutes)

### **Étape 1 : Accéder au module**
1. Ouvrir ATARYS dans votre navigateur
2. Aller dans **Module 8.1 - Extraction Documents**
3. Cliquer sur **"Nouveau document"**

### **Étape 2 : Uploader votre PDF**
1. Glisser-déposer votre fichier PDF dans la zone prévue
2. Le système analyse automatiquement le type de document
3. Attendre la fin du traitement (2-3 minutes en moyenne)

### **Étape 3 : Valider les résultats**
1. Vérifier les données extraites (numéro facture, fournisseur, montant)
2. Contrôler la ventilation IA proposée pour chaque bon
3. Corriger si nécessaire
4. Cliquer sur **"Valider et comptabiliser"**

**C'est terminé !** Votre facture est intégrée en comptabilité avec la ventilation par chantier.

---

## 📋 Interface Utilisateur Détaillée

### **Page d'Accueil Module 8.1**

```
┌─────────────────────────────────────────────────────────────────┐
│ 📄 Module 8.1 - Extraction Intelligente de Documents           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ [🆕 Nouveau document]  [📋 À valider (3)]  [📊 Historique]     │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 📊 Statistiques du mois                                    │ │
│ │ • Documents traités : 45                                   │ │
│ │ • Précision IA : 87%                                       │ │
│ │ • Temps moyen validation : 3 min                           │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 🔄 Dernières extractions                                   │ │
│ │ • facture_mbr_ca000190.pdf - ✅ Validé                    │ │
│ │ • lcr_delaire_janvier.pdf - ⏳ À valider                  │ │
│ │ • facture_foussier_12345.pdf - ❌ Erreur                  │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### **Zone d'Upload de Documents**

```
┌─────────────────────────────────────────────────────────────────┐
│ 📤 Nouveau Document à Extraire                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│         ┌─────────────────────────────────────┐                 │
│         │                                     │                 │
│         │  📄  Glisser-déposer votre PDF     │                 │
│         │      ou cliquer pour sélectionner  │                 │
│         │                                     │                 │
│         │     Types supportés :               │                 │
│         │     • Factures fournisseurs         │                 │
│         │     • LCR (Lettres de Change)       │                 │
│         │     • Relevés de livraison          │                 │
│         │                                     │                 │
│         └─────────────────────────────────────┘                 │
│                                                                 │
│ ⚙️ Options avancées :                                          │
│ ☐ Forcer le workflow d'extraction                              │
│ ☐ Désactiver la ventilation automatique IA                     │
│ ☐ Envoyer par email après traitement                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### **Traitement en Cours**

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔄 Traitement en cours - facture_mbr_ca000190.pdf             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ✅ Analyse du document terminée                                │
│    Type détecté : Facture MBR avec bons de livraison          │
│                                                                 │
│ 🔄 Extraction des données en cours...                         │
│    Workflow n8n actif : 8.1 extraction_tva                   │
│    ██████████████████████░░░░ 80%                             │
│                                                                 │
│ ⏳ Analyse IA de ventilation...                               │
│    Recherche des chantiers correspondants                      │
│                                                                 │
│ Temps estimé restant : 45 secondes                            │
│                                                                 │
│ [❌ Annuler]                            [📄 Voir détails]     │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✅ Validation des Extractions

### **Interface de Validation Principale**

```
┌─────────────────────────────────────────────────────────────────┐
│ ✅ Validation - facture_mbr_ca000190.pdf                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 📄 INFORMATIONS FACTURE                                        │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Numéro facture : CA000190                    [✏️ Modifier] │ │
│ │ Fournisseur : MBR                            [✏️ Modifier] │ │  
│ │ Date facture : 30/06/2025                    [✏️ Modifier] │ │
│ │ Total HT : 6 984,74 €                        [✏️ Modifier] │ │
│ │ Total TTC : 8 367,87 €                       [✏️ Modifier] │ │
│ │                                                             │ │
│ │ ✅ Cohérence montants : OK                                  │ │
│ │ 🎯 Confiance extraction : 95%                               │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ 📦 BONS DE LIVRAISON AVEC VENTILATION IA                       │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Bon 351020 - 65,09 € HT                                    │ │
│ │ Réf: MO/190DEBOIS/282963/S24                               │ │
│ │                                                             │ │
│ │ 🤖 SUGGESTION IA (98% sûr) :                               │ │
│ │ 🎯 Chantier "Maison DEBOIS rue des Lilas"                  │ │
│ │ 💡 Raison: Correspondance exacte "190DEBOIS"               │ │
│ │                                                             │ │
│ │ [✅ Accepter] [🔄 Changer] [➕ Nouveau chantier]           │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Bon 351022 - 1 118,25 € HT                                 │ │
│ │ Réf: BESCOND                                                │ │
│ │                                                             │ │
│ │ 🤖 SUGGESTION IA (85% sûr) :                               │ │
│ │ 🎯 Chantier "Extension BESCOND"                             │ │
│ │ 💡 Raison: Client connu, chantier actif                    │ │
│ │                                                             │ │
│ │ Autres suggestions :                                        │ │
│ │ • Nouveau chantier BESCOND (30%)                            │ │
│ │ • Frais généraux (10%)                                      │ │
│ │                                                             │ │
│ │ [✅ Accepter] [🔄 Changer] [➕ Nouveau chantier]           │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Bon 351023 - 66,54 € HT                                    │ │
│ │ Réf: PASCOT                                                 │ │
│ │                                                             │ │
│ │ ❓ VENTILATION INCERTAINE :                                │ │
│ │ 🎯 Suggestions IA :                                         │ │
│ │ • Chantier "Rénovation PASCOT" (60%)                       │ │
│ │ • Nouveau chantier PASCOT (30%)                             │ │  
│ │ • Frais généraux (10%)                                      │ │
│ │                                                             │ │
│ │ [🔽 Choisir manuellement ▼]                               │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ 📊 RÉCAPITULATIF VENTILATION                                   │
│ Total facture : 6 984,74 €                                     │
│ Total ventilé : 1 249,88 € (18%)                               │
│ Non ventilé : 5 734,86 € (82%) ⚠️                             │
│                                                                 │
│ [✅ VALIDER TOUT] [🔄 CORRIGER] [❌ REJETER]                  │
└─────────────────────────────────────────────────────────────────┘
```

### **Sélection Manuelle de Chantier**

```
┌─────────────────────────────────────────────────────────────────┐
│ 🎯 Affecter le bon 351023 (66,54 €) - Réf: PASCOT            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 🔍 Rechercher un chantier :                                    │
│ [PASCOT__________________] 🔍                                   │
│                                                                 │
│ 📋 Chantiers trouvés :                                         │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ ✅ Rénovation PASCOT - Salle de bain                       │ │
│ │    Client: M. PASCOT - Statut: EN_COURS                    │ │
│ │    Dernière livraison: 15/06/2025                          │ │
│ │    [SÉLECTIONNER]                                           │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 📋 Extension PASCOT - Garage                                │ │
│ │    Client: Mme PASCOT - Statut: PROJET                     │ │
│ │    Date début prévue: 01/08/2025                            │ │
│ │    [SÉLECTIONNER]                                           │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ 🆕 Actions alternatives :                                       │
│ [➕ Créer nouveau chantier PASCOT]                             │
│ [💼 Affecter aux frais généraux]                               │
│ [⏳ Traiter plus tard]                                         │
│                                                                 │
│ [❌ Annuler]                              [✅ Confirmer]      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Fonctionnalités Avancées

### **Corrections Manuelles**

#### **Corriger les Données de Facture**
```
┌─────────────────────────────────────────────────────────────────┐
│ ✏️ Correction Facture CA000190                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Numéro facture : [CA000190_______________] ✅                   │
│ Fournisseur : [MBR______________________] ✅                   │
│ Date facture : [30/06/2025______________] ✅                   │
│                                                                 │
│ Total HT : [6984,74_____________________] ⚠️                   │
│ ⚠️ Attention: Modification du montant HT                       │
│ Impact sur ventilation des bons                                 │
│                                                                 │
│ Total TTC : [8367,87____________________] ✅                   │
│                                                                 │
│ 📝 Motif de correction :                                        │
│ [Erreur lecture OCR montant HT_________________________]       │
│                                                                 │
│ [❌ Annuler]                          [✅ Appliquer]          │
└─────────────────────────────────────────────────────────────────┘
```

#### **Corriger un Bon de Livraison**
```
┌─────────────────────────────────────────────────────────────────┐
│ ✏️ Correction Bon 351020                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Numéro bon : [351020____________________] ✅                   │
│ Montant HT : [65,09_____________________] ✅                   │
│                                                                 │
│ Référence client :                                              │
│ [MO/190DEBOIS/282963/S24_________________________________]     │
│                                                                 │
│ Description :                                                   │
│ [Matériaux charpente bois traité_________________________]     │
│ [_______________________________________________________]      │
│                                                                 │
│ 📝 Motif de correction :                                        │
│ [Référence client mal extraite__________________________]      │
│                                                                 │
│ [❌ Annuler]                          [✅ Appliquer]          │
└─────────────────────────────────────────────────────────────────┘
```

### **Création de Nouveau Chantier**

```
┌─────────────────────────────────────────────────────────────────┐
│ 🆕 Créer Nouveau Chantier                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Informations principales :                                      │
│ Nom chantier : [Rénovation PASCOT garage________________]      │
│ Client : [M. PASCOT_________________________________]          │
│                                                                 │
│ Type de chantier :                                              │
│ [🔽 Rénovation                                           ▼]    │
│                                                                 │
│ Statut initial :                                                │
│ [🔽 Projet                                               ▼]    │
│                                                                 │
│ 📍 Adresse :                                                    │
│ [15 rue des Tilleuls_________________________________]         │
│ [35000 RENNES____________________________________]            │
│                                                                 │
│ 💰 Budget estimé :                                              │
│ [25000______________________] €                                │
│                                                                 │
│ 📅 Dates prévisionnelles :                                     │
│ Début : [01/08/2025__] Fin : [30/09/2025__]                   │
│                                                                 │
│ 🔑 Mots-clés pour IA (séparés par virgules) :                  │
│ [PASCOT,garage,renovation____________________________]         │
│                                                                 │
│ ✅ Affecter automatiquement ce bon au nouveau chantier         │
│                                                                 │
│ [❌ Annuler]                          [✅ Créer chantier]      │
└─────────────────────────────────────────────────────────────────┘
```

### **Gestion des Cas Particuliers**

#### **Frais Généraux**
```
┌─────────────────────────────────────────────────────────────────┐
│ 💼 Affectation aux Frais Généraux                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Bon concerné : 351023 - 66,54 € HT                             │
│ Référence : PASCOT                                              │
│                                                                 │
│ Type de frais généraux :                                        │
│ [🔽 Fournitures bureau                                    ▼]    │
│                                                                 │
│ Options disponibles :                                           │
│ • Fournitures bureau                                            │
│ • Carburant véhicules                                           │
│ • Outillage général                                             │
│ • Assurances                                                    │
│ • Entretien matériel                                            │
│ • Autres frais généraux                                         │
│                                                                 │
│ 📝 Commentaire (optionnel) :                                    │
│ [Achat consommables bureau_______________________________]     │
│                                                                 │
│ [❌ Annuler]                          [✅ Affecter]           │
└─────────────────────────────────────────────────────────────────┘
```

#### **Traitement Différé**
```
┌─────────────────────────────────────────────────────────────────┐
│ ⏳ Reporter le Traitement                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Bon concerné : 351023 - 66,54 € HT                             │
│ Référence : PASCOT                                              │
│                                                                 │
│ Raison du report :                                              │
│ [🔽 Attendre informations client                          ▼]    │
│                                                                 │
│ Options disponibles :                                           │
│ • Attendre informations client                                  │
│ • Vérifier avec comptable                                       │
│ • Clarifier avec fournisseur                                    │
│ • Nouveau chantier en cours de création                         │
│ • Autre raison                                                  │
│                                                                 │
│ 📅 Date de rappel :                                             │
│ [25/01/2025__] (dans 5 jours)                                  │
│                                                                 │
│ 📝 Note pour rappel :                                           │
│ [Vérifier si chantier PASCOT garage confirmé___________]       │
│ [_____________________________________________________]         │
│                                                                 │
│ [❌ Annuler]                          [✅ Reporter]           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Suivi et Historique

### **Page d'Historique des Extractions**

```
┌─────────────────────────────────────────────────────────────────┐
│ 📊 Historique des Extractions                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 🔍 Filtres :                                                    │
│ Période : [Janvier 2025 ▼] Fournisseur : [Tous ▼]            │
│ Statut : [Tous ▼] Utilisateur : [Tous ▼]                      │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Date        │ Fichier              │ Fournisseur │ Statut   │ │
│ ├─────────────┼─────────────────────┼─────────────┼─────────┤ │
│ │ 20/01 10:30 │ facture_mbr_ca0001  │ MBR         │ ✅ Validé│ │
│ │ 19/01 14:15 │ lcr_delaire_jan.pdf │ DELAIRE     │ ⏳ Attndt│ │
│ │ 18/01 09:22 │ facture_fouss_123   │ FOUSSIER    │ ❌ Erreur│ │
│ │ 17/01 16:45 │ facture_mbr_ca0002  │ MBR         │ ✅ Validé│ │
│ │ 16/01 11:33 │ lcr_rubion_dec.pdf  │ RUBION      │ ✅ Validé│ │
│ └─────────────┴─────────────────────┴─────────────┴─────────┘ │
│                                                                 │
│ 📈 Statistiques de la période :                                │
│ • Total extractions : 125                                      │
│ • Taux de succès : 94%                                         │
│ • Précision IA moyenne : 86%                                   │
│ • Temps moyen validation : 3 min 45s                           │
│                                                                 │
│ [📥 Exporter CSV] [📊 Rapport détaillé] [🔄 Actualiser]       │
└─────────────────────────────────────────────────────────────────┘
```

### **Détail d'une Extraction**

```
┌─────────────────────────────────────────────────────────────────┐
│ 📄 Détail Extraction - facture_mbr_ca000190.pdf               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 📋 Informations générales :                                    │
│ • Date traitement : 20/01/2025 à 10:30                         │
│ • Utilisateur : Julie MARTIN                                   │
│ • Workflow n8n : 8.1 extraction_tva                           │
│ • Temps total : 2 min 34s                                      │
│                                                                 │
│ ⚙️ Détails techniques :                                         │
│ • Taille fichier : 2.4 Mo                                      │
│ • Pages analysées : 3                                           │
│ • Confiance OCR : 97%                                          │
│ • Confiance IA : 89%                                           │
│                                                                 │
│ 📊 Résultats extraction :                                       │
│ • Facture principale : 1                                       │
│ • Bons de livraison : 3                                        │
│ • Montant total : 6 984,74 €                                   │
│ • Bons ventilés : 3/3 (100%)                                  │
│                                                                 │
│ 🎯 Performance IA :                                             │
│ • Suggestions acceptées : 2/3 (67%)                            │
│ • Suggestions modifiées : 1/3 (33%)                            │
│ • Créations de chantiers : 0                                   │
│                                                                 │
│ 📝 Actions utilisateur :                                       │
│ • Corrections facture : 0                                      │
│ • Corrections bons : 1 (référence client)                      │
│ • Temps validation : 4 min 12s                                 │
│                                                                 │
│ [📄 Voir PDF original] [🔍 Détails JSON] [📧 Envoyer rapport] │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Configuration et Personnalisation

### **Préférences Utilisateur**

```
┌─────────────────────────────────────────────────────────────────┐
│ ⚙️ Préférences Extraction Intelligente                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 🤖 Paramètres IA :                                             │
│ ☑️ Activer les suggestions automatiques                        │
│ ☑️ Accepter auto les suggestions >95% confiance                │
│ ☐ Désactiver notifications temps réel                          │
│                                                                 │
│ Seuil d'auto-validation : [90%_____] 🎚️                      │
│ (Suggestions IA acceptées automatiquement si >90%)             │
│                                                                 │
│ 📧 Notifications :                                              │
│ ☑️ Email à la fin de chaque extraction                         │
│ ☑️ Alerte si erreur d'extraction                               │
│ ☐ Rapport hebdomadaire automatique                             │
│                                                                 │
│ 🎯 Affectations par défaut :                                   │
│ Petits montants (<50€) : [Frais généraux ▼]                   │
│ Fournisseurs inconnus : [Créer automatiquement ▼]             │
│ Références ambiguës : [Demander confirmation ▼]                │
│                                                                 │
│ 📊 Interface :                                                  │
│ ☑️ Afficher les scores de confiance IA                         │
│ ☑️ Montrer les suggestions alternatives                         │
│ ☑️ Historique des corrections dans tooltips                    │
│                                                                 │
│ [❌ Annuler]              [💾 Sauvegarder] [🔄 Réinitialiser] │
└─────────────────────────────────────────────────────────────────┘
```

### **Configuration des Workflows**

```
┌─────────────────────────────────────────────────────────────────┐
│ ⚙️ Configuration Workflows n8n                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 🔄 Workflows actifs :                                           │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 8.1 extraction_tva         │ ✅ ACTIF    │ [Configurer]   │ │
│ │ Factures/LCR fournisseurs  │ 245 docs    │ [Tester]       │ │
│ │ Précision : 87%            │ dernière: 2h │ [Logs]         │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 8.2 extraction_devis       │ 🔄 DEV      │ [Configurer]   │ │
│ │ Devis clients              │ 0 docs      │ [Tester]       │ │
│ │ Statut : En développement  │ disponible: Q2 │ [Logs]      │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 8.3 extraction_planning    │ ⏳ PRÉVU    │ [Configurer]   │ │
│ │ Planning chantiers         │ 0 docs      │ [Tester]       │ │
│ │ Statut : Planifié Q3 2025  │ priorité: 3 │ [Logs]         │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ➕ [Ajouter nouveau workflow]                                   │
│                                                                 │
│ 🔧 Configuration globale :                                      │
│ URL n8n : [https://your-n8n.domain.com_____________]           │
│ Timeout : [30] secondes                                         │
│ Retry max : [3] tentatives                                      │
│                                                                 │
│ [💾 Sauvegarder] [🧪 Tester connexion] [📊 Statistiques]      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚨 Gestion des Erreurs

### **Types d'Erreurs Courantes**

#### **1. Erreur d'Extraction (PDF illisible)**
```
┌─────────────────────────────────────────────────────────────────┐
│ ❌ Erreur d'Extraction                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 📄 Fichier : facture_scan_flou.pdf                             │
│ ⚠️ Problème : PDF de mauvaise qualité, OCR difficile          │
│                                                                 │
│ 🔍 Détails techniques :                                         │
│ • Confiance OCR : 23% (seuil minimum : 70%)                    │
│ • Pages analysées : 2/3                                        │
│ • Erreur n8n : "Text extraction failed"                        │
│                                                                 │
│ 💡 Solutions recommandées :                                     │
│ ✅ Rescanner le document en meilleure qualité                  │
│ ✅ Utiliser un PDF original (pas de scan si possible)          │
│ ✅ Vérifier que le document n'est pas protégé                  │
│                                                                 │
│ 🔄 Actions possibles :                                          │
│ [📤 Réuploader nouveau fichier] [✏️ Saisie manuelle]          │
│ [🔄 Réessayer extraction] [❌ Abandonner]                      │
└─────────────────────────────────────────────────────────────────┘
```

#### **2. Erreur de Ventilation IA**
```
┌─────────────────────────────────────────────────────────────────┐
│ ⚠️ Ventilation IA Incomplète                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 📄 Fichier : facture_references_ambigues.pdf                   │
│ 🤖 Problème : IA n'arrive pas à identifier les chantiers       │
│                                                                 │
│ 📊 Résultat actuel :                                            │
│ • Total facture : 3 456,78 €                                   │
│ • Ventilé automatiquement : 890,23 € (26%)                     │
│ • Nécessite intervention : 2 566,55 € (74%)                    │
│                                                                 │
│ 🔍 Bons problématiques :                                        │
│ • Bon 12345 : "TRAVAUX DIVERS" → Pas de chantier trouvé        │
│ • Bon 12346 : "CLIENT123" → Référence inconnue                 │
│ • Bon 12347 : "REF/2025/45" → Format non reconnu               │
│                                                                 │
│ 💡 L'IA va apprendre de vos corrections !                      │
│                                                                 │
│ [✏️ Ventiler manuellement] [🔄 Réanalyser] [💾 Reporter]      │
└─────────────────────────────────────────────────────────────────┘
```

#### **3. Erreur de Cohérence**
```
┌─────────────────────────────────────────────────────────────────┐
│ ⚠️ Problème de Cohérence Détecté                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 📄 Fichier : facture_somme_incorrecte.pdf                      │
│ 🧮 Problème : Total bons ≠ Total facture                       │
│                                                                 │
│ 📊 Détail des montants :                                        │
│ • Total facture HT : 2 500,00 €                                │
│ • Somme des bons : 2 847,50 €                                  │
│ • Écart détecté : +347,50 €                                    │
│                                                                 │
│ 🔍 Causes possibles :                                           │
│ • Frais de port non détectés                                   │
│ • Remise ou escompte                                            │
│ • Erreur d'extraction OCR                                      │
│ • Bon de livraison d'une autre facture                         │
│                                                                 │
│ 💡 Actions recommandées :                                       │
│ ✅ Vérifier manuellement le PDF original                       │
│ ✅ Corriger les montants si nécessaire                          │
│ ✅ Exclure les bons qui ne correspondent pas                    │
│                                                                 │
│ [🔍 Analyser PDF] [✏️ Corriger montants] [➡️ Continuer malgré tout] │
└─────────────────────────────────────────────────────────────────┘
```

### **Centre d'Aide Intégré**

```
┌─────────────────────────────────────────────────────────────────┐
│ ❓ Centre d'Aide - Extraction Intelligente                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 🔍 Recherche rapide :                                           │
│ [Comment corriger une erreur d'extraction ?_________] 🔍        │
│                                                                 │
│ 📚 Questions fréquentes :                                       │
│                                                                 │
│ ▶️ Mon PDF n'est pas détecté, que faire ?                      │
│ ▶️ L'IA propose le mauvais chantier, comment corriger ?        │
│ ▶️ Comment créer un nouveau chantier depuis l'extraction ?     │
│ ▶️ Que faire si les montants ne correspondent pas ?            │
│ ▶️ Comment améliorer la précision de l'IA ?                    │
│                                                                 │
│ 🎥 Tutoriels vidéo :                                            │
│ • Extraction de base (2min) [▶️ Voir]                          │
│ • Ventilation avancée (5min) [▶️ Voir]                         │
│ • Gestion des erreurs (3min) [▶️ Voir]                         │
│ • Configuration IA (4min) [▶️ Voir]                            │
│                                                                 │
│ 📞 Support :                                                    │
│ • Chat en ligne : [💬 Démarrer]                                │
│ • Ticket support : [🎫 Créer]                                  │
│ • Formation : [📚 Planifier]                                   │
│                                                                 │
│ 📊 Votre utilisation :                                          │
│ • Documents traités : 67                                       │
│ • Taux de réussite : 91%                                       │
│ • Niveau : Utilisateur confirmé ✅                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Conseils et Bonnes Pratiques

### **Optimiser la Précision IA**

1. **Qualité des Documents**
   - ✅ Utiliser des PDF originaux plutôt que des scans
   - ✅ Scanner en 300 DPI minimum si nécessaire
   - ✅ Éviter les documents protégés par mot de passe

2. **Nommage des Fichiers**
   - ✅ `facture_mbr_ca000190.pdf` (fournisseur + numéro)
   - ✅ `lcr_delaire_janvier_2025.pdf` (type + période)
   - ❌ `document1.pdf` (trop générique)

3. **Gestion des Chantiers**
   - ✅ Mettre à jour les mots-clés régulièrement
   - ✅ Utiliser les mêmes références que les fournisseurs
   - ✅ Corriger l'IA quand elle se trompe (apprentissage)

### **Workflow Recommandé**

1. **Traitement par Lot** (plus efficace)
   - Grouper les factures par fournisseur
   - Traiter 5-10 documents à la fois
   - Valider en une seule session

2. **Validation Systématique**
   - Toujours vérifier les gros montants (>1000€)
   - Contrôler les nouveaux fournisseurs
   - Valider les créations de chantiers

3. **Suivi Régulier**
   - Consulter les stats IA chaque semaine
   - Former l'équipe aux corrections
   - Partager les bonnes pratiques

### **Cas d'Usage Avancés**

1. **Factures Multi-Chantiers**
   - LCR avec 10+ bons de livraison
   - Ventilation automatique intelligente
   - Validation rapide par exception

2. **Nouveaux Clients**
   - Détection automatique de nouveaux noms
   - Création guidée de chantiers
   - Apprentissage des nouvelles références

3. **Gestion des Retours**
   - Avoir de livraison négatifs
   - Corrections automatiques de factures
   - Traçabilité complète

---

## 📈 Performance et ROI

### **Gains Mesurés**

| Activité | Avant | Après | Gain |
|----------|-------|-------|------|
| Lecture PDF | 10 min | 30 sec | -95% |
| Saisie facture | 5 min | 1 min | -80% |
| Ventilation bons | 15 min | 2 min | -87% |
| **Total par facture** | **30 min** | **3,5 min** | **-88%** |

### **Métriques de Qualité**

- **Précision extraction** : 95% (vs 98% saisie manuelle)
- **Précision ventilation IA** : 87% (s'améliore avec l'usage)
- **Temps de formation** : 2 heures pour être autonome
- **Satisfaction utilisateur** : 9,2/10

### **ROI Entreprise**

Pour 100 factures/mois :
- **Temps gagné** : 44 heures/mois
- **Coût économisé** : 1 760€/mois (40€/h)
- **ROI annuel** : 21 120€

---

**✅ Guide utilisateur complet - Extraction intelligente maîtrisée !** 