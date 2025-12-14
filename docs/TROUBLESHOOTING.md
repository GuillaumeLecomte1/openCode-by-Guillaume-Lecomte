# Guide de Dépannage OpenCode v3.0

🔧 **Solutions aux problèmes courants et optimisation**

Ce guide vous aide à résoudre les problèmes les plus fréquents et à optimiser votre environnement OpenCode pour le développement e-commerce.

---

## 🚨 Problèmes d'Installation

### OpenCode non installé ou non détecté

#### Symptômes

- `opencode: command not found`
- Version non reconnue
- Erreur lors de l'installation

#### Solutions

```bash
# 1. Vérifier l'installation
which opencode
opencode --version

# 2. Réinstaller OpenCode
curl -fsSL https://opencode.ai/install | bash

# 3. Redémarrer le terminal
source ~/.bashrc  # ou ~/.zshrc

# 4. Vérifier le PATH
echo $PATH | grep opencode
```

#### Prévention

```bash
# Ajouter au ~/.bashrc ou ~/.zshrc
export PATH="$PATH:/usr/local/bin"
```

### Agents non visibles dans l'interface

#### Symptômes

- `/orchestrator` non reconnu
- Agents spécialisés manquants
- Interface vide

#### Solutions

```bash
# 1. Synchroniser les agents
./scripts/sync-agents.sh

# 2. Vérifier les permissions
ls -la ~/.opencode/agent/
chmod 644 ~/.opencode/agent/*.md

# 3. Redémarrer OpenCode
# Fermer et rouvrir OpenCode

# 4. Valider la configuration
./scripts/validate-config.sh
```

#### Vérification

```bash
# Compter les agents
ls ~/.opencode/agent/*.md | wc -l

# Vérifier les agents critiques
ls ~/.opencode/agent/orchestrator.md
ls ~/.opencode/agent/backend-nodejs-specialist.md
ls ~/.opencode/agent/frontend-react-specialist.md
```

---

## ⚙️ Problèmes de Configuration

### Configuration JSON invalide

#### Symptômes

- Erreur de syntaxe JSON
- Configuration non appliquée
- OpenCode ne démarre pas

#### Solutions

```bash
# 1. Valider la syntaxe JSON
python3 -m json.tool ~/.config/opencode/opencode.json

# 2. Restaurer la configuration par défaut
cp config/opencode.json ~/.config/opencode/opencode.json

# 3. Vérifier les permissions
chmod 644 ~/.config/opencode/opencode.json

# 4. Valider avec le script
./scripts/validate-config.sh
```

#### Erreurs courantes

```json
// Erreur : virgule manquante
{
  "model": "minimax-M2"
  "small_model": "grok-code-fast-1"  // <- virgule manquante
}

// Correction
{
  "model": "minimax-M2",
  "small_model": "grok-code-fast-1"
}
```

### Modèles non reconnus

#### Symptômes

- `Model 'minimax-M2' not found`
- Fallback sur un autre modèle
- Erreurs de routing

#### Solutions

```bash
# 1. Vérifier la disponibilité des modèles
opencode models list

# 2. Modifier la configuration
# Éditer ~/.config/opencode/opencode.json
{
  "model": "gpt-4",  // Fallback si minimax-M2 indisponible
  "small_model": "gpt-3.5-turbo"
}

# 3. Tester la configuration
opencode config test
```

---

## 🤖 Problèmes des Agents

### Orchestrateur ne répond pas

#### Symptômes

- `/orchestrator` timeout
- Erreurs de dispatch
- Coordination défaillante

#### Solutions

```bash
# 1. Vérifier l'orchestrateur
cat ~/.opencode/agent/orchestrator.md | head -20

# 2. Tester en mode simple
/orchestrator
"Test simple"

# 3. Vérifier les logs (si disponibles)
# Mode debug dans opencode.json
{
  "debug": {
    "enabled": true,
    "verbose_logging": true
  }
}

# 4. Redémarrer OpenCode
```

