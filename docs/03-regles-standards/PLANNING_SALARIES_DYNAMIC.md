# 📅 **PLANNING SALARIÉS - LIAISON DYNAMIQUE**

## 🎯 **Vue d'ensemble**

Le planning des salariés (Module 1.1) a été mis à jour pour utiliser **dynamiquement** les données de la table `salaries` au lieu de données hardcodées. Cette amélioration garantit la cohérence entre le module de gestion des salariés (Module 9.1) et le planning.

## 🔄 **Changements Implémentés**

### **✅ Suppression des données hardcodées**
- **AVANT** : `SALARIES_DATA` hardcodé dans `PlanningSalaries.jsx`
- **APRÈS** : Appel API dynamique vers `/api/salaries/?actif=true`

### **✅ Fonctionnalités conservées**
- ✅ **Gestion des dates d'entrée/sortie** : Les salariés n'apparaissent que pendant leur période d'activité
- ✅ **Positionnement par colonne** : Utilise le champ `colonne_planning` de la base de données
- ✅ **Filtrage des salariés actifs** : Seuls les salariés sans date de sortie ou avec une date future sont affichés
- ✅ **Interface utilisateur** : Même design et comportement qu'avant

## 🏗️ **Architecture Technique**

### **Frontend - PlanningSalaries.jsx**
```jsx
// États pour la gestion des données dynamiques
const [salaries, setSalaries] = useState([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

// Chargement des salariés depuis l'API
useEffect(() => {
  const fetchSalaries = async () => {
    const response = await fetch('/api/salaries/?actif=true');
    const data = await response.json();
    if (data.success) {
      setSalaries(data.data);
    }
  };
  fetchSalaries();
}, []);
```

### **Backend - API Enhanced**
```python
@module_9_bp.route('/api/salaries/', methods=['GET'])
def list_salaries():
    actif = request.args.get('actif', type=str)
    
    if actif == 'true':
        # Filtrer les salariés actifs
        from datetime import date
        today = date.today()
        items = Salaries.query.filter(
            (Salaries.date_sortie.is_(None)) | 
            (Salaries.date_sortie > today)
        ).all()
    else:
        items = Salaries.query.all()
```

## 📊 **Logique de Positionnement**

### **Utilisation du champ `colonne_planning`**
- **Position 1** : Premier salarié dans la première colonne
- **Position 2** : Deuxième salarié dans la deuxième colonne
- **Position N** : N-ième salarié dans la N-ième colonne

### **Fonction `getSalariesForDate()` adaptée**
```jsx
function getSalariesForDate(date, salaries) {
  const result = Array(12).fill("");
  salaries.forEach(salary => {
    if (!salary || !salary.date_entree || !salary.colonne_planning) return;
    
    const entree = new Date(salary.date_entree);
    const sortie = salary.date_sortie ? new Date(salary.date_sortie) : null;
    
    if (entree <= date && (!sortie || date <= sortie)) {
      // Positionner selon colonne_planning
      result[salary.colonne_planning - 1] = salary.prenom;
    }
  });
  return result;
}
```

## 🎨 **Interface Utilisateur**

### **États de chargement et d'erreur**
- **Chargement** : Spinner animé avec message "Chargement des salariés..."
- **Erreur** : Message d'erreur avec bouton "Réessayer"
- **Succès** : Affichage normal du planning

### **Compteur dynamique**
```jsx
{getSalariesForDateLimited(dateVisible, salaries).filter(s => s !== '').length} 
salarié{getSalariesForDateLimited(dateVisible, salaries).filter(s => s !== '').length > 1 ? 's' : ''} 
actif{getSalariesForDateLimited(dateVisible, salaries).filter(s => s !== '').length > 1 ? 's' : ''} 
aujourd'hui
```

## 🔧 **Configuration et Maintenance**

### **Champ `colonne_planning` obligatoire**
- **Type** : String (pour flexibilité)
- **Valeurs** : "1", "2", "3", etc.
- **Utilisation** : Position dans le planning (1 = première colonne)

