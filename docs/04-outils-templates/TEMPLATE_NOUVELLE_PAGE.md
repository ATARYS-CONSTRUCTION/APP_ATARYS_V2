# 📝 Template - Créer une Nouvelle Page ATARYS

> **Guide complet pour créer une nouvelle page selon la Nomenclature ATARYS**  
> Respecte l'architecture, les standards et la documentation complète

---

## 🎯 **Étape 1 : Identifier le Module selon Nomenclature**

### **Référence Nomenclature ATARYS**
Consultez `docs/NOMENCLATURE.txt` pour identifier le module :

| Module | Nom | Sous-modules |
|--------|-----|--------------|
| **1** | PLANNING | 1.1 PLANNING SALARIES, 1.2 PLANNING CHANTIER |
| **2** | LISTE DES TACHES | 2.2 JULIEN, 2.1 YANN |
| **3** | LISTE CHANTIERS | 3.1 LISTE CHANTIERS, 3.2 CHANTIERS PROJETS, 3.3 CHANTIERS SIGNES, 3.4 CHANTIERS EN COURS, 3.5 CHANTIERS ARCHIVES |
| **4** | CHANTIERS | 4.1 SUIVI DE CHANTIER, 4.2 NOTES DE CHANTIER, 4.3 COMMANDES, 4.4 DOCUMENTS |
| **5** | DEVIS-FACTURATION | 5.1 Ouvrages et articles BATAPPLI, 5.2 FICHE METRES, 5.3 DEVIS MEXT, 5.4 DEVIS TYPE |
| **6** | ATELIER | 6.1 QUINCAILLERIE, 6.2 CONSOMMABLES, 6.3 CAMION, 6.4 MATERIEL, 6.5 ECHAFAUDAGE |
| **7** | GESTION | 7.1 PREVISIONNEL, 7.2 SYNTHESE PREVISIONNELLE, 7.3 BILANS |
| **8** | COMPTABILITE | 8.1 TVA, 8.2 TABLEAU DE BORD |
| **9** | SOCIAL | 9.1 Liste_salaries, 9.2 Fiche mensuelle, 9.3 Récap et calculs |
| **10** | OUTILS | 10.1 CALCUL_ARDOISES, 10.2 Calcul_structures, 10.3 Staravina (base de données avec mots-clés de la documentation), 10.4 Documents types |
| **11** | ARCHIVES |  |
| **12** | PARAMETRES |  |
| **13** | AIDE | NOMENCLATURE |

### **Exemple : Module 3.1 - Liste Chantiers**
- **Module** : 3 (LISTE CHANTIERS)
- **Sous-module** : 3.1 (Liste Chantiers - Vue générale)
- **Nom de fichier** : `ListeChantiers.jsx`
- **Route** : `/liste-chantiers`

---

## 🏗️ **Étape 2 : Créer la Structure Backend (APIs)**

### **2.1 Créer le Modèle SQLAlchemy**
```bash
# Fichier : backend/app/models/chantier.py
```

```python
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Chantier(BaseModel):
    """Module 3.1 - Modèle Chantier pour Liste Chantiers"""
    __tablename__ = '🏗️ Module 3: Chantiers & Devis'
    
    id = Column(Integer, primary_key=True)
    nom = Column(String(200), nullable=False)
    client = Column(String(200), nullable=False)
    adresse = Column(Text)
    ville_id = Column(Integer, ForeignKey('🌍 Module 11: Géographie.id'))
    statut = Column(String(50), default='a_deviser')  # a_deviser, signe, en_cours, fini, archive
    date_creation = Column(DateTime, nullable=False)
    date_debut = Column(DateTime)
    date_fin_prevue = Column(DateTime)
    montant_estime = Column(Float)
    description = Column(Text)
    
    # Relations
    ville = relationship("🌍 Module 11: Géographie", back_populates="🏗️ Module 3: Chantiers & Devis")
    
    def to_dict(self):
        """Format compatible frontend"""
        return {
            'id': self.id,
            'nom': self.nom,
            '👥 Module 2: Clients': self.client,
            'adresse': self.adresse,
            '🌍 Module 11: Géographie': self.ville.commune if self.ville else None,
            'statut': self.statut,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            'date_debut': self.date_debut.isoformat() if self.date_debut else None,
            'date_fin_prevue': self.date_fin_prevue.isoformat() if self.date_fin_prevue else None,
            'montant_estime': self.montant_estime,
            'description': self.description
        }
```

