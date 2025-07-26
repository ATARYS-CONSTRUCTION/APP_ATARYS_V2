# 🛣️ API Endpoints ATARYS V2

> **Spécifications techniques des routes API REST**  
> **VERSION 2** : Backend Flask + SQLAlchemy opérationnel  
> Dernière mise à jour : 05/07/2025

---

## 📋 Vue d'ensemble

**Base URL :** `http://localhost:5000/api` (OPÉRATIONNEL)
**Format de réponse :** JSON standardisé `{success, data, message}`
**Stack Backend :** Flask 3.x + SQLAlchemy 2.0+ + SQLite
**Organisation :** APIs structurées par modules ATARYS prioritaires

---

## 🏗️ Stack Technique Backend

### **Framework et ORM**
```python
# Flask Factory Pattern - OPÉRATIONNEL
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Configuration base de données
    db_uri = 'sqlite:///../../data/atarys_data.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialisation extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)  # Communication frontend-backend
    
    return app
```

### **Pattern BaseModel Standard**
```python
# backend/app/models/base.py - OPÉRATIONNEL
class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
```

---

## ✅ **APIs Implémentées**

### **Module 5.1 - Articles ATARYS** (OPÉRATIONNEL)

#### **Base URL :** `/api/articles-atarys/`

#### **1. GET - Récupération des Articles**
```http
GET /api/articles-atarys/?per_page=all
```

**Réponse :**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "reference": "ART001",
      "libelle": "Article exemple",
      "prix_achat": "10.50",
      "coefficient": "1.20",
      "prix_unitaire": "12.60",
      "unite": "U",
      "tva_pct": "20.00",
      "famille": "Général",
      "actif": true,
      "date_import": "2025-07-05",
      "date_maj": "2025-07-05",
      "created_at": "2025-07-05T10:00:00Z",
      "updated_at": "2025-07-05T10:00:00Z"
    }
  ],
  "message": "Liste complète des articles ATARYS (176)",
  "pagination": {
    "page": 1,
    "per_page": 176,
    "total": 176,
    "has_next": false
  }
}
```

#### **2. POST - Création/Mise à jour (UPSERT)**
```http
POST /api/articles-atarys/
Content-Type: application/json

{
  "reference": "ART002",
  "libelle": "Nouvel article",
  "prix_achat": "15.00",
  "coefficient": "1.15",
  "prix_unitaire": "17.25",
  "unite": "U",
  "tva_pct": "20.00",
  "famille": "Général",
  "actif": true
}
```

**Logique UPSERT :**
- Si référence existe → Mise à jour
- Si référence n'existe pas → Création
- Dates automatiques si absentes

#### **3. PUT - Modification par ID**
```http
PUT /api/articles-atarys/1
Content-Type: application/json

{
  "libelle": "Article modifié",
  "prix_unitaire": "18.00"
}
```

#### **4. DELETE - Suppression par ID**
```http
DELETE /api/articles-atarys/1
```

#### **5. DELETE - Suppression de toutes les données**
```http
DELETE /api/articles-atarys/clear/
```

### **Module 12.1 - Création Dynamique de Tables** (OPÉRATIONNEL)

#### **Base URL :** `/api/create-table/`

#### **POST - Création de Table**
```http
POST /api/create-table/
Content-Type: application/json

