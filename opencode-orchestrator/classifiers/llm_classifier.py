"""
Classificateur LLM pour l'Orchestrateur OpenCode
Prompts optimisés et validation des réponses JSON
"""

import json
import time
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import re

@dataclass
class LLMClassificationResult:
    """Résultat de classification LLM structuré"""
    domain: str
    domain_confidence: float
    type: str
    type_confidence: float
    complexity: str
    complexity_confidence: float
    phase: str
    phase_confidence: float
    overall_confidence: float
    reasoning: str
    extracted_features: List[str]
    suggestions: List[str]
    metadata: Dict[str, Any]

@dataclass
class ValidationResult:
    """Résultat de validation d'une réponse LLM"""
    is_valid: bool
    confidence_score: float
    errors: List[str]
    warnings: List[str]
    normalized_result: Optional[LLMClassificationResult]

class ConfidenceLevel(Enum):
    """Niveaux de confiance pour classification LLM"""
    VERY_HIGH = "very_high"  # > 0.9
    HIGH = "high"           # > 0.7
    MEDIUM = "medium"       # > 0.5
    LOW = "low"             # > 0.3
    VERY_LOW = "very_low"   # <= 0.3

class LLMClassifier:
    """Classificateur basé sur LLM avec validation et confiance"""
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client  # Client LLM (OpenAI, Anthropic, etc.)
        self.logger = logging.getLogger(__name__)
        
        # Métriques de performance
        self.validation_stats = {
            'total_requests': 0,
            'valid_responses': 0,
            'invalid_responses': 0,
            'avg_validation_time': 0.0
        }
        
        # Cache pour éviter les requêtes répétées
        self._response_cache = {}
    
    def classify(self, text: str, context: Dict = None, 
                use_cache: bool = True) -> LLMClassificationResult:
        """
        Classification principale par LLM
        
        Args:
            text: Texte à classifier
            context: Contexte additionnel
            use_cache: Utiliser le cache pour éviter les requêtes répétées
        
        Returns:
            LLMClassificationResult structuré et validé
        """
        start_time = time.time()
        
        # Clé de cache
        cache_key = f"{hash(text)}_{hash(str(context))}"
        
        if use_cache and cache_key in self._response_cache:
            return self._response_cache[cache_key]
        
        # Génération du prompt
        prompt = self._build_classification_prompt(text, context)
        
        # Appel LLM
        raw_response = self._call_llm(prompt)
        
        # Validation et normalisation
        validation_result = self._validate_and_normalize_response(raw_response)
        
        if not validation_result.is_valid:
            # Fallback sur classification par mots-clés ou valeurs par défaut
            fallback_result = self._generate_fallback_classification(text)
            result = fallback_result
        else:
            result = validation_result.normalized_result
        
        # Ajout des métadonnées
        result.metadata.update({
            'processing_time': time.time() - start_time,
            'validation_time': getattr(validation_result, 'validation_time', 0),
            'cached': use_cache and cache_key in self._response_cache,
            'raw_llm_response': raw_response
        })
        
        # Mise en cache
        if use_cache:
            self._response_cache[cache_key] = result
        
        return result
    
    def _build_classification_prompt(self, text: str, context: Dict = None) -> str:
        """Construit un prompt optimisé pour la classification"""
        
        # Template de prompt avec few-shot examples
        prompt_template = """
Tu es un expert en classification de projets de développement logiciel. 
Ta tâche est de classifier un projet selon 4 dimensions : domaine, type, complexité et phase.

CONTEXTE DU PROJET:
{context_section}

TEXTE À CLASSIFIER:
{project_text}

INSTRUCTIONS:
1. Analyse le texte fourni en détail
2. Pour chaque dimension, sélectionne la catégorie la plus appropriée
3. Assigne un niveau de confiance (0.0 à 1.0) pour chaque classification
4. Explique brièvement ton raisonnement
5. Extrais les caractéristiques principales du projet
6. Suggère des améliorations ou recommandations

DOMAINES POSSIBLES:
- web_development: Applications web, sites internet, APIs web
- data_science: Analyse de données, machine learning, intelligence artificielle
- mobile_development: Applications mobiles iOS/Android
- desktop_development: Applications desktop natives
- devops: Infrastructure, déploiement, automatisation
- cybersecurity: Sécurité, cryptographie, audit
- blockchain: Applications blockchain, crypto
- game_development: Jeux vidéo, moteurs de jeu
- embedded_systems: Systèmes embarqués, IoT
- scientific_computing: Calcul scientifique, recherche

TYPES DE PROJETS POSSIBLES:
- web_application: Application web (SPA, PWA, site)
- api_service: Service API (REST, GraphQL, microservices)
- library: Bibliothèque, framework, SDK
- cli_tool: Outil en ligne de commande
- mobile_app: Application mobile native/hybride
- desktop_app: Application desktop
- script: Script d'automatisation
- documentation: Documentation technique
- configuration: Configuration, déploiement

NIVEAUX DE COMPLEXITÉ POSSIBLES:
- beginner: Débutant, simple, éducatif
- intermediate: Intermédiaire, fonctionnalités standards
- advanced: Avancé, architecture complexe
- expert: Expert, état de l'art, recherche

PHASES DE PROJET POSSIBLES:
- planning: Planification, conception, spécifications
- development: Développement, implémentation
- testing: Tests, validation, QA
- deployment: Déploiement, mise en production
- maintenance: Maintenance, évolution, optimisation

FORMAT DE RÉPONSE (JSON strict):
```json
{{
  "domain": "nom_du_domaine",
  "domain_confidence": 0.85,
  "type": "nom_du_type", 
  "type_confidence": 0.90,
  "complexity": "niveau_complexite",
  "complexity_confidence": 0.75,
  "phase": "phase_projet",
  "phase_confidence": 0.80,
  "overall_confidence": 0.83,
  "reasoning": "Explication concise du raisonnement",
  "extracted_features": ["feature1", "feature2", "feature3"],
  "suggestions": ["suggestion1", "suggestion2"]
}}
```

RÉPONSE:
"""
        
        # Construction du contexte
        context_section = "Aucun contexte additionnel fourni."
        if context:
            context_parts = []
            if 'files' in context:
                context_parts.append(f"Fichiers présents: {', '.join(context['files'])}")
            if 'structure' in context:
                context_parts.append(f"Structure: {context['structure']}")
            if 'technologies' in context:
                context_parts.append(f"Technologies: {', '.join(context['technologies'])}")
            
            context_section = " | ".join(context_parts)
        
        return prompt_template.format(
            context_section=context_section,
            project_text=text[:2000]  # Limiter la taille du texte
        )
    
    def _call_llm(self, prompt: str) -> str:
        """Appelle le client LLM pour classification"""
        try:
            # Simulation d'appel LLM (à remplacer par vrai client)
            # Dans un vrai implémentation, on utiliserait :
            # return self.llm_client.chat.completions.create(
            #     model="gpt-4",
            #     messages=[{"role": "user", "content": prompt}],
            #     temperature=0.1
            # ).choices[0].message.content
            
            # Simulation pour démonstration
            return self._simulate_llm_response(prompt)
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'appel LLM: {e}")
            raise
    
    def _simulate_llm_response(self, prompt: str) -> str:
        """Simulation d'une réponse LLM pour démonstration"""
        # Extraction de mots-clés du prompt pour simulation réaliste
        text_section = prompt.split("TEXTE À CLASSIFIER:")[1].split("INSTRUCTIONS:")[0]
        text_lower = text_section.lower()
        
        # Logique de simulation basée sur le contenu
        if any(word in text_lower for word in ['react', 'angular', 'vue', 'frontend']):
            domain = "web_development"
            domain_conf = 0.85
        elif any(word in text_lower for word in ['pandas', 'numpy', 'machine learning']):
            domain = "data_science"
            domain_conf = 0.90
        elif any(word in text_lower for word in ['mobile', 'android', 'ios']):
            domain = "mobile_development"
            domain_conf = 0.88
        else:
            domain = "web_development"
            domain_conf = 0.60
        
        # Simulation des autres classifications
        type_class = "web_application" if "web" in domain else "library"
        complexity_class = "intermediate"
        phase_class = "development"
        
        return f"""{{
  "domain": "{domain}",
  "domain_confidence": {domain_conf},
  "type": "{type_class}",
  "type_confidence": 0.80,
  "complexity": "{complexity_class}",
  "complexity_confidence": 0.75,
  "phase": "{phase_class}",
  "phase_confidence": 0.70,
  "overall_confidence": 0.78,
  "reasoning": "Classification basée sur l'analyse sémantique du contenu et des patterns identifiés.",
  "extracted_features": ["feature1", "feature2", "feature3"],
  "suggestions": ["Améliorer la documentation", "Ajouter des tests"]
}}"""
    
    def _validate_and_normalize_response(self, raw_response: str) -> ValidationResult:
        """Valide et normalise la réponse LLM"""
        start_time = time.time()
        
        errors = []
        warnings = []
        
        try:
            # Extraction du JSON de la réponse
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', raw_response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Essayer d'extraire directement le JSON
                json_match = re.search(r'(\{.*\})', raw_response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    errors.append("Aucun JSON trouvé dans la réponse")
                    return ValidationResult(False, 0.0, errors, warnings, None)
            
            # Parsing JSON
            try:
                parsed_data = json.loads(json_str)
            except json.JSONDecodeError as e:
                errors.append(f"Erreur parsing JSON: {e}")
                return ValidationResult(False, 0.0, errors, warnings, None)
            
            # Validation des champs requis
            required_fields = ['domain', 'domain_confidence', 'type', 'type_confidence',
                             'complexity', 'complexity_confidence', 'phase', 'phase_confidence',
                             'overall_confidence', 'reasoning']
            
            for field in required_fields:
                if field not in parsed_data:
                    errors.append(f"Champ requis manquant: {field}")
            
            if errors:
                return ValidationResult(False, 0.0, errors, warnings, None)
            
            # Validation des valeurs
            validation_result = self._validate_field_values(parsed_data)
            if not validation_result[0]:
                errors.extend(validation_result[1])
            
            # Normalisation des valeurs
            normalized_data = self._normalize_field_values(parsed_data)
            
            # Création du résultat normalisé
            result = LLMClassificationResult(**normalized_data)
            
            # Calcul du score de validation
            validation_score = self._calculate_validation_score(parsed_data, errors, warnings)
            
            validation_time = time.time() - start_time
            self.validation_stats['total_requests'] += 1
            self.validation_stats['valid_responses'] += 1
            self.validation_stats['avg_validation_time'] += validation_time
            
            return ValidationResult(True, validation_score, errors, warnings, result)
            
        except Exception as e:
            errors.append(f"Erreur validation: {e}")
            self.validation_stats['total_requests'] += 1
            self.validation_stats['invalid_responses'] += 1
            return ValidationResult(False, 0.0, errors, warnings, None)
    
    def _validate_field_values(self, data: Dict) -> Tuple[bool, List[str]]:
        """Valide les valeurs des champs classification"""
        errors = []
        
        # Validation des domaines
        valid_domains = ['web_development', 'data_science', 'mobile_development',
                        'desktop_development', 'devops', 'cybersecurity',
                        'blockchain', 'game_development', 'embedded_systems',
                        'scientific_computing']
        
        if data.get('domain') not in valid_domains:
            errors.append(f"Domaine invalide: {data.get('domain')}")
        
        # Validation des types
        valid_types = ['web_application', 'api_service', 'library', 'cli_tool',
                      'mobile_app', 'desktop_app', 'script', 'documentation', 'configuration']
        
        if data.get('type') not in valid_types:
            errors.append(f"Type invalide: {data.get('type')}")
        
        # Validation des complexités
        valid_complexities = ['beginner', 'intermediate', 'advanced', 'expert']
        
        if data.get('complexity') not in valid_complexities:
            errors.append(f"Complexité invalide: {data.get('complexity')}")
        
        # Validation des phases
        valid_phases = ['planning', 'development', 'testing', 'deployment', 'maintenance']
        
        if data.get('phase') not in valid_phases:
            errors.append(f"Phase invalide: {data.get('phase')}")
        
        # Validation des niveaux de confiance (0.0 à 1.0)
        confidence_fields = ['domain_confidence', 'type_confidence', 'complexity_confidence',
                           'phase_confidence', 'overall_confidence']
        
        for field in confidence_fields:
            value = data.get(field)
            if not isinstance(value, (int, float)) or not 0.0 <= value <= 1.0:
                errors.append(f"Confiance invalide pour {field}: {value}")
        
        return len(errors) == 0, errors
    
    def _normalize_field_values(self, data: Dict) -> Dict:
        """Normalise les valeurs des champs"""
        normalized = data.copy()
        
        # Normalisation des domaines (underscore)
        normalized['domain'] = normalized['domain'].lower().replace('-', '_')
        normalized['type'] = normalized['type'].lower().replace('-', '_')
        normalized['complexity'] = normalized['complexity'].lower()
        normalized['phase'] = normalized['phase'].lower()
        
        # Conversion des confiances en float
        confidence_fields = ['domain_confidence', 'type_confidence', 'complexity_confidence',
                           'phase_confidence', 'overall_confidence']
        
        for field in confidence_fields:
            normalized[field] = float(normalized[field])
        
        # Normalisation des listes
        if 'extracted_features' not in normalized:
            normalized['extracted_features'] = []
        elif not isinstance(normalized['extracted_features'], list):
            normalized['extracted_features'] = [str(normalized['extracted_features'])]
        
        if 'suggestions' not in normalized:
            normalized['suggestions'] = []
        elif not isinstance(normalized['suggestions'], list):
            normalized['suggestions'] = [str(normalized['suggestions'])]
        
        # Ajout de champs par défaut
        if 'reasoning' not in normalized:
            normalized['reasoning'] = "Pas de raisonnement fourni"
        
        normalized['metadata'] = {}
        
        return normalized
    
    def _calculate_validation_score(self, data: Dict, errors: List[str], warnings: List[str]) -> float:
        """Calcule un score de validation basé sur la qualité de la réponse"""
        base_score = 1.0
        
        # Pénalité pour les erreurs
        base_score -= len(errors) * 0.3
        
        # Pénalité pour les warnings
        base_score -= len(warnings) * 0.1
        
        # Bonus pour les champs optionnels
        if 'extracted_features' in data and data['extracted_features']:
            base_score += 0.05
        
        if 'suggestions' in data and data['suggestions']:
            base_score += 0.05
        
        # Bonus pour la cohérence des confiances
        confidences = [data.get('domain_confidence', 0), data.get('type_confidence', 0),
                      data.get('complexity_confidence', 0), data.get('phase_confidence', 0)]
        
        if confidences:
            variance = sum((c - sum(confidences)/len(confidences))**2 for c in confidences) / len(confidences)
            if variance < 0.1:  # Faible variance = bonne cohérence
                base_score += 0.1
        
        return max(0.0, min(1.0, base_score))
    
    def _generate_fallback_classification(self, text: str) -> LLMClassificationResult:
        """Génère une classification de fallback en cas d'échec LLM"""
        # Classification basique basée sur mots-clés
        text_lower = text.lower()
        
        # Détection de domaine basique
        if any(word in text_lower for word in ['react', 'vue', 'angular', 'javascript']):
            domain = 'web_development'
        elif any(word in text_lower for word in ['pandas', 'numpy', 'data']):
            domain = 'data_science'
        elif any(word in text_lower for word in ['mobile', 'android', 'ios']):
            domain = 'mobile_development'
        else:
            domain = 'web_development'  # Default
        
        return LLMClassificationResult(
            domain=domain,
            domain_confidence=0.5,
            type='web_application',
            type_confidence=0.5,
            complexity='intermediate',
            complexity_confidence=0.5,
            phase='development',
            phase_confidence=0.5,
            overall_confidence=0.5,
            reasoning="Classification de fallback basée sur l'analyse basique du contenu.",
            extracted_features=[],
            suggestions=["Améliorer la qualité du contenu pour une meilleure classification"],
            metadata={'fallback': True}
        )
    
    def get_classification_explanation(self, result: LLMClassificationResult) -> Dict:
        """Génère une explication détaillée de la classification LLM"""
        return {
            'confidence_assessment': self._assess_confidence_level(result.overall_confidence),
            'domain_analysis': {
                'primary_domain': result.domain,
                'confidence': result.domain_confidence,
                'reasoning': f"Domaine identifié avec {result.domain_confidence:.1%} de confiance"
            },
            'type_analysis': {
                'project_type': result.type,
                'confidence': result.type_confidence
            },
            'complexity_analysis': {
                'complexity_level': result.complexity,
                'confidence': result.complexity_confidence
            },
            'phase_analysis': {
                'current_phase': result.phase,
                'confidence': result.phase_confidence
            },
            'extracted_insights': {
                'features': result.extracted_features,
                'suggestions': result.suggestions,
                'reasoning': result.reasoning
            },
            'quality_indicators': {
                'overall_confidence': result.overall_confidence,
                'metadata': result.metadata
            }
        }
    
    def _assess_confidence_level(self, confidence: float) -> str:
        """Détermine le niveau de confiance textuel"""
        if confidence >= 0.9:
            return "Très élevée"
        elif confidence >= 0.7:
            return "Élevée"
        elif confidence >= 0.5:
            return "Moyenne"
        elif confidence >= 0.3:
            return "Faible"
        else:
            return "Très faible"
