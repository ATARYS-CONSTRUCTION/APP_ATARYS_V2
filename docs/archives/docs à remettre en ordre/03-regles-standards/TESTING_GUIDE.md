# 🧪 Guide de Tests ATARYS

> **Stratégie complète de tests pour le système ATARYS**  
> Framework : pytest + Jest  
> Dernière mise à jour : 22/06/2025

---

## 🎯 **Stratégie de Tests**

### **Pyramide de Tests**
```
                    🔺 E2E Tests (5%)
                 🔺🔺🔺 Integration Tests (15%)
            🔺🔺🔺🔺🔺🔺 Unit Tests (80%)
```

### **Types de Tests Implémentés**
1. **🔬 Tests Unitaires** : Logique métier, services, utilitaires
2. **🔗 Tests d'Intégration** : APIs, base de données, workflows
3. **🌐 Tests E2E** : Scénarios utilisateur complets
4. **📊 Tests de Performance** : Charge, stress, volume

---

## 🐍 **Tests Backend (Python/pytest)**

### **Configuration**

#### **Structure des Tests**
```
backend/tests/
├── conftest.py              # Configuration pytest
├── __init__.py
├── models/                  # Tests des modèles
│   ├── test_salarie.py
│   ├── test_planning.py
│   ├── test_ville.py
│   └── test_ardoise.py
├── routes/                  # Tests des APIs
│   ├── test_salaries.py
│   ├── test_planning.py
│   ├── test_villes.py
│   ├── test_ardoises.py
│   └── test_example_routes.py
├── services/                # Tests des services
│   ├── test_salarie_service.py
│   ├── test_calcul_service.py
│   └── test_database_service.py
└── utils/                   # Tests des utilitaires
    ├── test_validators.py
    ├── test_helpers.py
    └── test_security.py
```

#### **Configuration pytest (`conftest.py`)**
```python
import pytest
import tempfile
import os
from app import create_app
from app.models.base import db

@pytest.fixture
def app():
    """Application de test avec base de données temporaire"""
    # Créer une base de données temporaire
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """👥 Module 2: Clients de test Flask"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Runner CLI de test"""
    return app.test_cli_runner()

@pytest.fixture
def sample_salarie():
    """Données de test pour un salarié"""
    return {
        'prenom': 'Jean',
        'nom': 'Dupont',
        'salaire_brut_horaire': 15.5,
        'nombre_heure_hebdo': 35,
        'date_entree': '2023-01-15',
        'date_sortie': None,
        'niveau_id': 2,
        'colonne_planning': 1
    }
```

### **Tests Unitaires**

#### **Test Modèle (`test_salarie.py`)**
```python
import pytest
from datetime import date
from app.models.salarie import Salarie

class TestSalarieModel:
    """Tests du modèle Salarié"""
    
    def test_create_salarie(self, app, sample_salarie):
        """Test création d'un salarié"""
        with app.app_context():
            salarie = Salarie(**sample_salarie)
            assert salarie.prenom == 'Jean'
            assert salarie.nom == 'Dupont'
            assert salarie.is_active is True
            assert salarie.statut == 'CDI'
    
    def test_salarie_cdd(self, app, sample_salarie):
        """Test salarié en CDD"""
        with app.app_context():
            sample_salarie['date_sortie'] = '2023-12-31'
            salarie = Salarie(**sample_salarie)
            assert salarie.statut == 'CDD'
    
    def test_nom_complet(self, app, sample_salarie):
        """Test propriété nom complet"""
        with app.app_context():
            salarie = Salarie(**sample_salarie)
            assert salarie.nom_complet == 'Jean Dupont'
    
    def test_is_active_calculation(self, app, sample_salarie):
        """Test calcul du statut actif"""
        with app.app_context():
            # Salarié avec date de sortie dans le futur
            sample_salarie['date_sortie'] = '2025-12-31'
            salarie = Salarie(**sample_salarie)
            assert salarie.is_active is True
            
            # Salarié avec date de sortie dans le passé
            sample_salarie['date_sortie'] = '2022-12-31'
            salarie = Salarie(**sample_salarie)
            assert salarie.is_active is False
```

