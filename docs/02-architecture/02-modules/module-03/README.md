# 🏗️ Module 3 - LISTE CHANTIERS

> **Gestion des chantiers clients avec pipeline commercial complet**  
> **État : STRUCTURE CRÉÉE** 📋 - Modèles à définir  
> Dernière mise à jour : 19/07/2025

---

## 🎯 Vue d'ensemble

Le module **3 - LISTE CHANTIERS** gère l'ensemble du pipeline commercial des chantiers ATARYS, depuis les projets en prospection jusqu'aux chantiers archivés.

### **Objectifs Principaux**
- Gestion des chantiers clients
- Suivi des états (Projet, Signé, En cours, Terminé, Annulé)
- Pipeline commercial complet
- Vue par statut
- **Déclencheurs automatiques** : Génération de tâches selon les événements

---

## 📋 État d'Implémentation

### **✅ Implémenté**
- **Structure de fichier** : `module_3.py` créé
- **Pattern BaseModel** : Prêt pour les modèles

### **🔄 En Cours**
- **Modèles SQLAlchemy** : À définir selon besoins métier
- **API REST** : Endpoints à créer
- **Interface Frontend** : Composants React à développer

### **❌ À Implémenter**
- **Tables principales** : Chantiers, États, Pipeline
- **Relations** : Avec clients et devis
- **Logique métier** : Workflows commerciaux
- **Déclencheurs automatiques** : Intégration du service TacheAutomatiqueService

---

## 🏗️ Architecture Technique

### **Fichiers Concernés**
```
backend/app/models/module_3.py      # Modèles SQLAlchemy (structure créée)
backend/app/routes/module_3.py      # API REST (à créer)
backend/app/schemas/module_3.py     # Validation Marshmallow (à créer)
frontend/src/pages/Module3/         # Interface React (à créer)
```

### **Dépendances Critiques**
- **Module 5** : DEVIS-FACTURATION (relation chantier → devis)
- **Module 1** : PLANNING (planification chantiers)
- **Module 4** : CHANTIERS (suivi détaillé)

---

## 📊 Sous-modules

Selon `ATARYS_MODULES.md`, le module 3 comprend :

### **3.1 - LISTE CHANTIERS** ❌ **À IMPLÉMENTER**
- Vue d'ensemble de tous les chantiers
- Filtrage par état, client, période
- Recherche avancée
- Tableau de bord commercial

### **3.2 - CHANTIERS PROJETS** ❌ **À IMPLÉMENTER**
- Chantiers en phase de prospection
- Suivi des opportunités
- Conversion en chantiers signés
- Pipeline commercial

### **3.3 - CHANTIERS SIGNÉS** ❌ **À IMPLÉMENTER**
- Chantiers confirmés et contractualisés
- Préparation et planification
- Transition vers "En cours"
- Gestion administrative

### **3.4 - CHANTIERS EN COURS** ❌ **À IMPLÉMENTER**
- Chantiers actifs en réalisation
- Suivi d'avancement
- Gestion des interventions
- Reporting temps réel

### **3.5 - CHANTIERS ARCHIVES** ❌ **À IMPLÉMENTER**
- Chantiers terminés ou annulés
- Conservation des données
- Historique et références
- Analyses post-projet

---

## 🗄️ Structure de Données Proposée

