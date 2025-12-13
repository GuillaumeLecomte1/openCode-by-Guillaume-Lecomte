
"""
Configuration simplifiée des dictionnaires de mots-clés
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class KeywordPattern:
    pattern: str
    weight: float
    priority: int
    regex: bool = False

class KeywordsConfig:
    DOMAINS = {
        "web_development": {
            "high_priority": [
                KeywordPattern("react", 1.0, 1),
                KeywordPattern("angular", 1.0, 1),
                KeywordPattern("vue", 1.0, 1),
                KeywordPattern("django", 1.0, 1),
                KeywordPattern("flask", 1.0, 1),
            ],
            "medium_priority": [
                KeywordPattern("frontend", 0.8, 2),
                KeywordPattern("backend", 0.8, 2),
                KeywordPattern("api", 0.7, 3),
            ],
            "patterns": [
                r"\b(react|angular|vue)\b",
                r"\b(frontend|backend)\b",
            ]
        },
        "data_science": {
            "high_priority": [
                KeywordPattern("pandas", 1.0, 1),
                KeywordPattern("numpy", 1.0, 1),
                KeywordPattern("machine learning", 1.0, 1),
            ],
            "medium_priority": [
                KeywordPattern("data analysis", 0.7, 3),
                KeywordPattern("visualization", 0.6, 3),
            ],
            "patterns": [
                r"\b(pandas|numpy)\b",
                r"\b(machine learning|data)\b",
            ]
        }
    }
    
    PROJECT_TYPES = {
        "web_application": [
            KeywordPattern("website", 1.0, 1),
            KeywordPattern("web app", 1.0, 1),
        ],
        "library": [
            KeywordPattern("library", 1.0, 1),
            KeywordPattern("framework", 0.9, 1),
        ],
    }
    
    COMPLEXITY_LEVELS = {
        "beginner": {
            "indicators": [
                KeywordPattern("hello world", 1.0, 1),
                KeywordPattern("tutorial", 0.9, 1),
            ],
            "code_patterns": [
                r"print",
                r"console.log",
            ]
        },
        "intermediate": {
            "indicators": [
                KeywordPattern("CRUD", 0.9, 1),
                KeywordPattern("database", 0.8, 2),
            ],
            "code_patterns": [
                r"database",
                r"api",
            ]
        },
        "advanced": {
            "indicators": [
                KeywordPattern("microservices", 1.0, 1),
                KeywordPattern("distributed", 0.9, 1),
            ],
            "code_patterns": [
                r"microservice",
                r"distributed",
            ]
        }
    }
    
    PROJECT_PHASES = {
        "planning": [
            KeywordPattern("design", 0.9, 1),
            KeywordPattern("architecture", 0.9, 1),
        ],
        "development": [
            KeywordPattern("implementation", 1.0, 1),
            KeywordPattern("coding", 0.9, 1),
        ],
        "testing": [
            KeywordPattern("test", 1.0, 1),
            KeywordPattern("testing", 1.0, 1),
        ],
        "deployment": [
            KeywordPattern("deploy", 1.0, 1),
            KeywordPattern("production", 0.9, 1),
        ]
    }
    
    GLOBAL_PATTERNS = {
        "file_indicators": {
            "readme": r"\breadme\.md\b",
            "license": r"\blicense\b",
        }
    }
    
    @classmethod
    def get_scoring_weights(cls):
        return {"domain": 0.3, "type": 0.25, "complexity": 0.25, "phase": 0.2}
    
    @classmethod
    def get_priority_thresholds(cls):
        return {"high_confidence": 0.8, "medium_confidence": 0.6, "low_confidence": 0.4}
