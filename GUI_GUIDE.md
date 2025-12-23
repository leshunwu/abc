# ABC GUI - User Guide

## Overview

The ABC GUI provides a graphical interface for the ABC tool (System for Sequential Logic Synthesis and Formal Verification). It simplifies interaction with ABC by providing an intuitive interface for loading files, executing commands, and viewing results.

## Features

- **File Loading**: Support for AIGER (.aig), BLIF (.blif), Bench (.bench), PLA (.pla), and Verilog (.v) files
- **Command Execution**: Execute any ABC command with immediate feedback
- **Quick Actions**: One-click access to commonly used commands
- **Output Display**: Scrollable output window with syntax highlighting
- **Status Bar**: Real-time status updates during command execution

## Installation

### Prerequisites

- Python 3.x (typically pre-installed on most systems)
- tkinter module (usually included with Python)
- ABC binary (compiled from source)

### Installation Steps

1. **Build ABC** (if not already built):
   ```bash
   make ABC_USE_NO_READLINE=1
   ```

2. **Verify Python and tkinter**:
   ```bash
   python3 --version
   python3 -c "import tkinter"
   ```

3. **If tkinter is not installed**:
   - Ubuntu/Debian: `sudo apt-get install python3-tk`
   - Fedora/RHEL: `sudo dnf install python3-tkinter`
   - macOS: tkinter is included with Python

## Usage

### Launching the GUI

Use the provided launcher script:
```bash
./launch_gui.sh
```

Or run directly:
```bash
python3 abc_gui.py
```

### Loading Files

1. Click "Load File" button or use File → Open File menu
2. Select a file with supported format (.aig, .blif, .bench, .pla, .v)
3. The file will be automatically loaded and statistics will be displayed

### Executing Commands

**Method 1: Command Entry**
1. Type a command in the "Command:" field
2. Press Enter or click "Execute" button
3. View results in the output window

**Method 2: Quick Actions**
- Click any of the quick action buttons for common operations:
  - **Print Stats** - Display current design statistics
  - **Balance** - Balance the AIG
  - **Rewrite** - Apply rewriting
  - **Refactor** - Apply refactoring
  - **Help** - Show ABC help

### Common Commands

- `ps` - Print statistics
- `b` - Balance the network
- `rw` - Rewrite the network
- `rf` - Refactor the network
- `help` - Show available commands
- `write_blif <file>` - Write network to BLIF file
- `write_verilog <file>` - Write network to Verilog file

## Example Workflow

1. **Load a file**:
   ```
   File → Open File → select i10.aig
   ```

2. **View initial statistics**:
   - Automatically displayed after loading

3. **Optimize the design**:
   - Click "Balance" button
   - Click "Rewrite" button
   - Enter `rw -l` for more aggressive rewriting

4. **View final statistics**:
   - Click "Print Stats" button

5. **Save results**:
   - Enter `write_blif output.blif` to save optimized design

## Tips

- Use the Clear button to clean the output window
- Commands are executed in the context of the currently loaded file
- Press Enter in the command field to quickly execute commands
- The status bar shows command execution progress

## Troubleshooting

**GUI doesn't start**:
- Check that Python 3 is installed: `python3 --version`
- Verify tkinter is available: `python3 -c "import tkinter"`
- Install tkinter if missing (see Installation section)

**ABC commands fail**:
- Ensure ABC binary is in the same directory as abc_gui.py
- Or ensure ABC is in your system PATH
- Try building ABC: `make ABC_USE_NO_READLINE=1`

**File won't load**:
- Check that the file format is supported
- Verify the file is not corrupted
- Check the output window for error messages

## Technical Details

- **Language**: Python 3
- **GUI Framework**: tkinter (standard library)
- **Threading**: Commands execute in separate threads to prevent GUI freezing
- **Timeout**: 30 seconds per command execution

## License

ABC GUI follows the same license as the ABC tool. See copyright.txt for details.
