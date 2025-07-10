# ATARYS – Architecture du Module Planning (1.1 & 1.2)

> **Document de référence pour la conception, le développement et l’évolution du module Planning**
> 
> Version initiale – à compléter selon retours métier et techniques

---

## 1. Objectif et périmètre
Le module **Planning** d’ATARYS se compose de deux sous-modules :
- **1.1 Planning Salariés** : planification des interventions par salarié, visualisation hebdomadaire/mensuelle, gestion des absences et des dépassements d’heures.
- **1.2 Planning Chantier** : planification des interventions par chantier, visualisation multi-mois, suivi de l’avancement par lot/famille d’ouvrage.

## 2. Structure générale (maquette)
- **Menu latéral** : navigation entre modules ATARYS.
- **En-tête** : titre, filtres dynamiques (chantier, nombre d’heures, nombre de jours).
- **Tableau central** :
  - **Colonnes** : 1 colonne date, colonnes dynamiques pour chaque salarié (1.1) ou chaque chantier (1.2).
  - **Cellules** : chaque cellule = intervention possible (sélection chantier, fractionnement, verrouillage, SAV, etc.).
  - **Ligne d’insertion manuelle** : ajout d’interventions, fractionnement, etc.
- **Barre d’actions** : MAJ HEBDO, SEMAINE, MOIS, INSERER, FRACTIONNER, VERR/DEVERR, SAV.
- **Popups/Modales** : pour chaque action (voir maquettes).

## 3. Lien avec la base de données et autres modules
- **Tables utilisées** :
  - `chantier`, `devis_chantier`, `commande_chantier`, `salaries`, `famille_ouvrage`, `etat_chantier`
- **Lien fort avec le module 3 (Chantiers)** :
  - Les plannings sont alimentés par les données des chantiers et devis (lots/familles d’ouvrage).
  - Les états de chantier (cf. ATARYS_ARCHITECTURE.md et ETATS_CHANTIERS_COMPLETS.md) déterminent l’affichage dans les plannings :
    - **Planning Salariés** : un chantier apparaît à l’état **Signature** et disparaît à l’état **Terminé**.
    - **Planning Chantier** : un chantier apparaît à l’état **En cours de signature** et disparaît à l’état **Terminé**.

## 4. Règles de gestion spécifiques

### A. Règles salariés
- Certains salariés (ex : ITAI) ne travaillent que 4 jours/semaine.
- Certains salariés ne travaillent pas un vendredi sur deux (non bloquant, mais à afficher).
- Ces règles doivent être paramétrables et visibles dans le planning.

### B. Dépassements d’heures
- **Calcul** : journée standard = 7,5h. On considère que 75% des heures vendues sont réellement planifiables (ex : 100h vendues = 133h réelles à planifier).
- **Affichage** :
  - **Orange** : dépassement du temps planifié par rapport au temps réel calculé.
  - **Rouge** : dépassement > 30% du temps réel.
  - Les couleurs doivent rester discrètes.

### C. Fractionnement
- Un devis est organisé en **familles d’ouvrage** (lots), extraites automatiquement.
- On pourra planifier jusqu’à 6 interventions différentes (à confirmer), chaque intervention pouvant regrouper plusieurs familles d’ouvrage.
- Les heures liées à chaque famille d’ouvrage seront extraites et affectées à l’intervention correspondante.

### D. Verrouillage
- Permet de bloquer une intervention sur une date ou un chantier entier.
- Les fonctions d’insertion automatique ne peuvent pas décaler ou écraser les jours bloqués.
- Tout utilisateur peut verrouiller/déverrouiller.

### E. SAV
- Permet de créer une intervention sur un chantier terminé sans le réafficher dans le planning.
- La date d’intervention est saisie dans le formulaire SAV.
- Le coût peut être affecté soit à un budget SAV, soit au chantier (à confirmer).

### F. Absences et jours spéciaux
- Trois catégories de jours à gérer : **CONGES**, **MALADIE**, **ECOLE** (pour apprentis).
- Ces absences doivent être saisissables dans le planning.
- **À préciser :** Faut-il intégrer ces catégories dans la base de données (table dédiée ou champ dans la table planning) ?

### G. Archivage et export
- Les fonctions d’archivage et d’export (Excel, PDF, etc.) sont à prévoir mais seront détaillées dans des modules dédiés.

### H. Sécurité et droits
- **Aucune restriction d’accès** : toutes les fonctions sont accessibles à tous les utilisateurs.

## 5. Fonctionnalités principales (récapitulatif des actions)
- **MAJ HEBDO** : confirmation de la mise à jour du planning.
- **SEMAINE/MOIS** : navigation temporelle.
- **INSERER** : ajout d’une intervention (chantier, dates).
- **FRACTIONNER** : découpage d’un chantier en plusieurs interventions (par lots/familles d’ouvrage).
- **VERROUILLER/DEVERR** : blocage/déblocage d’une date ou d’un chantier.
- **SAV** : création d’une intervention SAV sur un chantier terminé.

## 6. Points à préciser / Questions ouvertes
1. **Absences** : souhaitez-vous une table dédiée pour les absences (congés, maladie, école) ou un champ dans la table planning ?
2. **Fractionnement** : confirmez-vous la limite de 6 interventions maximum par chantier ? Peut-on regrouper librement les familles d’ouvrage dans une intervention ?
3. **SAV** : le coût SAV doit-il être affecté systématiquement à un budget séparé ou parfois au chantier d’origine ?
4. **Export/Archivage** : quels formats d’export sont prioritaires (Excel, PDF, CSV) ?
5. **Règles salariés** : les règles d’exception (ex : vendredi sur deux) doivent-elles être affichées visuellement dans le planning (icône, couleur) ?

## 7. Synthèse visuelle (code couleur maquette)
- **Bleu** : Fonctions frontend (UI, interactions, popups, listes déroulantes, actions).
- **Rouge** : Données issues de la base (tables chantier, devis_chantier, commande_chantier, salariés, familles d’ouvrage).
- **Vert** : Calculs ou scripts backend (calcul des heures, bilans, etc.).

## 8. Conclusion
La maquette et la description permettent de rédiger une documentation structurée et conforme à la méthodologie ATARYS.
**Les points ci-dessus doivent être validés ou précisés pour garantir la cohérence métier et technique.**
Dès validation, la documentation pourra être structurée en sections détaillées (présentation, workflow, règles métier, schémas, exemples d’UI, etc.). 

---

## 9. Annexes visuelles (maquettes)

### Maquette 1 : Planning Salariés – Vue générale
![Planning Salariés – Vue générale](maquettes/planning_salaries_global.png)
*Code couleur : Bleu = fonctions frontend, Rouge = base de données, Vert = scripts backend*

### Maquette 2 : Planning Chantiers – Vue générale
![Planning Chantiers – Vue générale](maquettes/planning_chantiers_global.png)
*Code couleur : Bleu = fonctions frontend, Rouge = base de données, Vert = scripts backend*

### Maquette 3 : Actions et popups (zoom)
![Actions et popups – Planning](maquettes/planning_actions_popups.png)
*Exemples de popups : MAJ HEBDO, INSERER, FRACTIONNER, VERROUILLER, SAV*

### Maquette 4 : En-tête et filtres (zoom)
![En-tête et filtres – Planning](maquettes/planning_entete_filtres.png)
*Affichage dynamique des filtres, listes déroulantes intelligentes*

> **Remarque :** Les images doivent être placées dans le dossier `docs/maquettes/`. Adapter les chemins si besoin. 