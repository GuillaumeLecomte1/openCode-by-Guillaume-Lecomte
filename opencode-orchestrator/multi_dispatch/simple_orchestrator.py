#!/usr/bin/env python3
"""
Orchestrateur Multi-Dispatch Intelligent (Version Minimale)
Utilise seulement les composants existants pour une base fonctionnelle
"""

import logging
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import json
from concurrent.futures import ThreadPoolExecutor

# Imports des composants existants
from classifiers.keyword_classifier import KeywordClassifier
from classifiers.llm_classifier import LLMClassifier
from ..core.hybrid_fusion_simple import HybridFusionEngine, HybridClassificationResult
from ..core.routing_matrix import RoutingMatrix, RoutingDecision
from .agent_selector import IntelligentAgentSelector, AgentScore
from .dispatch_logic import IntelligentDispatchLogic, DispatchPlan, DispatchMode

class OrchestrationMode(Enum):
    """Modes d'orchestration disponibles"""
    STANDARD = "standard"
    INTELLIGENT = "intelligent"

@dataclass
class OrchestrationResult:
    """Résultat d'orchestration simplifié"""
    success: bool
    classification: Optional[HybridClassificationResult]
    routing_decision: Optional[RoutingDecision]
    agent_selection: List[AgentScore]
    dispatch_plan: Optional[DispatchPlan]
    execution_results: Dict[str, Any]
    final_output: Dict[str, Any]
    execution_time: float
    quality_metrics: Dict[str, float]

