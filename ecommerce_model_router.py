#!/usr/bin/env python3
"""
Configuration et Extension de l'Orchestrateur pour E-commerce
Implémentation du switching automatique minimax-M2 / grok-code-fast-1
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

class ModelType(Enum):
    """Types de modèles disponibles"""
    MINIMAX_M2 = "minimax-M2"
    GROK_FAST = "grok-code-fast-1"

class TaskComplexity(Enum):
    """Niveaux de complexité des tâches"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EXPERT = "expert"

@dataclass
class ModelConfig:
    """Configuration d'un modèle"""
    model_type: ModelType
    name: str
    cost_per_token: float
    speed_score: float  # 0-1, 1 = très rapide
    quality_score: float  # 0-1, 1 = très haute qualité
    specialties: List[str]
    max_context_length: int
    timeout_seconds: int

@dataclass
class TaskRoutingDecision:
    """Décision de routage de tâche"""
    task_id: str
    recommended_model: ModelType
    confidence_score: float
    reasoning: List[str]
    fallback_model: Optional[ModelType] = None

class EcommerceModelRouter:
    """Routeur intelligent pour les modèles e-commerce"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._initialize_models()
        self._setup_routing_rules()
    
    def _initialize_models(self):
        """Initialise la configuration des modèles"""
        
        self.models = {
            ModelType.MINIMAX_M2: ModelConfig(
                model_type=ModelType.MINIMAX_M2,
                name="minimax-M2",
                cost_per_token=0.002,  # Coût par 1K tokens
                speed_score=0.6,  # Modéré
                quality_score=0.95,  # Très haute qualité
                specialties=[
                    "architecture_analysis", "security_audit", "performance_optimization",
                    "complex_refactoring", "advanced_patterns", "system_design"
                ],
                max_context_length=128000,
                timeout_seconds=180
            ),
            ModelType.GROK_FAST: ModelConfig(
                model_type=ModelType.GROK_FAST,
                name="grok-code-fast-1",
                cost_per_token=0.0,  # Gratuit
                speed_score=1.0,  # Très rapide
                quality_score=0.75,  # Bonne qualité
                specialties=[
                    "basic_coding", "documentation", "simple_tests",
                    "code_comments", "basic_optimization", "template_generation"
                ],
                max_context_length=64000,
                timeout_seconds=30
            )
        }
        
        self.logger.info("Modèles initialisés: minimax-M2, grok-code-fast-1")
    
    def _setup_routing_rules(self):
        """Configure les règles de routage"""
        
        # Règles basées sur la complexité de la tâche
        self.complexity_rules = {
            TaskComplexity.SIMPLE: {
                "primary_model": ModelType.GROK_FAST,
                "confidence_threshold": 0.3,
                "fallback_enabled": False
            },
            TaskComplexity.MODERATE: {
                "primary_model": ModelType.GROK_FAST,
                "confidence_threshold": 0.4,
                "fallback_enabled": True,
                "fallback_model": ModelType.MINIMAX_M2
            },
            TaskComplexity.COMPLEX: {
                "primary_model": ModelType.MINIMAX_M2,
                "confidence_threshold": 0.3,
                "fallback_enabled": True,
                "fallback_model": ModelType.GROK_FAST
            },
            TaskComplexity.EXPERT: {
                "primary_model": ModelType.MINIMAX_M2,
                "confidence_threshold": 0.4,
                "fallback_enabled": False
            }
        }
        
        # Règles spécifiques e-commerce
        self.ecommerce_task_rules = {
            # Frontend React
            "react_component_architecture": ModelType.MINIMAX_M2,
            "react_performance_optimization": ModelType.MINIMAX_M2,
            "react_state_management": ModelType.MINIMAX_M2,
            "react_simple_component": ModelType.GROK_FAST,
            "react_basic_styling": ModelType.GROK_FAST,
            
            # Backend Node.js
            "nodejs_api_architecture": ModelType.MINIMAX_M2,
            "nodejs_security_implementation": ModelType.MINIMAX_M2,
            "nodejs_performance_tuning": ModelType.MINIMAX_M2,
            "nodejs_simple_endpoint": ModelType.GROK_FAST,
            "nodejs_basic_middleware": ModelType.GROK_FAST,
            
            # MongoDB
            "mongodb_schema_design": ModelType.MINIMAX_M2,
            "mongodb_performance_optimization": ModelType.MINIMAX_M2,
            "mongodb_complex_aggregation": ModelType.MINIMAX_M2,
            "mongodb_simple_query": ModelType.GROK_FAST,
            "mongodb_basic_index": ModelType.GROK_FAST,
            
            # E-commerce spécifique
            "payment_integration": ModelType.MINIMAX_M2,
            "shopping_cart_logic": ModelType.MINIMAX_M2,
            "order_management": ModelType.MINIMAX_M2,
            "product_catalog_basic": ModelType.GROK_FAST,
            "user_auth_basic": ModelType.GROK_FAST,
            
            # DevOps
            "docker_configuration": ModelType.GROK_FAST,
            "ci_cd_pipeline": ModelType.GROK_FAST,
            "deployment_script": ModelType.GROK_FAST,
            "complex_infrastructure": ModelType.MINIMAX_M2
        }
        
        self.logger.info("Règles de routage configurées")
    
    def route_task(self, 
                   task_description: str,
                   task_type: str,
                   context: Optional[Dict[str, Any]] = None) -> TaskRoutingDecision:
        """
        Route une tâche vers le modèle optimal
        
        Args:
            task_description: Description de la tâche
            task_type: Type de tâche (ex: 'react_component_architecture')
            context: Contexte additionnel
        
        Returns:
            TaskRoutingDecision avec le modèle recommandé
        """
        
        try:
            # Analyse de la complexité
            complexity = self._analyze_task_complexity(task_description, task_type)
            
            # Application des règles e-commerce spécifiques
            ecommerce_model = self._check_ecommerce_rules(task_type)
            
            # Détermination du modèle final
            if ecommerce_model:
                recommended_model = ecommerce_model
                reasoning = [f"Règle e-commerce spécifique: {task_type}"]
            else:
                rules = self.complexity_rules[complexity]
                recommended_model = rules["primary_model"]
                reasoning = [f"Complexité {complexity.value} → {recommended_model.value}"]
            
            # Calcul du score de confiance
            confidence = self._calculate_confidence(task_description, recommended_model, context)
            
            # Vérification des seuils et fallbacks
            rules = self.complexity_rules[complexity]
            fallback_model = None
            
            if (confidence < rules["confidence_threshold"] and 
                rules["fallback_enabled"]):
                fallback_model = rules["fallback_model"]
                reasoning.append(f"Confiance faible ({confidence:.2f}) → fallback vers {fallback_model.value}")
                recommended_model = fallback_model
                confidence = confidence * 0.8  # Réduction de confiance pour fallback
            
            # Raisonnement final
            if not reasoning:
                reasoning = [f"Modèle par défaut: {recommended_model.value}"]
            
            reasoning.append(f"Confiance finale: {confidence:.2f}")
            
            return TaskRoutingDecision(
                task_id=f"task_{hash(task_description) % 10000}",
                recommended_model=recommended_model,
                confidence_score=confidence,
                reasoning=reasoning,
                fallback_model=fallback_model
            )
            
        except Exception as e:
            self.logger.error(f"Erreur lors du routage: {e}")
            # Fallback vers grok-code-fast-1 en cas d'erreur
            return TaskRoutingDecision(
                task_id=f"task_{hash(task_description) % 10000}",
                recommended_model=ModelType.GROK_FAST,
                confidence_score=0.3,
                reasoning=[f"Erreur de routage → fallback grok-code-fast-1: {str(e)}"],
                fallback_model=None
            )
    
    def _analyze_task_complexity(self, task_description: str, task_type: str) -> TaskComplexity:
        """Analyse la complexité d'une tâche"""
        
        # Mots-clés indicateurs de complexité
        complex_keywords = [
            "architecture", "design pattern", "optimization", "refactoring",
            "security", "performance", "scalability", "microservices"
        ]
        
        simple_keywords = [
            "simple", "basic", "template", "comment", "documentation",
            "unit test", "style", "format"
        ]
        
        text_lower = task_description.lower()
        
        # Comptage des mots-clés
        complex_count = sum(1 for keyword in complex_keywords if keyword in text_lower)
        simple_count = sum(1 for keyword in simple_keywords if keyword in text_lower)
        
        # Classification par règles
        if complex_count >= 2 or "architecture" in text_lower:
            return TaskComplexity.COMPLEX
        elif simple_count >= 2 and complex_count == 0:
            return TaskComplexity.SIMPLE
        elif complex_count >= 1:
            return TaskComplexity.MODERATE
        else:
            return TaskComplexity.MODERATE
    
    def _check_ecommerce_rules(self, task_type: str) -> Optional[ModelType]:
        """Vérifie les règles spécifiques e-commerce"""
        return self.ecommerce_task_rules.get(task_type)
    
    def _calculate_confidence(self, 
                            task_description: str, 
                            model: ModelType, 
                            context: Optional[Dict[str, Any]]) -> float:
        """Calcule le score de confiance pour le modèle"""
        
        base_confidence = 0.7
        
        # Bonus/malus basé sur les spécialités du modèle
        model_config = self.models[model]
        text_lower = task_description.lower()
        
        specialty_bonus = 0.0
        for specialty in model_config.specialties:
            if specialty in text_lower:
                specialty_bonus += 0.1
        
        # Ajustement selon la complexité
        complexity = self._analyze_task_complexity(task_description, "")
        if complexity == TaskComplexity.EXPERT and model == ModelType.MINIMAX_M2:
            specialty_bonus += 0.2
        elif complexity == TaskComplexity.SIMPLE and model == ModelType.GROK_FAST:
            specialty_bonus += 0.15
        
        # Facteur de qualité du modèle
        quality_factor = model_config.quality_score
        
        # Calcul final
        confidence = min(base_confidence + specialty_bonus, 1.0) * quality_factor
        
        return max(confidence, 0.1)  # Minimum 0.1
    
    def get_model_info(self, model_type: ModelType) -> ModelConfig:
        """Retourne les informations d'un modèle"""
        return self.models[model_type]
    
    def get_routing_statistics(self) -> Dict[str, Any]:
        """Retourne les statistiques de routage (simulation)"""
        return {
            "models_available": len(self.models),
            "routing_rules_count": len(self.ecommerce_task_rules),
            "complexity_levels": len(self.complexity_rules),
            "estimated_cost_savings": "65%",  # grok-code-fast-1 gratuit
            "quality_assurance": "minimax-M2 pour tâches critiques"
        }