### **2.2 Créer le Service**
```bash
# Fichier : backend/app/services/chantier_service.py
```

```python
from sqlalchemy.orm import Session
from ..models.chantier import Chantier
from ..utils.exceptions import ValidationError, NotFoundError

class ChantierService:
    """Module 3.1 - Service pour gestion des chantiers"""
    
    @staticmethod
    def get_all_chantiers(db: Session, statut=None, page=1, per_page=50):
        """Récupère tous les chantiers avec pagination et filtrage"""
        query = db.query(Chantier)
        
        if statut:
            query = query.filter(Chantier.statut == statut)
        
        total = query.count()
        chantiers = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return {
            '🏗️ Module 3: Chantiers & Devis': [c.to_dict() for c in chantiers],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }
    
    @staticmethod
    def create_chantier(db: Session, chantier_data):
        """Crée un nouveau chantier"""
        if not chantier_data.get('nom'):
            raise ValidationError("Le nom du chantier est obligatoire")
        
        chantier = Chantier(**chantier_data)
        db.add(chantier)
        db.commit()
        db.refresh(chantier)
        
        return chantier.to_dict()
    
    @staticmethod
    def get_chantier_by_id(db: Session, chantier_id):
        """Récupère un chantier par ID"""
        chantier = db.query(Chantier).filter(Chantier.id == chantier_id).first()
        if not chantier:
            raise NotFoundError(f"🏗️ Module 3: Chantiers & Devis {chantier_id} non trouvé")
        
        return chantier.to_dict()
```

### **2.3 Créer les Routes API**
```bash
# Fichier : backend/app/routes/chantiers.py
```

```python
from flask import Blueprint, request, jsonify
from ..services.chantier_service import ChantierService
from ..middleware.error_handler import handle_api_error
from ..utils.validators import validate_pagination

# Module 3 - LISTE CHANTIERS
chantiers_bp = Blueprint('🏗️ Module 3: Chantiers & Devis', __name__, url_prefix='/api/chantiers')

@chantiers_bp.route('', methods=['GET'])
@handle_api_error
def get_chantiers():
    """Module 3.1 - Récupère la liste des chantiers"""
    # Paramètres de pagination et filtrage
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 50, type=int), 100)
    statut = request.args.get('statut')
    
    validate_pagination(page, per_page)
    
    from ..database_service import get_db
    db = next(get_db())
    
    result = ChantierService.get_all_chantiers(
        db=db, 
        statut=statut, 
        page=page, 
        per_page=per_page
    )
    
    return jsonify({
        'success': True,
        'data': result['🏗️ Module 3: Chantiers & Devis'],
        'pagination': result['pagination'],
        'message': f"Module 3.1 - {len(result['🏗️ Module 3: Chantiers & Devis'])} chantiers récupérés"
    })

@chantiers_bp.route('', methods=['POST'])
@handle_api_error
def create_chantier():
    """Module 3.1 - Crée un nouveau chantier"""
    data = request.get_json()
    
    from ..database_service import get_db
    db = next(get_db())
    
    chantier = ChantierService.create_chantier(db=db, chantier_data=data)
    
    return jsonify({
        'success': True,
        'data': chantier,
        'message': 'Module 3.1 - Chantier créé avec succès'
    }), 201

@chantiers_bp.route('/<int:chantier_id>', methods=['GET'])
@handle_api_error
def get_chantier(chantier_id):
    """Module 3.1 - Récupère un chantier par ID"""
    from ..database_service import get_db
    db = next(get_db())
    
    chantier = ChantierService.get_chantier_by_id(db=db, chantier_id=chantier_id)
    
    return jsonify({
        'success': True,
        'data': chantier,
        'message': f'Module 3.1 - Chantier {chantier_id} récupéré'
    })
```

### **2.4 Enregistrer le Blueprint**
```python
# Dans backend/app/__init__.py
from .routes.chantiers import chantiers_bp

def create_app():
    # ... existing code ...
    
    # Module 3 - LISTE CHANTIERS
    app.register_blueprint(chantiers_bp)
    
    return app
```

---

## 🎨 **Étape 3 : Créer la Page Frontend**

### **3.1 Créer le Hook API**
```bash
# Fichier : frontend/src/hooks/useChantiers.js
```

