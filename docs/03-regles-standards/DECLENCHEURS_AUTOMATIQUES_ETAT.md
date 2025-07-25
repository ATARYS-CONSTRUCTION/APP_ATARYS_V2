# 🚀 Déclencheurs Automatiques et Gestion des Échéances

> **État réel des déclencheurs automatiques + Gestion professionnelle des échéances**  
> **Ce qui existe VRAIMENT vs ce qui est prévu + Bonnes pratiques développeur pro**  
> Dernière mise à jour : 19/07/2025

---

## 🎯 **Vue d'Ensemble**

Cette documentation clarifie l'état actuel des déclencheurs automatiques dans ATARYS V2 et présente l'approche professionnelle pour la gestion des échéances configurables.

---

## ✅ **Ce qui EXISTE VRAIMENT**

### **1. Service Backend Fonctionnel**
- **Fichier** : `backend/app/services/tache_automatique_service.py`
- **Statut** : ✅ **OPÉRATIONNEL**
- **Tests** : ✅ **TOUS RÉUSSIS**

### **2. Déclencheurs Configurés (3 seulement)**

#### **Module 3 - Chantiers (EN COURS)**
- `chantier_creation` : 2 tâches automatiques
  - "Préparer dossier chantier" (3 jours après création)
  - "Contacter client pour signature" (1 jour après création)
- `chantier_signature` : 2 tâches automatiques
  - "Créer dossier chantier" (2 jours après signature)
  - "Préparer planning détaillé" (3 jours après signature)

#### **Module 9 - Salariés (EN COURS)**
- `insertion_salarié` : 1 tâche automatique
  - "Créer fiche salarié" (1 jour après création)

### **3. Tests Fonctionnels**
- **Fichier** : `backend/scripts/test_tache_automatique_service.py`
- **Résultats** : ✅ **TOUS LES TESTS RÉUSSIS**
- **Validation** : Service opérationnel et prêt à l'utilisation

---

## 🎯 **Gestion Professionnelle des Échéances**

### **Problématique :**
> "Comment paramétrer les dates d'échéances qui pourront être paramétrées 'par défaut' pour une liste automatique (ex: plan d'exécution = 1 mois après signature, modifiable facilement dans le frontend) ?"

### **Réponse Professionnelle :**
Créer une **table de configuration des règles d'échéance** avec un **service dédié** pour la gestion.

### **🏗️ Architecture Professionnelle**

#### **1. Table de Configuration : `regles_echeance`**
```sql
CREATE TABLE regles_echeance (
    id INTEGER PRIMARY KEY,
    code_regle VARCHAR(50) UNIQUE NOT NULL,  -- 'PLAN_EXECUTION_1_MOIS'
    nom_regle VARCHAR(100) NOT NULL,         -- 'Plan d\'exécution 1 mois'
    type_tache VARCHAR(100) NOT NULL,        -- 'Plan d\'exécution'
    famille_tache VARCHAR(50) NOT NULL,      -- 'chantier'
    
    -- Configuration des délais
    delai_jours INTEGER DEFAULT 1,
    delai_mois INTEGER DEFAULT 0,
    delai_annees INTEGER DEFAULT 0,
    
    -- Référence temporelle
    reference_temporelle VARCHAR(50) DEFAULT 'signature',
    -- Options: 'creation', 'signature', 'debut_chantier', 'fin_chantier'
    
    -- Configuration par défaut
    priorite VARCHAR(20) DEFAULT 'NORMALE',
    statut_defaut VARCHAR(30) DEFAULT 'A faire',
    actif BOOLEAN DEFAULT TRUE,
    
    description TEXT,
    created_at DATETIME,
    updated_at DATETIME
);
```

