# 🏗️ États de Chantiers ATARYS - Spécification Complète

> **Documentation des états et workflow des chantiers**  
> Basé sur l'analyse du document "Liste Chantiers"  
> Date : 05/07/2025

---

## 🎯 **Recommandation : TABLE (pas ENUM)**

### **✅ Avantages de la Table `etats_chantier`**
- **Flexibilité** : Ajout/modification sans migration
- **Métadonnées** : Couleur, ordre, règles métier
- **Workflow** : Transitions configurables
- **Interface** : Gestion via API REST
- **Évolutivité** : Extension facile des propriétés

---

## 📋 **États Complets Identifiés**

### **Structure Table Étendue**
```sql
CREATE TABLE etats_chantier (
    id INTEGER PRIMARY KEY,
    libelle TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL, -- Code technique
    couleur TEXT, -- Couleur hex (#RRGGBB)
    ordre INTEGER DEFAULT 0,
    description TEXT,
    actif INTEGER DEFAULT 1,
    workflow_suivants TEXT, -- JSON des états suivants possibles
    actions_requises TEXT, -- JSON des actions nécessaires
    notifications TEXT, -- JSON des alertes à envoyer
    duree_moyenne INTEGER, -- Durée moyenne en jours
    date_creation TEXT,
    date_modification TEXT
);
```

### **États Proposés selon Document**

| ID | Code | Libellé | Couleur | Ordre | Description |
|----|------|---------|---------|-------|-------------|
| 1 | PROJET | Projet | #3B82F6 | 10 | Chantier en phase de prospection/étude |
| 2 | MODIFICATION | Modification | #F59E0B | 20 | Modifications du projet en cours |
| 3 | EN_COURS_SIGNATURE | En cours de signature | #EF4444 | 30 | Négociation, validation contractuelle |
| 4 | SIGNATURE | Signature | #10B981 | 40 | Devis signé, chantier confirmé |
| 5 | EN_COURS | En cours | #8B5CF6 | 50 | Exécution des travaux |
| 6 | A_FINIR | À finir | #F97316 | 60 | Travaux en finition, réception |
| 7 | TERMINE | Terminé | #059669 | 70 | Chantier livré et facturé |
| 8 | SAV | SAV | #EC4899 | 80 | Service après-vente, garantie |
| 9 | NON_ABOUTI | Non abouti | #6B7280 | 90 | Chantier non abouti/sans suite |

---

## 🔄 **Workflow et Transitions**

### **Transitions Autorisées**
```json
{
  "PROJET": ["MODIFICATION", "EN_COURS_SIGNATURE", "NON_ABOUTI"],
  "MODIFICATION": ["EN_COURS_SIGNATURE", "PROJET", "NON_ABOUTI"],
  "EN_COURS_SIGNATURE": ["SIGNATURE", "MODIFICATION", "NON_ABOUTI"],
  "SIGNATURE": ["EN_COURS"],
  "EN_COURS": ["A_FINIR"],
  "A_FINIR": ["TERMINE", "SAV"],
  "TERMINE": ["SAV"],
  "SAV": ["TERMINE"],
  "NON_ABOUTI": ["PROJET", "MODIFICATION"]
}
```

### **Actions Requises par État (Tâches Chantier Récurrentes)**

> **⚠️ IMPORTANT :** Les actions ci-dessous sont des **EXEMPLES**.  
> Les vraies tâches seront récupérées automatiquement depuis la table `liste_taches`  
> par le service Python `etat_chantier_service.py` à créer.
> 
> **Liaison avec la Liste des Tâches :**  
> Famille : **CHANTIER RECURRENT**  
> Types : Administrative, Technique, Commerciale