```javascript
import { useState, useEffect } from 'react';
import { apiService } from '../api/apiService';

export const useChantiers = (statut = null) => {
  const [chantiers, setChantiers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState(null);

  const fetchChantiers = async (page = 1, filters = {}) => {
    try {
      setLoading(true);
      setError(null);
      
      const params = { page, per_page: 50, ...filters };
      if (statut) params.statut = statut;
      
      const response = await apiService.get('/chantiers', { params });
      
      if (response.success) {
        setChantiers(response.data);
        setPagination(response.pagination);
      } else {
        setError(response.message || 'Erreur lors du chargement des chantiers');
      }
    } catch (err) {
      setError('Erreur de connexion API');
      console.error('Erreur API chantiers:', err);
    } finally {
      setLoading(false);
    }
  };

  const createChantier = async (chantierData) => {
    try {
      const response = await apiService.post('/chantiers', chantierData);
      if (response.success) {
        await fetchChantiers(); // Recharger la liste
        return response.data;
      } else {
        throw new Error(response.message);
      }
    } catch (err) {
      throw new Error('Erreur lors de la création du chantier');
    }
  };

  useEffect(() => {
    fetchChantiers();
  }, [statut]);

  return {
    chantiers,
    loading,
    error,
    pagination,
    fetchChantiers,
    createChantier,
    refresh: () => fetchChantiers()
  };
};
```

### **3.2 Créer la Page Principal**
```bash
# Fichier : frontend/src/pages/ListeChantiers.jsx
```

