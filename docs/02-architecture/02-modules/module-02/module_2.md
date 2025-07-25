# 📋 Module 2 - LISTE DES TÂCHES

> **Gestion des listes de tâches personnalisées par utilisateur**  
> **État : STRUCTURE CRÉÉE** 📋 - Modèles à définir  
> Dernière mise à jour : 19/07/2025

---

## 🎯 Vue d'ensemble

Le module **2 - LISTE DES TÂCHES** gère les listes de tâches personnalisées pour chaque utilisateur du système ATARYS, permettant un suivi individuel et une priorisation des activités.

### **Objectifs Principaux**
- Liste de tâches personnalisées
- Suivi par utilisateur
- Priorisation des tâches
- Organisation du travail individuel

---

## 🚀 **NOUVELLE LOGIQUE D'AUTOMATISATION**

### **Principe de Fonctionnement**

1. **Table `chantiers`** : Table centrale qui rassemble toutes les infos d'un chantier
2. **Détection automatique** : Analyse du contenu des devis/familles d'ouvrages
3. **Création de tâches** : Basée sur des règles métier configurables

### **Exemple Concret**

**Scénario** : Un devis contient "Isolation des fils par Enedis"
**Action automatique** : Création d'une tâche "Contacter Enedis pour isolation"

---

## 🏗️ **ARCHITECTURE TECHNIQUE**

### **1. Table `chantiers` (À CRÉER)**

```python
class Chantier(BaseModel):
    __tablename__ = 'chantiers'
    
    # Informations de base
    reference = db.Column(db.String(50), nullable=False, unique=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Client et contact
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    contact_principal = db.Column(db.String(100))
    
    # Dates importantes
    date_creation = db.Column(db.Date, default=datetime.utcnow)
    date_signature = db.Column(db.Date)
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    
    # Statut et montants
    statut = db.Column(db.String(30), default='BROUILLON')
    # BROUILLON, SIGNE, EN_COURS, TERMINE, ANNULE
    
    montant_ht = db.Column(db.Numeric(10, 2), default=0.00)
    montant_ttc = db.Column(db.Numeric(10, 2), default=0.00)
    
    # Relations
    client = db.relationship('Clients', backref='chantiers')
    
    def __repr__(self):
        return f'<Chantier {self.reference}: {self.titre}>'
```

### **2. Table `famille_tach` (RÈGLES D'AUTOMATISATION)**

```python
class FamilleTach(BaseModel):
    __tablename__ = 'famille_tach'
    
    # Configuration de base
    famille_tache = db.Column(db.String(50), nullable=False)
    type_tache = db.Column(db.String(100), nullable=False)
    titre = db.Column(db.String(200))
    description = db.Column(db.Text)
    
    # Règles de déclenchement
    auto_generee = db.Column(db.Boolean, default=True)
    declencheur = db.Column(db.String(50))  # Événement déclencheur
    
    # **NOUVEAU : Règles de détection**
    mot_cle_famille_ouvrage = db.Column(db.String(100))  # "Enedis", "EDF", etc.
    famille_ouvrage_id = db.Column(db.Integer, db.ForeignKey('famille_ouvrages.id'))
    
    # Configuration des tâches
    statut_defaut = db.Column(db.String(30), default='A faire')
    priorite_defaut = db.Column(db.String(20), default='NORMALE')
    delai_jours = db.Column(db.Integer, default=1)
    
    # Relations
    famille_ouvrage = db.relationship('FamilleOuvrages', backref='taches_automatiques')
    
    def __repr__(self):
        return f'<FamilleTach {self.famille_tache}: {self.type_tache}>'
```

### **3. Tables de Tâches (APPROCHE DEUX TABLES)**

#### **Table `taches_chantiers` (TÂCHES LIÉES AUX CHANTIERS)**

