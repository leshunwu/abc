#!/bin/bash
# Launcher script for ABC GUI

# Check if Makefile exists
if [ ! -f "./Makefile" ]; then
    echo "Error: Makefile not found. Are you in the ABC root directory?"
    exit 1
fi

# Check if ABC is built
if [ ! -f "./abc" ]; then
    echo "ABC binary not found. Building ABC..."
    if ! make ABC_USE_NO_READLINE=1; then
        echo "Failed to build ABC."
        echo "Please check the error messages above and try building manually with 'make'."
        exit 1
    fi
    echo "ABC built successfully."
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check if tkinter is available
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: Python tkinter module is required but not installed."
    echo "Please install it using:"
    echo "  - Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  - Fedora/RHEL: sudo dnf install python3-tkinter"
    echo "  - macOS: tkinter should be included with Python"
    exit 1
fi

# Launch the GUI
echo "Launching ABC GUI..."
python3 abc_gui.py
