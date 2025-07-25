# 🔄 Workflows & Processus Métier ATARYS V2

> **Documentation des workflows et processus métier**  
> **VERSION 2** : Workflows opérationnels avec fonctionnalités avancées  
> Dernière mise à jour : 05/07/2025

---

## 📋 **Vue d'Ensemble**

Cette documentation décrit les workflows principaux de l'application ATARYS V2, les processus métier et les interactions entre les différents modules. Architecture opérationnelle avec fonctionnalités avancées.

---

## 🚀 **SYSTÈME DE DÉCLENCHEURS AUTOMATIQUES**

### **📋 Vue d'Ensemble des Déclencheurs**

Le système ATARYS V2 intègre un mécanisme de déclencheurs automatiques qui génère des tâches en fonction d'événements métier. Cette approche permet une automatisation complète sans modification de code.

#### **Principe de Fonctionnement**
1. **Configuration** : L'administrateur définit les tâches templates dans la table `famille_tach`
2. **Détection** : Les événements métier déclenchent automatiquement les tâches
3. **Génération** : Le service `TacheAutomatiqueService` crée les tâches réelles
4. **Suivi** : Les tâches sont assignées et suivies dans l'interface

### **🎯 Déclencheurs Configurés**

#### **Déclencheurs Chantier (Module 3)**
- `chantier_creation` : Création d'un nouveau chantier
- `chantier_signature` : Signature d'un chantier
- `chantier_preparation` : Phase de préparation du chantier
- `chantier_en_cours` : Chantier en cours d'exécution
- `chantier_termine` : Fin d'un chantier

#### **Déclencheurs RH (Module 9)**
- `insertion_salarié` : Création d'un nouveau salarié

#### **Déclencheurs Planning (Module 1)**
- `modification_planning` : Modification du planning (fonction dispo sur planning et liste_chantier et chantier)

### **🏗️ Workflow d'Intégration des Déclencheurs**

#### **Étape 1 : Configuration par l'Administrateur**
```python
# Exemple de configuration dans famille_tach
{
    "famille_tache": "chantier",
    "type_tache": "Chantier création",
    "declencheur": "chantier_creation",
    "auto_generee": True,
    "statut": "A faire",
    "date_echeance": "x jours après creation"
}
```

#### **Étape 2 : Intégration dans les Endpoints**
```python
# Exemple dans module_3.py - Création chantier
@chantier_bp.route('/api/chantiers/', methods=['POST'])
def create_chantier():
    # 1. Créer le chantier
    chantier = Chantier(**data)
    db.session.add(chantier)
    db.session.commit()
    
    # 2. DÉCLENCHEUR AUTOMATIQUE : Appeler le service
    service = TacheAutomatiqueService()
    contexte = {'chantier_id': chantier.id}
    taches_creees = service.declencher_taches('chantier_creation', contexte)
    
    return jsonify({
        'success': True,
        'data': chantier_schema.dump(chantier),
        'taches_creees': len(taches_creees)
    })
```

#### **Étape 3 : Service de Génération Automatique**
```python
class TacheAutomatiqueService:
    def declencher_taches(self, evenement: str, contexte: dict):
        """Déclencher les tâches automatiques selon l'événement"""
        
        # 1. Chercher toutes les tâches avec ce déclencheur
        taches_templates = FamilleTach.query.filter_by(
            declencheur=evenement,
            auto_generee=True
        ).all()
        
        # 2. Pour chaque template, créer une tâche selon le type
        taches_creees = []
        for template in taches_templates:
            if template.famille_tache == 'chantier' and contexte.get('chantier_id'):
                # Créer une tâche chantier
                nouvelle_tache = TachesChantiers(
                    titre=template.titre,
                    famille_tach=template.famille_tache,
                    type_tache=template.type_tache,
                    chantier_id=contexte.get('chantier_id'),
                    statut=template.statut,
                    date_creation=self._calculer_date_creation(template, contexte),
                    date_echeance=self._calculer_echeance(template, contexte),
                    auto_generee=True,
                    declencheur=evenement
                )
            else:
                # Créer une tâche administrative
                nouvelle_tache = TachesAdministratives(
                    titre=template.titre,
                    famille_tach=template.famille_tache,
                    type_tache=template.type_tache,
                    chantier_id=contexte.get('chantier_id'),  # Nullable pour admin
                    statut=template.statut,
                    date_creation=self._calculer_date_creation(template, contexte),
                    date_echeance=self._calculer_echeance(template, contexte),
                    auto_generee=True,
                    declencheur=evenement,
                    type_administratif=template.type_administratif or 'GENERAL'
                )
            
            db.session.add(nouvelle_tache)
            taches_creees.append(nouvelle_tache)
        
        db.session.commit()
        return taches_creees
```

