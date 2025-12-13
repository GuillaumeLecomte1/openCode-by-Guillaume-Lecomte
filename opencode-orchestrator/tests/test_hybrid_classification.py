"""
Tests unitaires pour le système de classification hybride OpenCode
Validation des composants et intégration
"""

import unittest
import time
from unittest.mock import Mock, patch

from classifiers.keyword_classifier import KeywordClassifier, ClassificationResult
from classifiers.llm_classifier import LLMClassifier, LLMClassificationResult
from core.hybrid_fusion import HybridFusionEngine, FusionStrategy, FusionWeights
from core.routing_matrix import RoutingMatrix, RoutingStrategy, RoutingTarget, RoutingRule

class TestKeywordClassifier(unittest.TestCase):
    """Tests pour le classificateur par mots-clés"""
    
    def setUp(self):
        self.classifier = KeywordClassifier()
    
    def test_basic_classification(self):
        """Test de classification basique"""
        text = "React frontend application with TypeScript"
        result = self.classifier.classify(text)
        
        self.assertIsInstance(result, ClassificationResult)
        self.assertGreater(result.confidence, 0.0)
        self.assertIn('web_development', result.domain)
    
    def test_domain_classification(self):
        """Test de classification par domaine"""
        # Test web development
        web_text = "Angular SPA with REST API"
        web_result = self.classifier.classify(web_text)
        self.assertGreater(web_result.domain.get('web_development', 0), 0)
        
        # Test data science
        data_text = "Pandas data analysis with machine learning"
        data_result = self.classifier.classify(data_text)
        self.assertGreater(data_result.domain.get('data_science', 0), 0)
    
    def test_complexity_detection(self):
        """Test de détection de complexité"""
        # Test beginner
        beginner_text = "Hello world tutorial example"
        beginner_result = self.classifier.classify(beginner_text)
        self.assertGreater(beginner_result.complexity.get('beginner', 0), 0)
        
        # Test advanced
        advanced_text = "Microservices architecture with distributed systems"
        advanced_result = self.classifier.classify(advanced_text)
        self.assertGreater(advanced_result.complexity.get('advanced', 0), 0)
    
    def test_preprocessing(self):
        """Test du prétraitement de texte"""
        text = "  React   Frontend   Application  "
        processed = self.classifier._preprocess_text(text)
        
        self.assertNotIn("  ", processed)
        self.assertIn("react", processed)
        self.assertIn("frontend", processed)

class TestLLMClassifier(unittest.TestCase):
    """Tests pour le classificateur LLM"""
    
    def setUp(self):
        self.classifier = LLMClassifier()
    
    @patch('classifiers.llm_classifier.LLMClassifier._simulate_llm_response')
    def test_classification_response(self, mock_response):
        """Test de réponse de classification LLM"""
        # Configuration du mock
        mock_response.return_value = '''{
            "domain": "web_development",
            "domain_confidence": 0.85,
            "type": "web_application",
            "type_confidence": 0.90,
            "complexity": "intermediate",
            "complexity_confidence": 0.75,
            "phase": "development",
            "phase_confidence": 0.80,
            "overall_confidence": 0.83,
            "reasoning": "Test reasoning",
            "extracted_features": ["feature1"],
            "suggestions": ["suggestion1"]
        }'''
        
        text = "React application with API"
        result = self.classifier.classify(text)
        
        self.assertIsInstance(result, LLMClassificationResult)
        self.assertEqual(result.domain, "web_development")
        self.assertEqual(result.type, "web_application")
        self.assertGreater(result.overall_confidence, 0.0)
    
    def test_response_validation(self):
        """Test de validation des réponses"""
        # Réponse valide
        valid_response = '''{
            "domain": "web_development",
            "domain_confidence": 0.8,
            "type": "web_application",
            "type_confidence": 0.9,
            "complexity": "intermediate",
            "complexity_confidence": 0.7,
            "phase": "development",
            "phase_confidence": 0.8,
            "overall_confidence": 0.8,
            "reasoning": "Valid response"
        }'''
        
        validation_result = self.classifier._validate_and_normalize_response(valid_response)
        self.assertTrue(validation_result.is_valid)
        self.assertGreater(validation_result.confidence_score, 0.0)
    
    def test_invalid_response_handling(self):
        """Test de gestion des réponses invalides"""
        # Réponse invalide (JSON mal formé)
        invalid_response = '{"domain": "web_development", invalid json'
        
        validation_result = self.classifier._validate_and_normalize_response(invalid_response)
        self.assertFalse(validation_result.is_valid)
        self.assertGreater(len(validation_result.errors), 0)

