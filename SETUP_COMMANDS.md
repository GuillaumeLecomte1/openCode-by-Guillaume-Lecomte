# 🚀 Commandes de Setup OpenCode

## Option 1: Setup Ultra-Rapide (Recommandé)

```bash
# Une seule commande - Clone + Setup automatique
curl -fsSL https://raw.githubusercontent.com/GuillaumeLecomte1/openCode-by-Guillaume-Lecomte/main/quick-setup.sh | bash
```

## Option 2: Setup depuis Repository Local

```bash
# 1. Cloner le repository
git clone https://github.com/GuillaumeLecomte1/openCode-by-Guillaume-Lecomte.git
cd openCode-by-Guillaume-Lecomte

# 2. Setup complet en une commande
./setup.sh
```

## Option 3: Installation Séparée

```bash
# 1. Cloner
git clone https://github.com/GuillaumeLecomte1/openCode-by-Guillaume-Lecomte.git
cd openCode-by-Guillaume-Lecomte

# 2. Installer OpenCode (si pas déjà fait)
curl -fsSL https://opencode.ai/install | bash

# 3. Setup configuration
./scripts/install.sh
```

## Commandes de Maintenance

### Mise à Jour

```bash
cd openCode-by-Guillaume-Lecomte
./scripts/update.sh
```

### Validation

```bash
cd openCode-by-Guillaume-Lecomte
./scripts/validate-config.sh
```

### Tests

```bash
cd openCode-by-Guillaume-Lecomte
./tests/agents-test.sh
./tests/integration-test.sh
```

## Vérification Rapide

```bash
# Vérifier que tout fonctionne
opencode
# Puis tester: /orchestrator "Test simple"
```

---

**💡 Recommandation**: Utilisez l'Option 1 pour un setup ultra-rapide, ou l'Option 2 pour plus de contrôle.
