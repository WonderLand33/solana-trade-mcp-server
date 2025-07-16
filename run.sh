#!/bin/bash
#
# Run script for Solana MCP Server on Linux/macOS
#

# --- Configuration ---
VENV_DIR="venv"
SERVER_SCRIPT="solana_mcp_server.py"
ENV_FILE=".env"

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
echo_error() {
    echo -e "${C_RED}ERROR: $1${C_RESET}"
}

# 1. Check for virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo_error "Virtual environment '$VENV_DIR' not found."
    echo_info "Please run the setup script first: ./setup.sh"
    exit 1
fi

# 2. Check for .env file
if [ ! -f "$ENV_FILE" ]; then
    echo_error "Configuration file '$ENV_FILE' not found."
    echo_info "Please run './setup.sh' or create '$ENV_FILE' manually."
    exit 1
fi

# 3. Activate virtual environment and run the server
echo_info "Activating virtual environment..."
source $VENV_DIR/bin/activate

echo_info "Starting Solana MCP Server..."
echo_info "Press Ctrl+C to stop the server."

$VENV_DIR/bin/python $SERVER_SCRIPT

# Deactivate on exit
deactivate
echo_info "Server stopped and virtual environment deactivated."