#!/bin/bash

# OpenCode Configuration Installer (Updated)
# by Guillaume Lecomte - E-commerce Optimized
# Version 2.0 with minimax-M2 + grok-code-fast-1 routing

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_ecommerce() {
    echo -e "${PURPLE}[E-COMMERCE]${NC} $1"
}

# Check if OpenCode is installed
check_opencode() {
    if ! command -v opencode &> /dev/null; then
        print_error "OpenCode is not installed. Please install it first:"
        echo "curl -fsSL https://opencode.ai/install | bash"
        exit 1
    fi
    print_success "OpenCode found: $(opencode --version)"
}

# Create necessary directories
create_directories() {
    print_status "Creating OpenCode configuration directories..."
    
    mkdir -p ~/.config/opencode
    mkdir -p ~/.opencode/agent
    mkdir -p ~/.opencode/command  
    mkdir -p ~/.opencode/tool
    mkdir -p ~/.opencode/plugin
    mkdir -p ~/.opencode/orchestrator
    
    print_success "Directories created"
}

# Install global configuration
install_global_config() {
    print_status "Installing global OpenCode configuration..."
    
    if [ -f "config/global.json" ]; then
        cp config/global.json ~/.config/opencode/opencode.json
        print_success "Global configuration installed with minimax-M2 + grok-code-fast-1 routing"
        print_ecommerce "E-commerce specialized configuration activated"
    else
        print_warning "Global configuration file not found"
    fi
}