{
  "tableData": {
    "moduleId": 12,
    "className": "ExampleModel",
    "tableName": "example_table",
    "columns": [
      {
        "name": "nom",
        "type": "String",
        "nullable": false,
        "maxLength": "100"
      },
      {
        "name": "prix_ht",
        "type": "Numeric",
        "nullable": true,
        "default": "0.00"
      }
    ]
  },
  "code": "from .base import BaseModel\nfrom app import db\n\nclass ExampleModel(BaseModel):\n    __tablename__ = 'example_table'\n    \n    id = db.Column(db.Integer, primary_key=True, autoincrement=True)\n    nom = db.Column(db.String(100), nullable=False)\n    prix_ht = db.Column(db.Numeric(10, 2), default=0.00)\n"
}
```

**Actions automatiques :**
1. Validation des données
2. Création du fichier modèle
3. Création de la table SQLite
4. Intégration dans l’API REST

---

## 🎯 **Modules Prioritaires à Implémenter**

### **Module 3.1 - LISTE CHANTIERS** (PRIORITÉ 1)
**Objectif :** Remplacer "LISTE DES TACHES" + "Liste_Chantiers" Excel
**Modèles :** À créer selon `DATABASE_SCHEMA.md`
**Relations :** À définir lors de la création des modèles

```python
# Endpoints Module 3.1 (à créer)
GET    /api/chantiers                 # Liste paginée
POST   /api/chantiers                 # Créer chantier
GET    /api/chantiers/<id>            # Détails chantier
PUT    /api/chantiers/<id>            # Modifier chantier
DELETE /api/chantiers/<id>            # Supprimer chantier
GET    /api/chantiers/search          # Recherche textuelle
```

### **Module 9.1 - LISTE SALARIÉS** (PRIORITÉ 2)
**Objectif :** Gestion des salariés de l'entreprise
**Modèles :** À créer selon `DATABASE_SCHEMA.md`
**Relations :** À définir lors de la création des modèles

```python
# Endpoints Module 9.1 (à créer)
GET    /api/salaries          # Liste des salariés
POST   /api/salaries          # Créer salarié
GET    /api/salaries/<id>     # Détails salarié
PUT    /api/salaries/<id>     # Modifier salarié
DELETE /api/salaries/<id>     # Supprimer salarié
```

#### **📁 Gestion des Fichiers (IMPLÉMENTÉ 2025)**

#### **POST `/api/open-explorer`** ✅ MODIFIÉ 2025
**Description** : Ouvre un dossier OneDrive (avec redirection Hostinger)
**Corps** :
```json
{
  "path": "./OneDrive/Administration/Volet social/0-Dossier salarié/Nom_Prenom"
}
```

**Logique 2025 (Architecture Hybride) :**
```python
1. Vérifier si chemin synchronisé sur Hostinger
2. SI OUI → Générer URL Hostinger File Manager → Ouvrir navigateur
3. SI NON → Résoudre chemin OneDrive local → Ouvrir explorateur
4. Retourner statut + location (hostinger|local)
```

**Réponse Hostinger** :
```json
{
  "success": true,
  "message": "Dossier ouvert sur Hostinger File Manager",
  "hostinger_url": "https://hpanel.hostinger.com/file-manager?path=...",
  "relative_path": "./OneDrive/Administration/...",
  "location": "hostinger"
}
```

**Réponse Fallback OneDrive** :
```json
{
  "success": true,
  "message": "Explorateur Windows ouvert: C:\\Users\\...",
  "resolved_path": "C:\\Users\\Dell15\\OneDrive\\...",
  "relative_path": "./OneDrive/Administration/...",
  "location": "local"
}
```

#### **POST `/api/test-hostinger-mapping`** 🆕 NOUVEAU 2025
**Description** : Teste le mapping OneDrive → Hostinger
**Corps** :
```json
{
  "path": "./OneDrive/Administration/Dossier"
}
```

**Réponse** :
```json
{
  "success": true,
  "mapping_info": {
    "onedrive_path": "./OneDrive/Administration/Dossier",
    "is_on_hostinger": true,
    "hostinger_url": "https://hpanel.hostinger.com/file-manager?path=...",
    "hostinger_path": "/home/atarys/Administration/Dossier",
    "synchronized_folders": ["Administration", "Chantiers", ...]
  }
}
```

### **Module 10.1 - CALCUL ARDOISES** (PRIORITÉ 3)
**Objectif :** Calculateur d'ardoises selon zones climatiques
**Modèles :** À créer selon `DATABASE_SCHEMA.md`
**Relations :** À définir lors de la création des modèles

```python
# Endpoints Module 10.1 (à créer)
GET    /api/ardoises/modeles           # Modèles d'ardoises
GET    /api/ardoises/modeles/<id>      # Détails modèle
POST   /api/ardoises/calcul            # Calculer besoins
GET    /api/ardoises/zones             # Zones climatiques
```

---

## 📊 Format de Réponse Standard

### **Succès avec données**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nom": "Exemple d'enregistrement",
      "description": "Description de l'élément",
      "created_at": "2025-07-05T10:00:00Z",
      "updated_at": "2025-07-05T10:00:00Z"
    }
  ],
  "message": "Données récupérées avec succès",
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total": 25,
    "pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

### **Erreur**
```json
{
  "success": false,
  "error": "Ressource non trouvée",
  "code": 404
}
```

---

## 🔧 Spécifications Techniques

### **Validation Marshmallow** (OPÉRATIONNEL)
```python
# Exemple pour articles_atarys
class ArticlesAtarysSchema(Schema):
    id = fields.Int(dump_only=True)
    reference = fields.Str(required=True, validate=validate.Length(max=100))
    libelle = fields.Str(required=True)
    prix_achat = fields.Decimal(as_string=True)
    coefficient = fields.Decimal(as_string=True)
    prix_unitaire = fields.Decimal(as_string=True)
    unite = fields.Str(validate=validate.Length(max=20))
    tva_pct = fields.Decimal(as_string=True)
    famille = fields.Str(validate=validate.Length(max=30))
    actif = fields.Bool()
    date_import = fields.Date()
    date_maj = fields.Date()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