```json
{
  "PROJET": {
    "chantier_recurrent_administrative": ["etablir_devis_initial", "creation_fiche_client"],
    "chantier_recurrent_technique": ["visite_technique", "etude_faisabilite"],
    "chantier_recurrent_commerciale": ["prospection_client", "negociation_initiale"]
  },
    "MODIFICATION": {
    "chantier_recurrent_administrative": ["avenant_devis", "mise_a_jour_contrat"],
    "chantier_recurrent_technique": ["nouvelle_etude_technique", "recalcul_metres"],
    "chantier_recurrent_commerciale": ["negociation_modifications", "validation_client"]
  },
  "EN_COURS_SIGNATURE": {
    "chantier_recurrent_administrative": ["finaliser_contrat", "validation_juridique"],
    "chantier_recurrent_commerciale": ["negociation_finale", "presentation_contrat"],
    "chantier_recurrent_technique": ["validation_technique_finale"]
  },
  "SIGNATURE": {
    "chantier_recurrent_administrative": ["planifier_travaux", "creation_planning"],
    "chantier_recurrent_technique": ["commander_materiaux", "mobiliser_equipes"],
    "chantier_recurrent_commerciale": ["confirmation_client", "lancement_chantier"]
  },
  "EN_COURS": {
    "chantier_recurrent_technique": ["execution_travaux", "controles_qualite"],
    "chantier_recurrent_administrative": ["suivi_avancement", "gestion_planning"],
    "chantier_recurrent_commerciale": ["communication_client", "suivi_satisfaction"]
  },
  "A_FINIR": {
    "chantier_recurrent_technique": ["travaux_finition", "controles_finaux"],
    "chantier_recurrent_administrative": ["preparation_reception", "documentation_finale"],
    "chantier_recurrent_commerciale": ["validation_client", "preparation_livraison"]
  },
  "TERMINE": {
    "chantier_recurrent_administrative": ["facturation_finale", "archivage_dossier"],
    "chantier_recurrent_commerciale": ["bilan_satisfaction", "demande_avis"],
    "chantier_recurrent_technique": ["bilan_technique", "retour_experience"]
  },
  "SAV": {
    "chantier_recurrent_technique": ["intervention_garantie", "diagnostic_probleme"],
    "chantier_recurrent_administrative": ["suivi_garantie", "gestion_reclamation"],
    "chantier_recurrent_commerciale": ["relation_client_sav", "satisfaction_intervention"]
  },
  "NON_ABOUTI": {
    "chantier_recurrent_administrative": ["cloture_administrative", "archivage", "analyse_causes"],
    "chantier_recurrent_commerciale": ["notification_client", "bilan_commercial"],
    "chantier_recurrent_technique": ["arret_commandes", "liberation_ressources"]
  },
  "REACTIVATION": {
    "chantier_recurrent_administrative": ["mise_a_jour_dossier", "verification_donnees"],
    "chantier_recurrent_commerciale": ["reprise_contact_client", "actualisation_besoins"],
    "chantier_recurrent_technique": ["verification_faisabilite", "mise_a_jour_prix"]
  }
}
```

---

## 🚨 **Règles Métier**

