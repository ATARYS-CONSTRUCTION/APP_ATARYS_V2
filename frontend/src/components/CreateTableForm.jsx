import React, { useState } from 'react';

// Modules ATARYS selon le script
const MODULES_ATARYS = {
  1: "PLANNING",
  2: "LISTE_DES_TACHES", 
  3: "LISTE_CHANTIERS",
  4: "CHANTIERS",
  5: "DEVIS_FACTURATION",
  6: "ATELIER",
  7: "GESTION",
  8: "COMPTABILITE",
  9: "SOCIAL",
  10: "OUTILS",
  11: "ARCHIVES",
  12: "PARAMETRES",
  13: "AIDE"
};

// Types de données selon le script
const TYPES = [
  { id: "Integer", label: "Nombre entier (Integer)", sql: "db.Integer" },
  { id: "String", label: "Texte court (String)", sql: "db.String" },
  { id: "Text", label: "Texte long (Text)", sql: "db.Text" },
  { id: "Numeric", label: "Montant financier (Numeric(10,2))", sql: "db.Numeric(10, 2)" },
  { id: "REAL", label: "Nombre décimal (REAL)", sql: "db.Float" },
  { id: "Boolean", label: "Vrai/Faux (Boolean)", sql: "db.Boolean" },
  { id: "Date", label: "Date seulement (Date)", sql: "db.Date" },
  { id: "DateTime", label: "Date/Heure (DateTime)", sql: "db.DateTime" },
  { id: "Time", label: "Heure seulement (Time)", sql: "db.Time" },
  { id: "Timestamp", label: "Horodatage (Timestamp)", sql: "db.Timestamp" },
  { id: "JSON", label: "Données JSON (JSON)", sql: "db.JSON" },
  { id: "LargeBinary", label: "Données binaires (LargeBinary)", sql: "db.LargeBinary" },
  { id: "Enum", label: "Liste de valeurs (Enum)", sql: "db.Enum" }
];

// Suggestions intelligentes selon le script
const SUGGESTIONS = {
  "actif": { type: "Boolean", cdefault: true, description: "Actif par défaut" },
  "active": { type: "Boolean", default: true, description: "Actif par défaut" },
  "enabled": { type: "Boolean", default: true, description: "Activé par défaut" },
  "visible": { type: "Boolean", default: true, description: "Visible par défaut" },
  "status": { type: "String", default: "actif", description: "Statut actif par défaut" },
  "etat": { type: "String", default: "actif", description: "État actif par défaut" },
  "date_creation": { type: "Date", default: "datetime.date.today", description: "Date de création aujourd'hui" },
  "date_import": { type: "Date", default: "datetime.date.today", description: "Date d'import aujourd'hui" },
  "date_maj": { type: "Date", default: "datetime.date.today", description: "Date de mise à jour aujourd'hui" },
  "date_modification": { type: "Date", default: "datetime.date.today", description: "Date de modification aujourd'hui" },
  "created_at": { type: "DateTime", default: "datetime.datetime.utcnow", description: "Horodatage de création" },
  "updated_at": { type: "DateTime", default: "datetime.datetime.utcnow", description: "Horodatage de mise à jour" },
  "timestamp": { type: "DateTime", default: "datetime.datetime.utcnow", description: "Horodatage actuel" },
  "prix_ht": { type: "Numeric", default: "0.00", description: "Prix HT à zéro" },
  "montant_ht": { type: "Numeric", default: "0.00", description: "Montant HT à zéro" },
  "tva_pct": { type: "Numeric", default: "20.00", description: "TVA 20% par défaut" },
  "coefficient": { type: "Numeric", default: "1.00", description: "Coefficient neutre" },
  "quantite": { type: "Integer", default: "0", description: "Quantité à zéro" },
  "stock": { type: "Integer", default: "0", description: "Stock à zéro" },
  "compteur": { type: "Integer", default: "0", description: "Compteur à zéro" },
  "description": { type: "Text", default: '""', description: "Description vide" },
  "notes": { type: "Text", default: '""', description: "Notes vides" },
  "commentaire": { type: "Text", default: '""', description: "Commentaire vide" }
};

// Fonction pour convertir PascalCase en snake_case
const pascalToSnake = (pascalCase) => {
  return pascalCase.replace(/([A-Z])/g, '_$1').toLowerCase().replace(/^_/, '');
};

// Fonction pour suggérer un type selon le nom de colonne
const suggestTypeForColumn = (colName) => {
  const lowerName = colName.toLowerCase();
  
  // Correspondance exacte
  if (SUGGESTIONS[lowerName]) {
    return SUGGESTIONS[lowerName];
  }
  
  // Correspondance partielle
  for (const [key, suggestion] of Object.entries(SUGGESTIONS)) {
    if (lowerName.includes(key)) {
      return suggestion;
    }
  }
  
  return null;
};

