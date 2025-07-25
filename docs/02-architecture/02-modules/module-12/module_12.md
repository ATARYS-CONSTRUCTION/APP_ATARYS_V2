# ⚙️ Module 12 - PARAMÈTRES

> **Configuration système et gestion de la base de données**  
> **État : OPÉRATIONNEL** ✅ - Interface complète avec gestion des ENUM  
> Dernière mise à jour : 22/07/2025

---

## 🎯 Vue d'ensemble

Le module **12 - PARAMÈTRES** fournit l'interface d'administration et de configuration du système ATARYS. Il comprend principalement la gestion dynamique de la base de données, la configuration système et la personnalisation.

### **Objectifs Principaux**
- ✅ **Gestion dynamique des tables SQLite** (BASE DE DONNÉES)
- ✅ **Configuration des paramètres système**
- ✅ **Interface d'administration complète**
- ✅ **Outils de maintenance et audit**
- ✅ **Personnalisation de l'interface**

---

## 📋 État d'Implémentation

### **✅ OPÉRATIONNEL**
- **Interface de gestion** : Création dynamique de tables avec validation
- **Service générateur** : `TableGeneratorService` complet
- **API REST complète** : Endpoints de gestion des tables
- **Gestion des ENUM** : Interface pour définir les valeurs d'énumération
- **Relations BDD** : Clés étrangères avec validation
- **Génération de code** : Modèles, routes, schémas automatiques

### **🔄 En Cours**
- **Paramètres système** : Configuration globale
- **Audit complet** : Logs et traçabilité
- **Sauvegarde/Restauration** : Outils de maintenance

### **📋 Planifié**
- **Agent IA** : Interface tchat et workflows n8n (après consolidation BDD)

### **❌ À Implémenter**
- **Interface de configuration** : Paramètres utilisateur
- **Gestion des préférences** : Personnalisation avancée

---

## 🏗️ Architecture Technique

### **Fichiers Opérationnels**
```
backend/app/models/module_12.py      # Modèles SQLAlchemy ✅
backend/app/routes/table_generator.py # API création tables ✅
backend/app/services/table_generator.py # Service génération ✅
frontend/src/pages/BaseDeDonnees.jsx # Interface React ✅
```

### **Fonctionnalités Clés**
1. **✅ Création dynamique de tables** avec validation complète
2. **✅ Modification de structure** (ajout/suppression de colonnes)
3. **✅ Suppression sécurisée** avec confirmation
4. **✅ Génération de code automatique** (modèles, routes, schémas)
5. **✅ Gestion des ENUM** avec interface utilisateur
6. **✅ Relations ForeignKey** avec validation

---

## 📊 Sous-modules

Selon `ATARYS_MODULES.md`, le module 12 comprend :

### **12.1 - BASE DE DONNÉES** ✅ **OPÉRATIONNEL**
- ✅ Interface de gestion des tables SQLite
- ✅ Création dynamique de tables SQLite
- ✅ Modification de structure de tables existantes
- ✅ Gestion des colonnes et contraintes
- ✅ Interface d'administration des bases de données
- ✅ Gestion des types ENUM avec valeurs personnalisées
- ✅ Relations ForeignKey avec validation

### **12.2 - AGENT IA** 📋 **PLANIFIÉ**
- 📋 Agent IA intégré à l'application ATARYS V2
- 📋 Interface tchat accessible en un clic depuis toute page
- 📋 Automatisations n8n avec workflows intelligents
- 📋 Extraction automatique des devis Excel/CSV
- 📋 APIs dédiées pour communication avec n8n
- 📋 Monitoring et gestion des workflows IA

#### **Fonctionnalités Agent IA**
- **Interface Tchat Intégrée** : Accessible sans quitter la page courante
- **Workflows n8n** : Automatisations métier via n8n + OpenAI
- **Extraction de Devis** : Premier workflow opérationnel
- **APIs de Communication** : Endpoints pour n8n webhooks
- **Monitoring Intelligent** : Suivi des traitements automatisés

#### **Workflows Prévus**
1. **Extraction Devis Excel** : Analyse automatique des devis vers `devis_chantiers`
2. **Génération Rapports** : Création automatique de documents
3. **Analyse Rentabilité** : Calculs prévisionnels automatisés
4. **Notifications Intelligentes** : Alertes contextuelles

### **Fonctionnalités Supplémentaires** 🔄 **EN COURS**
- Configuration système
- Personnalisation de l'interface
- Paramètres utilisateur
- Gestion des préférences

---

