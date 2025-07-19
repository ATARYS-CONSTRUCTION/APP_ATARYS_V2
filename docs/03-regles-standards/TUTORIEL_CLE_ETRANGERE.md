# 🔗 Tutoriel : Création de Clés Étrangères dans ATARYS V2

> **Guide complet pour créer des relations entre tables dans ATARYS**  
> Architecture SQLAlchemy + Flask + React + BaseModel pattern  
> **VERSION 2** : Workflow opérationnel avec outils intégrés  
> Dernière mise à jour : 16/07/2025

---

## 🎯 **Objectif du Tutoriel**

Créer une relation entre deux tables ATARYS en suivant l'architecture V2 :
1. **Clé étrangère** : Contrainte de base de données
2. **Relation Python** : Accès ORM avec SQLAlchemy
3. **Interface frontend** : Dropdowns et validation
4. **API REST** : Endpoints pour les relations

---

## 🏗️ **Architecture ATARYS V2 - Relations**

### **Stack Technique**
- **Base de données** : SQLite avec contraintes FOREIGN KEY
- **ORM** : SQLAlchemy 2.0+ avec `db.relationship()`
- **Backend** : Flask avec API REST standardisée
- **Frontend** : React avec dropdowns dynamiques
- **Validation** : Marshmallow pour les schémas

### **Pattern Standard ATARYS**
```python
# 1. Clé étrangère dans le modèle source
foreign_key_id = db.Column(db.Integer, db.ForeignKey('target_table.id'), nullable=False)

# 2. Relation Python pour l'accès ORM
relation = db.relationship('TargetModel', backref='source_models', lazy='select')

# 3. Validation Marshmallow
class SourceSchema(Schema):
    foreign_key_id = fields.Integer(required=True, validate=validate.Range(min=1))
```

---

## 📋 **Étapes Détaillées**

### **Étape 1 : Préparation - Identifier les Tables**

#### **1.1 Analyser les besoins métier**
```sql
-- Exemple : Relation entre chantiers et clients
-- Table source : chantiers (contient la clé étrangère)
-- Table cible : clients (référencée par la clé étrangère)
```

#### **1.2 Vérifier l'existence des tables**
- Aller dans **Module 12.1** → **Base de données**
- Onglet **"Tables existantes"** pour voir les tables disponibles
- Vérifier que les deux tables existent déjà

#### **1.3 Identifier les colonnes de liaison**
```sql
-- Exemple concret :
-- Table chantiers : client_id (clé étrangère)
-- Table clients : id (clé primaire référencée)
```

---

### **Étape 2 : Création de la Clé Étrangère**

#### **2.1 Utiliser l'interface frontend**
1. Aller dans **Module 12.1** → **Base de données**
2. Onglet **"Guide des modifications"**
3. Cliquer sur **"🔗 Ajouter une clé étrangère"**

#### **2.2 Remplir le formulaire de clé étrangère**
```javascript
// Exemple pour chantiers → clients
{
  source_table: "chantiers",        // Table qui contient la FK
  source_column: "client_id",       // Colonne FK à créer
  target_table: "clients",          // Table référencée
  target_column: "id",              // Colonne référencée (généralement 'id')
  relation_name: "client"           // Nom de la relation Python
}
```

#### **2.3 Générer le code de clé étrangère**
- Cliquer sur **"Générer le code"**
- Copier le code SQL généré
- Exécuter la migration Flask-Migrate

---

### **Étape 3 : Ajout de la Relation Python**

#### **3.1 Utiliser l'interface de relation Python**
1. Dans le même onglet **"Guide des modifications"**
2. Cliquer sur **"👨‍💻 Ajouter une relation Python"**

#### **3.2 Configurer la relation**
```javascript
// Configuration de la relation
{
  sourceTable: "chantiers",         // Table source
  targetTable: "clients",           // Table cible
  sourceClass: "Chantier",          // Classe Python source
  targetClass: "Client",            // Classe Python cible
  relationName: "client",           // Nom de l'attribut relation
  backrefName: "chantiers",         // Nom du backref (optionnel)
  relationType: "many-to-one",      // Type de relation
  cascade: "",                      // Cascade (optionnel)
  lazy: "select",                   // Lazy loading
  nullable: false                   // Nullable
}
```

