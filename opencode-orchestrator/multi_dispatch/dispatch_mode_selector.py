#!/usr/bin/env python3
"""
Sélectionneur Intelligent de Mode de Dispatch
Algorithme de sélection automatique du mode de dispatch optimal
"""

import logging
import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict
import numpy as np

from .agent_selector import AgentScore
from core.hybrid_fusion import HybridClassificationResult

class DispatchMode(Enum):
    """Modes de dispatch disponibles"""
    SINGLE = "single"
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HYBRID = "hybrid"
    ADAPTIVE = "adaptive"

class ComplexityLevel(Enum):
    """Niveaux de complexité projet"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class ProjectPhase(Enum):
    """Phases de projet"""
    PLANNING = "planning"
    DEVELOPMENT = "development"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"

@dataclass
class DispatchCriteria:
    """Critères pour la sélection du mode de dispatch"""
    complexity_score: float
    agent_count: int
    diversity_score: float
    confidence_score: float
    phase_priority: str
    time_constraints: Dict[str, Any]
    resource_constraints: Dict[str, Any]
    quality_requirements: Dict[str, float]

@dataclass
class ModeScore:
    """Score d'un mode de dispatch"""
    mode: DispatchMode
    total_score: float
    component_scores: Dict[str, float]
    reasoning: List[str]
    confidence: float

@dataclass
class DispatchRecommendation:
    """Recommandation de dispatch"""
    recommended_mode: DispatchMode
    alternative_modes: List[ModeScore]
    reasoning: str
    confidence: float
    estimated_performance: Dict[str, float]
    risk_assessment: Dict[str, Any]

