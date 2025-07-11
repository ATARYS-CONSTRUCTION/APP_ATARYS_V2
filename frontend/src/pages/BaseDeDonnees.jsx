import React, { useState } from 'react';
import { PageLayout, Card } from '../components/Layout';

// Exemple de structure des modules et tables (à remplacer par une récupération dynamique plus tard)
const MODULES = [
  {
    id: 1,
    nom: '1. Planning',
    tables: [
      { name: 'planning_salaries', label: 'Planning Salariés' },
      { name: 'planning_chantiers', label: 'Planning Chantiers' },
    ],
  },
  {
    id: 5,
    nom: '5. Devis-Facturation',
    tables: [
      { name: 'articles_atarys', label: 'Articles ATARYS' },
      { name: 'devis', label: 'Devis' },
    ],
  },
  {
    id: 12,
    nom: '12. Paramètres',
    tables: [
      { name: 'parametres_generaux', label: 'Paramètres Généraux' },
      { name: 'utilisateurs', label: 'Utilisateurs' },
    ],
  },
  // ... autres modules
];

// Placeholder pour les colonnes et données (à remplacer par l'appel API)
const COLUMNS_EXEMPLE = [
  { key: 'reference', label: 'Référence' },
  { key: 'libelle', label: 'Libellé' },
  { key: 'prix_achat', label: 'Prix Achat' },
  { key: 'coefficient', label: 'Coefficient' },
  { key: 'prix_unitaire', label: 'Prix Unitaire' },
];
const DATA_EXEMPLE = [
  { reference: 'ARD1', libelle: 'Ardoise 32x22', prix_achat: 1.15, coefficient: 1.3, prix_unitaire: 1.5 },
  { reference: 'ARD2', libelle: 'Ardoise 40x22', prix_achat: 1.7, coefficient: 1.3, prix_unitaire: 2.21 },
];

export default function BaseDeDonnees() {
  // Sélection de la table
  const [selectedTable, setSelectedTable] = useState(MODULES[0].tables[0].name);
  // Données du tableau (à remplacer par l'appel API)
  const [data, setData] = useState(DATA_EXEMPLE);

  // Gestion du collage Excel (collage dans le premier champ du tableau)
  const handlePaste = (e) => {
    const clipboard = e.clipboardData.getData('text');
    const rows = clipboard.split('\n').filter(Boolean);
    const newData = rows.map(row => {
      const values = row.split('\t'); // Collage Excel = tabulation
      const obj = {};
      COLUMNS_EXEMPLE.forEach((col, idx) => {
        obj[col.key] = values[idx] || '';
      });
      return obj;
    });
    setData([...data, ...newData]);
    e.preventDefault();
  };

  // Edition directe
  const handleChange = (rowIdx, key, value) => {
    const newData = [...data];
    newData[rowIdx][key] = value;
    setData(newData);
  };

  // Placeholder pour l'enregistrement (à brancher sur l'API)
  const handleSave = () => {
    alert('Enregistrement (à brancher sur l\'API)');
  };

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
        </div>
        <div className="overflow-x-auto">
          <table
            className="min-w-full border text-sm"
            onPaste={handlePaste}
          >
            <thead>
              <tr>
                {COLUMNS_EXEMPLE.map(col => (
                  <th key={col.key} className="px-3 py-2 bg-gray-100 border-b text-left font-semibold">{col.label}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, rowIdx) => (
                <tr key={rowIdx}>
                  {COLUMNS_EXEMPLE.map(col => (
                    <td key={col.key} className="border-b px-3 py-2">
                      <input
                        className="w-full bg-transparent outline-none"
                        value={row[col.key] || ''}
                        onChange={e => handleChange(rowIdx, col.key, e.target.value)}
                      />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="flex justify-end mt-4">
          <button
            className="bg-blue-600 text-white px-6 py-2 rounded shadow hover:bg-blue-700 font-semibold"
            onClick={handleSave}
          >
            Enregistrer
          </button>
        </div>
        <div className="text-xs text-gray-500 mt-2">
          <ul className="list-disc ml-5">
            <li>Copiez-collez directement depuis Excel (tabulation supportée).</li>
            <li>Classement des tables par module selon la documentation ATARYS.</li>
            <li>Respecte le layout et les standards UI/UX ATARYS.</li>
          </ul>
        </div>
      </Card>
    </PageLayout>
  );
} 