import React, { useState, useEffect } from 'react';
import { PageLayout, Card } from '../components/Layout';
import AddRowForm from '../components/AddRowForm';
import CreateTableForm from '../components/CreateTableForm';

// Configuration API ATARYS
const API_BASE_URL = 'http://localhost:5000/api';

// Structure des modules et tables ATARYS
const MODULES = [
  {
    id: 5,
    nom: '5. Devis-Facturation',
    tables: [
      { name: 'articles_atarys', label: 'Articles ATARYS', apiEndpoint: '/articles-atarys' },
    ],
  },
  // Autres modules à ajouter au fur et à mesure
];

// Colonnes pour articles_atarys (selon le modèle SQLAlchemy)
const COLUMNS_ARTICLES_ATARYS = [
  { key: 'reference', label: 'Référence', type: 'text' },
  { key: 'libelle', label: 'Libellé', type: 'text' },
  { key: 'prix_achat', label: 'Prix Achat', type: 'number' },
  { key: 'coefficient', label: 'Coefficient', type: 'number' },
  { key: 'prix_unitaire', label: 'Prix Unitaire', type: 'number' },
  { key: 'unite', label: 'Unité', type: 'text' },
  { key: 'tva_pct', label: 'TVA %', type: 'number' },
  { key: 'famille', label: 'Famille', type: 'text' },
  { key: 'actif', label: 'Actif', type: 'boolean' },
];