### **Table Principale : Chantiers**
```python
class Chantiers(BaseModel):
    __tablename__ = 'chantiers'
    
    # Identification
    numero_chantier = db.Column(db.String(50), nullable=False, unique=True)
    nom_chantier = db.Column(db.String(200), nullable=False)
    
    # Localisation
    adresse = db.Column(db.Text)
    ville = db.Column(db.String(100))
    code_postal = db.Column(db.String(10))
    
    # Relations (à définir selon autres modules)
    client_id = db.Column(db.Integer)  # Relation future avec module clients
    
    # États et workflow
    statut = db.Column(db.String(30), default='PROJET')
    # PROJET, SIGNE, EN_COURS, TERMINE, ANNULE, ARCHIVE
    
    # Dates
    date_creation = db.Column(db.Date, default=datetime.utcnow)
    date_signature = db.Column(db.Date)
    date_debut_prevue = db.Column(db.Date)
    date_fin_prevue = db.Column(db.Date)
    date_debut_reelle = db.Column(db.Date)
    date_fin_reelle = db.Column(db.Date)
    
    # Financier
    montant_estime = db.Column(db.Numeric(10, 2))
    montant_signe = db.Column(db.Numeric(10, 2))
    
    # Suivi
    avancement_pct = db.Column(db.Numeric(5, 2), default=0.00)
    notes = db.Column(db.Text)
    priorite = db.Column(db.String(10), default='NORMALE')
```

### **États des Chantiers**
```python
class EtatChantier(BaseModel):
    __tablename__ = 'etat_chantier'
    
    code = db.Column(db.String(20), nullable=False, unique=True)
    libelle = db.Column(db.String(100), nullable=False)
    couleur = db.Column(db.String(7))  # Code couleur hex
    ordre = db.Column(db.Integer)  # Ordre dans le pipeline
    actif = db.Column(db.Boolean, default=True)
```

---

## 🛣️ API Endpoints Proposées

### **Gestion des Chantiers**
```http
GET    /api/module-3/chantiers              # Liste avec filtres et pagination
POST   /api/module-3/chantiers              # Création nouveau chantier
GET    /api/module-3/chantiers/:id          # Détail d'un chantier
PUT    /api/module-3/chantiers/:id          # Modification chantier
DELETE /api/module-3/chantiers/:id          # Suppression (soft delete)
```

### **Pipeline Commercial**
```http
GET    /api/module-3/chantiers/projets      # Chantiers en prospection
GET    /api/module-3/chantiers/signes       # Chantiers signés
GET    /api/module-3/chantiers/en-cours     # Chantiers actifs
GET    /api/module-3/chantiers/archives     # Chantiers archivés
```

### **Gestion des États**
```http
GET    /api/module-3/etats                  # Liste des états disponibles
PUT    /api/module-3/chantiers/:id/etat     # Changement d'état
```

### **Statistiques et Reporting**
```http
GET    /api/module-3/stats/pipeline         # Statistiques du pipeline
GET    /api/module-3/stats/chiffre-affaires # CA par période et statut
GET    /api/module-3/stats/conversion       # Taux de conversion
```

---

## 🎯 Priorités de Développement

### **Phase 1 : Base (Priorité 1)**
1. **Modèle Chantiers** : Table principale avec statuts
2. **API CRUD** : Opérations de base
3. **États simples** : PROJET, SIGNE, EN_COURS, TERMINE

### **Phase 2 : Pipeline (Priorité 2)**
1. **Workflow** : Transitions d'états automatisées
2. **Vues par statut** : Interfaces spécialisées
3. **Filtrage avancé** : Recherche multi-critères

### **Phase 3 : Intégration (Priorité 3)**
1. **Relations** : Avec clients, devis, planning
2. **Reporting** : Tableaux de bord et KPI
3. **Automatisation** : Notifications et alertes

### **Phase 4 : Déclencheurs Automatiques (Priorité 4)**
1. **Service TacheAutomatiqueService** : Intégration du service de génération
2. **Déclencheurs chantier** : `chantier_creation`, `chantier_signature`, `chantier_en_cours`
3. **Configuration** : Interface admin pour les tâches automatiques
4. **Suivi** : Monitoring des tâches générées

---

## 🚀 **Déclencheurs Automatiques - Module 3**

### **📋 Vue d'Ensemble**

Le module 3 intègre un système de déclencheurs automatiques qui génère des tâches en fonction des événements liés aux chantiers. Cette automatisation améliore l'efficacité opérationnelle et réduit les oublis.

