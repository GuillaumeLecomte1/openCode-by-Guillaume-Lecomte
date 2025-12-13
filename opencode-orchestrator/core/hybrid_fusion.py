"""
Logique de fusion hybride pour l'Orchestrateur OpenCode
Combinaison des classificateurs par mots-clés et LLM avec gestion des conflits
"""

import time
import logging
from typing import Dict, List, Optional, Tuple, Any, NamedTuple
from dataclasses import dataclass, field
from enum import Enum
import statistics
import json

from classifiers.keyword_classifier import KeywordClassifier, ClassificationResult
from classifiers.llm_classifier import LLMClassifier, LLMClassificationResult, ConfidenceLevel

@dataclass
class FusionWeights:
    """Poids pour la fusion des classificateurs"""
    keyword_weight: float = 0.4
    llm_weight: float = 0.6
    domain_weight: float = 0.3
    type_weight: float = 0.25
    complexity_weight: float = 0.25
    phase_weight: float = 0.2

@dataclass
class ConflictAnalysis:
    """Analyse des conflits entre classificateurs"""
    has_conflict: bool
    conflict_type: str
    severity: str
    conflicting_dimensions: List[str]
    recommendation: str
    confidence_impact: float

@dataclass
class HybridClassificationResult:
    """Résultat final de classification hybride"""
    # Classifications fusionnées
    final_domain: str
    final_domain_confidence: float
    final_type: str
    final_type_confidence: float
    final_complexity: str
    final_complexity_confidence: float
    final_phase: str
    final_phase_confidence: float
    
    # Résultats individuels
    keyword_result: Optional[ClassificationResult] = None
    llm_result: Optional[LLMClassificationResult] = None
    
    # Métadonnées de fusion
    fusion_confidence: float = 0.0
    conflict_analysis: Optional[ConflictAnalysis] = None
    processing_time: float = 0.0
    fusion_method: str = ""
    fallback_used: bool = False
    
    # Scores détaillés
    domain_scores: Dict[str, float] = field(default_factory=dict)
    type_scores: Dict[str, float] = field(default_factory=dict)
    complexity_scores: Dict[str, float] = field(default_factory=dict)
    phase_scores: Dict[str, float] = field(default_factory=dict)
    
    # Suggestions et recommandations
    recommendations: List[str] = field(default_factory=list)
    quality_indicators: Dict[str, Any] = field(default_factory=dict)

class FusionStrategy(Enum):
    """Stratégies de fusion disponibles"""
    WEIGHTED_AVERAGE = "weighted_average"
    CONFIDENCE_BASED = "confidence_based"
    ENSEMBLE_VOTING = "ensemble_voting"
    ADAPTIVE_FUSION = "adaptive_fusion"
    CONSENSUS_BASED = "consensus_based"

