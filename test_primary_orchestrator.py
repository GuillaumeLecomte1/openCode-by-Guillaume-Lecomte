#!/usr/bin/env python3
"""
Test de l'Orchestrateur Principal pour OpenCode
Script de test pour vérifier le bon fonctionnement de l'orchestrateur
"""

import sys
import os
import json
from pathlib import Path

# Ajouter le chemin vers l'orchestrateur
sys.path.append(str(Path(__file__).parent))

def test_orchestrator():
    try:
        # Import de l'orchestrateur autonome
        from autonomous_orchestrator import AutonomousOrchestrator, OrchestrationMode, OrchestrationStrategy
        
        print("✅ Import de l'orchestrateur réussi")
        
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
        - Gestion des stocks et inventaire
        - Interface d'administration
        """
        
        project_context = {
            "project_type": "ecommerce",
            "technologies": ["React", "Node.js", "MongoDB"],
            "complexity": "high",
            "timeline": "3_months"
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
- Confiance classification: {result.quality_metrics.get('classification_confidence', 0):.2f}

📝 **Recommandations**
{chr(10).join(f'  • {rec}' for rec in result.final_output.get('recommendations', []))}
        """)
        
        # Test des statistiques
        stats = orchestrator.get_statistics()
        print(f"""
📊 **STATISTIQUES GLOBALES**
- Orchestrations totales: {stats['total_orchestrations']}
- Taux de réussite: {stats.get('success_rate', 0):.2%}
- Qualité moyenne: {stats.get('average_quality', 0):.2f}
- Temps moyen: {stats.get('average_execution_time', 0):.2f}s
        """)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_availability():
    """Test de la disponibilité de l'agent"""
    agent_file = Path(__file__).parent / "agent" / "primary-orchestrator.md"
    
    if agent_file.exists():
        print("✅ Fichier agent trouvé")
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if "Primary Orchestrator" in content:
                print("✅ Contenu agent valide")
                return True
            else:
                print("❌ Contenu agent invalide")
                return False
    else:
        print("❌ Fichier agent non trouvé")
        return False

if __name__ == "__main__":
    print("🧪 **TEST DE L'ORCHESTRATEUR OPENCODE**")
    print("=" * 50)
    
    # Test 1: Disponibilité de l'agent
    print("\n1️⃣ Test de disponibilité de l'agent...")
    agent_ok = test_agent_availability()
    
    # Test 2: Fonctionnement de l'orchestrateur
    print("\n2️⃣ Test de fonctionnement de l'orchestrateur...")
    orchestrator_ok = test_orchestrator()
    
    # Résumé
    print("\n" + "=" * 50)
    print("📋 **RÉSUMÉ DES TESTS**")
    print(f"Agent disponible: {'✅' if agent_ok else '❌'}")
    print(f"Orchestrateur fonctionnel: {'✅' if orchestrator_ok else '❌'}")
    
    if agent_ok and orchestrator_ok:
        print("\n🎉 Tous les tests sont passés ! L'orchestrateur est prêt pour opencode.")
        print("\n📝 Instructions pour utiliser l'agent dans opencode:")
        print("1. Redémarrez opencode")
        print("2. Tapez: /primary-orchestrator")
        print("3. Décrivez votre projet e-commerce")
    else:
        print("\n⚠️ Certains tests ont échoué. Vérifiez la configuration.")