"""
Matrice de routage multi-critères pour l'Orchestrateur OpenCode
Système de correspondance et optimisation pour le routage intelligent
"""

import logging
from typing import Dict, List, Tuple, Optional, Any, NamedTuple
from dataclasses import dataclass, field
from enum import Enum
import json
import numpy as np
from collections import defaultdict

from .hybrid_fusion import HybridClassificationResult

@dataclass
class RoutingRule:
    """Règle de routage avec conditions et actions"""
    rule_id: str
    name: str
    conditions: Dict[str, Any]
    actions: List[str]
    priority: int
    weight: float
    enabled: bool = True
    description: str = ""

@dataclass
class RoutingTarget:
    """Cible de routage (ressource, service, etc.)"""
    target_id: str
    name: str
    type: str
    capabilities: List[str]
    domain_expertise: List[str]
    complexity_support: List[str]
    phase_support: List[str]
    load_factor: float = 1.0
    availability: float = 1.0
    performance_score: float = 0.8

@dataclass
class RoutingDecision:
    """Décision de routage prise par le système"""
    target: RoutingTarget
    confidence: float
    routing_score: float
    reasoning: str
    alternatives: List[Tuple[RoutingTarget, float]]
    metadata: Dict[str, Any] = field(default_factory=dict)

class RoutingStrategy(Enum):
    """Stratégies de routage disponibles"""
    CAPABILITY_BASED = "capability_based"
    LOAD_BALANCED = "load_balanced"
    EXPERTISE_MATCHING = "expertise_matching"
    HYBRID_OPTIMIZATION = "hybrid_optimization"
    ADAPTIVE_ROUTING = "adaptive_routing"

