# 📊 Guide - Gestion des Devis Multiples par Chantier

## 🎯 Vue d'ensemble

Cette fonctionnalité permet de gérer automatiquement les cas où un client a plusieurs devis pour le même chantier. Le système détecte intelligemment les doublons et additionne les montants au lieu de créer plusieurs chantiers.

---

## 🔍 Détection Automatique des Chantiers Existants

### Critères de Détection

Le système utilise **3 critères fiables** pour détecter un chantier existant :

1. **Nom du client** (comparaison insensible à la casse)
2. **Prénom du client** (optionnel, toléré si manquant)
3. **Code postal** (comparaison exacte)

### Exemples de Détection

✅ **CAS DÉTECTÉS (même chantier)** :
```
Devis 1: DUPONT Jean - 35000 RENNES
Devis 2: DUPONT Jean - 35000 RENNES
→ MÊME CHANTIER détecté
```

```
Devis 1: MARTIN Pierre - 44000 NANTES  
Devis 2: MARTIN - 44000 NANTES (prénom manquant)
→ MÊME CHANTIER détecté (prénom toléré)
```

❌ **CAS NON DÉTECTÉS (chantiers différents)** :
```
Devis 1: DUPONT Jean - 35000 RENNES
Devis 2: DURAND Jean - 35000 RENNES
→ Noms différents = chantiers différents
```

```
Devis 1: MARTIN Pierre - 35000 RENNES
Devis 2: MARTIN Pierre - 44000 NANTES  
→ Codes postaux différents = chantiers différents
```

---

## 🚀 Workflow d'Utilisation

### 1. Premier Devis (Création)

1. Cliquer sur **"📄 Créer selon devis"**
2. Sélectionner le fichier de devis
3. Le système analyse et propose la création d'un nouveau chantier
4. Valider la création

**Résultat** : Chantier créé avec le premier devis

### 2. Devis Supplémentaires (Addition)

1. Cliquer à nouveau sur **"📄 Créer selon devis"**
2. Sélectionner le nouveau fichier de devis
3. **Le système détecte automatiquement le chantier existant**
4. Affiche un message de confirmation avec les totaux cumulés

**Résultat** : Devis ajouté au chantier existant, montants additionnés

---

## 📊 Calculs Automatiques

### Montants Cumulés

Le système additionne automatiquement :
- **Montant HT** de tous les devis
- **Montant TTC** de tous les devis  
- **Déboursé matériaux** de tous les devis
- **Heures totales** de tous les devis

### Familles d'Ouvrages Combinées

Les familles d'ouvrages sont **combinées intelligemment** :
```
Devis 1: COUVERTURE (12000€) + ZINGUERIE (3000€)
Devis 2: ISOLATION (5000€) + MENUISERIE (3500€)
→ Résultat: 4 familles combinées = 23500€ total
```

### Exemple Concret

```
📋 CHANTIER: DUPONT Jean - 35000 RENNES

Devis 1 (DEV-2025-001):
- Montant HT: 15 000€
- Heures: 120h
- Familles: COUVERTURE, ZINGUERIE

Devis 2 (DEV-2025-002):  
- Montant HT: 8 500€
- Heures: 65h
- Familles: ISOLATION, MENUISERIE

🎯 TOTAUX CUMULÉS:
- Montant HT: 23 500€
- Heures: 185h
- Familles: COUVERTURE, ZINGUERIE, ISOLATION, MENUISERIE
- Nombre de devis: 2
```

---

## 💻 Interface Utilisateur

### Messages d'Information

#### Chantier Existant Détecté
```
🎯 CHANTIER EXISTANT DÉTECTÉ !

📋 Chantier: DUPONT Jean
📍 Localisation: 35000 RENNES
📊 Devis total: 2

💰 Montant HT cumulé: 23 500 €
⏱️ Heures cumulées: 185h

✅ Devis ajouté au chantier existant. Total: 2 devis

Le chantier a été automatiquement mis à jour avec les totaux cumulés.
```