```python
class TachesChantiers(BaseModel):
    __tablename__ = 'taches_chantiers'
    
    # Informations de base
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Assignation
    utilisateur = db.Column(db.String(50), nullable=False)  # YANN, JULIEN
    
    # Gestion
    statut = db.Column(db.String(20), default='A_FAIRE')
    priorite = db.Column(db.String(10), default='NORMALE')
    
    # Dates
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_echeance = db.Column(db.DateTime)
    date_completion = db.Column(db.DateTime)
    
    # **OBLIGATOIRE : Lien vers chantier**
    chantier_id = db.Column(db.Integer, db.ForeignKey('chantiers.id'), nullable=False)
    
    # **Contexte d'automatisation**
    auto_generee = db.Column(db.Boolean, default=False)
    declencheur = db.Column(db.String(50))  # Événement qui a déclenché
    famille_tach_id = db.Column(db.Integer, db.ForeignKey('famille_tach.id'))
    
    # Relations
    famille_tach = db.relationship('FamilleTach', backref='taches_chantiers')
    chantier = db.relationship('Chantier', backref='taches')
    
    def __repr__(self):
        return f'<TachesChantiers {self.titre} - Chantier {self.chantier_id}>'
```

#### **Table `taches_administratives` (TÂCHES GÉNÉRALES)**

```python
class TachesAdministratives(BaseModel):
    __tablename__ = 'taches_administratives'
    
    # Informations de base
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Assignation
    utilisateur = db.Column(db.String(50), nullable=False)  # YANN, JULIEN
    
    # Gestion
    statut = db.Column(db.String(20), default='A_FAIRE')
    priorite = db.Column(db.String(10), default='NORMALE')
    
    # Dates
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_echeance = db.Column(db.DateTime)
    date_completion = db.Column(db.DateTime)
    
    # **OPTIONNEL : Référence chantier (nullable)**
    chantier_id = db.Column(db.Integer, db.ForeignKey('chantiers.id'), nullable=True)
    
    # **Contexte d'automatisation**
    auto_generee = db.Column(db.Boolean, default=False)
    declencheur = db.Column(db.String(50))  # Événement qui a déclenché
    famille_tach_id = db.Column(db.Integer, db.ForeignKey('famille_tach.id'))
    
    # **Type de tâche administrative**
    type_administratif = db.Column(db.String(50))  # FISCAL, RH, COMPTABLE, etc.
    
    # Relations
    famille_tach = db.relationship('FamilleTach', backref='taches_administratives')
    chantier = db.relationship('Chantier', backref='taches_admin')  # Optionnel
    
    def __repr__(self):
        return f'<TachesAdministratives {self.titre} - {self.type_administratif}>'
```

---

## 🔍 **LOGIQUE DE DÉTECTION AUTOMATIQUE**

### **1. Déclencheurs Configurés**

#### **Déclencheurs par Contenu**
- `famille_ouvrage_detectee` : Détection d'une famille d'ouvrage spécifique
- `mot_cle_detecte` : Détection d'un mot-clé dans le devis
- `montant_seuil` : Déclenchement si montant > seuil

#### **Déclencheurs par Événement**
- `chantier_creation` : Création d'un nouveau chantier
- `chantier_signature` : Signature d'un chantier
- `chantier_en_cours` : Chantier en cours d'exécution

### **2. Exemples de Règles Métier**

#### **Règle 1 : Isolation Enedis**
```python
{
    "famille_tache": "chantier",
    "type_tache": "Contact Enedis",
    "mot_cle_famille_ouvrage": "Enedis",
    "titre": "Contacter Enedis pour isolation",
    "statut_defaut": "A faire",
    "priorite_defaut": "HAUTE",
    "delai_jours": 2
}
```

#### **Règle 2 : Électricité EDF**
```python
{
    "famille_tache": "chantier", 
    "type_tache": "Contact EDF",
    "mot_cle_famille_ouvrage": "EDF",
    "titre": "Contacter EDF pour raccordement",
    "statut_defaut": "A faire",
    "priorite_defaut": "HAUTE",
    "delai_jours": 3
}
```

#### **Règle 3 : Montant Important**
```python
{
    "famille_tache": "chantier",
    "type_tache": "Validation direction",
    "montant_seuil": 50000.00,
    "titre": "Validation direction pour chantier > 50k€",
    "statut_defaut": "A faire",
    "priorite_defaut": "HAUTE",
    "delai_jours": 1
}
```

### **3. Service d'Automatisation**

