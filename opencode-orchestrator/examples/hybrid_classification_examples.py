"""
Exemples concrets d'utilisation de la classification hybride OpenCode
Démonstration des cas d'usage et des résultats
"""

import json
import time
from typing import Dict, List, Any
import logging

# Import des composants du système
from classifiers.keyword_classifier import KeywordClassifier
from classifiers.llm_classifier import LLMClassifier
from core.hybrid_fusion import HybridFusionEngine, FusionStrategy, FusionWeights
from core.routing_matrix import RoutingMatrix, RoutingStrategy

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HybridClassificationDemo:
    """Démonstrateur de la classification hybride OpenCode"""
    
    def __init__(self):
        self.keyword_classifier = KeywordClassifier()
        self.llm_classifier = LLMClassifier()
        self.fusion_engine = HybridFusionEngine()
        self.routing_matrix = RoutingMatrix()
        
        # Données d'exemple
        self.example_projects = self._load_example_projects()
    
    def _load_example_projects(self) -> Dict[str, Dict]:
        """Charge les exemples de projets pour la démonstration"""
        return {
            "ecommerce_web_app": {
                "name": "E-commerce Web Application",
                "text": """
# E-commerce Web Application

A modern e-commerce platform built with React and Node.js

## Features
- User authentication and authorization
- Product catalog with search and filtering
- Shopping cart and checkout process
- Payment integration with Stripe
- Order management system
- Admin dashboard

## Tech Stack
- Frontend: React 18, Redux, Material-UI
- Backend: Node.js, Express.js, MongoDB
- Authentication: JWT tokens
- Payments: Stripe API
- Testing: Jest, React Testing Library

## Project Structure
```
/src
  /components     # React components
  /pages         # Page components
  /services      # API services
  /utils         # Utility functions
  /tests         # Test files
```

## Installation
npm install
npm start

## Development
- npm run dev (development server)
- npm run test (run tests)
- npm run build (production build)
""",
                "context": {
                    "files": ["package.json", "README.md", "src/App.js", "server.js"],
                    "structure": "fullstack web application",
                    "technologies": ["React", "Node.js", "MongoDB", "Stripe"]
                },
                "expected_classification": {
                    "domain": "web_development",
                    "type": "web_application",
                    "complexity": "intermediate",
                    "phase": "development"
                }
            },
            
            "data_science_ml_project": {
                "name": "Machine Learning Data Analysis",
                "text": """
# ML Customer Churn Prediction

This project implements a machine learning solution to predict customer churn for a telecommunications company.

## Overview
Using historical customer data, we build predictive models to identify customers at risk of churning.

## Features
- Data preprocessing and cleaning
- Exploratory data analysis
- Feature engineering
- Multiple ML algorithms (Random Forest, XGBoost, Neural Networks)
- Model evaluation and comparison
- Prediction pipeline
- Model deployment with FastAPI

## Dataset
- Customer demographics
- Account information
- Service usage patterns
- Churn labels

## Technologies
- Python 3.9+
- pandas, numpy for data manipulation
- scikit-learn for machine learning
- XGBoost for gradient boosting
- TensorFlow for deep learning
- matplotlib, seaborn for visualization
- Jupyter notebooks for analysis
- FastAPI for model serving

## Model Performance
- Accuracy: 89.2%
- Precision: 87.5%
- Recall: 91.3%
- F1-Score: 89.4%

## Files
- data_preprocessing.py
- exploratory_analysis.ipynb
- model_training.py
- model_evaluation.py
- prediction_service.py
- requirements.txt
""",
                "context": {
                    "files": ["requirements.txt", "data_preprocessing.py", "model_training.py", "exploratory_analysis.ipynb"],
                    "structure": "machine learning project",
                    "technologies": ["Python", "pandas", "scikit-learn", "TensorFlow", "Jupyter"]
                },
                "expected_classification": {
                    "domain": "data_science",
                    "type": "library",
                    "complexity": "advanced",
                    "phase": "development"
                }
            },
            
            "mobile_app_react_native": {
                "name": "React Native Mobile App",
                "text": """
# Fitness Tracker Mobile App

A React Native mobile application for tracking fitness activities and health metrics.

## Features
- Step counting using device sensors
- Heart rate monitoring
- Workout logging and tracking
- Progress visualization
- Social features and challenges
- Integration with health apps

## Platform Support
- iOS 12+
- Android 8.0+

## Technology Stack
- React Native 0.68
- TypeScript for type safety
- Redux Toolkit for state management
- React Navigation for navigation
- AsyncStorage for local data
- Expo for development and building

## Key Components
- Fitness tracking service
- Chart visualization components
- User profile management
- Social feed component
- Settings and preferences

## Development Setup
npm install -g expo-cli
npm install
expo start

## Building
- iOS: expo build:ios
- Android: expo build:android

## Testing
- Unit tests with Jest
- Integration tests with Detox
- Manual testing on physical devices
""",
                "context": {
                    "files": ["package.json", "App.tsx", "src/screens", "src/components", "app.json"],
                    "structure": "mobile application",
                    "technologies": ["React Native", "TypeScript", "Redux", "Expo"]
                },
                "expected_classification": {
                    "domain": "mobile_development",
                    "type": "mobile_app",
                    "complexity": "intermediate",
                    "phase": "development"
                }
            },
            
            "devops_infrastructure": {
                "name": "DevOps Infrastructure Setup",
                "text": """
# Kubernetes Infrastructure as Code

Infrastructure setup for microservices application using Kubernetes and Terraform.

## Components
- Kubernetes cluster configuration
- Docker containerization
- CI/CD pipeline setup
- Monitoring and logging
- Security policies
- Backup and disaster recovery

## Tools and Technologies
- Kubernetes (k8s)
- Docker and Docker Compose
- Terraform for infrastructure
- Ansible for configuration management
- Jenkins for CI/CD
- Prometheus and Grafana for monitoring
- ELK stack for logging
- Helm charts for package management

## Infrastructure Components
- Load balancer configuration
- Auto-scaling groups
- Database clusters
- Cache layers (Redis)
- Message queues (RabbitMQ)
- SSL/TLS certificates

## Deployment Pipeline
1. Code commit triggers Jenkins build
2. Docker image creation and push to registry
3. Automated testing (unit, integration, e2e)
4. Security scanning
5. Deployment to staging environment
6. Automated testing in staging
7. Production deployment with blue-green strategy

## Monitoring
- Application performance monitoring
- Infrastructure monitoring
- Log aggregation and analysis
- Alerting and notification system
- Dashboard creation

## Security
- RBAC configuration
- Network policies
- Secret management
- Image vulnerability scanning
- Compliance monitoring
""",
                "context": {
                    "files": ["Dockerfile", "docker-compose.yml", "kubernetes/", "terraform/", "jenkinsfile"],
                    "structure": "infrastructure configuration",
                    "technologies": ["Kubernetes", "Docker", "Terraform", "Jenkins", "Prometheus"]
                },
                "expected_classification": {
                    "domain": "devops",
                    "type": "configuration",
                    "complexity": "advanced",
                    "phase": "deployment"
                }
            },
            
            "cybersecurity_audit": {
                "name": "Security Audit Tool",
                "text": """
# Web Application Security Scanner

Automated security scanning tool for web applications to identify vulnerabilities and compliance issues.

## Features
- SQL injection detection
- XSS vulnerability scanning
- CSRF protection analysis
- Authentication bypass testing
- Session management evaluation
- SSL/TLS configuration analysis
- OWASP Top 10 compliance checking
- Custom security rules engine

## Technologies
- Python 3.10+
- BeautifulSoup for HTML parsing
- Requests for HTTP communications
- Nmap for network scanning
- OpenSSL for SSL/TLS analysis
- SQLite for vulnerability database
- Flask for web interface
- Celery for background tasks

## Scanner Modules
- Web crawler for URL discovery
- Vulnerability scanner engine
- Report generator
- Database manager
- Configuration analyzer

## Security Checks
- Input validation testing
- Output encoding verification
- Access control testing
- Error handling analysis
- File upload security
- API security testing

## Output Formats
- JSON for programmatic use
- HTML reports for human review
- CSV for data analysis
- XML for integration with other tools

## Compliance Standards
- OWASP Top 10 2021
- SANS Top 25
- NIST Cybersecurity Framework
- ISO 27001 controls
""",
                "context": {
                    "files": ["scanner.py", "vulnerability_db.py", "report_generator.py", "requirements.txt"],
                    "structure": "security tool",
                    "technologies": ["Python", "BeautifulSoup", "Nmap", "Flask", "SQLite"]
                },
                "expected_classification": {
                    "domain": "cybersecurity",
                    "type": "cli_tool",
                    "complexity": "advanced",
                    "phase": "testing"
                }
            },
            
            "simple_tutorial": {
                "name": "Python Tutorial Example",
                "text": """
# Python Hello World Tutorial

A simple Python tutorial for beginners learning programming basics.

## What You'll Learn
- How to print text to the console
- Variables and data types
- Basic arithmetic operations
- Simple user input
- Conditional statements
- Basic loops

## Requirements
- Python 3.6 or higher
- No additional packages required

## Code Example
```python
# This is a comment
print("Hello, World!")

name = input("What's your name? ")
print(f"Nice to meet you, {name}!")

# Basic math
a = 10
b = 5
print(f"{a} + {b} = {a + b}")
print(f"{a} - {b} = {a - b}")
print(f"{a} * {b} = {a * b}")
print(f"{a} / {b} = {a / b}")
```

## How to Run
1. Save this code to a file named `hello.py`
2. Open terminal/command prompt
3. Navigate to the directory containing the file
4. Run: `python hello.py`

## Next Steps
- Learn about functions
- Explore data structures (lists, dictionaries)
- Practice with more complex programs
- Explore Python libraries
""",
                "context": {
                    "files": ["hello.py", "tutorial.md"],
                    "structure": "tutorial example",
                    "technologies": ["Python"]
                },
                "expected_classification": {
                    "domain": "web_development",  # Default domain for simple examples
                    "type": "script",
                    "complexity": "beginner",
                    "phase": "development"
                }
            }
        }
    
    def run_complete_classification_demo(self):
        """Lance une démonstration complète de classification hybride"""
        
        print("=" * 80)
        print("DÉMONSTRATION DE LA CLASSIFICATION HYBRIDE OPENCOD")
        print("=" * 80)
        print()
        
        for project_id, project_data in self.example_projects.items():
            print(f"\n{'='*60}")
            print(f"PROJET: {project_data['name']}")
            print(f"{'='*60}")
            
            # Classification par mots-clés
            print("\n1. CLASSIFICATION PAR MOTS-CLÉS")
            keyword_result = self.keyword_classifier.classify(
                project_data['text'], 
                project_data['context']
            )
            self._display_keyword_results(keyword_result)
            
            # Classification LLM
            print("\n2. CLASSIFICATION LLM")
            llm_result = self.llm_classifier.classify(
                project_data['text'], 
                project_data['context']
            )
            self._display_llm_results(llm_result)
            
            # Classification hybride
            print("\n3. CLASSIFICATION HYBRIDE")
            hybrid_result = self.fusion_engine.classify(
                project_data['text'], 
                project_data['context']
            )
            self._display_hybrid_results(hybrid_result)
            
            # Routage
            print("\n4. ROUTAGE INTELLIGENT")
            routing_decision = self.routing_matrix.route_project(
                hybrid_result, 
                project_data['context']
            )
            self._display_routing_decision(routing_decision)
            
            # Comparaison avec les attentes
            print("\n5. VALIDATION")
            self._validate_classification(hybrid_result, project_data['expected_classification'])
            
            print("\n" + "-"*60)
    
    def _display_keyword_results(self, result):
        """Affiche les résultats de classification par mots-clés"""
        print(f"Domaine: {result.domain}")
        print(f"Type: {result.type}")
        print(f"Complexité: {result.complexity}")
        print(f"Phase: {result.phase}")
        print(f"Confiance globale: {result.confidence:.2f}")
        print(f"Mots-clés trouvés: {result.matched_keywords}")
        print(f"Temps de traitement: {result.processing_time:.3f}s")
    
    def _display_llm_results(self, result):
        """Affiche les résultats de classification LLM"""
        print(f"Domaine: {result.domain} (confiance: {result.domain_confidence:.2f})")
        print(f"Type: {result.type} (confiance: {result.type_confidence:.2f})")
        print(f"Complexité: {result.complexity} (confiance: {result.complexity_confidence:.2f})")
        print(f"Phase: {result.phase} (confiance: {result.phase_confidence:.2f})")
        print(f"Confiance globale: {result.overall_confidence:.2f}")
        print(fRaisonnement: {result.reasoning}")
        print(f"Caractéristiques extraites: {result.extracted_features}")
        print(f"Suggestions: {result.suggestions}")
    
    def _display_hybrid_results(self, result):
        """Affiche les résultats de classification hybride"""
        print(f"Domaine final: {result.final_domain} (confiance: {result.final_domain_confidence:.2f})")
        print(f"Type final: {result.final_type} (confiance: {result.final_type_confidence:.2f})")
        print(f"Complexité finale: {result.final_complexity} (confiance: {result.final_complexity_confidence:.2f})")
        print(f"Phase finale: {result.final_phase} (confiance: {result.final_phase_confidence:.2f})")
        print(f"Confiance de fusion: {result.fusion_confidence:.2f}")
        print(f"Méthode de fusion: {result.fusion_method}")
        
        if result.conflict_analysis:
            conflict = result.conflict_analysis
            print(f"Conflits détectés: {conflict.has_conflict}")
            if conflict.has_conflict:
                print(f"Sévérité: {conflict.severity}")
                print(f"Dimensions en conflit: {conflict.conflicting_dimensions}")
                print(f"Recommandation: {conflict.recommendation}")
        
        print(f"Recommandations: {result.recommendations}")
        print(f"Temps de traitement: {result.processing_time:.3f}s")
    
    def _display_routing_decision(self, decision):
        """Affiche la décision de routage"""
        print(f"Cible sélectionnée: {decision.target.name}")
        print(f"Type de cible: {decision.target.type}")
        print(f"Confiance de routage: {decision.confidence:.2f}")
        print(f"Score de routage: {decision.routing_score:.2f}")
        print(f"Raisonnement: {decision.reasoning}")
        
        if decision.alternatives:
            print("Alternatives:")
            for alt_target, alt_score in decision.alternatives:
                print(f"  - {alt_target.name} (score: {alt_score:.2f})")
        
        # Détails de la cible
        print(f"Capacités: {decision.target.capabilities}")
        print(f"Expertise domaines: {decision.target.domain_expertise}")
        print(f"Score de performance: {decision.target.performance_score:.2f}")
        print(f"Disponibilité: {decision.target.availability:.2f}")
        print(f"Facteur de charge: {decision.target.load_factor:.2f}")
    
    def _validate_classification(self, result, expected):
        """Valide la classification contre les attentes"""
        matches = {}
        
        # Vérification du domaine
        domain_match = result.final_domain == expected['domain']
        matches['domaine'] = domain_match
        
        # Vérification du type
        type_match = result.final_type == expected['type']
        matches['type'] = type_match
        
        # Vérification de la complexité
        complexity_match = result.final_complexity == expected['complexity']
        matches['complexité'] = complexity_match
        
        # Vérification de la phase
        phase_match = result.final_phase == expected['phase']
        matches['phase'] = phase_match
        
        # Affichage des résultats
        print("Validation des classifications:")
        for dimension, match in matches.items():
            status = "✓" if match else "✗"
            print(f"  {status} {dimension.capitalize()}: {match}")
        
        accuracy = sum(matches.values()) / len(matches) * 100
        print(f"Précision globale: {accuracy:.1f}%")
    
    def run_performance_benchmark(self):
        """Lance un benchmark de performance"""
        print("\n" + "=" * 80)
        print("BENCHMARK DE PERFORMANCE")
        print("=" * 80)
        
        # Test sur différents textes de différentes tailles
        test_sizes = {
            "Petit (500 chars)": self.example_projects["simple_tutorial"]["text"][:500],
            "Moyen (2000 chars)": self.example_projects["ecommerce_web_app"]["text"][:2000],
            "Grand (5000+ chars)": self.example_projects["data_science_ml_project"]["text"]
        }
        
        results = {}
        
        for size_name, text in test_sizes.items():
            print(f"\nTest: {size_name}")
            
            # Benchmark classification par mots-clés
            start_time = time.time()
            keyword_result = self.keyword_classifier.classify(text)
            keyword_time = time.time() - start_time
            
            # Benchmark classification LLM
            start_time = time.time()
            llm_result = self.llm_classifier.classify(text)
            llm_time = time.time() - start_time
            
            # Benchmark classification hybride
            start_time = time.time()
            hybrid_result = self.fusion_engine.classify(text)
            hybrid_time = time.time() - start_time
            
            results[size_name] = {
                'keyword_time': keyword_time,
                'llm_time': llm_time,
                'hybrid_time': hybrid_time,
                'keyword_confidence': keyword_result.confidence,
                'llm_confidence': llm_result.overall_confidence,
                'hybrid_confidence': hybrid_result.fusion_confidence
            }
            
            print(f"  Mots-clés: {keyword_time:.3f}s (confiance: {keyword_result.confidence:.2f})")
            print(f"  LLM: {llm_time:.3f}s (confiance: {llm_result.overall_confidence:.2f})")
            print(f"  Hybride: {hybrid_time:.3f}s (confiance: {hybrid_result.fusion_confidence:.2f})")
        
        # Résumé des performances
        print("\nRÉSUMÉ DES PERFORMANCES:")
        print(f"{'Taille':<20} {'Mots-clés':<12} {'LLM':<12} {'Hybride':<12} {'Gain LLM':<10} {'Gain Hybride':<12}")
        print("-" * 80)
        
        for size_name, metrics in results.items():
            keyword_time = metrics['keyword_time']
            llm_time = metrics['llm_time']
            hybrid_time = metrics['hybrid_time']
            
            llm_gain = ((keyword_time - llm_time) / keyword_time) * 100 if keyword_time > 0 else 0
            hybrid_gain = ((keyword_time - hybrid_time) / keyword_time) * 100 if keyword_time > 0 else 0
            
            print(f"{size_name:<20} {keyword_time:<12.3f} {llm_time:<12.3f} {hybrid_time:<12.3f} "
                  f"{llm_gain:<10.1f}% {hybrid_gain:<12.1f}%")
    
    def run_conflict_resolution_demo(self):
        """Démontre la résolution des conflits entre classificateurs"""
        print("\n" + "=" * 80)
        print("DÉMONSTRATION DE RÉSOLUTION DE CONFLITS")
        print("=" * 80)
        
        # Projet avec contenu ambigu pour créer des conflits
        ambiguous_project = """
# Multi-Domain Project

This project involves web development, data analysis, and mobile components.

Features:
- React frontend for web interface
- Python backend with data processing
- Mobile app using React Native
- Machine learning components
- API services
- Database integration

The system processes user data, provides web dashboard, mobile interface, and ML predictions.
"""
        
        print("Projet ambigu détecté - Contenu multi-domaines")
        print("-" * 50)
        
        # Classification par mots-clés
        keyword_result = self.keyword_classifier.classify(ambiguous_project)
        print(f"Mots-clés - Domaine: {keyword_result.domain}")
        print(f"Mots-clés - Type: {keyword_result.type}")
        
        # Classification LLM
        llm_result = self.llm_classifier.classify(ambiguous_project)
        print(f"LLM - Domaine: {llm_result.domain}")
        print(f"LLM - Type: {llm_result.type}")
        
        # Détection des conflits
        keyword_top_domain = max(keyword_result.domain.items(), key=lambda x: x[1])[0]
        keyword_top_type = max(keyword_result.type.items(), key=lambda x: x[1])[0]
        
        conflicts = []
        if keyword_top_domain != llm_result.domain:
            conflicts.append(f"Domaine: '{keyword_top_domain}' vs '{llm_result.domain}'")
        if keyword_top_type != llm_result.type:
            conflicts.append(f"Type: '{keyword_top_type}' vs '{llm_result.type}'")
        
        print(f"\nConflits détectés:")
        for conflict in conflicts:
            print(f"  - {conflict}")
        
        # Classification hybride avec résolution
        hybrid_result = self.fusion_engine.classify(ambiguous_project)
        print(f"\nRésolution hybride:")
        print(f"  Domaine final: {hybrid_result.final_domain}")
        print(f"  Type final: {hybrid_result.final_type}")
        print(f"  Méthode de fusion: {hybrid_result.fusion_method}")
        
        if hybrid_result.conflict_analysis:
            print(f"  Sévérité du conflit: {hybrid_result.conflict_analysis.severity}")
            print(f"  Recommandation: {hybrid_result.conflict_analysis.recommendation}")
    
    def run_routing_optimization_demo(self):
        """Démontre l'optimisation du routage"""
        print("\n" + "=" * 80)
        print("DÉMONSTRATION D'OPTIMISATION DU ROUTAGE")
        print("=" * 80)
        
        # Test de routage pour différents types de projets
        test_cases = [
            {
                "name": "Projet Web Simple",
                "domain": "web_development",
                "type": "web_application",
                "complexity": "beginner",
                "phase": "development"
            },
            {
                "name": "Projet Data Science Avancé",
                "domain": "data_science",
                "type": "library",
                "complexity": "expert",
                "phase": "development"
            },
            {
                "name": "Projet Mobile Intermédiaire",
                "domain": "mobile_development",
                "type": "mobile_app",
                "complexity": "intermediate",
                "phase": "testing"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. {test_case['name']}")
            print("-" * 40)
            
            # Création d'un résultat de classification simulé
            class MockClassificationResult:
                def __init__(self, case):
                    self.final_domain = case['domain']
                    self.final_type = case['type']
                    self.final_complexity = case['complexity']
                    self.final_phase = case['phase']
                    self.fusion_confidence = 0.85
            
            mock_result = MockClassificationResult(test_case)
            
            # Routage
            routing_decision = self.routing_matrix.route_project(mock_result)
            
            print(f"Cible: {routing_decision.target.name}")
            print(f"Type: {routing_decision.target.type}")
            print(f"Confiance: {routing_decision.confidence:.2f}")
            print(f"Capacités: {routing_decision.target.capabilities}")
            
            if routing_decision.alternatives:
                print("Alternatives:")
                for alt_target, alt_score in routing_decision.alternatives:
                    print(f"  - {alt_target.name} ({alt_score:.2f})")
    
    def export_results(self, filename: str = "classification_results.json"):
        """Exporte les résultats de démonstration"""
        all_results = {}
        
        for project_id, project_data in self.example_projects.items():
            # Classification hybride
            hybrid_result = self.fusion_engine.classify(
                project_data['text'], 
                project_data['context']
            )
            
            # Routage
            routing_decision = self.routing_matrix.route_project(
                hybrid_result, 
                project_data['context']
            )
            
            # Compilation des résultats
            all_results[project_id] = {
                'project_info': {
                    'name': project_data['name'],
                    'expected_classification': project_data['expected_classification']
                },
                'classification': {
                    'domain': hybrid_result.final_domain,
                    'domain_confidence': hybrid_result.final_domain_confidence,
                    'type': hybrid_result.final_type,
                    'type_confidence': hybrid_result.final_type_confidence,
                    'complexity': hybrid_result.final_complexity,
                    'complexity_confidence': hybrid_result.final_complexity_confidence,
                    'phase': hybrid_result.final_phase,
                    'phase_confidence': hybrid_result.final_phase_confidence,
                    'fusion_confidence': hybrid_result.fusion_confidence,
                    'fusion_method': hybrid_result.fusion_method
                },
                'routing': {
                    'target': routing_decision.target.name,
                    'confidence': routing_decision.confidence,
                    'target_type': routing_decision.target.type,
                    'capabilities': routing_decision.target.capabilities
                },
                'metadata': {
                    'processing_time': hybrid_result.processing_time,
                    'conflict_analysis': hybrid_result.conflict_analysis.__dict__ if hybrid_result.conflict_analysis else None
                }
            }
        
        # Export en JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        
        print(f"Résultats exportés vers: {filename}")
        return all_results

def main():
    """Fonction principale de démonstration"""
    demo = HybridClassificationDemo()
    
    try:
        # Démonstration complète
        demo.run_complete_classification_demo()
        
        # Benchmark de performance
        demo.run_performance_benchmark()
        
        # Démonstration de résolution de conflits
        demo.run_conflict_resolution_demo()
        
        # Démonstration d'optimisation du routage
        demo.run_routing_optimization_demo()
        
        # Export des résultats
        results = demo.export_results("opencode_classification_demo_results.json")
        
        print("\n" + "=" * 80)
        print("DÉMONSTRATION TERMINÉE AVEC SUCCÈS")
        print("=" * 80)
        
        return results
        
    except Exception as e:
        logger.error(f"Erreur lors de la démonstration: {e}")
        raise

if __name__ == "__main__":
    main()