### **📋 Familles de Tâches**

#### **Temporelle**
- **Définition** : Tâches avec périodicité (tous les mois, toutes les semaines, tous les jours)
- **Exemples** : Période déclarative fiscale, audit annuel, campagne comptable
- **Logique date** : `date récurrente si temporelle`

#### **Ponctuelle**
- **Définition** : Tâches à exécution unique, non répétitive
- **Exemples** : Création contrat, déclaration exceptionnelle, signature acte
- **Logique date** : `date de création si ponctuelle`

#### **Chantier**
- **Définition** : Tâches propres à un chantier spécifique
- **Exemples** : Chantier création, Chantier signature, Chantier en cours
- **Logique date** : `date du declencheur si chantier`

### **🎯 Avantages du Système de Déclencheurs**

#### **Flexibilité Maximale**
- ✅ **Configuration sans code** : L'admin peut tout configurer via l'interface
- ✅ **Ajout de déclencheurs** : Nouveaux événements sans redéploiement
- ✅ **Modification des règles** : Changement des logiques de calcul en temps réel

#### **Maintenance Réduite**
- ✅ **Pas de redéploiement** : Modifications via interface admin
- ✅ **Configuration centralisée** : Tous les déclencheurs dans une table
- ✅ **Auditabilité** : Historique des configurations

#### **Évolutivité**
- ✅ **Nouveaux événements** : Ajout facile de déclencheurs
- ✅ **Règles métier** : Configuration des logiques de calcul
- ✅ **Notifications** : Possibilité d'ajouter des alertes

---

## 🎯 **STANDARDS INTERFACE UTILISATEUR ATARYS**

### **📋 Comportement Double-Clic OBLIGATOIRE**

#### **RÈGLE ABSOLUE : Double-clic sur ligne de tableau**
- **TOUJOURS** : Le double-clic sur une ligne de tableau doit ouvrir le formulaire de modification
- **JAMAIS** : Supprimer ou modifier ce comportement sans accord explicite
- **STANDARD** : Remplir automatiquement le formulaire avec les données de la ligne sélectionnée

#### **Implémentation Standard ATARYS**
```jsx
// ✅ COMPORTEMENT OBLIGATOIRE - À NE JAMAIS SUPPRIMER
<tr
  key={item.id}
  onClick={() => handleRowClick(item)}
  onDoubleClick={() => {
    setEditingItem(item);
    setFormData({
      // Remplir TOUS les champs avec les données de l'item
      nom: item.nom || '',
      prenom: item.prenom || '',
      // ... tous les autres champs
    });
    setShowModal(true);
  }}
  className={`hover:bg-gray-50 cursor-pointer transition-colors duration-150 ${
    selectedItem?.id === item.id ? 'bg-blue-50 border-l-4 border-blue-500' : ''
  }`}
>
```

### **📅 Planning Salariés - Liaison Dynamique**