### **Gestion des dates**
- **`date_entree`** : Date d'embauche (obligatoire)
- **`date_sortie`** : Date de départ (optionnelle)
- **Logique** : Salarié visible si `date_entree <= date_actuelle <= date_sortie`

### **Affichage des noms**
- **Champ utilisé** : `salary.nom` (contient le prénom dans la base de données)
- **Raison** : Dans la structure ATARYS, le prénom est stocké dans le champ `nom`
- **Affichage** : Seuls les prénoms sont affichés dans le planning

### **Scroll automatique vers la date du jour**
- **Comportement** : Au chargement, le planning se positionne automatiquement sur la date actuelle
- **Implémentation** : `useEffect` avec dépendances `[isMounted, todayRowIndex, rows]`
- **Centrage** : La date du jour est centrée dans la vue avec `scrollIntoView({ block: 'center' })`

## 🚀 **Avantages de cette Implémentation**

### **✅ Cohérence des données**
- Une seule source de vérité : la base de données
- Mise à jour automatique lors de modifications dans Module 9.1

### **✅ Flexibilité**
- Ajout/suppression de salariés sans modification du code
- Changement de position via le champ `colonne_planning`

### **✅ Robustesse**
- Gestion d'erreurs complète
- États de chargement appropriés
- Validation des données côté serveur

### **✅ Performance**
- Cache des données avec `useState`
- Appel API unique au chargement
- Pas de rechargement inutile

## 🔍 **Tests et Validation**

### **Scénarios de test**
1. **Salarié actif** : Apparaît dans sa colonne assignée
2. **Salarié inactif** : N'apparaît pas (date de sortie passée)
3. **Salarié futur** : N'apparaît pas (date d'entrée future)
4. **Erreur API** : Affichage du message d'erreur
5. **Chargement** : Affichage du spinner

### **Validation des données**
- ✅ Vérification du format des dates
- ✅ Validation du champ `colonne_planning`
- ✅ Gestion des valeurs nulles/undefined

## 📝 **Documentation Technique**

### **API Endpoint**
```
GET /api/salaries/?actif=true
```

### **Réponse API**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "prenom": "GOUJON",
      "nom": "ROMAIN",
      "colonne_planning": "1",
      "date_entree": "2018-05-14",
      "date_sortie": null,
      // ... autres champs
    }
  ],
  "message": "11 salaries trouvés"
}
```

### **Structure des données**
- **`colonne_planning`** : Position dans le planning (string)
- **`date_entree`** : Date d'embauche (YYYY-MM-DD)
- **`date_sortie`** : Date de départ (YYYY-MM-DD ou null)
- **`prenom`** : Prénom affiché dans le planning

## 🎯 **Utilisation**

### **Pour les utilisateurs**
1. **Ajouter un salarié** : Via Module 9.1 → Planning mis à jour automatiquement
2. **Modifier la position** : Changer `colonne_planning` dans Module 9.1
3. **Désactiver un salarié** : Ajouter une `date_sortie` dans Module 9.1

### **Pour les développeurs**
1. **Ajouter un salarié** : Utiliser l'API POST `/api/salaries/`
2. **Modifier la position** : Utiliser l'API PUT `/api/salaries/{id}`
3. **Filtrer les actifs** : Utiliser le paramètre `?actif=true`

## 🔮 **Évolutions Futures**

### **Améliorations possibles**
- **Tri automatique** : Par ancienneté ou qualification
- **Filtres avancés** : Par type de contrat, qualification, etc.
- **Export PDF** : Génération de planning imprimable
- **Notifications** : Alertes pour départs/arrivées

### **Optimisations**
- **Cache intelligent** : Mise en cache des données avec invalidation
- **Pagination** : Pour de gros volumes de salariés
- **WebSocket** : Mise à jour en temps réel

---

**📋 Cette implémentation garantit une cohérence parfaite entre la gestion des salariés et leur affichage dans le planning, tout en conservant toutes les fonctionnalités existantes.** 