#### **3.3 Générer et copier le code**
- Cliquer sur **"🔧 Générer le code"**
- Copier le code dans le modèle source (`backend/app/models/module_X.py`)
- Copier le code backref dans le modèle cible si bidirectionnel

---

### **Étape 4 : Migration de la Base de Données**

#### **4.1 Créer la migration**
```bash
# Dans le terminal, depuis la racine du projet
cd backend
flask db migrate -m "Add foreign key chantiers.client_id"
```

#### **4.2 Appliquer la migration**
```bash
flask db upgrade
```

#### **4.3 Vérifier la migration**
```bash
# Vérifier que la contrainte est créée
flask db current
```

---

### **Étape 5 : Mise à Jour des Schémas Marshmallow**

#### **5.1 Modifier le schéma source**
```python
# backend/app/schemas/module_X.py
from marshmallow import Schema, fields, validate

class ChantierSchema(Schema):
    id = fields.Integer(dump_only=True)
    client_id = fields.Integer(required=True, validate=validate.Range(min=1))
    # ... autres champs
    
    # Relation pour l'affichage
    client = fields.Nested('ClientSchema', dump_only=True)
```

#### **5.2 Modifier le schéma cible (si bidirectionnel)**
```python
# backend/app/schemas/module_Y.py
class ClientSchema(Schema):
    id = fields.Integer(dump_only=True)
    # ... autres champs
    
    # Backref pour l'affichage
    chantiers = fields.Nested('ChantierSchema', many=True, dump_only=True)
```

---

### **Étape 6 : Mise à Jour des Routes API**

#### **6.1 Ajouter l'import du modèle cible**
```python
# backend/app/routes/module_X.py
from app.models.module_Y import Client  # Modèle cible
from app.models.module_X import Chantier  # Modèle source
```

#### **6.2 Modifier les endpoints pour inclure la relation**
```python
# Exemple : Récupérer un chantier avec son client
@chantier_bp.route('/api/chantiers/<int:id>', methods=['GET'])
def get_chantier(id):
    chantier = Chantier.query.get_or_404(id)
    return jsonify({
        'success': True,
        'data': ChantierSchema().dump(chantier),
        'message': 'Chantier récupéré'
    })
```

---

### **Étape 7 : Interface Frontend**

#### **7.1 Ajouter les dropdowns dans les formulaires**
```javascript
// Dans le composant de formulaire
const [clients, setClients] = useState([]);

// Charger les clients au montage
useEffect(() => {
  fetch('/api/clients/')
    .then(res => res.json())
    .then(data => {
      if (data.success) setClients(data.data);
    });
}, []);

// Rendu du dropdown
<select 
  value={formData.client_id} 
  onChange={e => setFormData({...formData, client_id: e.target.value})}
>
  <option value="">Sélectionner un client...</option>
  {clients.map(client => (
    <option key={client.id} value={client.id}>
      {client.nom} {client.prenom}
    </option>
  ))}
</select>
```

#### **7.2 Validation côté frontend**
```javascript
// Validation avant envoi
const validateForm = () => {
  if (!formData.client_id) {
    setError('Le client est obligatoire');
    return false;
  }
  return true;
};
```

---

## 🔧 **Outils Intégrés ATARYS**

### **1. Interface de Création de Clés Étrangères**
- **Localisation** : Module 12.1 → Base de données → Guide des modifications
- **Fonctionnalité** : Génération automatique du code SQL
- **Validation** : Vérification de l'existence des tables

### **2. Interface de Relations Python**
- **Localisation** : Même onglet que les clés étrangères
- **Fonctionnalité** : Génération du code `db.relationship()`
- **Options** : Type de relation, cascade, lazy loading

### **3. Commandes de Migration**
- **Interface** : Onglet "Migrations" avec boutons de copie
- **Commandes** : `flask db migrate` et `flask db upgrade`
- **Conseils** : Guillemets doubles pour PowerShell