#### **2. Service Dédié : `EcheanceService`**
```python
# backend/app/services/echeance_service.py
class EcheanceService:
    def calculer_echeance_selon_regle(self, regle_id: int, 
                                     date_reference: datetime = None) -> datetime:
        """Calculer une échéance selon une règle configurée"""
        
    def creer_tache_chantier_avec_echeance(self, titre: str, type_tache: str, 
                                          famille_tache: str, regle_id: int,
                                          chantier_id: int,
                                          contexte: Dict = None) -> TachesChantiers:
        """Créer une tâche chantier avec échéance calculée automatiquement"""
        
    def creer_tache_administrative_avec_echeance(self, titre: str, type_tache: str, 
                                                famille_tache: str, regle_id: int,
                                                contexte: Dict = None) -> TachesAdministratives:
        """Créer une tâche administrative avec échéance calculée automatiquement"""
        
    def modifier_echeance_tache_chantier(self, tache_id: int, 
                                        nouvelle_date: datetime) -> bool:
        """Modifier l'échéance d'une tâche chantier (frontend)"""
        
    def modifier_echeance_tache_administrative(self, tache_id: int, 
                                              nouvelle_date: datetime) -> bool:
        """Modifier l'échéance d'une tâche administrative (frontend)"""
```

### **🎯 Exemples Concrets**

#### **Exemple 1 : Plan d'Exécution**
```python
# Créer la règle
regle = echeance_service.creer_regle_echeance(
    code_regle='PLAN_EXECUTION_1_MOIS',
    nom_regle='Plan d\'exécution 1 mois',
    type_tache='Plan d\'exécution',
    famille_tache='chantier',
    delai_mois=1,  # 1 mois
    reference_temporelle='signature',  # Après signature
    priorite='HAUTE',
    description='Plan d\'exécution détaillé à préparer 1 mois après signature'
)

# Utiliser la règle
tache = echeance_service.creer_tache_avec_echeance(
    titre='Préparer plan d\'exécution détaillé',
    type_tache='Plan d\'exécution',
    famille_tache='chantier',
    regle_id=regle.id,
    contexte={'chantier_id': 123}
)
```

#### **Exemple 2 : Contact Client**
```python
# Règle pour contacter le client
regle = echeance_service.creer_regle_echeance(
    code_regle='CONTACT_CLIENT_1_JOUR',
    nom_regle='Contact client 1 jour',
    type_tache='Contact client',
    famille_tache='chantier',
    delai_jours=1,  # 1 jour
    reference_temporelle='creation',
    priorite='HAUTE',
    description='Contacter le client 1 jour après création du chantier'
)
```

### **🎨 Interface Frontend**

#### **1. Configuration des Règles**
```jsx
// Interface admin pour configurer les règles
const RegleEcheanceForm = () => {
  const [regle, setRegle] = useState({
    code_regle: '',
    nom_regle: '',
    type_tache: '',
    famille_tache: '',
    delai_jours: 1,
    delai_mois: 0,
    delai_annees: 0,
    reference_temporelle: 'creation',
    priorite: 'NORMALE',
    statut_defaut: 'A faire'
  });

  return (
    <form>
      <input 
        placeholder="Code règle (ex: PLAN_EXECUTION_1_MOIS)"
        value={regle.code_regle}
        onChange={(e) => setRegle({...regle, code_regle: e.target.value})}
      />
      
      <select 
        value={regle.reference_temporelle}
        onChange={(e) => setRegle({...regle, reference_temporelle: e.target.value})}
      >
        <option value="creation">Après création</option>
        <option value="signature">Après signature</option>
        <option value="debut_chantier">Après début chantier</option>
        <option value="fin_chantier">Après fin chantier</option>
      </select>
      
      <div>
        <label>Délai :</label>
        <input type="number" placeholder="Jours" value={regle.delai_jours} />
        <input type="number" placeholder="Mois" value={regle.delai_mois} />
        <input type="number" placeholder="Années" value={regle.delai_annees} />
      </div>
    </form>
  );
};
```

#### **2. Modification d'Échéance**
```jsx
// Interface pour modifier une échéance
const ModifierEcheance = ({ tache }) => {
  const [nouvelleDate, setNouvelleDate] = useState(tache.date_echeance);
  
  const modifierEcheance = async () => {
    const response = await fetch(`/api/taches/${tache.id}/echeance`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date_echeance: nouvelleDate })
    });
    
    if (response.ok) {
      // Rafraîchir la liste des tâches
      refreshTaches();
    }
  };

  return (
    <div>
      <input 
        type="datetime-local" 
        value={nouvelleDate}
        onChange={(e) => setNouvelleDate(e.target.value)}
      />
      <button onClick={modifierEcheance}>
        Modifier échéance
      </button>
    </div>
  );
};
```

### **📊 Avantages de cette Approche**