#### **RÈGLE ABSOLUE : Données dynamiques pour le planning**
- **TOUJOURS** : Utiliser les données de la base de données pour le planning
- **JAMAIS** : Hardcoder les données des salariés dans le planning
- **STANDARD** : API `/api/salaries/?actif=true` pour récupérer les salariés actifs

#### **Documentation Complète**
- 📋 **Voir** : `docs/03-regles-standards/PLANNING_SALARIES_DYNAMIC.md`
- ✅ **Implémentation** : `frontend/src/pages/PlanningSalaries.jsx`
- 🔧 **API** : `backend/app/routes/module_9.py` - route `list_salaries()`

#### **Fonctionnalités OBLIGATOIRES**
1. **Chargement dynamique** : Appel API au montage du composant
2. **Gestion des états** : Loading, Error, Success
3. **Positionnement intelligent** : Utilisation du champ `colonne_planning`
4. **Filtrage des actifs** : Seuls les salariés actifs sont affichés
5. **Gestion des dates** : Respect des dates d'entrée/sortie

#### **Fonctionnalités Associées OBLIGATOIRES**
1. **Sélection visuelle** : Ligne sélectionnée avec bordure bleue
2. **Hover effect** : Effet de survol sans masquer la sélection
3. **Formulaire pré-rempli** : Tous les champs remplis automatiquement
4. **Modal d'édition** : Ouverture automatique du modal de modification

#### **Modules Concernés**
- ✅ **Module 9.1** : Salariés (OPÉRATIONNEL)
- ✅ **Module 3.1** : Chantiers (OPÉRATIONNEL)
- ✅ **Module 12.1** : Base de données (OPÉRATIONNEL)
- 🔄 **Tous les autres modules** : À implémenter selon ce standard

#### **Tests de Validation OBLIGATOIRES**
1. **Double-clic fonctionne** : Modal s'ouvre avec données pré-remplies
2. **Sélection visuelle** : Ligne reste sélectionnée après hover
3. **Formulaire complet** : Tous les champs sont remplis
4. **Sauvegarde** : Les modifications sont sauvegardées correctement

---

## 🏗️ **Workflow Gestion Articles ATARYS (Module 5.1)**

### **1. Gestion des Articles**

#### **Étapes du Processus**
1. **Accès à l'interface** : Module 12.1 Base de Données
2. **Sélection de la table** : `articles_atarys`
3. **Visualisation** : 176 lignes avec compteur dynamique
4. **Actions disponibles** :
   - Ajouter une ligne (formulaire dynamique)
   - Coller depuis Excel (import intelligent)
   - Créer une nouvelle table
   - Sauvegarder les modifications

#### **Règles de Validation**
- `reference` : obligatoire, unique, max 100 caractères
- `libelle` : obligatoire, texte libre
- `prix_achat` : optionnel, `db.Numeric(10, 2)`
- `coefficient` : optionnel, `db.Numeric(10, 2)`
- `prix_unitaire` : obligatoire, `db.Numeric(10, 2)`
- `unite` : obligatoire, max 20 caractères
- `tva_pct` : obligatoire, `db.Numeric(10, 2)`, défaut 20
- `famille` : optionnel, max 30 caractères
- `actif` : optionnel, booléen, défaut true

### **2. Import Excel Intelligent**

#### **Workflow de Collage**
1. **Copier depuis Excel** : Sélection des données
2. **Coller dans l'interface** : Ctrl+V dans le tableau
3. **Traitement automatique** :
   - Nettoyage des guillemets et espaces
   - Conversion des types (string → number, boolean)
   - Filtrage des lignes vides
   - Validation des données obligatoires
4. **Ajout à la liste** : Données prêtes pour sauvegarde

#### **Logique UPSERT**
```python
# Vérification de l'existence par référence
existing_article = articlesatarys.query.filter_by(reference=reference).first()

if existing_article:
    # Mise à jour de l'article existant
    for key, value in data.items():
        setattr(existing_article, key, value)
    existing_article.updated_at = datetime.utcnow()
else:
    # Création d'un nouvel article
    article = articlesatarys(**data)
    db.session.add(article)

db.session.commit()
```

