#!/bin/bash
#
# Solana MCP Server Setup Script for Linux/macOS
#

# --- Configuration ---
PYTHON_CMD="python3"
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
ENV_FILE=".env"
ENV_EXAMPLE_FILE=".env.example"

# --- Colors for output ---
C_RESET='\033[0m'
C_RED='\033[0;31m'
C_GREEN='\033[0;32m'
C_YELLOW='\033[0;33m'
C_BLUE='\033[0;34m'

# --- Helper Functions ---
echo_info() {
    echo -e "${C_BLUE}INFO: $1${C_RESET}"
}
echo_success() {
    echo -e "${C_GREEN}SUCCESS: $1${C_RESET}"
}
echo_warn() {
    echo -e "${C_YELLOW}WARN: $1${C_RESET}"
}
echo_error() {
    echo -e "${C_RED}ERROR: $1${C_RESET}"
}

# --- Main Script ---

# 1. Check for Python 3
echo_info "Checking for Python 3..."
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo_error "Python 3 is not installed or not in PATH. Please install Python 3 to continue."
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo_info "Found Python version: $PYTHON_VERSION"

# 2. Create virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo_info "Creating Python virtual environment in '$VENV_DIR'..."
    $PYTHON_CMD -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo_error "Failed to create virtual environment."
        exit 1
    fi
    echo_success "Virtual environment created."
else
    echo_info "Virtual environment '$VENV_DIR' already exists."
fi

# 3. Activate virtual environment and install dependencies
echo_info "Activating virtual environment and installing dependencies..."
source $VENV_DIR/bin/activate

# Upgrade pip
$VENV_DIR/bin/python -m pip install --upgrade pip > /dev/null

# Install from requirements.txt
if [ -f "$REQUIREMENTS_FILE" ]; then
    $VENV_DIR/bin/pip install -r $REQUIREMENTS_FILE
    if [ $? -ne 0 ]; then
        echo_error "Failed to install dependencies from $REQUIREMENTS_FILE."
        deactivate
        exit 1
    fi
    echo_success "Dependencies installed successfully."
else
    echo_warn "$REQUIREMENTS_FILE not found. Skipping dependency installation."
fi

# 4. Create .env file
if [ ! -f "$ENV_FILE" ]; then
    if [ -f "$ENV_EXAMPLE_FILE" ]; then
        echo_info "Creating .env file from $ENV_EXAMPLE_FILE..."
        cp $ENV_EXAMPLE_FILE $ENV_FILE
        echo_success ".env file created. Please review and edit it with your settings."
    else
        echo_warn "$ENV_EXAMPLE_FILE not found. Cannot create .env file."
    fi
else
    echo_info ".env file already exists. Skipping creation."
fi

# Deactivate virtual environment
deactivate

# --- Final Instructions ---
echo_info "-----------------------------------------------------"
echo_success "Setup complete!"
echo_info "To run the MCP server, use the following command:"
echo -e "  ${C_YELLOW}./run.sh${C_RESET}"

echo_info "To run the example script:"
echo -e "  ${C_YELLOW}source venv/bin/activate${C_RESET}"
echo -e "  ${C_YELLOW}python examples.py${C_RESET}"
echo -e "  ${C_YELLOW}deactivate${C_RESET}"

echo_warn "Remember to configure your .env file before running the server."