#### **1. Flexibilité Maximale**
- ✅ **Configuration sans code** : L'admin peut tout configurer
- ✅ **Modification en temps réel** : Changement des délais sans redéploiement
- ✅ **Références temporelles multiples** : Création, signature, début chantier, etc.

#### **2. Maintenabilité**
- ✅ **Service centralisé** : Toute la logique dans un service
- ✅ **Tests unitaires** : Facile à tester
- ✅ **Documentation intégrée** : Chaque règle documentée

#### **3. Évolutivité**
- ✅ **Nouvelles références temporelles** : Facile d'ajouter
- ✅ **Types de délais** : Jours, mois, années, heures, etc.
- ✅ **Règles conditionnelles** : Selon le contexte

#### **4. Interface Utilisateur**
- ✅ **Configuration intuitive** : Formulaire simple
- ✅ **Modification facile** : Interface pour changer les échéances
- ✅ **Prévisualisation** : Voir l'échéance calculée avant validation

### **🎯 Exemples de Règles Typiques**

#### **Chantiers**
```python
# Plan d'exécution : 1 mois après signature
'PLAN_EXECUTION_1_MOIS': {'delai_mois': 1, 'reference': 'signature'}

# Contact client : 1 jour après création
'CONTACT_CLIENT_1_JOUR': {'delai_jours': 1, 'reference': 'creation'}

# Préparation chantier : 3 jours après signature
'PREPARATION_CHANTIER_3_JOURS': {'delai_jours': 3, 'reference': 'signature'}
```

#### **Salariés**
```python
# Fiche salarié : 1 jour après création
'FICHE_SALARIE_1_JOUR': {'delai_jours': 1, 'reference': 'creation'}

# Formation : 7 jours après création
'FORMATION_7_JOURS': {'delai_jours': 7, 'reference': 'creation'}
```

---

## ❌ **Ce qui N'EXISTE PAS ENCORE**

### **Modules Non Implémentés**
- **Module 6 - Clients** : N'existe pas encore
- **Module 1 - Planning** : N'est pas encore implémenté
- **Autres modules** : À définir selon les besoins

### **Tables de Base de Données**
- **FamilleTach** : Table des templates de tâches (À créer)
- **TachesChantiers** : Table des tâches liées aux chantiers (À créer)
- **TachesAdministratives** : Table des tâches administratives générales (À créer)
- **RegleEcheance** : Table des règles d'échéance (À créer)

### **Intégration Frontend**
- **Interface admin** : Pour configurer les déclencheurs
- **Interface de suivi** : Pour gérer les tâches générées
- **Interface échéances** : Pour configurer les règles d'échéance

---

## 🔧 **Architecture Technique**

### **Service Backend**
```python
# backend/app/services/tache_automatique_service.py
class TacheAutomatiqueService:
    def __init__(self):
        self.declencheurs_supportes = {
            # Module 3 - Chantiers (EN COURS)
            'chantier_creation': self._declencher_taches_chantier_creation,
            'chantier_signature': self._declencher_taches_chantier_signature,
            
            # Module 9 - Salariés (EN COURS)
            'insertion_salarié': self._declencher_taches_insertion_salarie,
        }
```

### **Intégration dans les Endpoints**
```python
# Exemple d'intégration (À IMPLÉMENTER)
@chantier_bp.route('/api/chantiers/', methods=['POST'])
def create_chantier():
    # 1. Créer le chantier
    chantier = Chantier(**data)
    db.session.add(chantier)
    db.session.commit()
    
    # 2. DÉCLENCHEUR AUTOMATIQUE
    service = TacheAutomatiqueService()
    contexte = {'chantier_id': chantier.id}
    taches_creees = service.declencher_taches('chantier_creation', contexte)
    
    return jsonify({
        'success': True,
        'data': chantier_schema.dump(chantier),
        'taches_creees': len(taches_creees)
    })
```