---

## 🏗️ **Workflow Création Dynamique de Tables (Module 12.1)**

### **1. Interface Multi-Étapes**

#### **Étape 1 : Sélection du Module**
1. **Choix du module ATARYS** (1-13)
2. **Suggestion automatique** du module 12 (Paramètres)
3. **Validation** et passage à l'étape suivante

#### **Étape 2 : Définition de la Classe**
1. **Saisie du nom de classe** (PascalCase)
2. **Génération automatique** du nom de table (snake_case)
3. **Validation** de la syntaxe

#### **Étape 3 : Définition des Colonnes**
1. **Ajout de colonnes** une par une
2. **Suggestions intelligentes** selon le nom :
   ```python
   # Exemples de suggestions
   "actif" → Boolean, default=True
   "prix_ht" → Numeric(10, 2), default=0.00
   "date_creation" → Date, default=datetime.date.today
   "description" → Text, default=""
   ```
3. **Configuration des propriétés** :
   - Type de données
   - Nullable/obligatoire
   - Unique
   - Valeur par défaut
   - Longueur maximale

### **2. Génération Automatique**

#### **Génération du Code SQLAlchemy**
```python
# Code généré automatiquement
from .base import BaseModel
from app import db
import datetime

class ExampleModel(BaseModel):
    __tablename__ = 'example_table'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    prix_ht = db.Column(db.Numeric(10, 2), default=0.00)
    actif = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.Date, default=datetime.date.today)
    
    def __repr__(self):
        return f'<ExampleModel {self.id}>'
```

#### **Création de la Table SQLite**
```sql
CREATE TABLE example_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prix_ht REAL DEFAULT 0.00,
    actif INTEGER DEFAULT 1,
    date_creation TEXT DEFAULT CURRENT_DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### **3. Intégration Immédiate**
1. **Création du fichier modèle** dans `backend/app/models/`
2. **Création de la table** dans la base SQLite
3. **Intégration dans l'API REST** automatique
4. **Disponibilité immédiate** dans l'interface

---

## 🏗️ **Workflow Gestion Chantiers (Module 3.1 - EN COURS)**

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

4. **DÉCLENCHEUR AUTOMATIQUE** : Génération des tâches
   - Appel du service `TacheAutomatiqueService`
   - Création des tâches liées au chantier
   - Notification des tâches créées

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

## 👥 **Workflow Gestion Salariés (Module 9.1 - EN COURS)**

### **Affectation Planning**
1. **Sélection de la date** dans le planning
2. **Choix du salarié** (colonne correspondante)
3. **Saisie de la description** du chantier/tâche
4. **Validation** et enregistrement

### **Gestion des Compétences**
- **Association** salariés ↔ familles d'ouvrages
- **Calcul automatique** des coûts selon qualification
- **Planning optimisé** selon les compétences

### **DÉCLENCHEUR AUTOMATIQUE : Création Salarié**
```python
# Exemple dans module_9.py - Création salarié
@salaries_bp.route('/api/salaries/', methods=['POST'])
def create_salary():
    # 1. Créer le salarié
    salary = Salaries(**data)
    db.session.add(salary)
    db.session.commit()
    
    # 2. DÉCLENCHEUR AUTOMATIQUE : Appeler le service
    service = TacheAutomatiqueService()
    contexte = {'salary_id': salary.id}
    taches_creees = service.declencher_taches('insertion_salarié', contexte)
    
    return jsonify({
        'success': True,
        'data': salary_schema.dump(salary),
        'taches_creees': len(taches_creees)
    })
