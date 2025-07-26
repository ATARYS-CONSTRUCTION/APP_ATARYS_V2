# 🧠 Algorithmes de Matching IA - Ventilation Intelligente

> **Spécifications techniques des algorithmes d'intelligence artificielle**  
> **Matching automatique bons de livraison → chantiers ATARYS**  
> Dernière mise à jour : 20/01/2025

---

## 📋 Vue d'ensemble

**Objectif :** Développer des algorithmes d'IA capables d'affecter automatiquement les bons de livraison aux bons chantiers avec un taux de précision >85%.

**Approche :** Combinaison de plusieurs techniques de matching avec scoring pondéré et apprentissage automatique basé sur les corrections utilisateur.

**Performance cible :**
- **Précision >85%** : Suggestions acceptées par l'utilisateur
- **Temps <200ms** : Réponse pour l'analyse d'un bon
- **Apprentissage continu** : Amélioration automatique via feedback

---

## 🔬 Architecture Algorithmes

### **Pipeline de Matching Complet**

```
Bon de livraison → [1] Préprocessing → [2] Multi-Matching → [3] Scoring → [4] Ranking → Suggestions
                                          ↓
                    [5] Apprentissage ← [Feedback utilisateur]
```

### **Composants Principaux**

#### **1. Préprocesseur de Données**
```python
class BonLivraisonPreprocessor:
    """Nettoyage et normalisation des données d'entrée"""
    
    def preprocess_bon(self, bon_data):
        """Normaliser les données d'un bon de livraison"""
        
        # Nettoyage référence client
        reference_clean = self._clean_reference(bon_data['reference_client'])
        
        # Extraction des mots-clés
        keywords = self._extract_keywords(reference_clean)
        
        # Normalisation montant
        montant_normalized = self._normalize_amount(bon_data['montant_ht'])
        
        # Classification du type de bon
        type_bon = self._classify_bon_type(bon_data['description'])
        
        return {
            'reference_original': bon_data['reference_client'],
            'reference_clean': reference_clean,
            'keywords': keywords,
            'montant_ht': montant_normalized,
            'type_bon': type_bon,
            'fournisseur': bon_data.get('fournisseur'),
            'description_clean': self._clean_description(bon_data.get('description', ''))
        }
    
    def _clean_reference(self, reference):
        """Nettoyer une référence client"""
        if not reference:
            return ""
        
        # Supprimer caractères spéciaux
        clean = re.sub(r'[^\w\s/.-]', '', reference.upper())
        
        # Normaliser les espaces
        clean = re.sub(r'\s+', ' ', clean).strip()
        
        return clean
    
    def _extract_keywords(self, reference):
        """Extraire les mots-clés pertinents d'une référence"""
        if not reference:
            return []
        
        # Patterns courants dans les références ATARYS
        patterns = [
            r'(\d{3}[A-Z]+)',           # Ex: 190DEBOIS
            r'([A-Z]{2,}/\d+[A-Z]*)',   # Ex: MO/190DEBOIS
            r'([A-Z]{4,})',             # Noms clients (min 4 lettres)
            r'(\d{4,})'                 # Numéros de référence
        ]
        
        keywords = []
        for pattern in patterns:
            matches = re.findall(pattern, reference)
            keywords.extend(matches)
        
        # Ajouter les mots significatifs
        words = reference.split()
        keywords.extend([w for w in words if len(w) > 3])
        
        return list(set(keywords))  # Dédupliquer
```

#### **2. Matcheurs Spécialisés**