### **Intégration des Échéances dans les Déclencheurs**
```python
# backend/app/services/tache_automatique_service.py
from app.services.echeance_service import EcheanceService

class TacheAutomatiqueService:
    def __init__(self):
        self.echeance_service = EcheanceService()
    
    def declencher_taches(self, evenement: str, contexte: Dict) -> List[Dict]:
        # ... logique existante ...
        
        # Utiliser le service d'échéance pour créer les tâches
        for template in taches_templates:
            if template.get('regle_echeance_id'):
                # Déterminer le type de table selon le contexte
                if contexte.get('chantier_id'):
                    # Tâche liée à un chantier spécifique
                    tache = self.echeance_service.creer_tache_chantier_avec_echeance(
                        titre=template['type_tache'],
                        type_tache=template['type_tache'],
                        famille_tache=template['famille_tache'],
                        regle_id=template['regle_echeance_id'],
                        chantier_id=contexte['chantier_id'],
                        contexte=contexte
                    )
                else:
                    # Tâche administrative générale
                    tache = self.echeance_service.creer_tache_administrative_avec_echeance(
                        titre=template['type_tache'],
                        type_tache=template['type_tache'],
                        famille_tache=template['famille_tache'],
                        regle_id=template['regle_echeance_id'],
                        contexte=contexte
                    )
                taches_creees.append(tache.to_dict())
```

---

## 📋 **Prochaines Étapes**

### **1. Créer les Tables de Base de Données**
```python
# À créer dans backend/app/models/
class FamilleTach(BaseModel):
    __tablename__ = 'famille_tach'
    # Colonnes pour les templates de tâches

class TachesChantiers(BaseModel):
    __tablename__ = 'taches_chantiers'
    # Colonnes pour les tâches liées aux chantiers spécifiques
    chantier_id = db.Column(db.Integer, db.ForeignKey('chantiers.id'), nullable=False)

class TachesAdministratives(BaseModel):
    __tablename__ = 'taches_administratives'
    # Colonnes pour les tâches administratives générales
    # Pas de lien obligatoire vers un chantier

class RegleEcheance(BaseModel):
    __tablename__ = 'regles_echeance'
    # Colonnes pour les règles d'échéance
```

### **2. Intégrer dans les Endpoints Existants**
- **Module 3** : `backend/app/routes/module_3.py`
- **Module 9** : `backend/app/routes/module_9.py`

### **3. Créer l'Interface Frontend**
- **Configuration** : Interface admin pour les déclencheurs
- **Suivi** : Interface de gestion des tâches
- **Échéances** : Interface de configuration des règles d'échéance

### **4. Ajouter de Nouveaux Déclencheurs**
- **Selon les besoins métier** : Nouveaux événements
- **Configuration** : Via interface admin
- **Validation** : Tests pour chaque nouveau déclencheur

---

## 🚨 **Points d'Attention**

### **1. Ne Pas Inventer**
- ❌ **JAMAIS** créer des déclencheurs pour des modules inexistants
- ❌ **JAMAIS** inventer des tâches sans connaître les besoins métier
- ✅ **TOUJOURS** valider avec l'utilisateur avant d'ajouter

### **2. Validation Obligatoire**
- ✅ **Tester** chaque nouveau déclencheur
- ✅ **Documenter** les règles métier
- ✅ **Valider** avec l'utilisateur final

### **3. Évolution Progressive**
- ✅ **Commencer** par les modules existants
- ✅ **Ajouter** selon les besoins réels
- ✅ **Maintenir** la cohérence

---

## 📊 **Métriques Actuelles**

### **Service Backend**
- **Déclencheurs configurés** : 3
- **Templates de tâches** : 5
- **Tests réussis** : 100%
- **Statut** : ✅ **OPÉRATIONNEL**

### **Modules Couverts**
- **Module 3 - Chantiers** : ✅ Partiellement
- **Module 9 - Salariés** : ✅ Partiellement
- **Autres modules** : ❌ Non implémentés

---

## 🎯 **Conclusion**

### **Ce qui Fonctionne**
- ✅ **Service backend** opérationnel
- ✅ **3 déclencheurs** configurés et testés
- ✅ **Architecture** prête pour l'extension
- ✅ **Approche échéances** professionnelle définie

### **Ce qui Manque**
- ❌ **Tables de base de données** (FamilleTach, TacheReelle, RegleEcheance)
- ❌ **Intégration** dans les endpoints existants
- ❌ **Interface frontend** pour la configuration
- ❌ **Nouveaux déclencheurs** selon les besoins métier

### **Recommandation**
1. **Créer les tables** de base de données
2. **Intégrer** dans les endpoints existants
3. **Tester** en conditions réelles
4. **Ajouter** de nouveaux déclencheurs selon les besoins

---

**✅ Service opérationnel + Approche échéances professionnelle - Prêt pour l'intégration progressive !** 