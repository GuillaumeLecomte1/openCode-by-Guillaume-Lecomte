#!/usr/bin/env python3
"""
Script d'intégration pour l'Orchestrateur Principal OpenCode
Permet d'utiliser l'orchestrateur multi-dispatch depuis l'interface opencode
"""

import sys
import os
import json
from pathlib import Path

# Ajouter le chemin vers l'orchestrateur
sys.path.append(str(Path(__file__).parent / "opencode-orchestrator" / "multi_dispatch"))

def call_primary_orchestrator(task_description: str, project_context: dict = None) -> dict:
    """
    Appelle l'orchestrateur principal pour une tâche donnée
    
    Args:
        task_description: Description de la tâche à accomplir
        project_context: Contexte additionnel du projet
    
    Returns:
        Résultat de l'orchestration
    """
    try:
        from primary_orchestrator import PrimaryMultiDispatchOrchestrator, OrchestrationMode, OrchestrationStrategy
        
        # Créer l'orchestrateur
        orchestrator = PrimaryMultiDispatchOrchestrator(
            orchestration_mode=OrchestrationMode.INTELLIGENT,
            orchestration_strategy=OrchestrationStrategy.BALANCED
        )
        
        # Exécuter l'orchestration
        result = orchestrator.orchestrate(
            project_text=task_description,
            project_context=project_context or {},
            user_constraints={'source': 'opencode'},
            task_executor=None  # Utilise l'exécuteur par défaut
        )
        
        return {
            'success': result.success,
            'output': result.final_output,
            'metadata': result.orchestration_metadata,
            'quality_metrics': result.quality_metrics,
            'execution_time': result.execution_time,
            'error': result.error_details if not result.success else None
        }
        
    except ImportError as e:
        return {
            'success': False,
            'error': f"Erreur d'import: {str(e)}",
            'output': {},
            'metadata': {},
            'quality_metrics': {},
            'execution_time': 0.0
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Erreur d'orchestration: {str(e)}",
            'output': {},
            'metadata': {},
            'quality_metrics': {},
            'execution_time': 0.0
        }

def format_result(result: dict) -> str:
    """Formate le résultat pour l'affichage"""
    if not result['success']:
        return f"❌ Erreur: {result.get('error', 'Erreur inconnue')}"
    
    output = result['output']
    metadata = result['metadata']
    
    formatted = f"""
🎯 **Orchestration Terminée avec Succès**

📊 **Résumé du Projet**
- Domaine: {output.get('project_analysis', {}).get('domain', 'N/A')}
- Type: {output.get('project_analysis', {}).get('type', 'N/A')}
- Complexité: {output.get('project_analysis', {}).get('complexity', 'N/A')}
- Confiance: {output.get('project_analysis', {}).get('confidence', 'N/A')}

🔄 **Routage**
- Cible: {output.get('routing', {}).get('target', 'N/A')}
- Confiance: {output.get('routing', {}).get('confidence', 'N/A')}

⚡ **Exécution**
- Tâches totales: {output.get('execution_summary', {}).get('total_tasks', 0)}
- Tâches réussies: {output.get('execution_summary', {}).get('successful_tasks', 0)}
- Tâches échouées: {output.get('execution_summary', {}).get('failed_tasks', 0)}

🏆 **Qualité**
- Qualité globale: {output.get('quality_assessment', {}).get('overall_quality', 'N/A')}
- Score de confiance: {output.get('quality_assessment', {}).get('confidence_score', 'N/A')}
- Conflits résolus: {output.get('quality_assessment', {}).get('conflicts_resolved', 0)}

⏱️ **Performance**
- Temps d'exécution: {result['execution_time']:.2f}s
- Mode d'orchestration: {metadata.get('orchestration_mode', 'N/A')}
- Stratégie: {metadata.get('orchestration_strategy', 'N/A')}
- Agents utilisés: {metadata.get('agents_count', 0)}
- Tâches planifiées: {metadata.get('tasks_count', 0)}
"""
    
    return formatted

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python primary_orchestrator_integration.py 'description de la tâche'")
        sys.exit(1)
    
    task_description = sys.argv[1]
    project_context = {}
    
    # Parser les arguments supplémentaires
    if len(sys.argv) > 2:
        try:
            project_context = json.loads(sys.argv[2])
        except:
            pass
    
    print("🚀 Initialisation de l'Orchestrateur Principal...")
    result = call_primary_orchestrator(task_description, project_context)
    print(format_result(result))