#!/usr/bin/env python3
"""
Orchestrateur Principal Multi-Dispatch (Version Simplifiée)
Point d'entrée principal pour la coordination intelligente multi-agents
"""

import logging
import time
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

# Imports des composants existants
from classifiers.keyword_classifier import KeywordClassifier
from classifiers.llm_classifier import LLMClassifier
from core.hybrid_fusion import HybridFusionEngine, HybridClassificationResult
from core.routing_matrix import RoutingMatrix, RoutingDecision

# Imports des nouveaux composants multi-dispatch
from .agent_selector import IntelligentAgentSelector, AgentScore
from .dispatch_logic import IntelligentDispatchLogic, DispatchPlan, DispatchMode
from .result_fusion import IntelligentResultAggregator, FusionResult
from .dispatch_mode_selector import DispatchModeSelector, DispatchRecommendation

class OrchestrationMode(Enum):
    """Modes d'orchestration disponibles"""
    STANDARD = "standard"
    INTELLIGENT = "intelligent"
    ADAPTIVE = "adaptive"
    EMERGENCY = "emergency"

class OrchestrationStrategy(Enum):
    """Stratégies d'orchestration"""
    PERFORMANCE_OPTIMIZED = "performance_optimized"
    QUALITY_FOCUSED = "quality_focused"
    RESOURCE_EFFICIENT = "resource_efficient"
    BALANCED = "balanced"

@dataclass
class OrchestrationContext:
    """Contexte d'orchestration"""
    project_text: str
    project_context: Dict[str, Any]
    user_constraints: Dict[str, Any]
    performance_requirements: Dict[str, float]
    quality_requirements: Dict[str, float]
    timeline_constraints: Optional[Dict[str, Any]] = None
    resource_constraints: Optional[Dict[str, Any]] = None

@dataclass
class OrchestrationResult:
    """Résultat d'orchestration complet"""
    success: bool
    classification: Optional[HybridClassificationResult]
    routing_decision: Optional[RoutingDecision]
    agent_selection: List[AgentScore]
    dispatch_plan: Optional[DispatchPlan]
    fusion_result: Optional[FusionResult]
    final_output: Dict[str, Any]
    orchestration_metadata: Dict[str, Any]
    execution_time: float
    quality_metrics: Dict[str, float]
    error_details: Optional[Dict[str, Any]] = None

