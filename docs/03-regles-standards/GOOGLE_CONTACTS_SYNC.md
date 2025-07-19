# 🔗 **SYNCHRONISATION GOOGLE CONTACTS ↔ ATARYS**

## 🎯 **Vue d'ensemble**

Système de synchronisation bidirectionnelle entre ATARYS et Google Contacts permettant de :
- **Synchroniser** les clients ATARYS vers Google Contacts
- **Importer** les contacts Google vers ATARYS
- **Maintenir** la cohérence entre les deux bases de données
- **Gérer** les modifications en temps réel

## 🏗️ **Architecture Technique**

### **Stack Technologique**
- **API Google** : Google People API v1
- **Authentification** : OAuth2 avec refresh token
- **Backend** : Flask + SQLAlchemy (ATARYS V2)
- **Synchronisation** : Bidirectionnelle avec gestion des conflits

### **Mapping des Données**

#### **ATARYS → Google Contacts**
```python
# Correspondance des champs
'nom' → 'names.familyName'
'prenom' → 'names.givenName'
'email' → 'emailAddresses.value'
'telephone' → 'phoneNumbers.value'
'adresse' → 'addresses.formattedValue'
'ville' → 'addresses.city'
'code_postal' → 'addresses.postalCode'
'entreprise' → 'organizations.name'
'fonction' → 'organizations.title'
```

#### **Google Contacts → ATARYS**
```python
# Correspondance inverse
'names.familyName' → 'nom'
'names.givenName' → 'prenom'
'emailAddresses.value' → 'email'
'phoneNumbers.value' → 'telephone'
'addresses.formattedValue' → 'adresse'
'addresses.city' → 'ville'
'addresses.postalCode' → 'code_postal'
'organizations.name' → 'entreprise'
'organizations.title' → 'fonction'
```

## 🔧 **Configuration Initiale**

### **1. Créer un Projet Google Cloud**
1. Aller sur https://console.cloud.google.com
2. Créer un nouveau projet
3. Activer l'API "Google People API"
4. Créer des credentials OAuth2 pour application de bureau

### **2. Télécharger les Credentials**
1. Dans Google Cloud Console → APIs & Services → Credentials
2. Créer des credentials OAuth2
3. Télécharger le fichier JSON
4. Placer le fichier dans `data/google_credentials.json`

### **3. Installer les Dépendances**
```bash
cd backend
pip install -r requirements/google_contacts.txt
```

## 🛣️ **APIs Disponibles**

### **Authentification**
```http
POST /api/google-contacts/auth
```
**Réponse :**
```json
{
  "success": true,
  "message": "✅ Authentification Google réussie",
  "data": {
    "authenticated": true,
    "service_available": true
  }
}
```

### **Synchronisation ATARYS → Google**
```http
POST /api/google-contacts/sync-to-google/{client_id}
```
**Réponse :**
```json
{
  "success": true,
  "message": "Contact created dans Google Contacts",
  "data": {
    "google_id": "people/c123456789",
    "action": "created"
  }
}
```

### **Synchronisation Google → ATARYS**
```http
POST /api/google-contacts/sync-from-google/{google_id}
```
**Réponse :**
```json
{
  "success": true,
  "message": "Client created dans ATARYS",
  "data": {
    "client_id": 42,
    "action": "created"
  }
}
```

### **Synchronisation Complète**
```http
POST /api/google-contacts/sync-all
```
**Réponse :**
```json
{
  "success": true,
  "message": "Synchronisation complète terminée",
  "data": {
    "atarys_to_google": {"success": 15, "errors": 0},
    "google_to_atarys": {"success": 8, "errors": 0}
  }
}
```

### **Statut du Service**
```http
GET /api/google-contacts/status
```
**Réponse :**
```json
{
  "success": true,
  "data": {
    "authenticated": true,
    "service_available": true,
    "credentials_file_exists": true,
    "token_file_exists": true
  },
  "message": "✅ Service Google Contacts disponible"
}
```

### **Liste des Contacts Google**
```http
GET /api/google-contacts/list-contacts
```
**Réponse :**
```json
{
  "success": true,
  "data": [
    {
      "google_id": "people/c123456789",
      "nom": "Dupont",
      "prenom": "Jean",
      "email": "jean.dupont@example.com",
      "etag": "\"abc123\""
    }
  ],
  "message": "25 contacts trouvés dans Google"
}
```

### **Instructions de Configuration**
```http
GET /api/google-contacts/setup-instructions
```
**Réponse :**
```json
{
  "success": true,
  "data": {
    "steps": [
      {
        "step": 1,
        "title": "Créer un projet Google Cloud",
        "description": "Allez sur https://console.cloud.google.com et créez un nouveau projet",
        "url": "https://console.cloud.google.com"
      }
    ],
    "required_files": ["data/google_credentials.json"],
    "scopes": ["https://www.googleapis.com/auth/contacts"]
  },
  "message": "Instructions de configuration Google Contacts"
}
```

