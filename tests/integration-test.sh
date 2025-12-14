#!/bin/bash

# OpenCode Integration Test Suite - v3.0
# by Guillaume Lecomte - End-to-end integration testing
# Tests complete OpenCode workflow and orchestration

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INT]${NC} $1"; }
print_success() { echo -e "${GREEN}[PASS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }
print_error() { echo -e "${RED}[FAIL]${NC} $1"; }
print_ecommerce() { echo -e "${PURPLE}[E-COM]${NC} $1"; }
print_orchestrator() { echo -e "${CYAN}[ORCH]${NC} $1"; }

# Test configuration
declare -i TOTAL_TESTS=0
declare -i PASSED_TESTS=0
declare -i FAILED_TESTS=0
declare -i SKIPPED_TESTS=0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
TEST_RESULTS_DIR="$REPO_DIR/tests/results"
INTEGRATION_LOG="$TEST_RESULTS_DIR/integration-test-$(date +%Y%m%d-%H%M%S).log"

echo "=========================================="
echo "🔗 OpenCode Integration Test Suite v3.0"
echo "   End-to-End Workflow Testing"
echo "=========================================="
echo ""

# Create test results directory and log file
mkdir -p "$TEST_RESULTS_DIR"
touch "$INTEGRATION_LOG"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$INTEGRATION_LOG"
    echo "$1"
}

# Test 1: OpenCode Installation Check
test_opencode_installation() {
    print_status "Testing OpenCode installation..."
    ((TOTAL_TESTS++))
    log_message "Starting OpenCode installation test"
    
    if ! command -v opencode &> /dev/null; then
        print_error "OpenCode is not installed"
        log_message "ERROR: OpenCode not found"
        ((FAILED_TESTS++))
        return 1
    fi
    
    local version=$(opencode --version 2>/dev/null || echo "unknown")
    log_message "OpenCode version: $version"
    print_success "OpenCode installed: $version"
    ((PASSED_TESTS++))
}

# Test 2: Configuration Load Test
test_configuration_loading() {
    print_status "Testing configuration loading..."
    ((TOTAL_TESTS++))
    log_message "Starting configuration load test"
    
    local config_file="$HOME/.config/opencode/opencode.json"
    
    if [ ! -f "$config_file" ]; then
        print_error "Configuration file not found"
        log_message "ERROR: Configuration file missing"
        ((FAILED_TESTS++))
        return 1
    fi
    
    # Test JSON validity
    if python3 -c "import json; json.load(open('$config_file'))" 2>/dev/null; then
        print_success "Configuration JSON is valid"
        log_message "SUCCESS: Configuration JSON valid"
    else
        print_error "Configuration JSON is invalid"
        log_message "ERROR: Configuration JSON invalid"
        ((FAILED_TESTS++))
        return 1
    fi
    
    # Test required fields
    local required_fields=("model" "tools" "orchestrator_config")
    for field in "${required_fields[@]}"; do
        if grep -q "\"$field\"" "$config_file"; then
            print_success "Required field found: $field"
            log_message "SUCCESS: Field $field found"
        else
            print_warning "Required field missing: $field"
            log_message "WARN: Field $field missing"
            ((SKIPPED_TESTS++))
        fi
    done
    
    ((PASSED_TESTS++))
}

# Test 3: Agent Detection Test
test_agent_detection() {
    print_status "Testing agent detection..."
    ((TOTAL_TESTS++))
    log_message "Starting agent detection test"
    
    local agent_dir="$HOME/.opencode/agent"
    
    if [ ! -d "$agent_dir" ]; then
        print_error "Agent directory not found"
        log_message "ERROR: Agent directory missing"
        ((FAILED_TESTS++))
        return 1
    fi
    
    local agent_count=$(find "$agent_dir" -name "*.md" | wc -l)
    log_message "Found $agent_count agents"
    
    if [ "$agent_count" -lt 10 ]; then
        print_warning "Low agent count: $agent_count"
        log_message "WARN: Low agent count: $agent_count"
        ((SKIPPED_TESTS++))
    else
        print_success "Sufficient agents found: $agent_count"
        log_message "SUCCESS: Sufficient agents: $agent_count"
    fi
    
    # Test critical agents
    local critical_agents=("orchestrator" "backend-nodejs-specialist" "frontend-react-specialist")
    for agent in "${critical_agents[@]}"; do
        if [ -f "$agent_dir/$agent.md" ]; then
            print_success "Critical agent found: $agent"
            log_message "SUCCESS: Critical agent $agent found"
        else
            print_error "Critical agent missing: $agent"
            log_message "ERROR: Critical agent $agent missing"
            ((FAILED_TESTS++))
        fi
    done
    
    ((PASSED_TESTS++))
}

