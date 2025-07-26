# 📄 Module 8.1 - Extraction Intelligente de Documents

> **Extraction automatique et ventilation IA des factures/LCR fournisseurs**  
> **Module 8.1 : Comptabilité → Extraction Documents**  
> Dernière mise à jour : 20/01/2025

---

## 📋 Vue d'ensemble Module 8.1

**Objectif :** Automatiser complètement le traitement des LCR et factures fournisseurs via n8n + IA.

**Workflow complet :**
```
PDF → n8n extraction → IA matching → Validation utilisateur → Comptabilisation
```

**Tables gérées :**
- `extractions_documents` : Journal des PDF traités
- `factures_extraites` : Factures extraites par n8n
- `bons_livraison_extraits` : Détail avec ventilation IA

---

## 🗄️ Modèles SQLAlchemy

### **1. ExtractionDocument - Journal des traitements**

```python
# backend/app/models/module_8.py
class ExtractionDocument(BaseModel):
    """Trace de chaque PDF traité par les workflows n8n"""
    __tablename__ = 'extractions_documents'
    
    # Métadonnées du fichier
    nom_fichier = db.Column(db.String(255), nullable=False)
    taille_fichier = db.Column(db.Integer)
    hash_fichier = db.Column(db.String(64))  # SHA256 pour déduplication
    
    # Informations de traitement
    workflow_n8n_id = db.Column(db.String(20), default='8.1')
    statut = db.Column(db.String(20), default='EN_COURS')
    # Statuts possibles : EN_COURS, SUCCES, ERREUR, VALIDE, REJETE
    
    confidence_globale = db.Column(db.Numeric(3, 2))  # Score 0.00-1.00
    temps_traitement = db.Column(db.Integer)  # Millisecondes
    
    # Données brutes pour debug/historique
    json_n8n_brut = db.Column(db.Text)  # Réponse complète n8n
    json_ia_enrichi = db.Column(db.Text)  # Analyse IA avec suggestions
    
    # Métadonnées utilisateur
    valide_par_user_id = db.Column(db.Integer)  # Qui a validé
    date_validation = db.Column(db.DateTime)
    commentaire_validation = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Extraction {self.nom_fichier} - {self.statut}>'
    
    @property
    def needs_validation(self):
        """Détermine si l'extraction nécessite une validation manuelle"""
        return self.statut in ['SUCCES'] and not self.valide_par_user_id
    
    @property
    def factures_count(self):
        """Nombre de factures extraites de ce document"""
        return len(self.factures_extraites)
```

### **2. FactureExtraite - Données de facturation**

```python
class FactureExtraite(BaseModel):
    """Facture extraite d'un PDF par n8n"""
    __tablename__ = 'factures_extraites'
    
    # Liaison avec l'extraction source
    extraction_id = db.Column(db.Integer, db.ForeignKey('extractions_documents.id'), nullable=False)
    extraction = db.relationship('ExtractionDocument', backref='factures_extraites')
    
    # Données extraites par n8n
    numero_facture = db.Column(db.String(100), nullable=False)
    fournisseur = db.Column(db.String(100), nullable=False)
    date_facture = db.Column(db.Date)
    date_echeance = db.Column(db.Date)
    
    # Montants financiers (standard ATARYS : Numeric(10,2))
    total_ht = db.Column(db.Numeric(10, 2), default=0.00)
    total_ttc = db.Column(db.Numeric(10, 2), default=0.00)
    montant_tva = db.Column(db.Numeric(10, 2), default=0.00)
    
    # Références métier
    reference_chantier_detectee = db.Column(db.String(200))  # Trouvée par n8n
    
    # Statut de traitement
    statut_integration = db.Column(db.String(20), default='EXTRAIT')
    # Statuts : EXTRAIT, VALIDE, VENTILE, COMPTABILISE, REJETE
    
    # Contrôle de cohérence
    coherence_montants = db.Column(db.Boolean, default=True)
    nb_bons_detectes = db.Column(db.Integer, default=0)
    
    # Métadonnées utilisateur
    corrigee_par_user = db.Column(db.Boolean, default=False)
    corrections_apportees = db.Column(db.Text)  # JSON des champs modifiés
    
    def __repr__(self):
        return f'<Facture {self.numero_facture} - {self.fournisseur} - {self.total_ht}€>'
    
    @property
    def total_bons_ventiles(self):
        """Montant total des bons déjà ventilés"""
        return sum(bon.montant_ht for bon in self.bons_livraison 
                  if bon.chantier_affecte_id is not None)
    
    @property
    def ecart_ventilation(self):
        """Écart entre total facture et total bons ventilés"""
        return self.total_ht - self.total_bons_ventiles
    
    @property
    def ventilation_complete(self):
        """True si tous les bons sont ventilés"""
        return abs(self.ecart_ventilation) < 0.01
```