```javascript
import React, { useState } from 'react';
import { PageLayout, Card, FormLayout, FormSection, InputGroup } from '../components/Layout';
import { Input, Select, Button, ActionButtonGroup } from '../components/FormComponents';
import { useChantiers } from '../hooks/useChantiers';
import { useLoading } from '../components/LoadingOverlay';

function ListeChantiers() {
  // Module 3.1 - Liste Chantiers selon nomenclature ATARYS
  const [selectedStatut, setSelectedStatut] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newChantier, setNewChantier] = useState({
    nom: '',
    client: '',
    adresse: '',
    statut: 'a_deviser',
    montant_estime: '',
    description: ''
  });

  const { chantiers, loading, error, pagination, fetchChantiers, createChantier, refresh } = useChantiers(selectedStatut);
  const { setLoading } = useLoading();

  // Options de statut selon Module 3 (sous-modules 3.1 à 3.5)
  const statutOptions = [
    { value: '', label: 'Tous les chantiers' },
    { value: 'a_deviser', label: '3.2 - À Deviser' },
    { value: 'signe', label: '3.3 - Signés' },
    { value: 'en_cours', label: '3.4 - À Finir' },
    { value: 'archive', label: '3.5 - Archives' }
  ];

  const handleCreateChantier = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      await createChantier(newChantier);
      setShowCreateForm(false);
      setNewChantier({
        nom: '',
        client: '',
        adresse: '',
        statut: 'a_deviser',
        montant_estime: '',
        description: ''
      });
    } catch (err) {
      alert('Erreur: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const getStatutLabel = (statut) => {
    const option = statutOptions.find(opt => opt.value === statut);
    return option ? option.label : statut;
  };

  const getStatutColor = (statut) => {
    const colors = {
      'a_deviser': 'bg-yellow-100 text-yellow-800',
      'signe': 'bg-blue-100 text-blue-800',
      'en_cours': 'bg-green-100 text-green-800',
      'archive': 'bg-gray-100 text-gray-800'
    };
    return colors[statut] || 'bg-gray-100 text-gray-800';
  };

  if (error) {
    return (
      <PageLayout variant="wide" title="Module 3.1 - Liste Chantiers">
        <Card>
          <div classname="flex flex-col items-center justify-center h-64">
            <p classname="text-red-500">Erreur: {error}</p>
            <Button onClick={refresh} variant="primary" classname="mt-4">
              Réessayer
            </Button>
          </div>
        </Card>
      </PageLayout>
    );
  }

  return (
    <PageLayout variant="ultrawide" title="Module 3.1 - Liste Chantiers">
      {/* Filtres et Actions */}
      <Card padding="standard" classname="mb-4">
        <FormLayout gap="standard">
          <FormSection title="Filtres">
            <InputGroup>
              <Select
                label="Statut"
                options={statutOptions}
                value={selectedStatut}
                onChange={(e) => setSelectedStatut(e.target.value)}
                placeholder="Filtrer par statut"
              />
            </InputGroup>
          </FormSection>
          
          <FormSection title="Actions" divider>
            <div classname="flex gap-3">
              <Button
                variant="primary"
                onClick={() => setShowCreateForm(!showCreateForm)}
              >
                {showCreateForm ? 'Annuler' : 'Nouveau Chantier'}
              </Button>
              <Button variant="secondary" onClick={refresh}>
                Actualiser
              </Button>
            </div>
          </FormSection>
        </FormLayout>
      </Card>

      {/* Formulaire de Création */}
      {showCreateForm && (
        <Card padding="standard" classname="mb-4">
          <form onSubmit={handleCreateChantier}>
            <h3 classname="text-lg font-semibold mb-4">Nouveau Chantier</h3>
            <FormLayout gap="standard">
              <FormSection title="Informations générales">
                <InputGroup>
                  <Input
                    label="Nom du chantier"
                    value={newChantier.nom}
                    onChange={(e) => setNewChantier({...newChantier, nom: e.target.value})}
                    required
                  />
                  <Input
                    label="👥 Module 2: Clients"
                    value={newChantier.client}
                    onChange={(e) => setNewChantier({...newChantier, client: e.target.value})}
                    required
                  />
                  <Input
                    label="Adresse"
                    value={newChantier.adresse}
                    onChange={(e) => setNewChantier({...newChantier, adresse: e.target.value})}
                  />
                </InputGroup>
              </FormSection>
              
              <FormSection title="Détails" divider>
                <InputGroup>
                  <Select
                    label="Statut initial"
                    options={statutOptions.slice(1)} // Exclure "Tous"
                    value={newChantier.statut}
                    onChange={(e) => setNewChantier({...newChantier, statut: e.target.value})}
                  />
                  <Input
                    label="Montant estimé (€)"
                    type="number"
                    step="0.01"
                    value={newChantier.montant_estime}
                    onChange={(e) => setNewChantier({...newChantier, montant_estime: e.target.value})}
                  />
                </InputGroup>
              </FormSection>
            </FormLayout>
            
            <ActionButtonGroup variant="inline">
              <Button type="submit" variant="success">
                Créer le Chantier
              </Button>
              <Button 
                type="button" 
                variant="secondary"
                onClick={() => setShowCreateForm(false)}
              >
                Annuler
              </Button>
            </ActionButtonGroup>
          </form>
        </Card>
      )}

      {/* Liste des Chantiers */}
      <Card padding="tight">
        {loading ? (
          <div classname="flex justify-center items-center h-64">
            Chargement des chantiers...
          </div>
        ) : chantiers.length === 0 ? (
          <div classname="text-center text-gray-600 py-12">
            <p>Aucun chantier trouvé</p>
            {selectedStatut && (
              <p classname="text-sm mt-2">
                Essayez de changer le filtre de statut
              </p>
            )}
          </div>
        ) : (
          <div classname="overflow-x-auto">
            <table classname="w-full text-sm">
              <thead classname="bg-gray-50">
                <tr>
                  <th classname="p-3 text-left font-semibold">Nom</th>
                  <th classname="p-3 text-left font-semibold">Client</th>
                  <th classname="p-3 text-left font-semibold">Ville</th>
                  <th classname="p-3 text-left font-semibold">Statut</th>
                  <th classname="p-3 text-right font-semibold">Montant</th>
                  <th classname="p-3 text-center font-semibold">Actions</th>
                </tr>
              </thead>
              <tbody>
                {chantiers.map((chantier) => (
                  <tr key={chantier.id} classname="border-t hover:bg-gray-50">
                    <td classname="p-3 font-medium">{chantier.nom}</td>
                    <td classname="p-3">{chantier.client}</td>
                    <td classname="p-3">{chantier.ville || '-'}</td>
                    <td classname="p-3">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatutColor(chantier.statut)}`}>
                        {getStatutLabel(chantier.statut)}
                      </span>
                    </td>
                    <td classname="p-3 text-right">
                      {chantier.montant_estime ? 
                        `${parseFloat(chantier.montant_estime).toLocaleString('fr-FR', {
                          style: 'currency',
                          currency: 'EUR'
                        })}` : '-'
                      }
                    </td>
                    <td classname="p-3 text-center">
                      <Button size="sm" variant="outline">
                        Voir
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        
        {/* Pagination */}
        {pagination && pagination.pages > 1 && (
          <div classname="mt-4 flex justify-between items-center text-sm">
            <span>
              Page {pagination.page} sur {pagination.pages} 
              ({pagination.total} chantiers)
            </span>
            <div classname="flex gap-2">
              <Button
                size="sm"
                variant="secondary"
                disabled={pagination.page <= 1}
                onClick={() => fetchChantiers(pagination.page - 1)}
              >
                Précédent
              </Button>
              <Button
                size="sm"
                variant="secondary"
                disabled={pagination.page >= pagination.pages}
                onClick={() => fetchChantiers(pagination.page + 1)}
              >
                Suivant
              </Button>
            </div>
          </div>
        )}
      </Card>
    </PageLayout>
  );
}

