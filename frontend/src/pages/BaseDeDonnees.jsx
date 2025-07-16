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
  const [selectedOperation, setSelectedOperation] = useState(null);
  const [selectedTableForData, setSelectedTableForData] = useState('');
  const [pastedData, setPastedData] = useState('');
  const [parsedData, setParsedData] = useState([]);
  const [columnMapping, setColumnMapping] = useState({});
  const [showColumnMapping, setShowColumnMapping] = useState(false);
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

  // Nouveaux états pour les dropdowns de relations
  const [availableTables, setAvailableTables] = useState([]);
  const [targetTableColumns, setTargetTableColumns] = useState([]);
  const [selectedTargetTable, setSelectedTargetTable] = useState('');
  const [selectedTargetColumn, setSelectedTargetColumn] = useState('');

  // États pour la génération de code de relations
  const [relationData, setRelationData] = useState({
    sourceTable: '',
    targetTable: '',
    sourceClass: '',
    targetClass: '',
    relationName: '',
    backrefName: '',
    relationType: 'one-to-many',
    cascade: '',
    lazy: 'select',
    nullable: false
  });
  const [generatedRelationCode, setGeneratedRelationCode] = useState(null);

  // Charger la liste des tables existantes
  useEffect(() => {
    fetch('/api/table-generator/list-tables')
      .then(res => res.json())
      .then(data => {
        if (data.success && Array.isArray(data.data)) {
          setTables(data.data);
        } else {
          setTables([]);
        }
      })
      .catch(err => {
        console.error('Erreur chargement tables:', err);
        setTables([]);
      });
  }, []);

  // Charger l'état des migrations au montage
  useEffect(() => {
    checkMigrationStatus();
    getMigrationHelp();
    loadAvailableTables();
  }, []);

  // Charger les tables disponibles pour les clés étrangères
  const loadAvailableTables = async () => {
    try {
      const res = await fetch('/api/table-generator/list-tables-for-fk');
      const data = await res.json();
      if (data.success && Array.isArray(data.data)) {
        setAvailableTables(data.data);
      } else {
        setAvailableTables([]);
      }
    } catch (err) {
      console.error('Erreur chargement tables:', err);
      setAvailableTables([]);
    }
  };

  // Charger les colonnes d'une table cible
  const loadTargetTableColumns = async (tableName) => {
    if (!tableName) {
      setTargetTableColumns([]);
      return;
    }
    
    try {
      const res = await fetch(`/api/table-generator/get-table-columns?table=${tableName}`);
      const data = await res.json();
      if (data.success && Array.isArray(data.data)) {
        setTargetTableColumns(data.data);
        // Sélectionner automatiquement la colonne 'id' si elle existe
        const idColumn = data.data.find(col => col.name === 'id');
        if (idColumn) {
          setSelectedTargetColumn('id');
        }
      } else {
        setTargetTableColumns([]);
      }
    } catch (err) {
      console.error('Erreur chargement colonnes:', err);
      setTargetTableColumns([]);
    }
  };

  // Générer le code de relation
  const generateRelationCode = async () => {
    if (!relationData.sourceTable || !relationData.targetTable) {
      setMessage({ type: 'error', text: 'Tables source et cible requises' });
      return;
    }

    try {
      const res = await fetch('/api/table-generator/generate-relation-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(relationData)
      });
      const data = await res.json();
      
      if (data.success) {
        setGeneratedRelationCode(data.data);
        setMessage({ type: 'success', text: 'Code de relation généré avec succès' });
      } else {
        setMessage({ type: 'error', text: data.message });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Erreur lors de la génération du code' });
    }
  };

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
          .then(data => { if (data.success && Array.isArray(data.data)) setTables(data.data); });
      } else {
        setMessage({ type: 'error', text: data.message });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Erreur réseau ou serveur.' });
    } finally {
      setLoading(false);
    }
  };



  // Fonction de parsing des données Excel avec mapping contrôlé
  const parseExcelData = (pastedText, tableName) => {
    if (!pastedText.trim()) {
      setParsedData([]);
      return;
    }
    
    try {
      // Séparer les lignes
      const lines = pastedText.trim().split('\n');
      
      // Détecter les colonnes Excel
      const firstLine = lines[0];
      const excelColumns = firstLine.split('\t');
      
      // Créer le mapping par défaut
      const defaultMapping = {};
      excelColumns.forEach((col, idx) => {
        defaultMapping[`col_${idx}`] = col.trim();
      });
      
      setColumnMapping(defaultMapping);
      setShowColumnMapping(true);
      
      // Stocker les données brutes pour traitement ultérieur
      setParsedData(lines.slice(1).map(line => {
        const columns = line.split('\t');
        const row = {};
        columns.forEach((col, idx) => {
          row[`col_${idx}`] = col?.trim() || '';
        });
        return row;
      }).filter(row => {
        return Object.values(row).some(val => val !== '');
      }));
      
    } catch (error) {
      console.error('Erreur parsing Excel:', error);
      setParsedData([]);
    }
  };

  // Fonction de mapping des colonnes
  const handleColumnMapping = () => {
    if (!columnMapping || !selectedTableForData) return;
    
    // Colonnes auto-gérées à exclure
    const autoManagedColumns = ['id', 'created_at', 'updated_at'];
    
    // Mapping selon la table - exclure les colonnes auto-gérées
    let tableColumns = [];
    if (selectedTableForData === 'niveau_qualification') {
      tableColumns = ['niveau', 'categorie']; // Sans id, created_at, updated_at
    } else {
      // Pour les autres tables, récupérer les colonnes depuis l'API
      // et exclure les colonnes auto-gérées
      fetch(`/api/${selectedTableForData}/columns`)
        .then(response => response.json())
        .then(result => {
          if (result.success) {
            tableColumns = result.data.filter(col => !autoManagedColumns.includes(col));
          }
        })
        .catch(error => {
          console.error('Erreur récupération colonnes:', error);
        });
    }
    
    // Appliquer le mapping
    const mappedData = parsedData.map(row => {
      const mappedRow = {};
      tableColumns.forEach(tableCol => {
        const excelCol = columnMapping[tableCol];
        if (excelCol && row[excelCol]) {
          mappedRow[tableCol] = row[excelCol];
        } else {
          mappedRow[tableCol] = '';
        }
      });
      return mappedRow;
    });
    
    setParsedData(mappedData);
    setShowColumnMapping(false);
  };

  // Fonction d'insertion des données
  const handleInsertData = async () => {
    if (parsedData.length === 0 || !selectedTableForData) return;
    
    setLoading(true);
    
    try {
      // Insérer en lot via l'API
      const response = await fetch(`/api/${selectedTableForData}/bulk-insert`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          data: parsedData
        })
      });
      
      const result = await response.json();
      
      if (result.success) {
        setMessage({ 
          type: 'success', 
          text: `✅ ${result.inserted_count || parsedData.length} lignes insérées avec succès` 
        });
        setPastedData('');
        setParsedData([]);
      } else {
        setMessage({ 
          type: 'error', 
          text: `❌ Erreur : ${result.message}` 
        });
      }
      
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: 'Erreur réseau ou serveur' 
      });
    } finally {
      setLoading(false);
    }
  };

  // Composant OperationGuide pour l'onglet Guide Modifications
  const OperationGuide = ({ operation }) => {
    const guides = {
      remove_table: {
        title: "🗑️ Supprimer une table",
        warning: "⚠️ Cette opération est irréversible !",
        steps: [
          {
            title: "1. Identifier le module",
            description: "Trouver dans quel fichier module_X.py se trouve la table",
            code: `# Chercher dans backend/app/models/module_X.py
# Exemple : niveau_qualification → module_5.py`,
            copyText: "backend/app/models/module_X.py"
          },
          {
            title: "2. Supprimer le code Python",
            description: "Supprimer la classe du modèle, les routes et le schéma",
            code: `# Dans module_X.py, supprimer :
class MaTable(BaseModel):
    __tablename__ = 'ma_table'
    # ... tout le code de la classe

# Dans routes/module_X.py, supprimer :
# - Les routes CRUD pour cette table
# - Les imports du schéma

# Dans schemas/module_X.py, supprimer :
# - Le schéma MaTableSchema`,
            copyText: "class MaTable(BaseModel):"
          },
          {
            title: "3. Générer la migration",
            description: "Créer le script de migration Flask-Migrate",
            code: `flask db migrate -m "Remove table ma_table"`,
            copyText: "flask db migrate -m \"Remove table ma_table\""
          },
          {
            title: "4. Appliquer la migration",
            description: "Exécuter la migration pour supprimer la table",
            code: `flask db upgrade`,
            copyText: "flask db upgrade"
          }
        ]
      },
      
      add_columns: {
        title: "➕ Ajouter des colonnes",
        warning: "✅ Cette opération est sûre",
        steps: [
          {
            title: "1. Modifier le modèle",
            description: "Ajouter les nouvelles colonnes dans la classe",
            code: `# Dans module_X.py, ajouter :
class MaTable(BaseModel):
    __tablename__ = 'ma_table'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    # NOUVELLE COLONNE :
    description = db.Column(db.Text, nullable=True)
    prix_ht = db.Column(db.Numeric(10, 2), default=0.00)`,
            copyText: "description = db.Column(db.Text, nullable=True)"
          },
          {
            title: "2. Mettre à jour le schéma",
            description: "Ajouter les champs dans le schéma Marshmallow",
            code: `# Dans schemas/module_X.py :
class MaTableSchema(Schema):
    id = fields.Int(dump_only=True)
    nom = fields.Str(required=True)
    # NOUVEAUX CHAMPS :
    description = fields.Str(allow_none=True)
    prix_ht = fields.Decimal(places=2, default=0.00)`,
            copyText: "description = fields.Str(allow_none=True)"
          },
          {
            title: "3. Générer la migration",
            description: "Créer le script de migration",
            code: `flask db migrate -m "Add columns description and prix_ht to ma_table"`,
            copyText: "flask db migrate -m \"Add columns description and prix_ht to ma_table\""
          },
          {
            title: "4. Appliquer la migration",
            description: "Exécuter la migration",
            code: `flask db upgrade`,
            copyText: "flask db upgrade"
          }
        ]
      },
      
      foreign_keys: {
        title: "🔗 Ajouter une clé étrangère",
        warning: "⚠️ Attention aux contraintes de référentiel",
        steps: [
          {
            title: "1. Ajouter la clé étrangère",
            description: "Créer une relation entre deux tables",
            code: `# Dans le modèle, ajouter :
class Commande(BaseModel):
    __tablename__ = 'commandes'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', backref='commandes')
    
# Dans le schéma :
class CommandeSchema(Schema):
    id = fields.Int(dump_only=True)
    client_id = fields.Int(required=True)
    client = fields.Nested('ClientSchema', dump_only=True)`,
            copyText: "client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)"
          },
          {
            title: "2. Relation bidirectionnelle",
            description: "Configurer la relation dans les deux sens",
            code: `# Dans le modèle Client :
class Client(BaseModel):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    
    # Relation vers les commandes (automatique avec backref)
    # commandes = db.relationship('Commande', backref='client')
    
# Dans le schéma Client :
class ClientSchema(Schema):
    id = fields.Int(dump_only=True)
    nom = fields.Str(required=True)
    commandes = fields.Nested('CommandeSchema', many=True, dump_only=True)`,
            copyText: "commandes = fields.Nested('CommandeSchema', many=True, dump_only=True)"
          },
          {
            title: "3. Contraintes de suppression",
            description: "Gérer la suppression en cascade ou restriction",
            code: `# Cascade : supprimer les commandes si le client est supprimé
client_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)

# Restriction : empêcher la suppression si des commandes existent
client_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete='RESTRICT'), nullable=False)

# Set NULL : mettre NULL si le client est supprimé
client_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete='SET NULL'), nullable=True)`,
            copyText: "client_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)"
          },
          {
            title: "4. Générer la migration",
            description: "Créer la migration pour la clé étrangère",
            code: `flask db migrate -m "Add foreign key client_id to commandes table"`,
            copyText: "flask db migrate -m \"Add foreign key client_id to commandes table\""
          },
          {
            title: "5. Appliquer la migration",
            description: "Exécuter la migration",
            code: `flask db upgrade`,
            copyText: "flask db upgrade"
          }
        ]
      },
      
      foreign_key_best_practices: {
        title: "📚 Bonnes pratiques des clés étrangères",
        warning: "✅ Conseils pour des relations robustes",
        steps: [
          {
            title: "1. Nommage des clés étrangères",
            description: "Utiliser des noms explicites",
            code: `# ✅ BON : Nom explicite
client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

# ❌ MAUVAIS : Nom ambigu
id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)`,
            copyText: "client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)"
          },
          {
            title: "2. Contraintes de suppression",
            description: "Choisir la bonne stratégie selon le contexte",
            code: `# CASCADE : Supprimer les enfants avec le parent
# Utilisé pour : commandes → client (si client supprimé, commandes supprimées)

# RESTRICT : Empêcher la suppression du parent
# Utilisé pour : factures → client (empêcher suppression client avec factures)

# SET NULL : Mettre NULL dans l'enfant
# Utilisé pour : commentaires → utilisateur (garder commentaires, auteur anonyme)`,
            copyText: "client_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)"
          },
          {
            title: "3. Index sur les clés étrangères",
            description: "Créer des index pour les performances",
            code: `# Dans le modèle, ajouter un index :
class Commande(BaseModel):
    __tablename__ = 'commandes'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    
    # Index pour améliorer les performances
    __table_args__ = (
        db.Index('idx_commandes_client_id', 'client_id'),
    )`,
            copyText: "__table_args__ = (db.Index('idx_commandes_client_id', 'client_id'),)"
          },
          {
            title: "4. Validation des données",
            description: "Valider l'existence des références",
            code: `# Dans le schéma Marshmallow :
class CommandeSchema(Schema):
    client_id = fields.Int(required=True, validate=validate.Range(min=1))
    
    @validates('client_id')
    def validate_client_exists(self, value):
        client = Client.query.get(value)
        if not client:
            raise ValidationError('Client inexistant')`,
            copyText: "@validates('client_id')\ndef validate_client_exists(self, value):\n    client = Client.query.get(value)\n    if not client:\n        raise ValidationError('Client inexistant')"
          }
        ]
      },
      relation_python: {
        title: "👨‍💻 Ajouter une relation Python (db.relationship)",
        warning: "⚠️ Cette opération nécessite une modification manuelle du code Python pour garantir la cohérence ORM et la lisibilité du projet.",
        steps: [
          {
            title: "1. Identifier les tables à lier",
            description: "Déterminez la table source (celle qui contient la clé étrangère, ex : liste_salaries) et la table cible (ex : niveau_qualification).",
            code: `# Table source : liste_salaries\n# Table cible : niveau_qualification` ,
            copyText: "liste_salaries / niveau_qualification"
          },
          {
            title: "2. Ouvrir le fichier modèle concerné",
            description: "Ouvrez le fichier backend/app/models/module_X.py correspondant à la table source.",
            code: `# Exemple : backend/app/models/module_9.py` ,
            copyText: "backend/app/models/module_X.py"
          },
          {
            title: "3. Ajouter la relation Python dans la classe source",
            description: "Dans la classe de la table source, sous la clé étrangère, ajoutez :",
            code: `niveau_qualification = db.relationship('NiveauQualification')\n\n# Placez cette ligne sous :\nniveau_qualification_id = db.Column(db.Integer, db.ForeignKey('niveau_qualification.id'))` ,
            copyText: "niveau_qualification = db.relationship('NiveauQualification')"
          },
          {
            title: "4. (Optionnel) Ajouter la relation inverse dans la classe cible",
            description: "Dans la classe de la table cible, ajoutez si besoin :",
            code: `salaries = db.relationship('ListeSalaries', backref='niveau_qualification')\n\n# Cela permet d'accéder à tous les salariés d'un niveau via : niveau.salaries` ,
            copyText: "salaries = db.relationship('ListeSalaries', backref='niveau_qualification')"
          },
          {
            title: "5. Vérifier la syntaxe Python",
            description: "Enregistrez le fichier puis exécutez un linter pour vérifier la syntaxe :",
            code: `flake8 backend/app/models/module_X.py` ,
            copyText: "flake8 backend/app/models/module_X.py"
          },
          {
            title: "6. Vérifier la conformité ORM",
            description: "Redémarrez le serveur Flask et vérifiez que l'accès à la relation fonctionne dans l'API ou le shell Python :",
            code: `# Exemple dans le shell Flask :\ns = ListeSalaries.query.first()\nprint(s.niveau_qualification.niveau)\n# ou\nn = NiveauQualification.query.first()\nprint([sal.nom for sal in n.salaries])` ,
            copyText: "s.niveau_qualification.niveau"
          },
          {
            title: "FAQ et bonnes pratiques",
            description: "Pourquoi ajouter la relation à la main ?\n- Pour garantir la cohérence métier et la lisibilité du code.\n- Pour choisir le type de relation (unidirectionnelle, bidirectionnelle, backref, etc.).\n- Pour éviter les erreurs de génération automatique.\n\nAstuce :\n- Utilisez des noms explicites pour les relations.\n- Documentez chaque ajout dans le code.",
            code: `# Voir docs/03-regles-standards/WORKFLOWS.md pour les standards ATARYS` ,
            copyText: "docs/03-regles-standards/WORKFLOWS.md"
          }
        ]
      }
    };

    const guide = guides[operation];
    if (!guide) return null;

    const copyToClipboard = (text) => {
      navigator.clipboard.writeText(text);
    };

    if (operation === 'relation_python') {
      return (
        <div className="bg-blue-50 border border-blue-200 rounded p-4">
          <h3 className="font-semibold text-blue-900 mb-2">👨‍💻 Ajouter une relation Python (db.relationship)</h3>
          <div className="p-3 rounded mb-4 bg-yellow-50 border border-yellow-200 text-yellow-800">
            ⚠️ Cette opération nécessite une modification manuelle du code Python pour garantir la cohérence ORM et la lisibilité du projet.
          </div>
          
          <form className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block font-medium mb-1">Table source (contenant la clé étrangère)</label>
                <select 
                  className="border p-2 rounded w-full" 
                  value={relationData.sourceTable} 
                  onChange={e => {
                    const selectedTable = e.target.value;
                    setRelationData(prev => ({ 
                      ...prev, 
                      sourceTable: selectedTable,
                      sourceClass: selectedTable ? selectedTable.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join('') : ''
                    }));
                  }}
                >
                  <option value="">Choisir une table...</option>
                  {Array.isArray(availableTables) && availableTables.map(table => (
                    <option key={table.name} value={table.name}>
                      {table.name} ({table.module_name})
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block font-medium mb-1">Table cible (référencée)</label>
                <select 
                  className="border p-2 rounded w-full" 
                  value={relationData.targetTable} 
                  onChange={e => {
                    const selectedTable = e.target.value;
                    setRelationData(prev => ({ 
                      ...prev, 
                      targetTable: selectedTable,
                      targetClass: selectedTable ? selectedTable.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join('') : '',
                      relationName: selectedTable || ''
                    }));
                  }}
                >
                  <option value="">Choisir une table...</option>
                  {availableTables.map(table => (
                    <option key={table.name} value={table.name}>
                      {table.name} ({table.module_name})
                    </option>
                  ))}
                </select>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block font-medium mb-1">Nom de la relation (attribut Python)</label>
                <input 
                  type="text" 
                  className="border p-2 rounded w-full" 
                  value={relationData.relationName} 
                  onChange={e => setRelationData(prev => ({ ...prev, relationName: e.target.value }))} 
                  placeholder={relationData.targetTable || 'ex: niveau_qualification'} 
                />
              </div>
              <div>
                <label className="block font-medium mb-1">Nom du backref (optionnel)</label>
                <input 
                  type="text" 
                  className="border p-2 rounded w-full" 
                  value={relationData.backrefName} 
                  onChange={e => setRelationData(prev => ({ ...prev, backrefName: e.target.value }))} 
                  placeholder={relationData.sourceTable ? `${relationData.sourceTable}s` : 'ex: salaries'} 
                />
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block font-medium mb-1">Type de relation</label>
                <select 
                  className="border p-2 rounded w-full" 
                  value={relationData.relationType} 
                  onChange={e => setRelationData(prev => ({ ...prev, relationType: e.target.value }))}
                >
                  <option value="one-to-many">One-to-Many (par défaut)</option>
                  <option value="many-to-one">Many-to-One</option>
                  <option value="bidirectional">Bidirectionnelle</option>
                </select>
              </div>
              <div>
                <label className="block font-medium mb-1">Cascade (optionnel)</label>
                <select 
                  className="border p-2 rounded w-full" 
                  value={relationData.cascade} 
                  onChange={e => setRelationData(prev => ({ ...prev, cascade: e.target.value }))}
                >
                  <option value="">Aucun</option>
                  <option value="all">all</option>
                  <option value="delete-orphan">delete-orphan</option>
                  <option value="save-update">save-update</option>
                </select>
              </div>
              <div>
                <label className="block font-medium mb-1">Lazy loading</label>
                <select 
                  className="border p-2 rounded w-full" 
                  value={relationData.lazy} 
                  onChange={e => setRelationData(prev => ({ ...prev, lazy: e.target.value }))}
                >
                  <option value="select">select (par défaut)</option>
                  <option value="joined">joined</option>
                  <option value="subquery">subquery</option>
                  <option value="dynamic">dynamic</option>
                </select>
              </div>
            </div>
            
            <div className="flex gap-4">
              <label className="flex items-center gap-2">
                <input 
                  type="checkbox" 
                  checked={relationData.nullable} 
                  onChange={e => setRelationData(prev => ({ ...prev, nullable: e.target.checked }))} 
                />
                Nullable
              </label>
            </div>
            
            <div className="flex gap-2">
              <button 
                type="button"
                onClick={generateRelationCode}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                disabled={!relationData.sourceTable || !relationData.targetTable}
              >
                🔧 Générer le code
              </button>
            </div>
          </form>
          
          {/* Affichage du code généré */}
          {generatedRelationCode && (
            <div className="mt-6">
              <h4 className="font-semibold text-blue-900 mb-2">Code à copier dans le backend</h4>
              
              {/* Code pour la table source */}
              <div className="mb-4">
                <div className="mb-2 text-blue-800 text-sm">
                  Dans <b>backend/app/models/module_X.py</b>, dans la classe <b>{relationData.sourceClass}</b> (table source), sous la clé étrangère :
                </div>
                <div className="flex items-center gap-2 mb-2">
                  <code className="bg-blue-100 px-3 py-2 rounded font-mono text-blue-900 flex-1 text-sm">
                    {generatedRelationCode.source_code.foreign_key}
                  </code>
                  <button 
                    onClick={() => navigator.clipboard.writeText(generatedRelationCode.source_code.foreign_key)} 
                    className="px-3 py-2 bg-blue-200 rounded text-blue-800 hover:bg-blue-300 text-sm"
                  >
                    Copier
                  </button>
                </div>
                <div className="flex items-center gap-2 mb-4">
                  <code className="bg-blue-100 px-3 py-2 rounded font-mono text-blue-900 flex-1 text-sm">
                    {generatedRelationCode.source_code.relationship}
                  </code>
                  <button 
                    onClick={() => navigator.clipboard.writeText(generatedRelationCode.source_code.relationship)} 
                    className="px-3 py-2 bg-blue-200 rounded text-blue-800 hover:bg-blue-300 text-sm"
                  >
                    Copier
                  </button>
                </div>
              </div>
              
              {/* Code pour la table cible (si bidirectionnelle) */}
              {generatedRelationCode.target_code && (
                <div className="mb-4">
                  <div className="mb-2 text-blue-800 text-sm">
                    Dans <b>backend/app/models/module_Y.py</b>, dans la classe <b>{relationData.targetClass}</b> (table cible), à la fin de la classe :
                  </div>
                  <div className="flex items-center gap-2 mb-4">
                    <code className="bg-blue-100 px-3 py-2 rounded font-mono text-blue-900 flex-1 text-sm">
                      {generatedRelationCode.target_code.relationship}
                    </code>
                    <button 
                      onClick={() => navigator.clipboard.writeText(generatedRelationCode.target_code.relationship)} 
                      className="px-3 py-2 bg-blue-200 rounded text-blue-800 hover:bg-blue-300 text-sm"
                    >
                      Copier
                    </button>
                  </div>
                </div>
              )}
              
              {/* Code pour les schémas Marshmallow */}
              <div className="mb-4">
                <h5 className="font-semibold text-blue-900 mb-2">Schémas Marshmallow</h5>
                
                {/* Schéma source */}
                <div className="mb-3">
                  <div className="mb-1 text-blue-800 text-sm">
                    Dans <b>backend/app/schemas/module_X.py</b>, schéma <b>{relationData.sourceClass}Schema</b> :
                  </div>
                  <div className="flex items-center gap-2 mb-2">
                    <code className="bg-green-100 px-3 py-2 rounded font-mono text-green-900 flex-1 text-sm">
                      {generatedRelationCode.schema_code.source.foreign_key}
                    </code>
                    <button 
                      onClick={() => navigator.clipboard.writeText(generatedRelationCode.schema_code.source.foreign_key)} 
                      className="px-3 py-2 bg-green-200 rounded text-green-800 hover:bg-green-300 text-sm"
                    >
                      Copier
                    </button>
                  </div>
                  <div className="flex items-center gap-2 mb-3">
                    <code className="bg-green-100 px-3 py-2 rounded font-mono text-green-900 flex-1 text-sm">
                      {generatedRelationCode.schema_code.source.relation}
                    </code>
                    <button 
                      onClick={() => navigator.clipboard.writeText(generatedRelationCode.schema_code.source.relation)} 
                      className="px-3 py-2 bg-green-200 rounded text-green-800 hover:bg-green-300 text-sm"
                    >
                      Copier
                    </button>
                  </div>
                </div>
                
                {/* Schéma cible (si bidirectionnelle) */}
                {generatedRelationCode.schema_code.target && (
                  <div className="mb-3">
                    <div className="mb-1 text-blue-800 text-sm">
                      Dans <b>backend/app/schemas/module_Y.py</b>, schéma <b>{relationData.targetClass}Schema</b> :
                    </div>
                    <div className="flex items-center gap-2 mb-3">
                      <code className="bg-green-100 px-3 py-2 rounded font-mono text-green-900 flex-1 text-sm">
                        {generatedRelationCode.schema_code.target.relation}
                      </code>
                      <button 
                        onClick={() => navigator.clipboard.writeText(generatedRelationCode.schema_code.target.relation)} 
                        className="px-3 py-2 bg-green-200 rounded text-green-800 hover:bg-green-300 text-sm"
                      >
                        Copier
                      </button>
                    </div>
                  </div>
                )}
              </div>
              
              {/* Instructions */}
              <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded text-yellow-800 text-sm">
                <h5 className="font-semibold mb-2">Instructions d'implémentation :</h5>
                <ol className="list-decimal list-inside space-y-1">
                  {generatedRelationCode.instructions.steps.map((step, idx) => (
                    <li key={idx}>{step}</li>
                  ))}
                </ol>
                
                <h5 className="font-semibold mb-2 mt-4">Validation :</h5>
                <ul className="list-disc list-inside space-y-1">
                  {generatedRelationCode.instructions.validation.map((validation, idx) => (
                    <li key={idx}>{validation}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      );
    }

    return (
      <div className="bg-blue-50 border border-blue-200 rounded p-4">
        <h3 className="font-semibold text-blue-900 mb-2">{guide.title}</h3>
        
        {guide.warning && (
          <div className={`p-3 rounded mb-4 ${
            guide.warning.includes('⚠️') 
              ? 'bg-yellow-50 border border-yellow-200 text-yellow-800'
              : 'bg-green-50 border border-green-200 text-green-800'
          }`}>
            {guide.warning}
          </div>
        )}
        
        <div className="space-y-4">
          {guide.steps.map((step, idx) => (
            <div key={idx} className="border border-blue-200 rounded p-3 bg-white">
              <h4 className="font-medium text-blue-900 mb-2">{step.title}</h4>
              <p className="text-blue-800 text-sm mb-3">{step.description}</p>
              <div className="flex items-center gap-2">
                <code className="bg-blue-100 px-3 py-2 rounded font-mono text-blue-900 flex-1 text-sm">
                  {step.code}
                </code>
                <button 
                  onClick={() => copyToClipboard(step.copyText)}
                  className="px-3 py-2 bg-blue-200 rounded text-blue-800 hover:bg-blue-300 text-sm"
                >
                  Copier
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
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
              onClick={() => setActiveTab('migrations')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'migrations'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Migrations
            </button>
            <button
              onClick={() => setActiveTab('guide')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'guide'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Guide Modifications
            </button>
            <button
              onClick={() => setActiveTab('data')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'data'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              📊 Données
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
              {migrationInstructions.next_steps?.map((step, idx) => {
                // Corriger les guillemets pour Windows PowerShell
                const correctedStep = step.replace(/'/g, '"');
                return (
                  <li key={idx} className="flex items-center justify-between bg-blue-100 px-2 py-1 rounded">
                    <code className="font-mono">{correctedStep}</code>
                    <button 
                      type="button" 
                      className="px-2 py-1 bg-blue-200 rounded text-xs hover:bg-blue-300 ml-2" 
                      onClick={() => navigator.clipboard.writeText(correctedStep)}
                      title="Copier la commande"
                    >
                      📋 Copier
                    </button>
                  </li>
                );
              })}
            </ul>
            {migrationInstructions.warning && (
              <p className="mt-2 text-orange-700 font-medium">⚠️ {migrationInstructions.warning}</p>
            )}
            <div className="mt-3 p-2 bg-yellow-50 border border-yellow-200 rounded">
              <p className="text-yellow-800 text-xs">
                <strong>💡 Conseil :</strong> Utilisez les guillemets doubles <code>"</code> dans PowerShell Windows au lieu des guillemets simples <code>'</code>
              </p>
            </div>
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
                  <div className="flex flex-col gap-2 ml-4 p-3 bg-blue-50 border border-blue-200 rounded">
                    <div>
                      <label className="text-xs font-medium text-blue-900">Table cible</label>
                      <select
                        className="border p-1 rounded w-full text-sm"
                        value={foreignKey.table}
                        onChange={e => {
                          const selectedTable = e.target.value;
                          setForeignKey(fk => ({ ...fk, table: selectedTable, column: '' }));
                          if (selectedTable) {
                            loadTargetTableColumns(selectedTable);
                          }
                        }}
                      >
                        <option value="">Choisir une table...</option>
                        {Array.isArray(availableTables) && availableTables.map(table => (
                          <option key={table.name} value={table.name}>
                            {table.name} ({table.module_name})
                          </option>
                        ))}
                      </select>
                    </div>
                    {foreignKey.table && (
                      <div>
                        <label className="text-xs font-medium text-blue-900">Colonne cible</label>
                        <select
                          className="border p-1 rounded w-full text-sm"
                          value={foreignKey.column}
                          onChange={e => setForeignKey(fk => ({ ...fk, column: e.target.value }))}
                        >
                          <option value="">Choisir une colonne...</option>
                          {Array.isArray(targetTableColumns) && targetTableColumns.map(col => (
                            <option key={col.name} value={col.name}>
                              {col.name} ({col.type}) {col.primary_key ? '(PK)' : ''}
                            </option>
                          ))}
                        </select>
                      </div>
                    )}
                    <div className="flex gap-2">
                      <label className="flex items-center gap-1 text-xs">
                        <input 
                          type="checkbox" 
                          checked={col.nullable !== false} 
                          onChange={e => handleColumnChange(idx, 'nullable', e.target.checked)} 
                        />
                        Nullable
                      </label>
                      <label className="flex items-center gap-1 text-xs">
                        <select 
                          className="border p-1 rounded text-xs"
                          value={col.onDelete || 'RESTRICT'}
                          onChange={e => handleColumnChange(idx, 'onDelete', e.target.value)}
                        >
                          <option value="RESTRICT">RESTRICT</option>
                          <option value="CASCADE">CASCADE</option>
                          <option value="SET NULL">SET NULL</option>
                        </select>
                        onDelete
                      </label>
                    </div>
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

          {/* Guide des migrations */}
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
                    <div key={key} className="bg-blue-100 p-2 rounded flex items-center justify-between">
                      <code className="font-mono text-blue-900">{cmd}</code>
                      <button 
                        type="button" 
                        className="px-2 py-1 bg-blue-200 rounded text-xs hover:bg-blue-300 ml-2" 
                        onClick={() => navigator.clipboard.writeText(cmd)}
                      >
                        Copier
                      </button>
                    </div>
                  ))}
                </div>
                
                <h4 className="font-semibold text-blue-900 mb-2 mt-4">Activation de l'environnement :</h4>
                <div className="mb-2">
                  <span className="font-medium text-blue-800">Windows cmd.exe :</span>
                  <div className="flex items-center gap-2 mt-1">
                    <code className="bg-blue-100 px-2 py-1 rounded font-mono">venv\Scripts\activate.bat</code>
                    <button 
                      type="button" 
                      className="px-2 py-1 bg-blue-200 rounded text-xs hover:bg-blue-300" 
                      onClick={() => navigator.clipboard.writeText('venv\\Scripts\\activate.bat')}
                    >
                      Copier
                    </button>
                  </div>
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
              �� Actualiser l'état
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

      {/* Nouvel onglet Guide Modifications */}
      {activeTab === 'guide' && (
        <div className="bg-white shadow p-4 rounded mb-8">
          <h2 className="text-lg font-semibold mb-4">🗑️ Guide des Modifications et Suppressions</h2>
          
          {/* Sélection du type d'opération */}
          <div className="mb-6">
            <h3 className="font-medium mb-3">Choisir une opération :</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button 
                onClick={() => setSelectedOperation('remove_table')}
                className={`p-4 border rounded text-left ${
                  selectedOperation === 'remove_table' 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="font-medium">🗑️ Supprimer une table</div>
                <div className="text-sm text-gray-600">Supprimer complètement une table et son code</div>
              </button>
              
              <button 
                onClick={() => setSelectedOperation('add_columns')}
                className={`p-4 border rounded text-left ${
                  selectedOperation === 'add_columns' 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="font-medium">➕ Ajouter des colonnes</div>
                <div className="text-sm text-gray-600">Ajouter de nouvelles colonnes à une table</div>
              </button>
              
              <button 
                onClick={() => setSelectedOperation('foreign_keys')}
                className={`p-4 border rounded text-left ${
                  selectedOperation === 'foreign_keys' 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="font-medium">🔗 Ajouter une clé étrangère</div>
                <div className="text-sm text-gray-600">Créer une relation entre deux tables</div>
              </button>
              
              <button 
                onClick={() => setSelectedOperation('foreign_key_best_practices')}
                className={`p-4 border rounded text-left ${
                  selectedOperation === 'foreign_key_best_practices' 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="font-medium">📚 Bonnes pratiques</div>
                <div className="text-sm text-gray-600">Conseils pour des relations robustes</div>
              </button>
              <button 
                onClick={() => setSelectedOperation('relation_python')}
                className={`p-4 border rounded text-left ${
                  selectedOperation === 'relation_python' 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="font-medium">👨‍💻 Ajouter une relation Python</div>
                <div className="text-sm text-gray-600">db.relationship, accès ORM, guide pas à pas</div>
              </button>
            </div>
          </div>
          
          {/* Guide spécifique selon l'opération */}
          {selectedOperation && (
            <OperationGuide operation={selectedOperation} />
          )}
          
          {/* Message d'aide si aucune opération sélectionnée */}
          {!selectedOperation && (
            <div className="bg-gray-50 border border-gray-200 rounded p-4">
              <h3 className="font-medium text-gray-900 mb-2">ℹ️ Comment utiliser ce guide</h3>
              <p className="text-gray-700 text-sm">
                Sélectionnez une opération ci-dessus pour voir le guide détaillé avec les étapes à suivre, 
                les exemples de code et les commandes à exécuter. Toutes les opérations respectent 
                les standards professionnels Flask-Migrate.
              </p>
            </div>
          )}
        </div>
      )}

      {/* Nouvel onglet Données */}
      {activeTab === 'data' && (
        <div className="bg-white shadow p-4 rounded mb-8">
          <h2 className="text-lg font-semibold mb-4">📊 Gestion des Données - Copier-Coller Excel</h2>
          
          {/* Sélection de la table */}
          <div className="mb-6">
            <label className="block font-medium mb-2">Sélectionner une table :</label>
            <select 
              value={selectedTableForData} 
              onChange={e => {
                setSelectedTableForData(e.target.value);
                setPastedData('');
                setParsedData([]);
              }}
              className="border p-2 rounded w-full"
            >
              <option value="">Choisir une table...</option>
              {tables.map(table => (
                <option key={table.name} value={table.name}>
                  {table.name} ({table.module})
                </option>
              ))}
            </select>
          </div>
          
          {/* Interface d'insertion si table sélectionnée */}
          {selectedTableForData && (
            <div>
              {/* Instructions */}
              <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded">
                <h3 className="font-medium text-blue-900 mb-2">📋 Instructions :</h3>
                <ol className="text-blue-800 text-sm space-y-1">
                  <li>1. Préparez vos données dans Excel (avec en-têtes)</li>
                  <li>2. Sélectionnez et copiez les données (Ctrl+C)</li>
                  <li>3. Collez dans la zone ci-dessous (Ctrl+V)</li>
                  <li>4. Mappez les colonnes Excel vers les champs de la table</li>
                  <li>5. Cliquez sur "Insérer les données"</li>
                </ol>
                
                <div className="mt-3 p-3 bg-yellow-50 border border-yellow-200 rounded">
                  <h4 className="font-medium text-yellow-900 mb-2">⚠️ IMPORTANT - Champs auto-gérés :</h4>
                  <ul className="text-yellow-800 text-sm space-y-1">
                    <li>• <strong>id</strong> : Généré automatiquement (ne pas copier)</li>
                    <li>• <strong>created_at</strong> : Horodatage automatique (ne pas copier)</li>
                    <li>• <strong>updated_at</strong> : Horodatage automatique (ne pas copier)</li>
                  </ul>
                  <p className="text-yellow-800 text-xs mt-2">
                    <strong>Conseil :</strong> Excluez ces colonnes de vos données Excel ou elles seront ignorées automatiquement.
                  </p>
                  <p className="text-yellow-800 text-xs mt-2">
                    <strong>Performance :</strong> L'insertion en lot supporte jusqu'à 500 lignes pour des performances optimales.
                  </p>
                </div>
                
                {selectedTableForData === 'niveau_qualification' && (
                  <div className="mt-2 p-2 bg-blue-100 rounded">
                    <p className="text-blue-800 text-xs">
                      <strong>Exemple pour cette table :</strong> Collez vos données avec en-têtes, puis mappez uniquement "Niveau" et "Catégorie"
                    </p>
                  </div>
                )}
              </div>
              
              {/* Zone de collage */}
              <div className="mb-4">
                <label className="block font-medium mb-2">Collez vos données Excel ici :</label>
                <textarea
                  className="w-full h-32 border p-3 rounded font-mono text-sm"
                  placeholder={`Collez vos données Excel ici (avec en-têtes)...
Exemple pour ${selectedTableForData} :
Niveau	Catégorie
N1P1	Ouvrier d'exécution
N1P2	Ouvrier d'exécution
N2P1	Ouvrier Professionnel

Note : Les colonnes id, created_at, updated_at sont ignorées automatiquement`}
                  value={pastedData}
                  onChange={e => {
                    setPastedData(e.target.value);
                    parseExcelData(e.target.value, selectedTableForData);
                  }}
                />
              </div>
              
              {/* Mapping des colonnes */}
              {showColumnMapping && parsedData.length > 0 && (
                <div className="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded">
                  <h3 className="font-medium text-yellow-900 mb-3">🔧 Mapping des colonnes</h3>
                  <p className="text-yellow-800 text-sm mb-3">
                    Associez les colonnes Excel aux champs de la table {selectedTableForData} :
                  </p>
                  
                  <div className="space-y-2">
                    {selectedTableForData === 'niveau_qualification' && (
                      <>
                        <div className="flex items-center gap-3">
                          <label className="font-medium text-yellow-900 w-24">Niveau :</label>
                          <select 
                            value={columnMapping.niveau || ''}
                            onChange={e => setColumnMapping({...columnMapping, niveau: e.target.value})}
                            className="border p-2 rounded flex-1"
                          >
                            <option value="">Choisir une colonne...</option>
                            {Object.entries(columnMapping).map(([key, value]) => (
                              <option key={key} value={key}>{value}</option>
                            ))}
                          </select>
                        </div>
                        
                        <div className="flex items-center gap-3">
                          <label className="font-medium text-yellow-900 w-24">Catégorie :</label>
                          <select 
                            value={columnMapping.categorie || ''}
                            onChange={e => setColumnMapping({...columnMapping, categorie: e.target.value})}
                            className="border p-2 rounded flex-1"
                          >
                            <option value="">Choisir une colonne...</option>
                            {Object.entries(columnMapping).map(([key, value]) => (
                              <option key={key} value={key}>{value}</option>
                            ))}
                          </select>
                        </div>
                      </>
                    )}
                  </div>
                  
                  <div className="mt-4 flex gap-2">
                    <button 
                      onClick={handleColumnMapping}
                      className="px-4 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700"
                    >
                      ✅ Appliquer le mapping
                    </button>
                    <button 
                      onClick={() => setShowColumnMapping(false)}
                      className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
                    >
                      ❌ Annuler
                    </button>
                  </div>
                </div>
              )}
              
              {/* Prévisualisation finale */}
              {parsedData.length > 0 && !showColumnMapping && (
                <div className="mb-4">
                  <h3 className="font-medium mb-2">📋 Prévisualisation finale ({parsedData.length} lignes) :</h3>
                  <div className="max-h-60 overflow-y-auto border rounded">
                    <table className="w-full text-sm">
                      <thead className="bg-gray-100 sticky top-0">
                        <tr>
                          {Object.keys(parsedData[0] || {}).map(key => (
                            <th key={key} className="p-2 border">{key}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {parsedData.map((row, idx) => (
                          <tr key={idx} className={idx % 2 === 0 ? 'bg-gray-50' : ''}>
                            {Object.values(row).map((value, colIdx) => (
                              <td key={colIdx} className="p-2 border">{value}</td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
              
              {/* Boutons d'action */}
              <div className="flex gap-2">
                <button 
                  onClick={handleInsertData}
                  disabled={parsedData.length === 0 || loading || showColumnMapping}
                  className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:bg-gray-400"
                >
                  {loading ? '⏳ Insertion...' : `➕ Insérer ${parsedData.length} lignes`}
                </button>
                <button 
                  onClick={() => {
                    setPastedData('');
                    setParsedData([]);
                    setShowColumnMapping(false);
                    setColumnMapping({});
                  }}
                  className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
                >
                  🗑️ Effacer
                </button>
              </div>
            </div>
          )}
          
          {/* Message d'aide si aucune table sélectionnée */}
          {!selectedTableForData && (
            <div className="bg-gray-50 border border-gray-200 rounded p-4">
              <h3 className="font-medium text-gray-900 mb-2">ℹ️ Comment insérer des données</h3>
              <p className="text-gray-700 text-sm">
                Sélectionnez une table ci-dessus pour commencer l'insertion de données via copier-coller Excel. 
                Cette méthode permet d'insérer rapidement de grandes quantités de données.
              </p>
            </div>
          )}
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
            {Array.isArray(tables) && tables.map((t, idx) => (
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
                  {/* Bouton supprimé pour 12.1 : pas de suppression */}
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