#### Debug Avancé

```bash
# Activer le mode debug
echo '{"debug": true}' > ~/.opencode/debug.json

# Tester l'orchestration step by step
/orchestrator plan
/orchestrator build
/orchestrator test
```

### Agents spécialisés dysfonctionnels

#### Symptômes

- `/backend-nodejs-specialist` ne fonctionne pas
- Réponses incohérentes
- Capacités limitées

#### Solutions

```bash
# 1. Vérifier l'agent spécifique
cat ~/.opencode/agent/backend-nodejs-specialist.md | grep -A 5 "Configuration"

# 2. Synchroniser les agents mis à jour
./scripts/sync-agents.sh

# 3. Tester individuellement
/backend-nodejs-specialist
"Créer un endpoint simple /api/health"

# 4. Valider le format
./scripts/validate-config.sh --agent backend-nodejs-specialist
```

### Agents e-commerce manquants

#### Solutions Rapides

```bash
# 1. Copier manuellement les agents
cp agents/specialists/*.md ~/.opencode/agent/

# 2. Vérifier les agents critiques
for agent in backend-nodejs frontend-react mongodb ecommerce-business devops security; do
  if [ ! -f ~/.opencode/agent/${agent}-specialist.md ]; then
    echo "Missing: ${agent}-specialist"
    cp agents/specialists/${agent}-specialist.md ~/.opencode/agent/
  fi
done

# 3. Créer les liens symboliques
cd ~/.opencode/agent
ln -sf orchestrator.md primary-orchestrator.md
```

---

## 🏪 Problèmes E-commerce Spécifiques

### Dispatch modes ne fonctionnent pas

#### Symptômes

- SEQUENTIAL/PARALLEL/HYBRID ignorés
- Agents exécutés séquentiellement
- Performance dégradée

#### Solutions

```bash
# 1. Vérifier la configuration dispatch
grep -A 10 "dispatch_modes" ~/.config/opencode/opencode.json

# 2. Tester un mode spécifique
/orchestrator
"Mode test: backend development en parallèle"

# 3. Valider l'orchestrateur
python3 -c "
import json
with open('~/.config/opencode/opencode.json') as f:
    config = json.load(f)
    print('Dispatch modes:', list(config.get('orchestrator_config', {}).get('dispatch_modes', {}).keys()))
"
```

### Routing modèle défaillant

#### Symptômes

- Toujours minimax-M2 utilisé
- grok-code-fast-1 jamais sélectionné
- Coûts élevés

#### Solutions

```bash
# 1. Vérifier les seuils
grep -A 5 "execution_thresholds" ~/.config/opencode/opencode.json

# 2. Ajuster les seuils pour forcer le routing
{
  "performance_optimization": {
    "execution_thresholds": {
      "fast_task_threshold": 10,      // Réduire pour plus de fast tasks
      "complex_task_threshold": 60    // Réduire pour plus de complex tasks
    }
  }
}

# 3. Tester avec différentes complexités
/orchestrator
"Tâche simple: créer un README"           # -> grok-code-fast-1
"Tâche complexe: architecture système"    # -> minimax-M2
```

---

## 🔧 Problèmes Techniques

### Permissions insuffisantes

#### Symptômes

- `Permission denied`
- Fichiers non lisibles
- Installation échoue

#### Solutions

```bash
# 1. Corriger les permissions
sudo chown -R $USER:$USER ~/.opencode/
sudo chown -R $USER:$USER ~/.config/opencode/

# 2. Permissions standard
chmod 755 ~/.opencode/
chmod 644 ~/.opencode/agent/*.md
chmod 644 ~/.config/opencode/opencode.json

# 3. Ownership des dossiers
mkdir -p ~/.opencode/agent
mkdir -p ~/.config/opencode
chown -R $USER:$USER ~/.opencode ~/.config
```

