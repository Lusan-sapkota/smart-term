#!/usr/bin/env bash

# Smart-term AI CLI - One-line Installation Script
# Usage: curl -fsSL https://raw.githubusercontent.com/YOUR_REPO/main/install.sh | bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="$HOME/.smart-term"
BIN_DIR="$HOME/.local/bin"
CONFIG_FILE="$HOME/.ai_cli_config.json"
REPO_URL="https://github.com/Lusan-sapkota/smart-term.git"

# Print functions
print_header() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║                                                       ║"
    echo "║           Smart-term AI CLI Installer                 ║"
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

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

# Install Python if needed
install_python() {
    local os=$(detect_os)
    
    if command_exists python3; then
        print_success "Python3 is already installed"
        return 0
    fi
    
    print_info "Python3 not found. Installing..."
    
    if [[ "$os" == "macos" ]]; then
        if command_exists brew; then
            brew install python3
        else
            print_error "Homebrew not found. Please install Python3 manually from https://www.python.org/"
            exit 1
        fi
    elif [[ "$os" == "linux" ]]; then
        if command_exists apt-get; then
            sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv
        elif command_exists yum; then
            sudo yum install -y python3 python3-pip
        elif command_exists dnf; then
            sudo dnf install -y python3 python3-pip
        else
            print_error "Package manager not found. Please install Python3 manually."
            exit 1
        fi
    else
        print_error "Unsupported OS. Please install Python3 manually."
        exit 1
    fi
    
    print_success "Python3 installed successfully"
}

# Install git if needed
install_git() {
    if command_exists git; then
        print_success "Git is already installed"
        return 0
    fi
    
    print_info "Git not found. Installing..."
    local os=$(detect_os)
    
    if [[ "$os" == "macos" ]]; then
        if command_exists brew; then
            brew install git
        else
            print_error "Homebrew not found. Please install Git manually."
            exit 1
        fi
    elif [[ "$os" == "linux" ]]; then
        if command_exists apt-get; then
            sudo apt-get update && sudo apt-get install -y git
        elif command_exists yum; then
            sudo yum install -y git
        elif command_exists dnf; then
            sudo dnf install -y git
        else
            print_error "Package manager not found. Please install Git manually."
            exit 1
        fi
    fi
    
    print_success "Git installed successfully"
}

# Prompt for API key
prompt_api_key() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}API Key Setup${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Smart-term requires a Perplexity API key to function."
    echo "Get your free API key at: https://www.perplexity.ai/settings/api"
    echo ""
    
    read -p "Enter your Perplexity API key (or press Enter to skip): " api_key
    
    if [[ -n "$api_key" ]]; then
        # Create .env file in install directory
        echo "PERPLEXITY_API_KEY=$api_key" > "$INSTALL_DIR/.env"
        print_success "API key saved to $INSTALL_DIR/.env"
        return 0
    else
        print_warning "Skipped API key setup. You'll need to set PERPLEXITY_API_KEY environment variable later."
        echo ""
        echo "To set it up later, add this to your ~/.bashrc or ~/.zshrc:"
        echo "  export PERPLEXITY_API_KEY='your-api-key-here'"
        echo ""
        echo "Or create a .env file at: $INSTALL_DIR/.env"
        return 1
    fi
}

# Main installation
main() {
    print_header
    
    # Check prerequisites
    print_info "Checking prerequisites..."
    install_python
    install_git
    
    # Create directories
    print_info "Creating installation directories..."
    mkdir -p "$BIN_DIR"
    mkdir -p "$INSTALL_DIR"
    
    # Clone or update repository
    if [[ -d "$INSTALL_DIR/.git" ]]; then
        print_info "Updating existing installation..."
        cd "$INSTALL_DIR"
        git pull origin main
    else
        print_info "Downloading smart-term..."
        rm -rf "$INSTALL_DIR"
        git clone "$REPO_URL" "$INSTALL_DIR"
    fi
    
    cd "$INSTALL_DIR"
    
    # Create virtual environment
    print_info "Setting up Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    
    # Install dependencies
    print_info "Installing dependencies..."
    pip install --upgrade pip >/dev/null 2>&1
    pip install -e . >/dev/null 2>&1
    
    # Create wrapper script
    print_info "Creating command wrapper..."
    cat > "$BIN_DIR/ai" << 'EOF'
#!/usr/bin/env bash
# Smart-term AI CLI wrapper script

INSTALL_DIR="$HOME/.smart-term"

# Activate virtual environment and run
source "$INSTALL_DIR/venv/bin/activate"
cd "$INSTALL_DIR"
python3 -m smart_term.main "$@"
EOF
    
    chmod +x "$BIN_DIR/ai"
    
    # Prompt for API key
    prompt_api_key
    
    # Create default config if it doesn't exist
    if [[ ! -f "$CONFIG_FILE" ]]; then
        print_info "Creating default configuration..."
        cat > "$CONFIG_FILE" << 'EOF'
{
  "default_model": "sonar",
  "default_provider": "perplexity",
  "timeout": 30,
  "max_file_size_mb": 10,
  "output_format": "markdown",
  "show_thinking_animation": true,
  "log_level": "INFO"
}
EOF
        print_success "Configuration created at $CONFIG_FILE"
    fi
    
    # Add to PATH if needed
    echo ""
    print_info "Checking PATH configuration..."
    
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        print_warning "$BIN_DIR is not in your PATH"
        
        # Detect shell
        if [[ -n "$ZSH_VERSION" ]] || [[ "$SHELL" == *"zsh"* ]]; then
            SHELL_RC="$HOME/.zshrc"
        else
            SHELL_RC="$HOME/.bashrc"
        fi
        
        echo ""
        echo "Add this line to your $SHELL_RC:"
        echo -e "${GREEN}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
        echo ""
        
        read -p "Would you like me to add it automatically? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "" >> "$SHELL_RC"
            echo "# Smart-term AI CLI" >> "$SHELL_RC"
            echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_RC"
            print_success "Added to $SHELL_RC"
            print_warning "Please run: source $SHELL_RC"
        fi
    else
        print_success "$BIN_DIR is already in your PATH"
    fi
    
    # Installation complete
    echo ""
    echo -e "${GREEN}"
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║                                                       ║"
    echo "║          Installation Complete! 🎉                    ║"
    echo "║                                                       ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo -e "${CYAN}Quick Start:${NC}"
    echo ""
    echo "  Try these commands:"
    echo -e "    ${GREEN}ai 'What is the capital of France?'${NC}"
    echo -e "    ${GREEN}ai document.pdf 'Summarize this' --p${NC}"
    echo -e "    ${GREEN}ai image.png 'What is in this image?'${NC}"
    echo ""
    echo -e "${CYAN}Model Flags:${NC}"
    echo "    --s      Fast general-purpose (default)"
    echo "    --p      Enhanced reasoning"
    echo "    --r      Advanced reasoning"
    echo "    --deep   Deep research"
    echo ""
    echo -e "${CYAN}Configuration:${NC}"
    echo "    Config file: $CONFIG_FILE"
    echo "    Install dir: $INSTALL_DIR"
    echo ""
    
    if [[ ! -f "$INSTALL_DIR/.env" ]]; then
        echo -e "${YELLOW}⚠ Remember to set your API key:${NC}"
        echo "    export PERPLEXITY_API_KEY='your-key-here'"
        echo ""
    fi
    
    echo "For more info: https://github.com/Lusan-sapkota/smart-term"
    echo ""
}

# Run main installation
main
