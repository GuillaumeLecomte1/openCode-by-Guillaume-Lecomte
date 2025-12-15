#!/bin/bash

# OpenCode Configuration Installer
# by Guillaume Lecomte

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
    
    print_success "Directories created"
}

# Install global configuration
install_global_config() {
    print_status "Installing global OpenCode configuration..."
    
    if [ -f "config/global.json" ]; then
        cp config/global.json ~/.config/opencode/opencode.json
        print_success "Global configuration installed"
    else
        print_warning "Global configuration file not found"
    fi
}

# Install agents
install_agents() {
    print_status "Installing OpenCode agents..."
    
    for agent_file in agent/*.md; do
        if [ -f "$agent_file" ]; then
            cp "$agent_file" ~/.opencode/agent/
            print_success "Installed agent: $(basename "$agent_file")"
        fi
    done
}

# Install commands
install_commands() {
    print_status "Installing OpenCode commands..."
    
    for command_file in command/*.md; do
        if [ -f "$command_file" ]; then
            cp "$command_file" ~/.opencode/command/
            print_success "Installed command: $(basename "$command_file")"
        fi
    done
}

# Create MCP configuration
create_mcp_config() {
    print_status "Creating MCP configuration (.mcp.json)..."

    local project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
    local mcp_config="$project_root/.mcp.json"

    cat > "$mcp_config" << 'EOF'
{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "PROJECT_ROOT"],
      "env": {}
    },
    "git": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "PROJECT_ROOT"],
      "env": {}
    }
  }
}
EOF

    # Replace PROJECT_ROOT with actual path
    sed -i "s|PROJECT_ROOT|$project_root|g" "$mcp_config"

    print_success "MCP configuration created at $mcp_config"
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

    print_status "Context7 setup (optional):"
    echo "1. Get your API key from: https://context7.com/dashboard"
    echo "2. Add to .mcp.json if needed"
    echo "3. Restart OpenCode to apply changes"
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
    else
        print_error "Global configuration not found"
    fi
    
    # Check agents
    agent_count=$(ls ~/.opencode/agent/*.md 2>/dev/null | wc -l)
    print_success "Found $agent_count agents"
    
    # Check commands
    command_count=$(ls ~/.opencode/command/*.md 2>/dev/null | wc -l)
    print_success "Found $command_count commands"
}

# Main installation function
main() {
    echo "========================================"
    echo "OpenCode Configuration Installer"
    echo "by Guillaume Lecomte"
    echo "========================================"
    echo ""
    
    check_opencode
    create_directories
    install_global_config
    install_agents
    install_commands
    create_mcp_config
    install_mcp_servers
    setup_environment
    create_project_template
    verify_installation
    
    echo ""
    print_success "Installation completed!"
    echo ""
    echo "Next steps:"
    echo "1. Restart your terminal or run: source ~/.bashrc (or ~/.zshrc)"
    echo "2. Configure your API keys: opencode auth login"
    echo "3. Get Context7 API key: https://context7.com/dashboard"
    echo "4. Edit ~/.config/opencode/opencode.json and replace 'YOUR_CONTEXT7_API_KEY'"
    echo "5. For new projects, copy opencode.json.template to opencode.json"
    echo "6. Run: opencode"
    echo ""
    print_status "Enjoy your optimized OpenCode setup! 🚀"
}

# Run main function
main "$@"