class TestHybridFusion(unittest.TestCase):
    """Tests pour la fusion hybride"""
    
    def setUp(self):
        self.fusion_engine = HybridFusionEngine()
    
    def create_mock_keyword_result(self):
        """Crée un résultat mock de classification par mots-clés"""
        return ClassificationResult(
            domain={'web_development': 0.8, 'data_science': 0.2},
            type={'web_application': 0.9},
            complexity={'intermediate': 0.7},
            phase={'development': 0.8},
            confidence=0.75,
            matched_keywords=['react', 'api'],
            processing_time=0.1
        )
    
    def create_mock_llm_result(self):
        """Crée un résultat mock de classification LLM"""
        return LLMClassificationResult(
            domain="web_development",
            domain_confidence=0.85,
            type="web_application",
            type_confidence=0.90,
            complexity="intermediate",
            complexity_confidence=0.75,
            phase="development",
            phase_confidence=0.80,
            overall_confidence=0.83,
            reasoning="Mock LLM reasoning",
            extracted_features=["feature1"],
            suggestions=["suggestion1"],
            metadata={}
        )
    
    def test_weighted_average_fusion(self):
        """Test de fusion par moyenne pondérée"""
        keyword_result = self.create_mock_keyword_result()
        llm_result = self.create_mock_llm_result()
        
        result = self.fusion_engine._weighted_average_fusion(keyword_result, llm_result, None)
        
        self.assertEqual(result.final_domain, "web_development")
        self.assertEqual(result.final_type, "web_application")
        self.assertGreater(result.fusion_confidence, 0.0)
    
    def test_confidence_based_fusion(self):
        """Test de fusion basée sur la confiance"""
        keyword_result = self.create_mock_keyword_result()
        llm_result = self.create_mock_llm_result()
        
        result = self.fusion_engine._confidence_based_fusion(keyword_result, llm_result, None)
        
        self.assertIsNotNone(result.final_domain)
        self.assertIsNotNone(result.final_type)
        self.assertGreater(result.fusion_confidence, 0.0)
    
    def test_conflict_detection(self):
        """Test de détection de conflits"""
        keyword_result = self.create_mock_keyword_result()
        llm_result = self.create_mock_llm_result()
        
        # Modifier le résultat LLM pour créer un conflit
        llm_result.domain = "data_science"
        
        conflict_analysis = self.fusion_engine._analyze_conflicts(keyword_result, llm_result)
        
        self.assertTrue(conflict_analysis.has_conflict)
        self.assertIn("domain", conflict_analysis.conflicting_dimensions)
    
    def test_adaptive_fusion_strategy(self):
        """Test de la stratégie de fusion adaptative"""
        keyword_result = self.create_mock_keyword_result()
        llm_result = self.create_mock_llm_result()
        
        result = self.fusion_engine._adaptive_fusion(keyword_result, llm_result, None, "short text")
        
        self.assertIsNotNone(result.fusion_method)
        self.assertGreater(result.fusion_confidence, 0.0)

