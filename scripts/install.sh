#!/bin/bash

# OpenCode Configuration Installer - Optimized v3.0
# by Guillaume Lecomte - E-commerce & Multi-Dispatch Orchestration
# Repository: https://github.com/GuillaumeLecomte1/openCode-by-Guillaume-Lecomte

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print colored output
print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_ecommerce() { echo -e "${PURPLE}[E-COMMERCE]${NC} $1"; }
print_orchestrator() { echo -e "${CYAN}[ORCHESTRATOR]${NC} $1"; }

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="$REPO_DIR/config"
SCRIPTS_BIN="$SCRIPT_DIR/bin"

# Version info
VERSION="3.0"
INSTALL_DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Banner
echo "=========================================="
echo "🚀 OpenCode Configuration Installer v$VERSION"
echo "   by Guillaume Lecomte"
echo "   E-commerce + Multi-Dispatch Orchestration"
echo "=========================================="
echo ""

# Check if running from repo directory
if [ ! -f "$REPO_DIR/README.md" ]; then
    print_error "Please run this script from the repository root directory"
    exit 1
fi

# Validate OpenCode installation
check_opencode() {
    print_status "Checking OpenCode installation..."
    
    if ! command -v opencode &> /dev/null; then
        print_error "OpenCode is not installed. Please install it first:"
        echo "  curl -fsSL https://opencode.ai/install | bash"
        exit 1
    fi
    
    OPENCODE_VERSION=$(opencode --version 2>/dev/null || echo "unknown")
    print_success "OpenCode found: $OPENCODE_VERSION"
}

# Create necessary directories
create_directories() {
    print_status "Creating OpenCode configuration directories..."
    
    mkdir -p ~/.config/opencode
    mkdir -p ~/.opencode/{agent,command,tool,plugin,orchestrator}
    
    print_success "Directories created successfully"
}

# Install global configuration
install_global_config() {
    print_status "Installing global OpenCode configuration..."
    
    if [ -f "$CONFIG_DIR/opencode.json" ]; then
        cp "$CONFIG_DIR/opencode.json" ~/.config/opencode/opencode.json
        print_success "Global configuration installed"
        print_ecommerce "E-commerce + Orchestration mode activated"
    else
        print_warning "Configuration file not found, using fallback"
        create_fallback_config
    fi
}

# Create fallback configuration
create_fallback_config() {
    cat > ~/.config/opencode/opencode.json << 'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "model": "minimax-M2",
  "small_model": "grok-code-fast-1",
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
EOF
    print_warning "Fallback configuration created"
}