### **3. BonLivraisonExtrait - Détail avec IA**

```python
class BonLivraisonExtrait(BaseModel):
    """Bon de livraison extrait avec suggestions IA de ventilation"""
    __tablename__ = 'bons_livraison_extraits'
    
    # Liaison avec la facture
    facture_id = db.Column(db.Integer, db.ForeignKey('factures_extraites.id'), nullable=False)
    facture = db.relationship('FactureExtraite', backref='bons_livraison')
    
    # Données extraites par n8n
    numero_bon = db.Column(db.String(100), nullable=False)
    montant_ht = db.Column(db.Numeric(10, 2), default=0.00)
    reference_client = db.Column(db.String(200))
    description = db.Column(db.Text)
    
    # Analyse IA de ventilation
    chantier_suggere_id = db.Column(db.Integer)  # Suggestion IA principale
    confidence_suggestion = db.Column(db.Numeric(3, 2))  # Score 0.00-1.00
    raison_suggestion = db.Column(db.String(200))  # "Correspondance exacte 'DEBOIS'"
    
    suggestions_alternatives = db.Column(db.Text)  # JSON des autres suggestions
    
    # Ventilation finale (décision utilisateur)
    chantier_affecte_id = db.Column(db.Integer)  # Chantier final choisi
    type_affectation = db.Column(db.String(20))  # CHANTIER, FRAIS_GENERAUX, A_TRAITER
    
    # Apprentissage IA
    suggestion_acceptee = db.Column(db.Boolean)  # IA avait-elle raison ?
    correction_utilisateur = db.Column(db.Text)  # Feedback pour apprentissage
    
    # Métadonnées
    affecte_par_user_id = db.Column(db.Integer)
    date_affectation = db.Column(db.DateTime)
    commentaire_affectation = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Bon {self.numero_bon} - {self.montant_ht}€ - Chantier {self.chantier_affecte_id}>'
    
    @property
    def est_ventile(self):
        """True si le bon a été affecté à un chantier"""
        return self.chantier_affecte_id is not None
    
    @property
    def suggestion_acceptee_rate(self):
        """Taux d'acceptation des suggestions IA pour ce type de bon"""
        # Calcul basé sur l'historique des bons similaires
        pass
```

---

## 🔄 Services Métier

### **Service d'Intégration n8n**

```python
# backend/app/services/integration_n8n_service.py
class IntegrationN8nService:
    """Service pour traiter les extractions n8n et alimenter la BDD"""
    
    def integrer_extraction_complete(self, donnees_n8n):
        """
        Intégrer une extraction n8n complète
        
        Args:
            donnees_n8n (dict): JSON reçu du workflow n8n
            
        Returns:
            dict: Résultat de l'intégration avec IDs créés
        """
        try:
            # Étape 1 : Créer l'extraction conteneur
            extraction = self._creer_extraction_document(donnees_n8n)
            
            # Étape 2 : Créer la facture principale
            facture = self._creer_facture_extraite(donnees_n8n, extraction.id)
            
            # Étape 3 : Créer les bons avec analyse IA
            bons = self._creer_bons_avec_ia(donnees_n8n['bons_livraison'], facture.id)
            
            # Étape 4 : Mettre à jour les statistiques
            self._maj_statistiques_extraction(extraction, facture, bons)
            
            return {
                'success': True,
                'extraction_id': extraction.id,
                'facture_id': facture.id,
                'nb_bons': len(bons),
                'needs_validation': extraction.needs_validation
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _creer_bons_avec_ia(self, bons_data, facture_id):
        """Créer les bons avec suggestions IA de ventilation"""
        bons_crees = []
        
        for bon_data in bons_data:
            # Analyser la référence client avec l'IA
            suggestion_ia = self.ai_service.suggerer_chantier(
                reference=bon_data.get('reference_client'),
                montant=bon_data.get('montant_ht'),
                fournisseur=self.current_facture.fournisseur
            )
            
            bon = BonLivraisonExtrait(
                facture_id=facture_id,
                numero_bon=bon_data.get('numero_bon'),
                montant_ht=bon_data.get('montant_ht', 0),
                reference_client=bon_data.get('reference_client'),
                
                # Suggestions IA
                chantier_suggere_id=suggestion_ia.get('chantier_id'),
                confidence_suggestion=suggestion_ia.get('confidence'),
                raison_suggestion=suggestion_ia.get('raison'),
                suggestions_alternatives=json.dumps(suggestion_ia.get('alternatives', []))
            )
            bon.save()
            bons_crees.append(bon)
        
        return bons_crees
```