```python
class ExactMatcher:
    """Matching exact par correspondance directe"""
    
    def match(self, bon_preprocessed, chantiers_actifs):
        """Recherche de correspondances exactes"""
        matches = []
        
        for chantier in chantiers_actifs:
            score = self._calculate_exact_score(bon_preprocessed, chantier)
            if score > 0:
                matches.append({
                    'chantier_id': chantier.id,
                    'chantier_nom': chantier.nom,
                    'score': score,
                    'type': 'exact',
                    'raison': self._generate_reason(bon_preprocessed, chantier)
                })
        
        return matches
    
    def _calculate_exact_score(self, bon, chantier):
        """Calculer le score de correspondance exacte"""
        score = 0.0
        
        # Mots-clés du chantier
        chantier_keywords = chantier.mots_cles.split(',') if chantier.mots_cles else []
        
        for keyword in bon['keywords']:
            if keyword in chantier_keywords:
                if len(keyword) >= 6:  # Mots longs = plus fiables
                    score += 1.0
                elif len(keyword) >= 4:
                    score += 0.8
                else:
                    score += 0.5
        
        # Correspondance nom client
        if chantier.client_nom and chantier.client_nom.upper() in bon['reference_clean']:
            score += 0.9
        
        # Normaliser sur 1.0
        return min(score, 1.0)

class FuzzyMatcher:
    """Matching flou par similarité textuelle"""
    
    def __init__(self):
        from difflib import SequenceMatcher
        self.sequence_matcher = SequenceMatcher
    
    def match(self, bon_preprocessed, chantiers_actifs):
        """Recherche de correspondances approximatives"""
        matches = []
        
        for chantier in chantiers_actifs:
            # Similarité avec nom du chantier
            sim_nom = self._text_similarity(bon_preprocessed['reference_clean'], chantier.nom)
            
            # Similarité avec nom client
            sim_client = 0
            if chantier.client_nom:
                sim_client = self._text_similarity(bon_preprocessed['reference_clean'], chantier.client_nom)
            
            # Score global
            score = max(sim_nom, sim_client)
            
            if score >= 0.7:  # Seuil de similarité
                matches.append({
                    'chantier_id': chantier.id,
                    'chantier_nom': chantier.nom,
                    'score': score,
                    'type': 'fuzzy',
                    'raison': f"Similarité {int(score*100)}% avec {chantier.nom}"
                })
        
        return matches
    
    def _text_similarity(self, text1, text2):
        """Calculer la similarité entre deux textes"""
        if not text1 or not text2:
            return 0.0
        
        return self.sequence_matcher(None, text1.upper(), text2.upper()).ratio()

class HistoricalMatcher:
    """Matching basé sur l'historique des livraisons"""
    
    def match(self, bon_preprocessed, chantiers_actifs):
        """Recherche basée sur l'historique"""
        fournisseur = bon_preprocessed.get('fournisseur')
        montant = bon_preprocessed.get('montant_ht', 0)
        
        # Analyser les livraisons passées de ce fournisseur
        historical_data = self._get_historical_deliveries(fournisseur, days=90)
        
        matches = []
        for chantier in chantiers_actifs:
            score = self._calculate_historical_score(chantier, historical_data, montant)
            
            if score > 0.3:
                matches.append({
                    'chantier_id': chantier.id,
                    'chantier_nom': chantier.nom,
                    'score': score,
                    'type': 'historical',
                    'raison': f"Livraisons {fournisseur} fréquentes sur ce chantier"
                })
        
        return matches
    
    def _get_historical_deliveries(self, fournisseur, days=90):
        """Récupérer l'historique des livraisons"""
        depuis = datetime.utcnow() - timedelta(days=days)
        
        return db.session.query(BonLivraisonExtrait)\
            .join(FactureExtraite)\
            .filter(FactureExtraite.fournisseur == fournisseur)\
            .filter(BonLivraisonExtrait.created_at >= depuis)\
            .filter(BonLivraisonExtrait.chantier_affecte_id.isnot(None))\
            .all()

class ContextualMatcher:
    """Matching contextuel (montant, timing, type matériaux)"""
    
    def match(self, bon_preprocessed, chantiers_actifs):
        """Analyse contextuelle pour le matching"""
        montant = bon_preprocessed.get('montant_ht', 0)
        type_bon = bon_preprocessed.get('type_bon', 'unknown')
        
        matches = []
        for chantier in chantiers_actifs:
            score = self._calculate_contextual_score(chantier, montant, type_bon)
            
            if score > 0.2:
                matches.append({
                    'chantier_id': chantier.id,
                    'chantier_nom': chantier.nom,
                    'score': score,
                    'type': 'contextual',
                    'raison': self._generate_contextual_reason(chantier, montant, type_bon)
                })
        
        return matches
    
    def _calculate_contextual_score(self, chantier, montant, type_bon):
        """Score basé sur le contexte"""
        score = 0.0
        
        # Phase du chantier vs type matériaux
        if chantier.phase == 'gros_oeuvre' and type_bon in ['materiaux', 'structure']:
            score += 0.3
        elif chantier.phase == 'finition' and type_bon in ['peinture', 'carrelage', 'menuiserie']:
            score += 0.3
        
        # Cohérence du montant
        if self._is_amount_coherent(chantier, montant):
            score += 0.2
        
        # Timing (chantiers récemment actifs)
        if self._is_recently_active(chantier):
            score += 0.2
        
        return min(score, 1.0)
```

