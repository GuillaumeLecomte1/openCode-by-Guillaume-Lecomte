#!/bin/bash

# OpenCode Configuration Updater - v3.0
# by Guillaume Lecomte - Quick update from repository changes
# Updates OpenCode configuration from GitHub repository

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
print_ecommerce() { echo -e "${PURPLE}[E-COMMERCE]${NC} $1"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

# Check if in repo directory
if [ ! -f "$REPO_DIR/README.md" ]; then
    print_error "Please run this script from the repository root directory"
    exit 1
fi

echo "=========================================="
echo "🔄 OpenCode Configuration Updater v3.0"
echo "   Quick update from repository changes"
echo "=========================================="
echo ""

# Check git status
check_git_status() {
    print_status "Checking repository status..."
    
    if [ -d "$REPO_DIR/.git" ]; then
        cd "$REPO_DIR"
        
        # Check for uncommitted changes
        if ! git diff --quiet || ! git diff --cached --quiet; then
            print_warning "Uncommitted changes detected. Consider committing first."
            echo ""
            echo "Current changes:"
            git status --porcelain | head -10
            echo ""
            read -p "Continue anyway? (y/N): " -n 1 -r
            echo ""
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                print_status "Update cancelled"
                exit 0
            fi
        fi
        
        # Check if behind remote
        git fetch 2>/dev/null || true
        if [ $(git rev-parse HEAD) != $(git rev-parse @{u} 2>/dev/null | head -c 7) ]; then
            print_warning "Repository is behind remote. Consider pulling updates first."
            echo ""
            echo "Run: git pull origin main"
            echo ""
        fi
    fi
}

# Backup current configuration
backup_current() {
    print_status "Creating backup of current configuration..."
    
    local backup_dir="$HOME/.opencode-backup-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$backup_dir"
    
    # Backup config
    if [ -f ~/.config/opencode/opencode.json ]; then
        cp ~/.config/opencode/opencode.json "$backup_dir/"
        print_success "Configuration backed up"
    fi
    
    # Backup agents
    if [ -d ~/.opencode/agent ]; then
        cp -r ~/.opencode/agent "$backup_dir/"
        print_success "Agents backed up"
    fi
    
    # Backup orchestrator
    if [ -d ~/.opencode/orchestrator ]; then
        cp -r ~/.opencode/orchestrator "$backup_dir/"
        print_success "Orchestrator backed up"
    fi
    
    print_status "Backup saved to: $backup_dir"
}

# Update agents
update_agents() {
    print_status "Updating agents from repository..."
    
    local updated_count=0
    
    # Update main agents
    for agent_file in "$REPO_DIR/agents"/*.md; do
        if [ -f "$agent_file" ]; then
            agent_name=$(basename "$agent_file" .md)
            cp "$agent_file" ~/.opencode/agent/
            print_success "Updated agent: $agent_name"
            ((updated_count++))
        fi
    done
    
    # Update specialized agents
    for agent_file in "$REPO_DIR/agents/specialists"/*.md; do
        if [ -f "$agent_file" ]; then
            agent_name=$(basename "$agent_file" .md)
            cp "$agent_file" ~/.opencode/agent/
            print_success "Updated specialist: $agent_name"
            ((updated_count++))
        fi
    done
    
    print_success "Updated $updated_count agents"
}

# Update configuration
update_config() {
    print_status "Updating global configuration..."
    
    if [ -f "$REPO_DIR/config/opencode.json" ]; then
        cp "$REPO_DIR/config/opencode.json" ~/.config/opencode/opencode.json
        print_success "Configuration updated"
        print_ecommerce "E-commerce + Orchestration settings refreshed"
    else
        print_warning "New configuration file not found"
    fi
}

# Update orchestrator
update_orchestrator() {
    print_status "Updating Multi-Dispatch Orchestrator..."
    
    if [ -d "$REPO_DIR/opencode-orchestrator" ]; then
        rm -rf ~/.opencode/orchestrator
        mkdir -p ~/.opencode/orchestrator
        cp -r "$REPO_DIR/opencode-orchestrator"/* ~/.opencode/orchestrator/
        print_success "Orchestrator updated"
    fi
    
    # Update model router
    if [ -f "$REPO_DIR/ecommerce_model_router.py" ]; then
        cp "$REPO_DIR/ecommerce_model_router.py" ~/.opencode/orchestrator/
        print_success "Model router updated"
    fi
}

# Update commands
update_commands() {
    print_status "Updating commands..."
    
    if [ -d "$REPO_DIR/commands" ]; then
        for command_file in "$REPO_DIR/commands"/*.md; do
            if [ -f "$command_file" ]; then
                cp "$command_file" ~/.opencode/command/
                print_success "Updated command: $(basename "$command_file")"
            fi
        done
    fi
}

# Validate update
validate_update() {
    print_status "Validating update..."
    
    local errors=0
    
    # Check if agents exist
    local agent_count=$(ls ~/.opencode/agent/*.md 2>/dev/null | wc -l)
    if [ "$agent_count" -gt 0 ]; then
        print_success "Found $agent_count agents after update"
    else
        print_error "No agents found after update"
        ((errors++))
    fi
    
    # Check orchestrator
    if [ -f ~/.opencode/agent/orchestrator.md ]; then
        print_success "Orchestrator agent present"
    else
        print_error "Orchestrator agent missing"
        ((errors++))
    fi
    
    # Check specialized agents
    local ecommerce_agents=(
        "backend-nodejs-specialist"
        "frontend-react-specialist" 
        "mongodb-specialist"
        "ecommerce-business-logic"
        "devops-deployment-specialist"
        "security-specialist"
    )
    
    for agent in "${ecommerce_agents[@]}"; do
        if [ -f ~/.opencode/agent/$agent.md ]; then
            print_success "$agent agent present"
        else
            print_warning "$agent agent missing"
        fi
    done
    
    return $errors
}

# Show update summary
show_update_summary() {
    echo ""
    echo "=========================================="
    print_ecommerce "📊 UPDATE SUMMARY"
    echo "=========================================="
    echo ""
    echo "🕒 Update completed at: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    print_success "✅ Repository changes applied successfully"
    echo ""
    print_status "Available commands:"
    echo "  • /orchestrator 'project description'"
    echo "  • /backend-nodejs-specialist"
    echo "  • /frontend-react-specialist"
    echo "  • /mongodb-specialist"
    echo "  • /ecommerce-business-logic"
    echo "  • /devops-deployment-specialist"
    echo "  • /security-specialist"
    echo ""
    print_warning "⚠️ Restart OpenCode to apply changes"
    echo "   Run: opencode"
    echo ""
}

# Main update function
main() {
    check_git_status
    backup_current
    update_agents
    update_config
    update_orchestrator
    update_commands
    
    if validate_update; then
        show_update_summary
        print_success "🎉 Update completed successfully!"
    else
        print_error "Update completed with errors"
        exit 1
    fi
}

# Run main
main "$@"