### **Contraintes de Transition**
1. **Workflow linéaire** : Progression normale vers la signature puis les travaux
2. **États finaux** : TERMINE et SAV (avec possibilité d'aller-retour)
3. **Réactivation possible** : NON_ABOUTI peut revenir en PROJET ou MODIFICATION
4. **Validation obligatoire** des actions requises avant transition
5. **Traçabilité** : Chaque changement d'état est historisé avec date/utilisateur

### **Calculs Automatiques**
- **Durée moyenne** : Calculée automatiquement selon historique
- **Alertes** : Déclenchées selon durée dans l'état
- **Statistiques** : Temps moyen par état, taux de conversion

### **Notifications Automatiques**
```json
{
  "PROJET": {
    "delai": 15,
    "action": "suivi_devis",
    "destinataires": ["commercial", "gerant"]
  },
  "MODIFICATION": {
    "delai": 7,
    "action": "finaliser_modifications",
    "destinataires": ["commercial", "technique"]
  },
  "EN_COURS_SIGNATURE": {
    "delai": 14,
    "action": "suivi_signature",
    "destinataires": ["commercial"]
  },
  "SIGNATURE": {
    "delai": 3,
    "action": "lancement_chantier",
    "destinataires": ["conducteur_travaux", "gerant"]
  },
  "EN_COURS": {
    "delai": 30,
    "action": "point_avancement",
    "destinataires": ["conducteur_travaux", "gerant"]
  },
  "A_FINIR": {
    "delai": 7,
    "action": "finaliser_travaux",
    "destinataires": ["conducteur_travaux", "commercial"]
  },
  "SAV": {
    "delai": 5,
    "action": "intervention_sav",
    "destinataires": ["technique", "commercial"]
  }
}
```

---

## 🎨 **Interface Utilisateur**

### **Affichage dans l'Application**
- **Badges colorés** selon la couleur définie
- **Filtres** par état dans les listes
- **Tableau de bord** avec répartition par état
- **Workflow visuel** pour les transitions

### **Gestion Admin (API REST)**
- **CRUD complet** des états
- **Validation** des transitions
- **Import/Export** des configurations
- **Historique** des modifications

---

## 📊 **Métriques et Reporting**

### **KPIs par État**
- **Nombre de chantiers** par état
- **Durée moyenne** dans chaque état
- **Taux de conversion** entre états
- **Chantiers en retard** selon durée moyenne

### **Alertes Automatiques**
- **Chantiers bloqués** (trop longtemps dans un état)
- **Actions en retard** (actions requises non effectuées)
- **Workflow anormal** (transitions inhabituelles)

---

## 🔧 **Implémentation Technique**

### **⚠️ Script Python à Créer**

**Fichier à créer :** `backend/app/services/etat_chantier_service.py`

**Fonctionnalités requises :**
1. **Changement d'état automatisé** avec vérification des transitions
2. **Génération automatique des tâches récurrentes** depuis `liste_taches`
3. **Filtrage par famille** : `CHANTIER_RECURRENT` + état correspondant
4. **Création des tâches** liées au chantier spécifique
5. **Notifications** aux équipes concernées

**Table de liaison nécessaire :**
```sql
CREATE TABLE etats_taches_recurrentes (
    id INTEGER PRIMARY KEY,
    etat_id INTEGER REFERENCES etats_chantier(id),
    tache_id INTEGER REFERENCES liste_taches(id),
    obligatoire INTEGER DEFAULT 1,
    ordre INTEGER DEFAULT 0
);
```

**Workflow automatique :**
```
Changement d'état → Service Python → Requête liste_taches → Création tâches → Notifications
```

### **Modèle SQLAlchemy Étendu**
```python
class EtatChantier(db.Model):
    __tablename__ = 'etats_chantier'
    
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(30), unique=True, nullable=False)
    couleur = db.Column(db.String(7))  # #RRGGBB
    ordre = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    actif = db.Column(db.Integer, default=1)
    workflow_suivants = db.Column(db.Text)  # JSON
    actions_requises = db.Column(db.Text)  # JSON
    notifications = db.Column(db.Text)  # JSON
    duree_moyenne = db.Column(db.Integer)  # En jours
    date_creation = db.Column(db.String(20))
    date_modification = db.Column(db.String(20))
    
    def get_etats_suivants(self):
        """Retourne la liste des états suivants possibles"""
        import json
        if self.workflow_suivants:
            return json.loads(self.workflow_suivants)
        return []
    
    def get_actions_requises(self):
        """Retourne la liste des actions requises"""
        import json
        if self.actions_requises:
            return json.loads(self.actions_requises)
        return []
```

### **Service de Gestion des États**
```python
class EtatChantierService:
    @staticmethod
    def peut_transitioner(etat_actuel_code, nouvel_etat_code):
        """Vérifie si la transition est autorisée"""
        etat_actuel = EtatChantier.query.filter_by(code=etat_actuel_code).first()
        if not etat_actuel:
            return False
        
        etats_suivants = etat_actuel.get_etats_suivants()
        return nouvel_etat_code in etats_suivants
    
    @staticmethod
    def changer_etat(chantier_id, nouvel_etat_code, user_id):
        """Change l'état d'un chantier avec validation"""
        chantier = Chantier.query.get(chantier_id)
        if not chantier:
            raise ValueError("Chantier introuvable")
        
        if not EtatChantierService.peut_transitioner(
            chantier.etat.code, nouvel_etat_code
        ):
            raise ValueError("Transition non autorisée")
        
        nouvel_etat = EtatChantier.query.filter_by(code=nouvel_etat_code).first()
        chantier.etat_id = nouvel_etat.id
        
        # Historique des changements d'état
        historique = HistoriqueEtatChantier(
            chantier_id=chantier_id,
            ancien_etat_id=chantier.etat_id,
            nouvel_etat_id=nouvel_etat.id,
            user_id=user_id,
            date_changement=datetime.now()
        )
        
        db.session.add(historique)
        db.session.commit()
```

---

## 📋 **Conclusion**

La table `etats_chantier` étendue offre :
- **Flexibilité maximale** pour l'évolution des workflows
- **Gestion métier** complète avec actions et notifications
- **Interface utilisateur** riche et configurable
- **Traçabilité** complète des changements d'état

Cette approche permet d'adapter facilement le workflow aux évolutions des besoins métier sans modification du code source. 