"""
Mécanisme de Sélection d'Agents Multi-Critères
Système intelligent de scoring et matching pour la sélection optimale des sub-agents
"""

import logging
import time
import numpy as np
from typing import Dict, List, Tuple, Optional, Any, NamedTuple
from dataclasses import dataclass, field
from enum import Enum
import statistics
from collections import defaultdict
import json

from core.routing_matrix import RoutingTarget
from core.hybrid_fusion import HybridClassificationResult

@dataclass
class AgentCapability:
    """Représente une capacité spécifique d'un agent"""
    name: str
    proficiency_level: float  # 0.0 - 1.0
    experience_score: float   # 0.0 - 1.0
    context_relevance: float  # 0.0 - 1.0
    cost_factor: float        # 0.0 - 1.0 (lower is better)

@dataclass
class AgentScore:
    """Score détaillé pour un agent"""
    agent_id: str
    total_score: float
    capability_scores: Dict[str, float]
    performance_metrics: Dict[str, float]
    context_match: float
    resource_efficiency: float
    collaboration_score: float
    reasoning: List[str] = field(default_factory=list)

@dataclass
class SelectionCriteria:
    """Critères de sélection pour les agents"""
    primary_domain: str
    task_complexity: str
    project_phase: str
    required_capabilities: List[str]
    performance_priority: float = 0.3
    cost_priority: float = 0.2
    availability_priority: float = 0.2
    collaboration_priority: float = 0.15
    context_priority: float = 0.15
    max_agents: int = 5
    min_confidence: float = 0.6

class SelectionStrategy(Enum):
    """Stratégies de sélection d'agents"""
    PERFORMANCE_OPTIMIZED = "performance_optimized"
    COST_EFFECTIVE = "cost_effective"
    BALANCED_SCORE = "balanced_score"
    COLLABORATION_FOCUSED = "collaboration_focused"
    CONTEXT_ADAPTIVE = "context_adaptive"
    HYBRID_OPTIMIZATION = "hybrid_optimization"

