#!/bin/bash
# Launcher script for ABC GUI

# Check if ABC is built
if [ ! -f "./abc" ]; then
    echo "ABC binary not found. Building ABC..."
    make ABC_USE_NO_READLINE=1
    if [ $? -ne 0 ]; then
        echo "Failed to build ABC. Please run 'make' manually."
        exit 1
    fi
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed."
    exit 1
fi

# Check if tkinter is available
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Python tkinter module is required but not installed."
    echo "Please install it using:"
    echo "  - Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  - Fedora/RHEL: sudo dnf install python3-tkinter"
    echo "  - macOS: tkinter should be included with Python"
    exit 1
fi

# Launch the GUI
echo "Launching ABC GUI..."
python3 abc_gui.py