export default ListeChantiers;
```

---

## 🔗 **Étape 4 : Intégrer la Route**

### **4.1 Ajouter la Route dans App.jsx**
```javascript
// Dans frontend/src/App.jsx
import ListeChantiers from './pages/ListeChantiers';

function App() {
  return (
    <Router>
      <MenuProvider>
        <div classname="min-h-screen flex bg-gray-50">
          <Menu />
          <div classname="flex-1 relative">
            <LoadingProvider>
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/calcul-ardoises" element={<CalculArdoises />} />
                <Route path="/planning-salaries" element={<PlanningSalaries />} />
                <Route path="/planning-chantiers" element={<PlanningChantiers />} />
                {/* Module 3.1 - Nouvelle page */}
                <Route path="/liste-chantiers" element={<ListeChantiers />} />
              </Routes>
            </LoadingProvider>
          </div>
        </div>
      </MenuProvider>
    </Router>
  );
}
```

### **4.2 Ajouter le Lien dans Menu.jsx**
```javascript
// Dans frontend/src/components/Menu.jsx
<Link classname="block px-2 py-1 rounded hover:bg-gray-200 hover:text-black" to="/liste-chantiers">
  LISTE CHANTIERS
</Link>
```

---

## 🧪 **Étape 5 : Créer les Tests**

### **5.1 Test Backend**
```bash
# Fichier : backend/tests/routes/test_chantiers.py
```

```python
import pytest
from flask import url_for

def test_get_chantiers(client, db_session):
    """Module 3.1 - Test récupération liste chantiers"""
    response = client.get('/api/chantiers')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data
    assert 'pagination' in data

def test_create_chantier(client, db_session):
    """Module 3.1 - Test création chantier"""
    chantier_data = {
        'nom': 'Test Chantier',
        '👥 Module 2: Clients': 'Test Client',
        'adresse': '123 Test Street',
        'statut': 'a_deviser'
    }
    
    response = client.post('/api/chantiers', json=chantier_data)
    assert response.status_code == 201
    
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['nom'] == 'Test Chantier'
```

### **5.2 Test Frontend**
```bash
# Fichier : frontend/src/pages/__tests__/ListeChantiers.test.jsx
```

```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import ListeChantiers from '../ListeChantiers';
import { MenuProvider } from '../../contexts/MenuContext';

// Mock du hook
jest.mock('../../hooks/useChantiers', () => ({
  useChantiers: () => ({
    chantiers: [
      { id: 1, nom: 'Test Chantier', client: 'Test Client', statut: 'a_deviser' }
    ],
    loading: false,
    error: null,
    pagination: null,
    fetchChantiers: jest.fn(),
    createChantier: jest.fn(),
    refresh: jest.fn()
  })
}));

const renderWithProviders = (component) => {
  return render(
    <BrowserRouter>
      <MenuProvider>
        {component}
      </MenuProvider>
    </BrowserRouter>
  );
};

describe('Module 3.1 - ListeChantiers', () => {
  test('affiche la liste des chantiers', async () => {
    renderWithProviders(<ListeChantiers />);
    
    expect(screen.getByText('Module 3.1 - Liste Chantiers')).toBeInTheDocument();
    expect(screen.getByText('Test Chantier')).toBeInTheDocument();
    expect(screen.getByText('Test Client')).toBeInTheDocument();
  });

  test('peut ouvrir le formulaire de création', () => {
    renderWithProviders(<ListeChantiers />);
    
    const button = screen.getByText('Nouveau Chantier');
    fireEvent.click(button);
    
    expect(screen.getByText('Nouveau Chantier')).toBeInTheDocument();
    expect(screen.getByLabelText('Nom du chantier')).toBeInTheDocument();
  });
});
```

---

## 📚 **Étape 6 : Documenter selon Standards**

### **6.1 Mettre à jour API_ENDPOINTS.md**
```markdown
## Module 3 - LISTE CHANTIERS