```

### **Pagination Intelligente**
```python
# Support pour 'all' et pagination normale
per_page = request.args.get('per_page', 'all')

if per_page == 'all':
    # Récupérer toutes les données
    items = query.order_by(Model.id.desc()).all()
else:
    # Pagination normale
    per_page = int(per_page)
    items = query.paginate(page=page, per_page=per_page, error_out=False)
```

### **Gestion des Erreurs**
```python
# Middleware centralisé
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Ressource non trouvée",
        "code": 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({
        "success": False,
        "error": "Erreur interne du serveur",
        "code": 500
    }), 500
```

### **CORS Configuration**
```python
# Communication frontend-backend
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Autorise toutes les origines en développement
```

---

## 🚀 **Métriques et Performance**

### **APIs Opérationnelles**
- **Articles ATARYS** : 176 lignes, < 100ms response time
- **Création Tables** : Génération automatique, intégration immédiate
- **Validation** : Marshmallow pour intégrité des données
- **CORS** : Configuré pour communication frontend-backend

### **Standards de Performance**
- **Response time** : < 2s pour toutes les APIs
- **Validation** : Marshmallow pour intégrité
- **Rollback** : En cas d'erreur SQLAlchemy
- **Logging** : Logs structurés pour debugging

---

## 📚 **Documentation Associée**

### **Architecture**
- **[ATARYS_ARCHITECTURE.md](ATARYS_ARCHITECTURE.md)** - Architecture complète V2
- **[DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)** - Schéma base de données
- **[ATARYS_MODULES.md](ATARYS_MODULES.md)** - Organisation modulaire

### **Développement**
- **[WORKFLOWS.md](../03-regles-standards/WORKFLOWS.md)** - Processus de développement
- **[STANDARDS_DEV.md](../03-regles-standards/STANDARDS_DEV.md)** - Standards techniques

---

## 🤖 APIs d'Intégration n8n/IA

> **Architecture complète :** Voir [ATARYS_ARCHITECTURE.md](ATARYS_ARCHITECTURE.md#intégration-n8n--agent-ia--atarys)  
> **Workflows d'intégration :** Voir [WORKFLOWS.md](../../03-regles-standards/WORKFLOWS.md#workflows-dintégration-externe)

### **Réception des Workflows n8n**

#### **Webhook Principal n8n → ATARYS**
```http
POST /api/integration/n8n-webhook
Content-Type: application/json
X-Signature-256: sha256=signature_hmac

{
  "workflow_info": {
    "id": "8.1",
    "name": "extraction_tva",
    "timestamp": "2025-01-20T10:30:00Z"
  },
  "source_document": {
    "filename": "facture_mbr_ca000190.pdf",
    "file_hash": "sha256_hash"
  },
  "extraction_result": {
    "numero_facture": "CA000190",
    "fournisseur": "MBR",
    "total_ht": 6984.74,
    "bons_livraison": [...]
  }
}
```

**Réponse :**
```json
{
  "success": true,
  "data": {
    "extraction_id": 123,
    "facture_id": 456,
    "nb_bons": 3,
    "needs_validation": true
  },
  "message": "Extraction intégrée avec succès"
}
```

### **APIs pour n8n (Accès BDD)**

#### **Chantiers Actifs**
```http
GET /api/n8n/chantiers-actifs
Authorization: Bearer n8n_api_key
```

**Réponse :**
```json
{
  "success": true,
  "data": [
    {
      "id": 125,
      "nom": "Maison DEBOIS rue des Lilas",
      "client": "M. DEBOIS",
      "mots_cles": ["DEBOIS", "190DEBOIS", "MO/190DEBOIS"]
    }
  ]
}
```

#### **Matching Intelligent**
```http
GET /api/n8n/matching-chantier?reference=DEBOIS&montant=1000
Authorization: Bearer n8n_api_key
```

**Réponse :**
```json
{
  "success": true,
  "data": {
    "chantier_principal": {
      "id": 125,
      "nom": "Maison DEBOIS rue des Lilas",
      "confidence": 0.98,
      "raison": "Correspondance exacte 'DEBOIS'"
    },
    "alternatives": [
      {
        "id": 89,
        "nom": "Extension DEBOIS annexe",
        "confidence": 0.65
      }
    ]
  }
}
```

### **Gestion des Extractions**

#### **Extractions en Attente de Validation**
```http
GET /api/extractions/pending
```

**Réponse :**
```json
{
  "success": true,
  "data": [
    {
      "id": 123,
      "nom_fichier": "facture_mbr_ca000190.pdf",
      "statut": "SUCCES",
      "confidence_globale": 0.95,
      "nb_factures": 1,
      "nb_bons": 3,
      "created_at": "2025-01-20T10:30:00Z"
    }
  ],
  "message": "2 extractions à valider"
}
```

#### **Validation Extraction**
```http
POST /api/extractions/123/validate
Content-Type: application/json