class DispatchModeSelector:
    """Sélectionneur intelligent du mode de dispatch optimal"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Historique des performances par mode
        self.mode_performance_history = defaultdict(list)
        
        # Matrices de décision
        self.decision_matrices = self._initialize_decision_matrices()
        
        # Poids des critères de décision
        self.criteria_weights = {
            'complexity': 0.25,
            'agent_count': 0.20,
            'diversity': 0.15,
            'confidence': 0.15,
            'phase': 0.10,
            'constraints': 0.15
        }
        
        # Seuils de décision
        self.decision_thresholds = {
            'single_agent_threshold': 1,
            'parallel_min_agents': 2,
            'hybrid_complexity_threshold': 0.6,
            'adaptive_confidence_threshold': 0.7,
            'sequential_phase_requirements': ['planning']
        }
        
        self.logger.info("DispatchModeSelector initialisé")
    
    def _initialize_decision_matrices(self) -> Dict[str, np.ndarray]:
        """Initialise les matrices de décision basées sur l'expérience"""
        
        # Matrice complexité x mode
        complexity_modes = np.array([
            [0.9, 0.6, 0.3, 0.5, 0.7],  # beginner
            [0.4, 0.7, 0.6, 0.8, 0.8],  # intermediate
            [0.2, 0.8, 0.9, 0.9, 0.9],  # advanced
            [0.1, 0.9, 0.7, 0.8, 0.8]   # expert
        ])
        
        # Matrice nombre d'agents x mode
        agent_count_modes = np.array([
            [0.9, 0.7, 0.2, 0.4, 0.6],  # 1 agent
            [0.5, 0.8, 0.7, 0.8, 0.8],  # 2 agents
            [0.2, 0.6, 0.9, 0.9, 0.9],  # 3 agents
            [0.1, 0.5, 0.9, 0.9, 0.9],  # 4 agents
            [0.1, 0.4, 0.8, 0.9, 0.9]   # 5+ agents
        ])
        
        # Matrice phase x mode
        phase_modes = np.array([
            [0.3, 0.9, 0.4, 0.6, 0.7],  # planning
            [0.4, 0.6, 0.8, 0.9, 0.8],  # development
            [0.5, 0.5, 0.9, 0.8, 0.8],  # testing
            [0.3, 0.7, 0.8, 0.7, 0.8],  # deployment
            [0.6, 0.6, 0.6, 0.7, 0.7]   # maintenance
        ])
        
        return {
            'complexity_modes': complexity_modes,
            'agent_count_modes': agent_count_modes,
            'phase_modes': phase_modes
        }
    
    def select_optimal_mode(self,
                          agent_scores: List[AgentScore],
                          classification_result: HybridClassificationResult,
                          context: Dict[str, Any] = None) -> DispatchRecommendation:
        """
        Sélectionne le mode de dispatch optimal
        
        Args:
            agent_scores: Scores des agents sélectionnés
            classification_result: Résultat de classification
            context: Contexte additionnel
        
        Returns:
            DispatchRecommendation avec le mode optimal
        """
        
        try:
            # Phase 1: Analyse des critères
            criteria = self._analyze_dispatch_criteria(
                agent_scores, classification_result, context
            )
            
            # Phase 2: Calcul des scores pour chaque mode
            mode_scores = self._calculate_mode_scores(criteria)
            
            # Phase 3: Sélection du mode optimal
            optimal_mode = self._select_best_mode(mode_scores, criteria)
            
            # Phase 4: Génération de la recommandation
            recommendation = self._generate_recommendation(
                optimal_mode, mode_scores, criteria
            )
            
            self.logger.info(f"Mode sélectionné: {recommendation.recommended_mode.value} "
                           f"(confiance: {recommendation.confidence:.2f})")
            
            return recommendation
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la sélection du mode: {e}")
            return self._generate_fallback_recommendation()
    
    def _analyze_dispatch_criteria(self,
                                 agent_scores: List[AgentScore],
                                 classification_result: HybridClassificationResult,
                                 context: Dict[str, Any]) -> DispatchCriteria:
        """Analyse les critères pour la décision"""
        
        # Score de complexité
        complexity_mapping = {
            "beginner": 0.2,
            "intermediate": 0.5,
            "advanced": 0.8,
            "expert": 1.0
        }
        complexity_score = complexity_mapping.get(
            classification_result.final_complexity, 0.5
        )
        
        # Nombre d'agents
        agent_count = len(agent_scores)
        
        # Score de diversité des agents
        diversity_score = self._calculate_agent_diversity(agent_scores)
        
        # Score de confiance
        confidence_score = classification_result.fusion_confidence
        
        # Priorité de phase
        phase_priority = classification_result.final_phase
        
        # Contraintes temporelles
        time_constraints = context.get('time_constraints', {}) if context else {}
        
        # Contraintes de ressources
        resource_constraints = context.get('resource_constraints', {}) if context else {}
        
        # Exigences de qualité
        quality_requirements = context.get('quality_requirements', {}) if context else {}
        
        return DispatchCriteria(
            complexity_score=complexity_score,
            agent_count=agent_count,
            diversity_score=diversity_score,
            confidence_score=confidence_score,
            phase_priority=phase_priority,
            time_constraints=time_constraints,
            resource_constraints=resource_constraints,
            quality_requirements=quality_requirements
        )
    
    def _calculate_agent_diversity(self, agent_scores: List[AgentScore]) -> float:
        """Calcule un score de diversité des agents"""
        
        if len(agent_scores) < 2:
            return 0.0
        
        # Variance des scores totaux
        scores = [agent.total_score for agent in agent_scores]
        score_variance = np.var(scores)
        
        # Variance des capacités
        capabilities = []
        for agent in agent_scores:
            capabilities.extend(agent.capability_scores.values())
        capability_variance = np.var(capabilities) if capabilities else 0.0
        
        # Variance des types d'agents (simulation)
        type_variance = 0.3  # Valeur par défaut
        
        # Score de diversité global
        diversity_score = (score_variance + capability_variance + type_variance) / 3
        
        # Normalisation
        return min(diversity_score * 2, 1.0)
    
    def _calculate_mode_scores(self, criteria: DispatchCriteria) -> List[ModeScore]:
        """Calcule les scores pour chaque mode de dispatch"""
        
        mode_scores = []
        
        for mode in DispatchMode:
            # Score de complexité
            complexity_idx = self._complexity_to_index(criteria.complexity_score)
            complexity_score = self.decision_matrices['complexity_modes'][complexity_idx][mode.value]
            
            # Score du nombre d'agents
            agent_count_idx = min(criteria.agent_count, 4)  # Limite à 4 pour la matrice
            agent_count_score = self.decision_matrices['agent_count_modes'][agent_count_idx][mode.value]
            
            # Score de phase
            phase_idx = self._phase_to_index(criteria.phase_priority)
            phase_score = self.decision_matrices['phase_modes'][phase_idx][mode.value]
            
            # Score de diversité
            diversity_score = self._calculate_diversity_score(mode, criteria.diversity_score)
            
            # Score de confiance
            confidence_score = self._calculate_confidence_score(mode, criteria.confidence_score)
            
            # Score des contraintes
            constraint_score = self._calculate_constraint_score(mode, criteria)
            
            # Score total pondéré
            total_score = (
                complexity_score * self.criteria_weights['complexity'] +
                agent_count_score * self.criteria_weights['agent_count'] +
                diversity_score * self.criteria_weights['diversity'] +
                confidence_score * self.criteria_weights['confidence'] +
                phase_score * self.criteria_weights['phase'] +
                constraint_score * self.criteria_weights['constraints']
            )
            
            # Génération du raisonnement
            reasoning = self._generate_score_reasoning(
                mode, complexity_score, agent_count_score, phase_score, 
                diversity_score, confidence_score, constraint_score
            )
            
            mode_scores.append(ModeScore(
                mode=mode,
                total_score=total_score,
                component_scores={
                    'complexity': complexity_score,
                    'agent_count': agent_count_score,
                    'phase': phase_score,
                    'diversity': diversity_score,
                    'confidence': confidence_score,
                    'constraints': constraint_score
                },
                reasoning=reasoning,
                confidence=self._calculate_mode_confidence(mode, criteria)
            ))
        
        return mode_scores
    
    def _complexity_to_index(self, complexity_score: float) -> int:
        """Convertit le score de complexité en indice de matrice"""
        if complexity_score <= 0.3:
            return 0  # beginner
        elif complexity_score <= 0.6:
            return 1  # intermediate
        elif complexity_score <= 0.8:
            return 2  # advanced
        else:
            return 3  # expert
    
    def _phase_to_index(self, phase: str) -> int:
        """Convertit la phase en indice de matrice"""
        phase_mapping = {
            "planning": 0,
            "development": 1,
            "testing": 2,
            "deployment": 3,
            "maintenance": 4
        }
        return phase_mapping.get(phase, 1)  # default to development
    
    def _calculate_diversity_score(self, mode: DispatchMode, diversity_score: float) -> float:
        """Calcule le score de diversité pour un mode"""
        
        if mode == DispatchMode.PARALLEL:
            return min(diversity_score * 1.2, 1.0)  # Bonus pour parallèle
        elif mode == DispatchMode.HYBRID:
            return diversity_score * 1.1  # Bonus modéré pour hybride
        elif mode == DispatchMode.SINGLE:
            return 0.2  # Malus pour single avec diversité élevée
        else:
            return diversity_score
    
    def _calculate_confidence_score(self, mode: DispatchMode, confidence_score: float) -> float:
        """Calcule le score de confiance pour un mode"""
        
        if confidence_score > 0.8:
            # Haute confiance = modes plus sophistiqués
            if mode in [DispatchMode.PARALLEL, DispatchMode.HYBRID, DispatchMode.ADAPTIVE]:
                return 0.9
            else:
                return 0.7
        elif confidence_score < 0.5:
            # Faible confiance = modes plus simples
            if mode == DispatchMode.SINGLE:
                return 0.8
            else:
                return 0.4
        else:
            # Confiance moyenne = tous les modes
            return confidence_score
    
    def _calculate_constraint_score(self, mode: DispatchMode, criteria: DispatchCriteria) -> float:
        """Calcule le score basé sur les contraintes"""
        
        base_score = 0.5
        
        # Contraintes temporelles
        if criteria.time_constraints.get('urgent', False):
            if mode == DispatchMode.PARALLEL:
                base_score += 0.3  # Urgent = parallèle favorisé
            elif mode == DispatchMode.SEQUENTIAL:
                base_score -= 0.2  # Urgent = séquentiel pénalisé
        
        # Contraintes de ressources
        max_concurrent = criteria.resource_constraints.get('max_concurrent_tasks', 10)
        if max_concurrent < criteria.agent_count and mode == DispatchMode.PARALLEL:
            base_score -= 0.3  # Trop d'agents pour le parallèle
        
        # Exigences de qualité
        min_quality = criteria.quality_requirements.get('min_quality', 0.5)
        if min_quality > 0.8:
            if mode in [DispatchMode.HYBRID, DispatchMode.ADAPTIVE]:
                base_score += 0.2  # Haute qualité = modes sophistiqués
        
        return max(0.0, min(base_score, 1.0))
    
    def _calculate_mode_confidence(self, mode: DispatchMode, criteria: DispatchCriteria) -> float:
        """Calcule la confiance dans le choix d'un mode"""
        
        confidence = 0.5  # Base
        
        # Confiance plus élevée pour les modes bien adaptés
        if (mode == DispatchMode.SINGLE and criteria.agent_count <= 1) or \
           (mode == DispatchMode.PARALLEL and criteria.agent_count >= 2) or \
           (mode == DispatchMode.SEQUENTIAL and criteria.phase_priority == "planning"):
            confidence += 0.3
        
        # Confiance basée sur l'historique de performance
        if mode in self.mode_performance_history:
            avg_performance = np.mean(self.mode_performance_history[mode])
            confidence += avg_performance * 0.2
        
        return min(confidence, 1.0)
    
    def _generate_score_reasoning(self, mode: DispatchMode, complexity_score: float,
                                agent_count_score: float, phase_score: float,
                                diversity_score: float, confidence_score: float,
                                constraint_score: float) -> List[str]:
        """Génère le raisonnement pour le score d'un mode"""
        
        reasoning = []
        
        if complexity_score > 0.7:
            reasoning.append(f"Mode adapté à la complexité ({complexity_score:.2f})")
        elif complexity_score < 0.3:
            reasoning.append(f"Mode peu adapté à la complexité ({complexity_score:.2f})")
        
        if agent_count_score > 0.7:
            reasoning.append(f"Nombre d'agents favorable ({agent_count_score:.2f})")
        
        if phase_score > 0.7:
            reasoning.append(f"Phase de projet favorable ({phase_score:.2f})")
        
        if diversity_score > 0.6:
            reasoning.append(f"Diversité des agents favorable ({diversity_score:.2f})")
        
        if confidence_score > 0.7:
            reasoning.append(f"Confiance élevée ({confidence_score:.2f})")
        
        if constraint_score > 0.7:
            reasoning.append(f"Contraintes favorables ({constraint_score:.2f})")
        
        return reasoning
    
    def _select_best_mode(self, mode_scores: List[ModeScore], 
                         criteria: DispatchCriteria) -> ModeScore:
        """Sélectionne le meilleur mode parmi les scores calculés"""
        
        # Application des règles de override
        overridden_mode = self._apply_override_rules(mode_scores, criteria)
        if overridden_mode:
            return overridden_mode
        
        # Sélection du score le plus élevé
        best_mode = max(mode_scores, key=lambda x: x.total_score)
        
        return best_mode
    
    def _apply_override_rules(self, mode_scores: List[ModeScore], 
                            criteria: DispatchCriteria) -> Optional[ModeScore]:
        """Applique les règles de override pour cas spéciaux"""
        
        # Règle: Un seul agent → toujours SINGLE
        if criteria.agent_count == 1:
            single_mode = next((ms for ms in mode_scores if ms.mode == DispatchMode.SINGLE), None)
            if single_mode:
                single_mode.reasoning.append("Override: Un seul agent disponible")
                return single_mode
        
        # Règle: Phase de planification → SEQUENTIAL si possible
        if criteria.phase_priority == "planning":
            sequential_mode = next((ms for ms in mode_scores if ms.mode == DispatchMode.SEQUENTIAL), None)
            if sequential_mode and sequential_mode.total_score > 0.5:
                sequential_mode.reasoning.append("Override: Phase de planification")
                return sequential_mode
        
        # Règle: Urgence temporelle → PARALLEL si agents suffisants
        if criteria.time_constraints.get('urgent', False) and criteria.agent_count >= 2:
            parallel_mode = next((ms for ms in mode_scores if ms.mode == DispatchMode.PARALLEL), None)
            if parallel_mode and parallel_mode.total_score > 0.4:
                parallel_mode.reasoning.append("Override: Urgence temporelle")
                return parallel_mode
        
        # Règle: Très faible confiance → SINGLE
        if criteria.confidence_score < 0.4:
            single_mode = next((ms for ms in mode_scores if ms.mode == DispatchMode.SINGLE), None)
            if single_mode:
                single_mode.reasoning.append("Override: Confiance trop faible")
                return single_mode
        
        return None
    
    def _generate_recommendation(self, optimal_mode: ModeScore, 
                               all_mode_scores: List[ModeScore],
                               criteria: DispatchCriteria) -> DispatchRecommendation:
        """Génère la recommandation finale"""
        
        # Tri des modes alternatifs
        alternative_modes = sorted(
            [ms for ms in all_mode_scores if ms.mode != optimal_mode.mode],
            key=lambda x: x.total_score,
            reverse=True
        )[:2]  # Top 2 alternatives
        
        # Raisonnement global
        global_reasoning = self._generate_global_reasoning(optimal_mode, criteria)
        
        # Performance estimée
        estimated_performance = self._estimate_performance(optimal_mode.mode, criteria)
        
        # Évaluation des risques
        risk_assessment = self._assess_risks(optimal_mode.mode, criteria)
        
        return DispatchRecommendation(
            recommended_mode=optimal_mode.mode,
            alternative_modes=alternative_modes,
            reasoning=global_reasoning,
            confidence=optimal_mode.confidence,
            estimated_performance=estimated_performance,
            risk_assessment=risk_assessment
        )
    
    def _generate_global_reasoning(self, optimal_mode: ModeScore, 
                                 criteria: DispatchCriteria) -> str:
        """Génère le raisonnement global de la recommandation"""
        
        reasoning_parts = [
            f"Mode recommandé: {optimal_mode.mode.value}",
            f"Score total: {optimal_mode.total_score:.2f}",
            f"Confiance: {optimal_mode.confidence:.2f}"
        ]
        
        # Ajout des facteurs clés
        key_factors = []
        for factor, score in optimal_mode.component_scores.items():
            if score > 0.7:
                key_factors.append(f"{factor} favorable ({score:.2f})")
        
        if key_factors:
            reasoning_parts.append(f"Facteurs clés: {', '.join(key_factors)}")
        
        # Ajout des contraintes spécifiques
        if criteria.time_constraints.get('urgent', False):
            reasoning_parts.append("Contrainte temporelle: urgent")
        
        if criteria.resource_constraints.get('max_concurrent_tasks', 10) < criteria.agent_count:
            reasoning_parts.append("Contrainte: limitation du parallélisme")
        
        return " | ".join(reasoning_parts)
    
    def _estimate_performance(self, mode: DispatchMode, 
                            criteria: DispatchCriteria) -> Dict[str, float]:
        """Estime les performances attendues du mode"""
        
        # Estimation de base selon le mode
        base_performance = {
            DispatchMode.SINGLE: {'speed': 0.3, 'quality': 0.6, 'reliability': 0.8},
            DispatchMode.SEQUENTIAL: {'speed': 0.4, 'quality': 0.8, 'reliability': 0.9},
            DispatchMode.PARALLEL: {'speed': 0.9, 'quality': 0.7, 'reliability': 0.7},
            DispatchMode.HYBRID: {'speed': 0.7, 'quality': 0.9, 'reliability': 0.8},
            DispatchMode.ADAPTIVE: {'speed': 0.6, 'quality': 0.8, 'reliability': 0.8}
        }
        
        performance = base_performance[mode].copy()
        
        # Ajustements selon les critères
        if criteria.complexity_score > 0.8:  # Projets experts
            performance['quality'] *= 1.1
            performance['speed'] *= 0.9
        
        if criteria.agent_count >= 3:  # Agents multiples
            performance['speed'] *= 1.2
            performance['reliability'] *= 0.95
        
        if criteria.diversity_score > 0.7:  # Diversité élevée
            performance['quality'] *= 1.1
        
        # Normalisation
        for key in performance:
            performance[key] = max(0.1, min(performance[key], 1.0))
        
        return performance
    
    def _assess_risks(self, mode: DispatchMode, 
                     criteria: DispatchCriteria) -> Dict[str, Any]:
        """Évalue les risques associés au mode"""
        
        risks = {
            'risk_level': 'low',
            'risk_factors': [],
            'mitigation_strategies': []
        }
        
        # Risques par mode
        if mode == DispatchMode.PARALLEL:
            if criteria.agent_count > 4:
                risks['risk_factors'].append("Trop d'agents en parallèle")
                risks['risk_level'] = 'medium'
            
            if criteria.diversity_score < 0.3:
                risks['risk_factors'].append("Diversité faible des agents")
                risks['risk_level'] = 'medium'
        
        elif mode == DispatchMode.SEQUENTIAL:
            if criteria.time_constraints.get('urgent', False):
                risks['risk_factors'].append("Mode séquentiel lent pour projet urgent")
                risks['risk_level'] = 'medium'
        
        elif mode == DispatchMode.SINGLE:
            if criteria.complexity_score > 0.7:
                risks['risk_factors'].append("Complexité élevée pour un seul agent")
                risks['risk_level'] = 'high'
            
            if criteria.agent_count > 1:
                risks['risk_factors'].append("Agents multiples non utilisés")
                risks['risk_level'] = 'medium'
        
        # Stratégies de mitigation
        if risks['risk_factors']:
            risks['mitigation_strategies'].append("Monitoring en temps réel")
            risks['mitigation_strategies'].append("Fallback vers mode alternatif")
        
        if criteria.confidence_score < 0.6:
            risks['mitigation_strategies'].append("Validation manuelle des résultats")
        
        return risks
    
    def _generate_fallback_recommendation(self) -> DispatchRecommendation:
        """Génère une recommandation de fallback en cas d'erreur"""
        
        return DispatchRecommendation(
            recommended_mode=DispatchMode.SEQUENTIAL,
            alternative_modes=[],
            reasoning="Recommandation de fallback - erreur lors de l'analyse",
            confidence=0.3,
            estimated_performance={'speed': 0.5, 'quality': 0.7, 'reliability': 0.8},
            risk_assessment={'risk_level': 'low', 'risk_factors': [], 'mitigation_strategies': []}
        )
    
    def learn_from_performance(self, mode: DispatchMode, 
                             actual_performance: Dict[str, float],
                             criteria: DispatchCriteria):
        """Apprend des performances réelles pour améliorer les futures décisions"""
        
        performance_entry = {
            'timestamp': time.time(),
            'mode': mode.value,
            'performance': actual_performance,
            'criteria': {
                'complexity_score': criteria.complexity_score,
                'agent_count': criteria.agent_count,
                'diversity_score': criteria.diversity_score,
                'confidence_score': criteria.confidence_score
            }
        }
        
        self.mode_performance_history[mode].append(performance_entry)
        
        # Garder seulement les 100 dernières entrées par mode
        if len(self.mode_performance_history[mode]) > 100:
            self.mode_performance_history[mode] = self.mode_performance_history[mode][-100:]
        
        # Ajustement des poids basé sur l'apprentissage
        self._adjust_criteria_weights(mode, actual_performance)
    
    def _adjust_criteria_weights(self, mode: DispatchMode, performance: Dict[str, float]):
        """Ajuste les poids des critères basé sur les performances"""
        
        # Analyse simplifiée des performances par mode
        if performance.get('success_rate', 0) > 0.8:
            # Mode performant, ajuster légèrement les poids
            if mode == DispatchMode.PARALLEL:
                self.criteria_weights['agent_count'] *= 1.05
            elif mode == DispatchMode.SEQUENTIAL:
                self.criteria_weights['phase'] *= 1.05
        
        # Normalisation des poids
        total_weight = sum(self.criteria_weights.values())
        for key in self.criteria_weights:
            self.criteria_weights[key] /= total_weight