### Espace disque insuffisant

#### Symptômes

- Installation incomplète
- Agents manquants
- Erreurs de copie

#### Solutions

```bash
# 1. Vérifier l'espace disponible
df -h ~/.opencode ~/.config

# 2. Nettoyer si nécessaire
rm -rf ~/.opencode-backup-*
rm -rf ~/.opencode/cache/*

# 3. Optimiser les agents
# Supprimer les agents inutilisés
rm ~/.opencode/agent/tech-stack-researcher.md  # Si non utilisé
```

### Connexion réseau

#### Symptômes

- MCP servers échouent
- API calls timeout
- Installation MCP échoue

#### Solutions

```bash
# 1. Tester la connectivité
curl -I https://opencode.ai
curl -I https://registry.npmjs.org

# 2. Installer MCP manuellement
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-git

# 3. Configuration proxy (si nécessaire)
npm config set proxy http://proxy:port
npm config set https-proxy http://proxy:port
```

---

## 📊 Problèmes de Performance

### Réponses lentes

#### Symptômes

- Timeout agents (> 30s)
- OpenCode figé
- Performance dégradée

#### Solutions

```bash
# 1. Vérifier les ressources système
top
htop
free -h

# 2. Optimiser la configuration
{
  "performance_optimization": {
    "execution_thresholds": {
      "fast_task_threshold": 15,
      "complex_task_threshold": 90
    },
    "caching": {
      "agent_responses": false  // Désactiver si problème mémoire
    }
  }
}

# 3. Redémarrer OpenCode
killall opencode
opencode &
```

### Consommation mémoire élevée

#### Solutions

```bash
# 1. Surveiller la mémoire
ps aux | grep opencode
free -h

# 2. Optimiser le cache
{
  "caching": {
    "agent_responses": {
      "enabled": true,
      "ttl": 1800,  // Réduire à 30min
      "max_size": "50MB"  // Réduire la taille
    }
  }
}

# 3. Nettoyer le cache
rm -rf ~/.opencode/cache/*
```

---

## 🔍 Debug et Logs

### Activation du mode debug

```json
// ~/.config/opencode/opencode.json
{
  "debug": {
    "enabled": true,
    "verbose_logging": true,
    "performance_profiling": true,
    "agent_tracing": true
  },
  "logging": {
    "level": "DEBUG",
    "structured_logging": true,
    "performance_logging": true
  }
}
```

### Collecte d'informations pour le support

```bash
# 1. Informations système
uname -a
node --version
python3 --version

# 2. Configuration OpenCode
opencode --version
opencode config show

# 3. Logs et debug
./scripts/validate-config.sh > debug-report.txt 2>&1

# 4. Statut des agents
ls -la ~/.opencode/agent/ > agents-status.txt

# 5. Configuration complète
cat ~/.config/opencode/opencode.json > current-config.json
```

### Script de diagnostic automatique

```bash
#!/bin/bash
# diagnostic.sh - Script de diagnostic complet

echo "=== DIAGNOSTIC OPENCODE v3.0 ==="
echo "Date: $(date)"
echo ""

echo "1. SYSTEM INFO:"
echo "OS: $(uname -a)"
echo "Node: $(node --version 2>/dev/null || echo 'Not installed')"
echo "Python: $(python3 --version 2>/dev/null || echo 'Not installed')"
echo ""

echo "2. OPENCODE STATUS:"
which opencode && opencode --version || echo "OpenCode not found"
echo ""

echo "3. CONFIGURATION:"
ls -la ~/.config/opencode/ 2>/dev/null || echo "Config dir missing"
python3 -m json.tool ~/.config/opencode/opencode.json > /dev/null 2>&1 && echo "JSON valid" || echo "JSON invalid"
echo ""

echo "4. AGENTS:"
agent_count=$(ls ~/.opencode/agent/*.md 2>/dev/null | wc -l)
echo "Total agents: $agent_count"
echo "Critical agents:"
for agent in orchestrator plan build backend-nodejs frontend-react; do
  if [ -f ~/.opencode/agent/${agent}*.md ]; then
    echo "  ✓ $agent"
  else
    echo "  ✗ $agent"
  fi
done
echo ""

echo "5. ORCHESTRATOR:"
if [ -d ~/.opencode/orchestrator ]; then
  echo "  ✓ Orchestrator directory exists"
  ls ~/.opencode/orchestrator/ | head -5
else
  echo "  ✗ Orchestrator directory missing"
fi
echo ""

echo "6. PERMISSIONS:"
ls -la ~/.opencode/agent/ | head -3
echo ""

echo "7. VALIDATION:"
./scripts/validate-config.sh 2>&1 | tail -10
```

