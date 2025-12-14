#!/usr/bin/env python3
"""
Orchestrateur Principal Autonome pour OpenCode
Version complètement autonome sans dépendances externes
"""

import logging
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import json

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
class ClassificationResult:
    """Résultat de classification simplifié"""
    domain: str = "general"
    type: str = "development"
    complexity: str = "moderate"
    phase: str = "planning"
    confidence: float = 0.8

@dataclass
class OrchestrationResult:
    """Résultat d'orchestration complet"""
    success: bool
    classification: Optional[ClassificationResult]
    agent_selection: List[str]
    dispatch_plan: Optional[Dict[str, Any]]
    final_output: Dict[str, Any]
    orchestration_metadata: Dict[str, Any]
    execution_time: float
    quality_metrics: Dict[str, float]
    error_details: Optional[Dict[str, Any]] = None

class AutonomousOrchestrator:
    """Orchestrateur principal complètement autonome"""
    
    def __init__(self, 
                 orchestration_mode: OrchestrationMode = OrchestrationMode.INTELLIGENT,
                 orchestration_strategy: OrchestrationStrategy = OrchestrationStrategy.BALANCED):
        
        self.orchestration_mode = orchestration_mode
        self.orchestration_strategy = orchestration_strategy
        self.logger = logging.getLogger(__name__)
        
        # Configuration des agents disponibles
        self.available_agents = {
            "frontend-react-specialist": {
                "specialties": ["React", "TypeScript", "Redux", "UI/UX"],
                "model": "minimax-M2",
                "description": "Expert en développement frontend React"
            },
            "backend-nodejs-specialist": {
                "specialties": ["Node.js", "Express", "API", "Database"],
                "model": "minimax-M2", 
                "description": "Expert en développement backend Node.js"
            },
            "mongodb-specialist": {
                "specialties": ["MongoDB", "Database", "Aggregation", "Performance"],
                "model": "minimax-M2",
                "description": "Expert en base de données MongoDB"
            },
            "ecommerce-business-logic": {
                "specialties": ["E-commerce", "Business Logic", "Payment", "Inventory"],
                "model": "minimax-M2",
                "description": "Expert en logique métier e-commerce"
            },
            "devops-deployment-specialist": {
                "specialties": ["Docker", "CI/CD", "Cloud", "Monitoring"],
                "model": "grok-code-fast-1",
                "description": "Expert en déploiement et DevOps"
            },
            "security-specialist": {
                "specialties": ["Security", "Authentication", "OWASP", "Compliance"],
                "model": "minimax-M2",
                "description": "Expert en sécurité applicative"
            },
            "performance-engineer": {
                "specialties": ["Performance", "Optimization", "Scalability", "Monitoring"],
                "model": "grok-code-fast-1",
                "description": "Expert en optimisation des performances"
            },
            "system-architect": {
                "specialties": ["Architecture", "Design Patterns", "Scalability", "Best Practices"],
                "model": "minimax-M2",
                "description": "Architecte système expert"
            }
        }
        
        # Métriques globales
        self.orchestration_stats = {
            'total_orchestrations': 0,
            'successful_orchestrations': 0,
            'failed_orchestrations': 0,
            'average_execution_time': 0.0,
            'mode_usage': {mode.value: 0 for mode in OrchestrationMode},
            'strategy_usage': {strategy.value: 0 for strategy in OrchestrationStrategy},
            'quality_scores': [],
            'agent_usage': {agent: 0 for agent in self.available_agents.keys()}
        }
        
        self.logger.info("AutonomousOrchestrator initialisé")
    
    def orchestrate(self, 
                   project_text: str,
                   project_context: Optional[Dict[str, Any]] = None,
                   user_constraints: Optional[Dict[str, Any]] = None) -> OrchestrationResult:
        """
        Orchestration principale autonome
        
        Args:
            project_text: Texte du projet à analyser
            project_context: Contexte additionnel du projet
            user_constraints: Contraintes utilisateur
        
        Returns:
            OrchestrationResult complet
        """
        
        start_time = time.time()
        context = project_context or {}
        constraints = user_constraints or {}
        
        try:
            self.logger.info("Début de l'orchestration autonome")
            
            # Phase 1: Classification intelligente du projet
            classification_result = self._classify_project(project_text, context)
            
            # Phase 2: Sélection intelligente d'agents
            agent_selection = self._select_agents_intelligently(classification_result, context, constraints)
            
            # Phase 3: Planification du dispatch
            dispatch_plan = self._create_intelligent_dispatch_plan(agent_selection, classification_result, context)
            
            # Phase 4: Simulation d'exécution
            execution_results = self._simulate_execution(dispatch_plan, agent_selection)
            
            # Phase 5: Génération du rapport final
            final_output = self._generate_comprehensive_report(
                classification_result, agent_selection, execution_results, context
            )
            
            # Compilation du résultat
            orchestration_result = OrchestrationResult(
                success=True,
                classification=classification_result,
                agent_selection=agent_selection,
                dispatch_plan=dispatch_plan,
                final_output=final_output,
                orchestration_metadata=self._generate_metadata(agent_selection, dispatch_plan),
                execution_time=time.time() - start_time,
                quality_metrics=self._calculate_quality_metrics(agent_selection, execution_results)
            )
            
            # Mise à jour des statistiques
            self._update_stats(orchestration_result, True)
            
            self.logger.info(f"Orchestration terminée avec succès en {time.time() - start_time:.2f}s")
            return orchestration_result
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'orchestration: {e}")
            
            error_result = OrchestrationResult(
                success=False,
                classification=None,
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
                error_details={'error_type': type(e).__name__, 'error_message': str(e)}
            )
            
            self._update_stats(error_result, False)
            return error_result
    
    def _classify_project(self, project_text: str, context: Dict[str, Any]) -> ClassificationResult:
        """Classification intelligente du projet par analyse de contenu"""
        
        self.logger.info("Phase 1: Classification intelligente du projet")
        
        text_lower = project_text.lower()
        
        # Analyse par mots-clés pour déterminer le domaine
        if any(word in text_lower for word in ['ecommerce', 'e-commerce', 'shop', 'store', 'marketplace', 'boutique']):
            domain = "ecommerce"
            complexity = "high"
            phase = "development"
        elif any(word in text_lower for word in ['react', 'frontend', 'ui', 'interface', 'vue', 'angular']):
            domain = "frontend"
            complexity = "moderate"
            phase = "development"
        elif any(word in text_lower for word in ['node', 'backend', 'api', 'server', 'express']):
            domain = "backend"
            complexity = "moderate"
            phase = "development"
        elif any(word in text_lower for word in ['database', 'mongodb', 'mysql', 'sql']):
            domain = "database"
            complexity = "moderate"
            phase = "planning"
        elif any(word in text_lower for word in ['security', 'auth', 'authenticate', 'oauth']):
            domain = "security"
            complexity = "high"
            phase = "planning"
        elif any(word in text_lower for word in ['deploy', 'docker', 'ci/cd', 'production']):
            domain = "devops"
            complexity = "moderate"
            phase = "deployment"
        else:
            domain = "general"
            complexity = "moderate"
            phase = "planning"
        
        # Ajustement selon le contexte fourni
        if context.get('project_type') == 'ecommerce':
            domain = 'ecommerce'
            complexity = 'high'
        elif context.get('complexity') in ['high', 'expert']:
            complexity = 'high'
        
        confidence = self._calculate_classification_confidence(project_text, domain)
        
        return ClassificationResult(
            domain=domain,
            type=self._determine_project_type(text_lower),
            complexity=complexity,
            phase=phase,
            confidence=confidence
        )
    
    def _determine_project_type(self, text_lower: str) -> str:
        """Détermine le type de projet"""
        if any(word in text_lower for word in ['startup', 'saas', 'platform']):
            return "platform"
        elif any(word in text_lower for word in ['mobile', 'app', 'ios', 'android']):
            return "mobile_app"
        elif any(word in text_lower for word in ['web', 'website', 'site']):
            return "web_application"
        elif any(word in text_lower for word in ['api', 'service', 'microservice']):
            return "api_service"
        else:
            return "application"
    
    def _calculate_classification_confidence(self, project_text: str, domain: str) -> float:
        """Calcule la confiance de la classification"""
        
        # Analyse de la densité de mots-clés pertinents
        domain_keywords = {
            "ecommerce": ["commerce", "achat", "vente", "panier", "paiement", "produit"],
            "frontend": ["interface", "ui", "ux", "design", "react", "component"],
            "backend": ["serveur", "api", "base de données", "authentification"],
            "database": ["base de données", "requête", "stockage", "mongodb"],
            "security": ["sécurité", "authentification", "chiffrement", "protection"],
            "devops": ["déploiement", "docker", "ci/cd", "monitoring"]
        }
        
        keywords = domain_keywords.get(domain, [])
        keyword_count = sum(1 for keyword in keywords if keyword in project_text.lower())
        
        # Confiance basée sur la densité de mots-clés (max 0.9) + base (0.5)
        confidence = min(0.5 + (keyword_count * 0.1), 0.9)
        
        return confidence
    
    def _select_agents_intelligently(self, 
                                   classification: ClassificationResult,
                                   context: Dict[str, Any],
                                   constraints: Dict[str, Any]) -> List[str]:
        """Sélection intelligente d'agents basée sur la classification"""
        
        self.logger.info("Phase 2: Sélection intelligente d'agents")
        
        selected_agents = []
        
        # Sélection basée sur le domaine
        if classification.domain == "ecommerce":
            selected_agents = [
                "frontend-react-specialist",
                "backend-nodejs-specialist",
                "mongodb-specialist",
                "ecommerce-business-logic"
            ]
            
            # Ajout conditionnel d'agents selon la complexité
            if classification.complexity == "high":
                selected_agents.extend(["security-specialist", "system-architect"])
            
        elif classification.domain == "frontend":
            selected_agents = ["frontend-react-specialist"]
            if classification.complexity == "high":
                selected_agents.append("system-architect")
                
        elif classification.domain == "backend":
            selected_agents = ["backend-nodejs-specialist", "mongodb-specialist"]
            if classification.complexity == "high":
                selected_agents.extend(["security-specialist", "performance-engineer"])
                
        elif classification.domain == "database":
            selected_agents = ["mongodb-specialist", "backend-nodejs-specialist"]
            
        elif classification.domain == "security":
            selected_agents = ["security-specialist", "system-architect"]
            
        elif classification.domain == "devops":
            selected_agents = ["devops-deployment-specialist", "performance-engineer"]
            
        else:
            # Sélection par défaut intelligente
            selected_agents = ["system-architect", "performance-engineer"]
        
        # Filtrage selon les contraintes utilisateur
        if constraints.get('budget') == 'low':
            # Préférer les agents avec grok-code-fast-1
            fast_agents = [agent for agent in selected_agents 
                          if self.available_agents[agent]['model'] == 'grok-code-fast-1']
            if fast_agents:
                selected_agents = fast_agents[:2]  # Limiter à 2 agents
        
        if constraints.get('quality') == 'high':
            # Préférer minimax-M2
            selected_agents = [agent for agent in selected_agents 
                              if self.available_agents[agent]['model'] == 'minimax-M2']
        
        # Dédoublonnage et limitation
        selected_agents = list(dict.fromkeys(selected_agents))  # Préserve l'ordre
        max_agents = constraints.get('max_agents', 4)
        selected_agents = selected_agents[:max_agents]
        
        self.logger.info(f"Agents sélectionnés: {selected_agents}")
        return selected_agents
    
    def _create_intelligent_dispatch_plan(self,
                                        agent_selection: List[str],
                                        classification: ClassificationResult,
                                        context: Dict[str, Any]) -> Dict[str, Any]:
        """Création d'un plan de dispatch intelligent"""
        
        self.logger.info("Phase 3: Planification intelligente du dispatch")
        
        # Détermination du mode selon la complexité et le nombre d'agents
        if len(agent_selection) == 1:
            mode = "SINGLE"
        elif len(agent_selection) <= 2:
            mode = "SEQUENTIAL"
        elif len(agent_selection) <= 4:
            mode = "PARALLEL"
        else:
            mode = "HYBRID"
        
        # Ajustement du mode selon la phase
        if classification.phase == "planning":
            mode = "SEQUENTIAL"
        elif classification.phase == "deployment":
            mode = "SEQUENTIAL"
        
        # Estimation de la durée selon la complexité
        base_duration = {
            "beginner": 30,
            "moderate": 60,
            "high": 120,
            "expert": 180
        }
        
        estimated_duration = base_duration.get(classification.complexity, 60) * len(agent_selection)
        
        # Création des tâches
        tasks = []
        for i, agent_id in enumerate(agent_selection):
            agent_info = self.available_agents[agent_id]
            
            task = {
                'task_id': f"task_{i+1:02d}_{agent_id}",
                'agent_id': agent_id,
                'agent_name': agent_info['description'],
                'task_type': self._determine_task_type(agent_id, classification.domain),
                'priority': i + 1,
                'estimated_duration': estimated_duration // len(agent_selection),
                'model': agent_info['model'],
                'specialties': agent_info['specialties']
            }
            tasks.append(task)
        
        # Groupement pour l'exécution
        if mode == "PARALLEL":
            execution_order = [agent_selection]  # Tous en parallèle
        elif mode == "SEQUENTIAL":
            execution_order = [[agent] for agent in agent_selection]  # Un par un
        else:
            execution_order = [agent_selection]  # Par défaut
        
        dispatch_plan = {
            'dispatch_id': f"dispatch_{int(time.time())}",
            'mode': mode,
            'complexity': classification.complexity,
            'phase': classification.phase,
            'agents': agent_selection,
            'tasks': tasks,
            'estimated_duration': estimated_duration,
            'execution_order': execution_order,
            'confidence_score': classification.confidence
        }
        
        self.logger.info(f"Plan créé: mode {mode}, {len(agent_selection)} agents, durée estimée {estimated_duration}min")
        return dispatch_plan
    
    def _determine_task_type(self, agent_id: str, domain: str) -> str:
        """Détermine le type de tâche pour un agent donné"""
        
        task_types = {
            "frontend-react-specialist": "frontend_development",
            "backend-nodejs-specialist": "backend_development", 
            "mongodb-specialist": "database_design",
            "ecommerce-business-logic": "business_logic",
            "devops-deployment-specialist": "deployment_setup",
            "security-specialist": "security_review",
            "performance-engineer": "performance_optimization",
            "system-architect": "architecture_design"
        }
        
        return task_types.get(agent_id, "general_analysis")
    
    def _simulate_execution(self, dispatch_plan: Dict[str, Any], agent_selection: List[str]) -> Dict[str, Any]:
        """Simule l'exécution des tâches"""
        
        self.logger.info("Phase 4: Simulation d'exécution")
        
        task_results = []
        for task in dispatch_plan['tasks']:
            # Simulation réaliste des résultats
            success_probability = 0.9 if task['model'] == 'minimax-M2' else 0.85
            
            import random
            import time
            
            # Simulation du temps d'exécution
            execution_time = random.uniform(1.0, 5.0)
            time.sleep(min(execution_time, 0.1))  # Réduction pour les tests
            
            success = random.random() < success_probability
            
            if success:
                output_data = {
                    'result': f"Tâche {task['task_id']} terminée avec succès",
                    'agent': task['agent_id'],
                    'status': 'completed',
                    'deliverables': self._generate_deliverables(task),
                    'recommendations': self._generate_task_recommendations(task),
                    'next_steps': self._generate_next_steps(task)
                }
            else:
                output_data = {
                    'result': f"Tâche {task['task_id']} partiellement terminée",
                    'agent': task['agent_id'],
                    'status': 'partial',
                    'deliverables': ['Analyse initiale', 'Recommandations préliminaires'],
                    'limitations': ['Contraintes de temps', 'Données manquantes']
                }
            
            task_results.append({
                'task_id': task['task_id'],
                'agent_id': task['agent_id'],
                'success': success,
                'output_data': output_data,
                'execution_time': execution_time,
                'model_used': task['model']
            })
        
        return {
            'task_results': task_results,
            'execution_id': dispatch_plan['dispatch_id'],
            'mode': dispatch_plan['mode'],
            'total_agents': len(agent_selection)
        }
    
    def _generate_deliverables(self, task: Dict[str, Any]) -> List[str]:
        """Génère les livrables pour une tâche"""
        
        agent_id = task['agent_id']
        task_type = task['task_type']
        
        deliverables = {
            "frontend_development": ["Composants React", "Styles CSS", "Tests unitaires", "Documentation"],
            "backend_development": ["API endpoints", "Base de données", "Authentification", "Tests API"],
            "database_design": ["Schéma de base de données", "Requêtes optimisées", "Index", "Migration"],
            "business_logic": ["Logique métier", "Règles de validation", "Workflows", "Tests"],
            "deployment_setup": ["Dockerfile", "CI/CD pipeline", "Configuration prod", "Monitoring"],
            "security_review": ["Audit de sécurité", "Recommandations", "Tests de pénétration", "Compliance"],
            "performance_optimization": ["Analyse de performance", "Optimisations", "Métriques", "Benchmarks"],
            "architecture_design": ["Diagrammes d'architecture", "Patterns de design", "Documentation technique"]
        }
        
        return deliverables.get(task_type, ["Analyse", "Rapport", "Recommandations"])
    
    def _generate_task_recommendations(self, task: Dict[str, Any]) -> List[str]:
        """Génère des recommandations spécifiques à la tâche"""
        
        agent_id = task['agent_id']
        recommendations = {
            "frontend-react-specialist": [
                "Utiliser React 18 avec concurrentImplémenter la lazy features",
                " loading pour les composants",
                "Optimiser les re-renders avec React.memo"
            ],
            "backend-nodejs-specialist": [
                "Utiliser Express.js avec TypeScript",
                "Implémenter la validation des données avec Joi",
                "Ajouter la gestion d'erreurs centralisée"
            ],
            "mongodb-specialist": [
                "Créer des index appropriés pour les requêtes",
                "Utiliser l'agrégation pour les analytics",
                "Implémenter la réplication pour la haute disponibilité"
            ],
            "ecommerce-business-logic": [
                "Implémenter la gestion des stocks en temps réel",
                "Ajouter la logique de promotion flexible",
                "Intégrer les analytics de conversion"
            ]
        }
        
        return recommendations.get(agent_id, ["Suivre les bonnes pratiques", "Tester extensively"])
    
    def _generate_next_steps(self, task: Dict[str, Any]) -> List[str]:
        """Génère les prochaines étapes"""
        
        return [
            f"Revoir les livrables de {task['agent_id']}",
            "Valider les spécifications techniques",
            "Planifier l'intégration avec les autres composants",
            "Définir les critères de validation"
        ]
    
    def _generate_comprehensive_report(self,
                                     classification: ClassificationResult,
                                     agent_selection: List[str],
                                     execution_results: Dict[str, Any],
                                     context: Dict[str, Any]) -> Dict[str, Any]:
        """Génère un rapport complet"""
        
        task_results = execution_results['task_results']
        successful_tasks = len([r for r in task_results if r['success']])
        
        # Compilation des recommandations
        all_recommendations = []
        all_deliverables = []
        all_next_steps = []
        
        for result in task_results:
            if result['success']:
                output = result['output_data']
                all_recommendations.extend(output.get('recommendations', []))
                all_deliverables.extend(output.get('deliverables', []))
                all_next_steps.extend(output.get('next_steps', []))
        
        # Dédoublonnage des recommandations
        unique_recommendations = list(dict.fromkeys(all_recommendations))
        unique_deliverables = list(dict.fromkeys(all_deliverables))
        unique_next_steps = list(dict.fromkeys(all_next_steps))
        
        return {
            'project_analysis': {
                'domain': classification.domain,
                'type': classification.type,
                'complexity': classification.complexity,
                'phase': classification.phase,
                'confidence': classification.confidence,
                'estimated_effort': f"{len(agent_selection)} agents, {successful_tasks}/{len(task_results)} tâches réussies"
            },
            'execution_summary': {
                'total_tasks': len(task_results),
                'successful_tasks': successful_tasks,
                'failed_tasks': len(task_results) - successful_tasks,
                'success_rate': successful_tasks / len(task_results),
                'execution_id': execution_results['execution_id'],
                'mode_used': execution_results['mode']
            },
            'agents_used': [
                {
                    'agent_id': agent_id,
                    'description': self.available_agents[agent_id]['description'],
                    'model': self.available_agents[agent_id]['model'],
                    'specialties': self.available_agents[agent_id]['specialties']
                }
                for agent_id in agent_selection
            ],
            'deliverables': unique_deliverables,
            'recommendations': unique_recommendations,
            'next_steps': unique_next_steps,
            'technical_insights': self._generate_technical_insights(agent_selection, classification),
            'risk_assessment': self._assess_risks(agent_selection, classification),
            'success_probability': self._calculate_success_probability(classification, len(agent_selection))
        }
    
    def _generate_technical_insights(self, agent_selection: List[str], classification: ClassificationResult) -> List[str]:
        """Génère des insights techniques"""
        
        insights = []
        
        # Analyse de la stack technologique
        models_used = [self.available_agents[agent]['model'] for agent in agent_selection]
        if models_used.count('minimax-M2') > models_used.count('grok-code-fast-1'):
            insights.append("Stack de haute qualité avec minimax-M2 prioritaire")
        else:
            insights.append("Stack optimisée pour les coûts avec grok-code-fast-1")
        
        # Analyse de la complexité
        if classification.complexity == "high":
            insights.append("Projet complexe nécessitant une approche structurée")
            insights.append("Recommandation: phases de validation fréquentes")
        
        # Analyse du domaine
        if classification.domain == "ecommerce":
            insights.append("Domaine e-commerce: attention particulière à la sécurité et aux performances")
            insights.append("Intégration paiement et gestion des stocks à prévoir")
        
        return insights
    
    def _assess_risks(self, agent_selection: List[str], classification: ClassificationResult) -> List[str]:
        """Évalue les risques du projet"""
        
        risks = []
        
        if len(agent_selection) > 4:
            risks.append("Risque de complexité élevée avec de nombreux agents")
        
        if classification.complexity == "high":
            risks.append("Complexité élevée du projet")
        
        if classification.domain == "ecommerce":
            risks.append("Risques de sécurité et conformité réglementaire")
        
        if "security-specialist" not in agent_selection and classification.domain in ["ecommerce", "backend"]:
            risks.append("Absence d'expert sécurité pour un projet critique")
        
        return risks
    
    def _calculate_success_probability(self, classification: ClassificationResult, agent_count: int) -> float:
        """Calcule la probabilité de succès"""
        
        base_probability = 0.8
        
        # Ajustement selon la confiance de classification
        confidence_factor = classification.confidence
        
        # Ajustement selon le nombre d'agents (optimal entre 2-4)
        if agent_count < 2:
            agent_factor = 0.9  # Trop peu d'agents
        elif agent_count <= 4:
            agent_factor = 1.0  # Optimal
        else:
            agent_factor = 0.8  # Trop d'agents
        
        # Ajustement selon la complexité
        complexity_factors = {
            "beginner": 1.0,
            "moderate": 0.9,
            "high": 0.8,
            "expert": 0.7
        }
        
        complexity_factor = complexity_factors.get(classification.complexity, 0.8)
        
        final_probability = base_probability * confidence_factor * agent_factor * complexity_factor
        
        return min(final_probability, 0.95)  # Cap à 95%
    
    def _generate_metadata(self, agent_selection: List[str], dispatch_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Génère les métadonnées d'orchestration"""
        
        return {
            'orchestration_mode': self.orchestration_mode.value,
            'orchestration_strategy': self.orchestration_strategy.value,
            'agents_count': len(agent_selection),
            'tasks_count': len(dispatch_plan.get('tasks', [])),
            'dispatch_mode': dispatch_plan.get('mode', 'unknown'),
            'timestamp': time.time(),
            'orchestrator_version': '1.0.0-autonomous'
        }
    
    def _calculate_quality_metrics(self, agent_selection: List[str], execution_results: Dict[str, Any]) -> Dict[str, float]:
        """Calcule les métriques de qualité"""
        
        task_results = execution_results['task_results']
        successful_tasks = len([r for r in task_results if r['success']])
        
        # Calcul du score de diversité d'agents
        models_used = [self.available_agents[agent]['model'] for agent in agent_selection]
        unique_models = len(set(models_used))
        diversity_score = unique_models / len(models_used) if models_used else 0
        
        # Calcul du score de qualité
        quality_score = (
            (successful_tasks / len(task_results)) * 0.4 +  # 40% taux de réussite
            diversity_score * 0.3 +  # 30% diversité
            0.8 * 0.3  # 30% score de base
        )
        
        return {
            'execution_success_rate': successful_tasks / len(task_results) if task_results else 0.0,
            'agent_diversity_score': diversity_score,
            'overall_quality': quality_score,
            'model_balance': len([m for m in models_used if m == 'minimax-M2']) / len(models_used) if models_used else 0.5
        }
    
    def _update_stats(self, result: OrchestrationResult, success: bool):
        """Met à jour les statistiques"""
        self.orchestration_stats['total_orchestrations'] += 1
        
        if success:
            self.orchestration_stats['successful_orchestrations'] += 1
            self.orchestration_stats['quality_scores'].append(
                result.quality_metrics.get('overall_quality', 0.0)
            )
            self.orchestration_stats['mode_usage'][self.orchestration_mode.value] += 1
            self.orchestration_stats['strategy_usage'][self.orchestration_strategy.value] += 1
            
            # Mise à jour de l'usage des agents
            for agent in result.agent_selection:
                self.orchestration_stats['agent_usage'][agent] += 1
        else:
            self.orchestration_stats['failed_orchestrations'] += 1
        
        self.orchestration_stats['average_execution_time'] += result.execution_time
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retourne les statistiques complètes"""
        stats = self.orchestration_stats.copy()
        
        if stats['total_orchestrations'] > 0:
            stats['success_rate'] = stats['successful_orchestrations'] / stats['total_orchestrations']
            stats['average_quality'] = (
                sum(stats['quality_scores']) / len(stats['quality_scores'])
                if stats['quality_scores'] else 0.0
            )
            stats['average_execution_time'] = stats['average_execution_time'] / stats['total_orchestrations']
            
            # Top agents utilisés
            sorted_agents = sorted(stats['agent_usage'].items(), key=lambda x: x[1], reverse=True)
            stats['top_agents'] = sorted_agents[:5]
        
        return stats

# Fonction utilitaire
def create_autonomous_orchestrator(mode: OrchestrationMode = OrchestrationMode.INTELLIGENT,
                                  strategy: OrchestrationStrategy = OrchestrationStrategy.BALANCED) -> AutonomousOrchestrator:
    """Factory function pour créer un orchestrateur autonome"""
    return AutonomousOrchestrator(mode, strategy)