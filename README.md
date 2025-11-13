# OpenCode Configuration by Guillaume Lecomte

🚀 Configuration optimisée pour OpenCode avec agents, commandes et outils personnalisés.

## 📋 Description

Ce repository contient ma configuration personnelle d'OpenCode, incluant :
- Configuration globale optimisée
- Agents spécialisés (code review, performance, sécurité, etc.)
- Commandes personnalisées (test, lint, build)
- Serveurs MCP préconfigurés
- Script d'installation automatique

## 🚀 Installation Rapide

### Prérequis

1. **Installer OpenCode** :
   ```bash
   curl -fsSL https://opencode.ai/install | bash
   ```

2. **Cloner ce repository** :
   ```bash
   git clone https://github.com/votre-username/openCode-by-Guillaume-Lecomte.git
   cd openCode-by-Guillaume-Lecomte
   ```

### Installation Automatique

Lancer le script d'installation :
```bash
./install.sh
```

Le script va :
- ✅ Créer les répertoires de configuration
- ✅ Installer la configuration globale
- ✅ Configurer les agents spécialisés
- ✅ Installer les commandes personnalisées
- ✅ Configurer les serveurs MCP
- ✅ Mettre en place les variables d'environnement

### Configuration Post-Installation

1. **Redémarrer votre terminal** ou sourcer votre configuration :
   ```bash
   source ~/.bashrc  # ou ~/.zshrc
   ```

2. **Configurer vos clés API** :
   ```bash
   opencode auth login
   ```

3. **Lancer OpenCode** :
   ```bash
   opencode
   ```

## 📁 Structure du Repository

```
openCode-by-Guillaume-Lecomte/
├── README.md                    # Ce fichier
├── install.sh                   # Script d'installation
├── config/                      # Fichiers de configuration
│   ├── global.json             # Configuration globale OpenCode
│   └── project.json            # Configuration par projet
├── agents/                      # Agents spécialisés
│   ├── code-reviewer.md        # Agent de revue de code
│   ├── performance-engineer.md # Agent performance
│   ├── security-engineer.md    # Agent sécurité
│   ├── system-architect.md     # Architecte système
│   └── tech-stack-researcher.md # Chercheur tech stack
├── commands/                    # Commandes personnalisées
│   ├── test.md                 # Commande de test
│   ├── lint.md                 # Commande de linting
│   └── build.md                # Commande de build
├── tools/                       # Outils personnalisés (à venir)
├── themes/                      # Thèmes personnalisés (à venir)
├── mcp-servers/                 # Configuration MCP (à venir)
└── .opencode/                   # Configuration locale OpenCode
    ├── agent/                   # Agents locaux
    ├── command/                 # Commandes locales
    ├── tool/                    # Outils locaux
    └── plugin/                  # Plugins locaux
```

## 🤖 Agents Disponibles

### Code Reviewer
Analyse le code pour détecter :
- ⚠️ Vulnérabilités de sécurité
- 🐌 Problèmes de performance
- 📏 Violations des bonnes pratiques
- 🔧 Problèmes de maintenabilité

**Utilisation** : Demandez une revue de code après des modifications importantes.

### Performance Engineer
Optimise les performances applicatives :
- 📊 Profilage et analyse
- 🎯 Identification des goulots d'étranglement
- ⚡ Stratégies d'optimisation
- 💾 Optimisation mémoire

**Utilisation** : Pour les problèmes de lenteur ou avant mise en production.

### Security Engineer
Renforce la sécurité de vos applications :
- 🔍 Évaluation des vulnérabilités
- 🔐 Authentification et autorisation
- 🔒 Chiffrement des données
- 📋 Conformité et standards

**Utilisation** : Intégrez-le dans votre processus de développement.

### System Architect
Conçoit des architectures scalables :
- 🏗️ Design système et architecture
- 📈 Planification de la scalabilité
- 🛠️ Sélection de stack technique
- 🌐 Architecture microservices

**Utilisation** : Pour les nouveaux projets ou refontes majeures.

### Tech Stack Researcher
Recherche et recommande des technologies :
- 🔎 Évaluation comparative
- ⚖️ Analyse des trade-offs
- 📚 Veille technologique
- 🎯 Recommandations personnalisées

**Utilisation** : Avant de choisir une nouvelle technologie.

## ⚡ Commandes Personnalisées

### `/test`
Exécute la suite de tests complète avec rapport de couverture.
```bash
/test
```

### `/lint`
Lance le linting et la vérification des types.
```bash
/lint
```

### `/build`
Compile le projet et valide tous les prérequis.
```bash
/build
```

## 🔧 Configuration

### Globale (`~/.config/opencode/opencode.json`)
- Thème : `opencode`
- Modèle principal : `anthropic/claude-sonnet-4-5`
- Modèle léger : `anthropic/claude-haiku-4-5`
- Outils activés : tous
- Formatters : Prettier configuré

### Par Projet (`opencode.json`)
Pour utiliser dans un projet spécifique :
```bash
cp opencode.json.template opencode.json
```

## 🌐 Serveurs MCP

### Filesystem
Accès au système de fichiers local :
```json
{
  "filesystem": {
    "command": "npx",
    "args": ["@modelcontextprotocol/server-filesystem", "/home/glecomte"]
  }
}
```

### Git
Intégration Git avancée :
```json
{
  "git": {
    "command": "npx", 
    "args": ["@modelcontextprotocol/server-git", "--repository", "/home/glecomte"]
  }
}
```

## 🎯 Personnalisation

### Ajouter un Agent
1. Créer un fichier `.md` dans `agents/`
2. Décrire l'agent et sa configuration
3. Relancer `./install.sh`

### Ajouter une Commande
1. Créer un fichier `.md` dans `commands/`
2. Définir le template et la description
3. Relancer `./install.sh`

### Modifier la Configuration
1. Éditer `config/global.json` ou `config/project.json`
2. Relancer `./install.sh`

## 🔄 Mise à Jour

Pour mettre à jour votre configuration :
```bash
git pull origin main
./install.sh
```

## 🐛 Dépannage

### OpenCode ne trouve pas la configuration
```bash
export OPENCODE_CONFIG_DIR="/chemin/vers/openCode-by-Guillaume-Lecomte"
```

### Problèmes avec les serveurs MCP
Vérifiez que npm est installé :
```bash
npm --version
npm install -g @modelcontextprotocol/server-filesystem @modelcontextprotocol/server-git
```

### Agents non disponibles
Redémarrez votre terminal et vérifiez :
```bash
ls ~/.opencode/agent/
```

## 📚 Ressources

- [Documentation OpenCode](https://opencode.ai/docs)
- [Configuration Reference](https://opencode.ai/docs/config)
- [Agents Documentation](https://opencode.ai/docs/agents)
- [MCP Servers](https://opencode.ai/docs/mcp-servers)

## 🤝 Contribution

Contributions bienvenues ! N'hésitez pas à :
- ⭐ Forker ce repository
- 🐛 Signaler des issues
- 💡 Suggérer des améliorations
- 📝 Proposer des agents/commandes

## 📄 Licence

MIT License - faites-en ce que vous voulez !

---

**Créé avec ❤️ par Guillaume Lecomte**

*Optimisez votre développement avec OpenCode !*