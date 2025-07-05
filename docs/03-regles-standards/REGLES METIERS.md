# ATARYS - Règles Métier et Calculs

## 🧮 **Calcul des Ardoises**

### **Paramètres d'Entrée**
1. **Ville** → Détermine la **Zone climatique** (1, 2, ou 3)
2. **Pente** → En degrés (°) ou pourcentage (%)
3. **Projection** → Longueur rampant en mètres linéaires
   - Zone 1 : 0-5.5m, 5.5-11m, 11-16.5m
   - Zone 2 : 0-5.5m, 5.5-11m, 11-16.5m  
   - Zone 3 : 0-5.5m, 5.5-11m, 11-16.5m

### **Workflow de Calcul**
```
Ville → Zone → Pente + Projection → Recouvrement → Modèles → Résultats
```

### **Formules**
- **Conversion pente** : `tan(pente_degré) = pente_pourcentage / 100`
- **Recouvrement** : Fonction de (pente, zone, projection) via table `calcul_modele_ardoises`

### **Résultats Calculés**
- **Pureau** (mm) : Distance entre ardoises
- **Crochet** (mm) : Fixation ardoise
- **Nb ardoises/m²** : Quantité par mètre carré
- **Nb liteaux/m²** : Support par mètre carré

## 👥 **Gestion des Salariés**

### **Données Salariés**
- **Prénom** : Identification
- **Date d'entrée** : Format YYYY-MM-DD
- **Date de sortie** : Optionnelle (null si actif)
- **Colonne planning** : Position dans tableau planning

### **Règles Planning**
- **Salariés actifs** : `date_sortie IS NULL`
- **Affichage** : Tri par date d'entrée
- **Planning** : Colonnes dynamiques selon salariés

## 🏗️ **Planning Chantiers**

### **Structure Planning**
- **Date** : Date de l'intervention
- **Colonne** : Référence salarié ou chantier
- **Description** : Détail de l'activité

### **Règles d'Affichage**
- **Vue calendaire** : Grille date × salarié
- **Couleurs** : Selon type d'activité
- **Édition** : Modification en ligne

## 🌍 **Zones Climatiques Bretagne**

### **Répartition par Département**
- **Zone 1** : Intérieur des terres
- **Zone 2** : Zones intermédiaires  
- **Zone 3** : Zones côtières exposées

### **Impact sur Calculs**
- **Zone 1** : Recouvrement standard
- **Zone 2** : Recouvrement renforcé
- **Zone 3** : Recouvrement maximum (exposition marine)

## 📏 **Standards Techniques**

### **Unités de Mesure**
- **Pente** : Degrés (°) ou pourcentage (%)
- **Distances** : Millimètres (mm) pour précision
- **Surfaces** : Mètres carrés (m²)
- **Longueurs** : Mètres linéaires (ML)

### **Tolérances**
- **Pente** : ±0.1°
- **Recouvrement** : ±1mm
- **Calculs** : 2 décimales maximum

## 🔄 **Workflow Utilisateur**

### **Calcul Ardoises - Étapes**
1. **Saisie chantier** : Nom + ville
2. **Auto-détection zone** : Via base communes
3. **Saisie pente** : Conversion automatique °/% 
4. **Choix projection** : Selon longueur rampant
5. **Calcul recouvrement** : Automatique
6. **Sélection modèle** : Liste filtrée
7. **Résultats** : Affichage calculs finaux

### **Planning - Étapes**
1. **Vue d'ensemble** : Grille salariés × dates
2. **Sélection cellule** : Clic pour éditer
3. **Saisie activité** : Description intervention
4. **Validation** : Sauvegarde automatique

## ⚠️ **Gestion d'Erreurs**

### **Cas d'Erreur Métier**
- **Ville inconnue** : Message "🌍 Module 11: Géographie non trouvée"
- **Pente invalide** : "📐 Module 10: Outils Ardoises doit être entre 0° et 90°"
- **Recouvrement introuvable** : "Aucun modèle pour ces paramètres"

### **Valeurs par Défaut**
- **Pente** : 45° (100%)
- **Zone** : 2 (intermédiaire)
- **Projection** : 1 (0-5.5m)

---

*Dernière mise à jour : 22/06/2025* 