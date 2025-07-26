# 🚀 Template n8n pour Extraction ATARYS V2

## 📋 Vue d'ensemble

Ce template montre le **format de sortie standard** pour intégrer des données extraites depuis Excel/PDF vers l'API ATARYS V2 via n8n.

### 📁 Fichiers inclus
- `template-extraction-atarys.json` : Workflow n8n importable
- `README-Template-ATARYS.md` : Cette documentation

## 🎯 Modules supportés

### ✅ Module 5 - Articles ATARYS (OPÉRATIONNEL)
- **Table** : `articles_atarys` (176 lignes existantes)
- **Endpoint** : `POST /api/articles-atarys/bulk-import`
- **Usage** : Import devis, facturation, catalogue produits

### ⚠️ Module 3 - Chantiers (À CRÉER)
- **Table** : `chantiers` (à développer)
- **Endpoint** : `POST /api/chantiers/bulk-import` (à créer)
- **Usage** : Import données chantiers depuis Excel

### ⚠️ Module 9 - Salariés (PARTIEL)
- **Table** : `salaries` (structure existante, données partielles)
- **Endpoint** : `POST /api/salaries/bulk-import` (à créer)
- **Usage** : Import données RH

## 📊 Format de sortie JSON standard

### Structure obligatoire

```json
{
  "workflow_info": {
    "source_file": "nom_fichier.xlsx",
    "extraction_date": "2025-01-25T10:30:00Z",
    "workflow_name": "extraction_articles_atarys",
    "module_atarys": 5,
    "table_target": "articles_atarys"
  },
  "data": [
    {
      "reference": "ARD-001",
      "libelle": "Ardoise de couverture 32x22cm",
      "prix_achat": "1.25",
      "coefficient": "2.5", 
      "prix_unitaire": "3.13",
      "unite": "unité",
      "tva_pct": "20.00",
      "famille": "COUVERTURE",
      "actif": true,
      "date_import": "2025-01-25",
      "date_maj": "2025-01-25"
    }
  ],
  "validation": {
    "total_records": 1,
    "valid_records": 1,
    "errors": [],
    "api_endpoint": "/api/articles-atarys/bulk-import",
    "format_version": "2.0"
  }
}
```

## 🔧 Standards techniques ATARYS

### 💰 Montants financiers
- **Format** : String `"1234.56"`
- **Conversion API** : `Numeric(10, 2)`
- **Validation** : 2 décimales maximum

### 📅 Dates
- **Format** : `"YYYY-MM-DD"`
- **Standard** : ISO 8601
- **Exemple** : `"2025-01-25"`

### 🔤 Textes
- **Courts** : `String(longueur_max)`
- **Longs** : `Text` (descriptions)
- **Encodage** : UTF-8

### ✅ Booléens
- **Format** : `true`/`false` (JSON natif)
- **Conversion** : `Boolean` SQLite

## 📋 Prérequis pour utilisation

### 🗄️ Base de données ATARYS
- **Fichier** : `data/atarys_data.db`
- **Tables existantes** : `articles_atarys`, `villes`, `niveau_qualification`
- **Architecture** : BaseModel pattern obligatoire

### 🚀 API ATARYS en fonctionnement
```bash
# Lancer le backend ATARYS
cd backend
python run.py
# → Backend disponible sur http://localhost:5000
```

### 📡 Endpoints nécessaires

#### ✅ Existant - Module 5
```http
POST /api/articles-atarys/bulk-import
Content-Type: application/json
{
  "workflow_info": {...},
  "data": [...],
  "validation": {...}
}
```

#### ⚠️ À créer - Module 3 & 9
```http
POST /api/chantiers/bulk-import
POST /api/salaries/bulk-import
```

## 🛠️ Installation et utilisation

### 1. Importer dans n8n
```bash
# Dans l'interface n8n
Settings → Import workflow → Sélectionner template-extraction-atarys.json
```

### 2. Configuration initiale
- **URL API** : Modifier `http://localhost:5000` selon votre setup
- **Authentification** : Ajouter headers si nécessaire
- **Endpoints** : Vérifier que les routes existent