```

---

## 🏗️ **Workflow Calcul Ardoises (Module 10.1 - EN COURS)**

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

## 🔄 **Intégrations & Synchronisations V2**

### **Frontend ↔ Backend**
- **API REST** : Format standardisé `{success, data, message}`
- **Validation** : Marshmallow côté backend, validation côté frontend
- **CORS** : Communication cross-origin configurée
- **Gestion d'erreurs** : Messages explicites pour l'utilisateur

### **Base de Données ↔ Admin**
- **API REST** : Interface d'administration automatique
- **Pattern BaseModel** : Méthodes communes (save, delete, to_dict)
- **Types standards** : `db.Numeric(10, 2)` pour montants
- **Timestamps** : created_at, updated_at automatiques

### **Excel ↔ SQLite**
- **Import intelligent** : Collage direct depuis Excel
- **Nettoyage automatique** : Guillemets, espaces, types
- **Validation** : Filtrage des lignes vides
- **Logique UPSERT** : Création/mise à jour automatique

### **Déclencheurs ↔ Tâches**
- **Configuration** : Interface admin pour définir les déclencheurs
- **Détection automatique** : Intégration dans les endpoints
- **Génération** : Service automatique de création des tâches
- **Suivi** : Interface de gestion des tâches

---

## 📈 **Indicateurs & Reporting V2**

### **Métriques Opérationnelles**
- **176 lignes** dans `articles_atarys`
- **Compteur dynamique** : Total + lignes avec données
- **Response time** : < 100ms pour les requêtes simples
- **Validation** : Marshmallow pour intégrité

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

### **Métriques Déclencheurs**
- **Tâches générées** par déclencheur
- **Taux de conversion** des événements en tâches
- **Temps de traitement** des déclencheurs
- **Erreurs de génération** et corrections

---

## ⚠️ **Règles Métier Importantes V2**

### **Cohérence des Données**
1. **Référence unique** : Validation obligatoire
2. **Types de données** : Standards ATARYS respectés
3. **États workflow** : Définis et respectés
4. **Validation** systématique des saisies

### **Sécurité & Intégrité**
1. **Validation** des fichiers Excel
2. **Rollback** en cas d'erreur SQLAlchemy
3. **Logging** des opérations critiques
4. **Sauvegarde** automatique des données

### **Performance**
1. **Pagination** : 50 par défaut, `all` pour tout
2. **Index** sur les colonnes clés
3. **Cache** des calculs fréquents
4. **Optimisation** des requêtes

### **Fonctionnalités Avancées**
1. **Création dynamique** de tables
2. **Import Excel** intelligent
3. **Logique UPSERT** automatique
4. **Interface responsive** mobile/desktop
5. **Déclencheurs automatiques** configurables

---

## 🚀 **Workflows Futurs**

### **Module 3.1 - Liste Chantiers**
- **CRUD complet** : Création, lecture, modification, suppression
- **États workflow** : Projet → En cours → Terminé
- **Recherche** : Filtrage par état, client, date
- **Export** : Liste des chantiers en Excel/PDF
- **Déclencheurs** : Tâches automatiques selon les états

### **Module 9.1 - Liste Salariés**
- **Gestion RH** : Fiches salariés complètes
- **Planning** : Affectation des tâches
- **Compétences** : Association métiers/qualifications
- **Reporting** : Heures travaillées, disponibilités
- **Déclencheurs** : Tâches automatiques lors de la création

### **Module 10.1 - Calcul Ardoises**
- **Calculateur** : Interface de saisie des paramètres
- **Zones climatiques** : Base de données des villes
- **Modèles ardoises** : Catalogue des produits
- **Résultats** : Quantités, prix, recommandations

### **Module 2.1 - Liste des Tâches**
- **Gestion** : Interface de création et modification
- **Déclencheurs** : Configuration des tâches automatiques
- **Suivi** : Statuts et échéances
- **Notifications** : Alertes et rappels

---

**✅ Workflows ATARYS V2 - Processus métier optimisés avec fonctionnalités avancées et déclencheurs automatiques !**