# Install agents
install_agents() {
    print_status "Installing OpenCode agents..."
    
    agent_count=0
    
    # Install existing agents
    for agent_file in agent/*.md; do
        if [ -f "$agent_file" ]; then
            cp "$agent_file" ~/.opencode/agent/
            agent_name=$(basename "$agent_file" .md)
            print_success "Installed agent: $agent_name"
            ((agent_count++))
        fi
    done
    
    # Install new e-commerce specialized agents
    if [ -f "agent/backend-nodejs-specialist.md" ]; then
        cp agent/backend-nodejs-specialist.md ~/.opencode/agent/
        print_ecommerce "Installed backend-nodejs-specialist (minimax-M2)"
        ((agent_count++))
    fi
    
    if [ -f "agent/mongodb-specialist.md" ]; then
        cp agent/mongodb-specialist.md ~/.opencode/agent/
        print_ecommerce "Installed mongodb-specialist (minimax-M2)"
        ((agent_count++))
    fi
    
    if [ -f "agent/ecommerce-business-logic.md" ]; then
        cp agent/ecommerce-business-logic.md ~/.opencode/agent/
        print_ecommerce "Installed ecommerce-business-logic (minimax-M2)"
        ((agent_count++))
    fi
    
    if [ -f "agent/devops-deployment-specialist.md" ]; then
        cp agent/devops-deployment-specialist.md ~/.opencode/agent/
        print_ecommerce "Installed devops-deployment-specialist (grok-code-fast-1)"
        ((agent_count++))
    fi
    
    print_success "Total agents installed: $agent_count"
}

# Install commands
install_commands() {
    print_status "Installing OpenCode commands..."
    
    for command_file in commands/*.md; do
        if [ -f "$command_file" ]; then
            cp "$command_file" ~/.opencode/command/
            print_success "Installed command: $(basename "$command_file")"
        fi
    done
}

# Install orchestrator multi-dispatch
install_orchestrator() {
    print_status "Installing Multi-Dispatch Orchestrator..."
    
    if [ -f "opencode-orchestrator/multi_dispatch/primary_orchestrator.py" ]; then
        mkdir -p ~/.opencode/orchestrator
        cp -r opencode-orchestrator/* ~/.opencode/orchestrator/
        print_success "Multi-Dispatch Orchestrator installed"
        print_ecommerce "E-commerce dispatch modes configured"
    else
        print_warning "Orchestrator not found in opencode-orchestrator/"
    fi
    
    # Install ecommerce model router
    if [ -f "ecommerce_model_router.py" ]; then
        cp ecommerce_model_router.py ~/.opencode/orchestrator/
        print_success "E-commerce Model Router installed"
        print_ecommerce "minimax-M2 + grok-code-fast-1 routing active"
    fi
}

# Install MCP servers
install_mcp_servers() {
    print_status "Installing MCP servers..."
    
    # Check if npm is available
    if command -v npm &> /dev/null; then
        print_status "Installing MCP npm packages..."
        npm install -g @modelcontextprotocol/server-filesystem @modelcontextprotocol/server-git @upstash/context7-mcp || print_warning "Some MCP packages failed to install (this may be expected if they're not available)"
        print_success "MCP servers installation completed"
    else
        print_warning "npm not found. Please install MCP servers manually:"
        echo "npm install -g @modelcontextprotocol/server-filesystem @modelcontextprotocol/server-git @upstash/context7-mcp"
    fi
    
    print_status "Context7 setup:"
    echo "1. Get your API key from: https://context7.com/dashboard"
    echo "2. Edit ~/.config/opencode/opencode.json"
    echo "3. Replace 'YOUR_CONTEXT7_API_KEY' with your actual key"
    echo "4. Restart OpenCode to apply changes"
}

# Setup environment variables
setup_environment() {
    print_status "Setting up environment variables..."
    
    shell_rc=""
    if [ -n "$ZSH_VERSION" ]; then
        shell_rc="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        shell_rc="$HOME/.bashrc"
    fi
    
    if [ -n "$shell_rc" ] && [ -f "$shell_rc" ]; then
        if ! grep -q "# OpenCode Configuration" "$shell_rc"; then
            echo "" >> "$shell_rc"
            echo "# OpenCode Configuration" >> "$shell_rc"
            echo "export OPENCODE_CONFIG_DIR=\"$(pwd)\"" >> "$shell_rc"
            echo "export OPENCODE_ECOMMERCE_MODE=\"true\"" >> "$shell_rc"
            print_success "Environment variables added to $shell_rc"
        else
            print_warning "Environment variables already configured"
        fi
    fi
}

# Create project configuration template
create_project_template() {
    print_status "Creating project configuration template..."
    
    if [ -f "config/project.json" ]; then
        cp config/project.json ./opencode.json.template
        print_success "Project template created as opencode.json.template"
    fi
}

# Verify installation
verify_installation() {
    print_status "Verifying installation..."
    
    # Check if config file exists
    if [ -f ~/.config/opencode/opencode.json ]; then
        print_success "Global configuration found"
        
        # Check model configuration
        if grep -q "minimax-M2" ~/.config/opencode/opencode.json; then
            print_ecommerce "minimax-M2 configured as primary model"
        fi
        
        if grep -q "grok-code-fast-1" ~/.config/opencode/opencode.json; then
            print_ecommerce "grok-code-fast-1 configured as fast model"
        fi
    else
        print_error "Global configuration not found"
    fi
    
    # Check agents
    agent_count=$(ls ~/.opencode/agent/*.md 2>/dev/null | wc -l)
    print_success "Found $agent_count agents"
    
    # Check commands
    command_count=$(ls ~/.opencode/command/*.md 2>/dev/null | wc -l)
    print_success "Found $command_count commands"
    
    # Check orchestrator
    if [ -d ~/.opencode/orchestrator ]; then
        print_success "Multi-Dispatch Orchestrator installed"
    fi
}

# Display configuration summary
show_configuration_summary() {
    echo ""
    echo "=========================================="
    print_ecommerce "E-COMMERCE CONFIGURATION SUMMARY"
    echo "=========================================="
    echo ""
    
    print_ecommerce "🤖 Model Routing Strategy:"
    echo "  • Primary: minimax-M2 (complex tasks, high quality)"
    echo "  • Fast: grok-code-fast-1 (simple tasks, cost-effective)"
    echo ""
    
    print_ecommerce "🏪 E-commerce Specialized Agents:"
    echo "  • backend-nodejs-specialist (API, security, performance)"
    echo "  • mongodb-specialist (schema, queries, optimization)"
    echo "  • ecommerce-business-logic (cart, payments, orders)"
    echo "  • devops-deployment-specialist (Docker, CI/CD, monitoring)"
    echo ""
    
    print_ecommerce "⚡ Dispatch Modes Optimized:"
    echo "  • Planning: SEQUENTIAL (architecture first)"
    echo "  • Backend: PARALLEL (Node.js + MongoDB)"
    echo "  • Frontend: PARALLEL (React + Business Logic)"
    echo "  • Integration: HYBRID (coordinated execution)"
    echo "  • Deployment: SEQUENTIAL (secure deployment)"
    echo ""
    
    print_ecommerce "💰 Cost Optimization:"
    echo "  • Estimated savings: 65% (grok-code-fast-1 for simple tasks)"
    echo "  • Quality maintained via minimax-M2 for critical tasks"
    echo "  • Automatic model switching based on complexity"
    echo ""
}

# Main installation function
main() {
    echo "========================================"
    echo "OpenCode E-Commerce Configuration Installer"
    echo "by Guillaume Lecomte v2.0"
    echo "Multi-Dispatch Orchestrator + Model Routing"
    echo "========================================"
    echo ""
    
    check_opencode
    create_directories
    install_global_config
    install_agents
    install_commands
    install_orchestrator
    install_mcp_servers
    setup_environment
    create_project_template
    verify_installation
    show_configuration_summary
    
    echo ""
    print_success "Installation completed!"
    echo ""
    print_status "Next steps:"
    echo "1. Restart your terminal or run: source ~/.bashrc (or ~/.zshrc)"
    echo "2. Configure your API keys: opencode auth login"
    echo "3. Get Context7 API key: https://context7.com/dashboard"
    echo "4. Edit ~/.config/opencode/opencode.json and replace 'YOUR_CONTEXT7_API_KEY'"
    echo "5. For new projects, copy opencode.json.template to opencode.json"
    echo "6. Run: opencode"
    echo ""
    print_ecommerce "🚀 Your e-commerce development environment is ready!"
    echo "   Use specialized agents for optimal results:"
    echo "   • /backend-nodejs-specialist for API development"
    echo "   • /mongodb-specialist for database optimization"
    echo "   • /ecommerce-business-logic for business features"
    echo "   • /devops-deployment-specialist for infrastructure"
    echo ""
}

# Run main function
main "$@"