# [DOC] Ajout workflow standard et règles robustes pour la création d’API REST ATARYS

## Objectif
Renforcer la cohérence, la robustesse et la maintenabilité des APIs ATARYS en documentant un workflow standardisé, une checklist de validation, et des règles Cursor strictes pour toute nouvelle route/backend.

---

## Modifications apportées
- **docs/03-regles-standards/WORKFLOWS.md**
  - Ajout d’un workflow détaillé pour la création d’API REST (modèle, schéma Marshmallow, blueprint, enregistrement, CORS, requirements, test, documentation).
  - Ajout d’une checklist rapide à cocher pour chaque nouvelle route.
- **docs/02-architecture/API_ENDPOINTS.md**
  - Ajout d’un modèle de documentation pour chaque nouvel endpoint API (nom du blueprint, URL, méthodes, payload, format de réponse, pagination, schéma Marshmallow utilisé).
- **.cursorrules**
  - Ajout d’un bloc “Règles ATARYS pour la création de routes/API” : ce qu’il faut TOUJOURS faire et ce qu’il ne faut JAMAIS faire.

---

## Exemple d’utilisation
Pour chaque nouvelle API :
- Suivre le workflow (modèle → schéma → blueprint → enregistrement → CORS → requirements → test → doc)
- Cocher la checklist
- Documenter l’endpoint selon le modèle fourni
- Respecter les règles Cursor (validation, CORS, test direct, etc.)

---

## Bénéfices
- Moins d’erreurs de setup (CORS, dépendances, blueprint, etc.)
- Plus de cohérence et de robustesse pour chaque nouvelle API
- Documentation et règles Cursor à jour pour tous les développeurs

---

## Checklist PR
- [x] Documentation technique à jour
- [x] Règles Cursor enrichies
- [x] Modèle de doc API prêt à l’emploi
- [x] Workflow et checklist validés

---

**À merger pour garantir la qualité et la cohérence des développements backend ATARYS !** 