---

## ⚖️ Système de Scoring

### **Pondération des Sources**

```python
class MatchingScorer:
    """Système de scoring unifié pour tous les matcheurs"""
    
    def __init__(self):
        # Poids des différents types de matching
        self.weights = {
            'exact': 1.0,        # Correspondance exacte = priorité max
            'fuzzy': 0.8,        # Similarité textuelle
            'historical': 0.6,   # Historique
            'contextual': 0.4    # Contexte
        }
        
        # Seuils de confiance
        self.confidence_thresholds = {
            'auto_accept': 0.95,   # Acceptation automatique
            'high_confidence': 0.80,
            'medium_confidence': 0.60,
            'low_confidence': 0.40
        }
    
    def calculate_unified_score(self, all_matches):
        """Calculer un score unifié à partir de tous les matcheurs"""
        
        # Grouper par chantier
        chantier_scores = {}
        
        for match in all_matches:
            chantier_id = match['chantier_id']
            match_type = match['type']
            base_score = match['score']
            
            # Appliquer la pondération
            weighted_score = base_score * self.weights.get(match_type, 0.5)
            
            if chantier_id not in chantier_scores:
                chantier_scores[chantier_id] = {
                    'chantier_id': chantier_id,
                    'chantier_nom': match['chantier_nom'],
                    'scores': {},
                    'raisons': []
                }
            
            chantier_scores[chantier_id]['scores'][match_type] = weighted_score
            chantier_scores[chantier_id]['raisons'].append(match['raison'])
        
        # Calculer les scores finaux
        final_matches = []
        for chantier_id, data in chantier_scores.items():
            # Score composite (moyenne pondérée des scores non nuls)
            total_weight = sum(self.weights[t] for t in data['scores'].keys())
            if total_weight > 0:
                final_score = sum(data['scores'].values()) / total_weight
                
                # Bonus si plusieurs types de matching concordent
                if len(data['scores']) > 1:
                    final_score *= 1.1  # Bonus 10%
                
                # Bonus si correspondance exacte
                if 'exact' in data['scores'] and data['scores']['exact'] > 0.8:
                    final_score *= 1.2  # Bonus 20%
                
                final_matches.append({
                    'chantier_id': chantier_id,
                    'chantier_nom': data['chantier_nom'],
                    'score': min(final_score, 1.0),
                    'confidence_level': self._get_confidence_level(final_score),
                    'raisons': data['raisons'],
                    'detail_scores': data['scores']
                })
        
        return sorted(final_matches, key=lambda x: x['score'], reverse=True)
    
    def _get_confidence_level(self, score):
        """Déterminer le niveau de confiance"""
        if score >= self.confidence_thresholds['auto_accept']:
            return 'VERY_HIGH'
        elif score >= self.confidence_thresholds['high_confidence']:
            return 'HIGH'
        elif score >= self.confidence_thresholds['medium_confidence']:
            return 'MEDIUM'
        elif score >= self.confidence_thresholds['low_confidence']:
            return 'LOW'
        else:
            return 'VERY_LOW'
```