# Install agents
install_agents() {
    print_status "Installing OpenCode agents..."
    
    local agent_count=0
    
    # Install main agents
    for agent_file in "$REPO_DIR/agents"/*.md; do
        if [ -f "$agent_file" ]; then
            agent_name=$(basename "$agent_file" .md)
            cp "$agent_file" ~/.opencode/agent/
            print_success "Installed main agent: $agent_name"
            ((agent_count++))
        fi
    done
    
    # Install specialized agents
    for agent_file in "$REPO_DIR/agents/specialists"/*.md; do
        if [ -f "$agent_file" ]; then
            agent_name=$(basename "$agent_file" .md)
            cp "$agent_file" ~/.opencode/agent/
            print_success "Installed specialized agent: $agent_name"
            ((agent_count++))
        fi
    done
    
    print_success "Total agents installed: $agent_count"
}

# Install orchestrator
install_orchestrator() {
    print_status "Installing Multi-Dispatch Orchestrator..."
    
    if [ -d "$REPO_DIR/opencode-orchestrator" ]; then
        mkdir -p ~/.opencode/orchestrator
        cp -r "$REPO_DIR/opencode-orchestrator"/* ~/.opencode/orchestrator/
        print_success "Multi-Dispatch Orchestrator installed"
        print_orchestrator "Dispatch modes: SEQUENTIAL, PARALLEL, HYBRID"
    else
        print_warning "Orchestrator directory not found"
    fi
    
    # Install model router
    if [ -f "$REPO_DIR/ecommerce_model_router.py" ]; then
        cp "$REPO_DIR/ecommerce_model_router.py" ~/.opencode/orchestrator/
        print_success "E-commerce Model Router installed"
        print_ecommerce "minimax-M2 + grok-code-fast-1 routing active"
    fi
}

# Install commands
install_commands() {
    print_status "Installing OpenCode commands..."
    
    if [ -d "$REPO_DIR/commands" ]; then
        for command_file in "$REPO_DIR/commands"/*.md; do
            if [ -f "$command_file" ]; then
                cp "$command_file" ~/.opencode/command/
                print_success "Installed command: $(basename "$command_file")"
            fi
        done
    fi
}

# Sync agents from repository
sync_agents() {
    print_status "Synchronizing agents from repository..."
    
    if [ -f "$SCRIPT_DIR/sync-agents.sh" ]; then
        chmod +x "$SCRIPT_DIR/sync-agents.sh"
        "$SCRIPT_DIR/sync-agents.sh"
        print_success "Agents synchronized successfully"
    else
        print_warning "Sync script not found"
    fi
}

# Install MCP servers
install_mcp_servers() {
    print_status "Installing MCP servers..."
    
    if command -v npm &> /dev/null; then
        print_status "Installing MCP npm packages..."
        npm install -g @modelcontextprotocol/server-filesystem @modelcontextprotocol/server-git @upstash/context7-mcp 2>/dev/null || true
        print_success "MCP servers installation completed"
    else
        print_warning "npm not found. Please install MCP servers manually"
    fi
}

# Validate installation
validate_installation() {
    print_status "Validating installation..."
    
    local errors=0
    
    # Check config
    if [ -f ~/.config/opencode/opencode.json ]; then
        print_success "Global configuration found"
    else
        print_error "Global configuration missing"
        ((errors++))
    fi
    
    # Check agents
    local agent_count=$(ls ~/.opencode/agent/*.md 2>/dev/null | wc -l)
    if [ "$agent_count" -gt 0 ]; then
        print_success "Found $agent_count agents"
    else
        print_error "No agents found"
        ((errors++))
    fi
    
    # Check orchestrator
    if [ -d ~/.opencode/orchestrator ]; then
        print_success "Multi-Dispatch Orchestrator installed"
    fi
    
    return $errors
}

# Show configuration summary
show_summary() {
    echo ""
    echo "=========================================="
    print_ecommerce "📊 INSTALLATION SUMMARY"
    echo "=========================================="
    echo ""
    echo "📅 Install Date: $INSTALL_DATE"
    echo "🔧 Version: $VERSION"
    echo ""
    print_ecommerce "🤖 Model Routing Strategy:"
    echo "  • Primary: minimax-M2 (complex tasks)"
    echo "  • Fast: grok-code-fast-1 (simple tasks)"
    echo ""
    print_ecommerce "🏪 E-commerce Agents:"
    echo "  • backend-nodejs-specialist (API & Security)"
    echo "  • frontend-react-specialist (React & TypeScript)"
    echo "  • mongodb-specialist (Database & Queries)"
    echo "  • ecommerce-business-logic (Business Logic)"
    echo "  • devops-deployment-specialist (Infrastructure)"
    echo "  • security-specialist (Security & Audit)"
    echo ""
    print_orchestrator "⚡ Dispatch Modes:"
    echo "  • Planning: SEQUENTIAL"
    echo "  • Backend: PARALLEL"
    echo "  • Frontend: PARALLEL"
    echo "  • Integration: HYBRID"
    echo "  • Deployment: SEQUENTIAL"
    echo ""
    print_ecommerce "💰 Optimization:"
    echo "  • Estimated savings: 65%"
    echo "  • Automatic model switching"
    echo "  • Quality maintained for critical tasks"
    echo ""
}

# Main installation function
main() {
    check_opencode
    create_directories
    install_global_config
    install_agents
    install_orchestrator
    install_commands
    sync_agents
    install_mcp_servers
    
    # Validate and show summary
    if validate_installation; then
        show_summary
        echo ""
        print_success "🎉 Installation completed successfully!"
        echo ""
        print_status "Next steps:"
        echo "1. Restart your terminal or run: source ~/.bashrc"
        echo "2. Configure your API keys: opencode auth login"
        echo "3. For Context7: Get key7.com/dashboard at https://context"
        echo "4. Test: opencode"
        echo ""
        print_ecommerce "🚀 Your e-commerce development environment is ready!"
        echo "   Use: /orchestrator 'Your project description'"
    else
        print_error "Installation completed with errors. Please check the logs above."
        exit 1
    fi
}

# Run main function
main "$@"