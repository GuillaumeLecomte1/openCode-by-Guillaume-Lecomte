#!/bin/bash

# OpenCode Agents Test Suite - v3.0
# by Guillaume Lecomte - Comprehensive agents testing
# Tests all agents functionality and integration

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[TEST]${NC} $1"; }
print_success() { echo -e "${GREEN}[PASS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }
print_error() { echo -e "${RED}[FAIL]${NC} $1"; }
print_ecommerce() { echo -e "${PURPLE}[E-COM]${NC} $1"; }

# Test counters
declare -i TOTAL_TESTS=0
declare -i PASSED_TESTS=0
declare -i FAILED_TESTS=0
declare -i WARNING_TESTS=0

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
TEST_RESULTS_DIR="$REPO_DIR/tests/results"
AGENT_DIR="$HOME/.opencode/agent"

echo "=========================================="
echo "🧪 OpenCode Agents Test Suite v3.0"
echo "   Comprehensive Testing & Validation"
echo "=========================================="
echo ""

# Create test results directory
mkdir -p "$TEST_RESULTS_DIR"

# Test 1: Agent Directory Structure
test_agent_directory_structure() {
    print_status "Testing agent directory structure..."
    ((TOTAL_TESTS++))
    
    if [ -d "$AGENT_DIR" ]; then
        local agent_count=$(find "$AGENT_DIR" -name "*.md" | wc -l)
        if [ "$agent_count" -ge 10 ]; then
            print_success "Agent directory exists with $agent_count agents"
            ((PASSED_TESTS++))
        else
            print_warning "Agent directory exists but only $agent_count agents found"
            ((WARNING_TESTS++))
        fi
    else
        print_error "Agent directory not found"
        ((FAILED_TESTS++))
        return 1
    fi
}

# Test 2: Core Agents Presence
test_core_agents() {
    print_status "Testing core agents presence..."
    ((TOTAL_TESTS++))
    
    local core_agents=("orchestrator.md" "plan.md" "build.md")
    local missing_agents=0
    
    for agent in "${core_agents[@]}"; do
        if [ -f "$AGENT_DIR/$agent" ]; then
            print_success "Core agent found: $agent"
        else
            print_error "Core agent missing: $agent"
            ((missing_agents++))
        fi
    done
    
    if [ $missing_agents -eq 0 ]; then
        print_success "All core agents present"
        ((PASSED_TESTS++))
    else
        print_error "$missing_agents core agents missing"
        ((FAILED_TESTS++))
    fi
}

# Test 3: E-commerce Agents Presence
test_ecommerce_agents() {
    print_status "Testing e-commerce agents presence..."
    ((TOTAL_TESTS++))
    
    local ecommerce_agents=(
        "backend-nodejs-specialist.md"
        "frontend-react-specialist.md"
        "mongodb-specialist.md"
        "ecommerce-business-logic.md"
        "devops-deployment-specialist.md"
        "security-specialist.md"
    )
    
    local missing_count=0
    
    for agent in "${ecommerce_agents[@]}"; do
        if [ -f "$AGENT_DIR/$agent" ]; then
            print_success "E-commerce agent found: ${agent%.md}"
        else
            print_warning "E-commerce agent missing: ${agent%.md}"
            ((missing_count++))
        fi
    done
    
    if [ $missing_count -eq 0 ]; then
        print_success "All e-commerce agents present"
        ((PASSED_TESTS++))
    else
        print_warning "$missing_count e-commerce agents missing"
        ((WARNING_TESTS++))
    fi
}

# Test 4: Agent File Format Validation
test_agent_format() {
    print_status "Testing agent file format validation..."
    ((TOTAL_TESTS++))
    
    local format_errors=0
    local format_warnings=0
    
    for agent_file in "$AGENT_DIR"/*.md; do
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
                ((format_warnings++))
            fi
            
            # Check proper ending
            if ! tail -1 "$agent_file" | grep -q "^_.*_$"; then
                print_warning "$agent_name: Missing proper ending marker"
                ((format_warnings++))
            fi
            
            # Check for required sections
            if ! grep -q "## " "$agent_file"; then
                print_warning "$agent_name: Missing markdown sections"
                ((format_warnings++))
            fi
        fi
    done
    
    if [ $format_errors -eq 0 ]; then
        print_success "Agent format validation passed"
        ((PASSED_TESTS++))
    else
        print_error "Found $format_errors format errors"
        ((FAILED_TESTS++))
    fi
}

# Test 5: Orchestrator Configuration
test_orchestrator_config() {
    print_status "Testing orchestrator configuration..."
    ((TOTAL_TESTS++))
    
    local orchestrator_file="$AGENT_DIR/orchestrator.md"
    
    if [ ! -f "$orchestrator_file" ]; then
        print_error "Orchestrator agent not found"
        ((FAILED_TESTS++))
        return 1
    fi
    
    # Check for JSON configuration
    if grep -q '"orchestrator"' "$orchestrator_file"; then
        print_success "Orchestrator JSON configuration found"
    else
        print_error "Orchestrator JSON configuration missing"
        ((FAILED_TESTS++))
        return 1
    fi
    
    # Check for dispatch modes
    if grep -q "dispatch_modes\|Dispatch Modes" "$orchestrator_file"; then
        print_success "Dispatch modes documentation found"
    else
        print_warning "Dispatch modes documentation missing"
        ((WARNING_TESTS++))
    fi
    
    # Check for model routing
    if grep -q "model_routing\|routing" "$orchestrator_file"; then
        print_success "Model routing documentation found"
    else
        print_warning "Model routing documentation missing"
        ((WARNING_TESTS++))
    fi
    
    ((PASSED_TESTS++))
}

# Test 6: E-commerce Agents Integration
test_ecommerce_integration() {
    print_status "Testing e-commerce agents integration..."
    ((TOTAL_TESTS++))
    
    local integration_score=0
    local max_score=6
    
    # Check backend integration
    if grep -q "ecommerce\|E-commerce" "$AGENT_DIR/backend-nodejs-specialist.md"; then
        print_success "Backend agent has e-commerce focus"
        ((integration_score++))
    fi
    
    # Check frontend integration
    if grep -q "ecommerce\|E-commerce" "$AGENT_DIR/frontend-react-specialist.md"; then
        print_success "Frontend agent has e-commerce focus"
        ((integration_score++))
    fi
    
    # Check MongoDB integration
    if grep -q "ecommerce\|E-commerce" "$AGENT_DIR/mongodb-specialist.md"; then
        print_success "MongoDB agent has e-commerce focus"
        ((integration_score++))
    fi
    
    # Check business logic integration
    if grep -q "business\|ecommerce\|cart\|payment" "$AGENT_DIR/ecommerce-business-logic.md"; then
        print_success "Business logic agent has e-commerce focus"
        ((integration_score++))
    fi
    
    # Check devops integration
    if grep -q "ecommerce\|deployment" "$AGENT_DIR/devops-deployment-specialist.md"; then
        print_success "DevOps agent has e-commerce focus"
        ((integration_score++))
    fi
    
    # Check security integration
    if grep -q "ecommerce\|security\|PCI\|GDPR" "$AGENT_DIR/security-specialist.md"; then
        print_success "Security agent has e-commerce focus"
        ((integration_score++))
    fi
    
    local integration_percentage=$((integration_score * 100 / max_score))
    
    if [ $integration_percentage -ge 80 ]; then
        print_success "E-commerce integration: $integration_percentage% ($integration_score/$max_score)"
        ((PASSED_TESTS++))
    else
        print_warning "E-commerce integration: $integration_percentage% ($integration_score/$max_score)"
        ((WARNING_TESTS++))
    fi
}

# Test 7: Model Routing Configuration
test_model_routing() {
    print_status "Testing model routing configuration..."
    ((TOTAL_TESTS++))
    
    local config_file="$HOME/.config/opencode/opencode.json"
    
    if [ ! -f "$config_file" ]; then
        print_error "Configuration file not found"
        ((FAILED_TESTS++))
        return 1
    fi
    
    # Check for routing configuration
    if grep -q "model_routing\|routing" "$config_file"; then
        print_success "Model routing configuration found"
    else
        print_warning "Model routing configuration missing"
        ((WARNING_TESTS++))
    fi
    
    # Check for minimax-M2 configuration
    if grep -q "minimax-M2" "$config_file"; then
        print_success "minimax-M2 model configured"
    else
        print_warning "minimax-M2 model not configured"
        ((WARNING_TESTS++))
    fi
    
    # Check for grok-code-fast-1 configuration
    if grep -q "grok-code-fast-1" "$config_file"; then
        print_success "grok-code-fast-1 model configured"
    else
        print_warning "grok-code-fast-1 model not configured"
        ((WARNING_TESTS++))
    fi
    
    # Validate JSON syntax
    if python3 -c "import json; json.load(open('$config_file'))" 2>/dev/null; then
        print_success "Configuration JSON is valid"
    else
        print_error "Configuration JSON is invalid"
        ((FAILED_TESTS++))
        return 1
    fi
    
    ((PASSED_TESTS++))
}

# Test 8: Dispatch Modes Configuration
test_dispatch_modes() {
    print_status "Testing dispatch modes configuration..."
    ((TOTAL_TESTS++))
    
    local config_file="$HOME/.config/opencode/opencode.json"
    
    if [ ! -f "$config_file" ]; then
        print_error "Configuration file not found"
        ((FAILED_TESTS++))
        return 1
    fi
    
    # Check for dispatch modes
    if grep -q "dispatch_modes" "$config_file"; then
        print_success "Dispatch modes configuration found"
        
        # Check for specific modes
        local modes_found=0
        local expected_modes=("SEQUENTIAL" "PARALLEL" "HYBRID")
        
        for mode in "${expected_modes[@]}"; do
            if grep -q "$mode" "$config_file"; then
                print_success "Dispatch mode found: $mode"
                ((modes_found++))
            else
                print_warning "Dispatch mode missing: $mode"
            fi
        done
        
        if [ $modes_found -ge 2 ]; then
            print_success "Multiple dispatch modes configured ($modes_found/3)"
            ((PASSED_TESTS++))
        else
            print_warning "Limited dispatch modes configured ($modes_found/3)"
            ((WARNING_TESTS++))
        fi
    else
        print_error "Dispatch modes configuration missing"
        ((FAILED_TESTS++))
    fi
}

# Test 9: Agent Capabilities Validation
test_agent_capabilities() {
    print_status "Testing agent capabilities validation..."
    ((TOTAL_TESTS++))
    
    local capability_errors=0
    local agents_tested=0
    
    # Test key agents for capabilities
    local key_agents=(
        "orchestrator"
        "backend-nodejs-specialist"
        "frontend-react-specialist"
        "mongodb-specialist"
    )
    
    for agent_name in "${key_agents[@]}"; do
        local agent_file="$AGENT_DIR/$agent_name.md"
        if [ -f "$agent_file" ]; then
            ((agents_tested++))
            
            # Check for capabilities section
            if grep -q "capabilities\|Capabilities" "$agent_file"; then
                print_success "$agent_name has capabilities defined"
            else
                print_warning "$agent_name missing capabilities definition"
            fi
            
            # Check for tools configuration
            if grep -q "tools" "$agent_file"; then
                print_success "$agent_name has tools configuration"
            else
                print_warning "$agent_name missing tools configuration"
            fi
        fi
    done
    
    if [ $agents_tested -ge 3 ]; then
        print_success "Capabilities validation completed for $agents_tested agents"
        ((PASSED_TESTS++))
    else
        print_warning "Capabilities validation limited to $agents_tested agents"
        ((WARNING_TESTS++))
    fi
}

# Test 10: Repository Structure
test_repository_structure() {
    print_status "Testing repository structure..."
    ((TOTAL_TESTS++))
    
    local structure_errors=0
    
    # Check key directories
    local required_dirs=(
        "agents"
        "agents/specialists"
        "config"
        "scripts"
        "docs"
        "tests"
    )
    
    for dir in "${required_dirs[@]}"; do
        if [ -d "$REPO_DIR/$dir" ]; then
            print_success "Directory exists: $dir"
        else
            print_error "Directory missing: $dir"
            ((structure_errors++))
        fi
    done
    
    # Check key files
    local required_files=(
        "scripts/install.sh"
        "scripts/update.sh"
        "config/opencode.json"
        "docs/INSTALLATION.md"
        "README.md"
    )
    
    for file in "${required_files[@]}"; do
        if [ -f "$REPO_DIR/$file" ]; then
            print_success "File exists: $file"
        else
            print_error "File missing: $file"
            ((structure_errors++))
        fi
    done
    
    if [ $structure_errors -eq 0 ]; then
        print_success "Repository structure validation passed"
        ((PASSED_TESTS++))
    else
        print_error "Repository structure has $structure_errors issues"
        ((FAILED_TESTS++))
    fi
}

# Generate test report
generate_test_report() {
    local report_file="$TEST_RESULTS_DIR/agents-test-report-$(date +%Y%m%d-%H%M%S).txt"
    
    cat > "$report_file" << EOF
OpenCode Agents Test Report
Generated: $(date)
Repository: $REPO_DIR

TEST SUMMARY
============
Total Tests: $TOTAL_TESTS
Passed: $PASSED_TESTS
Failed: $FAILED_TESTS
Warnings: $WARNING_TESTS

Success Rate: $((PASSED_TESTS * 100 / TOTAL_TESTS))%

AGENT STATISTICS
================
Total Agents: $(find "$AGENT_DIR" -name "*.md" | wc -l)
Core Agents: $(ls "$AGENT_DIR"/{orchestrator,plan,build}.md 2>/dev/null | wc -l)
E-commerce Agents: $(ls "$AGENT_DIR"/*-specialist.md 2>/dev/null | wc -l)

CONFIGURATION STATUS
====================
OpenCode Config: $([ -f "$HOME/.config/opencode/opencode.json" ] && echo "✓ Present" || echo "✗ Missing")
JSON Valid: $(python3 -m json.tool "$HOME/.config/opencode/opencode.json" >/dev/null 2>&1 && echo "✓ Valid" || echo "✗ Invalid")
Model Routing: $(grep -q "model_routing" "$HOME/.config/opencode/opencode.json" 2>/dev/null && echo "✓ Configured" || echo "✗ Missing")
Dispatch Modes: $(grep -q "dispatch_modes" "$HOME/.config/opencode/opencode.json" 2>/dev/null && echo "✓ Configured" || echo "✗ Missing")

RECOMMENDATIONS
===============
EOF

    if [ $FAILED_TESTS -gt 0 ]; then
        echo "- Fix $FAILED_TESTS failed tests before production use" >> "$report_file"
    fi
    
    if [ $WARNING_TESTS -gt 0 ]; then
        echo "- Address $WARNING_TESTS warnings for optimal performance" >> "$report_file"
    fi
    
    if [ $PASSED_TESTS -eq $TOTAL_TESTS ]; then
        echo "- All tests passed! Configuration is production-ready." >> "$report_file"
    fi
    
    echo "" >> "$report_file"
    echo "Test completed at: $(date)" >> "$report_file"
    
    print_status "Test report saved: $report_file"
}

# Main test execution
main() {
    echo "Starting comprehensive agents test suite..."
    echo ""
    
    # Run all tests
    test_agent_directory_structure
    test_core_agents
    test_ecommerce_agents
    test_agent_format
    test_orchestrator_config
    test_ecommerce_integration
    test_model_routing
    test_dispatch_modes
    test_agent_capabilities
    test_repository_structure
    
    # Generate report
    generate_test_report
    
    # Final summary
    echo ""
    echo "=========================================="
    echo "📊 TEST RESULTS SUMMARY"
    echo "=========================================="
    echo "Total Tests: $TOTAL_TESTS"
    echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
    echo -e "Failed: ${RED}$FAILED_TESTS${NC}"
    echo -e "Warnings: ${YELLOW}$WARNING_TESTS${NC}"
    echo ""
    
    local success_rate=$((PASSED_TESTS * 100 / TOTAL_TESTS))
    
    if [ $FAILED_TESTS -eq 0 ]; then
        print_success "🎉 All critical tests passed!"
        print_status "Success rate: $success_rate%"
        echo ""
        print_ecommerce "✅ E-commerce configuration is ready for production"
    else
        print_error "⚠️ Some tests failed. Please review and fix issues."
        print_status "Success rate: $success_rate%"
        echo ""
        print_warning "Run ./scripts/update.sh to refresh configuration"
    fi
    
    echo ""
    echo "For detailed results, check: $TEST_RESULTS_DIR/"
    echo ""
    
    # Return appropriate exit code
    if [ $FAILED_TESTS -eq 0 ]; then
        return 0
    else
        return 1
    fi
}

# Run main function
main "$@"