### GET /api/chantiers
Récupère la liste des chantiers avec pagination et filtrage.

**Paramètres de requête :**
- `page` (int, optionnel) : Numéro de page (défaut: 1)
- `per_page` (int, optionnel) : Éléments par page (défaut: 50, max: 100)
- `statut` (string, optionnel) : Filtre par statut (a_deviser, signe, en_cours, archive)

**Réponse :**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nom": "Rénovation Toiture",
      "👥 Module 2: Clients": "Dupont Jean",
      "adresse": "123 Rue de la Paix",
      "🌍 Module 11: Géographie": "Rennes",
      "statut": "a_deviser",
      "date_creation": "2025-06-22T10:00:00",
      "montant_estime": 15000.00
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total": 25,
    "pages": 1
  }
}
```
```

### **6.2 Mettre à jour DATABASE_SCHEMA.md**
```markdown
## Table : chantiers (Module 3)

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique |
| nom | VARCHAR(200) | NOT NULL | Nom du chantier |
| client | VARCHAR(200) | NOT NULL | Nom du client |
| adresse | TEXT | - | Adresse du chantier |
| ville_id | INTEGER | FOREIGN KEY | Référence vers table villes |
| statut | VARCHAR(50) | DEFAULT 'a_deviser' | Statut du chantier |
| date_creation | DATETIME | NOT NULL | Date de création |
| montant_estime | FLOAT | - | Montant estimé en euros |

**Statuts possibles :**
- `a_deviser` : Module 3.2 - Chantiers à Deviser
- `signe` : Module 3.3 - Chantiers Signés
- `en_cours` : Module 3.4 - Chantiers à Finir
- `archive` : Module 3.5 - Chantiers Archives
```

### **6.3 Commit Git selon Standards**
```bash
git add .
git commit -m "Module 3.1: Implémentation Liste Chantiers

- Backend: Modèle, Service et Routes API
- Frontend: Page complète avec CRUD
- Tests: Backend et Frontend
- Documentation: APIs et schéma DB

Fonctionnalités:
- Liste avec pagination et filtrage par statut
- Création de nouveaux chantiers
- Interface responsive selon layout system
- Gestion d'erreurs et loading states"
```

---

## ✅ **Checklist Complète**

### **Backend ✅**
- [ ] Modèle SQLAlchemy créé avec relations
- [ ] Service avec logique métier
- [ ] Routes API avec gestion d'erreurs
- [ ] Blueprint enregistré dans app
- [ ] Tests unitaires backend

### **Frontend ✅**
- [ ] Hook personnalisé pour API
- [ ] Page principale avec tous les composants
- [ ] Formulaires avec validation
- [ ] Gestion des états (loading, error)
- [ ] Interface responsive
- [ ] Tests composants React

### **Intégration ✅**
- [ ] Route ajoutée dans App.jsx
- [ ] Lien ajouté dans Menu.jsx
- [ ] Cohérence avec layout system
- [ ] Respect de la nomenclature

### **Documentation ✅**
- [ ] API_ENDPOINTS.md mis à jour
- [ ] DATABASE_SCHEMA.md mis à jour
- [ ] Commit avec référence module
- [ ] Tests documentés

### **Standards ATARYS ✅**
- [ ] Référence module dans tous les fichiers
- [ ] Format API standardisé
- [ ] Composants réutilisables
- [ ] Gestion d'erreurs cohérente
- [ ] Layout variants appropriés

---

## 🎯 **Prochaines Étapes Suggérées**

1. **Module 3.2** - Chantiers à Deviser (workflow spécialisé)
2. **Module 3.3** - Chantiers Signés (suivi contrats)
3. **Module 5.1** - Intégration BATAPPLI (articles et ouvrages)
4. **Module 7.2** - Tableaux de bord (synthèse chantiers)

---

*Template créé selon Nomenclature ATARYS et documentation complète*  
*Référence : docs/INDEX.md, docs/ATARYS_ARCHITECTURE.md, docs/API_ENDPOINTS.md* 