### **🎯 Déclencheurs Configurés**

#### **Déclencheurs Chantier**
- `chantier_creation` : Création d'un nouveau chantier
- `chantier_signature` : Signature d'un chantier
- `chantier_preparation` : Phase de préparation du chantier
- `chantier_en_cours` : Chantier en cours d'exécution
- `chantier_termine` : Fin d'un chantier

### **🏗️ Intégration dans les Endpoints**

#### **Création de Chantier**
```python
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

#### **Changement d'État**
```python
@chantier_bp.route('/api/chantiers/<int:chantier_id>/etat', methods=['PUT'])
def change_etat_chantier(chantier_id):
    # 1. Modifier l'état du chantier
    chantier = Chantier.query.get_or_404(chantier_id)
    ancien_etat = chantier.statut
    chantier.statut = nouveau_etat
    db.session.commit()
    
    # 2. DÉCLENCHEUR AUTOMATIQUE : Selon le nouvel état
    service = TacheAutomatiqueService()
    contexte = {'chantier_id': chantier.id, 'ancien_etat': ancien_etat}
    
    if nouveau_etat == 'SIGNE':
        taches_creees = service.declencher_taches('chantier_signature', contexte)
    elif nouveau_etat == 'EN_COURS':
        taches_creees = service.declencher_taches('chantier_en_cours', contexte)
    elif nouveau_etat == 'TERMINE':
        taches_creees = service.declencher_taches('chantier_termine', contexte)
    
    return jsonify({
        'success': True,
        'data': chantier_schema.dump(chantier),
        'taches_creees': len(taches_creees)
    })
```

### **📋 Tâches Automatiques Typiques**

#### **Lors de la Création (`chantier_creation`)**
- **Tâche administrative** : "Préparer dossier chantier"
- **Tâche commerciale** : "Contacter client pour signature"
- **Tâche technique** : "Étudier faisabilité technique"
- **Tâche planning** : "Planifier visite chantier"

#### **Lors de la Signature (`chantier_signature`)**
- **Tâche administrative** : "Créer dossier chantier"
- **Tâche technique** : "Préparer planning détaillé"
- **Tâche RH** : "Affecter équipe chantier"
- **Tâche logistique** : "Commander matériaux"

#### **Lors du Début (`chantier_en_cours`)**
- **Tâche technique** : "Démarrer chantier"
- **Tâche communication** : "Informer client du démarrage"
- **Tâche suivi** : "Programmer visites régulières"
- **Tâche reporting** : "Mettre en place suivi avancement"

#### **Lors de la Fin (`chantier_termine`)**
- **Tâche administrative** : "Clôturer dossier chantier"
- **Tâche commerciale** : "Demander satisfaction client"
- **Tâche technique** : "Réceptionner chantier"
- **Tâche comptable** : "Facturer chantier"

### **🎯 Avantages pour le Module 3**

#### **Efficacité Opérationnelle**
- ✅ **Pas d'oubli** : Toutes les tâches sont générées automatiquement
- ✅ **Standardisation** : Processus uniforme pour tous les chantiers
- ✅ **Traçabilité** : Historique complet des actions

#### **Amélioration du Pipeline**
- ✅ **Suivi automatique** : Chaque étape génère les tâches suivantes
- ✅ **Réactivité** : Détection immédiate des changements d'état
- ✅ **Reporting** : Métriques sur les tâches générées

---

## 🔗 Liens Utiles

- **[Modèles SQLAlchemy](./database-schema.md)** - Structure détaillée des tables
- **[API Endpoints](./api-endpoints.md)** - Spécifications REST complètes
- **[Règles Métier](./business-rules.md)** - Workflows et validations
- **[ATARYS_MODULES.md](../../00-overview/ATARYS_MODULES.md)** - Nomenclature officielle
- **[Déclencheurs Automatiques](../module-02/README.md)** - Documentation complète du système