### **Service IA de Matching**

```python
# backend/app/services/ai_matching_service.py
class AIMatchingService:
    """Service d'intelligence artificielle pour le matching chantier"""
    
    def suggerer_chantier(self, reference, montant, fournisseur):
        """
        Suggérer un chantier pour un bon de livraison
        
        Args:
            reference (str): Référence client trouvée dans le bon
            montant (float): Montant du bon
            fournisseur (str): Fournisseur de la facture
            
        Returns:
            dict: Suggestion principale + alternatives
        """
        suggestions = []
        
        # 1. Recherche exacte par mots-clés
        exact_matches = self._recherche_exacte(reference)
        suggestions.extend(exact_matches)
        
        # 2. Recherche floue par similarité
        fuzzy_matches = self._recherche_floue(reference)
        suggestions.extend(fuzzy_matches)
        
        # 3. Analyse historique
        historical_matches = self._analyse_historique(fournisseur, montant)
        suggestions.extend(historical_matches)
        
        # 4. Scoring et ranking
        suggestions_ranked = self._calculer_scores(suggestions)
        
        if suggestions_ranked:
            principale = suggestions_ranked[0]
            alternatives = suggestions_ranked[1:3]  # Top 3 alternatives
            
            return {
                'chantier_id': principale['chantier_id'],
                'confidence': principale['score'],
                'raison': principale['raison'],
                'alternatives': alternatives
            }
        else:
            return {
                'chantier_id': None,
                'confidence': 0.0,
                'raison': 'Aucune correspondance trouvée',
                'alternatives': []
            }
    
    def _recherche_exacte(self, reference):
        """Recherche exacte dans les mots-clés des chantiers"""
        if not reference:
            return []
        
        # Recherche dans la table chantiers
        chantiers = db.session.query(Chantier).filter(
            Chantier.mots_cles.contains(reference.upper())
        ).all()
        
        matches = []
        for chantier in chantiers:
            matches.append({
                'chantier_id': chantier.id,
                'score': 1.0,
                'raison': f"Correspondance exacte '{reference}'",
                'type': 'exact'
            })
        
        return matches
    
    def _recherche_floue(self, reference):
        """Recherche approximative par similarité"""
        # Implémentation avec difflib ou fuzzywuzzy
        pass
    
    def enregistrer_feedback(self, bon_id, chantier_choisi, etait_suggestion_ia):
        """
        Enregistrer le feedback utilisateur pour l'apprentissage
        
        Args:
            bon_id (int): ID du bon traité
            chantier_choisi (int): Chantier finalement choisi
            etait_suggestion_ia (bool): L'utilisateur a-t-il suivi la suggestion IA
        """
        bon = BonLivraisonExtrait.query.get(bon_id)
        if bon:
            bon.suggestion_acceptee = etait_suggestion_ia
            bon.chantier_affecte_id = chantier_choisi
            bon.date_affectation = datetime.utcnow()
            bon.save()
            
            # Apprentissage automatique
            self._mise_a_jour_patterns(bon)
```

---

## 🛠️ Routes API Module 8.1

### **Endpoints de Réception n8n**

