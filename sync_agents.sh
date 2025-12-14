#!/bin/bash
# Script de Synchronisation des Agents OpenCode
# Copie les sub-agents vers le dossier agent/ pour que opencode les détecte

set -e

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_DIR="$BASE_DIR/agent"
SUB_AGENTS_DIR="$BASE_DIR/sub-agents"

echo "🔄 Synchronisation des agents OpenCode..."

# Créer le dossier sub-agents s'il n'existe pas
mkdir -p "$SUB_AGENTS_DIR"

# Synchroniser les sub-agents vers agent/
if [ -d "$SUB_AGENTS_DIR" ]; then
    echo "📁 Synchronisation des sub-agents..."
    for sub_agent in "$SUB_AGENTS_DIR"/*.md; do
        if [ -f "$sub_agent" ]; then
            filename=$(basename "$sub_agent")
            dest_file="$AGENT_DIR/$filename"
            cp "$sub_agent" "$dest_file"
            echo "✅ Copié: $filename"
        fi
    done
else
    echo "⚠️ Dossier sub-agents non trouvé"
fi

# Vérifier les agents primaires
echo ""
echo "🤖 Vérification des agents primaires:"
primary_agents=("orchestrator.md" "plan.md" "build.md")

for primary in "${primary_agents[@]}"; do
    if [ -f "$AGENT_DIR/$primary" ]; then
        echo "✅ $primary"
    else
        echo "❌ Manquant: $primary"
    fi
done

echo ""
echo "🎯 Synchronisation terminée!"
echo ""
echo "📋 Structure finale des agents:"
echo "🤖 Agents Primaires:"
for primary in "${primary_agents[@]}"; do
    if [ -f "$AGENT_DIR/$primary" ]; then
        echo "   • ${primary%.md}"
    fi
done

echo ""
echo "🔧 Sub-Agents:"
for sub_agent in "$AGENT_DIR"/*.md; do
    if [ -f "$sub_agent" ]; then
        filename=$(basename "$sub_agent")
        # Ne pas afficher les agents primaires
        if [[ ! " ${primary_agents[*]} " =~ " $filename " ]]; then
            echo "   • ${filename%.md}"
        fi
    fi
done

echo ""
echo "🚀 OpenCode peut maintenant détecter tous les agents!"