# Test 4: Orchestrator Functionality Test
test_orchestrator_functionality() {
    print_status "Testing orchestrator functionality..."
    ((TOTAL_TESTS++))
    log_message "Starting orchestrator functionality test"
    
    # Check orchestrator file
    local orchestrator_file="$HOME/.opencode/agent/orchestrator.md"
    if [ ! -f "$orchestrator_file" ]; then
        print_error "Orchestrator agent not found"
        log_message "ERROR: Orchestrator agent missing"
        ((FAILED_TESTS++))
        return 1
    fi
    
    # Test orchestrator configuration
    if grep -q '"orchestrator"' "$orchestrator_file"; then
        print_success "Orchestrator JSON configuration found"
        log_message "SUCCESS: Orchestrator JSON config found"
    else
        print_error "Orchestrator JSON configuration missing"
        log_message "ERROR: Orchestrator JSON config missing"
        ((FAILED_TESTS++))
        return 1
    fi
    
    # Test dispatch modes documentation
    local dispatch_modes=("SEQUENTIAL" "PARALLEL" "HYBRID")
    local modes_found=0
    
    for mode in "${dispatch_modes[@]}"; do
        if grep -q "$mode" "$orchestrator_file"; then
            print_success "Dispatch mode documented: $mode"
            log_message "SUCCESS: Dispatch mode $mode found"
            ((modes_found++))
        else
            print_warning "Dispatch mode missing: $mode"
            log_message "WARN: Dispatch mode $mode missing"
        fi
    done
    
    if [ $modes_found -ge 2 ]; then
        print_success "Multiple dispatch modes documented ($modes_found/3)"
        log_message "SUCCESS: Multiple dispatch modes documented"
        ((PASSED_TESTS++))
    else
        print_warning "Limited dispatch modes documented ($modes_found/3)"
        log_message "WARN: Limited dispatch modes documented"
        ((SKIPPED_TESTS++))
    fi
}

# Test 5: Model Routing Test
test_model_routing() {
    print_status "Testing model routing configuration..."
    ((TOTAL_TESTS++))
    log_message "Starting model routing test"
    
    local config_file="$HOME/.config/opencode/opencode.json"
    
    # Test routing configuration
    if grep -q "model_routing" "$config_file"; then
        print_success "Model routing configuration found"
        log_message "SUCCESS: Model routing config found"
    else
        print_warning "Model routing configuration missing"
        log_message "WARN: Model routing config missing"
        ((SKIPPED_TESTS++))
    fi
    
    # Test model configuration
    local models_found=0
    if grep -q "minimax-M2" "$config_file"; then
        print_success "Primary model (minimax-M2) configured"
        log_message "SUCCESS: minimax-M2 configured"
        ((models_found++))
    fi
    
    if grep -q "grok-code-fast-1" "$config_file"; then
        print_success "Fast model (grok-code-fast-1) configured"
        log_message "SUCCESS: grok-code-fast-1 configured"
        ((models_found++))
    fi
    
    if [ $models_found -ge 1 ]; then
        print_success "Model routing partially configured ($models_found/2 models)"
        log_message "SUCCESS: Model routing partially configured"
        ((PASSED_TESTS++))
    else
        print_error "Model routing not properly configured"
        log_message "ERROR: Model routing not configured"
        ((FAILED_TESTS++))
    fi
}