#### **Test Service (`test_salarie_service.py`)**
```python
import pytest
from app.services.salarie_service import SalarieService
from app.models.salarie import Salarie
from app.models.base import db

class TestSalarieService:
    """Tests du service Salarié"""
    
    def test_create_salarie(self, app, sample_salarie):
        """Test création via service"""
        with app.app_context():
            salarie = SalarieService.create(sample_salarie)
            assert salarie.id is not None
            assert salarie.prenom == 'Jean'
    
    def test_get_all_salaries(self, app, sample_salarie):
        """Test récupération de tous les salariés"""
        with app.app_context():
            # Créer des salariés de test
            SalarieService.create(sample_salarie)
            sample_salarie['prenom'] = 'Marie'
            SalarieService.create(sample_salarie)
            
            salaries = SalarieService.get_all()
            assert len(salaries) == 2
    
    def test_get_actifs(self, app, sample_salarie):
        """Test récupération salariés actifs"""
        with app.app_context():
            # Salarié actif
            SalarieService.create(sample_salarie)
            
            # Salarié inactif
            sample_salarie['prenom'] = 'Pierre'
            sample_salarie['date_sortie'] = '2022-12-31'
            SalarieService.create(sample_salarie)
            
            actifs = SalarieService.get_actifs()
            assert len(actifs) == 1
            assert actifs[0].prenom == 'Jean'
```

### **Tests d'Intégration API**

#### **Test Routes (`test_salaries.py`)**
```python
import pytest
import json
from app.models.base import db

class TestSalariesAPI:
    """Tests des APIs Salariés"""
    
    def test_get_all_salaries_empty(self, client):
        """Test GET /api/salaries avec base vide"""
        response = client.get('/api/salaries')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_create_salarie(self, client, sample_salarie):
        """Test POST /api/salaries"""
        response = client.post('/api/salaries',
                              data=json.dumps(sample_salarie),
                              content_type='application/json')
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['prenom'] == 'Jean'
    
    def test_get_salarie_by_id(self, client, sample_salarie):
        """Test GET /api/salaries/{id}"""
        # Créer un salarié
        create_response = client.post('/api/salaries',
                                    data=json.dumps(sample_salarie),
                                    content_type='application/json')
        salarie_id = json.loads(create_response.data)['data']['id']
        
        # Récupérer par ID
        response = client.get(f'/api/salaries/{salarie_id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['id'] == salarie_id
    
    def test_update_salarie(self, client, sample_salarie):
        """Test PUT /api/salaries/{id}"""
        # Créer un salarié
        create_response = client.post('/api/salaries',
                                    data=json.dumps(sample_salarie),
                                    content_type='application/json')
        salarie_id = json.loads(create_response.data)['data']['id']
        
        # Modifier
        update_data = {'prenom': 'Jean-Michel'}
        response = client.put(f'/api/salaries/{salarie_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['data']['prenom'] == 'Jean-Michel'
    
    def test_delete_salarie(self, client, sample_salarie):
        """Test DELETE /api/salaries/{id}"""
        # Créer un salarié
        create_response = client.post('/api/salaries',
                                    data=json.dumps(sample_salarie),
                                    content_type='application/json')
        salarie_id = json.loads(create_response.data)['data']['id']
        
        # Supprimer
        response = client.delete(f'/api/salaries/{salarie_id}')
        assert response.status_code == 200
        
        # Vérifier suppression
        get_response = client.get(f'/api/salaries/{salarie_id}')
        assert get_response.status_code == 404
```

### **Tests de Calcul Ardoises**

#### **Test Workflow Complet (`test_calcul_ardoises.py`)**
```python
import pytest
import json

class TestCalculArdoises:
    """Tests du workflow de calcul d'📐 Module 10: Outils Ardoises"""
    
    def test_calcul_workflow_complet(self, client):
        """Test du workflow complet de calcul"""
        # 1. Récupérer une ville
        response = client.get('/api/villes/commune/Rennes')
        assert response.status_code == 200
        ville_data = json.loads(response.data)
        zone = ville_data['data']['zone']
        
        # 2. Calculer le recouvrement
        params = {
            '📐 Module 10: Outils Ardoises': 45,
            'zone': zone,
            'projection': 2  # 5.5-11m
        }
        response = client.get('/api/ardoises/recouvrement-calcul', 
                            query_string=params)
        assert response.status_code == 200
        recouvrement_data = json.loads(response.data)
        recouvrement = recouvrement_data['data']['recouvrement']
        
        # 3. Récupérer les modèles disponibles
        response = client.get(f'/api/ardoises/modeles?recouvrement={recouvrement}')
        assert response.status_code == 200
        modeles_data = json.loads(response.data)
        assert len(modeles_data['data']) > 0
        
        # 4. Calculer les besoins
        calcul_data = {
            '🌍 Module 11: Géographie': 'Rennes',
            '📐 Module 10: Outils Ardoises': 45,
            'longueur_rampant': 8.5,
            'surface': 100,
            'modele_ardoise': modeles_data['data'][0]['modele']
        }
        response = client.post('/api/ardoises/calcul',
                             data=json.dumps(calcul_data),
                             content_type='application/json')
        assert response.status_code == 200
        
        result = json.loads(response.data)
        assert result['success'] is True
        assert 'nb_ardoises_total' in result['data']
```