```python
# backend/app/routes/module_8.py
from app.services.integration_n8n_service import IntegrationN8nService

module_8 = Blueprint('module_8', __name__)
integration_service = IntegrationN8nService()

@module_8.route('/api/integration/n8n-webhook', methods=['POST'])
def recevoir_extraction_n8n():
    """Endpoint principal pour recevoir les extractions n8n"""
    try:
        donnees = request.get_json()
        
        # Validation du format
        if not donnees or 'workflow_info' not in donnees:
            return jsonify({
                'success': False,
                'message': 'Format JSON invalide'
            }), 400
        
        # Intégration complète
        resultat = integration_service.integrer_extraction_complete(donnees)
        
        if resultat['success']:
            return jsonify({
                'success': True,
                'message': 'Extraction intégrée avec succès',
                'data': resultat
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': f"Erreur d'intégration: {resultat['error']}"
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur serveur: {str(e)}'
        }), 500

@module_8.route('/api/extractions/pending', methods=['GET'])
def lister_extractions_a_valider():
    """Lister les extractions qui nécessitent une validation"""
    extractions = ExtractionDocument.query.filter_by(
        statut='SUCCES'
    ).filter(
        ExtractionDocument.valide_par_user_id.is_(None)
    ).order_by(ExtractionDocument.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'data': [extraction.to_dict() for extraction in extractions],
        'message': f'{len(extractions)} extractions à valider'
    })

@module_8.route('/api/extractions/<int:extraction_id>/validate', methods=['POST'])
def valider_extraction(extraction_id):
    """Valider une extraction après vérification utilisateur"""
    data = request.get_json()
    corrections = data.get('corrections', {})
    commentaire = data.get('commentaire', '')
    
    extraction = ExtractionDocument.query.get_or_404(extraction_id)
    
    # Appliquer les corrections
    if corrections:
        for facture in extraction.factures_extraites:
            if str(facture.id) in corrections.get('factures', {}):
                facture_corrections = corrections['factures'][str(facture.id)]
                for field, value in facture_corrections.items():
                    setattr(facture, field, value)
                facture.corrigee_par_user = True
                facture.save()
    
    # Marquer comme validé
    extraction.statut = 'VALIDE'
    extraction.valide_par_user_id = get_current_user_id()
    extraction.date_validation = datetime.utcnow()
    extraction.commentaire_validation = commentaire
    extraction.save()
    
    return jsonify({
        'success': True,
        'message': 'Extraction validée avec succès'
    })
```

### **Endpoints de Ventilation IA**

```python
@module_8.route('/api/bons/<int:bon_id>/affecter-chantier', methods=['POST'])
def affecter_bon_chantier(bon_id):
    """Affecter un bon de livraison à un chantier"""
    data = request.get_json()
    chantier_id = data.get('chantier_id')
    
    bon = BonLivraisonExtrait.query.get_or_404(bon_id)
    
    # Vérifier si c'était la suggestion IA
    etait_suggestion = (bon.chantier_suggere_id == chantier_id)
    
    # Affecter
    bon.chantier_affecte_id = chantier_id
    bon.affecte_par_user_id = get_current_user_id()
    bon.date_affectation = datetime.utcnow()
    bon.save()
    
    # Apprentissage IA
    ai_service.enregistrer_feedback(bon_id, chantier_id, etait_suggestion)
    
    return jsonify({
        'success': True,
        'message': 'Bon affecté avec succès'
    })

@module_8.route('/api/n8n/chantiers-actifs', methods=['GET'])
def chantiers_actifs_pour_n8n():
    """API pour n8n : liste des chantiers actifs avec mots-clés"""
    chantiers = Chantier.query.filter_by(statut='ACTIF').all()
    
    return jsonify({
        'success': True,
        'data': [
            {
                'id': c.id,
                'nom': c.nom,
                'client': c.client_nom,
                'mots_cles': c.mots_cles.split(',') if c.mots_cles else []
            }
            for c in chantiers
        ]
    })
```

---

## 📊 Interface Utilisateur

### **Page de Validation des Extractions**

```jsx
// frontend/src/pages/Module8_1_ValidationExtractions.jsx
const ValidationExtractions = () => {
    const [extractions, setExtractions] = useState([]);
    const [selectedExtraction, setSelectedExtraction] = useState(null);
    
    useEffect(() => {
        loadExtractionsAValider();
    }, []);
    
    const loadExtractionsAValider = async () => {
        const response = await fetch('/api/extractions/pending');
        const data = await response.json();
        setExtractions(data.data);
    };
    
    return (
        <PageLayout title="Module 8.1 - Validation Extractions">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                
                {/* Liste des extractions */}
                <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-lg font-semibold mb-4">
                        Extractions à valider ({extractions.length})
                    </h3>
                    
                    {extractions.map(extraction => (
                        <ExtractionCard 
                            key={extraction.id}
                            extraction={extraction}
                            onSelect={setSelectedExtraction}
                        />
                    ))}
                </div>
                
                {/* Détail et validation */}
                {selectedExtraction && (
                    <div className="bg-white rounded-lg shadow p-6">
                        <ValidationInterface 
                            extraction={selectedExtraction}
                            onValidated={loadExtractionsAValider}
                        />
                    </div>
                )}
            </div>
        </PageLayout>
    );
};
```

### **Interface de Ventilation IA**

