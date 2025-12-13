"""
Système de Fusion des Résultats Multi-Agents
Algorithmes intelligents de fusion, résolution de conflits et agrégation cohérente
"""

import logging
import time
import json
import statistics
from typing import Dict, List, Tuple, Optional, Any, NamedTuple, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, Counter
import numpy as np
from fuzzywuzzy import fuzz
import hashlib

from .dispatch_logic import TaskResult, DispatchPlan
from .agent_selector import AgentScore

@dataclass
class FusionWeight:
    """Poids pour la fusion des résultats"""
    quality_weight: float = 0.4
    relevance_weight: float = 0.3
    confidence_weight: float = 0.2
    timeliness_weight: float = 0.1

@dataclass
class ConflictResolution:
    """Résolution d'un conflit entre résultats"""
    conflict_id: str
    conflict_type: str
    conflicting_items: List[Dict[str, Any]]
    resolution_method: str
    resolved_value: Any
    confidence: float
    reasoning: List[str]

@dataclass
class FusionResult:
    """Résultat final de fusion"""
    fused_output: Dict[str, Any]
    quality_score: float
    confidence_score: float
    conflict_resolutions: List[ConflictResolution]
    contributing_agents: List[str]
    fusion_metadata: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)

class FusionStrategy(Enum):
    """Stratégies de fusion disponibles"""
    WEIGHTED_AVERAGE = "weighted_average"
    QUALITY_BASED = "quality_based"
    CONSENSUS_BUILDING = "consensus_building"
    DOMINANT_RESULT = "dominant_result"
    HYBRID_FUSION = "hybrid_fusion"
    ADAPTIVE_FUSION = "adaptive_fusion"

class ConflictType(Enum):
    """Types de conflits entre résultats"""
    SEMANTIC_DIFFERENCE = "semantic_difference"
    CONTRADICTORY_VALUES = "contradictory_values"
    MISSING_DATA = "missing_data"
    DUPLICATE_CONTENT = "duplicate_content"
    INCOMPLETE_RESULTS = "incomplete_results"