{
  "corrections": {
    "factures": {
      "456": {
        "fournisseur": "MBR CORRECTED",
        "total_ht": 7000.00
      }
    }
  },
  "commentaire": "Correction montant facture"
}
```

#### **Affectation Bon → Chantier**
```http
POST /api/bons/789/affecter-chantier
Content-Type: application/json

{
  "chantier_id": 125,
  "type_affectation": "CHANTIER",
  "commentaire": "Matériaux charpente"
}
```

### **Agent IA Orchestrateur**

#### **Analyse Document**
```http
POST /api/ai-orchestrator/analyze-document
Content-Type: multipart/form-data

file: [PDF binaire]
```

**Réponse :**
```json
{
  "success": true,
  "data": {
    "document_type": "facture_fournisseur",
    "workflow_recommande": "8.1",
    "confidence": 0.92,
    "n8n_execution_id": "exec_123456"
  },
  "message": "Document analysé, workflow 8.1 déclenché"
}
```

#### **Workflows Disponibles**
```http
GET /api/ai-orchestrator/workflows-available
```

**Réponse :**
```json
{
  "success": true,
  "data": [
    {
      "id": "8.1",
      "name": "extraction_tva",
      "description": "Extraction factures/LCR avec bons de livraison",
      "types_documents": ["facture_fournisseur", "lcr"],
      "status": "ACTIVE"
    },
    {
      "id": "8.2", 
      "name": "extraction_devis",
      "description": "Extraction devis clients",
      "types_documents": ["devis_client"],
      "status": "DEVELOPMENT"
    }
  ]
}
```

### **Métriques et Monitoring**

#### **Statistiques d'Extraction**
```http
GET /api/integration/stats?periode=30
```

**Réponse :**
```json
{
  "success": true,
  "data": {
    "extractions": {
      "total": 245,
      "succes": 235,
      "erreurs": 10,
      "taux_succes": 95.9
    },
    "ia_matching": {
      "precision": 87.5,
      "suggestions_acceptees": 203,
      "corrections_utilisateur": 42
    },
    "temps_moyen": {
      "extraction_n8n": 2.3,
      "validation_utilisateur": 4.1
    }
  }
}
```

#### **Statut des Services**
```http
GET /api/integration/health
```

**Réponse :**
```json
{
  "success": true,
  "data": {
    "n8n_service": {
      "status": "UP",
      "last_check": "2025-01-20T10:35:00Z",
      "response_time_ms": 150
    },
    "ai_service": {
      "status": "UP", 
      "model_version": "claude-sonnet-4",
      "requests_today": 1240
    },
    "database": {
      "status": "UP",
      "connections_active": 5,
      "query_avg_ms": 25
    }
  }
}
```

### **Sécurité et Authentification**

#### **Headers Obligatoires**
```http
# Pour n8n
Authorization: Bearer n8n_api_key_from_env
X-Signature-256: sha256=hmac_signature

# Pour agent IA
Authorization: Bearer ai_service_token
X-Request-ID: uuid_unique
```

#### **Rate Limits**
- **n8n webhooks** : 60 requêtes/minute
- **APIs de consultation** : 100 requêtes/minute  
- **Agent IA** : 30 requêtes/minute
- **Validation/Affectation** : 200 requêtes/minute

### **Codes d'Erreur Spécifiques**

```json
{
  "success": false,
  "error": "INVALID_WORKFLOW_DATA",
  "code": 4001,
  "message": "Données workflow n8n invalides",
  "details": {
    "missing_fields": ["workflow_info.id"],
    "invalid_fields": ["extraction_result.total_ht"]
  }
}
```

**Codes d'erreur :**
- `4001` : Données workflow invalides
- `4002` : Signature webhook incorrecte
- `4003` : Document non supporté
- `4004` : Chantier introuvable pour affectation
- `5001` : Service n8n indisponible
- `5002` : Service IA temporairement surchargé

---

**✅ APIs ATARYS V2 - Backend opérationnel avec intégration intelligente n8n/IA !** 