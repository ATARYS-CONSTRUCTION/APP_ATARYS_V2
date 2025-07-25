# 🏗️ STRUCTURE TABLES - SYSTÈME TÂCHES AUTOMATIQUES

> **Structure complète basée sur l'Excel de déclencheurs**  
> **Approche : 2 tables séparées (chantiers + administratif)**  
> Dernière mise à jour : 22/07/2025

---

## 🎯 **PRINCIPE DE FONCTIONNEMENT**

### **Architecture Simple :**
1. **Table des règles** : Configuration des déclencheurs
2. **Table des états** : Référentiel des états de chantiers  
3. **Table chantiers** : Avec état actuel (1 seule clé étrangère)
4. **2 tables de tâches** : Chantiers + Administratif

### **Déclencheurs selon ton Excel :**
- **insertion_salarie** : Nouvelle embauche
- **modification_planning** : Planning modifié
- **changement_etat** : État chantier change

---

## 📋 **STRUCTURE COMPLÈTE DES TABLES**

### **1. Table `etat_chantiers` - Référentiel des états**

```sql
CREATE TABLE etat_chantiers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(20) NOT NULL UNIQUE,           -- 'PROJET', 'SIGNE', 'EN_COURS', 'TERMINE', 'SAV'
    libelle VARCHAR(100) NOT NULL,              -- 'Projet', 'Signé', 'En cours', 'Terminé', 'SAV'
    ordre INTEGER,                              -- 1, 2, 3, 4, 5 (ordre workflow)
    couleur VARCHAR(7),                         -- '#FF0000' pour l'UI
    actif BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Données d'exemple selon ton Excel
INSERT INTO etat_chantiers (code, libelle, ordre) VALUES
('PROJET', 'Projet', 1),
('EN_COURS_SIGNATURE', 'En cours de signature', 2), 
('SIGNE', 'Signé', 3),
('EN_COURS', 'En cours', 4),
('A_FINIR', 'À finir', 5),
('TERMINE', 'Terminé', 6),
('SAV', 'SAV', 7);
```

### **2. Table `regles_automatiques` - Configuration déclencheurs**

```sql
CREATE TABLE regles_automatiques (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_regle VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Type de déclencheur
    type_declencheur VARCHAR(50) NOT NULL,      -- 'changement_etat', 'temporel', 'evenement'
    
    -- Pour changements d'état chantier
    etat_source_id INTEGER,                     -- État avant (peut être NULL pour "création")
    etat_destination_id INTEGER,                -- État après
    
    -- Pour déclencheurs temporels
    regle_temporelle VARCHAR(50),               -- 'fin_mois', 'trimestre', 'annuel'
    jour_mois INTEGER,                          -- Jour du mois (1-31)
    
    -- Pour événements spécifiques  
    evenement_declencheur VARCHAR(50),          -- 'insertion_salarie', 'modification_planning'
    
    -- Configuration tâche à créer
    titre_tache_template VARCHAR(200) NOT NULL, -- 'Faire devis {nom_chantier}'
    description_tache TEXT,
    utilisateur_assigne VARCHAR(50) NOT NULL,   -- 'YANN', 'JULIEN'
    priorite_defaut VARCHAR(10) DEFAULT 'NORMALE',
    delai_jours INTEGER DEFAULT 0,              -- Délai pour échéance
    duree_estimee_minutes INTEGER,              -- Durée estimée
    
    -- Type de tâche générée
    type_tache_generee VARCHAR(20) NOT NULL,    -- 'chantier', 'administratif'
    type_administratif VARCHAR(50),             -- 'COMPTABILITE', 'JURIDIQUE', 'COMMERCIAL'
    
    -- Gestion
    actif BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (etat_source_id) REFERENCES etat_chantiers(id),
    FOREIGN KEY (etat_destination_id) REFERENCES etat_chantiers(id)
);
```

### **3. Table `chantiers` - Chantiers avec état**