```python
class TacheAutomatiqueService:
    """Service pour la génération automatique de tâches"""
    
    def analyser_chantier(self, chantier_id: int) -> List[TacheReelle]:
        """Analyser un chantier et créer les tâches automatiques"""
        
        # 1. Récupérer le chantier et ses familles d'ouvrages
        chantier = Chantier.query.get(chantier_id)
        familles_ouvrages = self._get_familles_ouvrages_chantier(chantier_id)
        
        # 2. Chercher les règles applicables
        regles = self._chercher_regles_applicables(familles_ouvrages, chantier)
        
        # 3. Créer les tâches automatiques
        taches_creees = []
        for regle in regles:
            # Déterminer le type de tâche selon la règle
            if regle.famille_tache == 'chantier':
                # Créer une tâche chantier
                nouvelle_tache = self._creer_tache_chantier_automatique(regle, chantier)
            else:
                # Créer une tâche administrative
                nouvelle_tache = self._creer_tache_administrative_automatique(regle, chantier)
            
            if nouvelle_tache:
                taches_creees.append(nouvelle_tache)
        
        return taches_creees
    
    def _chercher_regles_applicables(self, familles_ouvrages: List, chantier: Chantier) -> List[FamilleTach]:
        """Chercher les règles applicables selon le contenu"""
        
        regles = []
        
        # Règles par mot-clé dans familles d'ouvrages
        for famille in familles_ouvrages:
            regles_mot_cle = FamilleTach.query.filter(
                FamilleTach.mot_cle_famille_ouvrage.isnot(None),
                FamilleTach.auto_generee == True
            ).all()
            
            for regle in regles_mot_cle:
                if regle.mot_cle_famille_ouvrage.lower() in famille.libelle.lower():
                    regles.append(regle)
        
        # Règles par montant
        if chantier.montant_ht:
            regles_montant = FamilleTach.query.filter(
                FamilleTach.montant_seuil.isnot(None),
                FamilleTach.auto_generee == True,
                FamilleTach.montant_seuil <= chantier.montant_ht
            ).all()
            regles.extend(regles_montant)
        
        return regles
```

---

## 🛣️ **API ENDPOINTS**

### **Gestion des Tâches Automatiques**
```http
GET    /api/module-2/famille-tach              # Liste des règles d'automatisation
POST   /api/module-2/famille-tach              # Créer une nouvelle règle
PUT    /api/module-2/famille-tach/:id          # Modifier une règle
DELETE /api/module-2/famille-tach/:id          # Supprimer une règle

POST   /api/module-2/analyser-chantier/:id     # Analyser un chantier et créer les tâches
GET    /api/module-2/taches-auto/:chantier_id  # Tâches auto d'un chantier
```

### **Gestion des Tâches Chantiers**
```http
GET    /api/module-2/taches-chantiers          # Liste des tâches chantiers avec filtres
POST   /api/module-2/taches-chantiers          # Création nouvelle tâche chantier
GET    /api/module-2/taches-chantiers/:id      # Détail d'une tâche chantier
PUT    /api/module-2/taches-chantiers/:id      # Modification tâche chantier
DELETE /api/module-2/taches-chantiers/:id      # Suppression tâche chantier

GET    /api/module-2/taches-chantiers/chantier/:chantier_id  # Tâches d'un chantier
GET    /api/module-2/taches-chantiers/yann     # Tâches chantiers de Yann
GET    /api/module-2/taches-chantiers/julien   # Tâches chantiers de Julien
```

### **Gestion des Tâches Administratives**
```http
GET    /api/module-2/taches-admin              # Liste des tâches administratives
POST   /api/module-2/taches-admin              # Création nouvelle tâche administrative
GET    /api/module-2/taches-admin/:id          # Détail d'une tâche administrative
PUT    /api/module-2/taches-admin/:id          # Modification tâche administrative
DELETE /api/module-2/taches-admin/:id          # Suppression tâche administrative

GET    /api/module-2/taches-admin/yann         # Tâches administratives de Yann
GET    /api/module-2/taches-admin/julien       # Tâches administratives de Julien
GET    /api/module-2/taches-admin/type/:type   # Tâches par type (FISCAL, RH, etc.)
```

