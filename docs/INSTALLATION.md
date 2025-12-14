# Guide d'Installation OpenCode v3.0

🚀 **Configuration optimisée pour E-commerce avec Orchestrateur Multi-Dispatch**

Ce guide vous accompagne dans l'installation complète de votre environnement OpenCode optimisé pour le développement e-commerce.

---

## 📋 Prérequis

### 1. OpenCode Core

Installez OpenCode d'abord :

```bash
curl -fsSL https://opencode.ai/install | bash
```

Vérifiez l'installation :

```bash
opencode --version
```

### 2. Dépendances Système

Assurez-vous d'avoir les outils suivants installés :

- **Node.js** (version 16+) - Pour les MCP servers
- **Python 3.8+** - Pour les scripts de validation
- **Git** - Pour la gestion des mises à jour

```bash
# Vérification
node --version
python3 --version
git --version
```

---

## 🚀 Installation Rapide

### 1. Cloner le Repository

```bash
git clone https://github.com/GuillaumeLecomte1/openCode-by-Guillaume-Lecomte.git
cd openCode-by-Guillaume-Lecomte
```

### 2. Installation Automatique

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

L'installation automatique va :

✅ **Créer la structure de dossiers**  
✅ **Installer la configuration globale**  
✅ **Copier tous les agents**  
✅ **Installer l'orchestrateur multi-dispatch**  
✅ **Configurer les commandes**  
✅ **Installer les MCP servers**  
✅ **Valider l'installation**

### 3. Configuration des Variables d'Environnement

Créez votre fichier `.env` :

```bash
cp .env.example .env
```

Éditez `.env` et ajoutez vos clés API :

```bash
# Context7 (optionnel mais recommandé)
CONTEXT7_API_KEY=your_context7_api_key_here

# OpenAI (si utilisé)
OPENAI_API_KEY=your_openai_api_key_here

# Autres clés selon vos besoins
```

---

## 🔧 Installation Manuelle (Avancée)

Si vous préférez une installation manuelle ou personnalisée :

### 1. Configuration Globale

```bash
# Copier la configuration
mkdir -p ~/.config/opencode
cp config/opencode.json ~/.config/opencode/opencode.json
```

### 2. Installation des Agents

```bash
# Créer le dossier agents
mkdir -p ~/.opencode/agent

# Copier les agents principaux
cp agents/orchestrator.md ~/.opencode/agent/
cp agents/plan.md ~/.opencode/agent/
cp agents/build.md ~/.opencode/agent/

# Copier les agents spécialisés
cp agents/specialists/*.md ~/.opencode/agent/

# Créer le lien symbolique pour l'orchestrateur
cd ~/.opencode/agent
ln -sf orchestrator.md primary-orchestrator.md
```

### 3. Installation de l'Orchestrateur

```bash
mkdir -p ~/.opencode/orchestrator
cp -r opencode-orchestrator/* ~/.opencode/orchestrator/
cp ecommerce_model_router.py ~/.opencode/orchestrator/
```

### 4. Installation des Commandes

```bash
mkdir -p ~/.opencode/command
cp commands/*.md ~/.opencode/command/
```

---

## 🎯 Configuration Spécifique E-commerce

### Modèles Configurés

La configuration active automatiquement :

- **minimax-M2** : Analyses complexes, architecture, orchestration
- **grok-code-fast-1** : Tâches simples, documentation, optimisations basiques

### Agents Spécialisés Disponibles

#### 🏪 E-commerce Core

- **backend-nodejs-specialist** : API Node.js/Express
- **frontend-react-specialist** : React/TypeScript
- **mongodb-specialist** : Base de données MongoDB
- **ecommerce-business-logic** : Logique métier e-commerce

#### 🔒 Infrastructure

- **security-specialist** : Audit et sécurité
- **devops-deployment-specialist** : Déploiement et DevOps

#### 🏗️ Architecture & Qualité

- **system-architect** : Architecture système
- **performance-engineer** : Optimisation performances
- **code-reviewer** : Revue de code

### Dispatch Modes Optimisés

| Phase             | Mode       | Agents                      | Durée Estimée |
| ----------------- | ---------- | --------------------------- | ------------- |
| **Planification** | SEQUENTIAL | system-architect, plan      | 30-60 min     |
| **Backend**       | PARALLEL   | backend, mongodb, security  | 2-3h          |
| **Frontend**      | PARALLEL   | frontend, business-logic    | 2-3h          |
| **Intégration**   | HYBRID     | frontend, backend, security | 1-2h          |
| **Déploiement**   | SEQUENTIAL | devops, security            | 30-60 min     |

