# 🔄 Workflows & Processus Métier ATARYS

> **Documentation des workflows et processus métier**  
> Dernière mise à jour : 29/06/2025

---

## 📋 **Vue d'Ensemble**

Cette documentation décrit les workflows principaux de l'application ATARYS, les processus métier et les interactions entre les différents modules.

---

## 🏗️ **Workflow Gestion Chantiers**

### **1. Création d'un Chantier**

#### **Étapes du Processus**
1. **Saisie des informations client** (optionnel)
   - Civilité, nom, prénom
   - Coordonnées (email, téléphone)
   - Adresse du chantier

2. **Informations chantier** (obligatoire)
   - Description du chantier
   - **Référence chantier** (obligatoire et unique)
   - État initial (par défaut : "En cours")

3. **Validation et création**
   - Vérification de l'unicité de la référence
   - Création de l'enregistrement en base
   - Attribution d'un ID unique

#### **Règles de Validation**
- `reference_chantier` : obligatoire, unique, format libre
- `etat_id` : obligatoire (par défaut = 1 "En cours")
- Autres champs : optionnels lors de la création

### **2. Modification d'un Chantier**

#### **Workflow Standard**
1. **Sélection du chantier** dans la liste
2. **Clic sur "Modifier"** → Ouverture de la modale
3. **Modification des champs** existants
4. **Option "Insérer un devis"** (nouveau workflow)
5. **Validation** et mise à jour

#### **Workflow Insertion de Devis**
1. **Activation de l'option** "Insérer un devis"
2. **Sélection du fichier Excel** (.xlsx, .xls)
3. **Traitement automatique** :
   - Extraction des données du devis
   - Validation de la référence chantier
   - Calcul des totaux (montant HT, heures)
   - Mise à jour du chantier
4. **Confirmation** et retour à la liste

---

## 📊 **Workflow Extraction de Devis**

### **Processus d'Extraction**

#### **1. Analyse du Fichier Excel**
```python
# Fonction principale : extract_devis_data()
- Lecture du fichier Excel
- Identification des sections (client, devis, ouvrages)
- Extraction des métadonnées (numéro, date, montants)
- Parsing des lignes d'ouvrages
```

#### **2. Validation des Données**
- **Référence chantier** : vérification de cohérence
- **Montants** : validation numérique
- **Dates** : format et cohérence
- **Familles d'ouvrages** : classification automatique

#### **3. Intégration en Base**
```sql
-- Création du devis
INSERT INTO devis (chantier_id, reference_chantier, ...)

-- Mise à jour du chantier (totaux)
UPDATE chantiers SET 
  montant_ht_devis = (SELECT SUM(montant_ht) FROM devis WHERE chantier_id = ?),
  nombre_heures_total = (SELECT SUM(nombre_heures_total) FROM devis WHERE chantier_id = ?)
```

### **Gestion des Erreurs**
- **Fichier non valide** : message d'erreur explicite
- **Référence incohérente** : validation et correction
- **Données manquantes** : valeurs par défaut
- **Erreur d'insertion** : rollback automatique

---

## 👥 **Workflow Gestion Salariés**

### **Affectation Planning**
1. **Sélection de la date** dans le planning
2. **Choix du salarié** (colonne correspondante)
3. **Saisie de la description** du chantier/tâche
4. **Validation** et enregistrement

### **Gestion des Compétences**
- **Association** salariés ↔ familles d'ouvrages
- **Calcul automatique** des coûts selon qualification
- **Planning optimisé** selon les compétences

---

## 🏗️ **Workflow Calcul Ardoises**

### **Séquence de Calcul**
1. **Saisie des paramètres** :
   - Ville (→ zone climatique)
   - Pente de toiture
   - Longueur de rampant
   - Surface à couvrir

2. **Calcul automatique** :
   ```python
   # Détermination du recouvrement
   zone = get_zone_from_ville(ville)
   recouvrement = calculate_recouvrement(zone, pente, longueur_rampant)
   
   # Récupération des modèles disponibles
   modeles = get_modeles_for_recouvrement(recouvrement)
   
   # Calcul pour chaque modèle
   for modele in modeles:
       nb_ardoises = surface * modele.nb_ardoises_m2
       nb_liteaux = surface * modele.nb_liteaux_m2
   ```

3. **Présentation des résultats** :
   - Tableau comparatif des modèles
   - Quantités nécessaires
   - Recommandations techniques

---

## 🔄 **Intégrations & Synchronisations**

### **Chantiers ↔ Devis**
- **Relation 1:N** : un chantier peut avoir plusieurs devis
- **Calcul automatique** des totaux chantier
- **Cohérence** des références chantier

### **Salariés ↔ Planning**
- **Affectation** par colonne de planning
- **Suivi** des heures et disponibilités
- **Optimisation** selon les compétences

### **Devis ↔ Familles d'Ouvrages**
- **Classification automatique** des ouvrages
- **Analyse** des types de travaux
- **Statistiques** par famille

---

## 📈 **Indicateurs & Reporting**

### **Tableaux de Bord**
- **Chantiers actifs** par état
- **Montants** en cours et réalisés
- **Planning** des équipes
- **Statistiques** ardoises par région

### **Exports & Rapports**
- **Liste des chantiers** (filtrable)
- **Détail des devis** par chantier
- **Planning** par période
- **Calculs ardoises** historiques

---

## ⚠️ **Règles Métier Importantes**

### **Cohérence des Données**
1. **Référence chantier** : unique et obligatoire
2. **Totaux chantier** : recalculés automatiquement
3. **États chantier** : workflow défini
4. **Validation** systématique des saisies

### **Sécurité & Intégrité**
1. **Validation** des fichiers Excel
2. **Rollback** en cas d'erreur
3. **Logging** des opérations critiques
4. **Sauvegarde** automatique des données

### **Performance**
1. **Pagination** des listes importantes
2. **Index** sur les colonnes clés
3. **Cache** des calculs fréquents
4. **Optimisation** des requêtes

---

## 🔧 **Points d'Extension**

### **Modules Futurs**
- **Facturation** automatique
- **Suivi** des paiements
- **Gestion** des stocks
- **Interface** mobile

### **Intégrations Externes**
- **OneDrive** pour les documents
- **APIs** météo pour les plannings
- **Outils** de géolocalisation
- **Systèmes** comptables

---

## 📝 **Notes de Développement**

### **Architecture**
- **Backend** : Flask + SQLite
- **Frontend** : React + Vite
- **API** : REST avec format JSON standardisé
- **Documentation** : Swagger/OpenAPI

### **Bonnes Pratiques**
- **Validation** côté client et serveur
- **Gestion d'erreurs** centralisée
- **Logging** structuré
- **Tests** automatisés (à implémenter)

### **Maintenance**
- **Sauvegarde** régulière de la base
- **Monitoring** des performances
- **Mise à jour** de la documentation
- **Formation** des utilisateurs
