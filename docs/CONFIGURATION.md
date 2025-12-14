# Guide de Configuration OpenCode v3.0

⚙️ **Configuration avancée pour l'environnement E-commerce + Orchestration**

Ce guide détaille toutes les options de configuration disponibles pour optimiser votre environnement OpenCode selon vos besoins spécifiques.

---

## 📁 Structure de Configuration

### Fichiers de Configuration

```
config/
├── opencode.json          # Configuration principale OpenCode
├── agents.json           # Métadonnées des agents
└── project.json          # Template de configuration projet
```

### Fichiers de Scripts

```
scripts/
├── install.sh            # Installation complète
├── update.sh             # Mise à jour depuis le repo
├── sync-agents.sh        # Synchronisation agents
└── validate-config.sh    # Validation configuration
```

---

## 🔧 Configuration Principale (opencode.json)

### Section Modèles

```json
{
  "model": "minimax-M2",
  "small_model": "grok-code-fast-1"
}
```

#### Paramètres Disponibles

| Modèle               | Usage                                           | Coût   | Complexité |
| -------------------- | ----------------------------------------------- | ------ | ---------- |
| **minimax-M2**       | Analyses complexes, architecture, orchestration | Élevé  | Haute      |
| **grok-code-fast-1** | Tâches simples, documentation                   | Faible | Basse      |
| **gpt-4**            | Analyses générales (si disponible)              | Moyen  | Haute      |
| **claude-3**         | Analyses générales (si disponible)              | Moyen  | Haute      |

### Section Outils

```json
{
  "tools": {
    "write": true,
    "edit": true,
    "read": true,
    "bash": true,
    "glob": true,
    "grep": true,
    "list": true,
    "webfetch": true,
    "task": true,
    "todowrite": true,
    "todoread": true
  }
}
```

#### Configuration des Permissions

```json
{
  "permission": {
    "bash": "ask", // ask, auto, deny
    "edit": "auto", // auto, ask, deny
    "write": "auto" // auto, ask, deny
  }
}
```

### Section Orchestrateur

#### Routing de Modèles

```json
{
  "orchestrator_config": {
    "model_routing": {
      "primary_model": {
        "name": "minimax-M2",
        "usage": "Analyses complexes et architecture",
        "cost_optimization": false,
        "confidence_threshold": 0.8,
        "specialties": [
          "Architecture logicielle complexe",
          "Analyse de patterns de design",
          "Optimisation des performances"
        ]
      },
      "fast_model": {
        "name": "grok-code-fast-1",
        "usage": "Tâches rapides et simples",
        "cost_optimization": true,
        "confidence_threshold": 0.6,
        "specialties": [
          "Analyses syntaxiques",
          "Suggestions de code simples",
          "Documentation basique"
        ]
      }
    }
  }
}
```

#### Dispatch Modes

```json
{
  "dispatch_modes": {
    "orchestration": {
      "mode": "HYBRID", // SEQUENTIAL, PARALLEL, HYBRID
      "agents": ["orchestrator", "frontend-react-specialist"],
      "model_strategy": "primary_model_priority",
      "timeout": 300, // Timeout en secondes
      "retry_attempts": 2
    }
  }
}
```

##### Modes de Dispatch

| Mode           | Description               | Usage Recommandé           |
| -------------- | ------------------------- | -------------------------- |
| **SEQUENTIAL** | Exécution séquentielle    | Planification, déploiement |
| **PARALLEL**   | Exécution parallèle       | Backend, frontend          |
| **HYBRID**     | Coordination intelligente | Orchestration, intégration |

#### Spécialisation E-commerce

```json
{
  "ecommerce_specialization": {
    "domain_agents": [
      "frontend-react-specialist",
      "backend-nodejs-specialist",
      "mongodb-specialist",
      "ecommerce-business-logic"
    ],
    "priority_score": {
      "minimax-M2": 0.9,
      "grok-code-fast-1": 0.6
    },
    "patterns": ["shopping_cart", "payment_processing", "inventory_management"]
  }
}
```

### Section Optimisation Performance

```json
{
  "performance_optimization": {
    "execution_thresholds": {
      "fast_task_threshold": 30, // Tâches < 30s = fast model
      "complex_task_threshold": 120, // Tâches > 120s = modèle principal
      "parallel_execution_limit": 4,
      "max_concurrent_agents": 6
    },
    "model_switching_rules": {
      "confidence_based_switching": true,
      "cost_optimization": true,
      "quality_threshold": 0.8
    }
  }
}
```

---

## 🤖 Configuration des Agents

### Métadonnées (agents.json)

#### Structure des Agents

```json
{
  "agents": {
    "agent-name": {
      "name": "Nom Affiché",
      "category": "E-commerce", // Core, E-commerce, Architecture, Quality, Research
      "type": "specialist", // orchestrator, specialist, coordinator, builder
      "description": "Description",
      "priority": "high", // high, medium, low
      "model": "minimax-M2",
      "capabilities": ["capability1", "capability2"],
      "ecommerce_focus": true,
      "aliases": ["alias1", "alias2"]
    }
  }
}
```

#### Catégories d'Agents

| Catégorie        | Description                   | Agents                              |
| ---------------- | ----------------------------- | ----------------------------------- |
| **Core**         | Agents principaux             | orchestrator, plan, build           |
| **E-commerce**   | Agents e-commerce spécialisés | 6 agents                            |
| **Architecture** | Agents d'architecture         | angular-architect, system-architect |
| **Quality**      | Agents qualité                | code-reviewer, performance-engineer |
| **Research**     | Agents recherche              | tech-stack-researcher               |

---

## 🔄 Workflows Prédéfinis

### Workflow E-commerce Full Stack