---

## 📝 **Exemple Complet : Chantiers → Clients**

### **Contexte Métier**
- **Table chantiers** : Contient les projets
- **Table clients** : Contient les informations clients
- **Relation** : Chaque chantier appartient à un client

### **Étape 1 : Créer la clé étrangère**
```sql
-- Code généré automatiquement
ALTER TABLE chantiers ADD COLUMN client_id INTEGER;
ALTER TABLE chantiers ADD CONSTRAINT fk_chantiers_client 
    FOREIGN KEY (client_id) REFERENCES clients (id);
```

### **Étape 2 : Ajouter la relation Python**
```python
# Dans backend/app/models/module_3.py (chantiers)
class Chantier(BaseModel):
    __tablename__ = 'chantiers'
    
    # ... autres colonnes ...
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    
    # Relation Python
    client = db.relationship('Client', backref='chantiers', lazy='select')
```

### **Étape 3 : Schéma Marshmallow**
```python
# backend/app/schemas/module_3.py
class ChantierSchema(Schema):
    id = fields.Integer(dump_only=True)
    client_id = fields.Integer(required=True, validate=validate.Range(min=1))
    # ... autres champs ...
    client = fields.Nested('ClientSchema', dump_only=True)
```

### **Étape 4 : API REST**
```python
# backend/app/routes/module_3.py
@chantier_bp.route('/api/chantiers/', methods=['POST'])
def create_chantier():
    data = request.get_json()
    
    # Validation avec le schéma
    schema = ChantierSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({
            'success': False,
            'message': 'Données invalides',
            'errors': err.messages
        }), 400
    
    # Création avec relation
    chantier = Chantier(**validated_data)
    chantier.save()
    
    return jsonify({
        'success': True,
        'data': schema.dump(chantier),
        'message': 'Chantier créé avec succès'
    }), 201
```

---

## ⚠️ **Points d'Attention**

### **1. Ordre des Opérations**
1. ✅ Créer d'abord la table cible (clients)
2. ✅ Créer ensuite la table source (chantiers)
3. ✅ Ajouter la clé étrangère
4. ✅ Ajouter la relation Python
5. ✅ Mettre à jour les schémas
6. ✅ Tester les APIs

### **2. Validation des Données**
- **Côté frontend** : Validation avant envoi
- **Côté backend** : Validation Marshmallow
- **Base de données** : Contraintes FOREIGN KEY

### **3. Performance**
- **Lazy loading** : `lazy='select'` par défaut
- **Index** : Créer des index sur les clés étrangères
- **Pagination** : Pour les relations one-to-many

### **4. Gestion d'Erreurs**
- **Clé étrangère inexistante** : Validation côté frontend
- **Suppression en cascade** : Configurer `cascade='all, delete-orphan'`
- **Messages d'erreur** : Expliquer le problème à l'utilisateur

---

## 🎯 **Workflow Recommandé**

### **Phase 1 : Planification**
1. Identifier les tables source et cible
2. Définir le type de relation (one-to-many, many-to-one, etc.)
3. Choisir les noms des relations Python

### **Phase 2 : Implémentation**
1. Utiliser l'interface frontend pour générer le code
2. Copier-coller le code dans les modèles
3. Exécuter les migrations
4. Mettre à jour les schémas et routes

### **Phase 3 : Test et Validation**
1. Tester les APIs avec des données réelles
2. Vérifier les dropdowns dans l'interface
3. Valider les contraintes de base de données
4. Documenter les relations créées

---

## 📚 **Ressources Complémentaires**

- **Architecture ATARYS** : `docs/02-architecture/ATARYS_ARCHITECTURE.md`
- **Schéma Base de Données** : `docs/02-architecture/DATABASE_SCHEMA.md`
- **Standards de Développement** : `docs/03-regles-standards/WORKFLOWS.md`
- **APIs Existantes** : `docs/02-architecture/API_ENDPOINTS.md`

---

**Ce tutoriel suit les standards ATARYS V2 et utilise les outils intégrés pour une création de relations robuste et maintenable.** 