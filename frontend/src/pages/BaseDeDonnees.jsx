import React, { useState, useEffect } from 'react';

const MODULES = [
  { id: 1, label: '1. PLANNING' },
  { id: 2, label: '2. LISTE DES TÂCHES' },
  { id: 3, label: '3. LISTE CHANTIERS' },
  { id: 4, label: '4. CHANTIERS' },
  { id: 5, label: '5. DEVIS-FACTURATION' },
  { id: 6, label: '6. ATELIER' },
  { id: 7, label: '7. GESTION' },
  { id: 8, label: '8. COMPTABILITÉ' },
  { id: 9, label: '9. SOCIAL' },
  { id: 10, label: '10. OUTILS' },
  { id: 11, label: '11. ARCHIVES' },
  { id: 12, label: '12. PARAMÈTRES' },
  { id: 13, label: '13. AIDE' },
];

const COLUMN_TYPES = [
  { value: 'String', label: 'String (texte court)' },
  { value: 'Text', label: 'Text (texte long)' },
  { value: 'Integer', label: 'Integer (nombre entier)' },
  { value: 'Numeric', label: 'Numeric (montant)' },
  { value: 'REAL', label: 'REAL (nombre décimal)' },
  { value: 'Boolean', label: 'Boolean (vrai/faux)' },
  { value: 'Date', label: 'Date' },
  { value: 'DateTime', label: 'DateTime' },
  { value: 'Enum', label: 'Enum (liste de valeurs)' },
  { value: 'ForeignKey', label: 'Clé étrangère' },
];

