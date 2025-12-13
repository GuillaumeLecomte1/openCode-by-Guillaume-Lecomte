#!/usr/bin/env python3
"""
Orchestrateur Multi-Dispatch Minimal (Version Fonctionnelle)
Coordination basique des composants existants
"""

import logging
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum

# Imports des composants existants
from classifiers.keyword_classifier import KeywordClassifier
from classifiers.llm_classifier import LLMClassifier
from core.routing_matrix import RoutingMatrix, RoutingDecision
from multi_dispatch.agent_selector import IntelligentAgentSelector, AgentScore
from multi_dispatch.dispatch_logic import IntelligentDispatchLogic, DispatchPlan, DispatchMode

class OrchestrationMode(Enum):
    STANDARD = "standard"
    INTELLIGENT = "intelligent"

@dataclass
class MinimalOrchestrationResult:
    """Résultat d'orchestration minimal"""
    success: bool
    keyword_classification: Dict[str, Any]
    llm_classification: Dict[str, Any]
    routing_decision: Optional[RoutingDecision]
    agent_selection: List[AgentScore]
    dispatch_plan: Optional[DispatchPlan]
    execution_results: Dict[str, Any]
    final_output: Dict[str, Any]
    execution_time: float

class MinimalMultiDispatchOrchestrator:
    """Orchestrateur multi-dispatch minimal fonctionnel"""
    
    def __init__(self, mode: OrchestrationMode = OrchestrationMode.INTELLIGENT):
        self.mode = mode
        self.logger = logging.getLogger(__name__)
        
        # Initialisation des composants
        self.keyword_classifier = KeywordClassifier()
        self.llm_classifier = LLMClassifier()
        self.routing_matrix = RoutingMatrix()
        self.agent_selector = IntelligentAgentSelector()
        self.dispatch_logic = IntelligentDispatchLogic()
        
        self.logger.info("Minimal Multi-Dispatch Orchestrator initialisé")
    
    def orchestrate(self, 
                   project_text: str,
                   project_context: Dict[str, Any] = None,
                   task_executor: Callable = None) -> MinimalOrchestrationResult:
        """
        Orchestration principale minimal
        """
        
        start_time = time.time()
        project_context = project_context or {}
        
        try:
            self.logger.info("Début de l'orchestration minimal")
            
            # Phase 1: Classification par mots-clés
            keyword_result = self.keyword_classifier.classify(project_text, project_context)
            
            # Phase 2: Classification LLM
            llm_result = self.llm_classifier.classify(project_text, project_context)
            
            # Phase 3: Création d'un résultat hybride simplifié
            hybrid_result = self._create_simple_hybrid_result(keyword_result, llm_result)
            
            # Phase 4: Routage
            routing_decision = self.routing_matrix.route_project(hybrid_result, project_context)
            
            # Phase 5: Sélection d'agents
            agent_selection = self.agent_selector.select_agents(hybrid_result, project_context)
            
            # Phase 6: Plan de dispatch
            dispatch_plan = self.dispatch_logic.create_dispatch_plan(agent_selection, hybrid_result, project_context)
            
            # Phase 7: Exécution
            execution_results = self._execute_dispatch(dispatch_plan, task_executor)
            
            # Phase 8: Génération du output
            final_output = self._generate_output(keyword_result, llm_result, routing_decision, execution_results)
            
            result = MinimalOrchestrationResult(
                success=True,
                keyword_classification=keyword_result.__dict__,
                llm_classification=llm_result.__dict__,
                routing_decision=routing_decision,
                agent_selection=agent_selection,
                dispatch_plan=dispatch_plan,
                execution_results=execution_results,
                final_output=final_output,
                execution_time=time.time() - start_time
            )
            
            self.logger.info(f"Orchestration terminée en {result.execution_time:.2f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'orchestration: {e}")
            
            return MinimalOrchestrationResult(
                success=False,
                keyword_classification={},
                llm_classification={},
                routing_decision=None,
                agent_selection=[],
                dispatch_plan=None,
                execution_results={},
                final_output={'error': str(e)},
                execution_time=time.time() - start_time
            )
    
    def _create_simple_hybrid_result(self, keyword_result, llm_result):
        """Crée un résultat hybride simplifié compatible"""
        
        class SimpleHybridResult:
            def __init__(self, keyword_result, llm_result):
                self.final_domain = llm_result.domain if hasattr(llm_result, 'domain') else 'unknown'
                self.final_type = getattr(llm_result, 'type', 'unknown')
                self.final_complexity = getattr(llm_result, 'complexity', 'unknown')
                self.final_phase = getattr(llm_result, 'phase', 'unknown')
                self.fusion_confidence = getattr(llm_result, 'overall_confidence', 0.5)
                self.domain = keyword_result.domain
                self.type = keyword_result.type
                self.complexity = keyword_result.complexity
                self.phase = keyword_result.phase
        
        return SimpleHybridResult(keyword_result, llm_result)
    
    def _execute_dispatch(self, dispatch_plan: DispatchPlan, task_executor: Callable = None) -> Dict[str, Any]:
        """Exécute le dispatch"""
        
        if task_executor is None:
            task_executor = self._default_task_executor
        
        task_results = self.dispatch_logic.execute_dispatch_plan(dispatch_plan, task_executor)
        return {'task_results': task_results}
    
    def _generate_output(self, keyword_result, llm_result, routing_decision, execution_results) -> Dict[str, Any]:
        """Génère le output final"""
        
        return {
            'project_analysis': {
                'keyword_domain': max(keyword_result.domain.items(), key=lambda x: x[1])[0] if keyword_result.domain else 'unknown',
                'llm_domain': getattr(llm_result, 'domain', 'unknown'),
                'final_domain': getattr(llm_result, 'domain', 'unknown'),
                'confidence': getattr(llm_result, 'overall_confidence', 0.0)
            },
            'routing': {
                'target': routing_decision.target.name if routing_decision else None,
                'confidence': routing_decision.confidence if routing_decision else None
            },
            'execution_summary': {
                'total_tasks': len(execution_results['task_results']),
                'successful_tasks': len([r for r in execution_results['task_results'] if r.success]),
                'mode': execution_results['task_results'][0].task_id.split('_')[0] if execution_results['task_results'] else 'unknown'
            },
            'results': {
                'keyword_classification': keyword_result.__dict__,
                'llm_classification': llm_result.__dict__
            }
        }
    
    def _default_task_executor(self, task):
        """Exécuteur de tâches par défaut"""
        import random
        import time
        
        execution_time = random.uniform(1, 3)
        time.sleep(execution_time)
        
        success = random.random() > 0.1  # 90% de succès
        
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

def create_minimal_orchestrator(mode: OrchestrationMode = OrchestrationMode.INTELLIGENT) -> MinimalMultiDispatchOrchestrator:
    """Factory function pour créer un orchestrateur minimal"""
    return MinimalMultiDispatchOrchestrator(mode)