export default function BaseDeDonnees() {
  const [selectedTable, setSelectedTable] = useState('articles_atarys');
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);
  // Ajout d'un état pour annuler le dernier collage
  const [previousData, setPreviousData] = useState(null);
  // Ajout d'un état pour gérer l'ajout de lignes
  const [showAddForm, setShowAddForm] = useState(false);
  // Ajout d'un état pour gérer l'affichage du formulaire de création de table
  const [showCreateTableForm, setShowCreateTableForm] = useState(false);

  // Récupérer les colonnes selon la table sélectionnée
  const getColumnsForTable = (tableName) => {
    switch (tableName) {
      case 'articles_atarys':
        return COLUMNS_ARTICLES_ATARYS;
      default:
        return [];
    }
  };

  // Charger les données depuis l'API
  const loadData = async () => {
    const selectedModule = MODULES.find(m => m.tables.some(t => t.name === selectedTable));
    const table = selectedModule?.tables.find(t => t.name === selectedTable);
    
    if (!table?.apiEndpoint) {
      setError('API non disponible pour cette table');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      // Récupérer toutes les données avec une limite élevée
      const response = await fetch(`${API_BASE_URL}${table.apiEndpoint}/?per_page=1000`);
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }
      const result = await response.json();
      
      if (result.success) {
        setData(result.data || []);
        console.log(`📊 Chargé ${result.data?.length || 0} lignes depuis l'API`);
      } else {
        setError(result.message || 'Erreur lors du chargement');
      }
    } catch (err) {
      setError(`Erreur de connexion: ${err.message}`);
      console.error('Erreur API:', err);
    } finally {
      setLoading(false);
    }
  };

  // Charger les données au changement de table ou au montage
  useEffect(() => {
    loadData();
  }, [selectedTable]);

  // Gestion du collage Excel (collage dans le tableau)
  const handlePaste = (e) => {
    setPreviousData(data); // Sauvegarde l'état avant collage
    let clipboard = e.clipboardData.getData('text');
    // Remplace les retours à la ligne internes dans les cellules Excel (entre guillemets) par un espace
    clipboard = clipboard.replace(/"([^"]*)"/g, (match) => match.replace(/\r?\n/g, ' '));
    const rows = clipboard.split('\n').filter(Boolean);
    const columns = getColumnsForTable(selectedTable);
    let error = null;
    const newData = rows.map((row, rowIdx) => {
      const values = row.split('\t');
      if (values.length > columns.length) {
        error = 'Trop de colonnes dans la ligne ' + (rowIdx + 1);
      }
      const obj = {};
      columns.forEach((col, idx) => {
        let val = values[idx] || '';
        // Nettoyage automatique des guillemets et espaces
        if (typeof val === 'string') {
          val = val.trim().replace(/^"|"$/g, '');
        }
        if (col.type === 'boolean') {
          obj[col.key] = val === '1' || val.toLowerCase() === 'true' || val === 'oui';
        } else if (col.type === 'number') {
          obj[col.key] = val !== '' ? Number(val.replace(',', '.')) : '';
        } else {
          obj[col.key] = val;
        }
      });
      return obj;
    });

    if (error) {
      setError(error);
      e.preventDefault();
      return;
    }

    // Filtrer les lignes complètement vides
    const validNewData = newData.filter(row => {
      if (selectedTable === 'articles_atarys') {
        // Pour articles_atarys, vérifier que reference et libelle ne sont pas vides
        return row.reference && row.reference.toString().trim() !== '' && 
               row.libelle && row.libelle.toString().trim() !== '';
      }
      // Pour les autres tables, vérifier qu'au moins un champ n'est pas vide
      return Object.values(row).some(val => val !== '' && val !== null && val !== undefined);
    });

    if (validNewData.length === 0) {
      setError('Aucune donnée valide dans le collage (lignes vides ignorées)');
      e.preventDefault();
      return;
    }

    setData([...data, ...validNewData]);
    e.preventDefault();
  };

  // Annuler le dernier collage
  const handleUndoPaste = () => {
    if (previousData) {
      setData(previousData);
      setPreviousData(null);
    }
  };

  // Supprimer les lignes vides
  const handleRemoveEmptyRows = () => {
    const filteredData = data.filter(row => {
      if (selectedTable === 'articles_atarys') {
        return row.reference && row.reference.toString().trim() !== '' && 
               row.libelle && row.libelle.toString().trim() !== '';
      }
      return Object.values(row).some(val => val !== '' && val !== null && val !== undefined);
    });
    setData(filteredData);
  };

  // Supprimer toutes les données de la table (backend + frontend)
  const handleDeleteAll = async () => {
    const selectedModule = MODULES.find(m => m.tables.some(t => t.name === selectedTable));
    const table = selectedModule?.tables.find(t => t.name === selectedTable);
    if (!table?.apiEndpoint) {
      setError('API non disponible pour cette table');
      return;
    }
    if (!window.confirm('Voulez-vous vraiment supprimer toutes les données ? Cette action est irréversible.')) {
      return;
    }
    setSaving(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}${table.apiEndpoint}/clear/`, {
        method: 'DELETE',
      });
      const result = await response.json();
      if (result.success) {
        setData([]);
        alert(result.message || 'Toutes les données ont été supprimées.');
      } else {
        setError(result.message || 'Erreur lors de la suppression.');
      }
    } catch (err) {
      setError(`Erreur lors de la suppression: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  // Ajouter une ligne vide
  const handleAddRow = () => {
    setShowAddForm(true);
  };

  // Gérer l'ajout d'une ligne via le formulaire
  const handleAddRowFromForm = (newRowData) => {
    setData([...data, newRowData]);
    setShowAddForm(false);
  };

  // Annuler l'ajout de ligne
  const handleCancelAddRow = () => {
    setShowAddForm(false);
  };

  // Gérer la création de table
  const handleCreateTable = () => {
    setShowCreateTableForm(true);
  };

  // Gérer la création de table terminée
  const handleTableCreated = (tableData) => {
    setShowCreateTableForm(false);
    // Recharger les données pour inclure la nouvelle table
    loadData();
    alert(`Table "${tableData.tableName}" créée avec succès !`);
  };

  // Annuler la création de table
  const handleCancelCreateTable = () => {
    setShowCreateTableForm(false);
  };

  // Edition directe
  const handleChange = (rowIdx, key, value) => {
    const newData = [...data];
    newData[rowIdx][key] = value;
    setData(newData);
  };

  // Enregistrer les modifications via l'API
  const handleSave = async () => {
    const selectedModule = MODULES.find(m => m.tables.some(t => t.name === selectedTable));
    const table = selectedModule?.tables.find(t => t.name === selectedTable);
    
    if (!table?.apiEndpoint) {
      setError('API non disponible pour cette table');
      return;
    }

    setSaving(true);
    setError(null);
    
    try {
      // Filtrer les lignes vides et valider les données
      const validData = data.filter(item => {
        // Vérifier que les champs obligatoires ne sont pas vides
        if (selectedTable === 'articles_atarys') {
          return item.reference && item.reference.trim() !== '' && 
                 item.libelle && item.libelle.trim() !== '';
        }
        return true; // Pour les autres tables
      });

      if (validData.length === 0) {
        setError('Aucune donnée valide à enregistrer');
        setSaving(false);
        return;
      }

      // Nettoyer et valider les données avant envoi
      const cleanedData = validData.map(item => {
        const cleaned = { ...item };
        
        // Nettoyer les chaînes vides
        Object.keys(cleaned).forEach(key => {
          if (typeof cleaned[key] === 'string' && cleaned[key].trim() === '') {
            delete cleaned[key]; // Supprimer les champs vides
          }
        });

        // Convertir les types numériques
        if (cleaned.prix_achat !== undefined) {
          cleaned.prix_achat = Number(cleaned.prix_achat) || 0;
        }
        if (cleaned.coefficient !== undefined) {
          cleaned.coefficient = Number(cleaned.coefficient) || 1;
        }
        if (cleaned.prix_unitaire !== undefined) {
          cleaned.prix_unitaire = Number(cleaned.prix_unitaire) || 0;
        }
        if (cleaned.tva_pct !== undefined) {
          cleaned.tva_pct = Number(cleaned.tva_pct) || 20;
        }

        // Convertir les booléens
        if (cleaned.actif !== undefined) {
          cleaned.actif = Boolean(cleaned.actif);
        }

        return cleaned;
      });

      // Envoyer les données nettoyées
      const promises = cleanedData.map(async (item) => {
        if (item.id) {
          // Mise à jour
          const response = await fetch(`${API_BASE_URL}${table.apiEndpoint}/${item.id}/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(item)
          });
          return response.json();
        } else {
          // Création
          const response = await fetch(`${API_BASE_URL}${table.apiEndpoint}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(item)
          });
          return response.json();
        }
      });
      
      const results = await Promise.all(promises);
      const errors = results.filter(r => !r.success);
      
      if (errors.length > 0) {
        console.error('Erreurs API:', errors);
        setError(`Erreurs lors de l'enregistrement: ${errors.length} erreur(s)`);
      } else {
        // Recharger les données après sauvegarde
        await loadData();
        alert('Données enregistrées avec succès');
      }
    } catch (err) {
      console.error('Erreur de sauvegarde:', err);
      setError(`Erreur lors de l'enregistrement: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  const columns = getColumnsForTable(selectedTable);
  // Toujours afficher au moins une ligne vide si la table est vide
  const displayData = data.length === 0 ? [Object.fromEntries(columns.map(col => [col.key, '']))] : data;

  return (
    <PageLayout title="Base de données (12.1)" variant="wide">
      <Card>
        <div className="flex flex-col md:flex-row md:items-center gap-3 mb-4">
          <label htmlFor="table-select" className="font-semibold text-gray-700">Table à éditer :</label>
          <select
            id="table-select"
            className="border rounded px-3 py-2"
            value={selectedTable}
            onChange={e => setSelectedTable(e.target.value)}
          >
            {MODULES.map(module => (
              <optgroup key={module.id} label={module.nom}>
                {module.tables.map(table => (
                  <option key={table.name} value={table.name}>{table.label}</option>
                ))}
              </optgroup>
            ))}
          </select>
          
          {/* Bouton Ajouter une ligne */}
          <button
            className="bg-green-600 text-white px-4 py-2 rounded shadow hover:bg-green-700 font-semibold flex items-center gap-2"
            onClick={handleAddRow}
          >
            <span>➕</span>
            Ajouter une ligne
          </button>
          
          {/* Bouton Créer une table */}
          <button
            className="bg-purple-600 text-white px-4 py-2 rounded shadow hover:bg-purple-700 font-semibold flex items-center gap-2"
            onClick={handleCreateTable}
          >
            <span>🏗️</span>
            Créer une table
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded text-red-700">
            {error}
          </div>
        )}

        {loading ? (
          <div className="text-center py-8">
            <div className="text-gray-500">Chargement des données...</div>
          </div>
        ) : (
          <div>
            {/* Compteur de lignes amélioré */}
            <div className="mb-4 p-3 bg-gradient-to-r from-blue-50 to-blue-100 border-2 border-blue-300 rounded-lg shadow-sm">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">📊</span>
                  <div>
                    <div className="font-bold text-blue-900 text-lg">
                      {data.length} ligne{data.length > 1 ? 's' : ''} dans la table
                    </div>
                    {data.length > 0 && (
                      <div className="text-blue-700 text-sm">
                        Dont {data.filter(row => {
                          if (selectedTable === 'articles_atarys') {
                            return row.reference && row.reference.toString().trim() !== '' && 
                                   row.libelle && row.libelle.toString().trim() !== '';
                          }
                          return Object.values(row).some(val => val !== '' && val !== null && val !== undefined);
                        }).length} ligne{data.filter(row => {
                          if (selectedTable === 'articles_atarys') {
                            return row.reference && row.reference.toString().trim() !== '' && 
                                   row.libelle && row.libelle.toString().trim() !== '';
                          }
                          return Object.values(row).some(val => val !== '' && val !== null && val !== undefined);
                        }).length > 1 ? 's' : ''} avec données
                      </div>
                    )}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-xs text-blue-600 font-medium">
                    Table: {selectedTable}
                  </div>
                  <div className="text-xs text-blue-500">
                    {columns.length} colonne{columns.length > 1 ? 's' : ''}
                  </div>
                </div>
              </div>
            </div>
            
            <div className="overflow-x-auto">
              <table
                className="min-w-full border text-sm"
                onPaste={handlePaste}
              >
                <thead>
                  <tr>
                    {columns.map(col => (
                      <th key={col.key} className="px-3 py-2 bg-gray-100 border-b text-left font-semibold">{col.label}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {displayData.map((row, rowIdx) => (
                    <tr key={rowIdx}>
                      {columns.map(col => (
                        <td key={col.key} className="border-b px-3 py-2">
                          <input
                            className="w-full bg-transparent outline-none"
                            value={row[col.key] || ''}
                            onChange={e => handleChange(rowIdx, col.key, e.target.value)}
                            type={col.type === 'number' ? 'number' : col.type === 'boolean' ? 'checkbox' : 'text'}
                          />
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        <div className="flex justify-end mt-4 gap-3">
          {previousData && (
            <button
              className="bg-gray-300 text-gray-800 px-6 py-2 rounded shadow hover:bg-gray-400 font-semibold"
              onClick={handleUndoPaste}
            >
              Annuler le dernier collage
            </button>
          )}
          <button
            className="bg-yellow-500 text-white px-6 py-2 rounded shadow hover:bg-yellow-600 font-semibold"
            onClick={handleRemoveEmptyRows}
          >
            Nettoyer lignes vides
          </button>
          <button
            className="bg-red-600 text-white px-6 py-2 rounded shadow hover:bg-red-700 font-semibold"
            onClick={handleDeleteAll}
            disabled={saving || loading}
          >
            Supprimer toutes les données
          </button>
          <button
            className="bg-blue-600 text-white px-6 py-2 rounded shadow hover:bg-blue-700 font-semibold disabled:opacity-50"
            onClick={handleSave}
            disabled={saving || loading}
          >
            {saving ? 'Enregistrement...' : 'Enregistrer'}
          </button>
        </div>

        <div className="text-xs text-gray-500 mt-2">
          <ul className="list-disc ml-5">
            <li>Données chargées depuis l'API backend ATARYS.</li>
            <li>Copiez-collez directement depuis Excel (tabulation supportée).</li>
            <li>Classement des tables par module selon la documentation ATARYS.</li>
            <li>Respecte le layout et les standards UI/UX ATARYS.</li>
          </ul>
        </div>
      </Card>
      
      {/* Formulaire d'ajout de ligne */}
      {showAddForm && (
        <AddRowForm
          onAdd={handleAddRowFromForm}
          onCancel={handleCancelAddRow}
        />
      )}
      
      {/* Formulaire de création de table */}
      {showCreateTableForm && (
        <CreateTableForm
          onCancel={handleCancelCreateTable}
          onTableCreated={handleTableCreated}
        />
      )}
    </PageLayout>
  );
} 