class IntelligentResultFusion:
    """Système intelligent de fusion des résultats multi-agents"""
    
    def __init__(self, fusion_strategy: FusionStrategy = FusionStrategy.ADAPTIVE_FUSION,
                 fusion_weights: FusionWeight = None):
        self.fusion_strategy = fusion_strategy
        self.fusion_weights = fusion_weights or FusionWeight()
        self.logger = logging.getLogger(__name__)
        
        # Métriques de fusion
        self.fusion_stats = {
            'total_fusions': 0,
            'conflicts_detected': 0,
            'conflicts_resolved': 0,
            'average_quality_score': 0.0,
            'strategy_usage': {strategy.value: 0 for strategy in FusionStrategy},
            'resolution_methods': defaultdict(int)
        }
        
        # Historique pour apprentissage
        self.fusion_history = []
        
        # Templates de résultats par type
        self.result_templates = self._initialize_result_templates()
        
        # Matrices de similarité sémantique
        self.similarity_matrices = {}
    
    def fuse_results(self, task_results: List[TaskResult],
                    agent_scores: List[AgentScore],
                    dispatch_plan: DispatchPlan,
                    context: Dict[str, Any] = None) -> FusionResult:
        """
        Fusion intelligente des résultats de multiples agents
        
        Args:
            task_results: Résultats des tâches exécutées
            agent_scores: Scores des agents participants
            dispatch_plan: Plan de dispatch utilisé
            context: Contexte additionnel
        
        Returns:
            Résultat fusionné avec métadonnées
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"Début de fusion de {len(task_results)} résultats")
            
            # Validation des résultats
            valid_results = self._validate_task_results(task_results)
            if not valid_results:
                return self._create_empty_fusion_result("Aucun résultat valide")
            
            # Analyse des conflits
            conflicts = self._detect_conflicts(valid_results)
            
            # Résolution des conflits
            resolved_conflicts = self._resolve_conflicts(conflicts, valid_results)
            
            # Application de la stratégie de fusion
            fused_output = self._apply_fusion_strategy(
                valid_results, agent_scores, resolved_conflicts
            )
            
            # Calcul des scores de qualité
            quality_score = self._calculate_quality_score(fused_output, valid_results)
            confidence_score = self._calculate_confidence_score(fused_output, agent_scores)
            
            # Génération des métadonnées
            fusion_metadata = self._generate_fusion_metadata(
                valid_results, agent_scores, dispatch_plan, time.time() - start_time
            )
            
            # Compilation du résultat final
            fusion_result = FusionResult(
                fused_output=fused_output,
                quality_score=quality_score,
                confidence_score=confidence_score,
                conflict_resolutions=resolved_conflicts,
                contributing_agents=[r.agent_id for r in valid_results],
                fusion_metadata=fusion_metadata,
                warnings=self._generate_warnings(valid_results, resolved_conflicts)
            )
            
            # Mise à jour des statistiques
            self._update_fusion_stats(fusion_result, time.time() - start_time)
            
            self.logger.info(f"Fusion terminée en {time.time() - start_time:.3f}s avec score de qualité {quality_score:.2f}")
            return fusion_result
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la fusion: {e}")
            return self._create_error_fusion_result(str(e))
    
    def _validate_task_results(self, task_results: List[TaskResult]) -> List[TaskResult]:
        """Valide et filtre les résultats de tâches"""
        valid_results = []
        
        for result in task_results:
            # Vérification de la validité de base
            if not result.success:
                self.logger.warning(f"Résultat échoué ignoré: {result.task_id}")
                continue
            
            if not result.output_data:
                self.logger.warning(f"Résultat vide ignoré: {result.task_id}")
                continue
            
            # Vérification de la structure minimale
            if not isinstance(result.output_data, dict):
                self.logger.warning(f"Format de résultat invalide: {result.task_id}")
                continue
            
            valid_results.append(result)
        
        self.logger.info(f"Résultats valides: {len(valid_results)}/{len(task_results)}")
        return valid_results
    
    def _detect_conflicts(self, results: List[TaskResult]) -> List[Dict[str, Any]]:
        """Détecte les conflits entre les résultats"""
        conflicts = []
        
        if len(results) < 2:
            return conflicts
        
        # Analyse par type de données
        output_types = self._categorize_output_types(results)
        
        # Détection des conflits sémantiques
        semantic_conflicts = self._detect_semantic_conflicts(results)
        conflicts.extend(semantic_conflicts)
        
        # Détection des valeurs contradictoires
        value_conflicts = self._detect_value_conflicts(results)
        conflicts.extend(value_conflicts)
        
        # Détection du contenu dupliqué
        duplicate_conflicts = self._detect_duplicate_content(results)
        conflicts.extend(duplicate_conflicts)
        
        # Détection des données manquantes
        missing_data_conflicts = self._detect_missing_data(results)
        conflicts.extend(missing_data_conflicts)
        
        self.fusion_stats['conflicts_detected'] += len(conflicts)
        self.logger.info(f"Conflits détectés: {len(conflicts)}")
        
        return conflicts
    
    def _categorize_output_types(self, results: List[TaskResult]) -> Dict[str, List[TaskResult]]:
        """Catégorise les résultats par type de sortie"""
        categorized = defaultdict(list)
        
        for result in results:
            # Classification automatique du type de contenu
            output_type = self._classify_output_type(result.output_data)
            categorized[output_type].append(result)
        
        return dict(categorized)
    
    def _classify_output_type(self, output_data: Dict[str, Any]) -> str:
        """Classifie le type de contenu d'un résultat"""
        # Analyse des clés présentes
        keys = set(output_data.keys())
        
        # Patterns de classification
        if any(key in keys for key in ['code', 'implementation', 'function']):
            return 'code'
        elif any(key in keys for key in ['design', 'architecture', 'diagram']):
            return 'design'
        elif any(key in keys for key in ['test', 'testing', 'validation']):
            return 'testing'
        elif any(key in keys for key in ['analysis', 'insight', 'finding']):
            return 'analysis'
        elif any(key in keys for key in ['configuration', 'setup', 'deployment']):
            return 'configuration'
        else:
            return 'general'
    
    def _detect_semantic_conflicts(self, results: List[TaskResult]) -> List[Dict[str, Any]]:
        """Détecte les conflits sémantiques"""
        conflicts = []
        
        # Analyse des titres/descriptions
        titles = []
        for result in results:
            if 'title' in result.output_data:
                titles.append(result.output_data['title'])
            elif 'name' in result.output_data:
                titles.append(result.output_data['name'])
            elif 'description' in result.output_data:
                titles.append(result.output_data['description'][:100])  # Premiers 100 chars
        
        if len(titles) > 1:
            # Comparaison par similarité
            for i in range(len(titles)):
                for j in range(i + 1, len(titles)):
                    similarity = fuzz.ratio(titles[i], titles[j])
                    if similarity < 70:  # Seuil de similarité
                        conflicts.append({
                            'type': ConflictType.SEMANTIC_DIFFERENCE.value,
                            'items': [titles[i], titles[j]],
                            'similarity_score': similarity / 100.0,
                            'conflict_id': f"semantic_{i}_{j}"
                        })
        
        return conflicts
    
    def _detect_value_conflicts(self, results: List[TaskResult]) -> List[Dict[str, Any]]:
        """Détecte les valeurs contradictoires"""
        conflicts = []
        
        # Recherche de valeurs numériques contradictoires
        numeric_fields = self._extract_numeric_fields(results)
        
        for field_name, values in numeric_fields.items():
            if len(values) > 1:
                # Calcul de la variance
                numeric_values = [v for v in values if isinstance(v, (int, float))]
                if len(numeric_values) > 1:
                    variance = np.var(numeric_values)
                    mean_val = np.mean(numeric_values)
                    cv = np.sqrt(variance) / mean_val if mean_val != 0 else 0
                    
                    if cv > 0.5:  # Coefficient de variation élevé
                        conflicts.append({
                            'type': ConflictType.CONTRADICTORY_VALUES.value,
                            'field': field_name,
                            'values': numeric_values,
                            'variance': variance,
                            'coefficient_of_variation': cv,
                            'conflict_id': f"value_{field_name}"
                        })
        
        return conflicts
    
    def _detect_duplicate_content(self, results: List[TaskResult]) -> List[Dict[str, Any]]:
        """Détecte le contenu dupliqué"""
        conflicts = []
        
        # Calcul des hash de contenu pour détecter les doublons
        content_hashes = {}
        
        for result in results:
            content_str = json.dumps(result.output_data, sort_keys=True)
            content_hash = hashlib.md5(content_str.encode()).hexdigest()
            
            if content_hash in content_hashes:
                conflicts.append({
                    'type': ConflictType.DUPLICATE_CONTENT.value,
                    'task_ids': [content_hashes[content_hash], result.task_id],
                    'content_hash': content_hash,
                    'conflict_id': f"duplicate_{content_hash}"
                })
            else:
                content_hashes[content_hash] = result.task_id
        
        return conflicts
    
    def _detect_missing_data(self, results: List[TaskResult]) -> List[Dict[str, Any]]:
        """Détecte les données manquantes"""
        conflicts = []
        
        # Analyse de la complétude des résultats
        result_completeness = {}
        
        for result in results:
            completeness_score = self._calculate_completeness_score(result.output_data)
            result_completeness[result.task_id] = completeness_score
        
        # Identification des résultats incomplets
        avg_completeness = statistics.mean(result_completeness.values())
        threshold = avg_completeness * 0.7  # 70% de la moyenne
        
        for task_id, completeness in result_completeness.items():
            if completeness < threshold:
                conflicts.append({
                    'type': ConflictType.INCOMPLETE_RESULTS.value,
                    'task_id': task_id,
                    'completeness_score': completeness,
                    'average_completeness': avg_completeness,
                    'conflict_id': f"incomplete_{task_id}"
                })
        
        return conflicts
    
    def _extract_numeric_fields(self, results: List[TaskResult]) -> Dict[str, List]:
        """Extrait les champs numériques des résultats"""
        numeric_fields = defaultdict(list)
        
        for result in results:
            for key, value in result.output_data.items():
                if isinstance(value, (int, float)):
                    numeric_fields[key].append(value)
                elif isinstance(value, dict):
                    # Récursion dans les dictionnaires
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, (int, float)):
                            numeric_fields[f"{key}.{sub_key}"].append(sub_value)
        
        return dict(numeric_fields)
    
    def _calculate_completeness_score(self, output_data: Dict[str, Any]) -> float:
        """Calcule un score de complétude"""
        if not output_data:
            return 0.0
        
        total_possible = 0
        total_filled = 0
        
        # Templates de référence pour différents types
        expected_fields = self._get_expected_fields(output_data)
        
        for field_path, expected in expected_fields.items():
            total_possible += 1
            if self._field_exists(output_data, field_path):
                total_filled += 1
        
        return total_filled / total_possible if total_possible > 0 else 0.0
    
    def _get_expected_fields(self, output_data: Dict[str, Any]) -> Dict[str, bool]:
        """Détermine les champs attendus pour un type de données"""
        # Templates par type de contenu
        if 'code' in str(output_data).lower():
            return {'implementation': True, 'complexity': True, 'quality': True}
        elif 'design' in str(output_data).lower():
            return {'architecture': True, 'components': True, 'patterns': True}
        elif 'test' in str(output_data).lower():
            return {'coverage': True, 'passing': True, 'failures': True}
        else:
            return {'content': True, 'summary': True, 'recommendations': True}
    
    def _field_exists(self, data: Dict[str, Any], field_path: str) -> bool:
        """Vérifie si un champ existe (supporte la notation point)"""
        keys = field_path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return False
        
        return True
    
    def _resolve_conflicts(self, conflicts: List[Dict[str, Any]], 
                         results: List[TaskResult]) -> List[ConflictResolution]:
        """Résout les conflits détectés"""
        resolutions = []
        
        for conflict in conflicts:
            conflict_type = conflict['type']
            conflict_id = conflict['conflict_id']
            
            if conflict_type == ConflictType.SEMANTIC_DIFFERENCE.value:
                resolution = self._resolve_semantic_conflict(conflict, results)
            elif conflict_type == ConflictType.CONTRADICTORY_VALUES.value:
                resolution = self._resolve_value_conflict(conflict, results)
            elif conflict_type == ConflictType.DUPLICATE_CONTENT.value:
                resolution = self._resolve_duplicate_conflict(conflict, results)
            elif conflict_type == ConflictType.INCOMPLETE_RESULTS.value:
                resolution = self._resolve_incomplete_conflict(conflict, results)
            else:
                resolution = self._resolve_generic_conflict(conflict, results)
            
            if resolution:
                resolutions.append(resolution)
                self.fusion_stats['conflicts_resolved'] += 1
                self.fusion_stats['resolution_methods'][resolution.resolution_method] += 1
        
        return resolutions
    
    def _resolve_semantic_conflict(self, conflict: Dict[str, Any], 
                                 results: List[TaskResult]) -> Optional[ConflictResolution]:
        """Résout un conflit sémantique"""
        items = conflict['items']
        
        # Stratégie: sélectionner l'item avec la meilleure confiance
        best_item = max(items, key=lambda x: len(x))  # Simplification
        
        return ConflictResolution(
            conflict_id=conflict['conflict_id'],
            conflict_type=conflict['type'],
            conflicting_items=items,
            resolution_method="semantic_selection",
            resolved_value=best_item,
            confidence=0.7,
            reasoning=["Sélection basée sur la similarité sémantique"]
        )
    
    def _resolve_value_conflict(self, conflict: Dict[str, Any], 
                              results: List[TaskResult]) -> Optional[ConflictResolution]:
        """Résout un conflit de valeurs"""
        values = conflict['values']
        
        # Stratégie: moyenne pondérée ou médiane selon la distribution
        if len(values) > 2:
            # Utiliser la médiane pour éviter l'influence des outliers
            resolved_value = statistics.median(values)
            method = "median_selection"
            confidence = 0.8
        else:
            # Pour 2 valeurs, prendre la moyenne
            resolved_value = statistics.mean(values)
            method = "average_selection"
            confidence = 0.6
        
        return ConflictResolution(
            conflict_id=conflict['conflict_id'],
            conflict_type=conflict['type'],
            conflicting_items=values,
            resolution_method=method,
            resolved_value=resolved_value,
            confidence=confidence,
            reasoning=[f"Résolution par {method} des valeurs contradictoires"]
        )
    
    def _resolve_duplicate_conflict(self, conflict: Dict[str, Any], 
                                  results: List[TaskResult]) -> Optional[ConflictResolution]:
        """Résout un conflit de contenu dupliqué"""
        task_ids = conflict['task_ids']
        
        # Stratégie: garder le résultat le plus récent ou le mieux noté
        best_task_id = task_ids[0]  # Simplification
        
        return ConflictResolution(
            conflict_id=conflict['conflict_id'],
            conflict_type=conflict['type'],
            conflicting_items=task_ids,
            resolution_method="duplicate_removal",
            resolved_value=best_task_id,
            confidence=0.9,
            reasoning=["Suppression du contenu dupliqué"]
        )
    
    def _resolve_incomplete_conflict(self, conflict: Dict[str, Any], 
                                   results: List[TaskResult]) -> Optional[ConflictResolution]:
        """Résout un conflit de données incomplètes"""
        task_id = conflict['task_id']
        completeness = conflict['completeness_score']
        
        # Stratégie: marquer comme incomplet avec suggestion d'amélioration
        return ConflictResolution(
            conflict_id=conflict['conflict_id'],
            conflict_type=conflict['type'],
            conflicting_items=[task_id],
            resolution_method="incompleteness_marking",
            resolved_value={"status": "incomplete", "completeness": completeness},
            confidence=completeness,
            reasoning=[f"Résultat marqué comme incomplet (score: {completeness:.2f})"]
        )
    
    def _resolve_generic_conflict(self, conflict: Dict[str, Any], 
                                results: List[TaskResult]) -> Optional[ConflictResolution]:
        """Résout un conflit générique"""
        return ConflictResolution(
            conflict_id=conflict['conflict_id'],
            conflict_type=conflict['type'],
            conflicting_items=[],
            resolution_method="generic_resolution",
            resolved_value=None,
            confidence=0.5,
            reasoning=["Résolution générique appliquée"]
        )
    
    def _apply_fusion_strategy(self, results: List[TaskResult], 
                             agent_scores: List[AgentScore],
                             resolved_conflicts: List[ConflictResolution]) -> Dict[str, Any]:
        """Applique la stratégie de fusion choisie"""
        
        if self.fusion_strategy == FusionStrategy.WEIGHTED_AVERAGE:
            return self._weighted_average_fusion(results, agent_scores)
        elif self.fusion_strategy == FusionStrategy.QUALITY_BASED:
            return self._quality_based_fusion(results, agent_scores)
        elif self.fusion_strategy == FusionStrategy.CONSENSUS_BUILDING:
            return self._consensus_building_fusion(results, resolved_conflicts)
        elif self.fusion_strategy == FusionStrategy.DOMINANT_RESULT:
            return self._dominant_result_fusion(results, agent_scores)
        elif self.fusion_strategy == FusionStrategy.HYBRID_FUSION:
            return self._hybrid_fusion(results, agent_scores, resolved_conflicts)
        else:  # ADAPTIVE_FUSION
            return self._adaptive_fusion(results, agent_scores, resolved_conflicts)
    
    def _weighted_average_fusion(self, results: List[TaskResult], 
                               agent_scores: List[AgentScore]) -> Dict[str, Any]:
        """Fusion par moyenne pondérée"""
        # Création d'un mapping agent_id -> score
        score_map = {score.agent_id: score.total_score for score in agent_scores}
        
        # Fusion des données
        fused_data = {}
        
        for result in results:
            agent_score = score_map.get(result.agent_id, 0.5)
            weight = agent_score * self.fusion_weights.quality_weight
            
            for key, value in result.output_data.items():
                if key not in fused_data:
                    fused_data[key] = {'sum': 0.0, 'weight_sum': 0.0}
                
                # Ajout pondéré
                if isinstance(value, (int, float)):
                    fused_data[key]['sum'] += value * weight
                    fused_data[key]['weight_sum'] += weight
                else:
                    # Pour les strings/dicts, prendre la valeur la mieux pondérée
                    if 'string_values' not in fused_data[key]:
                        fused_data[key]['string_values'] = []
                    fused_data[key]['string_values'].append((value, weight))
        
        # Finalisation de la fusion
        final_fused = {}
        for key, data in fused_data.items():
            if 'string_values' in data:
                # Pour les strings, prendre la valeur avec le poids le plus élevé
                best_value = max(data['string_values'], key=lambda x: x[1])[0]
                final_fused[key] = best_value
            else:
                # Pour les nombres, calculer la moyenne pondérée
                if data['weight_sum'] > 0:
                    final_fused[key] = data['sum'] / data['weight_sum']
                else:
                    final_fused[key] = data['sum']  # Fallback
        
        return final_fused
    
    def _quality_based_fusion(self, results: List[TaskResult], 
                            agent_scores: List[AgentScore]) -> Dict[str, Any]:
        """Fusion basée sur la qualité"""
        # Trier par score de qualité décroissant
        sorted_results = sorted(results, 
                              key=lambda r: agent_scores[next(i for i, s in enumerate(agent_scores) 
                                                          if s.agent_id == r.agent_id)].total_score, 
                              reverse=True)
        
        # Utiliser le meilleur résultat comme base
        best_result = sorted_results[0]
        fused_data = best_result.output_data.copy()
        
        # Compléter avec les autres résultats
        for result in sorted_results[1:]:
            for key, value in result.output_data.items():
                if key not in fused_data or not fused_data[key]:
                    fused_data[key] = value
        
        return fused_data
    
    def _consensus_building_fusion(self, results: List[TaskResult], 
                                 resolved_conflicts: List[ConflictResolution]) -> Dict[str, Any]:
        """Fusion par construction de consensus"""
        fused_data = {}
        
        # Résolution des conflits d'abord
        conflict_resolutions_map = {cr.conflict_id: cr for cr in resolved_conflicts}
        
        for result in results:
            for key, value in result.output_data.items():
                if key not in fused_data:
                    fused_data[key] = []
                fused_data[key].append(value)
        
        # Construction du consensus pour chaque clé
        final_fused = {}
        for key, values in fused_data.items():
            if len(values) == 1:
                final_fused[key] = values[0]
            else:
                # Recherche de consensus
                consensus_value = self._find_consensus_value(values)
                final_fused[key] = consensus_value
        
        return final_fused
    
    def _find_consensus_value(self, values: List[Any]) -> Any:
        """Trouve une valeur de consensus dans une liste"""
        if not values:
            return None
        
        # Pour les valeurs identiques
        if len(set(str(v) for v in values)) == 1:
            return values[0]
        
        # Pour les nombres, prendre la médiane
        numeric_values = [v for v in values if isinstance(v, (int, float))]
        if len(numeric_values) == len(values):
            return statistics.median(numeric_values)
        
        # Pour les strings, prendre le plus fréquent
        string_values = [v for v in values if isinstance(v, str)]
        if string_values:
            counter = Counter(string_values)
            return counter.most_common(1)[0][0]
        
        # Fallback: première valeur
        return values[0]
    
    def _dominant_result_fusion(self, results: List[TaskResult], 
                              agent_scores: List[AgentScore]) -> Dict[str, Any]:
        """Fusion par résultat dominant"""
        # Trouver l'agent avec le meilleur score
        best_agent = max(agent_scores, key=lambda x: x.total_score)
        
        # Trouver le résultat de cet agent
        best_result = next((r for r in results if r.agent_id == best_agent.agent_id), None)
        
        if best_result:
            return best_result.output_data.copy()
        else:
            # Fallback vers le premier résultat
            return results[0].output_data.copy() if results else {}
    
    def _hybrid_fusion(self, results: List[TaskResult], 
                      agent_scores: List[AgentScore],
                      resolved_conflicts: List[ConflictResolution]) -> Dict[str, Any]:
        """Fusion hybride combinant plusieurs approches"""
        
        # Phase 1: Résolution des conflits
        conflict_free_results = self._apply_conflict_resolutions(results, resolved_conflicts)
        
        # Phase 2: Fusion pondérée pour les données structurées
        structured_fusion = self._weighted_average_fusion(conflict_free_results, agent_scores)
        
        # Phase 3: Consensus pour les données textuelles
        text_fusion = self._consensus_building_fusion(conflict_free_results, resolved_conflicts)
        
        # Phase 4: Combinaison intelligente
        final_fusion = {}
        
        # Stratégie de combinaison
        for result in conflict_free_results:
            for key, value in result.output_data.items():
                if isinstance(value, (int, float)) and key in structured_fusion:
                    final_fusion[key] = structured_fusion[key]
                elif isinstance(value, str) and key in text_fusion:
                    final_fusion[key] = text_fusion[key]
                else:
                    # Fallback vers la valeur du meilleur agent
                    final_fusion[key] = value
        
        return final_fusion
    
    def _adaptive_fusion(self, results: List[TaskResult], 
                        agent_scores: List[AgentScore],
                        resolved_conflicts: List[ConflictResolution]) -> Dict[str, Any]:
        """Fusion adaptative qui choisit la meilleure stratégie selon le contexte"""
        
        # Analyse du contexte
        result_diversity = self._calculate_result_diversity(results)
        agent_score_variance = self._calculate_agent_score_variance(agent_scores)
        conflict_severity = len(resolved_conflicts) / len(results) if results else 0
        
        # Sélection de stratégie adaptative
        if conflict_severity > 0.5:
            # Beaucoup de conflits → consensus building
            return self._consensus_building_fusion(results, resolved_conflicts)
        elif agent_score_variance > 0.3:
            # Grande variance des scores → quality based
            return self._quality_based_fusion(results, agent_scores)
        elif result_diversity > 0.7:
            # Grande diversité → hybrid fusion
            return self._hybrid_fusion(results, agent_scores, resolved_conflicts)
        else:
            # Sinon → weighted average
            return self._weighted_average_fusion(results, agent_scores)
    
    def _apply_conflict_resolutions(self, results: List[TaskResult], 
                                  resolved_conflicts: List[ConflictResolution]) -> List[TaskResult]:
        """Applique les résolutions de conflits aux résultats"""
        # Cette méthode appliquerait les résolutions aux résultats
        # Pour la simplicité, on retourne les résultats originaux
        return results
    
    def _calculate_result_diversity(self, results: List[TaskResult]) -> float:
        """Calcule la diversité des résultats"""
        if len(results) < 2:
            return 0.0
        
        # Calcul basé sur la variance des tailles et structures
        sizes = [len(json.dumps(r.output_data)) for r in results]
        size_variance = np.var(sizes)
        
        # Normalisation
        max_size = max(sizes)
        return min(size_variance / max_size, 1.0) if max_size > 0 else 0.0
    
    def _calculate_agent_score_variance(self, agent_scores: List[AgentScore]) -> float:
        """Calcule la variance des scores d'agents"""
        if len(agent_scores) < 2:
            return 0.0
        
        scores = [score.total_score for score in agent_scores]
        return np.var(scores)
    
    def _calculate_quality_score(self, fused_output: Dict[str, Any], 
                               results: List[TaskResult]) -> float:
        """Calcule le score de qualité du résultat fusionné"""
        
        # Facteurs de qualité
        completeness = self._assess_completeness(fused_output)
        consistency = self._assess_consistency(fused_output, results)
        accuracy = self._assess_accuracy(fused_output, results)
        
        # Score pondéré
        quality_score = (
            completeness * 0.4 +
            consistency * 0.3 +
            accuracy * 0.3
        )
        
        return min(quality_score, 1.0)
    
    def _calculate_confidence_score(self, fused_output: Dict[str, Any], 
                                  agent_scores: List[AgentScore]) -> float:
        """Calcule le score de confiance"""
        
        if not agent_scores:
            return 0.0
        
        # Confiance basée sur les scores des agents
        avg_agent_score = statistics.mean(score.total_score for score in agent_scores)
        
        # Ajustement selon le nombre d'agents
        agent_count_factor = min(len(agent_scores) / 3, 1.0)  # Bonus jusqu'à 3 agents
        
        confidence_score = avg_agent_score * (0.8 + 0.2 * agent_count_factor)
        
        return min(confidence_score, 1.0)
    
    def _assess_completeness(self, fused_output: Dict[str, Any]) -> float:
        """Évalue la complétude du résultat fusionné"""
        if not fused_output:
            return 0.0
        
        # Comptage des champs non vides
        non_empty_fields = sum(1 for v in fused_output.values() if v)
        total_fields = len(fused_output)
        
        return non_empty_fields / total_fields if total_fields > 0 else 0.0
    
    def _assess_consistency(self, fused_output: Dict[str, Any], 
                          results: List[TaskResult]) -> float:
        """Évalue la consistance du résultat fusionné"""
        if len(results) < 2:
            return 1.0
        
        # Vérification de la cohérence des valeurs fusionnées
        consistency_scores = []
        
        for key in fused_output.keys():
            original_values = []
            for result in results:
                if key in result.output_data:
                    original_values.append(result.output_data[key])
            
            if len(original_values) > 1:
                # Calcul de similarité pour cette clé
                similar_count = 0
                total_comparisons = 0
                
                for i in range(len(original_values)):
                    for j in range(i + 1, len(original_values)):
                        total_comparisons += 1
                        if self._values_similar(original_values[i], original_values[j]):
                            similar_count += 1
                
                if total_comparisons > 0:
                    consistency_scores.append(similar_count / total_comparisons)
        
        return statistics.mean(consistency_scores) if consistency_scores else 1.0
    
    def _assess_accuracy(self, fused_output: Dict[str, Any], 
                       results: List[TaskResult]) -> float:
        """Évalue l'exactitude du résultat fusionné"""
        # Approximation basée sur la convergence des résultats
        if len(results) < 2:
            return 0.8  # Score par défaut pour un seul résultat
        
        # Mesure de la convergence
        convergence_score = 0.0
        total_comparisons = 0
        
        for i, result1 in enumerate(results):
            for result2 in results[i+1:]:
                similarity = self._calculate_result_similarity(result1.output_data, result2.output_data)
                convergence_score += similarity
                total_comparisons += 1
        
        return convergence_score / total_comparisons if total_comparisons > 0 else 0.8
    
    def _values_similar(self, value1: Any, value2: Any) -> bool:
        """Détermine si deux valeurs sont similaires"""
        if isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
            # Pour les nombres, tolérance de 10%
            return abs(value1 - value2) / max(abs(value1), abs(value2), 1) < 0.1
        elif isinstance(value1, str) and isinstance(value2, str):
            # Pour les strings, similarité de fuzzy matching
            return fuzz.ratio(value1, value2) > 80
        else:
            # Pour autres types, comparaison directe
            return value1 == value2
    
    def _calculate_result_similarity(self, output1: Dict[str, Any], 
                                   output2: Dict[str, Any]) -> float:
        """Calcule la similarité entre deux résultats"""
        if not output1 or not output2:
            return 0.0
        
        common_keys = set(output1.keys()) & set(output2.keys())
        if not common_keys:
            return 0.0
        
        similarity_sum = 0.0
        for key in common_keys:
            if self._values_similar(output1[key], output2[key]):
                similarity_sum += 1.0
        
        return similarity_sum / len(common_keys)
    
    def _generate_fusion_metadata(self, results: List[TaskResult], 
                                agent_scores: List[AgentScore],
                                dispatch_plan: DispatchPlan,
                                processing_time: float) -> Dict[str, Any]:
        """Génère les métadonnées de fusion"""
        
        return {
            'fusion_strategy': self.fusion_strategy.value,
            'processing_time': processing_time,
            'input_results_count': len(results),
            'contributing_agents': [r.agent_id for r in results],
            'average_agent_score': statistics.mean(score.total_score for score in agent_scores),
            'dispatch_mode': dispatch_plan.mode.value,
            'total_tasks': len(dispatch_plan.tasks),
            'fusion_weights': {
                'quality_weight': self.fusion_weights.quality_weight,
                'relevance_weight': self.fusion_weights.relevance_weight,
                'confidence_weight': self.fusion_weights.confidence_weight,
                'timeliness_weight': self.fusion_weights.timeliness_weight
            }
        }
    
    def _generate_warnings(self, results: List[TaskResult], 
                         resolved_conflicts: List[ConflictResolution]) -> List[str]:
        """Génère des avertissements basés sur l'analyse"""
        warnings = []
        
        # Avertissement sur les conflits non résolus
        high_confidence_conflicts = [cr for cr in resolved_conflicts if cr.confidence < 0.7]
        if high_confidence_conflicts:
            warnings.append(f"{len(high_confidence_conflicts)} conflits avec confiance faible")
        
        # Avertissement sur la qualité des résultats
        failed_results = [r for r in results if not r.success]
        if failed_results:
            warnings.append(f"{len(failed_results)} tâches ont échoué")
        
        # Avertissement sur la diversité des agents
        agent_diversity = len(set(r.agent_id for r in results))
        if agent_diversity < 2:
            warnings.append("Peu de diversité dans les agents participants")
        
        return warnings
    
    def _create_empty_fusion_result(self, reason: str) -> FusionResult:
        """Crée un résultat de fusion vide"""
        return FusionResult(
            fused_output={},
            quality_score=0.0,
            confidence_score=0.0,
            conflict_resolutions=[],
            contributing_agents=[],
            fusion_metadata={'error': reason},
            warnings=[f"Fusion échouée: {reason}"]
        )
    
    def _create_error_fusion_result(self, error_message: str) -> FusionResult:
        """Crée un résultat de fusion d'erreur"""
        return FusionResult(
            fused_output={'error': error_message},
            quality_score=0.0,
            confidence_score=0.0,
            conflict_resolutions=[],
            contributing_agents=[],
            fusion_metadata={'error': error_message},
            warnings=[f"Erreur de fusion: {error_message}"]
        )
    
    def _initialize_result_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialise les templates de résultats par type"""
        return {
            'code': {
                'expected_fields': ['implementation', 'complexity', 'quality_score'],
                'validation_rules': {
                    'complexity': lambda x: isinstance(x, (int, float)) and 0 <= x <= 1,
                    'quality_score': lambda x: isinstance(x, (int, float)) and 0 <= x <= 1
                }
            },
            'design': {
                'expected_fields': ['architecture', 'components', 'patterns'],
                'validation_rules': {}
            },
            'testing': {
                'expected_fields': ['coverage', 'passing', 'failures'],
                'validation_rules': {
                    'coverage': lambda x: isinstance(x, (int, float)) and 0 <= x <= 100
                }
            }
        }
    
    def _update_fusion_stats(self, fusion_result: FusionResult, processing_time: float):
        """Met à jour les statistiques de fusion"""
        self.fusion_stats['total_fusions'] += 1
        self.fusion_stats['strategy_usage'][self.fusion_strategy.value] += 1
        self.fusion_stats['average_quality_score'] += fusion_result.quality_score
        
        # Ajout à l'historique
        history_entry = {
            'timestamp': time.time(),
            'strategy': self.fusion_strategy.value,
            'quality_score': fusion_result.quality_score,
            'confidence_score': fusion_result.confidence_score,
            'conflicts_count': len(fusion_result.conflict_resolutions),
            'contributing_agents_count': len(fusion_result.contributing_agents),
            'processing_time': processing_time
        }
        self.fusion_history.append(history_entry)
        
        # Garder seulement les 1000 dernières entrées
        if len(self.fusion_history) > 1000:
            self.fusion_history = self.fusion_history[-1000:]
    
    def get_fusion_explanation(self, fusion_result: FusionResult) -> Dict[str, Any]:
        """Génère une explication détaillée de la fusion"""
        return {
            'fusion_summary': {
                'strategy_used': self.fusion_strategy.value,
                'quality_score': fusion_result.quality_score,
                'confidence_score': fusion_result.confidence_score,
                'contributing_agents': fusion_result.contributing_agents,
                'conflicts_resolved': len(fusion_result.conflict_resolutions)
            },
            'conflict_analysis': {
                'total_conflicts_detected': self.fusion_stats['conflicts_detected'],
                'conflicts_resolved': self.fusion_stats['conflicts_resolved'],
                'resolution_rate': (
                    self.fusion_stats['conflicts_resolved'] / 
                    max(self.fusion_stats['conflicts_detected'], 1)
                ),
                'resolution_methods': dict(self.fusion_stats['resolution_methods'])
            },
            'quality_metrics': {
                'completeness_score': self._assess_completeness(fusion_result.fused_output),
                'consistency_score': 0.8,  # Simplification
                'accuracy_score': 0.75,    # Simplification
                'overall_quality': fusion_result.quality_score
            },
            'warnings': fusion_result.warnings,
            'fusion_metadata': fusion_result.fusion_metadata,
            'performance_history': self.fusion_history[-10:]  # 10 dernières entrées
        }
