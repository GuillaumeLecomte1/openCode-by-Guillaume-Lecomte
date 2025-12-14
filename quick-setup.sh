#!/bin/bash

# Quick Setup - Ultra Simple One Command Setup
# Usage: curl -fsSL https://raw.githubusercontent.com/GuillaumeLecomte1/openCode-by-Guillaume-Lecomte/main/quick-setup.sh | bash

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_status() { echo -e "${BLUE}ℹ️  $1${NC}"; }

echo "🚀 OpenCode E-commerce Setup - Quick Install"
echo "============================================"
echo ""

# Check prerequisites
print_status "Checking prerequisites..."

# Check git
if ! command -v git &> /dev/null; then
    print_error "Git is required but not installed"
    echo "Please install Git first:"
    echo "  Ubuntu/Debian: sudo apt install git"
    echo "  macOS: brew install git"
    echo "  Windows: Install from https://git-scm.com/"
    exit 1
fi
print_success "Git found"

# Check curl
if ! command -v curl &> /dev/null; then
    print_error "curl is required but not installed"
    exit 1
fi
print_success "curl found"

# Clone repository if not exists
if [ ! -d "openCode-by-Guillaume-Lecomte" ]; then
    print_status "Cloning repository..."
    git clone https://github.com/GuillaumeLecomte1/openCode-by-Guillaume-Lecomte.git
    print_success "Repository cloned"
else
    print_status "Repository already exists, updating..."
    cd openCode-by-Guillaume-Lecomte
    git pull origin main 2>/dev/null || true
    cd ..
fi

# Run the setup
cd openCode-by-Guillaume-Lecomte
chmod +x install.sh
./install.sh

echo ""
print_success "🎉 Setup completed! Open your terminal and run: opencode"