## 🔧 **PROBLÈME ENUM RÉSOLU**

### **Problème Identifié**
L'interface ENUM perdait les valeurs saisies lors de l'ajout d'une nouvelle colonne car :
- `enumValues` était un état global réinitialisé à chaque ajout
- Les valeurs n'étaient pas sauvegardées par colonne

### **Solution Implémentée**
```javascript
// AVANT (problématique)
const [enumValues, setEnumValues] = useState([]); // État global

// APRÈS (solution)
// Chaque colonne stocke ses propres valeurs ENUM
const handleColumnChange = (idx, field, value) => {
  if (field === 'type' && value === 'Enum') {
    // Initialiser les valeurs ENUM pour cette colonne
    handleColumnChange(idx, 'enumValues', []);
  }
  // ... reste de la logique
};
```

### **Interface ENUM Améliorée**
```jsx
{col.type === 'Enum' && (
  <div className="flex flex-col gap-1 ml-4">
    <label className="text-xs">Valeurs Enum (une par ligne)</label>
    <textarea
      className="border p-1 rounded"
      rows={3}
      value={col.enumValues ? col.enumValues.join('\n') : ''}
      onChange={e => handleColumnChange(idx, 'enumValues', e.target.value.split('\n'))}
      placeholder="ex: Brouillon\nValidé\nArchivé"
    />
  </div>
)}
```

---

## 🛠️ Interface de Gestion

### **Fonctionnalités Disponibles**
1. **✅ Créer une table** : Formulaire avec sélection module ATARYS
2. **✅ Modifier une table** : Ajout/suppression de colonnes
3. **✅ Supprimer une table** : Avec confirmation et nettoyage
4. **✅ Générer le code** : Modèles, routes, schémas automatiques
5. **✅ Gestion ENUM** : Interface pour définir les valeurs
6. **✅ Relations ForeignKey** : Sélection table/colonne cible

### **Types de Colonnes Supportés**
```javascript
const columnTypes = [
  { value: 'String', label: 'String (texte court)' },
  { value: 'Text', label: 'Text (texte long)' },
  { value: 'Integer', label: 'Integer (nombre entier)' },
  { value: 'Numeric', label: 'Numeric (nombre décimal)' },
  { value: 'Boolean', label: 'Boolean (vrai/faux)' },
  { value: 'Date', label: 'Date' },
  { value: 'DateTime', label: 'DateTime (date + heure)' },
  { value: 'Enum', label: 'Enum (liste de valeurs)' },
  { value: 'ForeignKey', label: 'ForeignKey (clé étrangère)' }
];
```

### **Workflow Professionnel**
1. **Définition de la structure** : Interface intuitive
2. **Validation en temps réel** : Vérification des contraintes
3. **Génération du code backend** : Modèles, routes, schémas
4. **Exécution des migrations** : Instructions automatiques
5. **Validation et tests** : Vérification du bon fonctionnement

---

## 🔗 Relations avec Autres Modules

### **Module 9 - LISTE_SALARIÉS**
```python
# Relation existante dans TestCle2
niveau_qualification_id → niveau_qualification.id
```

### **Tous les Modules**
- ✅ Génération automatique de modèles
- ✅ Création d'APIs REST standardisées
- ✅ Service de développement transversal

---

## 📊 **Métriques et Performance**

### **Tables Créées**
- **TestAuditTable** : Table de test avec audit
- **TestCle2** : Table avec relations ForeignKey
- **Tables dynamiques** : Générées via l'interface

### **Performance**
- **Génération de code** : < 2 secondes
- **Validation** : Temps réel
- **Interface** : Réactive et intuitive

---

## 🤖 **Agent IA - Documentation Technique**

### **Architecture Agent IA**
```
ATARYS V2 Frontend ←→ Agent IA Interface ←→ n8n Workflows ←→ OpenAI GPT-4 ←→ Base ATARYS
```

### **Composants Techniques**

#### **1. Interface Tchat Intégrée**
```javascript
// Composant React pour l'agent IA
// frontend/src/components/AgentIA.jsx
const AgentIA = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [workflows, setWorkflows] = useState([]);
  
  // Interface flottante accessible depuis toute page
  return (
    <div className="fixed bottom-4 right-4 z-50">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="bg-blue-600 text-white p-4 rounded-full shadow-lg"
      >
        🤖 Agent IA
      </button>
      {isOpen && <ChatInterface />}
    </div>
  );
};
```