```sql
CREATE TABLE chantiers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(200) NOT NULL,
    description TEXT,
    reference VARCHAR(50) UNIQUE,
    
    -- Client
    client_nom VARCHAR(100),
    client_telephone VARCHAR(20),
    client_email VARCHAR(100),
    adresse TEXT,
    
    -- ÉTAT ACTUEL (seule clé étrangère nécessaire)
    etat_id INTEGER NOT NULL,
    
    -- Dates importantes
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_signature DATETIME,
    date_debut DATETIME,
    date_fin_prevue DATETIME,
    date_fin_reelle DATETIME,
    
    -- Informations financières
    montant_ht DECIMAL(10,2),
    montant_ttc DECIMAL(10,2),
    
    -- Métadonnées
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (etat_id) REFERENCES etat_chantiers(id)
);
```

### **4. Table `taches_chantiers` - Tâches liées aux chantiers**

```sql
CREATE TABLE taches_chantiers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Informations de base
    titre VARCHAR(200) NOT NULL,
    description TEXT,
    
    -- Assignation
    utilisateur VARCHAR(50) NOT NULL,           -- 'YANN', 'JULIEN'
    
    -- Gestion
    statut VARCHAR(20) DEFAULT 'A_FAIRE',       -- 'A_FAIRE', 'EN_COURS', 'TERMINE', 'ANNULE'
    priorite VARCHAR(10) DEFAULT 'NORMALE',     -- 'BASSE', 'NORMALE', 'HAUTE', 'URGENTE'
    
    -- Dates
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_echeance DATETIME,
    date_completion DATETIME,
    
    -- Temps
    duree_estimee_minutes INTEGER,
    temps_passe_minutes INTEGER,
    
    -- Automatisation
    auto_generee BOOLEAN DEFAULT 0,
    regle_automatique_id INTEGER,               -- Référence vers règle qui a généré
    declencheur VARCHAR(50),                    -- 'changement_etat_PROJET_to_SIGNE'
    
    -- LIEN CHANTIER (obligatoire)
    chantier_id INTEGER NOT NULL,
    
    -- Métadonnées
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (chantier_id) REFERENCES chantiers(id) ON DELETE CASCADE,
    FOREIGN KEY (regle_automatique_id) REFERENCES regles_automatiques(id)
);
```

### **5. Table `taches_administratives` - Tâches admin**

```sql
CREATE TABLE taches_administratives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Informations de base
    titre VARCHAR(200) NOT NULL,
    description TEXT,
    
    -- Assignation
    utilisateur VARCHAR(50) NOT NULL,           -- 'YANN', 'JULIEN'
    
    -- Gestion
    statut VARCHAR(20) DEFAULT 'A_FAIRE',
    priorite VARCHAR(10) DEFAULT 'NORMALE',
    
    -- Dates
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_echeance DATETIME,
    date_completion DATETIME,
    
    -- Temps
    duree_estimee_minutes INTEGER,
    temps_passe_minutes INTEGER,
    
    -- Automatisation
    auto_generee BOOLEAN DEFAULT 0,
    regle_automatique_id INTEGER,
    declencheur VARCHAR(50),                    -- 'fin_mois', 'insertion_salarie'
    
    -- LIEN CHANTIER (optionnel)
    chantier_id INTEGER,                        -- NULL pour tâches purement admin
    
    -- SPÉCIFIQUE ADMIN
    type_administratif VARCHAR(50) DEFAULT 'GENERAL', -- 'COMPTABILITE', 'JURIDIQUE', 'COMMERCIAL'
    
    -- Métadonnées
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (chantier_id) REFERENCES chantiers(id) ON DELETE SET NULL,
    FOREIGN KEY (regle_automatique_id) REFERENCES regles_automatiques(id)
);
```

---

## 🎯 **EXEMPLES DE RÈGLES (selon ton Excel)**

### **Règles de changement d'état :**

```sql
-- Règle 1 : Création chantier → Tâche "À faire"
INSERT INTO regles_automatiques (
    nom_regle, type_declencheur, etat_destination_id, 
    titre_tache_template, utilisateur_assigne, type_tache_generee
) VALUES (
    'Tâche création chantier', 'changement_etat', 1,
    'Traiter nouveau chantier {nom_chantier}', 'YANN', 'chantier'
);

-- Règle 2 : Projet → Signé = Devis à faire
INSERT INTO regles_automatiques (
    nom_regle, type_declencheur, etat_source_id, etat_destination_id,
    titre_tache_template, utilisateur_assigne, delai_jours, type_tache_generee
) VALUES (
    'Devis après signature', 'changement_etat', 1, 3,
    'Faire devis pour {nom_chantier}', 'JULIEN', 2, 'chantier'
);
```