class HybridFusionEngine:
    """Moteur principal de fusion hybride"""
    
    def __init__(self, fusion_strategy: FusionStrategy = FusionStrategy.ADAPTIVE_FUSION,
                 fusion_weights: Optional[FusionWeights] = None,
                 keyword_classifier: Optional[KeywordClassifier] = None,
                 llm_classifier: Optional[LLMClassifier] = None):
        
        self.fusion_strategy = fusion_strategy
        self.fusion_weights = fusion_weights or FusionWeights()
        self.keyword_classifier = keyword_classifier or KeywordClassifier()
        self.llm_classifier = llm_classifier or LLMClassifier()
        
        self.logger = logging.getLogger(__name__)
        
        # Métriques de performance
        self.fusion_stats = {
            'total_fusions': 0,
            'conflicts_detected': 0,
            'fallbacks_used': 0,
            'avg_processing_time': 0.0,
            'strategy_usage': {strategy.value: 0 for strategy in FusionStrategy}
        }
        
        # Cache pour les résultats
        self._fusion_cache = {}
    
    def classify(self, text: str, context: Dict = None, 
                use_cache: bool = True) -> HybridClassificationResult:
        """
        Classification hybride principale
        
        Args:
            text: Texte à classifier
            context: Contexte additionnel
            use_cache: Utiliser le cache
        
        Returns:
            HybridClassificationResult fusionné et validé
        """
        start_time = time.time()
        
        # Clé de cache
        cache_key = f"{hash(text)}_{hash(str(context))}_{self.fusion_strategy.value}"
        
        if use_cache and cache_key in self._fusion_cache:
            return self._fusion_cache[cache_key]
        
        try:
            # Classification par mots-clés
            keyword_result = self.keyword_classifier.classify(text, context)
            
            # Classification LLM
            llm_result = self.llm_classifier.classify(text, context)
            
            # Fusion des résultats
            fused_result = self._fuse_results(keyword_result, llm_result, text, context)
            
            # Ajout des métadonnées
            fused_result.processing_time = time.time() - start_time
            fused_result.keyword_result = keyword_result
            fused_result.llm_result = llm_result
            
            # Mise à jour des statistiques
            self._update_fusion_stats(fused_result)
            
            # Cache du résultat
            if use_cache:
                self._fusion_cache[cache_key] = fused_result
            
            return fused_result
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la fusion hybride: {e}")
            return self._generate_fallback_result(text, context, time.time() - start_time)
    
    def _fuse_results(self, keyword_result: ClassificationResult, 
                     llm_result: LLMClassificationResult,
                     text: str, context: Dict) -> HybridClassificationResult:
        """Fusionne les résultats des deux classificateurs"""
        
        # Analyse des conflits
        conflict_analysis = self._analyze_conflicts(keyword_result, llm_result)
        
        # Sélection de la stratégie de fusion
        fusion_method = self._select_fusion_strategy(conflict_analysis)
        
        # Fusion selon la stratégie
        if fusion_method == FusionStrategy.WEIGHTED_AVERAGE:
            return self._weighted_average_fusion(keyword_result, llm_result, conflict_analysis)
        elif fusion_method == FusionStrategy.CONFIDENCE_BASED:
            return self._confidence_based_fusion(keyword_result, llm_result, conflict_analysis)
        elif fusion_method == FusionStrategy.ENSEMBLE_VOTING:
            return self._ensemble_voting_fusion(keyword_result, llm_result, conflict_analysis)
        elif fusion_method == FusionStrategy.CONSENSUS_BASED:
            return self._consensus_based_fusion(keyword_result, llm_result, conflict_analysis)
        else:  # ADAPTIVE_FUSION
            return self._adaptive_fusion(keyword_result, llm_result, conflict_analysis, text)
    
    def _weighted_average_fusion(self, keyword_result: ClassificationResult,
                               llm_result: LLMClassificationResult,
                               conflict_analysis: ConflictAnalysis) -> HybridClassificationResult:
        """Fusion par moyenne pondérée"""
        
        # Préparation des scores
        keyword_weights = self.fusion_weights
        llm_weights = self.fusion_weights
        
        # Fusion des domaines
        domain_scores = self._merge_domain_scores(keyword_result.domain, llm_result.domain)
        final_domain, final_domain_conf = self._select_best_option(domain_scores, keyword_weights.keyword_weight, llm_weights.llm_weight)
        
        # Fusion des types
        type_scores = self._merge_type_scores(keyword_result.type, llm_result.type)
        final_type, final_type_conf = self._select_best_option(type_scores, keyword_weights.keyword_weight, llm_weights.llm_weight)
        
        # Fusion des complexités
        complexity_scores = self._merge_complexity_scores(keyword_result.complexity, llm_result.complexity)
        final_complexity, final_complexity_conf = self._select_best_option(complexity_scores, keyword_weights.keyword_weight, llm_weights.llm_weight)
        
        # Fusion des phases
        phase_scores = self._merge_phase_scores(keyword_result.phase, llm_result.phase)
        final_phase, final_phase_conf = self._select_best_option(phase_scores, keyword_weights.keyword_weight, llm_weights.llm_weight)
        
        # Calcul de la confiance de fusion
        fusion_confidence = self._calculate_fusion_confidence(
            final_domain_conf, final_type_conf, final_complexity_conf, final_phase_conf,
            conflict_analysis
        )
        
        return HybridClassificationResult(
            final_domain=final_domain,
            final_domain_confidence=final_domain_conf,
            final_type=final_type,
            final_type_confidence=final_type_conf,
            final_complexity=final_complexity,
            final_complexity_confidence=final_complexity_conf,
            final_phase=final_phase,
            final_phase_confidence=final_phase_conf,
            fusion_confidence=fusion_confidence,
            conflict_analysis=conflict_analysis,
            fusion_method=FusionStrategy.WEIGHTED_AVERAGE.value,
            domain_scores=domain_scores,
            type_scores=type_scores,
            complexity_scores=complexity_scores,
            phase_scores=phase_scores,
            recommendations=self._generate_recommendations(keyword_result, llm_result, conflict_analysis)
        )
    
    def _confidence_based_fusion(self, keyword_result: ClassificationResult,
                               llm_result: LLMClassificationResult,
                               conflict_analysis: ConflictAnalysis) -> HybridClassificationResult:
        """Fusion basée sur la confiance"""
        
        # Pour chaque dimension, sélectionner le classificateur le plus confiant
        keyword_conf = keyword_result.confidence
        llm_conf = llm_result.overall_confidence
        
        use_keyword = keyword_conf > llm_conf
        
        if use_keyword:
            # Priorité aux mots-clés
            final_domain = max(keyword_result.domain.items(), key=lambda x: x[1])[0]
            final_domain_conf = keyword_result.domain.get(final_domain, 0.0)
            final_type = max(keyword_result.type.items(), key=lambda x: x[1])[0]
            final_type_conf = keyword_result.type.get(final_type, 0.0)
            final_complexity = max(keyword_result.complexity.items(), key=lambda x: x[1])[0]
            final_complexity_conf = keyword_result.complexity.get(final_complexity, 0.0)
            final_phase = max(keyword_result.phase.items(), key=lambda x: x[1])[0]
            final_phase_conf = keyword_result.phase.get(final_phase, 0.0)
        else:
            # Priorité au LLM
            final_domain = llm_result.domain
            final_domain_conf = llm_result.domain_confidence
            final_type = llm_result.type
            final_type_conf = llm_result.type_confidence
            final_complexity = llm_result.complexity
            final_complexity_conf = llm_result.complexity_confidence
            final_phase = llm_result.phase
            final_phase_conf = llm_result.phase_confidence
        
        fusion_confidence = max(keyword_conf, llm_conf)
        
        return HybridClassificationResult(
            final_domain=final_domain,
            final_domain_confidence=final_domain_conf,
            final_type=final_type,
            final_type_confidence=final_type_conf,
            final_complexity=final_complexity,
            final_complexity_confidence=final_complexity_conf,
            final_phase=final_phase,
            final_phase_confidence=final_phase_conf,
            fusion_confidence=fusion_confidence,
            conflict_analysis=conflict_analysis,
            fusion_method=FusionStrategy.CONFIDENCE_BASED.value
        )
    
    def _ensemble_voting_fusion(self, keyword_result: ClassificationResult,
                              llm_result: LLMClassificationResult,
                              conflict_analysis: ConflictAnalysis) -> HybridClassificationResult:
        """Fusion par vote d'ensemble"""
        
        # Collecte des votes
        domain_votes = {}
        type_votes = {}
        complexity_votes = {}
        phase_votes = {}
        
        # Votes des mots-clés
        for domain, score in keyword_result.domain.items():
            domain_votes[domain] = domain_votes.get(domain, 0) + score * 0.5
        
        for ptype, score in keyword_result.type.items():
            type_votes[ptype] = type_votes.get(ptype, 0) + score * 0.5
        
        for complexity, score in keyword_result.complexity.items():
            complexity_votes[complexity] = complexity_votes.get(complexity, 0) + score * 0.5
        
        for phase, score in keyword_result.phase.items():
            phase_votes[phase] = phase_votes.get(phase, 0) + score * 0.5
        
        # Vote du LLM
        domain_votes[llm_result.domain] = domain_votes.get(llm_result.domain, 0) + llm_result.domain_confidence * 0.5
        type_votes[llm_result.type] = type_votes.get(llm_result.type, 0) + llm_result.type_confidence * 0.5
        complexity_votes[llm_result.complexity] = complexity_votes.get(llm_result.complexity, 0) + llm_result.complexity_confidence * 0.5
        phase_votes[llm_result.phase] = phase_votes.get(llm_result.phase, 0) + llm_result.phase_confidence * 0.5
        
        # Sélection des gagnants
        final_domain = max(domain_votes.items(), key=lambda x: x[1])[0]
        final_domain_conf = domain_votes[final_domain]
        final_type = max(type_votes.items(), key=lambda x: x[1])[0]
        final_type_conf = type_votes[final_type]
        final_complexity = max(complexity_votes.items(), key=lambda x: x[1])[0]
        final_complexity_conf = complexity_votes[final_complexity]
        final_phase = max(phase_votes.items(), key=lambda x: x[1])[0]
        final_phase_conf = phase_votes[final_phase]
        
        fusion_confidence = statistics.mean([final_domain_conf, final_type_conf, final_complexity_conf, final_phase_conf])
        
        return HybridClassificationResult(
            final_domain=final_domain,
            final_domain_confidence=final_domain_conf,
            final_type=final_type,
            final_type_confidence=final_type_conf,
            final_complexity=final_complexity,
            final_complexity_confidence=final_complexity_conf,
            final_phase=final_phase,
            final_phase_confidence=final_phase_conf,
            fusion_confidence=fusion_confidence,
            conflict_analysis=conflict_analysis,
            fusion_method=FusionStrategy.ENSEMBLE_VOTING.value,
            domain_scores=domain_votes,
            type_scores=type_votes,
            complexity_scores=complexity_votes,
            phase_scores=phase_votes
        )
    
    def _consensus_based_fusion(self, keyword_result: ClassificationResult,
                              llm_result: LLMClassificationResult,
                              conflict_analysis: ConflictAnalysis) -> HybridClassificationResult:
        """Fusion basée sur le consensus"""
        
        # Recherche de consensus entre les classificateurs
        domain_consensus = self._find_consensus(
            keyword_result.domain, llm_result.domain, llm_result.domain_confidence
        )
        type_consensus = self._find_consensus(
            keyword_result.type, llm_result.type, llm_result.type_confidence
        )
        complexity_consensus = self._find_consensus(
            keyword_result.complexity, llm_result.complexity, llm_result.complexity_confidence
        )
        phase_consensus = self._find_consensus(
            keyword_result.phase, llm_result.phase, llm_result.phase_confidence
        )
        
        return HybridClassificationResult(
            final_domain=domain_consensus['value'],
            final_domain_confidence=domain_consensus['confidence'],
            final_type=type_consensus['value'],
            final_type_confidence=type_consensus['confidence'],
            final_complexity=complexity_consensus['value'],
            final_complexity_confidence=complexity_consensus['confidence'],
            final_phase=phase_consensus['value'],
            final_phase_confidence=phase_consensus['confidence'],
            fusion_confidence=domain_consensus['confidence'] * type_consensus['confidence'] * 
                           complexity_consensus['confidence'] * phase_consensus['confidence'],
            conflict_analysis=conflict_analysis,
            fusion_method=FusionStrategy.CONSENSUS_BASED.value
        )
    
    def _adaptive_fusion(self, keyword_result: ClassificationResult,
                        llm_result: LLMClassificationResult,
                        conflict_analysis: ConflictAnalysis,
                        text: str) -> HybridClassificationResult:
        """Fusion adaptative qui choisit la meilleure stratégie selon le contexte"""
        
        # Analyse du contexte pour choisir la stratégie
        text_length = len(text)
        keyword_conf = keyword_result.confidence
        llm_conf = llm_result.overall_confidence
        
        # Stratégie basée sur la longueur du texte et les confiances
        if text_length < 500:  # Texte court
            if llm_conf > keyword_conf + 0.2:
                strategy = FusionStrategy.CONFIDENCE_BASED
            else:
                strategy = FusionStrategy.WEIGHTED_AVERAGE
        elif text_length > 2000:  # Texte long
            if keyword_conf > 0.7 and llm_conf > 0.7:
                strategy = FusionStrategy.CONSENSUS_BASED
            else:
                strategy = FusionStrategy.ENSEMBLE_VOTING
        else:  # Texte moyen
            if conflict_analysis.has_conflict and conflict_analysis.severity == "high":
                strategy = FusionStrategy.CONSENSUS_BASED
            else:
                strategy = FusionStrategy.WEIGHTED_AVERAGE
        
        # Application de la stratégie choisie
        if strategy == FusionStrategy.CONFIDENCE_BASED:
            return self._confidence_based_fusion(keyword_result, llm_result, conflict_analysis)
        elif strategy == FusionStrategy.CONSENSUS_BASED:
            return self._consensus_based_fusion(keyword_result, llm_result, conflict_analysis)
        elif strategy == FusionStrategy.ENSEMBLE_VOTING:
            return self._ensemble_voting_fusion(keyword_result, llm_result, conflict_analysis)
        else:
            return self._weighted_average_fusion(keyword_result, llm_result, conflict_analysis)
    
    def _analyze_conflicts(self, keyword_result: ClassificationResult,
                          llm_result: LLMClassificationResult) -> ConflictAnalysis:
        """Analyse les conflits entre les résultats des classificateurs"""
        
        conflicts = []
        conflicting_dimensions = []
        
        # Comparaison des top domaines
        keyword_top_domain = max(keyword_result.domain.items(), key=lambda x: x[1])[0] if keyword_result.domain else None
        llm_domain = llm_result.domain
        
        if keyword_top_domain and keyword_top_domain != llm_domain:
            conflicts.append(f"Domaine: keyword={keyword_top_domain}, LLM={llm_domain}")
            conflicting_dimensions.append("domain")
        
        # Comparaison des top types
        keyword_top_type = max(keyword_result.type.items(), key=lambda x: x[1])[0] if keyword_result.type else None
        llm_type = llm_result.type
        
        if keyword_top_type and keyword_top_type != llm_type:
            conflicts.append(f"Type: keyword={keyword_top_type}, LLM={llm_type}")
            conflicting_dimensions.append("type")
        
        # Comparaison des complexités
        keyword_top_complexity = max(keyword_result.complexity.items(), key=lambda x: x[1])[0] if keyword_result.complexity else None
        llm_complexity = llm_result.complexity
        
        if keyword_top_complexity and keyword_top_complexity != llm_complexity:
            conflicts.append(f"Complexité: keyword={keyword_top_complexity}, LLM={llm_complexity}")
            conflicting_dimensions.append("complexity")
        
        # Comparaison des phases
        keyword_top_phase = max(keyword_result.phase.items(), key=lambda x: x[1])[0] if keyword_result.phase else None
        llm_phase = llm_result.phase
        
        if keyword_top_phase and keyword_top_phase != llm_phase:
            conflicts.append(f"Phase: keyword={keyword_top_phase}, LLM={llm_phase}")
            conflicting_dimensions.append("phase")
        
        # Détermination de la sévérité
        has_conflict = len(conflicts) > 0
        severity = "high" if len(conflicting_dimensions) >= 2 else "medium" if len(conflicting_dimensions) == 1 else "none"
        
        # Génération de recommandations
        recommendation = self._generate_conflict_recommendation(conflicting_dimensions, severity)
        
        return ConflictAnalysis(
            has_conflict=has_conflict,
            conflict_type="semantic_disagreement" if has_conflict else "none",
            severity=severity,
            conflicting_dimensions=conflicting_dimensions,
            recommendation=recommendation,
            confidence_impact=len(conflicting_dimensions) * 0.1  # Impact sur la confiance
        )
    
    def _generate_conflict_recommendation(self, conflicting_dimensions: List[str], severity: str) -> str:
        """Génère des recommandations basées sur les conflits détectés"""
        if not conflicting_dimensions:
            return "Aucun conflit détecté - Classification cohérente"
        
        base_recommendations = {
            "high": "Conflits multiples détectés. Recommandation: utiliser le classificateur LLM ou une analyse manuelle.",
            "medium": "Conflit modéré détecté. Recommandation: vérifier les sources et considérer le contexte additionnel.",
            "low": "Conflit mineur détecté. Recommandation: fusion par consensus recommandée."
        }
        
        dimension_specific = {
            "domain": "Le domaine semble ambigu. Examiner les technologies utilisées.",
            "type": "Le type de projet nécessite clarification. Vérifier la structure du projet.",
            "complexity": "La complexité nécessite expertise. Considérer l'analyse du code.",
            "phase": "La phase du projet n'est pas claire. Examiner les artefacts présents."
        }
        
        recommendation = base_recommendations.get(severity, "Conflit détecté")
        
        if conflicting_dimensions:
            dimension_advice = [dimension_specific.get(dim, f"Clarifier la dimension {dim}") 
                              for dim in conflicting_dimensions]
            recommendation += f" Actions suggérées: {'; '.join(dimension_advice)}"
        
        return recommendation
    
    def _select_fusion_strategy(self, conflict_analysis: ConflictAnalysis) -> FusionStrategy:
        """Sélectionne la stratégie de fusion basée sur l'analyse des conflits"""
        
        if conflict_analysis.severity == "high":
            return FusionStrategy.CONSENSUS_BASED
        elif conflict_analysis.severity == "medium":
            return FusionStrategy.ADAPTIVE_FUSION
        else:
            return FusionStrategy.WEIGHTED_AVERAGE
    
    def _generate_fallback_result(self, text: str, context: Dict, processing_time: float) -> HybridClassificationResult:
        """Génère un résultat de fallback en cas d'erreur"""
        return HybridClassificationResult(
            final_domain="unknown",
            final_domain_confidence=0.0,
            final_type="unknown",
            final_type_confidence=0.0,
            final_complexity="unknown",
            final_complexity_confidence=0.0,
            final_phase="unknown",
            final_phase_confidence=0.0,
            processing_time=processing_time,
            fallback_used=True,
            recommendations=["Erreur de classification - Analyse manuelle requise"]
        )
    
    def _update_fusion_stats(self, result: HybridClassificationResult):
        """Met à jour les statistiques de fusion"""
        self.fusion_stats['total_fusions'] += 1
        self.fusion_stats['strategy_usage'][result.fusion_method] += 1
        
        if result.conflict_analysis and result.conflict_analysis.has_conflict:
            self.fusion_stats['conflicts_detected'] += 1
        
        if result.fallback_used:
            self.fusion_stats['fallbacks_used'] += 1
        
        self.fusion_stats['avg_processing_time'] += result.processing_time
    
    def _find_consensus(self, scores1: Dict[str, float], scores2: Dict[str, float], llm_confidence: float) -> Dict[str, Any]:
        """Trouve le consensus entre deux ensembles de scores"""
        
        # Trouve le top score de chaque classificateur
        top1 = max(scores1.items(), key=lambda x: x[1]) if scores1 else ("unknown", 0.0)
        top2_key = None
        top2_value = 0.0
        
        # Pour scores2 (LLM), on a une seule valeur
        for key, value in scores2.items():
            if value > top2_value:
                top2_key = key
                top2_value = value
        
        if not top2_key:
            top2_key = "unknown"
            top2_value = 0.0
        
        # Si c'est la même catégorie
        if top1[0] == top2_key:
            # Consensus trouvé
            consensus_value = top1[0]
            confidence = (top1[1] + top2_value) / 2
        else:
            # Pas de consensus, prendre le plus confiant
            if top1[1] > top2_value:
                consensus_value = top1[0]
                confidence = top1[1] * 0.8  # Pénalité pour manque de consensus
            else:
                consensus_value = top2_key
                confidence = top2_value * 0.8
        
        return {
            'value': consensus_value,
            'confidence': min(confidence, 1.0)
        }

    def get_fusion_explanation(self, result: HybridClassificationResult) -> Dict:
        """Génère une explication détaillée du processus de fusion"""
        return {
            'fusion_summary': {
                'method_used': result.fusion_method,
                'overall_confidence': result.fusion_confidence,
                'processing_time': result.processing_time,
                'fallback_used': result.fallback_used
            },
            'conflict_analysis': {
                'conflicts_detected': result.conflict_analysis.has_conflict if result.conflict_analysis else False,
                'severity': result.conflict_analysis.severity if result.conflict_analysis else 'none',
                'conflicting_dimensions': result.conflict_analysis.conflicting_dimensions if result.conflict_analysis else [],
                'recommendation': result.conflict_analysis.recommendation if result.conflict_analysis else "Aucune"
            },
            'classification_details': {
                'domain': {
                    'value': result.final_domain,
                    'confidence': result.final_domain_confidence,
                    'scores': result.domain_scores
                },
                'type': {
                    'value': result.final_type,
                    'confidence': result.final_type_confidence,
                    'scores': result.type_scores
                },
                'complexity': {
                    'value': result.final_complexity,
                    'confidence': result.final_complexity_confidence,
                    'scores': result.complexity_scores
                },
                'phase': {
                    'value': result.final_phase,
                    'confidence': result.final_phase_confidence,
                    'scores': result.phase_scores
                }
            },
            'recommendations': result.recommendations,
            'quality_indicators': result.quality_indicators
        }