#### Nouveau Chantier
```
🆕 NOUVEAU CHANTIER DÉTECTÉ

📄 Module 3.1 - Extraction réussie
📋 Fichier: devis_client.xlsx
👤 Client: MARTIN Pierre
📍 Localisation: 44000 NANTES
💰 Montant HT: 18 000 €
⏱️ Heures: 150h
🏗️ Familles: CHARPENTE, COUVERTURE

Aucun chantier existant trouvé. Données prêtes pour création.
Vérifiez et complétez avant de créer le chantier.
```

---

## 🔧 Fonctionnalités Techniques

### API Endpoints

#### Analyse Intelligente
```http
POST /api/add-devis-to-chantier
Content-Type: multipart/form-data

Réponses possibles:
- action: "🏗️ Module 3: Chantiers & Devis_added" → Devis ajouté à chantier existant
- action: "create_new_chantier" → Nouveau chantier à créer
```

#### Consultation des Devis
```http
GET /api/chantier/{id}/devis

Retourne:
- Liste de tous les devis du chantier
- Totaux cumulés automatiques
- Détail par famille d'ouvrages
```

### Structure Base de Données

#### Table `chantiers`
```sql
-- Champs mis à jour automatiquement
montant_ht_devis: REAL    -- Somme de tous les devis
nombre_heures_total: REAL -- Somme de toutes les heures
date_modification: TEXT   -- Mise à jour automatique
```

#### Table `devis`
```sql
-- Un enregistrement par devis
chantier_id: INTEGER      -- Lien vers le chantier
numero_devis: TEXT        -- Numéro unique du devis
montant_ht: REAL         -- Montant de ce devis
montant_par_famille: TEXT -- JSON des montants par famille
heures_par_famille: TEXT  -- JSON des heures par famille
```

---

## 🎯 Avantages

### Pour l'Utilisateur
- ✅ **Pas de doublons** : Évite la création de chantiers multiples
- ✅ **Totaux automatiques** : Plus besoin de calculer manuellement
- ✅ **Historique complet** : Tous les devis conservés et consultables
- ✅ **Gain de temps** : Détection et traitement automatiques

### Pour la Gestion
- ✅ **Vue d'ensemble** : Un seul chantier = tous les devis
- ✅ **Suivi précis** : Évolution des montants dans le temps
- ✅ **Familles combinées** : Vision globale des travaux
- ✅ **Données cohérentes** : Pas de dispersion des informations

---

## 🔍 Cas d'Usage Typiques

### Cas 1: Devis Échelonnés
```
Janvier: Devis COUVERTURE (15 000€)
Mars: Devis ISOLATION (8 000€)  
Mai: Devis MENUISERIE (12 000€)
→ Un seul chantier = 35 000€ total
```

### Cas 2: Devis Modificatifs
```
V1: Devis initial (20 000€)
V2: Devis avec options (+5 000€)
V3: Devis final ajusté (+2 000€)
→ Un chantier = 27 000€ avec historique
```

### Cas 3: Lots Séparés
```
Lot 1: Gros œuvre (50 000€)
Lot 2: Second œuvre (30 000€)
Lot 3: Finitions (15 000€)
→ Un chantier = 95 000€ multi-lots
```

---

## 🚨 Points d'Attention

### Vérifications Manuelles
- **Contrôler les totaux** après ajout de devis
- **Vérifier la cohérence** des familles d'ouvrages
- **Valider les dates** de début/fin prévisionnelles

### Cas Particuliers
- **Clients homonymes** : Vérifier le code postal
- **Adresses multiples** : Un client peut avoir plusieurs chantiers
- **Devis annulés** : Marquer comme inactif plutôt que supprimer

---

## 📞 Support

En cas de problème :
1. Vérifier que les critères de détection sont corrects
2. Consulter les logs du backend pour les détails
3. Utiliser l'API de consultation des devis pour vérifier les totaux
4. Contacter le support technique si nécessaire

**Cette fonctionnalité révolutionne la gestion des devis multiples en automatisant complètement le processus !** 🚀 