---

## 🛠️ Solutions Rapides

### Reset Complet

```bash
# Backup et reset complet
./scripts/update.sh --backup
rm -rf ~/.opencode/ ~/.config/opencode/
./scripts/install.sh
```

### Mise à jour de dépannage

```bash
# Mise à jour forcée depuis le repository
git pull origin main
./scripts/sync-agents.sh
./scripts/validate-config.sh
```

### Test minimal

```bash
# Test avec configuration minimale
cat > ~/.config/opencode/opencode.json << 'EOF'
{
  "model": "grok-code-fast-1",
  "tools": {
    "write": true,
    "edit": true,
    "read": true
  }
}
EOF

# Tester OpenCode
opencode
# /orchestrator "Test simple"
```

---

## 📞 Support et Communauté

### Ressources d'Aide

1. **Documentation OpenCode** : https://opencode.ai/docs
2. **Repository GitHub** : https://github.com/GuillaumeLecomte1/openCode-by-Guillaume-Lecomte
3. **Issues GitHub** : https://github.com/GuillaumeLecomte1/openCode-by-Guillaume-Lecomte/issues

### Comment Signaler un Problème

Avant de signaler un problème, préparez :

1. **Informations système** (OS, versions)
2. **Configuration actuelle** (`opencode config show`)
3. **Logs d'erreur** complets
4. **Steps to reproduce** détaillés
5. **Comportement attendu** vs **Comportement actuel**

### Template de Rapport de Bug

```markdown
## Description

Description claire du problème

## Environnement

- OS: [ex: Ubuntu 20.04]
- OpenCode: [version]
- Node.js: [version]
- Python: [version]

## Étapes pour Reproduire

1. Étape 1
2. Étape 2
3. Erreur se produit

## Comportement Attendu

Ce qui devrait se passer

## Comportement Actuel

Ce qui se passe réellement

## Logs/Console Output
```

[Coller les logs pertinents]

```

## Configuration
[Coller ~/.config/opencode/opencode.json]
```

---

## 🎯 Optimisation Continue

### Métriques à Surveiller

```bash
# Performance des agents
time /orchestrator "Test performance"

# Taux de succès
grep "SUCCESS\|ERROR" ~/.opencode/logs/*.log | wc -l

# Utilisation des modèles
grep "minimax-M2\|grok-code-fast" ~/.opencode/logs/*.log | sort | uniq -c
```

### Optimisations Recommandées

1. **Ajuster les seuils** selon vos patterns d'usage
2. **Activer le cache** pour les tâches répétitives
3. **Désactiver les agents** non utilisés
4. **Mettre à jour régulièrement** depuis le repository

### Automatisation

```bash
# Cron job pour maintenance hebdomadaire
0 2 * * 0 /path/to/scripts/update.sh --quiet

# Monitoring quotidien
0 9 * * * /path/to/scripts/validate-config.sh --quiet
```

---

Ce guide de dépannage devrait vous aider à résoudre la plupart des problèmes courants. Pour des problèmes spécifiques non couverts ici, consultez la communauté GitHub ou créez une nouvelle issue avec les informations de diagnostic.