class SimpleMultiDispatchOrchestrator:
    """Orchestrateur multi-dispatch intelligent (version minimale fonctionnelle)"""
    
    def __init__(self, mode: OrchestrationMode = OrchestrationMode.INTELLIGENT):
        self.mode = mode
        self.logger = logging.getLogger(__name__)
        
        # Initialisation des composants
        self.keyword_classifier = KeywordClassifier()
        self.llm_classifier = LLMClassifier()
        self.hybrid_fusion = HybridFusionEngine()
        self.routing_matrix = RoutingMatrix()
        
        # Composants multi-dispatch
        self.agent_selector = IntelligentAgentSelector()
        self.dispatch_logic = IntelligentDispatchLogic()
        
        # Thread pool pour l'exécution
        self.thread_pool = ThreadPoolExecutor(max_workers=10)
        
        # Statistiques
        self.stats = {
            'total_orchestrations': 0,
            'successful_orchestrations': 0,
            'average_execution_time': 0.0
        }
        
        self.logger.info("Simple Multi-Dispatch Orchestrator initialisé")
    
    def orchestrate(self, 
                   project_text: str,
                   project_context: Optional[Dict[str, Any]] = None,
                   task_executor: Optional[Callable] = None) -> OrchestrationResult:
        """
        Orchestration principale
        
        Args:
            project_text: Texte du projet à analyser
            project_context: Contexte additionnel du projet
            task_executor: Fonction d'exécution des tâches
        
        Returns:
            OrchestrationResult complet
        """
        
        start_time = time.time()
        project_context = project_context or {}
        
        try:
            self.logger.info("Début de l'orchestration multi-dispatch")
            
            # Phase 1: Classification hybride
            classification_result = self._perform_classification(project_text, project_context)
            
            # Phase 2: Routage intelligent
            routing_decision = self._perform_routing(classification_result, project_context)
            
            # Phase 3: Sélection d'agents
            agent_selection = self._select_agents(classification_result, project_context)
            
            # Phase 4: Création du plan de dispatch
            dispatch_plan = self._create_dispatch_plan(agent_selection, classification_result, project_context)
            
            # Phase 5: Exécution du dispatch
            execution_results = self._execute_dispatch(dispatch_plan, task_executor)
            
            # Phase 6: Génération du output final
            final_output = self._generate_output(classification_result, routing_decision, execution_results)
            
            # Mise à jour des statistiques
            self.stats['total_orchestrations'] += 1
            self.stats['successful_orchestrations'] += 1
            self.stats['average_execution_time'] += time.time() - start_time
            
            result = OrchestrationResult(
                success=True,
                classification=classification_result,
                routing_decision=routing_decision,
                agent_selection=agent_selection,
                dispatch_plan=dispatch_plan,
                execution_results=execution_results,
                final_output=final_output,
                execution_time=time.time() - start_time,
                quality_metrics=self._calculate_quality_metrics(classification_result, execution_results)
            )
            
            self.logger.info(f"Orchestration terminée avec succès en {result.execution_time:.2f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'orchestration: {e}")
            
            # Mise à jour des statistiques
            self.stats['total_orchestrations'] += 1
            
            return OrchestrationResult(
                success=False,
                classification=None,
                routing_decision=None,
                agent_selection=[],
                dispatch_plan=None,
                execution_results={},
                final_output={'error': str(e)},
                execution_time=time.time() - start_time,
                quality_metrics={}
            )
    
    def _perform_classification(self, project_text: str, project_context: Dict[str, Any]) -> HybridClassificationResult:
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
    
    def _perform_routing(self, classification_result: HybridClassificationResult, project_context: Dict[str, Any]) -> RoutingDecision:
        """Exécute le routage intelligent"""
        
        self.logger.info("Phase 2: Routage intelligent")
        
        routing_decision = self.routing_matrix.route_project(classification_result, project_context)
        
        return routing_decision
    
    def _select_agents(self, classification_result: HybridClassificationResult, project_context: Dict[str, Any]) -> List[AgentScore]:
        """Sélectionne les agents optimaux"""
        
        self.logger.info("Phase 3: Sélection d'agents")
        
        agent_selection = self.agent_selector.select_agents(classification_result, project_context)
        
        self.logger.info(f"Sélection de {len(agent_selection)} agents")
        return agent_selection
    
    def _create_dispatch_plan(self, agent_selection: List[AgentScore], classification_result: HybridClassificationResult, project_context: Dict[str, Any]) -> DispatchPlan:
        """Crée le plan de dispatch"""
        
        self.logger.info("Phase 4: Création du plan de dispatch")
        
        dispatch_plan = self.dispatch_logic.create_dispatch_plan(agent_selection, classification_result, project_context)
        
        self.logger.info(f"Plan créé: mode {dispatch_plan.mode.value} avec {len(dispatch_plan.tasks)} tâches")
        return dispatch_plan
    
    def _execute_dispatch(self, dispatch_plan: DispatchPlan, task_executor: Optional[Callable] = None) -> Dict[str, Any]:
        """Exécute le dispatch"""
        
        self.logger.info("Phase 5: Exécution du dispatch")
        
        executor = task_executor if task_executor is not None else self._default_task_executor
        task_results = self.dispatch_logic.execute_dispatch_plan(dispatch_plan, executor)
        
        return {'task_results': task_results}
    
    def _generate_output(self, classification_result: HybridClassificationResult, routing_decision: RoutingDecision, execution_results: Dict[str, Any]) -> Dict[str, Any]:
        """Génère le output final"""
        
        # Fusion simple des résultats de tâches
        fused_output = self._simple_fusion(execution_results['task_results'])
        
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
                'failed_tasks': len([r for r in execution_results['task_results'] if not r.success])
            },
            'results': fused_output,
            'quality_assessment': {
                'classification_confidence': classification_result.fusion_confidence,
                'execution_success_rate': len([r for r in execution_results['task_results'] if r.success]) / len(execution_results['task_results']) if execution_results['task_results'] else 0.0
            }
        }
    
    def _simple_fusion(self, task_results: List[Any]) -> Dict[str, Any]:
        """Fusion simple des résultats"""
        
        if not task_results:
            return {}
        
        fused = {}
        
        for result in task_results:
            if hasattr(result, 'output_data') and result.output_data:
                if isinstance(result.output_data, dict):
                    for key, value in result.output_data.items():
                        if key not in fused:
                            fused[key] = []
                        fused[key].append(value)
                else:
                    # Si c'est un simple résultat, l'ajouter directement
                    if 'results' not in fused:
                        fused['results'] = []
                    fused['results'].append(result.output_data)
        
        # Simplifier les listes en valeurs uniques si possible
        for key, value in fused.items():
            if isinstance(value, list) and len(value) == 1:
                fused[key] = value[0]
        
        return fused
    
    def _calculate_quality_metrics(self, classification_result: HybridClassificationResult, execution_results: Dict[str, Any]) -> Dict[str, float]:
        """Calcule les métriques de qualité"""
        
        task_results = execution_results['task_results']
        successful_tasks = len([r for r in task_results if r.success]) if task_results else 0
        total_tasks = len(task_results) if task_results else 0
        
        return {
            'classification_confidence': classification_result.fusion_confidence,
            'execution_success_rate': successful_tasks / total_tasks if total_tasks > 0 else 0.0,
            'overall_quality': (
                classification_result.fusion_confidence * 0.6 +
                (successful_tasks / total_tasks) * 0.4
            ) if total_tasks > 0 else classification_result.fusion_confidence
        }
    
    def _default_task_executor(self, task) -> Any:
        """Exécuteur de tâches par défaut"""
        import random
        import time
        
        execution_time = random.uniform(1, 3)
        time.sleep(execution_time)
        
        success = random.random() > 0.1  # 90% de succès
        
        # Créer un objet résultat compatible avec TaskResult
        class TaskResult:
            def __init__(self, task_id, agent_id, success, output_data, execution_time):
                self.task_id = task_id
                self.agent_id = agent_id
                self.success = success
                self.output_data = output_data
                self.execution_time = execution_time
        
        return TaskResult(
            task_id=task.task_id,
            agent_id=task.agent_id,
            success=success,
            output_data={
                'result': f"Résultat de {task.task_id}",
                'status': 'completed' if success else 'failed',
                'execution_time': execution_time
            },
            execution_time=execution_time
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retourne les statistiques"""
        stats = self.stats.copy()
        
        if stats['total_orchestrations'] > 0:
            stats['success_rate'] = stats['successful_orchestrations'] / stats['total_orchestrations']
            stats['average_execution_time'] = stats['average_execution_time'] / stats['total_orchestrations']
        
        return stats

def create_orchestrator(mode: OrchestrationMode = OrchestrationMode.INTELLIGENT) -> SimpleMultiDispatchOrchestrator:
    """Factory function pour créer un orchestrateur"""
    return SimpleMultiDispatchOrchestrator(mode)