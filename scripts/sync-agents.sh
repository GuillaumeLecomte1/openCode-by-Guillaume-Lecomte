#!/bin/bash

# OpenCode Agent Synchronizer - v3.0
# by Guillaume Lecomte - Sync agents from repository to OpenCode
# Maintains consistent agent state across development and runtime

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
SOURCE_AGENTS="$REPO_DIR/agents"
SOURCE_SPECIALISTS="$REPO_DIR/agents/specialists"
TARGET_AGENTS="$HOME/.opencode/agent"

# Agent categories for better organization
declare -A AGENT_CATEGORIES
AGENT_CATEGORIES["orchestrator"]="Core"
AGENT_CATEGORIES["plan"]="Core" 
AGENT_CATEGORIES["build"]="Core"
AGENT_CATEGORIES["backend-nodejs-specialist"]="E-commerce"
AGENT_CATEGORIES["frontend-react-specialist"]="E-commerce"
AGENT_CATEGORIES["mongodb-specialist"]="E-commerce"
AGENT_CATEGORIES["ecommerce-business-logic"]="E-commerce"
AGENT_CATEGORIES["devops-deployment-specialist"]="E-commerce"
AGENT_CATEGORIES["security-specialist"]="E-commerce"
AGENT_CATEGORIES["angular-architect"]="Architecture"
AGENT_CATEGORIES["system-architect"]="Architecture"
AGENT_CATEGORIES["code-reviewer"]="Quality"
AGENT_CATEGORIES["performance-engineer"]="Quality"
AGENT_CATEGORIES["refactoring-specialist"]="Quality"
AGENT_CATEGORIES["tech-stack-researcher"]="Research"

echo "=========================================="
echo "🔄 OpenCode Agent Synchronizer v3.0"
echo "   Repository → OpenCode Runtime Sync"
echo "=========================================="
echo ""

# Create target directory if it doesn't exist
ensure_target_directory() {
    print_status "Ensuring target directory exists..."
    mkdir -p "$TARGET_AGENTS"
    print_success "Target directory ready: $TARGET_AGENTS"
}

# Sync main agents
sync_main_agents() {
    print_status "Syncing main agents..."
    
    local synced_count=0
    local main_agents=("orchestrator.md" "plan.md" "build.md")
    
    for agent in "${main_agents[@]}"; do
        local source_file="$SOURCE_AGENTS/$agent"
        if [ -f "$source_file" ]; then
            cp "$source_file" "$TARGET_AGENTS/"
            agent_name="${agent%.md}"
            print_success "Synced main agent: $agent_name"
            ((synced_count++))
        else
            print_warning "Main agent not found: $agent"
        fi
    done
    
    print_status "Main agents synced: $synced_count"
    return $synced_count
}