### 3. Test avec Module 5 (Articles ATARYS)
```javascript
// Format de test pour articles existants
{
  "workflow_info": {
    "source_file": "test.xlsx",
    "module_atarys": 5,
    "table_target": "articles_atarys"
  },
  "data": [
    {
      "reference": "TEST-001",
      "libelle": "Article de test",
      "prix_unitaire": "10.50",
      "unite": "unité",
      "tva_pct": "20.00",
      "date_import": "2025-01-25",
      "date_maj": "2025-01-25"
    }
  ]
}
```

## 🎯 Développement requis côté ATARYS

### 📡 Endpoints bulk-import à créer

```python
# backend/app/routes/module_5.py (exemple)
@articles_bp.route('/api/articles-atarys/bulk-import', methods=['POST'])
def bulk_import_articles():
    """Import en lot depuis n8n"""
    data = request.get_json()
    
    # Validation format n8n
    if not validate_n8n_format(data):
        return {"success": False, "message": "Format n8n invalide"}, 400
    
    # Import des données
    results = []
    errors = []
    
    for item in data['data']:
        try:
            # Validation et conversion des types
            article = articlesatarys(
                reference=item['reference'],
                libelle=item['libelle'],
                prix_achat=Decimal(item.get('prix_achat', '0.00')),
                prix_unitaire=Decimal(item['prix_unitaire']),
                unite=item['unite'],
                tva_pct=Decimal(item.get('tva_pct', '20.00')),
                famille=item.get('famille'),
                actif=item.get('actif', True),
                date_import=datetime.strptime(item['date_import'], '%Y-%m-%d').date(),
                date_maj=datetime.strptime(item['date_maj'], '%Y-%m-%d').date()
            )
            
            db.session.add(article)
            results.append(item['reference'])
            
        except Exception as e:
            errors.append({
                "reference": item.get('reference', 'unknown'),
                "error": str(e)
            })
    
    if errors:
        db.session.rollback()
        return {
            "success": False,
            "message": f"{len(errors)} erreurs détectées",
            "errors": errors
        }, 400
    
    db.session.commit()
    
    return {
        "success": True,
        "imported": len(results),
        "message": f"{len(results)} articles importés avec succès",
        "references": results
    }
```

### 🗄️ Tables à créer (si nécessaire)

#### Module 3 - Chantiers
```python
class Chantier(BaseModel):
    __tablename__ = 'chantiers'
    
    numero_chantier = db.Column(db.String(50), nullable=False, unique=True)
    nom_chantier = db.Column(db.String(200), nullable=False)
    client_nom = db.Column(db.String(100), nullable=False)
    montant_ht = db.Column(db.Numeric(10, 2))
    montant_ttc = db.Column(db.Numeric(10, 2))
    statut = db.Column(db.String(50), default='EN_ATTENTE')
    # ... autres champs selon besoins
```

## 🚀 Évolution et extensions

### 📁 Déclencheurs automatiques
- **OneDrive** : Détecter nouveaux fichiers
- **Email** : Import depuis pièces jointes
- **FTP** : Import depuis serveur distant

### 🔄 Transformations avancées
- **Validation** : Règles métier complexes
- **Enrichissement** : Calculs automatiques
- **Déduplication** : Éviter les doublons

### 📊 Monitoring
- **Logs** : Traçabilité des imports
- **Alertes** : Notification en cas d'erreur
- **Statistiques** : Dashboard des imports

## ❓ Questions fréquentes

### Q: Faut-il que toutes les tables soient créées ?
**R:** Non ! Commencez avec le Module 5 (articles_atarys) qui existe déjà. Créez les autres tables selon vos besoins.

### Q: Comment gérer les erreurs de format ?
**R:** Le workflow inclut une validation. Les erreurs sont collectées dans `validation.errors` et envoyées à l'API.

### Q: Peut-on modifier le format de sortie ?
**R:** Oui, mais respectez la structure `workflow_info`, `data`, `validation` pour la compatibilité ATARYS.

### Q: Comment tester sans affecter la production ?
**R:** Utilisez une copie de `atarys_data.db` et un endpoint de test `/api/test-import/`.

---

**🎯 Ce template vous donne une base solide pour remplacer vos scripts Python complexes par des workflows n8n visuels et maintenables !** 