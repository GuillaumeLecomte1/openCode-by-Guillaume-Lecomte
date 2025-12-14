#!/usr/bin/env python3
"""
Orchestrateur Principal Simplifié pour OpenCode
Version simplifiée qui fonctionne avec la configuration opencode existante
"""

import logging
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import json

# Imports des composants existants
try:
    from classifiers.keyword_classifier import KeywordClassifier
    from classifiers.llm_classifier import LLMClassifier
    from core.hybrid_fusion import HybridFusionEngine, HybridClassificationResult
    from core.routing_matrix import RoutingMatrix, RoutingDecision
except ImportError:
    # Fallback si les modules ne sont pas disponibles
    class HybridClassificationResult:
        def __init__(self):
            self.final_domain = "general"
            self.final_type = "development"
            self.final_complexity = "moderate"
            self.final_phase = "planning"
            self.fusion_confidence = 0.8
    
    class RoutingDecision:
        def __init__(self):
            self.target = None
            self.confidence = 0.8

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
    agent_selection: List[str]
    dispatch_plan: Optional[Dict[str, Any]]
    final_output: Dict[str, Any]
    orchestration_metadata: Dict[str, Any]
    execution_time: float
    quality_metrics: Dict[str, float]
    error_details: Optional[Dict[str, Any]] = None