class TestRoutingMatrix(unittest.TestCase):
    """Tests pour la matrice de routage"""
    
    def setUp(self):
        self.routing_matrix = RoutingMatrix()
    
    def test_target_creation(self):
        """Test de création de cibles"""
        target = RoutingTarget(
            target_id="test_target",
            name="Test Target",
            type="human_resource",
            capabilities=["test_capability"],
            domain_expertise=["web_development"],
            complexity_support=["intermediate"],
            phase_support=["development"]
        )
        
        self.routing_matrix.add_routing_target(target)
        self.assertIn("test_target", self.routing_matrix.routing_targets)
    
    def test_routing_decision(self):
        """Test de décision de routage"""
        # Création d'un résultat de classification mock
        class MockClassificationResult:
            def __init__(self):
                self.final_domain = "web_development"
                self.final_type = "web_application"
                self.final_complexity = "intermediate"
                self.final_phase = "development"
                self.fusion_confidence = 0.8
        
        mock_result = MockClassificationResult()
        decision = self.routing_matrix.route_project(mock_result)
        
        self.assertIsNotNone(decision.target)
        self.assertGreater(decision.confidence, 0.0)
        self.assertIsNotNone(decision.reasoning)
    
    def test_rule_matching(self):
        """Test de correspondance de règles"""
        rule = RoutingRule(
            rule_id="test_rule",
            name="Test Rule",
            conditions={"domain": ["web_development"]},
            actions=["route_to_web_dev_specialist"],
            priority=1,
            weight=0.8
        )
        
        self.routing_matrix.add_routing_rule(rule)
        
        class MockClassificationResult:
            def __init__(self):
                self.final_domain = "web_development"
                self.final_type = "web_application"
                self.final_complexity = "intermediate"
                self.final_phase = "development"
                self.fusion_confidence = 0.8
        
        mock_result = MockClassificationResult()
        matched_rules = self.fusion_engine._apply_routing_rules(mock_result)
        
        # Note: Cette méthode est dans hybrid_fusion, pas routing_matrix
        # On teste juste que les règles peuvent être ajoutées
        self.assertIn("test_rule", self.routing_matrix.routing_rules)

class TestIntegration(unittest.TestCase):
    """Tests d'intégration du système complet"""
    
    def setUp(self):
        self.keyword_classifier = KeywordClassifier()
        self.llm_classifier = LLMClassifier()
        self.fusion_engine = HybridFusionEngine()
        self.routing_matrix = RoutingMatrix()
    
    @patch('classifiers.llm_classifier.LLMClassifier._simulate_llm_response')
    def test_complete_classification_pipeline(self, mock_response):
        """Test du pipeline complet de classification"""
        # Configuration du mock
        mock_response.return_value = '''{
            "domain": "web_development",
            "domain_confidence": 0.85,
            "type": "web_application",
            "type_confidence": 0.90,
            "complexity": "intermediate",
            "complexity_confidence": 0.75,
            "phase": "development",
            "phase_confidence": 0.80,
            "overall_confidence": 0.83,
            "reasoning": "Integration test reasoning",
            "extracted_features": ["feature1"],
            "suggestions": ["suggestion1"]
        }'''
        
        # Texte de test
        text = "React application with Node.js backend and MongoDB database"
        context = {
            "files": ["package.json", "server.js", "App.js"],
            "structure": "fullstack web application",
            "technologies": ["React", "Node.js", "MongoDB"]
        }
        
        # Pipeline complet
        # 1. Classification par mots-clés
        keyword_result = self.keyword_classifier.classify(text, context)
        self.assertGreater(keyword_result.confidence, 0.0)
        
        # 2. Classification LLM
        llm_result = self.llm_classifier.classify(text, context)
        self.assertEqual(llm_result.domain, "web_development")
        
        # 3. Fusion hybride
        hybrid_result = self.fusion_engine.classify(text, context)
        self.assertEqual(hybrid_result.final_domain, "web_development")
        self.assertGreater(hybrid_result.fusion_confidence, 0.0)
        
        # 4. Routage
        routing_decision = self.routing_matrix.route_project(hybrid_result, context)
        self.assertIsNotNone(routing_decision.target)
        self.assertGreater(routing_decision.confidence, 0.0)
        
        print(f"Pipeline complet réussi:")
        print(f"  Domaine: {hybrid_result.final_domain}")
        print(f"  Type: {hybrid_result.final_type}")
        print(f"  Complexité: {hybrid_result.final_complexity}")
        print(f"  Phase: {hybrid_result.final_phase}")
        print(f"  Confiance: {hybrid_result.fusion_confidence:.2f}")
        print(f"  Routage: {routing_decision.target.name}")
    
    def test_performance_benchmark(self):
        """Test de benchmark de performance"""
        text = "React frontend application with authentication and API integration"
        
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
        
        # Vérifications de performance
        self.assertLess(keyword_time, 1.0)  # Moins de 1 seconde
        self.assertLess(llm_time, 2.0)      # Moins de 2 secondes
        self.assertLess(hybrid_time, 3.0)   # Moins de 3 secondes
        
        print(f"Performances:")
        print(f"  Mots-clés: {keyword_time:.3f}s")
        print(f"  LLM: {llm_time:.3f}s")
        print(f"  Hybride: {hybrid_time:.3f}s")
    
    def test_error_handling(self):
        """Test de gestion d'erreurs"""
        # Test avec texte vide
        empty_result = self.fusion_engine.classify("")
        self.assertIsNotNone(empty_result.final_domain)
        self.assertTrue(empty_result.fallback_used or empty_result.fusion_confidence >= 0)
        
        # Test avec texte très long
        long_text = "React " * 1000  # Texte très long
        long_result = self.fusion_engine.classify(long_text)
        self.assertIsNotNone(long_result.final_domain)
        
        print(f"Gestion d'erreurs testée avec succès")

