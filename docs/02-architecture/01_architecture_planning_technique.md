# ATARYS – Proposition technique : Mise en œuvre du module Planning (1.1 & 1.2)

> **Fichier de synthèse technique pour cadrer le développement du module Planning**
> Version initiale – à enrichir selon validation métier et technique

---

## 1. Positionnement dans l’architecture ATARYS
- **Frontend** : React 18.2.0 + Vite + Tailwind CSS (pages : `PlanningSalaries.jsx`, `PlanningChantiers.jsx`, composants réutilisables)
- **Backend** (à créer) : Flask 3.0+ + SQLAlchemy 2.0+ (pattern Factory, REST API)
- **Base de données** : SQLite (dev) → PostgreSQL (prod), modèles SQLAlchemy avec BaseModel
- **API** : REST, format `{success, data, message}`

---

## 2. Modélisation des données (backend à venir)
- **Tables principales** (voir nomenclature dédiée) :
  - `salaries`, `chantiers`, `devis_chantier`, `planning_salaries`, `planning_chantiers`, `absences`, `interventions`, `familles_ouvrage`, `commandes_chantier`, `etats_chantier`, `sav_interventions`, `verrouillages`
- **Règles d’état** (cf. `etats_chantier`) :
  - Planning salariés : chantiers affichés à partir de l’état SIGNATURE, masqués à l’état TERMINE
  - Planning chantiers : chantiers affichés à partir de l’état EN_COURS_SIGNATURE, masqués à l’état TERMINE
- **Calculs backend** :
  - Heures planifiées vs heures réelles (prise en compte du ratio 75%)
  - Dépassements (orange/rouge), calculs SAV, extraction familles d’ouvrage

---

## 3. API REST à prévoir
- **Endpoints principaux** (exemples) :
  - `GET /api/planning-salaries?semaine=YYYY-WW`
  - `POST /api/planning-salaries`
  - `GET /api/planning-chantiers?mois=YYYY-MM`
  - `POST /api/planning-chantiers`
  - `GET /api/chantiers/actifs`
  - `GET /api/salaries`
  - `GET /api/absences` / `POST /api/absences`
  - `POST /api/verrouillage`
  - `POST /api/sav`
  - **+** endpoints pour fractionnement, export, archivage (modules dédiés)
- **Format de réponse** : Toujours `{success, data, message, pagination?}`

---

## 4. Frontend (React) – Structure proposée
- **Pages** :
  - `PlanningSalaries.jsx` (module 1.1)
  - `PlanningChantiers.jsx` (module 1.2)
- **Composants réutilisables** :
  - `PlanningTable`, `PlanningCell`, `PlanningActionsBar`, `PopupInsert`, `PopupFraction`, `PopupVerrouillage`, `PopupSAV`, `AbsenceBadge`, `DepassementIndicator`, `FiltersBar`
- **Hooks personnalisés** :
  - `usePlanningData`, `useAbsences`, `useDepassements`
- **Gestion d’état** : Context API pour menu, sélection, filtres globaux
- **UI/UX** :
  - Respect strict des standards ATARYS (padding, gap, responsive, code couleur)
  - Affichage dynamique selon état du menu, sticky headers, responsive

---

## 5. Spécificité UI/UX : Règles de padding du module Planning
- **Exception planning** : Les composants du planning (tableaux, cellules, actions) utilisent des règles de padding différentes de celles du composant générique `Layout.jsx`.
  - **Objectif** : Maximiser la surface utile, réduire les marges/paddings pour une meilleure lisibilité du planning.
  - **Exemples** :
    - Colonnes et cellules avec padding réduit (`p-2` ou moins)
    - Hauteur de ligne augmentée, date colonne plus étroite
    - Card planning avec padding spécifique (ex : `p-6` ou custom)
  - **À documenter** dans chaque composant concerné pour éviter les régressions lors de refactoring UI.

---

## 6. Logique métier et calculs
- **Dépassements** : Calcul côté backend, affichage couleur côté frontend (orange/rouge)
- **Fractionnement** : Extraction automatique des familles d’ouvrage depuis le devis, limite à 6 interventions (à confirmer)
- **Verrouillage** : Blocage d’une date ou d’un chantier, tout utilisateur peut agir, insertions automatiques respectent les verrous
- **Absences** : Saisie via popup, affichage badge sur la cellule, table dédiée ou champ dans la table planning (à arbitrer)
- **SAV** : Création intervention sur chantier terminé, affectation du coût (SAV ou chantier)

---

## 7. Sécurité et droits
- **Aucune restriction d’accès** (conformément à la règle métier)
- Historique des modifications (à prévoir pour auditabilité, mais non bloquant)

---

## 8. Développement progressif (MVP)
1. **Frontend** : UI avec données statiques (JSON), validation ergonomie et workflows, intégration API progressive
2. **Backend** : Création des modèles SQLAlchemy, endpoints REST, logique métier
3. **Tests** : Unitaires backend, intégration frontend, validation croisée métier

---

## 9. Pourquoi anticiper le backend ?
- Permet de structurer le frontend pour qu’il soit prêt à consommer l’API dès qu’elle sera disponible
- Évite les impasses d’architecture (structure des données, pagination, gestion des états)
- Facilite la collaboration et le découpage des tâches (frontend/backend)
- Garantit la conformité avec la méthodologie ATARYS (documentation, standards, évolutivité)

---

**Ce fichier doit servir de référence technique pour toute l’équipe lors de la conception et du développement du module Planning.** 