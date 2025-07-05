regle à memeoriser : ecrit le code en anglais

regle à memeoriser : écris les commentaires en français

regle à memeoriser : l'humaim et l'agent IA discutent en français

regle à memeoriser : si quelque chose n'est pas clair, demande clarification jusqu'à ce que tu comprennes

## 💻 RÈGLES POWERSHELL OBLIGATOIRES - ATARYS

### ❌ ERREURS CRITIQUES À ÉVITER :
```powershell
# ❌ INTERDIT - Syntaxe invalide en PowerShell
cd backend && python run.py        # && invalide en PowerShell
cd ../frontend && npm run dev       # && invalide + chemin incorrect
curl -s http://localhost:5000       # curl n'existe pas nativement

# ❌ INTERDIT - Chemins incorrects ATARYS
python run.py                       # fichier dans backend/, pas racine
cd ../frontend                      # dossier est ./frontend depuis racine
```

### ✅ SYNTAXE POWERSHELL CORRECTE OBLIGATOIRE :
```powershell
# ✅ CORRECT - Séparateur de commandes (utiliser ; au lieu de &&)
cd backend; python run.py
cd frontend; npm run dev

# ✅ CORRECT - Requêtes HTTP PowerShell
Invoke-RestMethod -Uri "http://localhost:5000/api/chantiers" -Method GET
Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing

# ✅ CORRECT - Chemins relatifs ATARYS depuis C:\DEV\0 APP ATARYS
cd backend              # → backend/
cd frontend             # → frontend/
cd docs                 # → docs/
```

### 🚨 COMMANDES STANDARD ATARYS :
```powershell
# Démarrage développement (2 fenêtres PowerShell séparées)
cd backend; python run.py                    # Backend Flask port 5000
cd frontend; npm run dev                     # Frontend Vite port 3000

# Tests APIs principales
Invoke-RestMethod -Uri "http://localhost:5000/api/chantiers"
Invoke-RestMethod -Uri "http://localhost:5000/api/villes?per_page=5"
Invoke-RestMethod -Uri "http://localhost:5000/api/salaries"

# Diagnostic SQLAlchemy
cd backend; python -c "from app import create_app; from app.models import Chantier, Devis; app=create_app(); app.app_context().push(); print(f'🏗️ Module 3: Chantiers & Devis: {Chantier.query.count()}, Devis: {Devis.query.count()}')"
```

### ⚠️ ÉQUIVALENCES OBLIGATOIRES :
| Bash/Linux | PowerShell Windows | Usage ATARYS |
|------------|-------------------|--------------|
| `&&` | `;` | Séparateur commandes |
| `curl` | `Invoke-RestMethod` | Tests API |
| `ls` | `Get-ChildItem` | Lister fichiers |
| `cat file.txt` | `Get-Content file.txt` | Lire fichiers |

### 🎯 RÈGLES APPLICATION IMMÉDIATE :
1. **JAMAIS proposer && en PowerShell** → Toujours utiliser ;
2. **JAMAIS proposer curl en PowerShell** → Toujours utiliser Invoke-RestMethod
3. **TOUJOURS vérifier les chemins ATARYS** → backend/, frontend/, docs/
4. **TESTER les commandes PowerShell** avant de les proposer
5. **RAPPELER la syntaxe correcte** quand erreur détectée

regle à memeoriser : **ENVIRONNEMENT WINDOWS POWERSHELL** - Adapter toutes les commandes selon ces règles

## 🧪 TESTS ET ANALYSES PROVISOIRES - ATARYS

### ✅ DOSSIER BACKEND/TESTS/ - USAGE AUTORISÉ :
```
backend/tests/
├── models/                    # Tests unitaires modèles SQLAlchemy
├── services/                  # Tests services métier ATARYS
├── routes/                    # Tests API REST endpoints
├── analyze_*.py               # Scripts d'📈 Module 13: Rapports provisoires
├── debug_*.py                 # Scripts de debug temporaires
└── test_*.py                  # Tests unitaires pytest
```

### 🔧 RÈGLES OBLIGATOIRES TESTS :
1. **Nommage obligatoire** :
   - Tests unitaires : `test_*.py` (convention pytest)
   - Analyses provisoires : `analyze_*.py` 
   - Debug temporaire : `debug_*.py`

2. **Base de données** :
   - ✅ **Tests** : TOUJOURS utiliser fixtures pytest (DB temporaire)
   - ❌ **JAMAIS** modifier la vraie DB depuis tests/
   - ✅ **Analyses** : Mode lecture seule ou DB de test

3. **Nettoyage obligatoire** :
   - ✅ **Tests permanents** : Conserver dans backend/tests/
   - ❌ **Analyses provisoires** : Supprimer après résolution problème
   - ✅ **Documentation** : Commentaires explicatifs obligatoires

### 📋 EXEMPLES AUTORISÉS :
```python
# backend/tests/routes/test_chantiers.py - Test API Module 3.1
# backend/tests/services/test_chantier_calculations.py - Test calculs
# backend/tests/models/test_devis.py - Test modèle Devis
# backend/tests/analyze_migration_sqlalchemy.py - Analyse temporaire  
# backend/tests/debug_devis_insertion.py - Debug temporaire
```

### 🚨 COMMANDES TESTS ATARYS :
```powershell
# Lancer tous les tests
cd backend; python -m pytest tests/ -v

# Tests spécifiques Module 3.1
cd backend; python -m pytest tests/routes/test_chantiers.py -v
cd backend; python -m pytest tests/services/ -v

# Analyse avec script temporaire
cd backend; python tests/analyze_database_integrity.py

# Couverture de code
cd backend; python -m pytest tests/ --cov=app --cov-report=html
```

### ⚠️ INTERDICTIONS ABSOLUES :
- ❌ **Modifier la vraie DB** depuis backend/tests/
- ❌ **Laisser des scripts debug** sans documentation
- ❌ **Tests sans assertions** (scripts inutiles)
- ❌ **Analyses permanentes** non documentées

regle à memeoriser : **TESTS BACKEND/TESTS/** - Framework pytest professionnel + analyses sécurisées