function BaseDeDonnees() {
  // État du formulaire
  const [tableName, setTableName] = useState('');
  const [moduleId, setModuleId] = useState(12);
  const [columns, setColumns] = useState([
    { name: '', type: 'String', nullable: true, unique: false }
  ]);
  const [tables, setTables] = useState([]);
  const [message, setMessage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('create'); // 'create', 'sync', 'migrations'

  // Nouveaux états pour l'Option 1 professionnelle
  const [migrationStatus, setMigrationStatus] = useState(null);
  const [migrationHelp, setMigrationHelp] = useState(null);
  const [showMigrationInstructions, setShowMigrationInstructions] = useState(false);
  const [migrationInstructions, setMigrationInstructions] = useState(null);

  // Ajout d'un état pour les options globales de la table
  const [tableOptions, setTableOptions] = useState({
    id: true,
    created_at: true,
    updated_at: true,
    autoIncrement: true
  });

  // Ajout d'un état pour les valeurs Enum et ForeignKey de la colonne en cours
  const [enumValues, setEnumValues] = useState([]);
  const [foreignKey, setForeignKey] = useState({ table: '', column: '' });

  // Charger la liste des tables existantes
  useEffect(() => {
    fetch('/api/table-generator/list-tables')
      .then(res => res.json())
      .then(data => {
        if (data.success) setTables(data.data);
      });
  }, []);

  // Charger l'état des migrations au montage
  useEffect(() => {
    checkMigrationStatus();
    getMigrationHelp();
  }, []);

  // Vérifier l'état des migrations
  const checkMigrationStatus = async () => {
    try {
      const res = await fetch('/api/table-generator/check-migrations');
      const data = await res.json();
      setMigrationStatus(data);
    } catch (err) {
      setMigrationStatus({
        success: false,
        message: 'Erreur lors de la vérification des migrations',
        data: { status: 'error', error: err.message }
      });
    }
  };

  // Obtenir l'aide des migrations
  const getMigrationHelp = async () => {
    try {
      const res = await fetch('/api/table-generator/migration-help');
      const data = await res.json();
      setMigrationHelp(data);
    } catch (err) {
      setMigrationHelp({
        success: false,
        message: 'Erreur lors de la récupération de l\'aide',
        data: { error: err.message }
      });
    }
  };

  // Fonction de synchronisation
  const handleSyncAll = async () => {
    setLoading(true);
    setMessage(null);
    try {
      const res = await fetch('/api/table-sync/sync-all', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await res.json();
      if (data.success) {
        setMessage({ type: 'success', text: data.message });
        // Recharger la liste des tables
        fetch('/api/table-generator/list-tables')
          .then(res => res.json())
          .then(data => { if (data.success) setTables(data.data); });
      } else {
        setMessage({ type: 'error', text: data.message });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Erreur réseau ou serveur.' });
    } finally {
      setLoading(false);
    }
  };

  // Gestion dynamique des colonnes
  const handleColumnChange = (idx, field, value) => {
    setColumns(cols => cols.map((col, i) => i === idx ? { ...col, [field]: value } : col));
  };
  const addColumn = () => {
    let newCol = { ...columns[columns.length - 1] };
    if (newCol.type === 'Enum') newCol.enumValues = enumValues.filter(v => v.trim() !== '');
    if (newCol.type === 'ForeignKey') {
      newCol.isForeignKey = true;
      newCol.foreignKeyTable = foreignKey.table;
      newCol.foreignKeyColumn = foreignKey.column;
    }
    setColumns(cols => [...cols, newCol]);
    setEnumValues([]);
    setForeignKey({ table: '', column: '' });
  };
  const removeColumn = idx => setColumns(cols => cols.length > 1 ? cols.filter((_, i) => i !== idx) : cols);

  // Validation frontend
  const validate = () => {
    if (!tableName.match(/^[a-z][a-z0-9_]*$/)) return 'Nom de table invalide (snake_case requis)';
    if (!moduleId) return 'Module requis';
    if (columns.length === 0) return 'Au moins une colonne requise';
    for (const col of columns) {
      if (!col.name.match(/^[a-z][a-z0-9_]*$/)) return `Nom de colonne invalide : ${col.name}`;
      if (!col.type) return `Type manquant pour la colonne : ${col.name}`;
      if (col.type === 'String' && (!col.maxLength || isNaN(Number(col.maxLength)) || Number(col.maxLength) <= 0)) {
        return `Longueur max obligatoire pour la colonne '${col.name}' (type String)`;
      }
    }
    return null;
  };

  // Soumission du formulaire (version professionnelle)
  const handleSubmit = async e => {
    e.preventDefault();
    setMessage(null);
    setShowMigrationInstructions(false);
    setMigrationInstructions(null);
    
    const error = validate();
    if (error) {
      setMessage({ type: 'error', text: error });
      return;
    }
    setLoading(true);
    
    // Construction du payload
    const payload = {
      module_id: moduleId,
      table_name: tableName,
      class_name: tableName.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(''),
      columns: columns.map(col => ({
        ...col,
        enumValues: col.enumValues,
        isForeignKey: col.isForeignKey,
        foreignKeyTable: col.foreignKeyTable,
        foreignKeyColumn: col.foreignKeyColumn
      })),
      options: {
        ...tableOptions
      }
    };
    
    try {
      const res = await fetch('/api/table-generator/create-table', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      
      if (data.success) {
        setMessage({ type: 'success', text: data.message });
        setMigrationInstructions(data.data);
        setShowMigrationInstructions(true);
        
        // Réinitialiser le formulaire
        setTableName('');
        setColumns([{ name: '', type: 'String', nullable: true, unique: false }]);
        
        // Recharger la liste des tables
        fetch('/api/table-generator/list-tables')
          .then(res => res.json())
          .then(data => { if (data.success) setTables(data.data); });
      } else {
        setMessage({ type: 'error', text: data.message });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Erreur réseau ou serveur.' });
    } finally {
      setLoading(false);
    }
  };

  // Fonction de suppression d'une table (version professionnelle)
  const handleDeleteTable = async (tableName) => {
    if (!confirm(`Êtes-vous sûr de vouloir supprimer la table "${tableName}" ?\n\nCette action supprimera définitivement :\n- Le code Python généré (modèle, routes, schéma)\n- Vous devrez ensuite lancer les migrations pour supprimer la table de la base\n\nCette action est irréversible !`)) {
      return;
    }

    setLoading(true);
    setMessage(null);
    setShowMigrationInstructions(false);
    setMigrationInstructions(null);
    
    try {
      const res = await fetch('/api/table-generator/delete-table', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ table_name: tableName })
      });
      const data = await res.json();
      
      if (data.success) {
        setMessage({ type: 'success', text: data.message });
        setMigrationInstructions(data.data);
        setShowMigrationInstructions(true);
        
        // Recharger la liste des tables
        fetch('/api/table-generator/list-tables')
          .then(res => res.json())
          .then(data => { if (data.success) setTables(data.data); });
      } else {
        setMessage({ type: 'error', text: data.message });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Erreur réseau ou serveur.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Base de Données (Module 12.1)</h1>
      
      {/* Onglets */}
      <div className="mb-6">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('create')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'create'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Créer Table
            </button>
            <button
              onClick={() => setActiveTab('sync')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'sync'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Synchroniser
            </button>
            <button
              onClick={() => setActiveTab('migrations')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'migrations'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Migrations
            </button>
          </nav>
        </div>
      </div>

      {message && (
        <div className={`mb-4 p-2 rounded ${message.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
          {message.text}
        </div>
      )}

      {/* Instructions de migration */}
      {showMigrationInstructions && migrationInstructions && (
        <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded">
          <h3 className="font-semibold text-blue-900 mb-2">📋 Instructions de Migration</h3>
          <div className="text-blue-800 text-sm space-y-2">
            <p><strong>Prochaines étapes :</strong></p>
            <ul className="list-disc list-inside space-y-1">
              {migrationInstructions.next_steps?.map((step, idx) => (
                <li key={idx} className="font-mono bg-blue-100 px-2 py-1 rounded">{step}</li>
              ))}
            </ul>
            {migrationInstructions.warning && (
              <p className="mt-2 text-orange-700 font-medium">⚠️ {migrationInstructions.warning}</p>
            )}
            <button
              onClick={() => setShowMigrationInstructions(false)}
              className="mt-2 px-3 py-1 bg-blue-600 text-white rounded text-xs hover:bg-blue-700"
            >
              Fermer
            </button>
          </div>
        </div>
      )}

      {/* Onglet Créer Table */}
      {activeTab === 'create' && (
        <form onSubmit={handleSubmit} className="bg-white shadow p-4 rounded mb-8">
          <h2 className="text-lg font-semibold mb-2">Créer une nouvelle table (Version Professionnelle)</h2>
          <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded">
            <p className="text-yellow-800 text-sm">
              <strong>ℹ️ Nouveau workflow :</strong> Le générateur crée le code Python, puis vous devez lancer les migrations pour créer la table dans la base de données.
            </p>
          </div>
          
          {/* Options avancées : cases à cocher pour id, created_at, updated_at */}
          <div className="mb-4 flex gap-6">
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={tableOptions.id} onChange={e => setTableOptions(opts => ({ ...opts, id: e.target.checked }))} />
              <span>Colonne <code>id</code> (clé primaire auto-incrémentée)</span>
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={tableOptions.created_at} onChange={e => setTableOptions(opts => ({ ...opts, created_at: e.target.checked }))} />
              <span>Colonne <code>created_at</code> (date création)</span>
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={tableOptions.updated_at} onChange={e => setTableOptions(opts => ({ ...opts, updated_at: e.target.checked }))} />
              <span>Colonne <code>updated_at</code> (date modification)</span>
            </label>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block font-medium">Nom de la table</label>
              <input type="text" className="border p-2 rounded w-full" value={tableName} onChange={e => setTableName(e.target.value)} placeholder="ex: essai_table1" required />
            </div>
            <div>
              <label className="block font-medium">Module ATARYS</label>
              <select className="border p-2 rounded w-full" value={moduleId} onChange={e => setModuleId(Number(e.target.value))}>
                {MODULES.map(m => <option key={m.id} value={m.id}>{m.label}</option>)}
              </select>
            </div>
          </div>
          <div className="mt-4">
            <label className="block font-medium mb-2">Colonnes</label>
            {columns.map((col, idx) => (
              <div key={idx} className="flex gap-2 mb-2 items-center">
                <input type="text" className="border p-2 rounded flex-1" placeholder="nom_colonne" value={col.name} onChange={e => handleColumnChange(idx, 'name', e.target.value)} required />
                <select className="border p-2 rounded" value={col.type} onChange={e => handleColumnChange(idx, 'type', e.target.value)}>
                  {COLUMN_TYPES.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
                </select>
                {col.type === 'Enum' && (
                  <div className="flex flex-col gap-1 ml-4">
                    <label className="text-xs">Valeurs Enum (une par ligne)</label>
                    <textarea
                      className="border p-1 rounded"
                      rows={2}
                      value={enumValues.join('\n')}
                      onChange={e => setEnumValues(e.target.value.split('\n'))}
                      placeholder="ex: Brouillon\nValidé\nArchivé"
                    />
                  </div>
                )}
                {col.type === 'ForeignKey' && (
                  <div className="flex flex-col gap-1 ml-4">
                    <label className="text-xs">Table cible</label>
                    <input
                      className="border p-1 rounded"
                      value={foreignKey.table}
                      onChange={e => setForeignKey(fk => ({ ...fk, table: e.target.value }))}
                      placeholder="ex: users"
                    />
                    <label className="text-xs">Colonne cible</label>
                    <input
                      className="border p-1 rounded"
                      value={foreignKey.column}
                      onChange={e => setForeignKey(fk => ({ ...fk, column: e.target.value }))}
                      placeholder="ex: id"
                    />
                  </div>
                )}
                {col.type === 'String' && (
                  <div className="flex flex-col gap-1 ml-4">
                    <label className="text-xs">Longueur max</label>
                    <input
                      type="number"
                      min={1}
                      className="border p-1 rounded w-24"
                      value={col.maxLength || ''}
                      onChange={e => handleColumnChange(idx, 'maxLength', e.target.value)}
                      placeholder="ex: 100"
                      required
                    />
                  </div>
                )}
                <label className="flex items-center gap-1 text-sm"><input type="checkbox" checked={col.nullable} onChange={e => handleColumnChange(idx, 'nullable', e.target.checked)} />Nullable</label>
                <label className="flex items-center gap-1 text-sm"><input type="checkbox" checked={col.unique} onChange={e => handleColumnChange(idx, 'unique', e.target.checked)} />Unique</label>
                <button type="button" className="text-red-600 px-2" onClick={() => removeColumn(idx)} title="Supprimer">✕</button>
              </div>
            ))}
            <button type="button" className="mt-2 px-3 py-1 bg-gray-200 rounded" onClick={addColumn}>+ Ajouter une colonne</button>
          </div>
          <button type="submit" className="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700" disabled={loading}>{loading ? 'Génération...' : 'Générer le code'}</button>
        </form>
      )}

      {/* Onglet Synchroniser */}
      {activeTab === 'sync' && (
        <div className="bg-white shadow p-4 rounded mb-8">
          <h2 className="text-lg font-semibold mb-4">Synchroniser avec SQLite Studio</h2>
          <div className="bg-blue-50 border border-blue-200 rounded p-4 mb-4">
            <h3 className="font-semibold text-blue-900 mb-2">Instructions :</h3>
            <ol className="text-blue-800 text-sm space-y-1">
              <li>1. Ouvrir <code className="bg-blue-100 px-1 rounded">data/atarys_data.db</code> dans SQLite Studio</li>
              <li>2. Modifier la structure des tables (ajouter/supprimer colonnes)</li>
              <li>3. Sauvegarder les modifications</li>
              <li>4. Cliquer sur "Synchroniser Backend" ci-dessous</li>
            </ol>
          </div>
          <button 
            onClick={handleSyncAll}
            disabled={loading}
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50"
          >
            {loading ? 'Synchronisation...' : '🔄 Synchroniser Backend'}
          </button>
        </div>
      )}

      {/* Nouvel onglet Migrations */}
      {activeTab === 'migrations' && (
        <div className="bg-white shadow p-4 rounded mb-8">
          <h2 className="text-lg font-semibold mb-4">Gestion des Migrations Flask-Migrate</h2>
          
          {/* État des migrations */}
          <div className="mb-6">
            <h3 className="font-semibold mb-2">État des migrations</h3>
            {migrationStatus ? (
              <div className={`p-3 rounded ${migrationStatus.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                <p className={migrationStatus.success ? 'text-green-800' : 'text-red-800'}>
                  {migrationStatus.message}
                </p>
                {migrationStatus.data?.current_revision && (
                  <p className="text-sm mt-1 font-mono bg-gray-100 px-2 py-1 rounded">
                    Révision actuelle : {migrationStatus.data.current_revision}
                  </p>
                )}
                {migrationStatus.data?.next_steps && (
                  <div className="mt-2">
                    <p className="text-sm font-medium">Prochaines étapes :</p>
                    <ul className="list-disc list-inside text-sm space-y-1">
                      {migrationStatus.data.next_steps.map((step, idx) => (
                        <li key={idx} className="font-mono bg-gray-100 px-2 py-1 rounded">{step}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ) : (
              <div className="p-3 bg-gray-50 border border-gray-200 rounded">
                <p className="text-gray-600">Chargement de l'état des migrations...</p>
              </div>
            )}
          </div>

          {/* Aide des migrations */}
          <div className="mb-6">
            <h3 className="font-semibold mb-2">Guide des migrations</h3>
            {migrationHelp ? (
              <div className="bg-blue-50 border border-blue-200 rounded p-4">
                <h4 className="font-semibold text-blue-900 mb-2">Workflow professionnel :</h4>
                <ol className="text-blue-800 text-sm space-y-1 mb-4">
                  {migrationHelp.data?.workflow?.map((step, idx) => (
                    <li key={idx}>{step}</li>
                  ))}
                </ol>
                
                <h4 className="font-semibold text-blue-900 mb-2">Commandes principales :</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
                  {migrationHelp.data?.commands && Object.entries(migrationHelp.data.commands).map(([key, cmd]) => (
                    <div key={key} className="bg-blue-100 p-2 rounded">
                      <code className="font-mono text-blue-900">{cmd}</code>
                    </div>
                  ))}
                </div>
                
                <h4 className="font-semibold text-blue-900 mb-2 mt-4">Bonnes pratiques :</h4>
                <ul className="text-blue-800 text-sm space-y-1">
                  {migrationHelp.data?.tips?.map((tip, idx) => (
                    <li key={idx}>{tip}</li>
                  ))}
                </ul>
              </div>
            ) : (
              <div className="p-3 bg-gray-50 border border-gray-200 rounded">
                <p className="text-gray-600">Chargement de l'aide...</p>
              </div>
            )}
          </div>

          {/* Boutons d'action */}
          <div className="flex gap-2">
            <button
              onClick={checkMigrationStatus}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              🔄 Actualiser l'état
            </button>
            <button
              onClick={getMigrationHelp}
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            >
              📚 Actualiser l'aide
            </button>
          </div>
        </div>
      )}

      <div className="bg-white shadow p-4 rounded">
        <h2 className="text-lg font-semibold mb-2">Tables existantes</h2>
        <table className="w-full text-sm border">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2 border">Nom</th>
              <th className="p-2 border">Module</th>
              <th className="p-2 border">Colonnes</th>
              <th className="p-2 border">Créée</th>
              <th className="p-2 border">Actions</th>
            </tr>
          </thead>
          <tbody>
            {tables.length === 0 && <tr><td colSpan={5} className="text-center p-4">Aucune table générée</td></tr>}
            {tables.map((t, idx) => (
              <tr key={idx}>
                <td className="border p-2">{t.name}</td>
                <td className="border p-2">{t.module}</td>
                <td className="border p-2">{t.columns ? t.columns.length : '-'}</td>
                <td className="border p-2">
                  {t.created_at && t.created_at !== '-' && !isNaN(new Date(t.created_at.replace(' ', 'T') + 'Z'))
                    ? new Date(t.created_at.replace(' ', 'T') + 'Z').toLocaleString()
                    : '-'}
                </td>
                <td className="border p-2">
                  <button
                    type="button"
                    className="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700 text-xs"
                    onClick={() => handleDeleteTable(t.name)}
                    disabled={loading}
                    title="Supprimer le code généré (puis lancer les migrations)"
                  >
                    {loading ? '...' : '🗑️ Supprimer'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default BaseDeDonnees; 