# ==================== FONCTIONS UTILITAIRES ====================

def merge_scores(score_dict1: Dict, score_dict2: Dict, weight1: float = 0.5, weight2: float = 0.5) -> Dict:
    """Fusionne deux dictionnaires de scores avec pondération"""
    all_keys = set(score_dict1.keys()) | set(score_dict2.keys())
    merged_scores = {}
    
    for key in all_keys:
        score1 = score_dict1.get(key, 0.0)
        score2 = score_dict2.get(key, 0.0)
        merged_scores[key] = score1 * weight1 + score2 * weight2
    
    return merged_scores

def calculate_consensus_score(scores1: Dict, scores2: Dict, threshold: float = 0.7) -> float:
    """Calcule un score de consensus entre deux ensembles de scores"""
    if not scores1 or not scores2:
        return 0.0
    
    # Trouve le top score de chaque classificateur
    top1 = max(scores1.items(), key=lambda x: x[1])
    top2 = max(scores2.items(), key=lambda x: x[1])
    
    # Si c'est la même catégorie
    if top1[0] == top2[0]:
        # Score basé sur les valeurs de confiance
        return (top1[1] + top2[1]) / 2
    else:
        # Pas de consensus, score basé sur la différence
        return 1.0 - abs(top1[1] - top2[1])