class PrimaryOrchestrator:
    """Orchestrateur principal simplifié pour opencode"""
    
    def __init__(self, 
                 orchestration_mode: OrchestrationMode = OrchestrationMode.INTELLIGENT,
                 orchestration_strategy: OrchestrationStrategy = OrchestrationStrategy.BALANCED):
        
        self.orchestration_mode = orchestration_mode
        self.orchestration_strategy = orchestration_strategy
        self.logger = logging.getLogger(__name__)
        
        # Initialisation des composants principaux (avec fallback)
        self._initialize_components()
        
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
        
        self.logger.info("Primary Orchestrator initialisé")
    
    def _initialize_components(self):
        """Initialise les composants avec fallback"""
        
        try:
            # Classificateurs
            self.keyword_classifier = KeywordClassifier()
            self.llm_classifier = LLMClassifier()
            
            # Moteur de fusion hybride
            self.hybrid_fusion = HybridFusionEngine()
            
            # Matrice de routage
            self.routing_matrix = RoutingMatrix()
            
            self.logger.info("Composants avancés initialisés")
            
        except (ImportError, Exception) as e:
            self.logger.warning(f"Erreur lors de l'initialisation des composants avancés: {e}")
            self.logger.info("Utilisation du mode simplifié")
            
            # Mode simplifié
            self.keyword_classifier = None
            self.llm_classifier = None
            self.hybrid_fusion = None
            self.routing_matrix = None
    
    def orchestrate(self, 
                   project_text: str,
                   project_context: Optional[Dict[str, Any]] = None,
                   user_constraints: Optional[Dict[str, Any]] = None,
                   task_executor: Optional[Callable] = None) -> OrchestrationResult:
        """
        Orchestration principale simplifiée
        
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
            self.logger.info("Début de l'orchestration")
            
            # Phase 1: Classification simplifiée
            classification_result = self._perform_classification(
                project_text, project_context
            )
            
            # Phase 2: Sélection d'agents
            agent_selection = self._select_agents(
                classification_result, project_context
            )
            
            # Phase 3: Planification du dispatch
            dispatch_plan = self._create_dispatch_plan(
                agent_selection, classification_result, project_context
            )
            
            # Phase 4: Exécution simulée
            execution_results = self._execute_dispatch(
                dispatch_plan, task_executor, project_context
            )
            
            # Phase 5: Génération du résultat final
            final_output = self._generate_final_output(
                classification_result, agent_selection, execution_results, project_context
            )
            
            # Compilation du résultat d'orchestration
            orchestration_result = OrchestrationResult(
                success=True,
                classification=classification_result,
                routing_decision=None,  # Simplifié
                agent_selection=agent_selection,
                dispatch_plan=dispatch_plan,
                final_output=final_output,
                orchestration_metadata=self._generate_orchestration_metadata(
                    classification_result, agent_selection, dispatch_plan
                ),
                execution_time=time.time() - start_time,
                quality_metrics=self._calculate_quality_metrics(
                    classification_result, execution_results
                )
            )
            
            # Mise à jour des statistiques
            self._update_orchestration_stats(orchestration_result, True)
            
            self.logger.info(f"Orchestration terminée avec succès en {time.time() - start_time:.2f}s")
            return orchestration_result
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'orchestration: {e}")
            
            # Gestion d'erreur simplifiée
            error_result = OrchestrationResult(
                success=False,
                classification=None,
                routing_decision=None,
                agent_selection=[],
                dispatch_plan=None,
                final_output={'error': str(e)},
                orchestration_metadata={
                    'error_type': type(e).__name__,
                    'execution_time': time.time() - start_time,
                    'orchestration_mode': self.orchestration_mode.value
                },
                execution_time=time.time() - start_time,
                quality_metrics={},
                error_details={
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            )
            
            self._update_orchestration_stats(error_result, False)
            return error_result
    
    def _perform_classification(self, 
                              project_text: str, 
                              project_context: Optional[Dict[str, Any]]) -> HybridClassificationResult:
        """Classification simplifiée du projet"""
        
        self.logger.info("Phase 1: Classification du projet")
        
        if self.hybrid_fusion and self.keyword_classifier and self.llm_classifier:
            try:
                # Classification avancée si disponible
                keyword_result = self.keyword_classifier.classify(project_text, project_context or {})
                llm_result = self.llm_classifier.classify(project_text, project_context or {})
                
                fusion_result = self.hybrid_fusion._fuse_results(
                    keyword_result, llm_result, project_text, project_context or {}
                )
                
                return fusion_result
            except Exception as e:
                self.logger.warning(f"Erreur classification avancée: {e}")
        
        # Classification simplifiée par mots-clés
        project_lower = project_text.lower()
        
        if any(word in project_lower for word in ['ecommerce', 'e-commerce', 'shop', 'store', 'marketplace']):
            domain = "ecommerce"
        elif any(word in project_lower for word in ['react', 'frontend', 'ui', 'interface']):
            domain = "frontend"
        elif any(word in project_lower for word in ['node', 'backend', 'api', 'server']):
            domain = "backend"
        else:
            domain = "general"
        
        return HybridClassificationResult()
    
    def _select_agents(self,
                      classification_result: HybridClassificationResult,
                      project_context: Optional[Dict[str, Any]]) -> List[str]:
        """Sélection d'agents basée sur la classification"""
        
        self.logger.info("Phase 2: Sélection d'agents")
        
        # Agents disponibles dans la configuration
        available_agents = [
            "frontend-react-specialist",
            "backend-nodejs-specialist", 
            "mongodb-specialist",
            "ecommerce-business-logic",
            "devops-deployment-specialist",
            "security-specialist",
            "performance-engineer",
            "system-architect"
        ]
        
        # Sélection intelligente basée sur le contexte
        selected_agents = []
        project_text = classification_result.final_domain if hasattr(classification_result, 'final_domain') else "general"
        
        # Logique de sélection
        if "ecommerce" in str(project_text).lower():
            selected_agents = [
                "frontend-react-specialist",
                "backend-nodejs-specialist",
                "mongodb-specialist", 
                "ecommerce-business-logic"
            ]
        elif "frontend" in str(project_text).lower() or "react" in str(project_text).lower():
            selected_agents = ["frontend-react-specialist"]
        elif "backend" in str(project_text).lower() or "node" in str(project_text).lower():
            selected_agents = ["backend-nodejs-specialist", "mongodb-specialist"]
        else:
            # Sélection par défaut
            selected_agents = ["system-architect", "performance-engineer"]
        
        self.logger.info(f"Agents sélectionnés: {selected_agents}")
        return selected_agents
    
    def _create_dispatch_plan(self,
                            agent_selection: List[str],
                            classification_result: HybridClassificationResult,
                            project_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Création du plan de dispatch"""
        
        self.logger.info("Phase 3: Planification du dispatch")
        
        # Détermination du mode selon la complexité
        if len(agent_selection) <= 1:
            mode = "SINGLE"
        elif len(agent_selection) <= 3:
            mode = "SEQUENTIAL"
        else:
            mode = "PARALLEL"
        
        dispatch_plan = {
            'dispatch_id': f"dispatch_{int(time.time())}",
            'mode': mode,
            'agents': agent_selection,
            'tasks': [
                {
                    'task_id': f"task_{i}_{agent}",
                    'agent_id': agent,
                    'task_type': 'analysis',
                    'priority': i + 1
                }
                for i, agent in enumerate(agent_selection)
            ],
            'estimated_duration': len(agent_selection) * 30,  # 30 min par agent
            'execution_order': [agent_selection]  # Simplifié
        }
        
        self.logger.info(f"Plan créé: mode {mode} avec {len(agent_selection)} agents")
        return dispatch_plan
    
    def _execute_dispatch(self,
                         dispatch_plan: Dict[str, Any],
                         task_executor: Optional[Callable],
                         project_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Exécution du dispatch"""
        
        self.logger.info("Phase 4: Exécution du dispatch")
        
        if task_executor:
            # Utilisation de l'exécuteur fourni
            task_results = []
            for task in dispatch_plan['tasks']:
                try:
                    result = task_executor(task)
                    task_results.append({
                        'task_id': task['task_id'],
                        'agent_id': task['agent_id'],
                        'success': True,
                        'output_data': result,
                        'execution_time': 1.0
                    })
                except Exception as e:
                    task_results.append({
                        'task_id': task['task_id'],
                        'agent_id': task['agent_id'],
                        'success': False,
                        'output_data': {'error': str(e)},
                        'execution_time': 0.0
                    })
        else:
            # Exécution simulée
            task_results = []
            for task in dispatch_plan['tasks']:
                task_results.append({
                    'task_id': task['task_id'],
                    'agent_id': task['agent_id'],
                    'success': True,
                    'output_data': {
                        'result': f"Tâche {task['task_id']} terminée avec succès",
                        'agent': task['agent_id'],
                        'status': 'completed'
                    },
                    'execution_time': 2.5
                })
        
        return {
            'task_results': task_results,
            'execution_id': dispatch_plan['dispatch_id']
        }
    
    def _generate_final_output(self,
                             classification_result: HybridClassificationResult,
                             agent_selection: List[str],
                             execution_results: Dict[str, Any],
                             project_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Génération du output final"""
        
        task_results = execution_results['task_results']
        successful_tasks = len([r for r in task_results if r['success']])
        
        return {
            'project_analysis': {
                'domain': getattr(classification_result, 'final_domain', 'general'),
                'type': getattr(classification_result, 'final_type', 'development'),
                'complexity': getattr(classification_result, 'final_complexity', 'moderate'),
                'phase': getattr(classification_result, 'final_phase', 'planning'),
                'confidence': getattr(classification_result, 'fusion_confidence', 0.8)
            },
            'execution_summary': {
                'total_tasks': len(task_results),
                'successful_tasks': successful_tasks,
                'failed_tasks': len(task_results) - successful_tasks,
                'execution_id': execution_results['execution_id']
            },
            'agents_used': agent_selection,
            'results': {
                'task_results': [r['output_data'] for r in task_results],
                'summary': f"Orchestration terminée avec {successful_tasks}/{len(task_results)} tâches réussies"
            },
            'recommendations': self._generate_recommendations(agent_selection, task_results)
        }
    
    def _generate_recommendations(self, agent_selection: List[str], task_results: List[Dict]) -> List[str]:
        """Génère des recommandations basées sur l'exécution"""
        recommendations = []
        
        if len(agent_selection) > 3:
            recommendations.append("Considérez la réduction du nombre d'agents pour améliorer l'efficacité")
        
        failed_tasks = [r for r in task_results if not r['success']]
        if failed_tasks:
            recommendations.append(f"Investiguer les {len(failed_tasks)} tâches échouées")
        
        if "ecommerce-business-logic" in agent_selection:
            recommendations.append("Intégrer des tests de performance pour les fonctionnalités e-commerce")
        
        return recommendations
    
    def _generate_orchestration_metadata(self,
                                       classification_result: HybridClassificationResult,
                                       agent_selection: List[str],
                                       dispatch_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Génère les métadonnées d'orchestration"""
        
        return {
            'orchestration_mode': self.orchestration_mode.value,
            'orchestration_strategy': self.orchestration_strategy.value,
            'agents_count': len(agent_selection),
            'tasks_count': len(dispatch_plan.get('tasks', [])),
            'dispatch_mode': dispatch_plan.get('mode', 'unknown'),
            'timestamp': time.time()
        }
    
    def _calculate_quality_metrics(self,
                                 classification_result: HybridClassificationResult,
                                 execution_results: Dict[str, Any]) -> Dict[str, float]:
        """Calcule les métriques de qualité"""
        
        task_results = execution_results['task_results']
        successful_tasks = len([r for r in task_results if r['success']])
        
        return {
            'classification_confidence': getattr(classification_result, 'fusion_confidence', 0.8),
            'execution_success_rate': successful_tasks / len(task_results) if task_results else 0.0,
            'overall_quality': (
                getattr(classification_result, 'fusion_confidence', 0.8) * 0.5 +
                (successful_tasks / len(task_results)) * 0.5
            ) if task_results else 0.0
        }
    
    def _extract_performance_requirements(self, project_context: Optional[Dict[str, Any]]) -> Dict[str, float]:
        """Extrait les exigences de performance"""
        return project_context.get('performance_requirements', {
            'max_execution_time': 300.0,  # 5 minutes
            'min_success_rate': 0.8,
            'max_concurrent_tasks': 5
        }) if project_context else {
            'max_execution_time': 300.0,
            'min_success_rate': 0.8,
            'max_concurrent_tasks': 5
        }
    
    def _extract_quality_requirements(self, project_context: Optional[Dict[str, Any]]) -> Dict[str, float]:
        """Extrait les exigences de qualité"""
        return project_context.get('quality_requirements', {
            'min_classification_confidence': 0.6,
            'min_success_rate': 0.8
        }) if project_context else {
            'min_classification_confidence': 0.6,
            'min_success_rate': 0.8
        }
    
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

# Fonction utilitaire pour créer l'orchestrateur
def create_orchestrator(mode: OrchestrationMode = OrchestrationMode.INTELLIGENT,
                       strategy: OrchestrationStrategy = OrchestrationStrategy.BALANCED) -> PrimaryOrchestrator:
    """Factory function pour créer un orchestrateur"""
    return PrimaryOrchestrator(mode, strategy)