---

## 🌐 **Tests Frontend (Jest/React Testing Library)**

### **Configuration**

#### **Installation**
```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom jest-environment-jsdom
```

#### **Configuration Jest (`package.json`)**
```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "jest": {
    "testEnvironment": "jsdom",
    "setupFilesAfterEnv": ["<rootDir>/src/setupTests.js"],
    "moduleNameMapping": {
      "^@/(.*)$": "<rootDir>/src/$1"
    }
  }
}
```

### **Tests Composants**

#### **Test Page (`CalculArdoises.test.jsx`)**
```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MenuProvider } from '../contexts/MenuContext';
import CalculArdoises from '../pages/CalculArdoises';

// Mock des APIs
jest.mock('../api/apiService', () => ({
  getVilles: jest.fn(() => Promise.resolve(['Rennes', 'Nantes'])),
  getVilleDetails: jest.fn(() => Promise.resolve({
    commune: 'Rennes',
    zone: '2'
  })),
  calculerRecouvrement: jest.fn(() => Promise.resolve({
    recouvrement: 100
  }))
}));

const renderWithContext = (component) => {
  return render(
    <MenuProvider>
      {component}
    </MenuProvider>
  );
};

describe('CalculArdoises', () => {
  test('affiche le formulaire de calcul', () => {
    renderWithContext(<CalculArdoises />);
    
    expect(screen.getByLabelText(/ville/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/pente/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/projection/i)).toBeInTheDocument();
  });
  
  test('calcule le recouvrement quand tous les champs sont remplis', async () => {
    renderWithContext(<CalculArdoises />);
    
    // Remplir les champs
    fireEvent.change(screen.getByLabelText(/ville/i), {
      target: { value: 'Rennes' }
    });
    fireEvent.change(screen.getByLabelText(/pente/i), {
      target: { value: '45' }
    });
    fireEvent.change(screen.getByLabelText(/projection/i), {
      target: { value: '8' }
    });
    
    // Attendre le calcul automatique
    await waitFor(() => {
      expect(screen.getByText(/recouvrement.*100/i)).toBeInTheDocument();
    });
  });
});
```

#### **Test Service API (`apiService.test.js`)**
```javascript
import { getVilles, createSalarie } from '../api/apiService';

// Mock axios
jest.mock('axios', () => ({
  create: () => ({
    get: jest.fn(),
    post: jest.fn(),
    interceptors: {
      response: {
        use: jest.fn()
      }
    }
  })
}));

describe('API Service', () => {
  test('getVilles retourne la liste des villes', async () => {
    const mockVilles = ['Rennes', 'Nantes', 'Brest'];
    require('axios').create().get.mockResolvedValue({
      data: mockVilles
    });
    
    const villes = await getVilles();
    expect(villes).toEqual(mockVilles);
  });
  
  test('createSalarie envoie les bonnes données', async () => {
    const mockSalarie = {
      prenom: 'Jean',
      nom: 'Dupont',
      salaire_brut_horaire: 15.5
    };
    
    const mockResponse = {
      data: { success: true, data: { id: 1, ...mockSalarie } }
    };
    
    require('axios').create().post.mockResolvedValue(mockResponse);
    
    const result = await createSalarie(mockSalarie);
    expect(result.success).toBe(true);
    expect(result.data.prenom).toBe('Jean');
  });
});
```

---

## 🚀 **Tests E2E (Playwright)**

### **Configuration**

#### **Installation**
```bash
npm install --save-dev @playwright/test
npx playwright install
```