### **Vue Globale des Tâches**
```http
GET    /api/module-2/taches-globales           # Toutes les tâches (chantiers + admin)
GET    /api/module-2/taches-globales/yann      # Toutes les tâches de Yann
GET    /api/module-2/taches-globales/julien    # Toutes les tâches de Julien
```

---

## 🎯 **WORKFLOW D'IMPLÉMENTATION**

### **Phase 1 : Structure de Base**
1. ✅ **Modèles SQLAlchemy** : `FamilleTach`, `TachesChantiers`, `TachesAdministratives`
2. ✅ **API REST** : Endpoints CRUD pour les deux types de tâches
3. ✅ **Service d'automatisation** : `TacheAutomatiqueService` avec logique deux tables

### **Phase 2 : Intégration Chantiers**
1. 🔄 **Table `chantiers`** : Création de la table centrale
2. 🔄 **Service d'analyse** : Intégration avec les familles d'ouvrages
3. 🔄 **Déclencheurs automatiques** : Dans les endpoints chantiers

### **Phase 3 : Interface Utilisateur**
1. 🔄 **Configuration des règles** : Interface admin pour créer/modifier les règles
2. 🔄 **Visualisation des tâches** : Interface séparée pour tâches chantiers vs administratives
3. 🔄 **Vue globale** : Dashboard unifié pour Yann/Julien avec les deux types
4. 🔄 **Notifications** : Alertes pour nouvelles tâches automatiques

---

## 🎯 **AVANTAGES DE L'APPROCHE DEUX TABLES**

### **Pourquoi Deux Tables au lieu d'Une ?**

#### **✅ Avantages de `taches_chantiers` + `taches_administratives`**
- **Contraintes adaptées** : `chantier_id` obligatoire pour tâches chantiers, optionnel pour admin
- **Requêtes optimisées** : Filtrage plus rapide par type de tâche
- **Évolutivité** : Champs spécifiques par type (`type_administratif`)
- **Maintenance** : Logique métier séparée et plus claire
- **Performance** : Index optimisés selon le type d'usage
- **Sécurité** : Permissions différenciées par type de tâche

#### **❌ Inconvénients d'une Table Unique**
- **Complexité** : Nombreux champs nullable
- **Performance** : Index moins efficaces
- **Maintenance** : Logique métier mélangée
- **Contraintes** : Difficile d'imposer des règles spécifiques

### **Exemple Concret**

#### **Tâche Chantier** (Table `taches_chantiers`)
```python
{
    "titre": "Contacter Enedis pour isolation",
    "chantier_id": 123,  # OBLIGATOIRE
    "utilisateur": "YANN",
    "auto_generee": True,
    "declencheur": "famille_ouvrage_detectee"
}
```

#### **Tâche Administrative** (Table `taches_administratives`)
```python
{
    "titre": "Déclaration TVA mensuelle",
    "chantier_id": None,  # OPTIONNEL
    "type_administratif": "FISCAL",
    "utilisateur": "JULIEN",
    "auto_generee": True,
    "declencheur": "echeance_mensuelle"
}
```

---

## 📊 **EXEMPLES D'UTILISATION**

### **Scénario 1 : Devis avec Isolation Enedis**
1. **Création du chantier** : Devis "Isolation des fils par Enedis"
2. **Détection automatique** : Service détecte "Enedis" dans les familles d'ouvrages
3. **Création de tâche** : "Contacter Enedis pour isolation" assignée à Yann
4. **Échéance** : 2 jours après création du chantier

### **Scénario 2 : Devis Important (>50k€)**
1. **Création du chantier** : Devis de 75 000€
2. **Détection automatique** : Service détecte montant > seuil de 50k€
3. **Création de tâche** : "Validation direction pour chantier > 50k€" assignée à Julien
4. **Échéance** : 1 jour après création du chantier

---

## 🔗 **LIENS UTILES**

- **[Modèles SQLAlchemy](./database-schema.md)** - Structure détaillée des tables
- **[API Endpoints](./api-endpoints.md)** - Spécifications REST complètes
- **[ATARYS_MODULES.md](../../00-overview/ATARYS_MODULES.md)** - Nomenclature officielle

---

**✅ Module 2 - Automatisation intelligente basée sur les familles d'ouvrages !**