### **Règles événementielles :**

```sql
-- Règle 3 : Insertion salarié → Tâche admin
INSERT INTO regles_automatiques (
    nom_regle, type_declencheur, evenement_declencheur,
    titre_tache_template, utilisateur_assigne, type_tache_generee, type_administratif
) VALUES (
    'Nouveau salarié', 'evenement', 'insertion_salarie',
    'Finaliser embauche {nom_salarie}', 'JULIEN', 'administratif', 'JURIDIQUE'
);

-- Règle 4 : Modification planning → Tâche admin
INSERT INTO regles_automatiques (
    nom_regle, type_declencheur, evenement_declencheur,
    titre_tache_template, utilisateur_assigne, type_tache_generee, type_administratif
) VALUES (
    'Planning modifié', 'evenement', 'modification_planning',
    'Valider nouveau planning', 'YANN', 'administratif', 'GENERAL'
);
```

### **Règles temporelles :**

```sql
-- Règle 5 : Fin de mois → Déclaration TVA
INSERT INTO regles_automatiques (
    nom_regle, type_declencheur, regle_temporelle, jour_mois,
    titre_tache_template, utilisateur_assigne, type_tache_generee, type_administratif
) VALUES (
    'Déclaration TVA mensuelle', 'temporel', 'fin_mois', 25,
    'Préparer déclaration TVA', 'JULIEN', 'administratif', 'COMPTABILITE'
);
```

---

## 🔧 **LOGIQUE DE FONCTIONNEMENT**

### **Changement d'état chantier :**

```python
def changer_etat_chantier(chantier_id, nouvel_etat_id):
    chantier = Chantier.query.get(chantier_id)
    ancien_etat_id = chantier.etat_id
    
    # Mettre à jour l'état
    chantier.etat_id = nouvel_etat_id
    db.session.commit()
    
    # Chercher les règles applicables
    regles = ReglesAutomatiques.query.filter_by(
        type_declencheur='changement_etat',
        etat_source_id=ancien_etat_id,
        etat_destination_id=nouvel_etat_id,
        actif=True
    ).all()
    
    # Créer les tâches
    for regle in regles:
        if regle.type_tache_generee == 'chantier':
            creer_tache_chantier(regle, chantier)
        else:
            creer_tache_administrative(regle, chantier)
```

### **Création de tâche automatique :**

```python
def creer_tache_chantier(regle, chantier):
    # Remplacer les variables dans le titre
    titre = regle.titre_tache_template.replace('{nom_chantier}', chantier.nom)
    
    # Calculer échéance
    date_echeance = datetime.now() + timedelta(days=regle.delai_jours)
    
    # Créer la tâche
    tache = TachesChantiers(
        titre=titre,
        description=regle.description_tache,
        utilisateur=regle.utilisateur_assigne,
        priorite=regle.priorite_defaut,
        date_echeance=date_echeance,
        duree_estimee_minutes=regle.duree_estimee_minutes,
        chantier_id=chantier.id,
        auto_generee=True,
        regle_automatique_id=regle.id,
        declencheur=f'changement_etat_{ancien_etat_id}_to_{nouvel_etat_id}'
    )
    
    db.session.add(tache)
    db.session.commit()
```

---

## 📊 **AVANTAGES DE CETTE STRUCTURE**

### **Simplicité :**
- **1 seule clé étrangère** par table de tâches
- **Configuration centralisée** dans regles_automatiques
- **Traçabilité complète** des tâches générées

### **Flexibilité :**
- **Nouveaux déclencheurs** sans modification de code
- **Règles temporelles** configurables
- **Types de tâches** extensibles

### **Performance :**
- **Index optimisés** sur les clés étrangères
- **Requêtes simples** pour retrouver les tâches
- **Pas de jointures complexes**

---

**Cette structure respecte exactement ce qu'on a défini et ton Excel de déclencheurs !** 