#### **Test E2E (`e2e/calcul-ardoises.spec.js`)**
```javascript
import { test, expect } from '@playwright/test';

test.describe('📐 Module 10: Outils Ardoises Ardoises E2E', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3001');
  });
  
  test('workflow complet de calcul', async ({ page }) => {
    // Naviguer vers la page de calcul
    await page.click('text=Calcul Ardoises');
    
    // Remplir le formulaire
    await page.fill('input[name="🌍 Module 11: Géographie"]', 'Rennes');
    await page.fill('input[name="📐 Module 10: Outils Ardoises"]', '45');
    await page.fill('input[name="projection"]', '8');
    
    // Attendre le calcul automatique
    await expect(page.locator('text=Recouvrement')).toBeVisible();
    
    // Vérifier que les modèles sont chargés
    await expect(page.locator('select[name="modele"]')).toBeVisible();
    
    // Sélectionner un modèle
    await page.selectOption('select[name="modele"]', '22x16');
    
    // Vérifier les résultats
    await expect(page.locator('text=Nombre d\'📐 Module 10: Outils Ardoises')).toBeVisible();
    await expect(page.locator('text=Nombre de liteaux')).toBeVisible();
  });
});
```

---

## 📊 **Tests de Performance**

### **Test de Charge Backend**

#### **Configuration Locust (`locustfile.py`)**
```python
from locust import HttpUser, task, between

class AtarysUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Actions à l'initialisation"""
        pass
    
    @task(3)
    def get_salaries(self):
        """Test charge GET /api/salaries"""
        self.client.get("/api/salaries")
    
    @task(2)
    def get_villes(self):
        """Test charge GET /api/villes"""
        self.client.get("/api/villes")
    
    @task(1)
    def calcul_recouvrement(self):
        """Test charge calcul recouvrement"""
        self.client.get("/api/ardoises/recouvrement-calcul?pente=45&zone=2&projection=2")
    
    @task(1)
    def create_salarie(self):
        """Test charge création salarié"""
        self.client.post("/api/salaries", json={
            "prenom": "Test",
            "nom": "User",
            "salaire_brut_horaire": 15.0,
            "nombre_heure_hebdo": 35,
            "date_entree": "2023-01-01",
            "niveau_id": 1,
            "colonne_planning": 1
        })
```

### **Exécution Tests de Charge**
```bash
# Installer Locust
pip install locust

# Lancer les tests
locust -f locustfile.py --host=http://localhost:5000
```

---

## 🔧 **Commandes de Test**

### **Backend (pytest)**
```bash
# Tests unitaires
cd backend
python -m pytest tests/ -v

# Tests avec couverture
python -m pytest tests/ --cov=app --cov-report=html

# Tests spécifiques
python -m pytest tests/routes/test_salaries.py -v

# Tests en mode watch
python -m pytest tests/ -f
```

### **Frontend (Jest)**
```bash
# Tests unitaires
cd frontend
npm test

# Tests avec couverture
npm run test:coverage

# Tests en mode watch
npm run test:watch

# Tests E2E
npx playwright test
```

---

## 📋 **Checklist Qualité**

### **Avant Chaque Commit**
- [ ] ✅ Tests unitaires passent (>90% couverture)
- [ ] ✅ Tests d'intégration passent
- [ ] ✅ Linting sans erreurs
- [ ] ✅ Formatage du code respecté
- [ ] ✅ Documentation mise à jour

### **Avant Chaque Release**
- [ ] ✅ Tests E2E complets
- [ ] ✅ Tests de performance acceptables
- [ ] ✅ Tests de sécurité passés
- [ ] ✅ Tests de compatibilité navigateurs
- [ ] ✅ Tests de charge validés

---

## 🎯 **Objectifs de Couverture**

### **Couverture de Code**
- **Backend** : >90% (services, models, routes)
- **Frontend** : >80% (composants, services)
- **E2E** : 100% des workflows critiques

### **Métriques de Performance**
- **API Response Time** : <200ms (95e percentile)
- **Page Load Time** : <2s
- **Database Queries** : <50ms moyenne

### **Seuils d'Alerte**
- **Temps de réponse API** : >500ms
- **Erreurs** : >1% des requêtes
- **Couverture** : <85% backend, <75% frontend

---

## 📚 **Ressources**

### **Documentation**
- [pytest Documentation](https://docs.pytest.org/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Playwright Documentation](https://playwright.dev/)

### **Outils Recommandés**
- **Coverage** : pytest-cov, jest --coverage
- **Mocking** : pytest-mock, jest.mock
- **Fixtures** : pytest fixtures, factory-boy
- **CI/CD** : GitHub Actions, GitLab CI 