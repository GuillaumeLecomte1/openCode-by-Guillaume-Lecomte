# Configuration OpenCode avec Orchestrateur - Guide de Migration

## 🎯 Nouvelle Structure

### Architecture des Agents

```
openCode-by-Guillaume-Lecomte/
├── agent/                          # 🤖 Agents Primaires (OpenCode les détecte)
│   ├── orchestrator.md             # Orchestrateur principal multi-agents
│   ├── plan.md                     # Agent de planification
│   └── build.md                    # Agent de construction
├── sub-agents/                     # 🔧 Sub-Agents (synchronisés vers agent/)
│   ├── frontend-react-specialist.md
│   ├── backend-nodejs-specialist.md
│   ├── mongodb-specialist.md
│   ├── ecommerce-business-logic.md
│   ├── devops-deployment-specialist.md
│   ├── security-specialist.md
│   ├── performance-engineer.md
│   ├── system-architect.md
│   └── ... (autres agents)
├── config/                         # ⚙️ Configurations JSON
├── sync_agents.sh                  # 🔄 Script de synchronisation
├── install-opencode.sh             # 🚀 Installation mise à jour
└── autonomous_orchestrator.py      # 🐍 Orchestrateur Python autonome
```

## 🤖 Agents Primaires

### 1. **Orchestrateur** (`/orchestrator`)

- **Rôle** : Orchestration intelligente multi-agents
- **Usage** : ` /orchestrator Analyser et orchestrer une marketplace e-commerce complète`
- **Fonctionnalités** :
  - Classification automatique du projet
  - Sélection intelligente d'agents
  - Planification de dispatch (SEQUENTIAL/PARALLEL/HYBRID)
  - Exécution coordonnée
  - Rapport complet avec métriques

### 2. **Plan** (`/plan`)

- **Rôle** : Planification stratégique et architecture
- **Usage** : ` /plan Analyser les besoins pour une marketplace e-commerce`
- **Fonctionnalités** :
  - Analyse de besoins
  - Architecture système
  - Planification de projet
  - Modélisation de données

### 3. **Build** (`/build`)

- **Rôle** : Construction et déploiement
- **Usage** : ` /build Construire et déployer la marketplace e-commerce`
- **Fonctionnalités** :
  - Build automatisé
  - Déploiement CI/CD
  - Tests automatisés
  - Monitoring

## 🔧 Sub-Agents

Tous les autres agents sont maintenant des sub-agents disponibles via l'orchestrateur ou directement :

- `/frontend-react-specialist` - Développement React/TypeScript
- `/backend-nodejs-specialist` - Développement Node.js/Express
- `/mongodb-specialist` - Base de données MongoDB
- `/ecommerce-business-logic` - Logique métier e-commerce
- `/devops-deployment-specialist` - Infrastructure et déploiement
- `/security-specialist` - Audit et sécurité
- `/performance-engineer` - Optimisation performances
- `/system-architect` - Architecture logicielle
- Et plus...

## 🚀 Installation sur Nouvel Ordinateur

```bash
# 1. Cloner le repository
git clone <votre-repo>
cd openCode-by-Guillaume-Lecomte

# 2. Installation complète (inclut synchronisation des agents)
./install-opencode.sh

# 3. Redémarrer OpenCode

# 4. Utiliser l'orchestrateur
opencode
> /orchestrator
> Créer une marketplace e-commerce avec React, Node.js et MongoDB
```

## 🔄 Synchronisation Automatique

Le script `install-opencode.sh` exécute automatiquement `sync_agents.sh` qui :

1. Copie tous les sub-agents vers le dossier `agent/`
2. Vérifie que les agents primaires sont présents
3. S'assure qu'OpenCode peut détecter tous les agents

## 🧪 Test de la Configuration

```bash
# Tester la nouvelle configuration
./test_new_config.sh
```

Ce test vérifie :

- ✅ Structure des dossiers
- ✅ Agents primaires (3)
- ✅ Sub-agents (12+)
- ✅ Synchronisation
- ✅ Configurations JSON
- ✅ Orchestrateur Python

## 💡 Utilisation Recommandée

### Pour Projets E-commerce Complets

```bash
# Utiliser l'orchestrateur pour orchestration automatique
/ orchestrator
> Je veux créer une marketplace e-commerce complète avec React frontend,
> Node.js backend, MongoDB database, paiement Stripe et gestion des stocks
```

### Pour Tâches Spécifiques

```bash
# Utiliser directement les sub-agents
/backend-nodejs-specialist
> Créer l'API REST pour la gestion des produits

/frontend-react-specialist
> Créer les composants React pour la page produit

/mongodb-specialist
> Optimiser les requêtes pour les filtres produits
```

## 🎯 Avantages de cette Configuration

1. **Orchestrateur Central** : Coordination intelligente de tous les agents
2. **Configuration Centralisée** : Un seul repository pour tous vos ordinateurs
3. **Synchronisation Automatique** : Installation simple et cohérente
4. **Agents Primaires Clairs** : Seuls 3 agents principaux visibles
5. **Sub-Agents Disponibles** : Tous les agents spécialisés accessibles
6. **Test Automatique** : Validation complète de la configuration

## 🔧 Maintenance

Pour mettre à jour la configuration :

```bash
git pull origin main
./install-opencode.sh
```

Pour resynchroniser les agents uniquement :

```bash
./sync_agents.sh
```

---

**Configuration créée par Guillaume Lecomte**  
_Optimisée pour le développement e-commerce avec orchestration multi-agents_
