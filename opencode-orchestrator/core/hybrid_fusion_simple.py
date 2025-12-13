#!/usr/bin/env python3
"""
HybridFusionEngine Simplifié
Version simplifiée pour la compatibilité
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

from classifiers.keyword_classifier import KeywordClassifier, ClassificationResult
from classifiers.llm_classifier import LLMClassifier, LLMClassificationResult

@dataclass
class HybridClassificationResult:
    """Résultat final de classification hybride"""
    final_domain: str
    final_domain_confidence: float
    final_type: str
    final_type_confidence: float
    final_complexity: str
    final_complexity_confidence: float
    final_phase: str
    final_phase_confidence: float
    fusion_confidence: float = 0.0
    fusion_method: str = "simple_fusion"
    keyword_result: Optional[ClassificationResult] = None
    llm_result: Optional[LLMClassificationResult] = None
    domain_scores: Dict[str, float] = None
    type_scores: Dict[str, float] = None
    complexity_scores: Dict[str, float] = None
    phase_scores: Dict[str, float] = None

class FusionStrategy(Enum):
    ADAPTIVE_FUSION = "adaptive_fusion"
    SIMPLE_FUSION = "simple_fusion"

class HybridFusionEngine:
    """Moteur de fusion hybride simplifié"""
    
    def __init__(self, fusion_strategy: FusionStrategy = FusionStrategy.ADAPTIVE_FUSION):
        self.fusion_strategy = fusion_strategy
        self.logger = logging.getLogger(__name__)
        
        # Classificateurs
        self.keyword_classifier = KeywordClassifier()
        self.llm_classifier = LLMClassifier()
        
        self.logger.info("HybridFusionEngine simplifié initialisé")
    
    def classify(self, text: str, context: Dict = None, use_cache: bool = True) -> HybridClassificationResult:
        """Classification hybride principale"""
        
        try:
            # Classification par mots-clés
            keyword_result = self.keyword_classifier.classify(text, context)
            
            # Classification LLM
            llm_result = self.llm_classifier.classify(text, context)
            
            # Fusion simple
            fusion_result = self._simple_fusion(keyword_result, llm_result)
            
            # Attribution des résultats individuels
            fusion_result.keyword_result = keyword_result
            fusion_result.llm_result = llm_result
            
            return fusion_result
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la classification hybride: {e}")
            return self._fallback_result()
    
    def _simple_fusion(self, keyword_result: ClassificationResult, llm_result: LLMClassificationResult) -> HybridClassificationResult:
        """Fusion simple entre les classificateurs"""
        
        # Extraction des meilleures valeurs
        keyword_domain = max(keyword_result.domain.items(), key=lambda x: x[1]) if keyword_result.domain else ("unknown", 0.0)
        keyword_type = max(keyword_result.type.items(), key=lambda x: x[1]) if keyword_result.type else ("unknown", 0.0)
        keyword_complexity = max(keyword_result.complexity.items(), key=lambda x: x[1]) if keyword_result.complexity else ("unknown", 0.0)
        keyword_phase = max(keyword_result.phase.items(), key=lambda x: x[1]) if keyword_result.phase else ("unknown", 0.0)
        
        # Fusion avec priorité au LLM
        final_domain = llm_result.domain if hasattr(llm_result, 'domain') and llm_result.domain else keyword_domain[0]
        final_type = llm_result.type if hasattr(llm_result, 'type') and llm_result.type else keyword_type[0]
        final_complexity = llm_result.complexity if hasattr(llm_result, 'complexity') and llm_result.complexity else keyword_complexity[0]
        final_phase = llm_result.phase if hasattr(llm_result, 'phase') and llm_result.phase else keyword_phase[0]
        
        # Confiances
        final_domain_conf = llm_result.domain_confidence if hasattr(llm_result, 'domain_confidence') else keyword_result.confidence
        final_type_conf = llm_result.type_confidence if hasattr(llm_result, 'type_confidence') else keyword_result.confidence
        final_complexity_conf = llm_result.complexity_confidence if hasattr(llm_result, 'complexity_confidence') else keyword_result.confidence
        final_phase_conf = llm_result.phase_confidence if hasattr(llm_result, 'phase_confidence') else keyword_result.confidence
        
        # Confiance globale
        fusion_confidence = (final_domain_conf + final_type_conf + final_complexity_conf + final_phase_conf) / 4
        
        return HybridClassificationResult(
            final_domain=final_domain,
            final_domain_confidence=final_domain_conf,
            final_type=final_type,
            final_type_confidence=final_type_conf,
            final_complexity=final_complexity,
            final_complexity_confidence=final_complexity_conf,
            final_phase=final_phase,
            final_phase_confidence=final_phase_conf,
            fusion_confidence=fusion_confidence,
            fusion_method="simple_fusion",
            domain_scores=keyword_result.domain if keyword_result.domain else {},
            type_scores=keyword_result.type if keyword_result.type else {},
            complexity_scores=keyword_result.complexity if keyword_result.complexity else {},
            phase_scores=keyword_result.phase if keyword_result.phase else {}
        )
    
    def _fuse_results(self, keyword_result: ClassificationResult, llm_result: LLMClassificationResult, text: str, context: Dict) -> HybridClassificationResult:
        """Méthode pour compatibilité avec l'orchestrateur"""
        return self._simple_fusion(keyword_result, llm_result)
    
    def _fallback_result(self) -> HybridClassificationResult:
        """Résultat de fallback en cas d'erreur"""
        return HybridClassificationResult(
            final_domain="unknown",
            final_domain_confidence=0.0,
            final_type="unknown",
            final_type_confidence=0.0,
            final_complexity="unknown",
            final_complexity_confidence=0.0,
            final_phase="unknown",
            final_phase_confidence=0.0,
            fusion_confidence=0.0,
            fusion_method="fallback"
        )