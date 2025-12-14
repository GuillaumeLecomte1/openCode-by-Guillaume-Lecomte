#!/bin/bash

# OpenCode Configuration Validator - v3.0
# by Guillaume Lecomte - Comprehensive configuration validation
# Validates OpenCode setup and agent configuration

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_ecommerce() { echo -e "${PURPLE}[E-COMMERCE]${NC} $1"; }
print_orchestrator() { echo -e "${CYAN}[ORCHESTRATOR]${NC} $1"; }

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

# Validation counters
declare -i ERRORS=0
declare -i WARNINGS=0
declare -i CHECKS=0

echo "=========================================="
echo "🔍 OpenCode Configuration Validator v3.0"
echo "   Comprehensive Setup Validation"
echo "=========================================="
echo ""

# Check OpenCode installation
check_opencode_installation() {
    print_status "Checking OpenCode installation..."
    ((CHECKS++))
    
    if ! command -v opencode &> /dev/null; then
        print_error "OpenCode is not installed"
        ((ERRORS++))
        return 1
    fi
    
    local version=$(opencode --version 2>/dev/null || echo "unknown")
    print_success "OpenCode installed: $version"
    
    # Check version compatibility
    if [[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        print_success "Version format valid"
    else
        print_warning "Version format unexpected: $version"
        ((WARNINGS++))
    fi
}

# Check configuration file
validate_config_file() {
    print_status "Validating global configuration..."
    ((CHECKS++))
    
    local config_file="$HOME/.config/opencode/opencode.json"
    
    if [ ! -f "$config_file" ]; then
        print_error "Configuration file not found: $config_file"
        ((ERRORS++))
        return 1
    fi
    
    print_success "Configuration file exists"
    
    # Validate JSON syntax
    if python3 -c "import json; json.load(open('$config_file'))" 2>/dev/null; then
        print_success "Configuration JSON is valid"
    else
        print_error "Configuration JSON is invalid"
        ((ERRORS++))
        return 1
    fi
    
    # Check required fields
    local required_fields=("model" "tools")
    for field in "${required_fields[@]}"; do
        if grep -q "\"$field\"" "$config_file"; then
            print_success "Required field found: $field"
        else
            print_error "Required field missing: $field"
            ((ERRORS++))
        fi
    done
    
    # Check e-commerce specific fields
    if grep -q "orchestrator_config" "$config_file"; then
        print_ecommerce "E-commerce orchestration config found"
    else
        print_warning "E-commerce orchestration config not found"
        ((WARNINGS++))
    fi
}

# Check agent installation
validate_agents() {
    print_status "Validating agent installation..."
    ((CHECKS++))
    
    local agent_dir="$HOME/.opencode/agent"
    
    if [ ! -d "$agent_dir" ]; then
        print_error "Agent directory not found: $agent_dir"
        ((ERRORS++))
        return 1
    fi
    
    local agent_count=$(find "$agent_dir" -name "*.md" | wc -l)
    print_success "Found $agent_count agents"
    
    if [ "$agent_count" -eq 0 ]; then
        print_error "No agents found"
        ((ERRORS++))
        return 1
    fi
    
    # Check critical agents
    local critical_agents=("orchestrator.md" "plan.md" "build.md")
    for agent in "${critical_agents[@]}"; do
        if [ -f "$agent_dir/$agent" ]; then
            print_success "Critical agent found: $agent"
        else
            print_error "Critical agent missing: $agent"
            ((ERRORS++))
        fi
    done
    
    # Check e-commerce agents
    local ecommerce_agents=(
        "backend-nodejs-specialist.md"
        "frontend-react-specialist.md"
        "mongodb-specialist.md"
        "ecommerce-business-logic.md"
        "devops-deployment-specialist.md"
        "security-specialist.md"
    )
    
    print_ecommerce "Checking e-commerce agents:"
    for agent in "${ecommerce_agents[@]}"; do
        if [ -f "$agent_dir/$agent" ]; then
            print_success "  ✅ $agent"
        else
            print_error "  ❌ $agent"
            ((ERRORS++))
        fi
    done
}

# Validate agent format
validate_agent_formats() {
    print_status "Validating agent file formats..."
    ((CHECKS++))
    
    local agent_dir="$HOME/.opencode/agent"
    local format_errors=0
    
    for agent_file in "$agent_dir"/*.md; do
        if [ -f "$agent_file" ]; then
            local agent_name=$(basename "$agent_file" .md)
            
            # Check title
            if ! head -1 "$agent_file" | grep -q "^# "; then
                print_error "$agent_name: Missing or invalid title"
                ((format_errors++))
            fi
            
            # Check JSON configuration
            if ! grep -q '"agent":' "$agent_file"; then
                print_warning "$agent_name: Missing JSON configuration"
                ((WARNINGS++))
            fi
            
            # Check proper ending
            if ! tail -1 "$agent_file" | grep -q "^_.*_$"; then
                print_warning "$agent_name: Missing proper ending marker"
                ((WARNINGS++))
            fi
        fi
    done
    
    if [ $format_errors -eq 0 ]; then
        print_success "Agent formats validated successfully"
    else
        print_error "Found $format_errors agent format errors"
        ((ERRORS++))
    fi
}

# Check orchestrator installation
validate_orchestrator() {
    print_status "Validating orchestrator installation..."
    ((CHECKS++))
    
    local orchestrator_dir="$HOME/.opencode/orchestrator"
    
    if [ ! -d "$orchestrator_dir" ]; then
        print_warning "Orchestrator directory not found"
        ((WARNINGS++))
        return 1
    fi
    
    print_success "Orchestrator directory exists"
    
    # Check key orchestrator files
    local orchestrator_files=(
        "opencode_orchestrator.py"
        "multi_dispatch"
        "classifiers"
        "core"
    )
    
    for file in "${orchestrator_files[@]}"; do
        if [ -e "$orchestrator_dir/$file" ]; then
            print_success "Orchestrator component found: $file"
        else
            print_warning "Orchestrator component missing: $file"
            ((WARNINGS++))
        fi
    done
    
    # Check model router
    if [ -f "$orchestrator_dir/ecommerce_model_router.py" ]; then
        print_success "E-commerce model router found"
    else
        print_warning "E-commerce model router not found"
        ((WARNINGS++))
    fi
}

# Check commands installation
validate_commands() {
    print_status "Validating commands installation..."
    ((CHECKS++))
    
    local command_dir="$HOME/.opencode/command"
    
    if [ ! -d "$command_dir" ]; then
        print_warning "Command directory not found"
        ((WARNINGS++))
        return 1
    fi
    
    local command_count=$(find "$command_dir" -name "*.md" | wc -l)
    print_success "Found $command_count commands"
}

# Check permissions
validate_permissions() {
    print_status "Validating file permissions..."
    ((CHECKS++))
    
    local agent_dir="$HOME/.opencode/agent"
    local permission_errors=0
    
    for agent_file in "$agent_dir"/*.md; do
        if [ -f "$agent_file" ]; then
            if [ ! -r "$agent_file" ]; then
                print_error "Agent file not readable: $(basename "$agent_file")"
                ((permission_errors++))
            fi
        fi
    done
    
    if [ $permission_errors -eq 0 ]; then
        print_success "All agent files are readable"
    else
        print_error "Found $permission_errors permission errors"
        ((ERRORS++))
    fi
}

# Check directory structure
validate_directory_structure() {
    print_status "Validating directory structure..."
    ((CHECKS++))
    
    local required_dirs=(
        "$HOME/.config/opencode"
        "$HOME/.opencode/agent"
        "$HOME/.opencode/command"
    )
    
    for dir in "${required_dirs[@]}"; do
        if [ -d "$dir" ]; then
            print_success "Directory exists: $(basename "$dir")"
        else
            print_error "Directory missing: $dir"
            ((ERRORS++))
        fi
    done
}

# Generate validation report
generate_report() {
    echo ""
    echo "=========================================="
    echo "📊 VALIDATION REPORT"
    echo "=========================================="
    echo ""
    echo "🔍 Total checks performed: $CHECKS"
    echo ""
    
    if [ $ERRORS -eq 0 ]; then
        echo -e "${GREEN}✅ All critical checks passed${NC}"
    else
        echo -e "${RED}❌ $ERRORS errors found${NC}"
    fi
    
    if [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}✅ No warnings${NC}"
    else
        echo -e "${YELLOW}⚠️  $WARNINGS warnings${NC}"
    fi
    
    echo ""
    
    # Status summary
    if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
        print_success "🎉 Configuration is perfect!"
        echo ""
        print_status "Your OpenCode setup is fully optimized for e-commerce development"
        echo ""
        print_orchestrator "Available orchestration modes:"
        echo "  • SEQUENTIAL (Planning, Deployment)"
        echo "  • PARALLEL (Backend, Frontend)"
        echo "  • HYBRID (Integration)"
        echo ""
        print_ecommerce "Use /orchestrator with your project description"
        return 0
    elif [ $ERRORS -eq 0 ]; then
        print_warning "Configuration is good with minor warnings"
        echo ""
        print_status "Run ./scripts/update.sh to refresh configuration"
        return 0
    else
        print_error "Configuration has critical errors"
        echo ""
        print_status "Please fix the errors above and run installation again"
        echo "  ./scripts/install.sh"
        return 1
    fi
}

# Main validation function
main() {
    check_opencode_installation
    validate_config_file
    validate_agents
    validate_agent_formats
    validate_orchestrator
    validate_commands
    validate_permissions
    validate_directory_structure
    
    generate_report
}

# Run validation
main "$@"