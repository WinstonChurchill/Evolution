#!/bin/bash

# Stop script execution on any error
set -e

echo "=== Starting project deployment ==="

# Get the parent directory of the script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ProjectRoot="$(dirname "$SCRIPT_DIR")"

pythonValid=false
pythonCmd=""

# Check if python3 is available
if command -v python3 &> /dev/null; then
    # Get major and minor version
    version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    
    # Check if version is >= 3.12 (using bc for float comparison)
    if echo "$version >= 3.12" | bc -l &> /dev/null 2>&1 || [ "$(echo "$version" | tr -d '.')" -ge 312 ] 2>/dev/null; then
        pythonValid=true
        pythonCmd="python3"
        echo -e "Found compatible system Python version: $version\n"
    fi
fi

# If Python is missing or outdated
if [ "$pythonValid" = false ]; then
    echo -e "[ERROR] Python 3.12+ not found in the system."
    echo "Please install Python 3.12 or higher using your package manager."
    echo "Example (Ubuntu/Debian): sudo apt update && sudo apt install python3.12 python3.12-venv"
    exit 1
fi

# Create an isolated virtual environment (.venv)
echo "Checking for .venv virtual environment..."
if [ -d "$ProjectRoot/.venv" ]; then
    echo -e "Virtual environment detected.\n"
else
    echo -e "Virtual environment not found.\nCreating .venv..."
    
    # Try to create venv, catch error if python3-venv package is missing on Ubuntu/Debian
    if ! $pythonCmd -m venv "$ProjectRoot/.venv"; then
        echo -e "\n[ERROR] Failed to create virtual environment."
        echo "You might be missing the venv component."
        echo "Try running: sudo apt install python3-venv"
        exit 1
    fi
    echo -e "Environment created successfully\n"
fi

# Upgrade pip and install libraries INSIDE .venv
echo "Upgrading pip and installing dependencies..."
"$ProjectRoot/.venv/bin/python" -m pip install --upgrade pip

echo "Attempting to install the project package..."
if "$ProjectRoot/.venv/bin/python" -m pip install "$ProjectRoot"; then
    echo "Project package installed successfully."
else
    echo -e "\n[ERROR] Project deployment failed during package installation."
    echo -e "Please check your pyproject.toml configuration and file layout.\n"
    echo "Deployment halted: pip install . failed to execute successfully."
    exit 1