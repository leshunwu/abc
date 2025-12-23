#!/usr/bin/env python3
"""
ABC GUI - A simple graphical user interface for the ABC tool
(System for Sequential Logic Synthesis and Formal Verification)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import subprocess
import os
import threading
import shlex

class AbcGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ABC - Sequential Logic Synthesis Tool")
        self.root.geometry("900x700")
        
        # Get ABC executable path
        self.abc_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "abc")
        if not os.path.exists(self.abc_path):
            self.abc_path = "abc"  # Try system PATH
        
        self.current_file = None
        self.create_widgets()
        
    def create_widgets(self):
        """Create the GUI components"""
        
        # Menu Bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open File...", command=self.load_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="ABC Help", command=self.show_help)
        
        # Top Frame - File Info
        top_frame = ttk.Frame(self.root, padding="5")
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="Current File:").pack(side=tk.LEFT)
        self.file_label = ttk.Label(top_frame, text="No file loaded", foreground="gray")
        self.file_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(top_frame, text="Load File", command=self.load_file).pack(side=tk.RIGHT, padx=2)
        
        # Command Frame
        cmd_frame = ttk.LabelFrame(self.root, text="ABC Commands", padding="10")
        cmd_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=5)
        
        # Command entry
        ttk.Label(cmd_frame, text="Command:").pack(side=tk.LEFT)
        self.command_entry = ttk.Entry(cmd_frame, width=60)
        self.command_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.command_entry.bind('<Return>', lambda e: self.execute_command())
        
        ttk.Button(cmd_frame, text="Execute", command=self.execute_command).pack(side=tk.LEFT, padx=2)
        ttk.Button(cmd_frame, text="Clear", command=self.clear_output).pack(side=tk.LEFT, padx=2)
        
        # Quick Actions Frame
        actions_frame = ttk.LabelFrame(self.root, text="Quick Actions", padding="5")
        actions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        quick_commands = [
            ("Print Stats", "ps"),
            ("Balance", "b"),
            ("Rewrite", "rw"),
            ("Rewrite -z", "rw -z"),
            ("Refactor", "rf"),
            ("Refactor -z", "rf -z"),
            ("Help", "help"),
        ]
        
        for i, (label, cmd) in enumerate(quick_commands):
            btn = ttk.Button(actions_frame, text=label, 
                           command=lambda c=cmd: self.quick_execute(c))
            btn.pack(side=tk.LEFT, padx=2)
        
        # Output Frame
        output_frame = ttk.LabelFrame(self.root, text="Output", padding="5")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, 
                                                     height=20, font=("Courier", 10))
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Status Bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Initial message
        self.append_output("ABC GUI initialized. Load a file or enter commands.\n")
        self.append_output("Supported file formats: .aig, .blif, .bench, .pla, .v\n\n")
        
    def load_file(self):
        """Open file dialog and load a file"""
        filetypes = [
            ("All Supported", "*.aig *.blif *.bench *.pla *.v"),
            ("AIGER files", "*.aig"),
            ("BLIF files", "*.blif"),
            ("Bench files", "*.bench"),
            ("PLA files", "*.pla"),
            ("Verilog files", "*.v"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(title="Select a file", filetypes=filetypes)
        
        if filename:
            self.current_file = filename
            self.file_label.config(text=os.path.basename(filename), foreground="black")
            
            # Determine read command based on file extension
            # Using shlex.quote for safety, though subprocess list format already protects us
            safe_filename = shlex.quote(filename)
            ext = os.path.splitext(filename)[1].lower()
            if ext == '.aig':
                cmd = f"read {safe_filename}"
            elif ext == '.blif':
                cmd = f"read_blif {safe_filename}"
            elif ext == '.bench':
                cmd = f"read_bench {safe_filename}"
            elif ext == '.pla':
                cmd = f"read_pla {safe_filename}"
            elif ext == '.v':
                cmd = f"read_verilog {safe_filename}"
            else:
                cmd = f"read {safe_filename}"
            
            self.append_output(f"\n=== Loading file: {os.path.basename(filename)} ===\n")
            self.execute_abc_command(cmd)
            self.execute_abc_command("ps")  # Show stats after loading
            
    def quick_execute(self, command):
        """Execute a quick command"""
        self.command_entry.delete(0, tk.END)
        self.command_entry.insert(0, command)
        self.execute_command()
        
    def execute_command(self):
        """Execute the command entered in the entry field"""
        command = self.command_entry.get().strip()
        if command:
            self.append_output(f"\nabc> {command}\n")
            self.execute_abc_command(command)
            
    def execute_abc_command(self, command):
        """Execute ABC command in a separate thread"""
        self.status_bar.config(text="Executing...")
        
        def run_command():
            try:
                # Build the command - check if command starts with specific keywords
                command_parts = command.strip().split()
                first_cmd = command_parts[0] if command_parts else ""
                
                # Build the command string
                if self.current_file and first_cmd not in ['read', 'read_blif', 'read_bench', 'read_pla', 'read_verilog', 'write', 'write_blif', 'write_verilog', 'help']:
                    # For commands that need a loaded file, use shlex.quote for safety
                    safe_filename = shlex.quote(self.current_file)
                    abc_cmd = f"read {safe_filename}; {command}"
                else:
                    abc_cmd = command
                
                # Execute the command safely using list format to avoid shell injection
                process = subprocess.Popen([self.abc_path, "-c", abc_cmd], 
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE,
                                         text=True)
                stdout, stderr = process.communicate(timeout=30)
                
                # Display output
                if stdout:
                    self.root.after(0, self.append_output, stdout)
                if stderr:
                    self.root.after(0, self.append_output, f"Error: {stderr}\n")
                    
                self.root.after(0, self.status_bar.config, {"text": "Ready"})
                
            except subprocess.TimeoutExpired:
                self.root.after(0, self.append_output, "\nError: Command timed out\n")
                self.root.after(0, self.status_bar.config, {"text": "Timeout"})
            except Exception as e:
                self.root.after(0, self.append_output, f"\nError: {str(e)}\n")
                self.root.after(0, self.status_bar.config, {"text": "Error"})
        
        # Run in separate thread to avoid blocking GUI
        thread = threading.Thread(target=run_command, daemon=True)
        thread.start()
        
    def append_output(self, text):
        """Append text to the output window"""
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        
    def clear_output(self):
        """Clear the output window"""
        self.output_text.delete(1.0, tk.END)
        
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About ABC GUI",
                          "ABC GUI v1.0\n\n"
                          "A simple graphical interface for ABC:\n"
                          "System for Sequential Logic Synthesis\n"
                          "and Formal Verification\n\n"
                          "ABC is maintained by Alan Mishchenko\n"
                          "at UC Berkeley")
        
    def show_help(self):
        """Show ABC help"""
        self.append_output("\n=== ABC Help ===\n")
        self.execute_abc_command("help")

def main():
    """Main entry point"""
    root = tk.Tk()
    app = AbcGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