---

## ✅ Validation de l'Installation

### 1. Validation Automatique

```bash
./scripts/validate-config.sh
```

### 2. Test Manuel

```bash
# Test de l'orchestrateur
opencode

# Dans l'interface OpenCode
/orchestrator
```

### 3. Test des Agents Spécialisés

```bash
# Test backend
/backend-nodejs-specialist
"Créer une API REST pour un système de gestion de produits"

# Test frontend
/frontend-react-specialist
"Créer une interface de panier d'achat en React"

# Test base de données
/mongodb-specialist
"Optimiser les requêtes pour un catalogue de produits"
```

---

## 🔄 Mise à Jour

### Mise à Jour Simple

Après avoir fait des modifications dans le repository :

```bash
./scripts/update.sh
```

### Mise à Jour Complète

```bash
# Synchroniser depuis le repository
./scripts/sync-agents.sh

# Valider la configuration
./scripts/validate-config.sh
```

### Réinstallation Complète

```bash
# Réinstaller depuis zéro
./scripts/install.sh
```

---

## 🛠️ Personnalisation

### Ajouter de Nouveaux Agents

1. **Créer l'agent** dans `agents/specialists/`
2. **Ajouter les métadonnées** dans `config/agents.json`
3. **Synchroniser** : `./scripts/sync-agents.sh`
4. **Valider** : `./scripts/validate-config.sh`

### Modifier la Configuration

1. **Éditer** `config/opencode.json`
2. **Tester** : `./scripts/validate-config.sh`
3. **Appliquer** : `./scripts/update.sh`

### Personnaliser les Dispatch Modes

Modifiez les dispatch modes dans `config/opencode.json` section `orchestrator_config.dispatch_modes`.

---

## 🚨 Dépannage

### Problèmes Courants

#### OpenCode non détecté

```bash
# Vérifier l'installation
which opencode
opencode --version

# Réinstaller si nécessaire
curl -fsSL https://opencode.ai/install | bash
```

#### Agents non visibles

```bash
# Synchroniser les agents
./scripts/sync-agents.sh

# Vérifier les permissions
ls -la ~/.opencode/agent/
```

#### Configuration invalide

```bash
# Valider la configuration
./scripts/validate-config.sh

# Restaurer la configuration par défaut
cp config/opencode.json ~/.config/opencode/opencode.json
```

#### Erreurs de permissions

```bash
# Corriger les permissions
chmod -R 755 ~/.opencode/
chmod 644 ~/.opencode/agent/*.md
```

### Logs et Debug

#### Activer le mode verbose

```bash
# Dans OpenCode
/settings
Enable verbose logging
```

#### Vérifier les logs système

```bash
# Logs OpenCode (si disponibles)
tail -f ~/.local/share/opencode/logs/*.log

# Vérifier les erreurs bash
bash -x scripts/install.sh
```

---

## 📞 Support

### Ressources

- **Documentation OpenCode** : https://opencode.ai/docs
- **Repository GitHub** : https://github.com/GuillaumeLecomte1/openCode-by-Guillaume-Lecomte
- **Issues GitHub** : https://github.com/GuillaumeLecomte1/openCode-by-Guillaume-Lecomte/issues

### Communauté

- **GitHub Discussions** : Pour les questions générales
- **GitHub Issues** : Pour les bugs et problèmes
- **Pull Requests** : Pour les contributions

---

## 📈 Métriques et Optimisation

### Performances Attendues

- **Temps de réponse** : < 5 secondes
- **Taux de succès** : 95%+
- **Économies de coûts** : 65% (grâce au routing automatique)

### Monitoring

Surveillez les métriques via :

```bash
# Vérifier la santé du système
./scripts/validate-config.sh

# Statistiques d'agents
ls -la ~/.opencode/agent/ | wc -l
```

---

## 🎉 Félicitations !

Votre environnement OpenCode est maintenant configuré pour le développement e-commerce optimisé !

### Prochaines Étapes

1. **Testez l'orchestrateur** : `/orchestrator "votre projet e-commerce"`
2. **Explorez les agents spécialisés** pour vos besoins spécifiques
3. **Personnalisez la configuration** selon vos préférences
4. **Contribuez** au projet via GitHub

🚀 **Bonne开发 avec votre nouvel environnement e-commerce optimisé !**
