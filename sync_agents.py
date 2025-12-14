#!/bin/bash
"""
Script de Synchronisation des Agents OpenCode
Copie les sub-agents vers le dossier agent/ pour que opencode les détecte
"""

import os
import shutil
from pathlib import Path

def sync_sub_agents():
    """Synchronise les sub-agents vers le dossier agent/"""
    
    base_dir = Path(__file__).parent
    agent_dir = base_dir / "agent"
    sub_agents_dir = base_dir / "sub-agents"
    
    # Créer le dossier sub-agents s'il n'existe pas
    sub_agents_dir.mkdir(exist_ok=True)
    
    print("🔄 Synchronisation des agents...")
    
    # Lister les fichiers dans sub-agents
    sub_agent_files = []
    if sub_agents_dir.exists():
        sub_agent_files = list(sub_agents_dir.glob("*.md"))
        print(f"📁 Trouvé {len(sub_agent_files)} sub-agents")
        
        # Copier chaque sub-agent vers agent/
        for sub_agent_file in sub_agent_files:
            dest_file = agent_dir / sub_agent_file.name
            try:
                shutil.copy2(sub_agent_file, dest_file)
                print(f"✅ Copié: {sub_agent_file.name}")
            except Exception as e:
                print(f"❌ Erreur copie {sub_agent_file.name}: {e}")
    else:
        print("⚠️ Dossier sub-agents non trouvé")
    
    # Vérifier que les agents primaires sont présents
    primary_agents = ["orchestrator.md", "plan.md", "build.md"]
    for primary_agent in primary_agents:
        primary_file = agent_dir / primary_agent
        if primary_file.exists():
            print(f"✅ Agent primaire présent: {primary_agent}")
        else:
            print(f"⚠️ Agent primaire manquant: {primary_agent}")
    
    print("🎯 Synchronisation terminée!")
    print("\n📋 Structure des agents:")
    print("🤖 Agents Primaires (dans agent/):")
    for primary in primary_agents:
        if (agent_dir / primary).exists():
            print(f"   • {primary.replace('.md', '')}")
    
    print("\n🔧 Sub-Agents (synchronisés vers agent/):")
    for sub_agent_file in sub_agent_files:
        print(f"   • {sub_agent_file.stem}")

if __name__ == "__main__":
    sync_sub_agents()