export default function CreateTableForm({ onCancel, onTableCreated }) {
  const [step, setStep] = useState(1);
  const [tableData, setTableData] = useState({
    moduleId: 12,
    className: '',
    tableName: '',
    columns: []
  });
  const [currentColumn, setCurrentColumn] = useState({
    name: '',
    type: 'String',
    nullable: false,
    unique: false,
    default: '',
    maxLength: '100',
    isForeignKey: false,
    foreignKeyTarget: '',
    foreignKeyColumn: 'id'
  });

  const handleModuleChange = (moduleId) => {
    setTableData(prev => ({ ...prev, moduleId: parseInt(moduleId) }));
  };

  const handleClassNameChange = (className) => {
    const tableName = pascalToSnake(className);
    setTableData(prev => ({ 
      ...prev, 
      className, 
      tableName 
    }));
  };

  const handleAddColumn = () => {
    if (!currentColumn.name) return;

    // Vérifier que ce n'est pas 'id' (déjà ajouté automatiquement)
    if (currentColumn.name.toLowerCase() === 'id') {
      alert('La colonne "id" est ajoutée automatiquement (clé primaire)');
      return;
    }

    const newColumn = { ...currentColumn };
    
    // Ajouter la colonne à la table
    setTableData(prev => ({
      ...prev,
      columns: [...prev.columns, newColumn]
    }));

    // Réinitialiser le formulaire de colonne
    setCurrentColumn({
      name: '',
      type: 'String',
      nullable: false,
      unique: false,
      default: '',
      maxLength: '100',
      isForeignKey: false,
      foreignKeyTarget: '',
      foreignKeyColumn: 'id'
    });
  };

  const handleColumnNameChange = (name) => {
    setCurrentColumn(prev => ({ ...prev, name }));
    
    // Suggestion automatique
    const suggestion = suggestTypeForColumn(name);
    if (suggestion) {
      setCurrentColumn(prev => ({
        ...prev,
        type: suggestion.type,
        default: suggestion.default
      }));
    }
  };

  const handleCreateTable = () => {
    // Générer le code SQLAlchemy
    const code = generateSQLAlchemyCode(tableData);
    // Envoyer au backend pour création
    fetch('/api/create-table/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tableData, code })
    })
      .then(response => response.json())
      .then(result => {
        if (result.success) {
          // Appel API pour générer le modèle Python
          fetch('/api/create-table/generate-model', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              class_name: tableData.className,
              table_name: tableData.tableName,
              columns: tableData.columns,
              module_id: tableData.moduleId
            })
          })
            .then(res => res.json())
            .then(modelResult => {
              if (modelResult.success) {
                alert('Table et modèle Python créés avec succès !\n' + modelResult.reminder);
                onTableCreated(tableData);
              } else {
                alert('Table créée, mais erreur lors de la génération du modèle : ' + modelResult.message);
                onTableCreated(tableData);
              }
            })
            .catch(error => {
              alert('Table créée, mais erreur lors de la génération du modèle : ' + error.message);
              onTableCreated(tableData);
            });
        } else {
          alert('Erreur lors de la création : ' + result.message);
        }
      })
      .catch(error => {
        alert('Erreur de connexion : ' + error.message);
      });
  };

  const generateSQLAlchemyCode = (data) => {
    let code = `from .base import BaseModel\nfrom app import db\nimport datetime\n\n`;
    
    code += `class ${data.className}(BaseModel):\n`;
    code += `    __tablename__ = '${data.tableName}'\n\n`;
    
    // Colonne id automatique
    code += `    id = db.Column(db.Integer, primary_key=True, autoincrement=True)\n`;
    
    // Colonnes personnalisées
    data.columns.forEach(col => {
      let colDef = `    ${col.name} = db.Column(`;
      
      // Type de base
      const typeInfo = TYPES.find(t => t.id === col.type);
      if (col.isForeignKey) {
        colDef += `db.Integer, db.ForeignKey('${col.foreignKeyTarget}.${col.foreignKeyColumn}')`;
      } else if (col.type === 'String') {
        colDef += `db.String(${col.maxLength})`;
      } else {
        colDef += typeInfo.sql;
      }
      
      // Contraintes
      if (!col.nullable) colDef += `, nullable=False`;
      if (col.unique) colDef += `, unique=True`;
      if (col.default) {
        if (col.type === 'Boolean') {
          colDef += `, default=${col.default}`;
        } else if (col.type === 'String') {
          colDef += `, default="${col.default}"`;
        } else {
          colDef += `, default=${col.default}`;
        }
      }
      
      colDef += `)\n`;
      code += colDef;
    });
    
    code += `\n    def __repr__(self):\n`;
    code += `        return f'<${data.className} {{{{self.id}}}}>'\n`;
    
    return code;
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl p-6 max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-gray-900">
            🏗️ Créer une nouvelle table ATARYS
          </h2>
          <button
            onClick={onCancel}
            className="text-gray-400 hover:text-gray-600"
          >
            ✕
          </button>
        </div>

        {/* Étapes */}
        <div className="mb-6">
          <div className="flex space-x-4">
            <div className={`px-3 py-1 rounded ${step >= 1 ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}>
              1. Module
            </div>
            <div className={`px-3 py-1 rounded ${step >= 2 ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}>
              2. Classe
            </div>
            <div className={`px-3 py-1 rounded ${step >= 3 ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}>
              3. Colonnes
            </div>
          </div>
        </div>

        {/* Étape 1: Sélection du module */}
        {step === 1 && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Sélectionner le module ATARYS</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {Object.entries(MODULES_ATARYS).map(([id, name]) => (
                <button
                  key={id}
                  onClick={() => handleModuleChange(id)}
                  className={`p-3 border rounded-lg text-left ${
                    tableData.moduleId === parseInt(id)
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <div className="font-medium">{id}. {name}</div>
                </button>
              ))}
            </div>
            <div className="flex justify-end">
              <button
                onClick={() => setStep(2)}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Suivant
              </button>
            </div>
          </div>
        )}

        {/* Étape 2: Nom de la classe */}
        {step === 2 && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Définir la classe</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nom de la classe (PascalCase)
                </label>
                <input
                  type="text"
                  value={tableData.className}
                  onChange={(e) => handleClassNameChange(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="ex: ArticleClient"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nom de la table (généré automatiquement)
                </label>
                <input
                  type="text"
                  value={tableData.tableName}
                  onChange={(e) => setTableData(prev => ({ ...prev, tableName: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50"
                  placeholder="ex: article_client"
                />
              </div>
            </div>
            <div className="flex justify-between">
              <button
                onClick={() => setStep(1)}
                className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300"
              >
                Précédent
              </button>
              <button
                onClick={() => setStep(3)}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Suivant
              </button>
            </div>
          </div>
        )}

        {/* Étape 3: Colonnes */}
        {step === 3 && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold">Définir les colonnes</h3>
            
            {/* Colonnes existantes */}
            {tableData.columns.length > 0 && (
              <div>
                <h4 className="font-medium mb-2">Colonnes définies :</h4>
                <div className="space-y-2">
                  {tableData.columns.map((col, index) => (
                    <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                      <span className="font-medium">{col.name}</span>
                      <span className="text-sm text-gray-600">{col.type}</span>
                      <button
                        onClick={() => setTableData(prev => ({
                          ...prev,
                          columns: prev.columns.filter((_, i) => i !== index)
                        }))}
                        className="text-red-600 hover:text-red-800"
                      >
                        ✕
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Formulaire d'ajout de colonne */}
            <div className="border-t pt-4">
              <h4 className="font-medium mb-4">Ajouter une colonne :</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nom de la colonne
                  </label>
                  <input
                    type="text"
                    value={currentColumn.name}
                    onChange={(e) => handleColumnNameChange(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="ex: nom, prix, actif"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Type de données
                  </label>
                  <select
                    value={currentColumn.type}
                    onChange={(e) => setCurrentColumn(prev => ({ ...prev, type: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    {TYPES.map(type => (
                      <option key={type.id} value={type.id}>
                        {type.label}
                      </option>
                    ))}
                  </select>
                </div>

                {currentColumn.type === 'String' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Longueur maximale
                    </label>
                    <input
                      type="number"
                      value={currentColumn.maxLength}
                      onChange={(e) => setCurrentColumn(prev => ({ ...prev, maxLength: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                )}

                <div className="space-y-2">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={currentColumn.nullable}
                      onChange={(e) => setCurrentColumn(prev => ({ ...prev, nullable: e.target.checked }))}
                      className="mr-2"
                    />
                    <span className="text-sm">Nullable (optionnel)</span>
                  </label>
                  
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={currentColumn.unique}
                      onChange={(e) => setCurrentColumn(prev => ({ ...prev, unique: e.target.checked }))}
                      className="mr-2"
                    />
                    <span className="text-sm">Unique</span>
                  </label>
                  
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={currentColumn.isForeignKey}
                      onChange={(e) => setCurrentColumn(prev => ({ ...prev, isForeignKey: e.target.checked }))}
                      className="mr-2"
                    />
                    <span className="text-sm">Clé étrangère</span>
                  </label>
                </div>

                {currentColumn.isForeignKey && (
                  <div className="md:col-span-2 grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Table cible
                      </label>
                      <input
                        type="text"
                        value={currentColumn.foreignKeyTarget}
                        onChange={(e) => setCurrentColumn(prev => ({ ...prev, foreignKeyTarget: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="ex: users"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Colonne cible
                      </label>
                      <input
                        type="text"
                        value={currentColumn.foreignKeyColumn}
                        onChange={(e) => setCurrentColumn(prev => ({ ...prev, foreignKeyColumn: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="ex: id"
                      />
                    </div>
                  </div>
                )}

                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Valeur par défaut
                  </label>
                  <input
                    type="text"
                    value={currentColumn.default}
                    onChange={(e) => setCurrentColumn(prev => ({ ...prev, default: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="ex: 0, true, 'NC'"
                  />
                </div>
              </div>

              <div className="mt-4">
                <button
                  onClick={handleAddColumn}
                  className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
                >
                  ➕ Ajouter la colonne
                </button>
              </div>
            </div>

            <div className="flex justify-between pt-4 border-t">
              <button
                onClick={() => setStep(2)}
                className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300"
              >
                Précédent
              </button>
              <button
                onClick={handleCreateTable}
                disabled={!tableData.className || tableData.columns.length === 0}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                🏗️ Créer la table
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 