class RoutingMatrix:
    """Matrice de routage multi-critères principale"""
    
    def __init__(self, routing_strategy: RoutingStrategy = RoutingStrategy.HYBRID_OPTIMIZATION):
        self.routing_strategy = routing_strategy
        self.logger = logging.getLogger(__name__)
        
        # Initialisation des données
        self.routing_rules: Dict[str, RoutingRule] = {}
        self.routing_targets: Dict[str, RoutingTarget] = {}
        self.domain_mappings: Dict[str, List[str]] = {}
        self.complexity_mappings: Dict[str, List[str]] = {}
        self.phase_mappings: Dict[str, List[str]] = {}
        
        # Matrices de correspondance
        self.correspondence_matrices = {}
        
        # Métriques de performance
        self.routing_stats = {
            'total_routing_decisions': 0,
            'successful_routes': 0,
            'failed_routes': 0,
            'average_routing_time': 0.0,
            'strategy_usage': {strategy.value: 0 for strategy in RoutingStrategy}
        }
        
        # Cache pour les décisions
        self._routing_cache = {}
        
        # Initialisation des données par défaut
        self._initialize_default_data()
    
    def _initialize_default_data(self):
        """Initialise les données par défaut du système de routage"""
        
        # ==================== CIBLES DE ROUTAGE PAR DÉFAUT ====================
        
        # Développeurs spécialisés par domaine
        web_dev_target = RoutingTarget(
            target_id="web_dev_specialist",
            name="Développeur Web Spécialisé",
            type="human_resource",
            capabilities=["frontend", "backend", "fullstack", "api_development"],
            domain_expertise=["web_development"],
            complexity_support=["beginner", "intermediate", "advanced"],
            phase_support=["development", "testing", "deployment"],
            load_factor=0.7,
            availability=0.9,
            performance_score=0.85
        )
        
        data_science_target = RoutingTarget(
            target_id="data_scientist",
            name="Data Scientist",
            type="human_resource",
            capabilities=["machine_learning", "data_analysis", "statistical_modeling"],
            domain_expertise=["data_science"],
            complexity_support=["intermediate", "advanced", "expert"],
            phase_support=["development", "testing", "deployment"],
            load_factor=0.6,
            availability=0.8,
            performance_score=0.90
        )
        
        mobile_dev_target = RoutingTarget(
            target_id="mobile_dev_specialist",
            name="Développeur Mobile Spécialisé",
            type="human_resource",
            capabilities=["android_development", "ios_development", "react_native", "flutter"],
            domain_expertise=["mobile_development"],
            complexity_support=["intermediate", "advanced"],
            phase_support=["development", "testing", "deployment"],
            load_factor=0.8,
            availability=0.85,
            performance_score=0.88
        )
        
        devops_target = RoutingTarget(
            target_id="devops_engineer",
            name="Ingénieur DevOps",
            type="human_resource",
            capabilities=["infrastructure", "automation", "ci_cd", "monitoring"],
            domain_expertise=["devops"],
            complexity_support=["intermediate", "advanced", "expert"],
            phase_support=["deployment", "maintenance", "planning"],
            load_factor=0.5,
            availability=0.9,
            performance_score=0.92
        )
        
        # Outils automatisés
        code_generator_tool = RoutingTarget(
            target_id="code_generator_ai",
            name="Générateur de Code IA",
            type="automated_tool",
            capabilities=["code_generation", "template_creation", "boilerplate"],
            domain_expertise=["web_development", "data_science", "mobile_development"],
            complexity_support=["beginner", "intermediate"],
            phase_support=["development"],
            load_factor=0.2,
            availability=0.95,
            performance_score=0.75
        )
        
        security_scanner = RoutingTarget(
            target_id="security_scanner",
            name="Scanner de Sécurité",
            type="automated_tool",
            capabilities=["security_analysis", "vulnerability_detection", "compliance_check"],
            domain_expertise=["cybersecurity"],
            complexity_support=["intermediate", "advanced"],
            phase_support=["testing", "deployment"],
            load_factor=0.1,
            availability=0.98,
            performance_score=0.85
        )
        
        # Ajout des cibles
        self.routing_targets = {
            "web_dev_specialist": web_dev_target,
            "data_scientist": data_science_target,
            "mobile_dev_specialist": mobile_dev_target,
            "devops_engineer": devops_target,
            "code_generator_ai": code_generator_tool,
            "security_scanner": security_scanner
        }
        
        # ==================== RÈGLES DE ROUTAGE ====================
        
        # Règle pour projets web simples
        simple_web_rule = RoutingRule(
            rule_id="simple_web_project",
            name="Projet Web Simple",
            conditions={
                "domain": ["web_development"],
                "complexity": ["beginner"],
                "type": ["web_application", "library"],
                "confidence_threshold": 0.6
            },
            actions=["route_to_code_generator", "route_to_web_dev_specialist"],
            priority=1,
            weight=0.8,
            description="Route les projets web simples vers l'IA génératrice de code"
        )
        
        # Règle pour projets data science
        data_science_rule = RoutingRule(
            rule_id="data_science_project",
            name="Projet Data Science",
            conditions={
                "domain": ["data_science"],
                "complexity": ["intermediate", "advanced", "expert"],
                "confidence_threshold": 0.7
            },
            actions=["route_to_data_scientist"],
            priority=2,
            weight=0.9,
            description="Route les projets data science vers le data scientist"
        )
        
        # Règle pour projets de sécurité
        security_rule = RoutingRule(
            rule_id="security_project",
            name="Projet Sécurité",
            conditions={
                "domain": ["cybersecurity"],
                "phase": ["testing", "deployment"]
            },
            actions=["route_to_security_scanner", "route_to_devops_engineer"],
            priority=1,
            weight=0.95,
            description="Route les projets de sécurité vers les outils spécialisés"
        )
        
        # Règle pour projets mobiles
        mobile_rule = RoutingRule(
            rule_id="mobile_project",
            name="Projet Mobile",
            conditions={
                "domain": ["mobile_development"],
                "complexity": ["intermediate", "advanced"]
            },
            actions=["route_to_mobile_dev_specialist"],
            priority=2,
            weight=0.85,
            description="Route les projets mobiles vers le spécialiste mobile"
        )
        
        self.routing_rules = {
            "simple_web_project": simple_web_rule,
            "data_science_project": data_science_rule,
            "security_project": security_rule,
            "mobile_project": mobile_rule
        }
        
        # ==================== MATRICES DE CORRESPONDANCE ====================
        
        self._build_correspondence_matrices()
    
    def _build_correspondence_mappings(self):
        """Construit les mappings de correspondance"""
        
        # Mappings domaine -> capacités
        self.domain_mappings = {
            "web_development": ["frontend", "backend", "fullstack", "api_development", "ui_ux"],
            "data_science": ["machine_learning", "data_analysis", "statistical_modeling", "visualization"],
            "mobile_development": ["android_development", "ios_development", "react_native", "flutter", "app_design"],
            "devops": ["infrastructure", "automation", "ci_cd", "monitoring", "containerization"],
            "cybersecurity": ["security_analysis", "vulnerability_detection", "penetration_testing", "compliance_check"],
            "blockchain": ["smart_contracts", "crypto_development", "defi", "nft_development"],
            "game_development": ["game_design", "unity", "unreal_engine", "mobile_gaming"],
            "embedded_systems": ["iot_development", "firmware", "hardware_integration", "real_time_systems"],
            "scientific_computing": ["simulation", "numerical_analysis", "research_computing", "parallel_processing"]
        }
        
        # Mappings complexité -> ressources nécessaires
        self.complexity_mappings = {
            "beginner": ["code_generator_ai", "tutorial_resources", "basic_templates"],
            "intermediate": ["web_dev_specialist", "mobile_dev_specialist", "standard_frameworks"],
            "advanced": ["senior_developers", "architecture_review", "advanced_frameworks"],
            "expert": ["research_specialists", "cutting_edge_tools", "custom_solutions"]
        }
        
        # Mappings phase -> actions requises
        self.phase_mappings = {
            "planning": ["architecture_review", "requirement_analysis", "technical_planning"],
            "development": ["code_generation", "implementation_support", "debugging_assistance"],
            "testing": ["automated_testing", "security_scanning", "performance_testing"],
            "deployment": ["ci_cd_setup", "infrastructure_deployment", "monitoring_setup"],
            "maintenance": ["monitoring_tools", "update_systems", "performance_optimization"]
        }
    
    def _build_correspondence_matrices(self):
        """Construit les matrices de correspondance numériques"""
        
        domains = list(self.domain_mappings.keys())
        complexities = list(self.complexity_mappings.keys())
        phases = list(self.phase_mappings.keys())
        targets = list(self.routing_targets.keys())
        
        # Matrice Domaine x Cible (score de correspondance)
        domain_target_matrix = np.zeros((len(domains), len(targets)))
        
        for i, domain in enumerate(domains):
            domain_caps = set(self.domain_mappings.get(domain, []))
            for j, target_id in enumerate(targets):
                target = self.routing_targets[target_id]
                target_caps = set(target.capabilities)
                
                # Score basé sur l'intersection des capacités
                intersection = len(domain_caps & target_caps)
                union = len(domain_caps | target_caps)
                jaccard_score = intersection / union if union > 0 else 0.0
                
                # Bonus si le domaine est dans l'expertise
                expertise_bonus = 1.0 if domain in target.domain_expertise else 0.5
                
                domain_target_matrix[i, j] = jaccard_score * expertise_bonus
        
        self.correspondence_matrices['domain_target'] = domain_target_matrix
        
        # Matrice Complexité x Cible
        complexity_target_matrix = np.zeros((len(complexities), len(targets)))
        
        for i, complexity in enumerate(complexities):
            for j, target_id in enumerate(targets):
                target = self.routing_targets[target_id]
                if complexity in target.complexity_support:
                    # Score basé sur le support de complexité
                    complexity_level = complexities.index(complexity)
                    if complexity_level <= 1:  # beginner, intermediate
                        complexity_target_matrix[i, j] = 0.8
                    elif complexity_level == 2:  # advanced
                        complexity_target_matrix[i, j] = 0.9
                    else:  # expert
                        complexity_target_matrix[i, j] = 0.7
                else:
                    complexity_target_matrix[i, j] = 0.2
        
        self.correspondence_matrices['complexity_target'] = complexity_target_matrix
        
        # Matrice Phase x Cible
        phase_target_matrix = np.zeros((len(phases), len(targets)))
        
        for i, phase in enumerate(phases):
            for j, target_id in enumerate(targets):
                target = self.routing_targets[target_id]
                if phase in target.phase_support:
                    phase_target_matrix[i, j] = 0.8
                else:
                    phase_target_matrix[i, j] = 0.3
        
        self.correspondence_matrices['phase_target'] = phase_target_matrix
    
    def route_project(self, classification_result: HybridClassificationResult,
                     context: Dict = None) -> RoutingDecision:
        """
        Route un projet vers la meilleure ressource/cible
        
        Args:
            classification_result: Résultat de classification hybride
            context: Contexte additionnel
        
        Returns:
            RoutingDecision avec la cible recommandée
        """
        
        # Clé de cache
        cache_key = self._generate_cache_key(classification_result, context)
        
        if cache_key in self._routing_cache:
            return self._routing_cache[cache_key]
        
        try:
            # Application des règles de routage
            matched_rules = self._apply_routing_rules(classification_result)
            
            # Sélection de la stratégie de routage
            routing_targets = self._select_routing_targets(classification_result, matched_rules)
            
            # Calcul des scores pour chaque cible
            target_scores = self._calculate_target_scores(
                classification_result, routing_targets, context
            )
            
            # Sélection de la meilleure cible
            best_target, best_score, alternatives = self._select_best_target(target_scores)
            
            # Génération de la décision
            decision = RoutingDecision(
                target=best_target,
                confidence=best_score,
                routing_score=best_score,
                reasoning=self._generate_routing_reasoning(
                    classification_result, best_target, best_score
                ),
                alternatives=alternatives,
                metadata={
                    'matched_rules': [rule.rule_id for rule in matched_rules],
                    'routing_strategy': self.routing_strategy.value,
                    'context': context
                }
            )
            
            # Mise à jour des statistiques
            self._update_routing_stats(decision)
            
            # Cache de la décision
            self._routing_cache[cache_key] = decision
            
            return decision
            
        except Exception as e:
            self.logger.error(f"Erreur lors du routage: {e}")
            return self._generate_fallback_decision()
    
    def _apply_routing_rules(self, classification_result: HybridClassificationResult) -> List[RoutingRule]:
        """Applique les règles de routage applicables"""
        matched_rules = []
        
        for rule in self.routing_rules.values():
            if not rule.enabled:
                continue
            
            if self._rule_matches_classification(rule, classification_result):
                matched_rules.append(rule)
        
        # Tri par priorité et poids
        matched_rules.sort(key=lambda r: (r.priority, r.weight), reverse=True)
        
        return matched_rules
    
    def _rule_matches_classification(self, rule: RoutingRule, 
                                   classification_result: HybridClassificationResult) -> bool:
        """Vérifie si une règle correspond à la classification"""
        
        conditions = rule.conditions
        
        # Vérification du domaine
        if "domain" in conditions:
            if classification_result.final_domain not in conditions["domain"]:
                return False
        
        # Vérification du type
        if "type" in conditions:
            if classification_result.final_type not in conditions["type"]:
                return False
        
        # Vérification de la complexité
        if "complexity" in conditions:
            if classification_result.final_complexity not in conditions["complexity"]:
                return False
        
        # Vérification de la phase
        if "phase" in conditions:
            if classification_result.final_phase not in conditions["phase"]:
                return False
        
        # Vérification du seuil de confiance
        if "confidence_threshold" in conditions:
            if classification_result.fusion_confidence < conditions["confidence_threshold"]:
                return False
        
        return True
    
    def _select_routing_targets(self, classification_result: HybridClassificationResult,
                              matched_rules: List[RoutingRule]) -> List[RoutingTarget]:
        """Sélectionne les cibles de routage possibles"""
        
        targets = set()
        
        # Ajout des cibles des règles匹配
        for rule in matched_rules:
            for action in rule.actions:
                target_id = self._extract_target_from_action(action)
                if target_id in self.routing_targets:
                    targets.add(self.routing_targets[target_id])
        
        # Si aucune cible trouvée via les règles, sélection intelligente
        if not targets:
            targets = self._intelligent_target_selection(classification_result)
        
        return list(targets)
    
    def _extract_target_from_action(self, action: str) -> Optional[str]:
        """Extrait l'ID de cible depuis une action"""
        # Mapping des actions vers les IDs de cibles
        action_mapping = {
            "route_to_code_generator": "code_generator_ai",
            "route_to_web_dev_specialist": "web_dev_specialist",
            "route_to_data_scientist": "data_scientist",
            "route_to_mobile_dev_specialist": "mobile_dev_specialist",
            "route_to_devops_engineer": "devops_engineer",
            "route_to_security_scanner": "security_scanner"
        }
        
        return action_mapping.get(action)
    
    def _intelligent_target_selection(self, classification_result: HybridClassificationResult) -> List[RoutingTarget]:
        """Sélection intelligente des cibles basée sur la classification"""
        
        selected_targets = []
        
        # Sélection basée sur le domaine
        domain = classification_result.final_domain
        complexity = classification_result.final_complexity
        phase = classification_result.final_phase
        
        for target in self.routing_targets.values():
            # Vérification de l'expertise en domaine
            if domain in target.domain_expertise:
                # Vérification du support de complexité
                if complexity in target.complexity_support:
                    # Vérification du support de phase
                    if phase in target.phase_support:
                        selected_targets.append(target)
        
        # Si pas de correspondance exacte, sélection par capacités
        if not selected_targets:
            domain_capabilities = self.domain_mappings.get(domain, [])
            
            for target in self.routing_targets.values():
                target_capabilities = set(target.capabilities)
                domain_cap_set = set(domain_capabilities)
                
                # Si il y a une intersection de capacités
                if target_capabilities & domain_cap_set:
                    selected_targets.append(target)
        
        return selected_targets[:5]  # Limite à 5 cibles maximum
    
    def _calculate_target_scores(self, classification_result: HybridClassificationResult,
                               targets: List[RoutingTarget], context: Dict = None) -> Dict[str, float]:
        """Calcule les scores pour chaque cible de routage"""
        
        scores = {}
        
        # Récupération des indices dans les matrices
        domain_idx = list(self.domain_mappings.keys()).index(classification_result.final_domain)
        complexity_idx = list(self.complexity_mappings.keys()).index(classification_result.final_complexity)
        phase_idx = list(self.phase_mappings.keys()).index(classification_result.final_phase)
        
        for target in targets:
            target_idx = list(self.routing_targets.keys()).index(target.target_id)
            
            # Scores de correspondance
            domain_score = self.correspondence_matrices['domain_target'][domain_idx, target_idx]
            complexity_score = self.correspondence_matrices['complexity_target'][complexity_idx, target_idx]
            phase_score = self.correspondence_matrices['phase_target'][phase_idx, target_idx]
            
            # Score global de correspondance
            correspondence_score = (domain_score + complexity_score + phase_score) / 3
            
            # Score de performance de la cible
            performance_score = target.performance_score
            
            # Score de disponibilité
            availability_score = target.availability
            
            # Facteur de charge (plus faible = mieux)
            load_score = 1.0 - target.load_factor
            
            # Confiance de la classification
            confidence_score = classification_result.fusion_confidence
            
            # Score final pondéré
            final_score = (
                correspondence_score * 0.3 +
                performance_score * 0.25 +
                availability_score * 0.2 +
                load_score * 0.15 +
                confidence_score * 0.1
            )
            
            scores[target.target_id] = final_score
        
        return scores
    
    def _select_best_target(self, target_scores: Dict[str, float]) -> Tuple[RoutingTarget, float, List[Tuple[RoutingTarget, float]]]:
        """Sélectionne la meilleure cible et les alternatives"""
        
        if not target_scores:
            raise ValueError("Aucun score de cible disponible")
        
        # Tri par score décroissant
        sorted_targets = sorted(target_scores.items(), key=lambda x: x[1], reverse=True)
        
        best_target_id, best_score = sorted_targets[0]
        best_target = self.routing_targets[best_target_id]
        
        # Alternatives (top 3)
        alternatives = []
        for target_id, score in sorted_targets[1:4]:
            if score > 0.3:  # Seuil minimal pour les alternatives
                alternatives.append((self.routing_targets[target_id], score))
        
        return best_target, best_score, alternatives
    
    def _generate_routing_reasoning(self, classification_result: HybridClassificationResult,
                                  target: RoutingTarget, score: float) -> str:
        """Génère le raisonnement de la décision de routage"""
        
        reasoning_parts = [
            f"Cible sélectionnée: {target.name}",
            f"Score de routage: {score:.2f}",
            f"Domaine projet: {classification_result.final_domain}",
            f"Complexité: {classification_result.final_complexity}",
            f"Phase: {classification_result.final_phase}",
            f"Confiance classification: {classification_result.fusion_confidence:.2f}"
        ]
        
        if target.type == "automated_tool":
            reasoning_parts.append("Type: Outil automatisé")
        elif target.type == "human_resource":
            reasoning_parts.append("Type: Ressource humaine")
        
        return " | ".join(reasoning_parts)
    
    def _generate_cache_key(self, classification_result: HybridClassificationResult, context: Dict) -> str:
        """Génère une clé de cache pour les décisions de routage"""
        key_parts = [
            classification_result.final_domain,
            classification_result.final_type,
            classification_result.final_complexity,
            classification_result.final_phase,
            f"{classification_result.fusion_confidence:.2f}"
        ]
        
        if context:
            key_parts.append(hash(str(context)))
        
        return "_".join(key_parts)
    
    def _generate_fallback_decision(self) -> RoutingDecision:
        """Génère une décision de fallback en cas d'erreur"""
        fallback_target = RoutingTarget(
            target_id="fallback_handler",
            name="Gestionnaire de Fallback",
            type="human_resource",
            capabilities=["general_support"],
            domain_expertise=["general"],
            complexity_support=["beginner", "intermediate", "advanced", "expert"],
            phase_support=["planning", "development", "testing", "deployment", "maintenance"],
            load_factor=0.5,
            availability=0.7,
            performance_score=0.5
        )
        
        return RoutingDecision(
            target=fallback_target,
            confidence=0.1,
            routing_score=0.1,
            reasoning="Décision de fallback - Erreur dans le routage principal",
            alternatives=[],
            metadata={'fallback': True}
        )
    
    def _update_routing_stats(self, decision: RoutingDecision):
        """Met à jour les statistiques de routage"""
        self.routing_stats['total_routing_decisions'] += 1
        self.routing_stats['strategy_usage'][self.routing_strategy.value] += 1
        
        if decision.confidence > 0.5:
            self.routing_stats['successful_routes'] += 1
        else:
            self.routing_stats['failed_routes'] += 1
    
    def add_routing_target(self, target: RoutingTarget):
        """Ajoute une nouvelle cible de routage"""
        self.routing_targets[target.target_id] = target
        self._build_correspondence_matrices()  # Reconstruction des matrices
    
    def add_routing_rule(self, rule: RoutingRule):
        """Ajoute une nouvelle règle de routage"""
        self.routing_rules[rule.rule_id] = rule
    
    def get_routing_explanation(self, decision: RoutingDecision) -> Dict:
        """Génère une explication détaillée de la décision de routage"""
        return {
            'routing_summary': {
                'selected_target': decision.target.name,
                'confidence': decision.confidence,
                'routing_score': decision.routing_score,
                'reasoning': decision.reasoning
            },
            'target_details': {
                'type': decision.target.type,
                'capabilities': decision.target.capabilities,
                'domain_expertise': decision.target.domain_expertise,
                'performance_score': decision.target.performance_score,
                'availability': decision.target.availability,
                'load_factor': decision.target.load_factor
            },
            'alternatives': [
                {
                    'target': alt[0].name,
                    'score': alt[1],
                    'capabilities': alt[0].capabilities
                }
                for alt in decision.alternatives
            ],
            'metadata': decision.metadata,
            'quality_indicators': {
                'has_high_confidence': decision.confidence > 0.8,
                'has_alternatives': len(decision.alternatives) > 0,
                'is_automated': decision.target.type == "automated_tool"
            }
        }

# ==================== FONCTIONS UTILITAIRES ====================

def optimize_routing_matrix(routing_matrix: RoutingMatrix, historical_data: List[Dict]) -> None:
    """Optimise la matrice de routage basée sur des données historiques"""
    
    # Analyse des performances historiques
    performance_analysis = defaultdict(list)
    
    for entry in historical_data:
        if 'routing_decision' in entry and 'success' in entry:
            target_id = entry['routing_decision']['target_id']
            success = entry['success']
            performance_analysis[target_id].append(success)
    
    # Mise à jour des scores de performance
    for target_id, successes in performance_analysis.items():
        if target_id in routing_matrix.routing_targets:
            target = routing_matrix.routing_targets[target_id]
            avg_success = sum(successes) / len(successes)
            target.performance_score = avg_success
    
    # Reconstruction des matrices
    routing_matrix._build_correspondence_matrices()

def batch_route_projects(classification_results: List[HybridClassificationResult], 
                        routing_matrix: RoutingMatrix) -> List[RoutingDecision]:
    """Route plusieurs projets en lot pour optimiser les performances"""
    decisions = []
    
    for classification_result in classification_results:
        decision = routing_matrix.route_project(classification_result)
        decisions.append(decision)
    
    return decisions