# Sync specialized agents
sync_specialized_agents() {
    print_status "Syncing specialized agents..."
    
    local synced_count=0
    
    for agent_file in "$SOURCE_SPECIALISTS"/*.md; do
        if [ -f "$agent_file" ]; then
            agent_name=$(basename "$agent_file" .md)
            cp "$agent_file" "$TARGET_AGENTS/"
            category="${AGENT_CATEGORIES[$agent_name]:-Other}"
            print_success "Synced $category agent: $agent_name"
            ((synced_count++))
        fi
    done
    
    print_status "Specialized agents synced: $synced_count"
    return $synced_count
}

# Create primary orchestrator symlink
create_orchestrator_symlink() {
    print_status "Creating orchestrator symlinks..."
    
    # Primary orchestrator symlink
    if [ -f "$TARGET_AGENTS/orchestrator.md" ]; then
        cd "$TARGET_AGENTS"
        if [ ! -L "primary-orchestrator.md" ]; then
            ln -sf orchestrator.md primary-orchestrator.md
            print_success "Created primary-orchestrator symlink"
        else
            print_success "Primary-orchestrator symlink already exists"
        fi
    fi
}

# Validate agent format
validate_agent_format() {
    print_status "Validating agent format..."
    
    local errors=0
    local warnings=0
    
    for agent_file in "$TARGET_AGENTS"/*.md; do
        if [ -f "$agent_file" ]; then
            agent_name=$(basename "$agent_file" .md)
            
            # Check for required sections
            if ! grep -q "^#" "$agent_file"; then
                print_error "$agent_name: Missing title"
                ((errors++))
                continue
            fi
            
            # Check for Configuration JSON
            if ! grep -q '"agent":' "$agent_file"; then
                print_warning "$agent_name: Missing JSON configuration"
                ((warnings++))
            fi
            
            # Check for proper ending
            if ! grep -q "^---" "$agent_file" | tail -1; then
                print_warning "$agent_name: Missing proper ending"
                ((warnings++))
            fi
        fi
    done
    
    if [ $errors -eq 0 ]; then
        print_success "Agent format validation passed"
        if [ $warnings -gt 0 ]; then
            print_warning "Format validation completed with $warnings warnings"
        fi
    else
        print_error "Agent format validation failed with $errors errors"
    fi
    
    return $errors
}

# Show synchronization statistics
show_sync_stats() {
    echo ""
    echo "=========================================="
    echo "📊 SYNCHRONIZATION STATISTICS"
    echo "=========================================="
    echo ""
    
    local total_agents=$(ls "$TARGET_AGENTS"/*.md 2>/dev/null | wc -l)
    print_status "Total agents synced: $total_agents"
    
    # Count by category
    declare -A category_counts
    for agent_file in "$TARGET_AGENTS"/*.md; do
        if [ -f "$agent_file" ]; then
            agent_name=$(basename "$agent_file" .md)
            category="${AGENT_CATEGORIES[$agent_name]:-Other}"
            ((category_counts[$category]++))
        fi
    done
    
    for category in "${!category_counts[@]}"; do
        count=${category_counts[$category]}
        if [ "$category" == "E-commerce" ]; then
            echo -e "${PURPLE}  🏪 $category: $count agents${NC}"
        elif [ "$category" == "Core" ]; then
            echo -e "${GREEN}  🏗️  $category: $count agents${NC}"
        elif [ "$category" == "Architecture" ]; then
            echo -e "${BLUE}  🏛️  $category: $count agents${NC}"
        elif [ "$category" == "Quality" ]; then
            echo -e "${YELLOW}  ✅ $category: $count agents${NC}"
        else
            echo -e "  🔧 $category: $count agents"
        fi
    done
    
    echo ""
    
    # E-commerce agents verification
    local ecommerce_agents=(
        "backend-nodejs-specialist"
        "frontend-react-specialist" 
        "mongodb-specialist"
        "ecommerce-business-logic"
        "devops-deployment-specialist"
        "security-specialist"
    )
    
    print_status "E-commerce agents verification:"
    for agent in "${ecommerce_agents[@]}"; do
        if [ -f "$TARGET_AGENTS/$agent.md" ]; then
            echo -e "${GREEN}  ✅ $agent${NC}"
        else
            echo -e "${RED}  ❌ $agent${NC}"
        fi
    done
}

# Clean orphaned agents
clean_orphaned_agents() {
    print_status "Checking for orphaned agents..."
    
    local repo_agents=()
    
    # Get all agents from repository
    for agent_file in "$SOURCE_AGENTS"/*.md; do
        if [ -f "$agent_file" ]; then
            repo_agents+=("$(basename "$agent_file")")
        fi
    done
    
    for agent_file in "$SOURCE_SPECIALISTS"/*.md; do
        if [ -f "$agent_file" ]; then
            repo_agents+=("$(basename "$agent_file")")
        fi
    done
    
    # Check for agents in target not in repository
    local orphaned=0
    for agent_file in "$TARGET_AGENTS"/*.md; do
        if [ -f "$agent_file" ]; then
            agent_basename=$(basename "$agent_file")
            if [[ ! " ${repo_agents[@]} " =~ " $agent_basename " ]] && [[ ! "$agent_basename" == "primary-orchestrator.md" ]]; then
                print_warning "Orphaned agent found: $agent_basename"
                ((orphaned++))
            fi
        fi
    done
    
    if [ $orphaned -eq 0 ]; then
        print_success "No orphaned agents found"
    else
        print_warning "Found $orphaned orphaned agents"
    fi
}

# Main synchronization function
main() {
    ensure_target_directory
    local total_synced=0
    
    # Sync agents
    sync_main_agents
    total_synced=$((total_synced + $?))
    
    sync_specialized_agents
    total_synced=$((total_synced + $?))
    
    # Create symlinks
    create_orchestrator_symlink
    
    # Validation and cleanup
    if validate_agent_format; then
        clean_orphaned_agents
        show_sync_stats
        
        echo ""
        print_success "🎉 Agent synchronization completed!"
        print_status "Total agents synced: $total_synced"
        echo ""
        print_status "Next steps:"
        echo "1. Restart OpenCode to load new agents"
        echo "2. Test with: opencode"
        echo "3. Use: /orchestrator 'your project'"
    else
        print_error "Agent synchronization completed with errors"
        exit 1
    fi
}

# Run main
main "$@"