---

## 🎓 Apprentissage Automatique

### **Collecte du Feedback**

```python
class FeedbackCollector:
    """Collecte et analyse du feedback utilisateur pour l'apprentissage"""
    
    def record_feedback(self, bon_id, suggested_chantier_id, actual_chantier_id, user_action):
        """Enregistrer le feedback utilisateur"""
        
        feedback = MatchingFeedback(
            bon_id=bon_id,
            suggested_chantier_id=suggested_chantier_id,
            actual_chantier_id=actual_chantier_id,
            user_action=user_action,  # ACCEPTED, MODIFIED, REJECTED
            timestamp=datetime.utcnow()
        )
        
        # Analyser le feedback pour l'apprentissage
        self._analyze_feedback(feedback)
        
        feedback.save()
        return feedback
    
    def _analyze_feedback(self, feedback):
        """Analyser le feedback pour identifier des patterns"""
        
        # Si l'utilisateur a rejeté la suggestion
        if feedback.user_action == 'REJECTED':
            self._learn_from_rejection(feedback)
        
        # Si l'utilisateur a modifié la suggestion
        elif feedback.user_action == 'MODIFIED':
            self._learn_from_modification(feedback)
        
        # Si l'utilisateur a accepté
        elif feedback.user_action == 'ACCEPTED':
            self._reinforce_patterns(feedback)
    
    def _learn_from_rejection(self, feedback):
        """Apprendre des rejets utilisateur"""
        
        # Analyser pourquoi la suggestion était mauvaise
        bon = BonLivraisonExtrait.query.get(feedback.bon_id)
        suggested_chantier = Chantier.query.get(feedback.suggested_chantier_id)
        
        # Identifier les patterns à éviter
        negative_pattern = {
            'reference_keywords': bon.reference_client.split(),
            'chantier_keywords': suggested_chantier.mots_cles.split(','),
            'montant_range': self._get_amount_range(bon.montant_ht),
            'fournisseur': bon.facture.fournisseur
        }
        
        # Stocker le pattern négatif
        self._store_negative_pattern(negative_pattern)
    
    def _learn_from_modification(self, feedback):
        """Apprendre des corrections utilisateur"""
        
        bon = BonLivraisonExtrait.query.get(feedback.bon_id)
        correct_chantier = Chantier.query.get(feedback.actual_chantier_id)
        
        # Créer un pattern positif basé sur la correction
        positive_pattern = {
            'reference_keywords': bon.reference_client.split(),
            'chantier_keywords': correct_chantier.mots_cles.split(','),
            'chantier_id': correct_chantier.id,
            'success_weight': 1.0
        }
        
        # Renforcer ce pattern
        self._reinforce_pattern(positive_pattern)

class PatternLearner:
    """Apprentissage automatique des patterns de matching"""
    
    def __init__(self):
        self.positive_patterns = []  # Patterns qui marchent
        self.negative_patterns = []  # Patterns à éviter
        self.pattern_weights = {}    # Poids des patterns
    
    def learn_new_pattern(self, bon_data, chantier_data, success=True):
        """Apprendre un nouveau pattern"""
        
        pattern = self._extract_pattern(bon_data, chantier_data)
        pattern_key = self._generate_pattern_key(pattern)
        
        if success:
            # Renforcer les patterns positifs
            if pattern_key in self.pattern_weights:
                self.pattern_weights[pattern_key] += 0.1
            else:
                self.pattern_weights[pattern_key] = 1.0
                self.positive_patterns.append(pattern)
        else:
            # Diminuer le poids des patterns négatifs
            if pattern_key in self.pattern_weights:
                self.pattern_weights[pattern_key] = max(0.1, self.pattern_weights[pattern_key] - 0.2)
            else:
                self.pattern_weights[pattern_key] = 0.1
                self.negative_patterns.append(pattern)
    
    def get_pattern_score(self, bon_data, chantier_data):
        """Obtenir le score d'un pattern basé sur l'apprentissage"""
        
        pattern = self._extract_pattern(bon_data, chantier_data)
        pattern_key = self._generate_pattern_key(pattern)
        
        return self.pattern_weights.get(pattern_key, 0.5)  # Score neutre par défaut
    
    def _extract_pattern(self, bon_data, chantier_data):
        """Extraire un pattern à partir des données"""
        return {
            'fournisseur': bon_data.get('fournisseur', '').upper(),
            'keywords_intersection': self._get_keywords_intersection(bon_data, chantier_data),
            'amount_category': self._categorize_amount(bon_data.get('montant_ht', 0)),
            'chantier_type': chantier_data.get('type_chantier', 'unknown')
        }
```

