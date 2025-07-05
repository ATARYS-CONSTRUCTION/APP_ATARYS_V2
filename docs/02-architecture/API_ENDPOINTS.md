# 🛣️ API Endpoints ATARYS

> **Documentation complète des routes API REST**
> Dernière mise à jour : 04/07/2025

---

## 📋 Vue d'ensemble

**Base URL :** `http://localhost:5000/api`
**Format de réponse :** JSON standardisé `{success, data, message}`

---

## 🏗️ Module 3 - LISTE CHANTIERS

### Chantiers
- `GET /api/chantiers` - Liste des chantiers avec pagination
- `POST /api/chantiers` - Créer un nouveau chantier
- `GET /api/chantiers/<id>` - Détails d'un chantier
- `PUT /api/chantiers/<id>` - Modifier un chantier
- `DELETE /api/chantiers/<id>` - Supprimer un chantier
- `GET /api/chantiers/etat/<etat_id>` - Chantiers par état
- `GET /api/chantiers/search` - Recherche de chantiers

### États Chantier
- `GET /api/etats-chantier` - Liste des états disponibles

---

## 💰 Module 5 - DEVIS-FACTURATION

### Devis
- `GET /api/devis` - Liste des devis
- `POST /api/devis` - Créer un devis
- `GET /api/devis/<id>` - Détails d'un devis
- `PUT /api/devis/<id>` - Modifier un devis
- `DELETE /api/devis/<id>` - Supprimer un devis

### Factures
- `GET /api/factures` - Liste des factures
- `POST /api/factures` - Créer une facture
- `GET /api/factures/<id>` - Détails d'une facture

---

## 📅 Module 1 - PLANNING

### Planning Chantiers
- `GET /api/planning/chantiers` - Planning des chantiers
- `POST /api/planning/chantiers` - Ajouter un chantier au planning
- `GET /api/planning/chantiers/<id>` - Détails planning chantier

### Planning Salariés
- `GET /api/planning/salaries` - Planning des salariés
- `POST /api/planning/salaries` - Ajouter un salarié au planning

---

## 👥 Module 9 - SOCIAL

### Salariés
- `GET /api/salaries` - Liste des salariés
- `POST /api/salaries` - Créer un salarié
- `GET /api/salaries/<id>` - Détails d'un salarié
- `PUT /api/salaries/<id>` - Modifier un salarié
- `DELETE /api/salaries/<id>` - Supprimer un salarié

---

## 🏗️ Module 10 - OUTILS ARDOISES

### Modèles d'📐 Module 10: Outils Ardoises
- `GET /api/ardoises/modeles` - Liste des modèles d'📐 Module 10: Outils Ardoises
- `GET /api/ardoises/modeles/<id>` - Détails d'un modèle
- `GET /api/ardoises/modeles/details` - Détails par nom et recouvrement

### Pentes
- `GET /api/ardoises/pentes` - Liste des pentes disponibles

### Recouvrements
- `GET /api/ardoises/recouvrements` - Recouvrements par zone/pente
- `GET /api/ardoises/recouvrement-calcul` - Calcul de recouvrement

### Calculs
- `POST /api/ardoises/calcul` - Calculer besoins en ardoises
- `GET /api/ardoises/zones` - Zones géographiques
- `GET /api/ardoises/longueurs-rampant` - Longueurs de rampant

### Gestion des Données
- `GET /api/recouvrements/status` - Statut des recouvrements
- `POST /api/recouvrements/restore` - Restaurer recouvrements
- `DELETE /api/recouvrements/clear` - Vider recouvrements
- `GET /api/modeles-ardoise/status` - Statut des modèles
- `POST /api/modeles-ardoise/restore` - Restaurer modèles
- `DELETE /api/modeles-ardoise/clear` - Vider modèles

---

## 🌍 Module 11 - GÉOGRAPHIE

### Villes
- `GET /api/villes` - Liste des villes (avec pagination)
- `GET /api/villes/paginated` - Liste paginée
- `GET /api/villes/<id>` - Détails d'une ville
- `GET /api/villes/commune/<nom>` - Ville par nom
- `GET /api/villes/search` - Recherche autocomplete
- `GET /api/villes/zones` - Liste des zones
- `GET /api/villes/zone/<zone>` - Villes par zone
- `GET /api/villes/communes` - Liste des communes

---

## 🔧 Routes Utilitaires

### Santé
- `GET /health` - Vérification de santé de l'API
- `GET /api/test` - Test de l'API

---

## 📊 Format de Réponse Standard

### Succès
```json
{
  "success": true,
  "data": [...],
  "message": "Opération réussie",
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total": 100,
    "pages": 2,
    "has_next": true,
    "has_prev": false
  }
}
```

### Erreur
```json
{
  "success": false,
  "error": "Message d'erreur détaillé"
}
```

---

## 🔐 Authentification

**Actuellement :** Aucune authentification requise
**Futur :** JWT tokens pour sécurisation

---

## 📝 Notes Techniques

- **Pagination :** Toutes les listes supportent `page` et `per_page`
- **Recherche :** Paramètre `search` pour filtrage textuel
- **Tri :** Ordre par défaut selon la logique métier
- **Validation :** Validation automatique des données d'entrée
- **Logs :** Toutes les requêtes sont loggées

---

## 🚀 Statut des Modules

| Module | Routes | Statut | Endpoints |
|--------|--------|--------|-----------|
| **3.1** | Chantiers | ✅ Actif | 7 endpoints |
| **5.1** | Devis | ✅ Actif | 5 endpoints |
| **5.2** | Factures | ✅ Actif | 3 endpoints |
| **1.1** | Planning | ✅ Actif | 5 endpoints |
| **9.1** | Salariés | ✅ Actif | 5 endpoints |
| **10.1** | Ardoises | ✅ **RÉACTIVÉ** | 12 endpoints |
| **11.1** | Villes | ✅ Actif | 8 endpoints |

**Total :** 45 endpoints API actifs 