class IntelligentAgentSelector:
    """Sélecteur intelligent d'agents avec algorithmes multi-critères"""
    
    def __init__(self, selection_strategy: SelectionStrategy = SelectionStrategy.HYBRID_OPTIMIZATION):
        self.selection_strategy = selection_strategy
        self.logger = logging.getLogger(__name__)
        
        # Cache pour les évaluations d'agents
        self._agent_cache = {}
        
        # Métriques de performance
        self.selection_stats = {
            'total_selections': 0,
            'successful_matches': 0,
            'average_selection_time': 0.0,
            'strategy_usage': {strategy.value: 0 for strategy in SelectionStrategy},
            'capability_usage': defaultdict(int),
            'collaboration_patterns': defaultdict(int)
        }
        
        # Historique des performances pour apprentissage
        self.performance_history = []
        
        # Matrices de correspondance capabilities
        self._initialize_capability_matrices()
    
    def _initialize_capability_matrices(self):
        """Initialise les matrices de correspondance des capacités"""
        
        # Mapping des capacités par domaine
        self.domain_capabilities = {
            "web_development": [
                "frontend_development", "backend_development", "fullstack_development",
                "api_development", "database_integration", "ui_ux_design",
                "performance_optimization", "testing_automation", "deployment_setup"
            ],
            "data_science": [
                "machine_learning", "data_analysis", "statistical_modeling",
                "data_visualization", "feature_engineering", "model_deployment",
                "big_data_processing", "predictive_analytics", "experiment_design"
            ],
            "mobile_development": [
                "android_development", "ios_development", "react_native", "flutter",
                "mobile_ui_design", "app_store_optimization", "mobile_testing",
                "push_notifications", "offline_capabilities"
            ],
            "devops": [
                "infrastructure_automation", "ci_cd_setup", "monitoring_setup",
                "containerization", "orchestration", "security_hardening",
                "disaster_recovery", "performance_tuning", "scalability_planning"
            ],
            "cybersecurity": [
                "security_analysis", "vulnerability_assessment", "penetration_testing",
                "compliance_auditing", "incident_response", "threat_modeling",
                "security_architecture", "risk_assessment", "security_training"
            ]
        }
        
        # Matrice de synergie entre agents
        self.synergy_matrix = self._build_synergy_matrix()
    
    def _build_synergy_matrix(self) -> Dict[str, Dict[str, float]]:
        """Construit la matrice de synergie entre agents"""
        synergy = defaultdict(lambda: defaultdict(float))
        
        # Synergies haute collaboration
        high_synergy_pairs = [
            ("frontend_development", "ui_ux_design", 0.9),
            ("backend_development", "database_integration", 0.85),
            ("machine_learning", "data_visualization", 0.8),
            ("infrastructure_automation", "ci_cd_setup", 0.9),
            ("security_analysis", "penetration_testing", 0.85),
            ("android_development", "ios_development", 0.75),
            ("react_native", "flutter", 0.7),
            ("api_development", "testing_automation", 0.8)
        ]
        
        for cap1, cap2, score in high_synergy_pairs:
            synergy[cap1][cap2] = score
            synergy[cap2][cap1] = score
        
        return dict(synergy)
    
    def select_agents(self, classification_result: HybridClassificationResult,
                     context: Dict[str, Any] = None,
                     criteria: SelectionCriteria = None) -> List[AgentScore]:
        """
        Sélection intelligente des agents optimaux
        
        Args:
            classification_result: Résultat de classification hybride
            context: Contexte additionnel du projet
            criteria: Critères de sélection
        
        Returns:
            Liste ordonnée des agents avec scores détaillés
        """
        start_time = time.time()
        
        try:
            # Génération des critères de sélection
            if criteria is None:
                criteria = self._generate_selection_criteria(classification_result, context)
            
            # Construction du profil de besoin
            need_profile = self._build_need_profile(classification_result, context, criteria)
            
            # Évaluation de tous les agents disponibles
            agent_evaluations = self._evaluate_all_agents(need_profile, criteria)
            
            # Application de la stratégie de sélection
            selected_agents = self._apply_selection_strategy(
                agent_evaluations, criteria, need_profile
            )
            
            # Optimisation de la collaboration
            optimized_agents = self._optimize_agent_collaboration(selected_agents, need_profile)
            
            # Mise à jour des statistiques
            self._update_selection_stats(optimized_agents, time.time() - start_time, True)
            
            self.logger.info(f"Sélection de {len(optimized_agents)} agents en {time.time() - start_time:.3f}s")
            return optimized_agents
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la sélection d'agents: {e}")
            self._update_selection_stats([], time.time() - start_time, False)
            return []
    
    def _generate_selection_criteria(self, classification_result: HybridClassificationResult,
                                   context: Dict[str, Any] = None) -> SelectionCriteria:
        """Génère automatiquement les critères de sélection"""
        
        # Extraction des dimensions principales
        domain = classification_result.final_domain
        complexity = classification_result.final_complexity
        phase = classification_result.final_phase
        
        # Adaptation des critères selon la complexité
        if complexity == "beginner":
            max_agents = 2
            min_confidence = 0.5
            performance_priority = 0.2
        elif complexity == "expert":
            max_agents = 4
            min_confidence = 0.8
            performance_priority = 0.4
        else:
            max_agents = 3
            min_confidence = 0.6
            performance_priority = 0.3
        
        # Adaptation selon la phase
        if phase == "planning":
            cost_priority = 0.3  # Focus sur le coût en phase de planification
        elif phase == "deployment":
            performance_priority = 0.4  # Focus sur la performance en déploiement
        else:
            cost_priority = 0.2
        
        # Extraction des capacités requises depuis le contexte
        required_capabilities = self.domain_capabilities.get(domain, [])
        
        # Ajout de capacités spécifiques selon le contexte
        if context:
            if 'technologies' in context:
                tech_capabilities = self._map_technologies_to_capabilities(context['technologies'])
                required_capabilities.extend(tech_capabilities)
        
        return SelectionCriteria(
            primary_domain=domain,
            task_complexity=complexity,
            project_phase=phase,
            required_capabilities=list(set(required_capabilities)),
            max_agents=max_agents,
            min_confidence=min_confidence,
            performance_priority=performance_priority,
            cost_priority=cost_priority
        )
    
    def _build_need_profile(self, classification_result: HybridClassificationResult,
                          context: Dict[str, Any], criteria: SelectionCriteria) -> Dict[str, Any]:
        """Construit le profil de besoin du projet"""
        
        return {
            'domain': classification_result.final_domain,
            'complexity': classification_result.final_complexity,
            'phase': classification_result.final_phase,
            'confidence': classification_result.fusion_confidence,
            'required_capabilities': criteria.required_capabilities,
            'domain_scores': classification_result.domain_scores,
            'context_technologies': context.get('technologies', []) if context else [],
            'project_size': self._estimate_project_size(context),
            'timeline_pressure': self._assess_timeline_pressure(classification_result, context),
            'risk_level': self._assess_risk_level(classification_result, context)
        }
    
    def _evaluate_all_agents(self, need_profile: Dict[str, Any], 
                           criteria: SelectionCriteria) -> List[AgentScore]:
        """Évalue tous les agents disponibles"""
        
        # Récupération des agents depuis la matrice de routage
        from core.routing_matrix import RoutingMatrix
        routing_matrix = RoutingMatrix()
        
        agent_evaluations = []
        
        for target_id, target in routing_matrix.routing_targets.items():
            evaluation = self._evaluate_single_agent(target, need_profile, criteria)
            if evaluation and evaluation.total_score >= criteria.min_confidence:
                agent_evaluations.append(evaluation)
        
        # Tri par score total
        agent_evaluations.sort(key=lambda x: x.total_score, reverse=True)
        
        return agent_evaluations
    
    def _evaluate_single_agent(self, target: RoutingTarget, 
                             need_profile: Dict[str, Any],
                             criteria: SelectionCriteria) -> Optional[AgentScore]:
        """Évalue un agent individuel"""
        
        agent_id = target.target_id
        
        # Scores par dimension
        capability_score = self._calculate_capability_score(target, need_profile)
        performance_score = self._calculate_performance_score(target, need_profile)
        context_score = self._calculate_context_score(target, need_profile)
        efficiency_score = self._calculate_efficiency_score(target, need_profile)
        collaboration_score = self._calculate_collaboration_score(target, need_profile)
        
        # Score total pondéré
        total_score = (
            capability_score * 0.35 +
            performance_score * criteria.performance_priority +
            context_score * criteria.context_priority +
            efficiency_score * criteria.cost_priority +
            collaboration_score * criteria.collaboration_priority
        )
        
        # Génération du raisonnement
        reasoning = self._generate_evaluation_reasoning(
            target, capability_score, performance_score, context_score, 
            efficiency_score, collaboration_score, total_score
        )
        
        return AgentScore(
            agent_id=agent_id,
            total_score=total_score,
            capability_scores={'main': capability_score},
            performance_metrics={
                'performance': performance_score,
                'context_match': context_score,
                'efficiency': efficiency_score,
                'collaboration': collaboration_score
            },
            context_match=context_score,
            resource_efficiency=efficiency_score,
            collaboration_score=collaboration_score,
            reasoning=reasoning
        )
    
    def _calculate_capability_score(self, target: RoutingTarget, 
                                  need_profile: Dict[str, Any]) -> float:
        """Calcule le score de correspondance des capacités"""
        
        domain = need_profile['domain']
        required_capabilities = need_profile['required_capabilities']
        
        # Agent capabilities du target
        agent_caps = target.capabilities
        
        # Score basé sur l'intersection des capacités
        required_set = set(required_capabilities)
        agent_set = set(agent_caps)
        
        if not required_set:
            return 0.5  # Score par défaut si pas de capacités requises
        
        intersection = len(required_set & agent_set)
        union = len(required_set | agent_set)
        
        jaccard_score = intersection / union if union > 0 else 0.0
        
        # Bonus pour expertise de domaine
        domain_expertise_bonus = 1.0 if domain in target.domain_expertise else 0.3
        
        # Bonus pour support de complexité
        complexity_bonus = 1.0 if need_profile['complexity'] in target.complexity_support else 0.2
        
        # Bonus pour support de phase
        phase_bonus = 1.0 if need_profile['phase'] in target.phase_support else 0.4
        
        final_score = jaccard_score * (0.4 + 0.3 * domain_expertise_bonus + 
                                     0.2 * complexity_bonus + 0.1 * phase_bonus)
        
        return min(final_score, 1.0)
    
    def _calculate_performance_score(self, target: RoutingTarget, 
                                   need_profile: Dict[str, Any]) -> float:
        """Calcule le score de performance historique"""
        
        base_performance = target.performance_score
        
        # Ajustement selon la complexité du projet
        complexity = need_profile['complexity']
        if complexity == "expert" and target.performance_score < 0.8:
            # Réduction du score pour projets experts si performance insuffisante
            return base_performance * 0.8
        elif complexity == "beginner" and base_performance > 0.9:
            # Bonus pour projets simples si performance élevée
            return min(base_performance * 1.1, 1.0)
        
        return base_performance
    
    def _calculate_context_score(self, target: RoutingTarget, 
                               need_profile: Dict[str, Any]) -> float:
        """Calcule le score de correspondance contextuelle"""
        
        base_score = 0.5
        
        # Score de disponibilité
        availability_score = target.availability
        
        # Score de charge (inversé - moins de charge = meilleur score)
        load_score = 1.0 - target.load_factor
        
        # Bonus pour technologies spécifiques si présentes dans le contexte
        tech_bonus = 0.0
        if 'context_technologies' in need_profile:
            tech_capabilities = self._map_technologies_to_capabilities(need_profile['context_technologies'])
            agent_capabilities = set(target.capabilities)
            tech_cap_set = set(tech_capabilities)
            
            if agent_capabilities & tech_cap_set:
                tech_bonus = 0.2
        
        final_score = (base_score + availability_score + load_score + tech_bonus) / 3.0
        return min(final_score, 1.0)
    
    def _calculate_efficiency_score(self, target: RoutingTarget, 
                                  need_profile: Dict[str, Any]) -> float:
        """Calcule le score d'efficacité des ressources"""
        
        # Facteur de coût (inversé - moins coûteux = meilleur score)
        cost_factor = 1.0 - target.load_factor
        
        # Disponibilité comme proxy de l'efficacité
        availability_factor = target.availability
        
        # Ajustement selon la phase du projet
        phase = need_profile['phase']
        if phase == "planning":
            # En planification, l'efficacité de coût est plus importante
            efficiency_score = (cost_factor * 0.7 + availability_factor * 0.3)
        elif phase == "deployment":
            # En déploiement, la disponibilité est plus critique
            efficiency_score = (cost_factor * 0.3 + availability_factor * 0.7)
        else:
            efficiency_score = (cost_factor * 0.5 + availability_factor * 0.5)
        
        return efficiency_score
    
    def _calculate_collaboration_score(self, target: RoutingTarget, 
                                     need_profile: Dict[str, Any]) -> float:
        """Calcule le score de collaboration potentielle"""
        
        # Score basé sur la synergie avec les capacités requises
        required_capabilities = need_profile['required_capabilities']
        agent_capabilities = target.capabilities
        
        synergy_score = 0.0
        if required_capabilities and agent_capabilities:
            for req_cap in required_capabilities:
                for agent_cap in agent_capabilities:
                    synergy_score += self.synergy_matrix.get(req_cap, {}).get(agent_cap, 0.0)
            
            synergy_score /= len(required_capabilities)  # Normalisation
        
        # Bonus pour le type d'agent (humain vs automatisé)
        type_bonus = 0.1 if target.type == "human_resource" else 0.05
        
        return min(synergy_score + type_bonus, 1.0)
    
    def _apply_selection_strategy(self, agent_evaluations: List[AgentScore],
                                criteria: SelectionCriteria,
                                need_profile: Dict[str, Any]) -> List[AgentScore]:
        """Applique la stratégie de sélection"""
        
        if not agent_evaluations:
            return []
        
        selected_agents = agent_evaluations[:criteria.max_agents]
        
        if self.selection_strategy == SelectionStrategy.PERFORMANCE_OPTIMIZED:
            selected_agents.sort(key=lambda x: x.performance_metrics['performance'], reverse=True)
        elif self.selection_strategy == SelectionStrategy.COST_EFFECTIVE:
            selected_agents.sort(key=lambda x: x.resource_efficiency, reverse=True)
        elif self.selection_strategy == SelectionStrategy.COLLABORATION_FOCUSED:
            selected_agents.sort(key=lambda x: x.collaboration_score, reverse=True)
        elif self.selection_strategy == SelectionStrategy.CONTEXT_ADAPTIVE:
            selected_agents.sort(key=lambda x: x.context_match, reverse=True)
        # HYBRID_OPTIMIZATION et BALANCED_SCORE utilisent déjà le tri par score total
        
        return selected_agents[:criteria.max_agents]
    
    def _optimize_agent_collaboration(self, selected_agents: List[AgentScore],
                                    need_profile: Dict[str, Any]) -> List[AgentScore]:
        """Optimise la collaboration entre agents sélectionnés"""
        
        if len(selected_agents) < 2:
            return selected_agents
        
        # Récupération des agents depuis la matrice de routage
        from core.routing_matrix import RoutingMatrix
        routing_matrix = RoutingMatrix()
        
        optimized_selection = []
        used_agent_ids = set()
        
        # Sélection du premier agent (meilleur score)
        first_agent = selected_agents[0]
        optimized_selection.append(first_agent)
        used_agent_ids.add(first_agent.agent_id)
        
        # Sélection des agents suivants en optimisant la collaboration
        remaining_agents = selected_agents[1:]
        
        for candidate in remaining_agents:
            if len(optimized_selection) >= need_profile.get('max_agents', 3):
                break
            
            # Calcul du score de collaboration avec la sélection actuelle
            collaboration_bonus = 0.0
            for selected in optimized_selection:
                selected_target = routing_matrix.routing_targets[selected.agent_id]
                candidate_target = routing_matrix.routing_targets[candidate.agent_id]
                
                # Calcul de la synergie
                for selected_cap in selected_target.capabilities:
                    for candidate_cap in candidate_target.capabilities:
                        collaboration_bonus += self.synergy_matrix.get(selected_cap, {}).get(candidate_cap, 0.0)
            
            if collaboration_bonus > 0.1:  # Seuil minimal de collaboration
                candidate.collaboration_score += collaboration_bonus * 0.1
                candidate.total_score += collaboration_bonus * 0.05  # Petit bonus au score total
            
            if candidate.agent_id not in used_agent_ids:
                optimized_selection.append(candidate)
                used_agent_ids.add(candidate.agent_id)
        
        # Retri par score total après optimisation
        optimized_selection.sort(key=lambda x: x.total_score, reverse=True)
        
        return optimized_selection[:criteria.max_agents] if 'criteria' in locals() else optimized_selection[:3]
    
    def _map_technologies_to_capabilities(self, technologies: List[str]) -> List[str]:
        """Mappe les technologies vers des capacités"""
        tech_capability_map = {
            "React": ["frontend_development", "ui_ux_design"],
            "Angular": ["frontend_development", "ui_ux_design"],
            "Vue": ["frontend_development", "ui_ux_design"],
            "Node.js": ["backend_development", "api_development"],
            "Django": ["backend_development", "database_integration"],
            "Flask": ["backend_development", "api_development"],
            "Python": ["machine_learning", "data_analysis", "backend_development"],
            "TensorFlow": ["machine_learning", "model_deployment"],
            "scikit-learn": ["machine_learning", "data_analysis"],
            "Docker": ["containerization", "infrastructure_automation"],
            "Kubernetes": ["orchestration", "infrastructure_automation"],
            "Jenkins": ["ci_cd_setup", "infrastructure_automation"],
            "MongoDB": ["database_integration"],
            "PostgreSQL": ["database_integration"],
            "Redis": ["performance_optimization"],
            "AWS": ["infrastructure_automation", "scalability_planning"],
            "Azure": ["infrastructure_automation", "scalability_planning"]
        }
        
        capabilities = []
        for tech in technologies:
            if tech in tech_capability_map:
                capabilities.extend(tech_capability_map[tech])
        
        return list(set(capabilities))
    
    def _estimate_project_size(self, context: Dict[str, Any]) -> str:
        """Estime la taille du projet"""
        if not context:
            return "medium"
        
        files = context.get('files', [])
        if len(files) > 50:
            return "large"
        elif len(files) > 20:
            return "medium"
        else:
            return "small"
    
    def _assess_timeline_pressure(self, classification_result: HybridClassificationResult,
                                context: Dict[str, Any]) -> float:
        """Évalue la pression temporelle du projet"""
        base_pressure = 0.5
        
        # Ajustement selon la phase
        if classification_result.final_phase == "deployment":
            pressure = 0.8
        elif classification_result.final_phase == "testing":
            pressure = 0.7
        else:
            pressure = base_pressure
        
        # Contexte additionnel
        if context:
            if 'deadline' in context:
                pressure += 0.2
            if 'urgency' in context:
                pressure += 0.3
        
        return min(pressure, 1.0)
    
    def _assess_risk_level(self, classification_result: HybridClassificationResult,
                         context: Dict[str, Any]) -> float:
        """Évalue le niveau de risque du projet"""
        base_risk = 0.3
        
        # Ajustement selon la complexité
        complexity_risk = {
            "beginner": 0.1,
            "intermediate": 0.3,
            "advanced": 0.6,
            "expert": 0.8
        }.get(classification_result.final_complexity, 0.3)
        
        # Ajustement selon le domaine
        domain_risk = {
            "cybersecurity": 0.7,
            "devops": 0.5,
            "data_science": 0.4,
            "web_development": 0.3,
            "mobile_development": 0.4
        }.get(classification_result.final_domain, 0.3)
        
        final_risk = (complexity_risk + domain_risk) / 2
        return min(final_risk, 1.0)
    
    def _generate_evaluation_reasoning(self, target: RoutingTarget, 
                                     capability_score: float, performance_score: float,
                                     context_score: float, efficiency_score: float,
                                     collaboration_score: float, total_score: float) -> List[str]:
        """Génère le raisonnement de l'évaluation"""
        reasoning = []
        
        if capability_score > 0.8:
            reasoning.append("Excellente correspondance des capacités")
        elif capability_score > 0.6:
            reasoning.append("Bonne correspondance des capacités")
        else:
            reasoning.append("Correspondance limitée des capacités")
        
        if performance_score > 0.8:
            reasoning.append("Performance historique élevée")
        elif performance_score < 0.5:
            reasoning.append("Performance historique faible")
        
        if context_score > 0.8:
            reasoning.append("Contexte très favorable")
        elif context_score < 0.4:
            reasoning.append("Contexte défavorable")
        
        if efficiency_score > 0.8:
            reasoning.append("Excellente efficacité des ressources")
        elif efficiency_score < 0.5:
            reasoning.append("Efficacité limitée des ressources")
        
        if collaboration_score > 0.7:
            reasoning.append("Potentiel de collaboration élevé")
        
        reasoning.append(f"Score total: {total_score:.2f}")
        
        return reasoning
    
    def _update_selection_stats(self, selected_agents: List[AgentScore], 
                              selection_time: float, success: bool):
        """Met à jour les statistiques de sélection"""
        self.selection_stats['total_selections'] += 1
        self.selection_stats['average_selection_time'] += selection_time
        
        if success and selected_agents:
            self.selection_stats['successful_matches'] += 1
            
            # Mise à jour de l'usage des stratégies
            self.selection_stats['strategy_usage'][self.selection_strategy.value] += 1
            
            # Mise à jour de l'usage des capacités
            for agent in selected_agents:
                self.selection_stats['capability_usage'][agent.agent_id] += 1
    
    def get_selection_explanation(self, selected_agents: List[AgentScore]) -> Dict[str, Any]:
        """Génère une explication détaillée de la sélection"""
        if not selected_agents:
            return {'error': 'Aucun agent sélectionné'}
        
        return {
            'selection_summary': {
                'total_agents_selected': len(selected_agents),
                'selection_strategy': self.selection_strategy.value,
                'top_agent': selected_agents[0].agent_id,
                'average_score': statistics.mean([agent.total_score for agent in selected_agents])
            },
            'agent_details': [
                {
                    'agent_id': agent.agent_id,
                    'total_score': agent.total_score,
                    'capability_score': agent.capability_scores.get('main', 0.0),
                    'performance_score': agent.performance_metrics.get('performance', 0.0),
                    'collaboration_score': agent.collaboration_score,
                    'reasoning': agent.reasoning
                }
                for agent in selected_agents
            ],
            'selection_criteria': {
                'strategy_used': self.selection_strategy.value,
                'total_selections': self.selection_stats['total_selections'],
                'success_rate': (
                    self.selection_stats['successful_matches'] / 
                    max(self.selection_stats['total_selections'], 1)
                )
            }
        }
    
    def learn_from_performance(self, agent_selection: List[AgentScore], 
                             actual_performance: Dict[str, float]):
        """Apprend des performances réelles pour améliorer les sélections futures"""
        performance_entry = {
            'timestamp': time.time(),
            'selection': [agent.agent_id for agent in agent_selection],
            'expected_performance': [agent.total_score for agent in agent_selection],
            'actual_performance': actual_performance,
            'selection_strategy': self.selection_strategy.value
        }
        
        self.performance_history.append(performance_entry)
        
        # Garder seulement les 1000 dernières entrées
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]
        
        # Ajustement des poids de stratégie si nécessaire
        self._adjust_strategy_weights()
    
    def _adjust_strategy_weights(self):
        """Ajuste les poids des stratégies basé sur les performances historiques"""
        if len(self.performance_history) < 10:
            return
        
        # Analyse des performances par stratégie
        strategy_performance = defaultdict(list)
        
        for entry in self.performance_history[-100:]:  # Analyse des 100 dernières
            strategy = entry['selection_strategy']
            actual_perf = statistics.mean(list(entry['actual_performance'].values()))
            strategy_performance[strategy].append(actual_perf)
        
        # Si une stratégie performs significativement mieux, favoriser son usage
        if len(strategy_performance) > 1:
            best_strategy = max(strategy_performance.items(), 
                              key=lambda x: statistics.mean(x[1]))
            worst_strategy = min(strategy_performance.items(), 
                               key=lambda x: statistics.mean(x[1]))
            
            if statistics.mean(best_strategy[1]) - statistics.mean(worst_strategy[1]) > 0.2:
                self.logger.info(f"Stratégie {best_strategy[0]} surperforme, ajustement recommandé")
