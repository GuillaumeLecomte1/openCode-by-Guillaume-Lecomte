#!/usr/bin/env python3
"""
Exemple d'utilisation de l'Orchestrateur Multi-Dispatch Intelligent
Démonstration des capacités de coordination multi-agents
"""

import logging
import json
from .simple_orchestrator import create_orchestrator, OrchestrationMode

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def demo_orchestrator():
    """Démonstration de l'orchestrateur multi-dispatch"""
    
    print("=== Démonstration de l'Orchestrateur Multi-Dispatch Intelligent ===\n")
    
    # Création de l'orchestrateur
    orchestrator = create_orchestrator(OrchestrationMode.INTELLIGENT)
    
    # Exemple 1: Projet Web Complexe
    print("1. Test avec un projet web complexe")
    web_project = """
    E-commerce Web Application
    
    This is a modern React-based e-commerce platform with Node.js backend.
    
    Features:
    - User authentication and authorization
    - Product catalog with search and filtering
    - Shopping cart and checkout process
    - Payment integration with Stripe
    - Admin dashboard for product management
    
    Tech Stack:
    - Frontend: React 18, Redux Toolkit, Material-UI
    - Backend: Node.js, Express.js, MongoDB
    - Authentication: JWT tokens, OAuth2
    - Deployment: Docker, Kubernetes, AWS
    
    The project is in active development phase and requires multiple specialists:
    - Frontend developer for React components
    - Backend developer for API endpoints
    - DevOps engineer for deployment automation
    - UI/UX designer for interface improvements
    """
    
    web_context = {
        'technologies': ['React', 'Node.js', 'MongoDB', 'AWS', 'Docker'],
        'complexity': 'advanced',
        'phase': 'development',
        'team_size': 4,
        'performance_requirements': {
            'max_execution_time': 600.0,
            'min_success_rate': 0.9
        }
    }
    
    result1 = orchestrator.orchestrate(web_project, web_context)
    
    print(f"✓ Classification: {result1.classification.final_domain} / {result1.classification.final_type}")
    print(f"✓ Routage: {result1.routing_decision.target.name if result1.routing_decision else 'N/A'}")
    print(f"✓ Agents sélectionnés: {len(result1.agent_selection)}")
    print(f"✓ Mode de dispatch: {result1.dispatch_plan.mode.value}")
    print(f"✓ Tâches exécutées: {len(result1.execution_results['task_results'])}")
    print(f"✓ Score de qualité: {result1.quality_metrics['overall_quality']:.2f}")
    print(f"✓ Temps d'exécution: {result1.execution_time:.2f}s\n")
    
    # Exemple 2: Projet Data Science
    print("2. Test avec un projet data science")
    data_project = """
    Machine Learning Customer Churn Prediction
    
    This project implements a comprehensive machine learning solution to predict customer churn.
    
    Features:
    - Data preprocessing and feature engineering
    - Exploratory data analysis with visualizations
    - Multiple ML algorithms (Random Forest, XGBoost, Neural Networks)
    - Model evaluation and comparison
    - Automated model retraining pipeline
    
    Technologies:
    - Python 3.9+, pandas, numpy, scikit-learn
    - XGBoost for gradient boosting
    - TensorFlow for deep learning
    - Jupyter notebooks for analysis
    - MLflow for experiment tracking
    
    The project is in the modeling phase and needs:
    - Data scientist for feature engineering
    - ML engineer for model deployment
    - Data analyst for business insights
    """
    
    data_context = {
        'technologies': ['Python', 'scikit-learn', 'XGBoost', 'TensorFlow'],
        'complexity': 'expert',
        'phase': 'development',
        'team_size': 3
    }
    
    result2 = orchestrator.orchestrate(data_project, data_context)
    
    print(f"✓ Classification: {result2.classification.final_domain} / {result2.classification.final_type}")
    print(f"✓ Routage: {result2.routing_decision.target.name if result2.routing_decision else 'N/A'}")
    print(f"✓ Agents sélectionnés: {len(result2.agent_selection)}")
    print(f"✓ Mode de dispatch: {result2.dispatch_plan.mode.value}")
    print(f"✓ Tâches exécutées: {len(result2.execution_results['task_results'])}")
    print(f"✓ Score de qualité: {result2.quality_metrics['overall_quality']:.2f}")
    print(f"✓ Temps d'exécution: {result2.execution_time:.2f}s\n")
    
    # Exemple 3: Projet Mobile Simple
    print("3. Test avec un projet mobile simple")
    mobile_project = """
    Simple Mobile Task Manager
    
    A basic task management mobile application for personal use.
    
    Features:
    - Add, edit, delete tasks
    - Set due dates and priorities
    - Simple local storage
    - Clean, minimal UI
    
    Tech Stack:
    - React Native
    - AsyncStorage for local data
    - Basic React Native components
    
    This is a beginner-level project that should be straightforward to implement.
    """
    
    mobile_context = {
        'technologies': ['React Native'],
        'complexity': 'beginner',
        'phase': 'development',
        'team_size': 1
    }
    
    result3 = orchestrator.orchestrate(mobile_project, mobile_context)
    
    print(f"✓ Classification: {result3.classification.final_domain} / {result3.classification.final_type}")
    print(f"✓ Routage: {result3.routing_decision.target.name if result3.routing_decision else 'N/A'}")
    print(f"✓ Agents sélectionnés: {len(result3.agent_selection)}")
    print(f"✓ Mode de dispatch: {result3.dispatch_plan.mode.value}")
    print(f"✓ Tâches exécutées: {len(result3.execution_results['task_results'])}")
    print(f"✓ Score de qualité: {result3.quality_metrics['overall_quality']:.2f}")
    print(f"✓ Temps d'exécution: {result3.execution_time:.2f}s\n")
    
    # Affichage des statistiques globales
    print("=== Statistiques Globales ===")
    stats = orchestrator.get_statistics()
    print(f"Total orchestrations: {stats['total_orchestrations']}")
    print(f"Taux de réussite: {stats.get('success_rate', 0):.2%}")
    print(f"Temps moyen: {stats.get('average_execution_time', 0):.2f}s\n")
    
    # Sauvegarde des résultats
    results_summary = {
        'web_project': {
            'domain': result1.classification.final_domain,
            'confidence': result1.classification.fusion_confidence,
            'agents_count': len(result1.agent_selection),
            'dispatch_mode': result1.dispatch_plan.mode.value,
            'quality_score': result1.quality_metrics['overall_quality']
        },
        'data_project': {
            'domain': result2.classification.final_domain,
            'confidence': result2.classification.fusion_confidence,
            'agents_count': len(result2.agent_selection),
            'dispatch_mode': result2.dispatch_plan.mode.value,
            'quality_score': result2.quality_metrics['overall_quality']
        },
        'mobile_project': {
            'domain': result3.classification.final_domain,
            'confidence': result3.classification.fusion_confidence,
            'agents_count': len(result3.agent_selection),
            'dispatch_mode': result3.dispatch_plan.mode.value,
            'quality_score': result3.quality_metrics['overall_quality']
        },
        'global_statistics': stats
    }
    
    with open('orchestration_results.json', 'w', encoding='utf-8') as f:
        json.dump(results_summary, f, indent=2, ensure_ascii=False)
    
    print("✓ Résultats sauvegardés dans 'orchestration_results.json'")
    
    return results_summary

def test_error_handling():
    """Test de la gestion d'erreurs"""
    
    print("\n=== Test de Gestion d'Erreurs ===")
    
    orchestrator = create_orchestrator()
    
    # Test avec un projet invalide
    try:
        invalid_result = orchestrator.orchestrate("", {})
        print(f"✓ Gestion d'erreur réussie: {invalid_result.success}")
        print(f"✓ Message d'erreur: {invalid_result.final_output.get('error', 'N/A')}")
    except Exception as e:
        print(f"✗ Erreur non gérée: {e}")

if __name__ == "__main__":
    # Exécution de la démonstration
    demo_orchestrator()
    
    # Test de gestion d'erreurs
    test_error_handling()
    
    print("\n=== Démonstration Terminée ===")