class PrimaryMultiDispatchOrchestrator:
    """Orchestrateur principal multi-dispatch intelligent"""
    
    def __init__(self, 
                 orchestration_mode: OrchestrationMode = OrchestrationMode.INTELLIGENT,
                 orchestration_strategy: OrchestrationStrategy = OrchestrationStrategy.BALANCED):
        
        self.orchestration_mode = orchestration_mode
        self.orchestration_strategy = orchestration_strategy
        self.logger = logging.getLogger(__name__)
        
        # Initialisation des composants principaux
        self._initialize_core_components()
        self._initialize_multi_dispatch_components()
        
        # Pool d'exécuteurs
        self.thread_pool = ThreadPoolExecutor(max_workers=10)
        
        # Métriques globales
        self.orchestration_stats = {
            'total_orchestrations': 0,
            'successful_orchestrations': 0,
            'failed_orchestrations': 0,
            'average_execution_time': 0.0,
            'mode_usage': {mode.value: 0 for mode in OrchestrationMode},
            'strategy_usage': {strategy.value: 0 for strategy in OrchestrationStrategy},
            'quality_scores': [],
            'performance_scores': []
        }
        
        self.logger.info("Primary Multi-Dispatch Orchestrator initialisé")
    
    def _initialize_core_components(self):
        """Initialise les composants core existants"""
        
        # Classificateurs
        self.keyword_classifier = KeywordClassifier()
        self.llm_classifier = LLMClassifier()
        
        # Moteur de fusion hybride
        self.hybrid_fusion = HybridFusionEngine()
        
        # Matrice de routage
        self.routing_matrix = RoutingMatrix()
        
        self.logger.info("Composants core initialisés")
    
    def _initialize_multi_dispatch_components(self):
        """Initialise les nouveaux composants multi-dispatch"""
        
        # Sélecteur d'agents intelligent
        self.agent_selector = IntelligentAgentSelector()
        
        # Logique de dispatch intelligente
        self.dispatch_logic = IntelligentDispatchLogic()
        
        # Agrégateur de résultats
        self.result_aggregator = IntelligentResultAggregator()
        
        # Sélecteur de mode de dispatch
        self.dispatch_mode_selector = DispatchModeSelector()
        
        self.logger.info("Composants multi-dispatch initialisés")
    
    def orchestrate(self, 
                   project_text: str,
                   project_context: Dict[str, Any] = None,
                   user_constraints: Dict[str, Any] = None,
                   task_executor: Callable = None) -> OrchestrationResult:
        """
        Orchestration principale multi-dispatch
        
        Args:
            project_text: Texte du projet à analyser
            project_context: Contexte additionnel du projet
            user_constraints: Contraintes utilisateur
            task_executor: Fonction d'exécution des tâches
        
        Returns:
            OrchestrationResult complet
        """
        
        start_time = time.time()
        context = OrchestrationContext(
            project_text=project_text,
            project_context=project_context or {},
            user_constraints=user_constraints or {},
            performance_requirements=self._extract_performance_requirements(project_context),
            quality_requirements=self._extract_quality_requirements(project_context)
        )
        
        try:
            self.logger.info("Début de l'orchestration multi-dispatch")
            
            # Phase 1: Classification hybride
            classification_result = self._perform_hybrid_classification(
                project_text, project_context
            )
            
            # Phase 2: Routage intelligent
            routing_decision = self._perform_intelligent_routing(
                classification_result, project_context
            )
            
            # Phase 3: Sélection d'agents
            agent_selection = self._perform_agent_selection(
                classification_result, project_context
            )
            
            # Phase 4: Sélection du mode de dispatch
            dispatch_recommendation = self._select_dispatch_mode(
                agent_selection, classification_result, project_context
            )
            
            # Phase 5: Planification du dispatch
            dispatch_plan = self._create_dispatch_plan(
                agent_selection, classification_result, project_context, dispatch_recommendation
            )
            
            # Phase 6: Exécution coordonnée
            execution_results = self._execute_coordinated_dispatch(
                dispatch_plan, task_executor, project_context
            )
            
            # Phase 7: Fusion des résultats
            fusion_result = self._perform_intelligent_fusion(
                execution_results, agent_selection, dispatch_plan, project_context
            )
            
            # Phase 8: Génération du résultat final
            final_output = self._generate_final_output(
                classification_result, routing_decision, fusion_result, 
                execution_results, project_context
            )
            
            # Compilation du résultat d'orchestration
            orchestration_result = OrchestrationResult(
                success=True,
                classification=classification_result,
                routing_decision=routing_decision,
                agent_selection=agent_selection,
                dispatch_plan=dispatch_plan,
                fusion_result=fusion_result,
                final_output=final_output,
                orchestration_metadata=self._generate_orchestration_metadata(
                    classification_result, agent_selection, dispatch_plan, fusion_result
                ),
                execution_time=time.time() - start_time,
                quality_metrics=self._calculate_quality_metrics(
                    classification_result, fusion_result, execution_results
                )
            )
            
            # Mise à jour des statistiques
            self._update_orchestration_stats(orchestration_result, True)
            
            self.logger.info(f"Orchestration terminée avec succès en {time.time() - start_time:.2f}s")
            return orchestration_result
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'orchestration: {e}")
            
            # Gestion d'erreur
            error_result = self._handle_orchestration_error(
                e, context, time.time() - start_time
            )
            
            self._update_orchestration_stats(error_result, False)
            return error_result
    
    def _perform_hybrid_classification(self, 
                                     project_text: str, 
                                     project_context: Dict[str, Any]) -> HybridClassificationResult:
        """Exécute la classification hybride"""
        
        self.logger.info("Phase 1: Classification hybride")
        
        # Classification par mots-clés
        keyword_result = self.keyword_classifier.classify(project_text, project_context)
        
        # Classification LLM
        llm_result = self.llm_classifier.classify(project_text, project_context)
        
        # Fusion hybride
        fusion_result = self.hybrid_fusion._fuse_results(
            keyword_result, llm_result, project_text, project_context
        )
        
        return fusion_result
    
    def _perform_intelligent_routing(self,
                                   classification_result: HybridClassificationResult,
                                   project_context: Dict[str, Any]) -> RoutingDecision:
        """Exécute le routage intelligent"""
        
        self.logger.info("Phase 2: Routage intelligent")
        
        routing_decision = self.routing_matrix.route_project(
            classification_result, project_context
        )
        
        return routing_decision
    
    def _perform_agent_selection(self,
                               classification_result: HybridClassificationResult,
                               project_context: Dict[str, Any]) -> List[AgentScore]:
        """Exécute la sélection d'agents intelligente"""
        
        self.logger.info("Phase 3: Sélection d'agents")
        
        agent_selection = self.agent_selector.select_agents(
            classification_result, project_context
        )
        
        self.logger.info(f"Sélection de {len(agent_selection)} agents")
        return agent_selection
    
    def _select_dispatch_mode(self,
                            agent_selection: List[AgentScore],
                            classification_result: HybridClassificationResult,
                            project_context: Dict[str, Any]) -> DispatchRecommendation:
        """Sélectionne le mode de dispatch optimal"""
        
        self.logger.info("Phase 4: Sélection du mode de dispatch")
        
        dispatch_recommendation = self.dispatch_mode_selector.select_optimal_mode(
            agent_selection, classification_result, project_context
        )
        
        self.logger.info(f"Mode sélectionné: {dispatch_recommendation.recommended_mode.value}")
        return dispatch_recommendation
    
    def _create_dispatch_plan(self,
                            agent_selection: List[AgentScore],
                            classification_result: HybridClassificationResult,
                            project_context: Dict[str, Any],
                            dispatch_recommendation: DispatchRecommendation) -> DispatchPlan:
        """Crée le plan de dispatch intelligent"""
        
        self.logger.info("Phase 5: Planification du dispatch")
        
        dispatch_plan = self.dispatch_logic.create_dispatch_plan(
            agent_selection, classification_result, project_context
        )
        
        # Override du mode si nécessaire
        if dispatch_recommendation.recommended_mode != dispatch_plan.mode:
            self.logger.info(f"Override du mode: {dispatch_plan.mode.value} → {dispatch_recommendation.recommended_mode.value}")
            dispatch_plan.mode = dispatch_recommendation.recommended_mode
        
        self.logger.info(f"Plan créé: mode {dispatch_plan.mode.value} avec {len(dispatch_plan.tasks)} tâches")
        return dispatch_plan
    
    def _execute_coordinated_dispatch(self,
                                    dispatch_plan: DispatchPlan,
                                    task_executor: Callable,
                                    project_context: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute le dispatch coordonné"""
        
        self.logger.info("Phase 6: Exécution coordonnée")
        
        # Exécution du plan
        task_results = self.dispatch_logic.execute_dispatch_plan(
            dispatch_plan, task_executor or self._default_task_executor
        )
        
        return {
            'task_results': task_results,
            'execution_id': f"exec_{dispatch_plan.dispatch_id}"
        }
    
    def _perform_intelligent_fusion(self,
                                  execution_results: Dict[str, Any],
                                  agent_selection: List[AgentScore],
                                  dispatch_plan: DispatchPlan,
                                  project_context: Dict[str, Any]) -> FusionResult:
        """Exécute la fusion intelligente des résultats"""
        
        self.logger.info("Phase 7: Fusion intelligente")
        
        fusion_result = self.result_aggregator.fuse_results(
            execution_results['task_results'],
            agent_selection,
            dispatch_plan,
            project_context
        )
        
        self.logger.info(f"Fusion terminée avec score de qualité: {fusion_result.quality_score:.2f}")
        return fusion_result
    
    def _generate_final_output(self,
                             classification_result: HybridClassificationResult,
                             routing_decision: RoutingDecision,
                             fusion_result: FusionResult,
                             execution_results: Dict[str, Any],
                             project_context: Dict[str, Any]) -> Dict[str, Any]:
        """Génère le output final"""
        
        return {
            'project_analysis': {
                'domain': classification_result.final_domain,
                'type': classification_result.final_type,
                'complexity': classification_result.final_complexity,
                'phase': classification_result.final_phase,
                'confidence': classification_result.fusion_confidence
            },
            'routing': {
                'target': routing_decision.target.name if routing_decision else None,
                'confidence': routing_decision.confidence if routing_decision else None
            },
            'execution_summary': {
                'total_tasks': len(execution_results['task_results']),
                'successful_tasks': len([r for r in execution_results['task_results'] if r.success]),
                'failed_tasks': len([r for r in execution_results['task_results'] if not r.success]),
                'execution_id': execution_results['execution_id']
            },
            'results': fusion_result.fused_output,
            'quality_assessment': {
                'overall_quality': fusion_result.quality_score,
                'confidence_score': fusion_result.confidence_score,
                'conflicts_resolved': len(fusion_result.conflict_resolutions)
            },
            'recommendations': fusion_result.fused_output.get('recommendations', [])
        }
    
    def _generate_orchestration_metadata(self,
                                       classification_result: HybridClassificationResult,
                                       agent_selection: List[AgentScore],
                                       dispatch_plan: DispatchPlan,
                                       fusion_result: FusionResult) -> Dict[str, Any]:
        """Génère les métadonnées d'orchestration"""
        
        return {
            'orchestration_mode': self.orchestration_mode.value,
            'orchestration_strategy': self.orchestration_strategy.value,
            'classification_method': classification_result.fusion_method,
            'dispatch_mode': dispatch_plan.mode.value,
            'fusion_strategy': fusion_result.fusion_metadata.get('fusion_strategy', 'unknown'),
            'agents_count': len(agent_selection),
            'tasks_count': len(dispatch_plan.tasks),
            'execution_levels': len(dispatch_plan.execution_order),
            'conflict_resolutions': len(fusion_result.conflict_resolutions),
            'contributing_agents': fusion_result.contributing_agents,
            'timestamp': time.time()
        }
    
    def _calculate_quality_metrics(self,
                                 classification_result: HybridClassificationResult,
                                 fusion_result: FusionResult,
                                 execution_results: Dict[str, Any]) -> Dict[str, float]:
        """Calcule les métriques de qualité"""
        
        task_results = execution_results['task_results']
        successful_tasks = len([r for r in task_results if r.success])
        
        return {
            'classification_confidence': classification_result.fusion_confidence,
            'fusion_quality': fusion_result.quality_score,
            'execution_success_rate': successful_tasks / len(task_results) if task_results else 0.0,
            'overall_quality': (
                classification_result.fusion_confidence * 0.3 +
                fusion_result.quality_score * 0.4 +
                (successful_tasks / len(task_results)) * 0.3
            ) if task_results else 0.0
        }
    
    def _default_task_executor(self, task) -> Dict[str, Any]:
        """Exécuteur de tâches par défaut pour démonstration"""
        import random
        import time
        
        # Simulation d'exécution
        execution_time = random.uniform(1, 5)
        time.sleep(execution_time)
        
        success = random.random() > 0.1  # 90% de succès
        
        return {
            'task_id': task.task_id,
            'agent_id': task.agent_id,
            'success': success,
            'output_data': {
                'result': f"Résultat de {task.task_id}",
                'status': 'completed' if success else 'failed',
                'execution_time': execution_time
            },
            'execution_time': execution_time
        }
    
    def _extract_performance_requirements(self, project_context: Dict[str, Any]) -> Dict[str, float]:
        """Extrait les exigences de performance"""
        return project_context.get('performance_requirements', {
            'max_execution_time': 300.0,  # 5 minutes
            'min_success_rate': 0.8,
            'max_concurrent_tasks': 5
        })
    
    def _extract_quality_requirements(self, project_context: Dict[str, Any]) -> Dict[str, float]:
        """Extrait les exigences de qualité"""
        return project_context.get('quality_requirements', {
            'min_classification_confidence': 0.6,
            'min_fusion_quality': 0.7,
            'min_agent_score': 0.5
        })
    
    def _handle_orchestration_error(self,
                                  error: Exception,
                                  context: OrchestrationContext,
                                  execution_time: float) -> OrchestrationResult:
        """Gère les erreurs d'orchestration"""
        
        self.logger.error(f"Erreur d'orchestration: {error}")
        
        return OrchestrationResult(
            success=False,
            classification=None,
            routing_decision=None,
            agent_selection=[],
            dispatch_plan=None,
            fusion_result=None,
            final_output={'error': str(error)},
            orchestration_metadata={
                'error_type': type(error).__name__,
                'error_message': str(error),
                'execution_time': execution_time,
                'orchestration_mode': self.orchestration_mode.value
            },
            execution_time=execution_time,
            quality_metrics={},
            error_details={
                'error_type': type(error).__name__,
                'error_message': str(error)
            }
        )
    
    def _update_orchestration_stats(self, result: OrchestrationResult, success: bool):
        """Met à jour les statistiques d'orchestration"""
        self.orchestration_stats['total_orchestrations'] += 1
        
        if success:
            self.orchestration_stats['successful_orchestrations'] += 1
            self.orchestration_stats['quality_scores'].append(
                result.quality_metrics.get('overall_quality', 0.0)
            )
            self.orchestration_stats['mode_usage'][self.orchestration_mode.value] += 1
            self.orchestration_stats['strategy_usage'][self.orchestration_strategy.value] += 1
        else:
            self.orchestration_stats['failed_orchestrations'] += 1
        
        self.orchestration_stats['average_execution_time'] += result.execution_time
    
    def get_orchestration_statistics(self) -> Dict[str, Any]:
        """Retourne les statistiques d'orchestration"""
        stats = self.orchestration_stats.copy()
        
        # Calculs additionnels
        if stats['total_orchestrations'] > 0:
            stats['success_rate'] = stats['successful_orchestrations'] / stats['total_orchestrations']
            stats['average_quality'] = (
                sum(stats['quality_scores']) / len(stats['quality_scores'])
                if stats['quality_scores'] else 0.0
            )
            stats['average_execution_time'] = stats['average_execution_time'] / stats['total_orchestrations']
        
        return stats
    
    def export_orchestration_report(self, filename: str = None) -> Dict[str, Any]:
        """Exporte un rapport d'orchestration"""
        
        report = {
            'orchestration_summary': {
                'mode': self.orchestration_mode.value,
                'strategy': self.orchestration_strategy.value,
                'statistics': self.get_orchestration_statistics()
            },
            'component_status': {
                'agent_selector': 'active',
                'dispatch_logic': 'active',
                'result_aggregator': 'active',
                'dispatch_mode_selector': 'active'
            },
            'performance_metrics': {
                'throughput': self._calculate_throughput(),
                'quality_trend': self._calculate_quality_trend(),
                'error_rate': self._calculate_error_rate()
            },
            'timestamp': time.time()
        }
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Rapport exporté vers {filename}")
        
        return report
    
    def _calculate_throughput(self) -> float:
        """Calcule le throughput (orchestrations par minute)"""
        # Implémentation simplifiée
        return self.orchestration_stats['total_orchestrations'] / max(
            (time.time() - self.orchestration_stats.get('start_time', time.time())) / 60, 1
        )
    
    def _calculate_quality_trend(self) -> List[float]:
        """Calcule la tendance de qualité"""
        return self.orchestration_stats['quality_scores'][-10:]  # 10 dernières valeurs
    
    def _calculate_error_rate(self) -> float:
        """Calcule le taux d'erreur"""
        total = self.orchestration_stats['total_orchestrations']
        if total == 0:
            return 0.0
        return self.orchestration_stats['failed_orchestrations'] / total

# Fonction utilitaire pour créer l'orchestrateur
def create_intelligent_orchestrator(mode: OrchestrationMode = OrchestrationMode.INTELLIGENT,
                                   strategy: OrchestrationStrategy = OrchestrationStrategy.BALANCED) -> PrimaryMultiDispatchOrchestrator:
    """Factory function pour créer un orchestrateur intelligent"""
    return PrimaryMultiDispatchOrchestrator(mode, strategy)