#!/usr/bin/env bash

# Smart-term Update Script
# Updates an existing smart-term installation to the latest version
# Usage: ./update.sh [--yes|-y]  (skip confirmation)

set -e

# Check for --yes flag
AUTO_YES=false
if [[ "$1" == "--yes" ]] || [[ "$1" == "-y" ]]; then
    AUTO_YES=true
fi

# If piped (not interactive), auto-confirm
if [[ ! -t 0 ]]; then
    AUTO_YES=true
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="$HOME/.smart-term"

# Print functions
print_header() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║                                                       ║"
    echo "║           Smart-term Update Script                    ║"
    echo "║                                                       ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if smart-term is installed
check_installation() {
    if [[ ! -d "$INSTALL_DIR" ]]; then
        print_error "Smart-term is not installed at $INSTALL_DIR"
        echo ""
        echo "To install smart-term, run:"
        echo "  curl -fsSL https://raw.githubusercontent.com/Lusan-sapkota/smart-term/main/install.sh | bash"
        exit 1
    fi
    
    if [[ ! -d "$INSTALL_DIR/.git" ]]; then
        print_error "Installation directory exists but is not a git repository"
        echo ""
        echo "Please reinstall smart-term using:"
        echo "  curl -fsSL https://raw.githubusercontent.com/Lusan-sapkota/smart-term/main/install.sh | bash"
        exit 1
    fi
}

# Main update process
main() {
    print_header
    
    print_info "Checking installation..."
    check_installation
    print_success "Installation found at $INSTALL_DIR"
    
    # Navigate to install directory
    cd "$INSTALL_DIR"
    
    # Check current version/commit
    print_info "Current version:"
    git log -1 --oneline
    echo ""
    
    # Fetch latest changes
    print_info "Fetching latest changes from GitHub..."
    git fetch origin main
    
    # Check if updates are available
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse origin/main)
    
    if [[ "$LOCAL" == "$REMOTE" ]]; then
        print_success "Already up to date!"
        echo ""
        echo "You're running the latest version of smart-term."
        exit 0
    fi
    
    # Show what will be updated
    print_info "Updates available:"
    echo ""
    git log --oneline HEAD..origin/main
    echo ""
    
    # Ask for confirmation (unless auto-confirmed)
    if [[ "$AUTO_YES" == false ]]; then
        read -p "Do you want to update? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_warning "Update cancelled"
            exit 0
        fi
    else
        print_info "Auto-updating (piped mode)..."
    fi
    
    # Stash any local changes
    if [[ -n $(git status -s) ]]; then
        print_info "Stashing local changes..."
        git stash
    fi
    
    # Pull latest changes
    print_info "Pulling latest changes..."
    git pull origin main
    
    # Activate virtual environment
    print_info "Activating virtual environment..."
    source venv/bin/activate
    
    # Update dependencies
    print_info "Updating dependencies..."
    pip install --upgrade pip >/dev/null 2>&1
    pip install -e . >/dev/null 2>&1
    
    # Update complete
    echo ""
    echo -e "${GREEN}"
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║                                                       ║"
    echo "║          Update Complete! 🎉                          ║"
    echo "║                                                       ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    
    print_info "Updated to version:"
    git log -1 --oneline
    echo ""
    
    print_success "Smart-term has been updated successfully!"
    echo ""
    echo "Try it out:"
    echo "  ai 'What's new in this update?'"
    echo ""
}

# Run main update
main