### **Optimisation Continue**

```python
class MatchingOptimizer:
    """Optimisation continue des algorithmes de matching"""
    
    def __init__(self):
        self.performance_metrics = {}
        self.optimization_history = []
    
    def analyze_performance(self, period_days=30):
        """Analyser les performances sur une période"""
        
        depuis = datetime.utcnow() - timedelta(days=period_days)
        
        # Récupérer tous les matchings de la période
        feedbacks = MatchingFeedback.query.filter(
            MatchingFeedback.timestamp >= depuis
        ).all()
        
        metrics = {
            'total_suggestions': len(feedbacks),
            'accepted': len([f for f in feedbacks if f.user_action == 'ACCEPTED']),
            'modified': len([f for f in feedbacks if f.user_action == 'MODIFIED']),
            'rejected': len([f for f in feedbacks if f.user_action == 'REJECTED']),
            'precision': 0,
            'learning_rate': 0
        }
        
        if metrics['total_suggestions'] > 0:
            metrics['precision'] = metrics['accepted'] / metrics['total_suggestions']
            metrics['learning_rate'] = (metrics['modified'] + metrics['rejected']) / metrics['total_suggestions']
        
        # Analyser par fournisseur
        fournisseur_metrics = self._analyze_by_supplier(feedbacks)
        
        # Recommandations d'optimisation
        recommendations = self._generate_recommendations(metrics, fournisseur_metrics)
        
        return {
            'global_metrics': metrics,
            'supplier_metrics': fournisseur_metrics,
            'recommendations': recommendations
        }
    
    def auto_tune_parameters(self):
        """Ajustement automatique des paramètres"""
        
        performance = self.analyze_performance()
        
        # Si la précision est faible, ajuster les seuils
        if performance['global_metrics']['precision'] < 0.8:
            self._increase_confidence_thresholds()
        
        # Si trop de rejets, revoir les poids des algorithmes
        rejection_rate = performance['global_metrics']['rejected'] / performance['global_metrics']['total_suggestions']
        if rejection_rate > 0.3:
            self._adjust_algorithm_weights()
        
        # Optimiser les patterns les moins performants
        self._optimize_weak_patterns()
    
    def _generate_recommendations(self, metrics, supplier_metrics):
        """Générer des recommandations d'amélioration"""
        recommendations = []
        
        # Recommandations globales
        if metrics['precision'] < 0.8:
            recommendations.append({
                'type': 'PRECISION_LOW',
                'message': 'Précision globale faible. Réviser les mots-clés des chantiers actifs.',
                'priority': 'HIGH'
            })
        
        # Recommandations par fournisseur
        for fournisseur, fmetrics in supplier_metrics.items():
            if fmetrics['precision'] < 0.7:
                recommendations.append({
                    'type': 'SUPPLIER_PRECISION_LOW',
                    'message': f'Précision faible pour {fournisseur}. Analyser les patterns spécifiques.',
                    'fournisseur': fournisseur,
                    'priority': 'MEDIUM'
                })
        
        return recommendations
```

---

## 📊 Métriques et Évaluation

### **KPIs Algorithmes**