#### **2. APIs de Communication n8n**
```python
# backend/app/routes/agent_ia.py
@agent_ia_bp.route('/api/agent-ia/webhook/<workflow_id>', methods=['POST'])
def receive_n8n_webhook(workflow_id):
    """Réception des webhooks n8n"""
    data = request.get_json()
    
    # Traitement selon le type de workflow
    if workflow_id == 'extraction-devis':
        return handle_devis_extraction(data)
    elif workflow_id == 'generation-rapport':
        return handle_rapport_generation(data)
    
    return jsonify({'success': True, 'message': 'Webhook reçu'})

@agent_ia_bp.route('/api/agent-ia/workflows', methods=['GET'])
def get_available_workflows():
    """Liste des workflows n8n disponibles"""
    workflows = [
        {
            'id': 'extraction-devis',
            'name': 'Extraction Devis Excel',
            'description': 'Analyse automatique des devis vers base de données',
            'status': 'active',
            'trigger_url': '/webhook/extraction-devis'
        }
    ]
    return jsonify({'success': True, 'data': workflows})
```

#### **3. Service Agent IA Backend**
```python
# backend/app/services/agent_ia_service.py
class AgentIAService:
    def __init__(self):
        self.n8n_base_url = "http://localhost:5678"
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
    
    def trigger_workflow(self, workflow_id, data):
        """Déclencher un workflow n8n"""
        webhook_url = f"{self.n8n_base_url}/webhook/{workflow_id}"
        response = requests.post(webhook_url, json=data)
        return response.json()
    
    def get_workflow_status(self, execution_id):
        """Statut d'un workflow en cours"""
        # API n8n pour suivre l'exécution
        pass
    
    def chat_with_ai(self, message, context=None):
        """Interface avec OpenAI pour le tchat"""
        # Intégration OpenAI pour assistance utilisateur
        pass
```

### **Workflow 1 : Extraction Devis Excel**

#### **Configuration n8n**
```json
{
  "name": "ATARYS - Extraction Devis",
  "nodes": [
    {
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "/extraction-devis",
        "httpMethod": "POST"
      }
    },
    {
      "name": "Read Excel File",
      "type": "n8n-nodes-base.spreadsheetFile",
      "parameters": {
        "operation": "read",
        "binaryProperty": "file"
      }
    },
    {
      "name": "OpenAI Analysis",
      "type": "n8n-nodes-base.openAi",
      "parameters": {
        "model": "gpt-4",
        "messages": [
          {
            "role": "system",
            "content": "Analyse ce devis BTP et extrait : numéro devis, client, montant HT, heures main d'œuvre, familles d'ouvrage. Format JSON pour ATARYS."
          }
        ]
      }
    },
    {
      "name": "Insert ATARYS DB",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "http://localhost:5000/api/devis-chantiers/"
      }
    }
  ]
}
```

#### **API Integration ATARYS**
```python
# backend/app/routes/devis_chantiers.py
@devis_bp.route('/api/devis-chantiers/from-ia', methods=['POST'])
def create_devis_from_ia():
    """Création devis depuis extraction IA"""
    data = request.get_json()
    
    # Validation des données IA
    schema = DevisChantierIASchema()
    validated_data = schema.load(data)
    
    # Création avec marquage source IA
    devis = DevisChantier(**validated_data)
    devis.source = 'AGENT_IA'
    devis.date_import = datetime.utcnow()
    
    db.session.add(devis)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': devis_schema.dump(devis),
        'message': 'Devis créé par Agent IA'
    })
```

### **Interface Utilisateur Agent IA**

#### **Composant Tchat**
```jsx
// frontend/src/components/AgentIAChat.jsx
const AgentIAChat = () => {
  const [messages, setMessages] = useState([
    {
      type: 'system',
      content: 'Bonjour ! Je suis votre Agent IA ATARYS. Comment puis-je vous aider ?',
      timestamp: new Date()
    }
  ]);
  
  const quickActions = [
    {
      label: 'Extraire un devis',
      action: 'extract-devis',
      icon: '📄'
    },
    {
      label: 'Générer un rapport',
      action: 'generate-report', 
      icon: '📊'
    }
  ];
  
  return (
    <div className="bg-white border rounded-lg shadow-xl w-80 h-96">
      <div className="p-4 border-b bg-blue-600 text-white rounded-t-lg">
        <h3 className="font-bold">🤖 Agent IA ATARYS</h3>
      </div>
      
      <div className="p-4 h-64 overflow-y-auto">
        {messages.map((msg, idx) => (
          <div key={idx} className={`mb-2 ${msg.type === 'user' ? 'text-right' : ''}`}>
            <div className={`inline-block p-2 rounded ${
              msg.type === 'user' 
                ? 'bg-blue-100 text-blue-800' 
                : 'bg-gray-100 text-gray-800'
            }`}>
              {msg.content}
            </div>
          </div>
        ))}
      </div>
      
      <div className="p-2 border-t">
        <div className="flex gap-1 mb-2">
          {quickActions.map(action => (
            <button
              key={action.action}
              className="text-xs bg-gray-100 px-2 py-1 rounded"
              onClick={() => handleQuickAction(action.action)}
            >
              {action.icon} {action.label}
            </button>
          ))}
        </div>
        <input
          type="text"
          placeholder="Tapez votre message..."
          className="w-full p-2 border rounded"
          onKeyPress={handleSendMessage}
        />
      </div>
    </div>
  );
};
```