# Configuration d'exemple pour intégration
EXAMPLE_ECMOMMERCE_TASKS = [
    {
        "description": "Créer l'architecture des composants React pour la page produit",
        "type": "react_component_architecture",
        "expected_model": "minimax-M2",
        "reasoning": "Architecture complexe nécessite modèle haute qualité"
    },
    {
        "description": "Ajouter les styles CSS pour le composant bouton",
        "type": "react_basic_styling", 
        "expected_model": "grok-code-fast-1",
        "reasoning": "Styling basique peut être géré par modèle rapide"
    },
    {
        "description": "Implémenter l'API REST pour la gestion des commandes",
        "type": "nodejs_api_architecture",
        "expected_model": "minimax-M2", 
        "reasoning": "Architecture API critique pour e-commerce"
    },
    {
        "description": "Créer un endpoint simple pour récupérer les produits",
        "type": "nodejs_simple_endpoint",
        "expected_model": "grok-code-fast-1",
        "reasoning": "Endpoint simple adapté au modèle rapide"
    },
    {
        "description": "Optimiser les requêtes MongoDB pour les filtres produits",
        "type": "mongodb_performance_optimization",
        "expected_model": "minimax-M2",
        "reasoning": "Optimisation performance critique"
    }
]

if __name__ == "__main__":
    # Test du routeur
    router = EcommerceModelRouter()
    
    print("=== Test du Routeur E-commerce ===")
    for task in EXAMPLE_ECMOMMERCE_TASKS:
        decision = router.route_task(task["description"], task["type"])
        print(f"\nTâche: {task['description']}")
        print(f"Modèle recommandé: {decision.recommended_model.value}")
        print(f"Confiance: {decision.confidence_score:.2f}")
        print(f"Raisonnement: {'; '.join(decision.reasoning)}")
        print(f"Attendu: {task['expected_model']} ✓" if decision.recommended_model.value == task["expected_model"] else f"Attendu: {task['expected_model']} ✗")
    
    print(f"\n=== Statistiques ===")
    stats = router.get_routing_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")