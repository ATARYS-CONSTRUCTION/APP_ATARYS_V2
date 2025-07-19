# ATARYS – Nomenclature des tables du module Planning (1.1 & 1.2)

> **Fichier de référence pour la structuration technique du module Planning**
> À valider et compléter avant toute implémentation

---

## 1. Principes de nommage
- **snake_case** pour toutes les tables backend
- **Nom explicite, pluriel, sans majuscules ni accents**
- **Tables de liaison** : nom1_nom2 (ex : etats_taches_recurrentes)

---

## 2. Synthèse des tables nécessaires (planning et dépendances)

| Usage métier                  | Nom pressenti              | Statut dans la doc      | Remarques principales |
|-------------------------------|----------------------------|-------------------------|----------------------|
| Chantiers                     | chantiers                  | FORMALISÉ               | Table centrale, module 3.1 |
| Devis liés à chantier         | devis_chantier             | FORMALISÉ               | Liée à chantiers, familles d'ouvrage |
| Salariés                      | salaries                   | FORMALISÉ               | Module 9.1 |
| États de chantier             | etats_chantier             | FORMALISÉ               | Workflow, statuts |
| Affectation planning salariés | planning_salaries           | À FORMALISER            | Affectation par jour/salarié/intervention |
| Affectation planning chantier | planning_chantiers          | À FORMALISER            | Affectation par jour/chantier/intervention |
| Absences                      | absences                   | À FORMALISER            | Gestion congés, maladie, école |
| Interventions (ligne planning)| interventions              | À FORMALISER            | Détail d'une affectation planning |
| Familles d’ouvrage            | familles_ouvrage           | À FORMALISER            | Extraction automatique depuis devis |
| Commandes chantier            | commandes_chantier         | FORMALISÉ               | Gestion commandes liées au chantier |
| SAV                           | sav_interventions (ou sav) | À FORMALISER            | Interventions SAV sur chantiers terminés |
| Verrouillages                 | verrouillages              | À FORMALISER            | Blocage dates/interventions |

---

## 3. Prochaines étapes
- **Valider** cette liste avec l'équipe projet
- **Définir** pour chaque table : usage précis, champs principaux, liens (FK)
- **Documenter** la structure minimale de chaque table avant toute implémentation

---

**Ce fichier doit être mis à jour à chaque évolution de la nomenclature ou du périmètre du module Planning.** 

---

### **Commande SQL à exécuter dans un client SQLite (sqlite3, DB Browser, etc.)**

```sql
.tables
```
ou, pour un résultat sous forme de liste :

```sql
<code_block_to_apply_changes_from>
```

---

### **Exemple de commande en ligne de commande (Windows : PowerShell ou CMD)**

```powershell
sqlite3 "C:\DEV\APP_ATARYS V2\0 APP ATARYS - Copie\data\atarys_data.db" ".tables"
```
ou pour un export dans un fichier texte :

```powershell
sqlite3 "C:\DEV\APP_ATARYS V2\0 APP ATARYS - Copie\data\atarys_data.db" "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;" > tables_v1.txt
```

---

### **À faire :**
1. Ouvrez un terminal ou DB Browser for SQLite.
2. Exécutez l’une des commandes ci-dessus.
3. Vous obtiendrez la liste exhaustive de toutes les tables présentes dans la base V1.

---

**Si vous souhaitez que je vous aide à interpréter ou à croiser cette liste avec la nomenclature V2, copiez-collez ici le résultat obtenu.**