```python
class AlgorithmMetrics:
    """Calcul et suivi des métriques algorithmes"""
    
    def calculate_precision_recall(self, period_days=30):
        """Calculer précision et recall"""
        
        depuis = datetime.utcnow() - timedelta(days=period_days)
        
        # True Positives: Suggestions acceptées
        tp = MatchingFeedback.query.filter(
            MatchingFeedback.timestamp >= depuis,
            MatchingFeedback.user_action == 'ACCEPTED'
        ).count()
        
        # False Positives: Suggestions rejetées  
        fp = MatchingFeedback.query.filter(
            MatchingFeedback.timestamp >= depuis,
            MatchingFeedback.user_action == 'REJECTED'
        ).count()
        
        # False Negatives: Cas où l'IA n'a pas trouvé mais utilisateur a trouvé
        fn = BonLivraisonExtrait.query.filter(
            BonLivraisonExtrait.created_at >= depuis,
            BonLivraisonExtrait.chantier_suggere_id.is_(None),
            BonLivraisonExtrait.chantier_affecte_id.isnot(None)
        ).count()
        
        # Calculs
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'true_positives': tp,
            'false_positives': fp,
            'false_negatives': fn
        }
    
    def algorithm_performance_by_type(self):
        """Performance par type d'algorithme"""
        
        performance = {}
        
        for algo_type in ['exact', 'fuzzy', 'historical', 'contextual']:
            # Compter les succès par type d'algorithme
            # (nécessite de tracker le type d'algo dans le feedback)
            
            performance[algo_type] = {
                'precision': 0.85,  # À calculer réellement
                'usage_frequency': 0.3,
                'avg_confidence': 0.75
            }
        
        return performance
```

### **Dashboard de Performance**

```python
def generate_performance_dashboard():
    """Générer un dashboard de performance IA"""
    
    metrics = AlgorithmMetrics()
    
    # Métriques globales
    global_perf = metrics.calculate_precision_recall(30)
    
    # Performance par algorithme
    algo_perf = metrics.algorithm_performance_by_type()
    
    # Tendance dans le temps
    trend_data = []
    for i in range(12):  # 12 dernières semaines
        week_start = datetime.utcnow() - timedelta(weeks=i+1)
        week_end = datetime.utcnow() - timedelta(weeks=i)
        
        week_metrics = metrics.calculate_precision_recall_period(week_start, week_end)
        trend_data.append({
            'week': week_start.strftime('%Y-W%W'),
            'precision': week_metrics['precision'],
            'volume': week_metrics['true_positives'] + week_metrics['false_positives']
        })
    
    return {
        'global_performance': global_perf,
        'algorithm_performance': algo_perf,
        'trend_data': reversed(trend_data),
        'recommendations': generate_improvement_recommendations(global_perf, algo_perf)
    }
```

---

## 🔧 Configuration et Tuning

### **Paramètres Configurables**

