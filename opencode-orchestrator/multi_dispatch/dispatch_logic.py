"""
Logique Multi-Dispatch Intelligente
Détermination automatique des modes de dispatch et coordination des exécutions
"""

import logging
import time
import asyncio
from typing import Dict, List, Tuple, Optional, Any, NamedTuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from collections import defaultdict, deque

from .agent_selector import AgentScore, SelectionCriteria
from core.hybrid_fusion import HybridClassificationResult

@dataclass
class DispatchTask:
    """Représente une tâche de dispatch"""
    task_id: str
    agent_id: str
    task_type: str
    input_data: Dict[str, Any]
    dependencies: List[str] = field(default_factory=list)
    priority: int = 1
    timeout: float = 300.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TaskResult:
    """Résultat d'une tâche de dispatch"""
    task_id: str
    agent_id: str
    success: bool
    output_data: Dict[str, Any]
    execution_time: float
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DispatchPlan:
    """Plan de dispatch détaillé"""
    dispatch_id: str
    mode: 'DispatchMode'
    tasks: List[DispatchTask]
    execution_order: List[List[str]]  # Groupes de tâches à exécuter en parallèle
    estimated_duration: float
    resource_requirements: Dict[str, Any]
    fallback_strategy: str
    metadata: Dict[str, Any] = field(default_factory=dict)

class DispatchMode(Enum):
    """Modes de dispatch disponibles"""
    SINGLE = "single"
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HYBRID = "hybrid"
    ADAPTIVE = "adaptive"

class DispatchStrategy(Enum):
    """Stratégies de dispatch"""
    PERFORMANCE_OPTIMIZED = "performance_optimized"
    RESOURCE_EFFICIENT = "resource_efficient"
    QUALITY_FOCUSED = "quality_focused"
    ADAPTIVE_SELECTION = "adaptive_selection"
    DEPENDENCY_AWARE = "dependency_aware"