## 🔄 **Logique de Synchronisation**

### **Gestion des Conflits**
1. **Email comme clé unique** : Utilisé pour identifier les contacts
2. **ETag Google** : Détecte les modifications côté Google
3. **Timestamp ATARYS** : Détecte les modifications côté ATARYS
4. **Résolution automatique** : Priorité aux modifications les plus récentes

### **Stratégie de Synchronisation**
```python
# Algorithme de synchronisation
def sync_contact(client_id):
    # 1. Récupérer le client ATARYS
    client = Clients.query.get(client_id)
    
    # 2. Chercher le contact Google par email
    google_contact = find_contact_by_email(client.email)
    
    # 3. Comparer les timestamps
    if google_contact and client.google_last_sync < google_contact['updated']:
        # Google plus récent → Mettre à jour ATARYS
        update_atarys_from_google(google_contact)
    else:
        # ATARYS plus récent → Mettre à jour Google
        update_google_from_atarys(client)
```

## 📊 **Gestion des Erreurs**

### **Erreurs Courantes**
1. **Authentification échouée** : Vérifier les credentials
2. **API non activée** : Activer Google People API
3. **Quota dépassé** : Limites Google API
4. **Conflit de données** : Résolution automatique

### **Logs et Monitoring**
```python
# Logs de synchronisation
logs/google_contacts_sync.log

# Métriques
- Nombre de synchronisations réussies
- Nombre d'erreurs
- Temps de synchronisation
- Contacts traités
```

## 🚀 **Utilisation Pratique**

### **Interface Utilisateur (Frontend)**
```jsx
// Composant de synchronisation
const GoogleContactsSync = () => {
  const [syncStatus, setSyncStatus] = useState('idle');
  
  const handleSyncAll = async () => {
    setSyncStatus('syncing');
    try {
      const response = await fetch('/api/google-contacts/sync-all', {
        method: 'POST'
      });
      const result = await response.json();
      if (result.success) {
        setSyncStatus('success');
        // Afficher les résultats
      }
    } catch (error) {
      setSyncStatus('error');
    }
  };
  
  return (
    <div>
      <button onClick={handleSyncAll}>
        Synchroniser avec Google Contacts
      </button>
      <div>Statut: {syncStatus}</div>
    </div>
  );
};
```

### **Synchronisation Automatique**
```python
# Tâche planifiée (cron)
def auto_sync_contacts():
    """Synchronisation automatique toutes les heures"""
    sync_service = GoogleContactsSync()
    if sync_service.authenticate():
        result = sync_service.sync_all_contacts()
        log_sync_result(result)
```

## 🔒 **Sécurité et Permissions**

### **Scopes OAuth2**
- `https://www.googleapis.com/auth/contacts` : Accès complet aux contacts

### **Stockage Sécurisé**
- **Credentials** : `data/google_credentials.json` (non versionné)
- **Tokens** : `data/google_contacts_token.pickle` (non versionné)
- **Cache** : Local uniquement, pas de partage

### **Permissions Requises**
- Lecture des contacts Google
- Écriture des contacts Google
- Gestion des profils utilisateur

## 📈 **Avantages de l'Intégration**

### **Pour ATARYS**
- ✅ **Cohérence** : Données clients synchronisées
- ✅ **Productivité** : Pas de saisie double
- ✅ **Fiabilité** : Sauvegarde cloud Google
- ✅ **Collaboration** : Partage d'équipe

### **Pour Google Contacts**
- ✅ **Organisation** : Gestion centralisée ATARYS
- ✅ **Automatisation** : Synchronisation bidirectionnelle
- ✅ **Intégration** : Workflow métier intégré

## 🚨 **Limitations et Considérations**

### **Limites Google API**
- **Quota** : 10,000 requêtes/jour par défaut
- **Rate limiting** : 1000 requêtes/100 secondes
- **Taille** : Contacts limités à 25,000

### **Gestion des Données**
- **Doublons** : Détection par email
- **Champs manquants** : Gestion des valeurs nulles
- **Formatage** : Normalisation des données

### **Performance**
- **Synchronisation incrémentale** : Seuls les changements
- **Cache intelligent** : Évite les requêtes inutiles
- **Traitement par lot** : Optimisation des performances

---

## 📚 **Ressources et Liens**

- **Google People API** : https://developers.google.com/people
- **OAuth2 Guide** : https://developers.google.com/identity/protocols/oauth2
- **ATARYS Documentation** : docs/01-guides-principaux/DEV_MASTER.md
- **Support** : Consulter les logs pour le dépannage 