#!/usr/bin/env python3
"""
Test rapide de l'Orchestrateur Principal pour OpenCode
"""

import sys
from pathlib import Path

# Ajouter le répertoire courant au path
sys.path.append(str(Path.cwd()))

def quick_test():
    try:
        from autonomous_orchestrator import AutonomousOrchestrator, OrchestrationMode, OrchestrationStrategy
        
        print("✅ Import réussi")
        
        # Création de l'orchestrateur
        orchestrator = AutonomousOrchestrator(
            orchestration_mode=OrchestrationMode.INTELLIGENT,
            orchestration_strategy=OrchestrationStrategy.BALANCED
        )
        
        print("✅ Orchestrateur créé avec succès")
        
        # Test avec un projet e-commerce
        test_project = """
        Je veux créer une marketplace e-commerce complète avec :
        - Frontend React avec Redux pour la gestion d'état
        - Backend Node.js avec Express et API REST
        - Base de données MongoDB pour les produits et commandes
        - Système de paiement Stripe intégré
        """
        
        project_context = {
            "project_type": "ecommerce",
            "technologies": ["React", "Node.js", "MongoDB"],
            "complexity": "high"
        }
        
        print("🚀 Lancement de l'orchestration...")
        
        # Exécution de l'orchestration
        result = orchestrator.orchestrate(
            project_text=test_project,
            project_context=project_context,
            user_constraints={"budget": "medium", "quality": "high"}
        )
        
        print("✅ Orchestration terminée")
        
        # Affichage des résultats
        print(f"""
🎯 **RÉSULTAT DE L'ORCHESTRATION**

📊 **Statut**: {'✅ Succès' if result.success else '❌ Échec'}
⏱️ **Temps d'exécution**: {result.execution_time:.2f}s

📋 **Analyse du Projet**
- Domaine: {result.final_output.get('project_analysis', {}).get('domain', 'N/A')}
- Type: {result.final_output.get('project_analysis', {}).get('type', 'N/A')}
- Complexité: {result.final_output.get('project_analysis', {}).get('complexity', 'N/A')}

🤖 **Agents Sélectionnés**
{chr(10).join(f'  • {agent}' for agent in result.agent_selection)}

📈 **Métriques de Qualité**
- Score global: {result.quality_metrics.get('overall_quality', 0):.2f}
- Taux de réussite: {result.quality_metrics.get('execution_success_rate', 0):.2f}

📝 **Recommandations**
{chr(10).join(f'  • {rec}' for rec in list(result.final_output.get('recommendations', []))[:3])}
        """)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 **TEST RAPIDE DE L'ORCHESTRATEUR**")
    print("=" * 40)
    
    success = quick_test()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 Orchestrateur fonctionne parfaitement !")
        print("\n📝 Instructions pour l'utiliser dans opencode:")
        print("1. Votre agent primary-orchestrator est prêt")
        print("2. Redémarrez opencode pour qu'il soit détecté")
        print("3. Utilisez: /primary-orchestrator")
        print("4. Décrivez votre projet e-commerce")
    else:
        print("⚠️ Des erreurs ont été détectées")