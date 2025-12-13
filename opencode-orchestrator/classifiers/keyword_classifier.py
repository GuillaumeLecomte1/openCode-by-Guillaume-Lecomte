"""
Classificateur par mots-clés pour l'Orchestrateur OpenCode
Algorithmes de matching, scoring et priorisation
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, NamedTuple
from dataclasses import dataclass
from collections import defaultdict, Counter
import math

from config.keywords_config import KeywordsConfig, KeywordPattern

@dataclass
class ClassificationResult:
    """Résultat de classification par mots-clés"""
    domain: Dict[str, float]
    type: Dict[str, float]
    complexity: Dict[str, float]
    phase: Dict[str, float]
    confidence: float
    matched_keywords: List[str]
    processing_time: float
    algorithm_version: str = "1.0"

@dataclass
class KeywordMatch:
    """Représente un match de mot-clé trouvé"""
    keyword: str
    pattern: str
    weight: float
    priority: int
    position: int
    context: str
    match_type: str  # 'exact', 'regex', 'fuzzy'

class KeywordClassifier:
    """Classificateur principal par mots-clés avec algorithmes avancés"""
    
    def __init__(self, config: KeywordsConfig = None):
        self.config = config or KeywordsConfig()
        self.logger = logging.getLogger(__name__)
        
        # Cache pour les patterns regex compilés
        self._compiled_patterns = {}
        self._build_regex_cache()
        
        # Métriques de performance
        self.processing_stats = defaultdict(int)
    
    def _build_regex_cache(self):
        """Compile et met en cache tous les patterns regex"""
        # Patterns globaux
        for category, patterns in self.config.GLOBAL_PATTERNS.items():
            self._compiled_patterns[f"global_{category}"] = {}
            for name, pattern in patterns.items():
                try:
                    self._compiled_patterns[f"global_{category}"][name] = re.compile(
                        pattern, re.IGNORECASE | re.MULTILINE
                    )
                except re.error as e:
                    self.logger.warning(f"Erreur compilation regex {name}: {e}")
        
        # Patterns par domaine
        for domain, domain_config in self.config.DOMAINS.items():
            if 'patterns' in domain_config:
                self._compiled_patterns[f"domain_{domain}"] = []
                for pattern in domain_config['patterns']:
                    try:
                        self._compiled_patterns[f"domain_{domain}"].append(
                            re.compile(pattern, re.IGNORECASE | re.MULTILINE)
                        )
                    except re.error as e:
                        self.logger.warning(f"Erreur compilation regex domaine {domain}: {e}")
        
        # Patterns de complexité
        for level, complexity_config in self.config.COMPLEXITY_LEVELS.items():
            if 'code_patterns' in complexity_config:
                self._compiled_patterns[f"complexity_{level}"] = []
                for pattern in complexity_config['code_patterns']:
                    try:
                        self._compiled_patterns[f"complexity_{level}"].append(
                            re.compile(pattern, re.IGNORECASE | re.MULTILINE)
                        )
                    except re.error as e:
                        self.logger.warning(f"Erreur compilation regex complexité {level}: {e}")
    
    def classify(self, text: str, context: Dict = None) -> ClassificationResult:
        """
        Classification principale par mots-clés
        
        Args:
            text: Texte à classifier (README, code, etc.)
            context: Contexte additionnel (fichiers, structure, etc.)
        
        Returns:
            ClassificationResult avec scores pour chaque dimension
        """
        import time
        start_time = time.time()
        
        # Prétraitement du texte
        processed_text = self._preprocess_text(text)
        
        # Classification par dimension
        domain_scores = self._classify_domain(processed_text)
        type_scores = self._classify_type(processed_text)
        complexity_scores = self._classify_complexity(processed_text)
        phase_scores = self._classify_phase(processed_text)
        
        # Calcul de la confiance globale
        confidence = self._calculate_confidence(
            domain_scores, type_scores, complexity_scores, phase_scores
        )
        
        # Extraction des mots-clés matched
        matched_keywords = self._extract_matched_keywords(processed_text)
        
        processing_time = time.time() - start_time
        
        # Mise à jour des statistiques
        self.processing_stats['total_classifications'] += 1
        self.processing_stats['avg_processing_time'] += processing_time
        
        return ClassificationResult(
            domain=domain_scores,
            type=type_scores,
            complexity=complexity_scores,
            phase=phase_scores,
            confidence=confidence,
            matched_keywords=matched_keywords,
            processing_time=processing_time
        )
    
    def _preprocess_text(self, text: str) -> str:
        """Prétraitement du texte pour améliorer la classification"""
        if not text:
            return ""
        
        # Normalisation
        text = text.lower().strip()
        
        # Suppression des caractères spéciaux mais préservation des espaces
        text = re.sub(r'[^\w\s\-_]', ' ', text)
        
        # Normalisation des espaces
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def _classify_domain(self, text: str) -> Dict[str, float]:
        """Classification par domaine avec algorithme de scoring pondéré"""
        scores = defaultdict(float)
        matches_found = []
        
        for domain, domain_config in self.config.DOMAINS.items():
            domain_score = 0.0
            keyword_matches = []
            
            # Mots-clés haute priorité
            for keyword_pattern in domain_config.get('high_priority', []):
                score, match = self._match_keyword_pattern(text, keyword_pattern)
                if score > 0:
                    domain_score += score * 1.5  # Bonus priorité haute
                    keyword_matches.append(match)
            
            # Mots-clés priorité moyenne
            for keyword_pattern in domain_config.get('medium_priority', []):
                score, match = self._match_keyword_pattern(text, keyword_pattern)
                if score > 0:
                    domain_score += score * 1.0
                    keyword_matches.append(match)
            
            # Patterns regex spécifiques
            domain_key = f"domain_{domain}"
            if domain_key in self._compiled_patterns:
                for regex_pattern in self._compiled_patterns[domain_key]:
                    matches = regex_pattern.findall(text)
                    if matches:
                        domain_score += len(matches) * 0.3
                        for match in matches:
                            keyword_matches.append(KeywordMatch(
                                keyword=str(match),
                                pattern=regex_pattern.pattern,
                                weight=0.3,
                                priority=2,
                                position=0,
                                context="",
                                match_type="regex"
                            ))
            
            # Bonus pour cohérence des matches
            if keyword_matches:
                coherence_bonus = min(len(keyword_matches) * 0.1, 0.5)
                domain_score += coherence_bonus
                matches_found.extend(keyword_matches)
            
            scores[domain] = min(domain_score, 1.0)  # Cap à 1.0
        
        return dict(scores)
    
    def _classify_type(self, text: str) -> Dict[str, float]:
        """Classification par type de projet"""
        scores = defaultdict(float)
        
        for project_type, keyword_patterns in self.config.PROJECT_TYPES.items():
            type_score = 0.0
            
            for keyword_pattern in keyword_patterns:
                score, match = self._match_keyword_pattern(text, keyword_pattern)
                if score > 0:
                    type_score += score * keyword_pattern.weight
            
            # Bonus pour patterns de fichiers indicateurs
            type_score += self._check_file_indicators(text, project_type)
            
            scores[project_type] = min(type_score, 1.0)
        
        return dict(scores)
    
    def _classify_complexity(self, text: str) -> Dict[str, float]:
        """Classification par niveau de complexité"""
        scores = defaultdict(float)
        
        for complexity_level, complexity_config in self.config.COMPLEXITY_LEVELS.items():
            complexity_score = 0.0
            
            # Indicateurs textuels
            for keyword_pattern in complexity_config.get('indicators', []):
                score, match = self._match_keyword_pattern(text, keyword_pattern)
                if score > 0:
                    complexity_score += score * keyword_pattern.weight
            
            # Patterns de code
            complexity_key = f"complexity_{complexity_level}"
            if complexity_key in self._compiled_patterns:
                for regex_pattern in self._compiled_patterns[complexity_key]:
                    matches = regex_pattern.findall(text)
                    if matches:
                        complexity_score += len(matches) * 0.4
            
            scores[complexity_level] = min(complexity_score, 1.0)
        
        return dict(scores)
    
    def _classify_phase(self, text: str) -> Dict[str, float]:
        """Classification par phase de projet"""
        scores = defaultdict(float)
        
        for phase, keyword_patterns in self.config.PROJECT_PHASES.items():
            phase_score = 0.0
            
            for keyword_pattern in keyword_patterns:
                score, match = self._match_keyword_pattern(text, keyword_pattern)
                if score > 0:
                    phase_score += score * keyword_pattern.weight
            
            scores[phase] = min(phase_score, 1.0)
        
        return dict(scores)
    
    def _match_keyword_pattern(self, text: str, pattern: KeywordPattern) -> Tuple[float, Optional[KeywordMatch]]:
        """Match un pattern de mot-clé dans le texte"""
        if pattern.regex:
            # Pattern regex
            try:
                regex = re.compile(pattern.pattern, re.IGNORECASE)
                if regex.search(text):
                    return pattern.weight, KeywordMatch(
                        keyword=pattern.pattern,
                        pattern=pattern.pattern,
                        weight=pattern.weight,
                        priority=pattern.priority,
                        position=regex.search(text).start(),
                        context=self._extract_context(text, regex.search(text).start()),
                        match_type="regex"
                    )
            except re.error:
                pass
        else:
            # Mot exact
            words = text.split()
            for i, word in enumerate(words):
                if pattern.pattern.lower() in word.lower():
                    return pattern.weight, KeywordMatch(
                        keyword=pattern.pattern,
                        pattern=pattern.pattern,
                        weight=pattern.weight,
                        priority=pattern.priority,
                        position=i,
                        context=" ".join(words[max(0, i-2):i+3]),
                        match_type="exact"
                    )
        
        return 0.0, None
    
    def _extract_context(self, text: str, position: int, context_size: int = 50) -> str:
        """Extrait le contexte autour d'une position"""
        start = max(0, position - context_size)
        end = min(len(text), position + context_size)
        return text[start:end]
    
    def _check_file_indicators(self, text: str, project_type: str) -> float:
        """Vérifie la présence d'indicateurs de fichiers pour le type de projet"""
        score = 0.0
        
        # Mapping type -> indicateurs de fichiers
        type_indicators = {
            'web_application': ['package_json', 'dockerfile'],
            'api_service': ['readme', 'config_files'],
            'library': ['package_json', 'readme'],
            'cli_tool': ['config_files'],
            'mobile_app': ['package_json']
        }
        
        indicators = type_indicators.get(project_type, [])
        for indicator in indicators:
            pattern_key = f"global_file_indicators"
            if pattern_key in self._compiled_patterns and indicator in self._compiled_patterns[pattern_key]:
                if self._compiled_patterns[pattern_key][indicator].search(text):
                    score += 0.2
        
        return score
    
    def _calculate_confidence(self, domain_scores: Dict, type_scores: Dict, 
                            complexity_scores: Dict, phase_scores: Dict) -> float:
        """Calcule la confiance globale basée sur la cohérence des scores"""
        all_scores = list(domain_scores.values()) + list(type_scores.values()) + \
                    list(complexity_scores.values()) + list(phase_scores.values())
        
        if not all_scores:
            return 0.0
        
        # Confiance basée sur la variance des scores
        mean_score = sum(all_scores) / len(all_scores)
        variance = sum((score - mean_score) ** 2 for score in all_scores) / len(all_scores)
        
        # Plus la variance est faible, plus la confiance est élevée
        confidence = max(0.0, 1.0 - variance)
        
        # Bonus pour les scores élevés
        max_score = max(all_scores)
        if max_score > 0.8:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _extract_matched_keywords(self, text: str) -> List[str]:
        """Extrait tous les mots-clés trouvés dans le texte"""
        matched_keywords = []
        
        # Extraction des mots-clés par domaine
        for domain, domain_config in self.config.DOMAINS.items():
            for keyword_pattern in domain_config.get('high_priority', []) + \
                                 domain_config.get('medium_priority', []):
                score, match = self._match_keyword_pattern(text, keyword_pattern)
                if score > 0 and match:
                    matched_keywords.append(match.keyword)
        
        # Suppression des doublons et retour
        return list(set(matched_keywords))
    
    def get_classification_explanation(self, result: ClassificationResult) -> Dict:
        """Génère une explication détaillée de la classification"""
        explanation = {
            'confidence_level': self._get_confidence_level(result.confidence),
            'top_domain': max(result.domain.items(), key=lambda x: x[1]) if result.domain else None,
            'top_type': max(result.type.items(), key=lambda x: x[1]) if result.type else None,
            'top_complexity': max(result.complexity.items(), key=lambda x: x[1]) if result.complexity else None,
            'top_phase': max(result.phase.items(), key=lambda x: x[1]) if result.phase else None,
            'processing_stats': {
                'matched_keywords_count': len(result.matched_keywords),
                'processing_time': result.processing_time,
                'algorithm_version': result.algorithm_version
            },
            'scoring_breakdown': {
                'domain_scores': result.domain,
                'type_scores': result.type,
                'complexity_scores': result.complexity,
                'phase_scores': result.phase
            }
        }
        
        return explanation
    
    def _get_confidence_level(self, confidence: float) -> str:
        """Détermine le niveau de confiance"""
        if confidence >= 0.8:
            return "Haute"
        elif confidence >= 0.6:
            return "Moyenne"
        elif confidence >= 0.4:
            return "Faible"
        else:
            return "Très faible"

# ==================== FONCTIONS UTILITAIRES ====================

def calculate_keyword_similarity(text1: str, text2: str) -> float:
    """Calcule la similarité entre deux textes basée sur les mots-clés"""
    classifier = KeywordClassifier()
    
    result1 = classifier.classify(text1)
    result2 = classifier.classify(text2)
    
    # Similarité basée sur les scores de classification
    domains1 = set(result1.domain.keys())
    domains2 = set(result2.domain.keys())
    
    if not domains1 and not domains2:
        return 1.0
    if not domains1 or not domains2:
        return 0.0
    
    intersection = len(domains1.intersection(domains2))
    union = len(domains1.union(domains2))
    
    return intersection / union if union > 0 else 0.0

def batch_classify(texts: List[str], batch_size: int = 10) -> List[ClassificationResult]:
    """Classification par lots pour optimiser les performances"""
    classifier = KeywordClassifier()
    results = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        for text in batch:
            results.append(classifier.classify(text))
    
    return results
