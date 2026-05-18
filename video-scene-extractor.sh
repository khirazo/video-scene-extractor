#!/bin/bash
# This file includes AI-generated code - Review and modify as needed

# Video Scene Extractor - Wrapper Script
# This script automatically activates the virtual environment and runs the tool

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Path to virtual environment
VENV_DIR="$SCRIPT_DIR/venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR"
    echo "Please run the setup script first:"
    echo "  ./setup.sh"
    exit 1
fi

# Check if Python is available in venv
if [ ! -f "$VENV_DIR/bin/python" ]; then
    echo "Error: Python not found in virtual environment"
    echo "Please reinstall the virtual environment"
    exit 1
fi

# Activate virtual environment and run the command
source "$VENV_DIR/bin/activate"

# Run video-scene-extractor with all arguments passed to this script
video-scene-extractor "$@"

# Capture exit code
EXIT_CODE=$?

# Deactivate virtual environment
deactivate

# Exit with the same code as the Python script
exit $EXIT_CODE

# Made with Bob