```python
# config/matching_config.py
class MatchingConfig:
    """Configuration des algorithmes de matching"""
    
    # Seuils de confiance
    CONFIDENCE_THRESHOLDS = {
        'auto_accept': float(os.getenv('AI_AUTO_ACCEPT_THRESHOLD', '0.95')),
        'high_confidence': float(os.getenv('AI_HIGH_CONFIDENCE_THRESHOLD', '0.80')),
        'medium_confidence': float(os.getenv('AI_MEDIUM_CONFIDENCE_THRESHOLD', '0.60')),
        'low_confidence': float(os.getenv('AI_LOW_CONFIDENCE_THRESHOLD', '0.40'))
    }
    
    # Poids des algorithmes
    ALGORITHM_WEIGHTS = {
        'exact': float(os.getenv('AI_EXACT_WEIGHT', '1.0')),
        'fuzzy': float(os.getenv('AI_FUZZY_WEIGHT', '0.8')),
        'historical': float(os.getenv('AI_HISTORICAL_WEIGHT', '0.6')),
        'contextual': float(os.getenv('AI_CONTEXTUAL_WEIGHT', '0.4'))
    }
    
    # Paramètres d'apprentissage
    LEARNING_PARAMS = {
        'pattern_reinforcement_rate': float(os.getenv('AI_LEARNING_RATE', '0.1')),
        'pattern_decay_rate': float(os.getenv('AI_DECAY_RATE', '0.05')),
        'min_pattern_confidence': float(os.getenv('AI_MIN_PATTERN_CONF', '0.3')),
        'max_patterns_per_type': int(os.getenv('AI_MAX_PATTERNS', '1000'))
    }
    
    # Performance
    PERFORMANCE_PARAMS = {
        'max_suggestions': int(os.getenv('AI_MAX_SUGGESTIONS', '3')),
        'response_timeout_ms': int(os.getenv('AI_TIMEOUT_MS', '200')),
        'batch_processing_size': int(os.getenv('AI_BATCH_SIZE', '10'))
    }
    
    @classmethod
    def update_from_performance(cls, performance_metrics):
        """Mise à jour automatique basée sur les performances"""
        
        # Si précision trop faible, augmenter les seuils
        if performance_metrics['precision'] < 0.75:
            cls.CONFIDENCE_THRESHOLDS['auto_accept'] = min(0.98, 
                cls.CONFIDENCE_THRESHOLDS['auto_accept'] + 0.02)
        
        # Si trop peu de suggestions, diminuer les seuils
        elif performance_metrics['suggestions_per_bon'] < 1.5:
            cls.CONFIDENCE_THRESHOLDS['low_confidence'] = max(0.2,
                cls.CONFIDENCE_THRESHOLDS['low_confidence'] - 0.05)
```

---

## 🚀 Évolutions Futures

### **Roadmap IA**

#### **Phase 1 : IA de Base (4 semaines)**
- ✅ Matching exact par mots-clés
- ✅ Matching flou par similarité
- ✅ Système de scoring unifié
- ✅ Feedback utilisateur basique

#### **Phase 2 : IA Avancée (6 semaines)**
- 🔄 Matching historique intelligent
- 🔄 Analyse contextuelle poussée
- 🔄 Apprentissage automatique des patterns
- 🔄 Optimisation continue des paramètres

#### **Phase 3 : IA Experte (8 semaines)**
- 🔄 Machine Learning avancé (Random Forest, Neural Networks)
- 🔄 Détection automatique de nouveaux patterns
- 🔄 Prédiction proactive des besoins chantiers
- 🔄 IA explicable (pourquoi cette suggestion ?)

### **Technologies Avancées**

```python
# Évolution vers des modèles ML plus sophistiqués
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

class MLMatcher:
    """Matcher basé sur Machine Learning"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.classifier = RandomForestClassifier(n_estimators=100)
        self.is_trained = False
    
    def train(self, historical_data):
        """Entraîner le modèle ML"""
        
        # Préparer les features
        features = []
        labels = []
        
        for bon, chantier_id in historical_data:
            feature_vector = self._extract_ml_features(bon)
            features.append(feature_vector)
            labels.append(chantier_id)
        
        # Entraînement
        X = self.vectorizer.fit_transform(features)
        self.classifier.fit(X, labels)
        self.is_trained = True
    
    def predict(self, bon_data):
        """Prédire le chantier le plus probable"""
        if not self.is_trained:
            return None
        
        feature_vector = self._extract_ml_features(bon_data)
        X = self.vectorizer.transform([feature_vector])
        
        probabilities = self.classifier.predict_proba(X)[0]
        classes = self.classifier.classes_
        
        # Retourner les top 3 prédictions
        top_indices = probabilities.argsort()[-3:][::-1]
        
        predictions = []
        for idx in top_indices:
            predictions.append({
                'chantier_id': classes[idx],
                'probability': probabilities[idx],
                'type': 'ml_prediction'
            })
        
        return predictions
```

---

**✅ Algorithmes de Matching IA - Intelligence artificielle opérationnelle pour la ventilation automatique !** 