class TestConfiguration(unittest.TestCase):
    """Tests de configuration et paramètres"""
    
    def test_fusion_weights(self):
        """Test des poids de fusion"""
        weights = FusionWeights(
            keyword_weight=0.3,
            llm_weight=0.7,
            domain_weight=0.4,
            type_weight=0.3,
            complexity_weight=0.2,
            phase_weight=0.1
        )
        
        fusion_engine = HybridFusionEngine(fusion_weights=weights)
        self.assertEqual(fusion_engine.fusion_weights.keyword_weight, 0.3)
        self.assertEqual(fusion_engine.fusion_weights.llm_weight, 0.7)
    
    def test_routing_strategy(self):
        """Test des stratégies de routage"""
        routing_matrix = RoutingMatrix(RoutingStrategy.LOAD_BALANCED)
        self.assertEqual(routing_matrix.routing_strategy, RoutingStrategy.LOAD_BALANCED)
    
    def test_custom_targets(self):
        """Test d'ajout de cibles personnalisées"""
        matrix = RoutingMatrix()
        
        custom_target = RoutingTarget(
            target_id="custom_ai",
            name="Custom AI Tool",
            type="automated_tool",
            capabilities=["custom_capability"],
            domain_expertise=["custom_domain"],
            complexity_support=["beginner", "intermediate"],
            phase_support=["development"]
        )
        
        matrix.add_routing_target(custom_target)
        self.assertIn("custom_ai", matrix.routing_targets)

def run_comprehensive_tests():
    """Lance tous les tests de manière comprehensive"""
    print("=" * 80)
    print("LANCEMENT DES TESTS COMPREHENSIFS - CLASSIFICATION HYBRIDE OPENCOD")
    print("=" * 80)
    
    # Création de la suite de tests
    test_suite = unittest.TestSuite()
    
    # Ajout des tests
    test_classes = [
        TestKeywordClassifier,
        TestLLMClassifier,
        TestHybridFusion,
        TestRoutingMatrix,
        TestIntegration,
        TestConfiguration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Exécution des tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Résumé
    print("\n" + "=" * 80)
    print("RÉSUMÉ DES TESTS")
    print("=" * 80)
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Succès: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✓ TOUS LES TESTS ONT RÉUSSI!")
    else:
        print("✗ CERTAINS TESTS ONT ÉCHOUÉ:")
        for failure in result.failures:
            print(f"  ÉCHEC: {failure[0]}")
            print(f"    {failure[1]}")
        for error in result.errors:
            print(f"  ERREUR: {error[0]}")
            print(f"    {error[1]}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_comprehensive_tests()
    exit(0 if success else 1)