class IntelligentDispatchLogic:
    """Logique intelligente de dispatch multi-mode"""
    
    def __init__(self, dispatch_strategy: DispatchStrategy = DispatchStrategy.ADAPTIVE_SELECTION):
        self.dispatch_strategy = dispatch_strategy
        self.logger = logging.getLogger(__name__)
        
        # Pool d'exécuteurs pour les tâches parallèles
        self.thread_pool = ThreadPoolExecutor(max_workers=10)
        
        # Cache des plans de dispatch
        self._dispatch_cache = {}
        
        # Métriques de performance
        self.dispatch_stats = {
            'total_dispatches': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'mode_usage': {mode.value: 0 for mode in DispatchMode},
            'strategy_usage': {strategy.value: 0 for strategy in DispatchStrategy},
            'average_execution_time': 0.0,
            'resource_utilization': defaultdict(float)
        }
        
        # Historique des performances pour optimisation
        self.performance_history = deque(maxlen=1000)
        
        # Gestion des dépendances
        self.dependency_graph = defaultdict(set)
        
        # État des exécutions en cours
        self.active_executions = {}
    
    def create_dispatch_plan(self, agent_scores: List[AgentScore],
                           classification_result: HybridClassificationResult,
                           context: Dict[str, Any] = None) -> DispatchPlan:
        """
        Crée un plan de dispatch intelligent
        
        Args:
            agent_scores: Agents sélectionnés avec leurs scores
            classification_result: Résultat de classification
            context: Contexte additionnel
        
        Returns:
            Plan de dispatch optimisé
        """
        start_time = time.time()
        
        try:
            # Génération de l'ID unique du plan
            dispatch_id = f"dispatch_{int(time.time())}_{hash(str(agent_scores))}"
            
            # Détermination du mode de dispatch optimal
            optimal_mode = self._determine_optimal_dispatch_mode(
                agent_scores, classification_result, context
            )
            
            # Création des tâches
            tasks = self._create_dispatch_tasks(agent_scores, classification_result, context)
            
            # Analyse des dépendances
            self._analyze_task_dependencies(tasks)
            
            # Planification de l'ordre d'exécution
            execution_order = self._plan_execution_order(tasks, optimal_mode)
            
            # Estimation de la durée
            estimated_duration = self._estimate_execution_duration(tasks, optimal_mode)
            
            # Détermination des ressources requises
            resource_requirements = self._calculate_resource_requirements(tasks, optimal_mode)
            
            # Stratégie de fallback
            fallback_strategy = self._determine_fallback_strategy(optimal_mode, classification_result)
            
            plan = DispatchPlan(
                dispatch_id=dispatch_id,
                mode=optimal_mode,
                tasks=tasks,
                execution_order=execution_order,
                estimated_duration=estimated_duration,
                resource_requirements=resource_requirements,
                fallback_strategy=fallback_strategy,
                metadata={
                    'creation_time': time.time(),
                    'strategy_used': self.dispatch_strategy.value,
                    'agent_count': len(agent_scores),
                    'task_count': len(tasks)
                }
            )
            
            # Mise à jour des statistiques
            self._update_dispatch_stats(plan, time.time() - start_time, True)
            
            self.logger.info(f"Plan de dispatch créé: {optimal_mode.value} avec {len(tasks)} tâches")
            return plan
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la création du plan de dispatch: {e}")
            self._update_dispatch_stats(None, time.time() - start_time, False)
            raise
    
    def execute_dispatch_plan(self, plan: DispatchPlan, 
                            task_executor: Callable[[DispatchTask], TaskResult]) -> List[TaskResult]:
        """
        Exécute un plan de dispatch
        
        Args:
            plan: Plan de dispatch à exécuter
            task_executor: Fonction pour exécuter une tâche
        
        Returns:
            Résultats de toutes les tâches
        """
        execution_id = f"exec_{plan.dispatch_id}"
        self.active_executions[execution_id] = {
            'start_time': time.time(),
            'status': 'running',
            'plan_id': plan.dispatch_id
        }
        
        try:
            self.logger.info(f"Début d'exécution du dispatch {plan.dispatch_id}")
            
            if plan.mode == DispatchMode.SINGLE:
                results = self._execute_single_mode(plan, task_executor)
            elif plan.mode == DispatchMode.SEQUENTIAL:
                results = self._execute_sequential_mode(plan, task_executor)
            elif plan.mode == DispatchMode.PARALLEL:
                results = self._execute_parallel_mode(plan, task_executor)
            elif plan.mode == DispatchMode.HYBRID:
                results = self._execute_hybrid_mode(plan, task_executor)
            else:  # ADAPTIVE
                results = self._execute_adaptive_mode(plan, task_executor)
            
            # Mise à jour de l'état d'exécution
            self.active_executions[execution_id]['status'] = 'completed'
            self.active_executions[execution_id]['end_time'] = time.time()
            self.active_executions[execution_id]['results'] = results
            
            # Mise à jour des statistiques
            self._update_execution_stats(results, plan.mode, True)
            
            self.logger.info(f"Dispatch {plan.dispatch_id} terminé avec {len(results)} résultats")
            return results
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution du dispatch {plan.dispatch_id}: {e}")
            self.active_executions[execution_id]['status'] = 'failed'
            self.active_executions[execution_id]['end_time'] = time.time()
            self.active_executions[execution_id]['error'] = str(e)
            
            # Exécution du fallback si configuré
            if plan.fallback_strategy:
                return self._execute_fallback(plan, task_executor, str(e))
            
            raise
        
        finally:
            # Nettoyage après un délai
            threading.Timer(300, lambda: self.active_executions.pop(execution_id, None)).start()
    
    def _determine_optimal_dispatch_mode(self, agent_scores: List[AgentScore],
                                       classification_result: HybridClassificationResult,
                                       context: Dict[str, Any]) -> DispatchMode:
        """Détermine le mode de dispatch optimal"""
        
        # Analyse des caractéristiques du projet
        complexity = classification_result.final_complexity
        phase = classification_result.final_phase
        confidence = classification_result.fusion_confidence
        agent_count = len(agent_scores)
        
        # Règles de décision
        
        # Si un seul agent ou faible confiance → mode single
        if agent_count == 1 or confidence < 0.6:
            return DispatchMode.SINGLE
        
        # Phase de planification → sequential pour éviter la duplication
        if phase == "planning":
            return DispatchMode.SEQUENTIAL
        
        # Projets complexes → hybrid ou parallel
        if complexity in ["advanced", "expert"]:
            if agent_count >= 3 and confidence > 0.8:
                return DispatchMode.PARALLEL
            else:
                return DispatchMode.HYBRID
        
        # Projets intermédiaires → hybrid
        if complexity == "intermediate":
            if agent_count >= 2:
                return DispatchMode.HYBRID
            else:
                return DispatchMode.SEQUENTIAL
        
        # Projets simples → parallel si agents multiples
        if complexity == "beginner" and agent_count > 1:
            return DispatchMode.PARALLEL
        
        # Mode adaptatif par défaut
        return DispatchMode.ADAPTIVE
    
    def _create_dispatch_tasks(self, agent_scores: List[AgentScore],
                             classification_result: HybridClassificationResult,
                             context: Dict[str, Any]) -> List[DispatchTask]:
        """Crée les tâches de dispatch pour chaque agent"""
        
        tasks = []
        domain = classification_result.final_domain
        phase = classification_result.final_phase
        
        for i, agent_score in enumerate(agent_scores):
            agent_id = agent_score.agent_id
            
            # Type de tâche selon la phase et le domaine
            if phase == "planning":
                task_type = "architecture_review" if i == 0 else "requirement_analysis"
            elif phase == "development":
                if domain == "web_development":
                    task_type = "frontend_development" if "frontend" in agent_score.agent_id else "backend_development"
                elif domain == "data_science":
                    task_type = "data_processing" if i == 0 else "model_development"
                else:
                    task_type = "development"
            elif phase == "testing":
                task_type = "automated_testing"
            elif phase == "deployment":
                task_type = "deployment_setup"
            else:
                task_type = "general_task"
            
            # Priorité basée sur le score de l'agent
            priority = max(1, min(5, int(agent_score.total_score * 5)))
            
            # Timeout basé sur la complexité
            timeout = self._calculate_task_timeout(classification_result.final_complexity)
            
            task = DispatchTask(
                task_id=f"task_{agent_id}_{i}",
                agent_id=agent_id,
                task_type=task_type,
                input_data={
                    'classification': classification_result.__dict__,
                    'context': context,
                    'agent_score': agent_score.__dict__
                },
                priority=priority,
                timeout=timeout,
                metadata={
                    'agent_rank': i,
                    'task_complexity': classification_result.final_complexity,
                    'domain': domain,
                    'phase': phase
                }
            )
            
            tasks.append(task)
        
        return tasks
    
    def _analyze_task_dependencies(self, tasks: List[DispatchTask]):
        """Analyse les dépendances entre tâches"""
        
        # Reset du graphe de dépendances
        self.dependency_graph.clear()
        
        # Règles de dépendances selon les types de tâches
        dependency_rules = {
            "architecture_review": ["requirement_analysis"],
            "frontend_development": ["backend_development"],
            "data_processing": ["model_development"],
            "testing": ["development"],
            "deployment_setup": ["testing"]
        }
        
        for task in tasks:
            self.dependency_graph[task.task_id] = set()
            
            # Application des règles de dépendances
            if task.task_type in dependency_rules:
                required_types = dependency_rules[task.task_type]
                for other_task in tasks:
                    if other_task.task_id != task.task_id and other_task.task_type in required_types:
                        self.dependency_graph[task.task_id].add(other_task.task_id)
        
        # Détection des dépendances circulaires (simple)
        self._detect_circular_dependencies(tasks)
    
    def _detect_circular_dependencies(self, tasks: List[DispatchTask]):
        """Détecte et résout les dépendances circulaires"""
        
        visited = set()
        rec_stack = set()
        
        def has_cycle(task_id):
            if task_id in rec_stack:
                return True
            if task_id in visited:
                return False
            
            visited.add(task_id)
            rec_stack.add(task_id)
            
            for neighbor in self.dependency_graph.get(task_id, set()):
                if has_cycle(neighbor):
                    return True
            
            rec_stack.remove(task_id)
            return False
        
        # Suppression des dépendances circulaires
        for task in tasks:
            if has_cycle(task.task_id):
                self.logger.warning(f"Dépendance circulaire détectée pour {task.task_id}, suppression")
                self.dependency_graph[task.task_id].clear()
    
    def _plan_execution_order(self, tasks: List[DispatchTask], mode: DispatchMode) -> List[List[str]]:
        """Planifie l'ordre d'exécution des tâches"""
        
        if mode == DispatchMode.SINGLE:
            return [[tasks[0].task_id]] if tasks else []
        
        elif mode == DispatchMode.SEQUENTIAL:
            # Exécution séquentielle - une tâche à la fois
            return [[task.task_id] for task in sorted(tasks, key=lambda x: x.priority, reverse=True)]
        
        elif mode == DispatchMode.PARALLEL:
            # Toutes les tâches en parallèle si pas de dépendances
            parallel_groups = []
            remaining_tasks = {task.task_id: task for task in tasks}
            
            while remaining_tasks:
                # Trouve les tâches sans dépendances non satisfaites
                ready_tasks = []
                for task_id, task in remaining_tasks.items():
                    deps = self.dependency_graph.get(task_id, set())
                    if not deps.intersection(set(remaining_tasks.keys())):
                        ready_tasks.append(task_id)
                
                if ready_tasks:
                    parallel_groups.append(ready_tasks)
                    for task_id in ready_tasks:
                        del remaining_tasks[task_id]
                else:
                    # Si aucune tâche prête, prendre la plus prioritaire
                    if remaining_tasks:
                        next_task = min(remaining_tasks.keys(), 
                                      key=lambda x: remaining_tasks[x].priority)
                        parallel_groups.append([next_task])
                        del remaining_tasks[next_task]
            
            return parallel_groups
        
        elif mode == DispatchMode.HYBRID:
            # Combinaison séquentielle et parallèle
            high_priority_tasks = [task for task in tasks if task.priority >= 4]
            normal_priority_tasks = [task for task in tasks if task.priority < 4]
            
            execution_order = []
            
            # Exécution séquentielle des tâches à haute priorité
            if high_priority_tasks:
                execution_order.append([task.task_id for task in 
                                      sorted(high_priority_tasks, key=lambda x: x.priority, reverse=True)])
            
            # Exécution en parallèle des tâches normales
            if normal_priority_tasks:
                execution_order.extend(self._plan_execution_order(normal_priority_tasks, DispatchMode.PARALLEL))
            
            return execution_order
        
        else:  # ADAPTIVE
            # Mode adaptatif basé sur les caractéristiques
            if len(tasks) <= 2:
                return self._plan_execution_order(tasks, DispatchMode.SEQUENTIAL)
            elif len(tasks) >= 4:
                return self._plan_execution_order(tasks, DispatchMode.PARALLEL)
            else:
                return self._plan_execution_order(tasks, DispatchMode.HYBRID)
    
    def _estimate_execution_duration(self, tasks: List[DispatchTask], mode: DispatchMode) -> float:
        """Estime la durée d'exécution du dispatch"""
        
        # Durée de base par tâche
        base_task_duration = 60.0  # 1 minute par défaut
        
        # Ajustements selon la complexité
        complexity_multipliers = {
            "beginner": 0.5,
            "intermediate": 1.0,
            "advanced": 2.0,
            "expert": 3.5
        }
        
        # Calcul de la durée totale estimée
        total_estimated = 0.0
        
        for task in tasks:
            complexity = task.metadata.get('task_complexity', 'intermediate')
            multiplier = complexity_multipliers.get(complexity, 1.0)
            task_duration = base_task_duration * multiplier
            
            total_estimated += task_duration
        
        # Ajustement selon le mode
        if mode == DispatchMode.PARALLEL:
            # En parallèle, durée = durée de la tâche la plus longue
            total_estimated = max(total_estimated / len(tasks), base_task_duration)
        elif mode == DispatchMode.SEQUENTIAL:
            # En séquentiel, durée = somme des durées
            pass  # total_estimated déjà correct
        elif mode == DispatchMode.HYBRID:
            # Mix séquentiel/parallèle
            total_estimated *= 0.7  # Optimisation de 30%
        
        return total_estimated
    
    def _calculate_resource_requirements(self, tasks: List[DispatchTask], mode: DispatchMode) -> Dict[str, Any]:
        """Calcule les ressources nécessaires"""
        
        return {
            'max_concurrent_tasks': len(tasks) if mode == DispatchMode.PARALLEL else 1,
            'estimated_memory': len(tasks) * 100,  # MB
            'estimated_cpu': len(tasks) * 0.5,  # CPU cores
            'estimated_network': len(tasks) * 10,  # MB
            'execution_mode': mode.value,
            'task_complexity_distribution': self._get_complexity_distribution(tasks)
        }
    
    def _get_complexity_distribution(self, tasks: List[DispatchTask]) -> Dict[str, int]:
        """Distribue la complexité des tâches"""
        distribution = defaultdict(int)
        for task in tasks:
            complexity = task.metadata.get('task_complexity', 'intermediate')
            distribution[complexity] += 1
        return dict(distribution)
    
    def _determine_fallback_strategy(self, mode: DispatchMode, 
                                   classification_result: HybridClassificationResult) -> str:
        """Détermine la stratégie de fallback"""
        
        if mode == DispatchMode.PARALLEL:
            return "sequential_fallback"
        elif mode == DispatchMode.HYBRID:
            return "sequential_fallback"
        elif mode == DispatchMode.SINGLE:
            return "retry_with_different_agent"
        else:
            return "sequential_fallback"
    
    def _calculate_task_timeout(self, complexity: str) -> float:
        """Calcule le timeout pour une tâche"""
        timeouts = {
            "beginner": 60.0,      # 1 minute
            "intermediate": 300.0, # 5 minutes
            "advanced": 900.0,     # 15 minutes
            "expert": 1800.0       # 30 minutes
        }
        return timeouts.get(complexity, 300.0)
    
    def _execute_single_mode(self, plan: DispatchPlan, task_executor: Callable) -> List[TaskResult]:
        """Exécute en mode single"""
        results = []
        for task_group in plan.execution_order:
            for task_id in task_group:
                task = next(t for t in plan.tasks if t.task_id == task_id)
                result = task_executor(task)
                results.append(result)
        return results
    
    def _execute_sequential_mode(self, plan: DispatchPlan, task_executor: Callable) -> List[TaskResult]:
        """Exécute en mode séquentiel"""
        results = []
        for task_group in plan.execution_order:
            for task_id in task_group:
                task = next(t for t in plan.tasks if t.task_id == task_id)
                result = task_executor(task)
                results.append(result)
                
                # Si échec et tâche critique, arrêt
                if not result.success and task.priority >= 4:
                    self.logger.error(f"Tâche critique échouée: {task.task_id}")
                    break
        return results
    
    def _execute_parallel_mode(self, plan: DispatchPlan, task_executor: Callable) -> List[TaskResult]:
        """Exécute en mode parallèle"""
        results = []
        
        for task_group in plan.execution_order:
            # Exécute le groupe de tâches en parallèle
            futures = {}
            for task_id in task_group:
                task = next(t for t in plan.tasks if t.task_id == task_id)
                future = self.thread_pool.submit(self._execute_task_with_timeout, task, task_executor)
                futures[future] = task_id
            
            # Collecte les résultats
            for future in as_completed(futures, timeout=max(t.timeout for t in plan.tasks if t.task_id in futures.values())):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    task_id = futures[future]
                    self.logger.error(f"Erreur lors de l'exécution parallèle de {task_id}: {e}")
                    # Créer un résultat d'erreur
                    task = next(t for t in plan.tasks if t.task_id == task_id)
                    error_result = TaskResult(
                        task_id=task_id,
                        agent_id=task.agent_id,
                        success=False,
                        output_data={},
                        execution_time=0.0,
                        error_message=str(e)
                    )
                    results.append(error_result)
        
        return results
    
    def _execute_hybrid_mode(self, plan: DispatchPlan, task_executor: Callable) -> List[TaskResult]:
        """Exécute en mode hybride"""
        results = []
        
        for task_group in plan.execution_order:
            if len(task_group) == 1:
                # Exécution séquentielle (une tâche)
                task = next(t for t in plan.tasks if t.task_id == task_group[0])
                result = task_executor(task)
                results.append(result)
            else:
                # Exécution en parallèle (groupe de tâches)
                futures = {}
                for task_id in task_group:
                    task = next(t for t in plan.tasks if t.task_id == task_id)
                    future = self.thread_pool.submit(self._execute_task_with_timeout, task, task_executor)
                    futures[future] = task_id
                
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        task_id = futures[future]
                        task = next(t for t in plan.tasks if t.task_id == task_id)
                        error_result = TaskResult(
                            task_id=task_id,
                            agent_id=task.agent_id,
                            success=False,
                            output_data={},
                            execution_time=0.0,
                            error_message=str(e)
                        )
                        results.append(error_result)
        
        return results
    
    def _execute_adaptive_mode(self, plan: DispatchPlan, task_executor: Callable) -> List[TaskResult]:
        """Exécute en mode adaptatif"""
        # Basé sur la performance en temps réel
        results = []
        
        # Commence en parallèle pour les tâches indépendantes
        if len(plan.execution_order) > 1:
            # Exécute le premier groupe en parallèle
            first_group = plan.execution_order[0]
            parallel_results = self._execute_parallel_group(first_group, task_executor)
            results.extend(parallel_results)
            
            # Analyse les résultats pour adapter la suite
            success_rate = sum(1 for r in parallel_results if r.success) / len(parallel_results)
            
            if success_rate > 0.8:
                # Continue en parallèle
                for group in plan.execution_order[1:]:
                    group_results = self._execute_parallel_group(group, task_executor)
                    results.extend(group_results)
            else:
                # Bascule en séquentiel
                for group in plan.execution_order[1:]:
                    group_results = self._execute_sequential_group(group, task_executor)
                    results.extend(group_results)
        else:
            # Un seul groupe, exécution directe
            results = self._execute_parallel_group(plan.execution_order[0], task_executor)
        
        return results
    
    def _execute_task_with_timeout(self, task: DispatchTask, task_executor: Callable) -> TaskResult:
        """Exécute une tâche avec timeout"""
        start_time = time.time()
        try:
            result = task_executor(task)
            result.execution_time = time.time() - start_time
            return result
        except Exception as e:
            return TaskResult(
                task_id=task.task_id,
                agent_id=task.agent_id,
                success=False,
                output_data={},
                execution_time=time.time() - start_time,
                error_message=str(e)
            )
    
    def _execute_parallel_group(self, task_group: List[str], task_executor: Callable) -> List[TaskResult]:
        """Exécute un groupe de tâches en parallèle"""
        # Cette méthode est appelée dans _execute_adaptive_mode
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        with ThreadPoolExecutor(max_workers=len(task_group)) as executor:
            futures = {}
            for task_id in task_group:
                # Recrée la tâche (simplification)
                future = executor.submit(self._simulate_task_execution, task_id)
                futures[future] = task_id
            
            results = []
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    task_id = futures[future]
                    results.append(TaskResult(
                        task_id=task_id,
                        agent_id="unknown",
                        success=False,
                        output_data={},
                        execution_time=0.0,
                        error_message=str(e)
                    ))
            return results
    
    def _execute_sequential_group(self, task_group: List[str], task_executor: Callable) -> List[TaskResult]:
        """Exécute un groupe de tâches en séquentiel"""
        results = []
        for task_id in task_group:
            # Simulation simple de l'exécution séquentielle
            result = self._simulate_task_execution(task_id)
            results.append(result)
        return results
    
    def _simulate_task_execution(self, task_id: str) -> TaskResult:
        """Simulation simple d'exécution de tâche"""
        import random
        import time
        
        # Simulation d'un temps d'exécution variable
        execution_time = random.uniform(1, 5)
        time.sleep(execution_time)
        
        # Simulation d'un taux de succès de 90%
        success = random.random() > 0.1
        
        return TaskResult(
            task_id=task_id,
            agent_id="simulated_agent",
            success=success,
            output_data={"simulated": True, "task_id": task_id},
            execution_time=execution_time
        )
    
    def _execute_fallback(self, plan: DispatchPlan, task_executor: Callable, error: str) -> List[TaskResult]:
        """Exécute la stratégie de fallback"""
        self.logger.info(f"Exécution du fallback pour {plan.dispatch_id}: {error}")
        
        if plan.fallback_strategy == "sequential_fallback":
            # Force l'exécution séquentielle
            plan.mode = DispatchMode.SEQUENTIAL
            return self._execute_sequential_mode(plan, task_executor)
        elif plan.fallback_strategy == "retry_with_different_agent":
            # Retry avec d'autres agents (simulation)
            self.logger.info("Retry avec agents alternatifs")
            return []
        else:
            self.logger.warning(f"Stratégie de fallback inconnue: {plan.fallback_strategy}")
            return []
    
    def _update_dispatch_stats(self, plan: Optional[DispatchPlan], creation_time: float, success: bool):
        """Met à jour les statistiques de dispatch"""
        self.dispatch_stats['total_dispatches'] += 1
        
        if success and plan:
            self.dispatch_stats['mode_usage'][plan.mode.value] += 1
            self.dispatch_stats['strategy_usage'][self.dispatch_strategy.value] += 1
        
        self.dispatch_stats['average_execution_time'] += creation_time
    
    def _update_execution_stats(self, results: List[TaskResult], mode: DispatchMode, success: bool):
        """Met à jour les statistiques d'exécution"""
        if success:
            self.dispatch_stats['successful_executions'] += 1
        else:
            self.dispatch_stats['failed_executions'] += 1
        
        # Enregistrement de la performance
        performance_entry = {
            'timestamp': time.time(),
            'mode': mode.value,
            'success_rate': sum(1 for r in results if r.success) / len(results) if results else 0,
            'average_execution_time': sum(r.execution_time for r in results) / len(results) if results else 0
        }
        self.performance_history.append(performance_entry)
    
    def get_dispatch_explanation(self, plan: DispatchPlan) -> Dict[str, Any]:
        """Génère une explication détaillée du dispatch"""
        return {
            'dispatch_summary': {
                'dispatch_id': plan.dispatch_id,
                'mode_selected': plan.mode.value,
                'strategy_used': self.dispatch_strategy.value,
                'total_tasks': len(plan.tasks),
                'estimated_duration': plan.estimated_duration,
                'execution_groups': len(plan.execution_order)
            },
            'task_breakdown': [
                {
                    'task_id': task.task_id,
                    'agent_id': task.agent_id,
                    'task_type': task.task_type,
                    'priority': task.priority,
                    'timeout': task.timeout,
                    'dependencies': list(self.dependency_graph.get(task.task_id, set()))
                }
                for task in plan.tasks
            ],
            'execution_plan': plan.execution_order,
            'resource_requirements': plan.resource_requirements,
            'fallback_strategy': plan.fallback_strategy,
            'performance_history': list(self.performance_history)[-10:]  # 10 dernières entrées
        }