```jsx
// Composant pour afficher les suggestions IA
const VentilationIA = ({ bon, onVentilationChange }) => {
    const [chantiers, setChantiers] = useState([]);
    
    return (
        <div className="border rounded-lg p-4 mb-4">
            <div className="flex justify-between items-start mb-3">
                <div>
                    <h4 className="font-medium">Bon {bon.numero_bon}</h4>
                    <p className="text-sm text-gray-600">{bon.reference_client}</p>
                    <p className="font-semibold">{bon.montant_ht}€ HT</p>
                </div>
                
                {/* Suggestion IA principale */}
                {bon.chantier_suggere && (
                    <div className="bg-blue-50 rounded-lg p-3">
                        <div className="flex items-center mb-2">
                            <span className="text-blue-600 font-medium">🤖 Suggestion IA</span>
                            <ConfidenceScore score={bon.confidence_suggestion} />
                        </div>
                        <p className="text-sm font-medium">{bon.chantier_suggere.nom}</p>
                        <p className="text-xs text-gray-600">{bon.raison_suggestion}</p>
                        
                        <div className="mt-2 flex gap-2">
                            <button 
                                className="btn-primary-sm"
                                onClick={() => accepterSuggestion(bon.id)}
                            >
                                ✅ Accepter
                            </button>
                            <button 
                                className="btn-secondary-sm" 
                                onClick={() => ouvrirChoixManuel(bon.id)}
                            >
                                ✏️ Choisir autre
                            </button>
                        </div>
                    </div>
                )}
            </div>
            
            {/* Alternatives */}
            {bon.suggestions_alternatives?.length > 0 && (
                <div className="mt-3">
                    <p className="text-sm font-medium mb-2">Autres suggestions :</p>
                    {bon.suggestions_alternatives.map((alt, idx) => (
                        <button
                            key={idx}
                            className="block w-full text-left p-2 hover:bg-gray-50 rounded"
                            onClick={() => choisirAlternative(bon.id, alt.chantier_id)}
                        >
                            <span className="font-medium">{alt.nom}</span>
                            <span className="text-sm text-gray-500 ml-2">
                                ({Math.round(alt.confidence * 100)}%)
                            </span>
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
};
```

---

## 📈 Métriques et KPIs

### **Tableaux de Bord Module 8.1**

```python
# backend/app/services/metrics_extraction_service.py
class MetricsExtractionService:
    """Service pour calculer les métriques d'extraction et IA"""
    
    def get_kpis_extraction(self, periode_jours=30):
        """KPIs d'extraction sur une période"""
        depuis = datetime.utcnow() - timedelta(days=periode_jours)
        
        extractions = ExtractionDocument.query.filter(
            ExtractionDocument.created_at >= depuis
        ).all()
        
        return {
            'total_extractions': len(extractions),
            'taux_succes': len([e for e in extractions if e.statut == 'SUCCES']) / len(extractions) * 100,
            'temps_moyen_traitement': np.mean([e.temps_traitement for e in extractions if e.temps_traitement]),
            'documents_per_day': len(extractions) / periode_jours,
            'fournisseurs_traites': len(set(f.fournisseur for e in extractions for f in e.factures_extraites))
        }
    
    def get_kpis_ia(self, periode_jours=30):
        """KPIs d'intelligence artificielle"""
        depuis = datetime.utcnow() - timedelta(days=periode_jours)
        
        bons = BonLivraisonExtrait.query.filter(
            BonLivraisonExtrait.created_at >= depuis,
            BonLivraisonExtrait.chantier_affecte_id.isnot(None)
        ).all()
        
        suggestions_acceptees = len([b for b in bons if b.suggestion_acceptee])
        
        return {
            'precision_ia': suggestions_acceptees / len(bons) * 100 if bons else 0,
            'bons_ventiles_auto': len([b for b in bons if b.confidence_suggestion >= 0.9]),
            'temps_validation_moyen': self._calculer_temps_validation_moyen(bons),
            'apprentissage_points': len([b for b in bons if not b.suggestion_acceptee])
        }
```

---

## 🚀 Prochaines Étapes

### **Développement Prioritaire**
1. **Modèles SQLAlchemy** : Créer les 3 tables principales
2. **Service d'intégration** : Traitement des données n8n
3. **Service IA de base** : Matching simple par mots-clés
4. **Interface de validation** : Page de validation utilisateur

### **Optimisations**
1. **IA avancée** : Algorithmes de fuzzy matching et apprentissage
2. **Performance** : Index BDD et cache Redis
3. **Interface** : UX avancée avec drag&drop
4. **Monitoring** : Métriques temps réel et alertes

---

**✅ Module 8.1 - Extraction intelligente opérationnelle avec ventilation IA !** 