### **Configuration et Déploiement**

#### **Variables d'Environnement**
```bash
# .env - Configuration Agent IA
OPENAI_API_KEY=sk-...
N8N_BASE_URL=http://localhost:5678
N8N_WEBHOOK_URL=https://votre-domaine.com/webhook
AGENT_IA_ENABLED=true
```

#### **Requirements Supplémentaires**
```txt
# backend/requirements/development.txt - Ajouts Agent IA
openai==1.3.0
requests==2.31.0
celery==5.3.0  # Pour tâches asynchrones
redis==4.6.0   # Cache workflows
```

### **Monitoring et Analytics**

#### **Dashboard Agent IA**
```python
# backend/app/routes/agent_ia_analytics.py
@analytics_bp.route('/api/agent-ia/stats', methods=['GET'])
def get_agent_stats():
    """Statistiques utilisation Agent IA"""
    stats = {
        'workflows_executed': db.session.query(WorkflowExecution).count(),
        'devis_extracted': db.session.query(DevisChantier).filter_by(source='AGENT_IA').count(),
        'success_rate': calculate_success_rate(),
        'avg_processing_time': calculate_avg_processing_time()
    }
    return jsonify({'success': True, 'data': stats})
```

---

## 🚀 **Fonctionnalités Avancées**

### **1. Gestion des ENUM**
- ✅ Interface utilisateur intuitive
- ✅ Validation des valeurs
- ✅ Génération automatique du code SQLAlchemy
- ✅ Support SQLite (conversion en TEXT)

### **2. Relations ForeignKey**
- ✅ Sélection de table cible
- ✅ Sélection de colonne cible
- ✅ Configuration des actions (CASCADE, RESTRICT, SET NULL)
- ✅ Validation des relations

### **3. Génération de Code**
- ✅ Modèles SQLAlchemy avec BaseModel
- ✅ Routes API REST standardisées
- ✅ Schémas Marshmallow de validation
- ✅ Instructions de migration

### **4. Interface Utilisateur**
- ✅ Formulaire dynamique
- ✅ Validation en temps réel
- ✅ Gestion des erreurs
- ✅ Instructions claires

---

## 🔗 Liens Utiles

- **[Modèles SQLAlchemy](./database-schema.md)** - Structure des tables
- **[API Endpoints](./api-endpoints.md)** - Spécifications REST
- **[Service Generator](./table-generator.md)** - Documentation technique
- **[ATARYS_MODULES.md](../../00-overview/ATARYS_MODULES.md)** - Nomenclature officielle

---

## 🎯 **Prochaines Étapes**

### **Phase 1 : Optimisations**
1. **Interface de configuration** : Paramètres système
2. **Gestion des préférences** : Personnalisation utilisateur
3. **Audit complet** : Logs et traçabilité

### **Phase 2 : Fonctionnalités Avancées**
1. **Sauvegarde/Restauration** : Outils de maintenance
2. **Import/Export** : Données et structures
3. **Templates** : Modèles de tables prédéfinis

### **Phase 3 : Agent IA** (après consolidation base de données)
1. **Interface Tchat** : Composant React flottant accessible depuis toute page
2. **APIs n8n** : Endpoints webhooks pour communication avec workflows
3. **Workflow Extraction Devis** : Premier workflow opérationnel avec OpenAI
4. **Service Backend** : `AgentIAService` pour gestion des workflows
5. **Monitoring** : Dashboard de suivi des automatisations IA
6. **Workflows IA Avancés** : Génération rapports, analyses prédictives

---

**✅ Module 12 - PARAMÈTRES : Interface complète et opérationnelle avec gestion des ENUM !** 🎉
