# ATARYS V2 - Gestion d'Entreprise

> **Application web complète de gestion d'entreprise du BTP**  
> Automatisation des processus, planning intelligent et gestion des chantiers

## 🎯 Objectifs

- **Automatiser** les tâches informatiques récurrentes et indispensables
- **Remplacer** tous les fichiers Excel par une application qui archive, calcule et organise
- **Créer** des processus de travail efficaces et ludiques
- **Organiser** le travail du bureau en binôme
- **Améliorer** la rentabilité par une meilleure organisation

## 🏗️ Architecture

### Stack Technologique

**Frontend :**
- React 18.2.0 + Vite 5.1.0
- Tailwind CSS 3.4.1
- React Router DOM 6.22.0
- Axios 1.6.7

**Backend :**
- Flask 2.3.3 + SQLAlchemy 2.0.23
- Base de données SQLite (dev) / PostgreSQL (prod)
- API REST avec format JSON standardisé
- Flask-CORS pour l'intégration frontend

### Structure du Projet

```
ATARYS V2/
├── frontend/           # Application React
│   ├── src/
│   │   ├── pages/      # Pages par module (1.1, 3.1, etc.)
│   │   ├── components/ # Composants réutilisables
│   │   ├── contexts/   # Context API
│   │   └── api/        # Services API
│   └── package.json
├── backend/            # API Flask
│   ├── app/
│   │   ├── models/     # Modèles SQLAlchemy
│   │   ├── routes/     # Endpoints API
│   │   ├── services/   # Logique métier
│   │   └── config/     # Configuration
│   └── requirements.txt
├── data/               # Base de données SQLite
├── docs/               # Documentation complète
└── .bat/               # Scripts PowerShell
```

## 📋 Modules ATARYS

### ✅ Modules Disponibles

1. **PLANNING** → 1.1 Salariés, 1.2 Chantiers
2. **LISTE DES TÂCHES** → 2.1 Yann, 2.2 Julien
3. **LISTE CHANTIERS** → 3.1 Liste, 3.2 Projets, 3.3 Signés, 3.4 En cours, 3.5 Archives
4. **CHANTIERS** → 4.1 Suivi, 4.2 Notes, 4.3 Commandes, 4.4 Documents
5. **DEVIS-FACTURATION** → 5.1 BATAPPLI, 5.2 Fiche Mètres, 5.3 MEXT, 5.4 Type
6. **ATELIER** → 6.1-6.5 Quincaillerie, Consommables, Camion, Matériel, Échafaudage
7. **GESTION** → 7.1-7.3 Prévisionnel, Synthèse, Bilans
8. **COMPTABILITÉ** → 8.1-8.2 TVA, Tableau de bord
9. **SOCIAL** → 9.1-9.3 Salariés, Fiche mensuelle, Récap
10. **OUTILS** → 10.1-10.5 Ardoises, Structures, Staravina, Domaine, Documents
11. **GÉOGRAPHIE** → 11.1 Villes et communes
12. **PARAMÈTRES** → Configuration système
13. **AIDE** → Nomenclature + Documentation

## 🚀 Installation

### Prérequis

**Langages et Runtime :**
- Node.js 18+ et npm
- Python 3.9+
- Git

**Outils Externes :**
- rclone v1.70.3+ (synchronisation fichiers) - Emplacement : `C:\DEV\ATARYS_TOOLS\rclone.exe`

### Installation Frontend

```powershell
cd frontend
npm install
npm run dev
```

### Installation Backend

```powershell
cd backend
pip install -r requirements.txt
python run.py
```

## 🔧 Développement

### URLs de Développement

- **Frontend React** : http://localhost:3001
- **Backend Flask** : http://localhost:5000
- **API** : http://localhost:5000/api

### Commandes Utiles

```powershell
# Démarrer le frontend
cd frontend
npm run dev

# Démarrer le backend
cd backend
python run.py

# Tests
cd backend
pytest

# Linter
cd frontend
npm run lint
```

## 📊 Base de Données

### Structure

- **13 tables principales** avec relations
- **SQLAlchemy ORM** pour l'abstraction
- **Migrations** automatiques avec Flask-Migrate
- **Données de référence** : villes, modèles ardoises, etc.

### Modèles Principaux

- `Chantier` : Projets et clients
- `Salarie` : Employés et planning
- `Devis` : Devis et facturation
- `Planning` : Planning général
- `Ville` : Géographie et zones
- `ModeleArdoise` : Calculs techniques

## 🛣️ API

### Format de Réponse Standard

```json
{
  "success": true,
  "data": [...],
  "message": "Opération réussie",
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total": 100,
    "has_next": true
  }
}
```

### Endpoints Principaux

- `GET /api/chantiers` - Liste des chantiers
- `GET /api/salaries` - Liste des salariés
- `GET /api/planning/salaries` - Planning salariés
- `GET /api/ardoises/calcul` - Calcul ardoises
- `GET /api/villes` - Villes et communes

## 📚 Documentation

La documentation complète est disponible dans le dossier `docs/` :

- **Architecture** : Structure technique et modèles
- **API** : Endpoints et formats
- **Guides** : Développement et déploiement
- **Standards** : Conventions et règles

## 🔐 Sécurité

- Validation des données d'entrée
- Gestion des erreurs centralisée
- Logs détaillés pour debugging
- CORS configuré pour le développement

## 🚀 Déploiement

### Environnement de Production

- Base de données PostgreSQL
- Serveur WSGI (Gunicorn)
- Reverse proxy (Nginx)
- SSL/TLS

## 📞 Support

Pour toute question ou problème :

1. Consulter la documentation dans `docs/`
2. Vérifier les logs dans `logs/atarys.log`
3. Utiliser les outils de debug intégrés

## 📄 Licence

Propriétaire - Tous droits réservés

---

**ATARYS V2** - Version 2.0.0 - Développé avec ❤️ pour l'automatisation du BTP 