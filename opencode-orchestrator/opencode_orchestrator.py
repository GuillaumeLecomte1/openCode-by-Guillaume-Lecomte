#!/usr/bin/env python3
"""
Orchestrateur Principal OpenCode
Point d'entrée principal pour la classification hybride de projets
"""

import sys
import logging
import argparse
from typing import Dict, List, Any, Optional
import json
import time

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OpenCodeOrchestrator:
    """Orchestrateur principal du système de classification hybride"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialise l'orchestrateur avec la configuration"""
        
        # Configuration par défaut
        self.config = config or self._get_default_config()
        
        # Initialisation des composants
        self._initialize_components()
        
        # Métriques globales
        self.global_stats = {
            'total_classifications': 0,
            'successful_classifications': 0,
            'failed_classifications': 0,
            'total_processing_time': 0.0,
            'average_confidence': 0.0
        }
        
        logger.info("OpenCode Orchestrator initialisé avec succès")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Retourne la configuration par défaut"""
        return {
            'fusion_strategy': 'adaptive_fusion',
            'routing_strategy': 'hybrid_optimization',
            'enable_cache': True,
            'cache_size': 1000,
            'confidence_threshold': 0.5,
            'max_processing_time': 30.0,
            'enable_routing': True,
            'output_format': 'json',
            'verbose': False,
            'performance_monitoring': True
        }
    
    def _initialize_components(self):
        """Initialise tous les composants du système"""
        
        # Import des composants
        from classifiers.keyword_classifier import KeywordClassifier
        from classifiers.llm_classifier import LLMClassifier
        from core.hybrid_fusion import HybridFusionEngine, FusionStrategy
        from core.routing_matrix import RoutingMatrix, RoutingStrategy
        
        # Configuration des stratégies
        fusion_strategy = FusionStrategy(self.config['fusion_strategy'])
        routing_strategy = RoutingStrategy(self.config['routing_strategy'])
        
        # Initialisation des classificateurs
        self.keyword_classifier = KeywordClassifier()
        self.llm_classifier = LLMClassifier()
        
        # Initialisation du moteur de fusion
        self.fusion_engine = HybridFusionEngine(
            fusion_strategy=fusion_strategy,
            keyword_classifier=self.keyword_classifier,
            llm_classifier=self.llm_classifier
        )
        
        # Initialisation de la matrice de routage
        self.routing_matrix = RoutingMatrix(
            routing_strategy=routing_strategy
        )
        
        logger.info("Tous les composants initialisés")
    
    def classify_project(self, project_text: str, context: Dict[str, Any] = None,
                        enable_routing: bool = None) -> Dict[str, Any]:
        """
        Classification complète d'un projet
        
        Args:
            project_text: Texte du projet (README, code, etc.)
            context: Contexte additionnel
            enable_routing: Activer le routage (override la config)
        
        Returns:
            Résultat complet de classification et routage
        """
        
        start_time = time.time()
        should_route = enable_routing if enable_routing is not None else self.config['enable_routing']
        
        try:
            # Classification hybride
            logger.info("Début de la classification hybride")
            hybrid_result = self.fusion_engine.classify(
                project_text, 
                context, 
                use_cache=self.config['enable_cache']
            )
            
            # Routage si activé
            routing_result = None
            if should_route:
                logger.info("Début du routage intelligent")
                routing_result = self.routing_matrix.route_project(
                    hybrid_result, 
                    context
                )
            
            # Compilation du résultat final
            final_result = {
                'success': True,
                'classification': {
                    'domain': hybrid_result.final_domain,
                    'domain_confidence': hybrid_result.final_domain_confidence,
                    'type': hybrid_result.final_type,
                    'type_confidence': hybrid_result.final_type_confidence,
                    'complexity': hybrid_result.final_complexity,
                    'complexity_confidence': hybrid_result.final_complexity_confidence,
                    'phase': hybrid_result.final_phase,
                    'phase_confidence': hybrid_result.final_phase_confidence,
                    'overall_confidence': hybrid_result.fusion_confidence,
                    'fusion_method': hybrid_result.fusion_method,
                    'matched_keywords': hybrid_result.keyword_result.matched_keywords if hybrid_result.keyword_result else [],
                    'reasoning': hybrid_result.llm_result.reasoning if hybrid_result.llm_result else "No reasoning available"
                },
                'routing': self._format_routing_result(routing_result) if routing_result else None,
                'metadata': {
                    'processing_time': time.time() - start_time,
                    'timestamp': time.time(),
                    'config_used': self.config,
                    'component_versions': {
                        'keyword_classifier': '1.0',
                        'llm_classifier': '1.0',
                        'fusion_engine': '1.0',
                        'routing_matrix': '1.0'
                    }
                }
            }
            
            # Ajout des explications détaillées si mode verbeux
            if self.config['verbose']:
                final_result['explanations'] = {
                    'keyword_explanation': self.keyword_classifier.get_classification_explanation(hybrid_result.keyword_result) if hybrid_result.keyword_result else None,
                    'llm_explanation': self.llm_classifier.get_classification_explanation(hybrid_result.llm_result) if hybrid_result.llm_result else None,
                    'fusion_explanation': self.fusion_engine.get_fusion_explanation(hybrid_result),
                    'routing_explanation': self.routing_matrix.get_routing_explanation(routing_result) if routing_result else None
                }
            
            # Mise à jour des statistiques
            self._update_global_stats(final_result, True, time.time() - start_time)
            
            logger.info(f"Classification réussie en {final_result['metadata']['processing_time']:.3f}s")
            return final_result
            
        except Exception as e:
            logger.error(f"Erreur lors de la classification: {e}")
            
            # Résultat d'erreur
            error_result = {
                'success': False,
                'error': str(e),
                'classification': None,
                'routing': None,
                'metadata': {
                    'processing_time': time.time() - start_time,
                    'timestamp': time.time(),
                    'error_type': type(e).__name__
                }
            }
            
            # Mise à jour des statistiques
            self._update_global_stats(error_result, False, time.time() - start_time)
            
            return error_result
    
    def _format_routing_result(self, routing_result) -> Dict[str, Any]:
        """Formate le résultat de routage pour la sortie"""
        if not routing_result:
            return None
        
        return {
            'target_name': routing_result.target.name,
            'target_type': routing_result.target.type,
            'target_id': routing_result.target.target_id,
            'confidence': routing_result.confidence,
            'routing_score': routing_result.routing_score,
            'reasoning': routing_result.reasoning,
            'capabilities': routing_result.target.capabilities,
            'domain_expertise': routing_result.target.domain_expertise,
            'performance_score': routing_result.target.performance_score,
            'availability': routing_result.target.availability,
            'load_factor': routing_result.target.load_factor,
            'alternatives': [
                {
                    'name': alt[0].name,
                    'score': alt[1],
                    'capabilities': alt[0].capabilities
                }
                for alt in routing_result.alternatives
            ],
            'metadata': routing_result.metadata
        }
    
    def _update_global_stats(self, result: Dict[str, Any], success: bool, processing_time: float):
        """Met à jour les statistiques globales"""
        self.global_stats['total_classifications'] += 1
        
        if success:
            self.global_stats['successful_classifications'] += 1
            confidence = result.get('classification', {}).get('overall_confidence', 0.0)
            # Mise à jour de la confiance moyenne
            total_successful = self.global_stats['successful_classifications']
            current_avg = self.global_stats['average_confidence']
            self.global_stats['average_confidence'] = (
                (current_avg * (total_successful - 1) + confidence) / total_successful
            )
        else:
            self.global_stats['failed_classifications'] += 1
        
        self.global_stats['total_processing_time'] += processing_time
    
    def batch_classify(self, projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Classification par lots pour optimiser les performances
        
        Args:
            projects: Liste des projets avec 'text' et 'context' optionnel
        
        Returns:
            Liste des résultats de classification
        """
        logger.info(f"Début de la classification par lots de {len(projects)} projets")
        
        results = []
        for i, project in enumerate(projects, 1):
            logger.info(f"Traitement du projet {i}/{len(projects)}")
            
            result = self.classify_project(
                project['text'],
                project.get('context')
            )
            
            result['batch_position'] = i
            results.append(result)
        
        logger.info("Classification par lots terminée")
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retourne les statistiques globales du système"""
        stats = self.global_stats.copy()
        
        # Calculs additionnels
        if stats['total_classifications'] > 0:
            stats['success_rate'] = stats['successful_classifications'] / stats['total_classifications']
            stats['average_processing_time'] = stats['total_processing_time'] / stats['total_classifications']
        else:
            stats['success_rate'] = 0.0
            stats['average_processing_time'] = 0.0
        
        # Statistiques des composants
        stats['component_stats'] = {
            'keyword_classifier': {
                'processing_stats': self.keyword_classifier.processing_stats
            },
            'fusion_engine': {
                'fusion_stats': self.fusion_engine.fusion_stats
            },
            'routing_matrix': {
                'routing_stats': self.routing_matrix.routing_stats
            }
        }
        
        return stats
    
    def reset_statistics(self):
        """Remet à zéro les statistiques globales"""
        self.global_stats = {
            'total_classifications': 0,
            'successful_classifications': 0,
            'failed_classifications': 0,
            'total_processing_time': 0.0,
            'average_confidence': 0.0
        }
        logger.info("Statistiques remises à zéro")
    
    def export_configuration(self, filename: str = None) -> Dict[str, Any]:
        """Exporte la configuration actuelle"""
        config_export = {
            'current_config': self.config,
            'statistics': self.get_statistics(),
            'component_info': {
                'keyword_classifier': {
                    'domains_configured': len(self.keyword_classifier.config.DOMAINS),
                    'project_types_configured': len(self.keyword_classifier.config.PROJECT_TYPES),
                    'complexity_levels_configured': len(self.keyword_classifier.config.COMPLEXITY_LEVELS),
                    'phases_configured': len(self.keyword_classifier.config.PROJECT_PHASES)
                },
                'routing_matrix': {
                    'targets_configured': len(self.routing_matrix.routing_targets),
                    'rules_configured': len(self.routing_matrix.routing_rules)
                }
            }
        }
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(config_export, f, indent=2, ensure_ascii=False)
            logger.info(f"Configuration exportée vers {filename}")
        
        return config_export

def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(
        description="OpenCode Orchestrator - Classification Hybride de Projets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:

  # Classification simple
  python opencode_orchestrator.py --text "React application with Node.js backend"

  # Classification avec fichier
  python opencode_orchestrator.py --file README.md

  # Classification par lots
  python opencode_orchestrator.py --batch projects.json --output results.json

  # Mode verbeux avec routage
  python opencode_orchestrator.py --text "..." --verbose --enable-routing

  # Configuration personnalisée
  python opencode_orchestrator.py --config config.json --text "..."
        """
    )
    
    # Arguments d'entrée
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--text', type=str, help='Texte du projet à classifier')
    input_group.add_argument('--file', type=str, help='Fichier contenant le texte du projet')
    input_group.add_argument('--batch', type=str, help='Fichier JSON contenant plusieurs projets')
    
    # Arguments de configuration
    parser.add_argument('--config', type=str, help='Fichier de configuration JSON')
    parser.add_argument('--fusion-strategy', type=str, 
                       choices=['weighted_average', 'confidence_based', 'ensemble_voting', 'consensus_based', 'adaptive_fusion'],
                       help='Stratégie de fusion hybride')
    parser.add_argument('--routing-strategy', type=str,
                       choices=['capability_based', 'load_balanced', 'expertise_matching', 'hybrid_optimization', 'adaptive_routing'],
                       help='Stratégie de routage')
    
    # Arguments de fonctionnalités
    parser.add_argument('--enable-routing', action='store_true', help='Activer le routage intelligent')
    parser.add_argument('--disable-routing', action='store_true', help='Désactiver le routage')
    parser.add_argument('--verbose', action='store_true', help='Mode verbeux avec explications détaillées')
    parser.add_argument('--no-cache', action='store_true', help='Désactiver le cache')
    
    # Arguments de sortie
    parser.add_argument('--output', type=str, help='Fichier de sortie pour les résultats')
    parser.add_argument('--format', type=str, choices=['json', 'yaml', 'table'], default='json', help='Format de sortie')
    parser.add_argument('--stats', action='store_true', help='Afficher les statistiques')
    
    # Arguments utilitaires
    parser.add_argument('--export-config', type=str, help='Exporter la configuration vers un fichier')
    parser.add_argument('--reset-stats', action='store_true', help='Remettre à zéro les statistiques')
    
    args = parser.parse_args()
    
    # Chargement de la configuration
    config = {}
    if args.config:
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la configuration: {e}")
            sys.exit(1)
    
    # Configuration des options de ligne de commande
    if args.fusion_strategy:
        config['fusion_strategy'] = args.fusion_strategy
    if args.routing_strategy:
        config['routing_strategy'] = args.routing_strategy
    if args.verbose:
        config['verbose'] = True
    if args.no_cache:
        config['enable_cache'] = False
    if args.disable_routing:
        config['enable_routing'] = False
    elif args.enable_routing:
        config['enable_routing'] = True
    
    # Initialisation de l'orchestrateur
    try:
        orchestrator = OpenCodeOrchestrator(config)
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation: {e}")
        sys.exit(1)
    
    # Traitement des utilitaires
    if args.reset_stats:
        orchestrator.reset_statistics()
        print("Statistiques remises à zéro")
        return
    
    if args.export_config:
        orchestrator.export_configuration(args.export_config)
        print(f"Configuration exportée vers {args.export_config}")
        return
    
    if args.stats:
        stats = orchestrator.get_statistics()
        print(json.dumps(stats, indent=2, ensure_ascii=False))
        return
    
    # Traitement principal
    try:
        if args.text:
            # Classification simple
            result = orchestrator.classify_project(args.text, enable_routing=args.enable_routing)
            
        elif args.file:
            # Classification depuis fichier
            with open(args.file, 'r', encoding='utf-8') as f:
                project_text = f.read()
            result = orchestrator.classify_project(project_text, enable_routing=args.enable_routing)
            
        elif args.batch:
            # Classification par lots
            with open(args.batch, 'r', encoding='utf-8') as f:
                projects_data = json.load(f)
            
            if not isinstance(projects_data, list):
                logger.error("Le fichier de lot doit contenir une liste de projets")
                sys.exit(1)
            
            results = orchestrator.batch_classify(projects_data)
            
            # Formatage pour sortie
            if args.format == 'json':
                output_data = {
                    'batch_results': results,
                    'summary': {
                        'total_projects': len(results),
                        'successful': sum(1 for r in results if r['success']),
                        'failed': sum(1 for r in results if not r['success']),
                        'statistics': orchestrator.get_statistics()
                    }
                }
                result = output_data
            else:
                result = results
        
        # Sortie des résultats
        output_content = None
        
        if args.format == 'json':
            output_content = json.dumps(result, indent=2, ensure_ascii=False)
        elif args.format == 'yaml':
            try:
                import yaml
                output_content = yaml.dump(result, default_flow_style=False, allow_unicode=True)
            except ImportError:
                logger.error("PyYAML requis pour le format YAML. Installez avec: pip install PyYAML")
                sys.exit(1)
        elif args.format == 'table':
            output_content = format_table_result(result)
        
        # Affichage ou sauvegarde
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_content)
            print(f"Résultats sauvegardés dans {args.output}")
        else:
            print(output_content)
        
        # Affichage des statistiques si mode verbeux
        if args.verbose or args.stats:
            stats = orchestrator.get_statistics()
            print(f"\nStatistiques: {stats['total_classifications']} classifications, "
                  f"{stats['success_rate']:.1%} de réussite, "
                  f"{stats['average_processing_time']:.3f}s en moyenne")
    
    except Exception as e:
        logger.error(f"Erreur lors du traitement: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def format_table_result(result) -> str:
    """Formate les résultats en tableau"""
    if isinstance(result, dict) and 'batch_results' in result:
        # Format lot
        output = "RÉSULTATS DE CLASSIFICATION PAR LOTS\n"
        output += "=" * 80 + "\n"
        
        for i, project_result in enumerate(result['batch_results'], 1):
            if project_result['success']:
                classification = project_result['classification']
                output += f"Projet {i}: {classification['domain']} / {classification['type']} "
                output += f"(confiance: {classification['overall_confidence']:.2f})\n"
            else:
                output += f"Projet {i}: ERREUR - {project_result.get('error', 'Erreur inconnue')}\n"
        
        output += f"\nRésumé: {result['summary']['successful']}/{result['summary']['total_projects']} réussites"
        return output
    
    else:
        # Format simple
        if result.get('success'):
            classification = result['classification']
            output = f"Domaine: {classification['domain']} (confiance: {classification['domain_confidence']:.2f})\n"
            output += f"Type: {classification['type']} (confiance: {classification['type_confidence']:.2f})\n"
            output += f"Complexité: {classification['complexity']} (confiance: {classification['complexity_confidence']:.2f})\n"
            output += f"Phase: {classification['phase']} (confiance: {classification['phase_confidence']:.2f})\n"
            output += f"Confiance globale: {classification['overall_confidence']:.2f}\n"
            
            if result.get('routing'):
                routing = result['routing']
                output += f"Routage: {routing['target_name']} (confiance: {routing['confidence']:.2f})\n"
            
            return output
        else:
            return f"ERREUR: {result.get('error', 'Erreur inconnue')}"

if __name__ == "__main__":
    main()