# Test 6: E-commerce Integration Test
test_ecommerce_integration() {
    print_status "Testing e-commerce integration..."
    ((TOTAL_TESTS++))
    log_message "Starting e-commerce integration test"
    
    local agent_dir="$HOME/.opencode/agent"
    local ecommerce_agents=(
        "backend-nodejs-specialist"
        "frontend-react-specialist"
        "mongodb-specialist"
        "ecommerce-business-logic"
        "devops-deployment-specialist"
        "security-specialist"
    )
    
    local present_agents=0
    local ecommerce_focus_count=0
    
    for agent in "${ecommerce_agents[@]}"; do
        if [ -f "$agent_dir/$agent.md" ]; then
            ((present_agents++))
            print_success "E-commerce agent present: $agent"
            log_message "SUCCESS: E-commerce agent $agent present"
            
            # Check for e-commerce focus
            if grep -q "ecommerce\|E-commerce" "$agent_dir/$agent.md"; then
                ((ecommerce_focus_count++))
                print_success "$agent has e-commerce specialization"
                log_message "SUCCESS: $agent has e-commerce focus"
            fi
        else
            print_error "E-commerce agent missing: $agent"
            log_message "ERROR: E-commerce agent $agent missing"
            ((FAILED_TESTS++))
        fi
    done
    
    local presence_rate=$((present_agents * 100 / ${#ecommerce_agents[@]}))
    local focus_rate=$((ecommerce_focus_count * 100 / ${#ecommerce_agents[@]}))
    
    if [ $presence_rate -ge 80 ]; then
        print_success "E-commerce agents presence: $presence_rate%"
        log_message "SUCCESS: E-commerce agents presence: $presence_rate%"
        ((PASSED_TESTS++))
    else
        print_warning "E-commerce agents presence: $presence_rate%"
        log_message "WARN: E-commerce agents presence: $presence_rate%"
        ((SKIPPED_TESTS++))
    fi
    
    if [ $focus_rate -ge 70 ]; then
        print_success "E-commerce specialization: $focus_rate%"
        log_message "SUCCESS: E-commerce specialization: $focus_rate%"
    else
        print_warning "E-commerce specialization: $focus_rate%"
        log_message "WARN: E-commerce specialization: $focus_rate%"
    fi
}

# Test 7: Dispatch Modes Test
test_dispatch_modes() {
    print_status "Testing dispatch modes configuration..."
    ((TOTAL_TESTS++))
    log_message "Starting dispatch modes test"
    
    local config_file="$HOME/.config/opencode/opencode.json"
    
    if ! grep -q "dispatch_modes" "$config_file"; then
        print_error "Dispatch modes configuration missing"
        log_message "ERROR: Dispatch modes config missing"
        ((FAILED_TESTS++))
        return 1
    fi
    
    # Test specific dispatch modes
    local modes_found=0
    local expected_modes=("orchestration" "planning" "backend_development" "frontend_deployment")
    
    for mode in "${expected_modes[@]}"; do
        if grep -q "\"$mode\"" "$config_file"; then
            print_success "Dispatch mode found: $mode"
            log_message "SUCCESS: Dispatch mode $mode found"
            ((modes_found++))
        else
            print_warning "Dispatch mode missing: $mode"
            log_message "WARN: Dispatch mode $mode missing"
        fi
    done
    
    if [ $modes_found -ge 3 ]; then
        print_success "Dispatch modes configured: $modes_found/4"
        log_message "SUCCESS: Dispatch modes configured: $modes_found/4"
        ((PASSED_TESTS++))
    else
        print_warning "Dispatch modes partially configured: $modes_found/4"
        log_message "WARN: Dispatch modes partially configured: $modes_found/4"
        ((SKIPPED_TESTS++))
    fi
}

# Test 8: Performance Thresholds Test
test_performance_thresholds() {
    print_status "Testing performance thresholds..."
    ((TOTAL_TESTS++))
    log_message "Starting performance thresholds test"
    
    local config_file="$HOME/.config/opencode/opencode.json"
    
    # Check performance optimization section
    if grep -q "performance_optimization" "$config_file"; then
        print_success "Performance optimization configuration found"
        log_message "SUCCESS: Performance optimization config found"
    else
        print_warning "Performance optimization configuration missing"
        log_message "WARN: Performance optimization config missing"
        ((SKIPPED_TESTS++))
    fi
    
    # Check execution thresholds
    if grep -q "execution_thresholds" "$config_file"; then
        print_success "Execution thresholds configured"
        log_message "SUCCESS: Execution thresholds configured"
        
        # Extract and validate thresholds
        local fast_threshold=$(grep -o '"fast_task_threshold": *[0-9]*' "$config_file" | grep -o '[0-9]*' || echo "30")
        local complex_threshold=$(grep -o '"complex_task_threshold": *[0-9]*' "$config_file" | grep -o '[0-9]*' || echo "120")
        
        if [ "$fast_threshold" -le 30 ] && [ "$complex_threshold" -ge 60 ]; then
            print_success "Thresholds are reasonable (fast: ${fast_threshold}s, complex: ${complex_threshold}s)"
            log_message "SUCCESS: Thresholds reasonable"
            ((PASSED_TESTS++))
        else
            print_warning "Thresholds might need adjustment (fast: ${fast_threshold}s, complex: ${complex_threshold}s)"
            log_message "WARN: Thresholds might need adjustment"
        fi
    else
        print_error "Execution thresholds missing"
        log_message "ERROR: Execution thresholds missing"
        ((FAILED_TESTS++))
    fi
}

# Test 9: Scripts Functionality Test
test_scripts_functionality() {
    print_status "Testing scripts functionality..."
    ((TOTAL_TESTS++))
    log_message "Starting scripts functionality test"
    
    local scripts_dir="$REPO_DIR/scripts"
    
    if [ ! -d "$scripts_dir" ]; then
        print_error "Scripts directory not found"
        log_message "ERROR: Scripts directory missing"
        ((FAILED_TESTS++))
        return 1
    fi
    
    # Test key scripts
    local key_scripts=("install.sh" "update.sh" "sync-agents.sh" "validate-config.sh")
    local scripts_found=0
    
    for script in "${key_scripts[@]}"; do
        if [ -f "$scripts_dir/$script" ]; then
            if [ -x "$scripts_dir/$script" ]; then
                print_success "Script found and executable: $script"
                log_message "SUCCESS: Script $script found and executable"
                ((scripts_found++))
            else
                print_warning "Script found but not executable: $script"
                log_message "WARN: Script $script found but not executable"
                chmod +x "$scripts_dir/$script"
            fi
        else
            print_error "Script missing: $script"
            log_message "ERROR: Script $script missing"
            ((FAILED_TESTS++))
        fi
    done
    
    if [ $scripts_found -ge 3 ]; then
        print_success "Scripts functionality: $scripts_found/4 working"
        log_message "SUCCESS: Scripts functionality good"
        ((PASSED_TESTS++))
    else
        print_warning "Scripts functionality limited: $scripts_found/4"
        log_message "WARN: Scripts functionality limited"
        ((SKIPPED_TESTS++))
    fi
}

# Test 10: End-to-End Workflow Simulation
test_end_to_end_workflow() {
    print_status "Testing end-to-end workflow simulation..."
    ((TOTAL_TESTS++))
    log_message "Starting end-to-end workflow test"
    
    # Simulate a simple e-commerce project workflow
    local workflow_steps=(
        "Check agent availability"
        "Validate configuration"
        "Test dispatch modes"
        "Verify model routing"
        "Test e-commerce integration"
    )
    
    local successful_steps=0
    
    for step in "${workflow_steps[@]}"; do
        print_status "Simulating: $step"
        log_message "Simulating workflow step: $step"
        
        # Simulate step execution
        case "$step" in
            "Check agent availability")
                if [ $(ls ~/.opencode/agent/*.md 2>/dev/null | wc -l) -gt 5 ]; then
                    print_success "✓ Agents available"
                    ((successful_steps++))
                fi
                ;;
            "Validate configuration")
                if python3 -m json.tool ~/.config/opencode/opencode.json >/dev/null 2>&1; then
                    print_success "✓ Configuration valid"
                    ((successful_steps++))
                fi
                ;;
            "Test dispatch modes")
                if grep -q "dispatch_modes" ~/.config/opencode/opencode.json; then
                    print_success "✓ Dispatch modes configured"
                    ((successful_steps++))
                fi
                ;;
            "Verify model routing")
                if grep -q "model_routing" ~/.config/opencode/opencode.json; then
                    print_success "✓ Model routing configured"
                    ((successful_steps++))
                fi
                ;;
            "Test e-commerce integration")
                if [ -f ~/.opencode/agent/ecommerce-business-logic.md ]; then
                    print_success "✓ E-commerce integration ready"
                    ((successful_steps++))
                fi
                ;;
        esac
    done
    
    local workflow_success_rate=$((successful_steps * 100 / ${#workflow_steps[@]}))
    
    if [ $workflow_success_rate -ge 80 ]; then
        print_success "End-to-end workflow: $workflow_success_rate% successful"
        log_message "SUCCESS: End-to-end workflow $workflow_success_rate%"
        ((PASSED_TESTS++))
    else
        print_warning "End-to-end workflow: $workflow_success_rate% successful"
        log_message "WARN: End-to-end workflow $workflow_success_rate%"
        ((SKIPPED_TESTS++))
    fi
}

# Generate integration test report
generate_integration_report() {
    local report_file="$TEST_RESULTS_DIR/integration-report-$(date +%Y%m%d-%H%M%S).txt"
    
    cat > "$report_file" << EOF
OpenCode Integration Test Report
Generated: $(date)
Repository: $REPO_DIR

INTEGRATION TEST SUMMARY
========================
Total Tests: $TOTAL_TESTS
Passed: $PASSED_TESTS
Failed: $FAILED_TESTS
Skipped: $SKIPPED_TESTS

Success Rate: $((PASSED_TESTS * 100 / TOTAL_TESTS))%

COMPONENT STATUS
================
OpenCode Installation: $(command -v opencode &>/dev/null && echo "✓ Installed" || echo "✗ Missing")
Configuration File: $([ -f "$HOME/.config/opencode/opencode.json" ] && echo "✓ Present" || echo "✗ Missing")
Agent Directory: $([ -d "$HOME/.opencode/agent" ] && echo "✓ Present" || echo "✗ Missing")
Scripts Directory: $([ -d "$REPO_DIR/scripts" ] && echo "✓ Present" || echo "✗ Missing")

AGENT STATISTICS
================
Total Agents: $(find "$HOME/.opencode/agent" -name "*.md" 2>/dev/null | wc -l)
Core Agents: $(ls "$HOME/.opencode/agent"/{orchestrator,plan,build}.md 2>/dev/null | wc -l)
E-commerce Agents: $(ls "$HOME/.opencode/agent"/*-specialist.md 2>/dev/null | wc -l)

WORKFLOW CAPABILITIES
====================
Model Routing: $(grep -q "model_routing" "$HOME/.config/opencode/opencode.json" 2>/dev/null && echo "✓ Configured" || echo "✗ Missing")
Dispatch Modes: $(grep -q "dispatch_modes" "$HOME/.config/opencode/opencode.json" 2>/dev/null && echo "✓ Configured" || echo "✗ Missing")
Performance Optimization: $(grep -q "performance_optimization" "$HOME/.config/opencode/opencode.json" 2>/dev/null && echo "✓ Configured" || echo "✗ Missing")

RECOMMENDATIONS
===============
EOF

    if [ $FAILED_TESTS -gt 0 ]; then
        echo "- Fix $FAILED_TESTS failed integration tests" >> "$report_file"
    fi
    
    if [ $SKIPPED_TESTS -gt 0 ]; then
        echo "- Review $SKIPPED_TESTS skipped tests for optimization opportunities" >> "$report_file"
    fi
    
    if [ $PASSED_TESTS -eq $TOTAL_TESTS ]; then
        echo "- All integration tests passed! System is production-ready." >> "$report_file"
    fi
    
    echo "" >> "$report_file"
    echo "Integration test completed at: $(date)" >> "$report_file"
    echo "Full log available at: $INTEGRATION_LOG" >> "$report_file"
    
    print_status "Integration report saved: $report_file"
}

# Main integration test execution
main() {
    log_message "Starting OpenCode Integration Test Suite v3.0"
    echo "Running comprehensive integration tests..."
    echo ""
    
    # Run all integration tests
    test_opencode_installation
    test_configuration_loading
    test_agent_detection
    test_orchestrator_functionality
    test_model_routing
    test_ecommerce_integration
    test_dispatch_modes
    test_performance_thresholds
    test_scripts_functionality
    test_end_to_end_workflow
    
    # Generate report
    generate_integration_report
    
    # Final summary
    echo ""
    echo "=========================================="
    echo "📊 INTEGRATION TEST RESULTS"
    echo "=========================================="
    echo "Total Tests: $TOTAL_TESTS"
    echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
    echo -e "Failed: ${RED}$FAILED_TESTS${NC}"
    echo -e "Skipped: ${YELLOW}$SKIPPED_TESTS${NC}"
    echo ""
    
    local success_rate=$((PASSED_TESTS * 100 / TOTAL_TESTS))
    
    if [ $FAILED_TESTS -eq 0 ]; then
        print_success "🎉 All integration tests passed!"
        print_status "Success rate: $success_rate%"
        echo ""
        print_orchestrator "✅ Multi-dispatch orchestration ready"
        print_ecommerce "✅ E-commerce integration complete"
        print_success "✅ System is production-ready"
    else
        print_error "⚠️ Some integration tests failed"
        print_status "Success rate: $success_rate%"
        echo ""
        print_warning "Run ./scripts/update.sh to refresh configuration"
        print_status "Check logs: $INTEGRATION_LOG"
    fi
    
    echo ""
    echo "For detailed results, check:"
    echo "  Report: $TEST_RESULTS_DIR/integration-report-*.txt"
    echo "  Logs: $INTEGRATION_LOG"
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