```json
{
  "workflows": {
    "ecommerce_fullstack": {
      "name": "E-commerce Full Stack Development",
      "phases": [
        {
          "name": "Architecture",
          "mode": "SEQUENTIAL",
          "agents": ["system-architect", "plan"],
          "estimated_duration": "30-60 min"
        },
        {
          "name": "Backend Development",
          "mode": "PARALLEL",
          "agents": ["backend-nodejs-specialist", "mongodb-specialist"],
          "estimated_duration": "2-3h"
        },
        {
          "name": "Frontend Development",
          "mode": "PARALLEL",
          "agents": ["frontend-react-specialist", "ecommerce-business-logic"],
          "estimated_duration": "2-3h"
        }
      ]
    }
  }
}
```

---

## ⚡ Configuration Avancée

### MCP Servers

```json
{
  "mcp": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/home/glecomte"]
    },
    "git": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-git",
        "--repository",
        "/home/glecomte"
      ]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {
        "CONTEXT7_API_KEY": "$CONTEXT7_API_KEY"
      }
    }
  }
}
```

### Monitoring et Logging

```json
{
  "advanced_features": {
    "monitoring": {
      "performance_tracking": true,
      "cost_monitoring": true,
      "quality_metrics": true
    },
    "logging": {
      "level": "INFO", // DEBUG, INFO, WARN, ERROR
      "structured_logging": true,
      "performance_logging": true
    }
  }
}
```

---

## 🎯 Personnalisation par Projet

### Configuration Projet Spécifique

Créez `opencode.json` à la racine de votre projet :

```json
{
  "$extends": "~/.config/opencode/opencode.json",
  "model": "grok-code-fast-1", // Override pour ce projet
  "orchestrator_config": {
    "dispatch_modes": {
      "my_custom_mode": {
        "mode": "PARALLEL",
        "agents": ["my-specialist"],
        "model_strategy": "fast_model_priority"
      }
    }
  }
}
```

### Variables d'Environnement

Créez `.env` pour les variables sensibles :

```bash
# API Keys
CONTEXT7_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Configuration
OPENCODE_LOG_LEVEL=INFO
OPENCODE_CACHE_ENABLED=true
OPENCODE_PERFORMANCE_MONITORING=true

# E-commerce spécifiques
ECOMMERCE_ENVIRONMENT=development  # development, staging, production
ECOMMERCE_SECURITY_LEVEL=high      # low, medium, high
```

---

## 🔧 Scripts de Configuration

### Synchronisation Personnalisée

Créez `scripts/custom-sync.sh` :

```bash
#!/bin/bash
# Synchronisation personnalisée

# Copier uniquement certains agents
cp agents/specialists/ecommerce-*.md ~/.opencode/agent/

# Appliquer une configuration spécifique
cp config/ecommerce-only.json ~/.config/opencode/opencode.json

# Valider
./scripts/validate-config.sh
```

### Configuration Multi-Environnement

```bash
# Développement
./scripts/configure.sh --env development

# Staging
./scripts/configure.sh --env staging

# Production
./scripts/configure.sh --env production
```

---

## 📊 Monitoring et Métriques

### Métriques de Performance

```json
{
  "quality_assurance": {
    "confidence_scoring": {
      "high_confidence": 0.8,
      "medium_confidence": 0.6,
      "low_confidence": 0.4
    },
    "metrics": {
      "response_time_target": 5000, // ms
      "success_rate_target": 0.95, // 95%
      "cost_efficiency_target": 0.85 // 85%
    }
  }
}
```

### Alertes et Notifications

```json
{
  "alerts": {
    "performance_threshold": 10000, // ms
    "error_rate_threshold": 0.05, // 5%
    "cost_threshold": 100, // USD/month
    "notifications": {
      "email": "admin@example.com",
      "slack": "#opencode-alerts"
    }
  }
}
```

---

## 🚀 Optimisation Avancée

### Auto-Scaling

```json
{
  "auto_scaling": {
    "enabled": true,
    "agent_scaling": true,
    "model_scaling": true,
    "thresholds": {
      "cpu_usage": 80, // %
      "memory_usage": 85, // %
      "response_time": 10000 // ms
    }
  }
}
```

### Cache Configuration

```json
{
  "caching": {
    "agent_responses": {
      "enabled": true,
      "ttl": 3600, // 1 heure
      "max_size": "100MB"
    },
    "model_predictions": {
      "enabled": true,
      "ttl": 1800, // 30 minutes
      "algorithm": "lru"
    }
  }
}
```

---

## 🛠️ Debug et Troubleshooting

### Mode Debug

```json
{
  "debug": {
    "enabled": true,
    "verbose_logging": true,
    "performance_profiling": true,
    "agent_tracing": true
  }
}
```

### Validation de Configuration

```bash
# Validation syntaxique JSON
python3 -m json.tool config/opencode.json

# Validation des agents
./scripts/validate-config.sh

# Test de configuration
opencode config test
```

---

## 📚 Exemples de Configuration

### Configuration Minimale

```json
{
  "model": "grok-code-fast-1",
  "tools": {
    "write": true,
    "edit": true,
    "read": true
  }
}
```

### Configuration E-commerce Avancée

Voir `config/opencode.json` pour l'exemple complet.

### Configuration Développeur

```json
{
  "model": "minimax-M2",
  "debug": {
    "enabled": true,
    "verbose_logging": true
  },
  "performance_optimization": {
    "caching": {
      "enabled": false
    }
  }
}
```

---

Cette configuration avancée vous permet d'optimiser parfaitement votre environnement OpenCode selon vos besoins spécifiques. Pour plus d'aide, consultez le [Guide de Dépannage](TROUBLESHOOTING.md) ou les [Exemples d'Agents](AGENTS.md).
