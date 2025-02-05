#!/bin/bash
# update_all.sh
# This script creates/updates all project files and then updates Git.

set -e  # exit immediately if a command exits with a non-zero status

# 1. Create/update .gitignore
cat << 'EOF' > .gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environment directories
venv/
env/
.env/

# OS-specific files
.DS_Store
Thumbs.db
EOF

# 2. Create/update LICENSE (using MIT License as an example)
cat << 'EOF' > LICENSE
MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# 3. Create/update README.md
cat << 'EOF' > README.md
# Nurdsem

**Nurdsem** is a NurdRage-themed placeholder text generator. It replaces each word in an input file with a cyclic token drawn from a custom placeholder text—while preserving the file's structure and capitalization.

## Features
- **GUI File Pickers:** Native dialogs for selecting input/output files when options are omitted.
- **Auto Dependency Helper:** Checks for and prompts installation of required dependencies.
- **Robust Error Handling:** Extensive error handling throughout the code.

## Installation

Clone the repository and install globally:
\`\`\`bash
git clone https://github.com/yourusername/nurdsem-ragesum.git nsem
cd nsem
pip install -e .
\`\`\`

This installs the global command \`nurdsem\`.

## Usage

Run from the command line:
\`\`\`bash
nurdsem --input path/to/input.txt --output path/to/output.txt
\`\`\`

If options are omitted, GUI dialogs will appear.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
EOF

# 4. Create/update requirements.txt
cat << 'EOF' > requirements.txt
regex
EOF

# 5. Create/update pyproject.toml
cat << 'EOF' > pyproject.toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
EOF

# 6. Create/update setup.py
cat << 'EOF' > setup.py
from setuptools import setup, find_packages

setup(
    name="nurdsem",
    version="0.1.0",
    description="A NurdRage-themed placeholder text generator with GUI file pickers and robust error handling.",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "regex",
    ],
    entry_points={
        "console_scripts": [
            "nurdsem = nurdsem.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
EOF

# 7. Create/update package files

# Create the package directory if it doesn't exist
mkdir -p nurdsem

# 7a. Create/update nurdsem/__init__.py (empty file)
cat << 'EOF' > nurdsem/__init__.py
# This file marks the directory as a Python package.
EOF

# 7b. Create/update nurdsem/main.py
cat << 'EOF' > nurdsem/main.py
#!/usr/bin/env python3
"""
Nurdsem: A NurdRage-themed placeholder text generator.

Replaces each word in an input file with a cyclic token from custom placeholder text,
preserving file structure and capitalization. Accepts input/output file options via CLI,
and uses GUI file pickers if omitted.
"""

import sys
import argparse
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog
from itertools import cycle

# ------------------------------------------------------------------------
# Helper: Ensure the 'regex' module is installed.
# ------------------------------------------------------------------------
def ensure_regex_installed():
    try:
        import regex
        return regex, None
    except ImportError:
        print("The 'regex' module is not installed.")
        try:
            choice = input("Install it now? [Y/n]: ").strip().lower()
        except Exception as e:
            sys.exit(f"Error reading input: {e}")
        if choice and choice[0] == "n":
            sys.exit("The 'regex' module is required. Exiting.")
        print("Select package manager for 'regex':")
        print("  1. pip (recommended)")
        print("  2. brew")
        print("  3. snap")
        print("  4. Other (defaults to pip)")
        pm_choice = input("Enter choice [1-4]: ").strip()
        if pm_choice == "2":
            package_manager = "brew"
        elif pm_choice == "3":
            package_manager = "snap"
        else:
            package_manager = "pip"

        def install_regex():
            try:
                if package_manager == "pip":
                    cmd = [sys.executable, "-m", "pip", "install", "regex"]
                elif package_manager == "brew":
                    cmd = ["brew", "install", "regex"]
                elif package_manager == "snap":
                    cmd = ["snap", "install", "regex"]
                else:
                    cmd = [sys.executable, "-m", "pip", "install", "regex"]
                print(f"Installing 'regex' via {package_manager} (command: {' '.join(cmd)})...")
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = proc.communicate()
                if proc.returncode == 0:
                    print("'regex' installed successfully.")
                else:
                    print(f"Installation failed:\n{stderr.decode('utf-8')}")
                return proc.returncode
            except Exception as e:
                print(f"Exception during installation: {e}")
                return -1

        install_thread = threading.Thread(target=install_regex, daemon=True)
        install_thread.start()
        return None, install_thread

regex_module, install_thread = ensure_regex_installed()
if regex_module is not None:
    globals()['regex'] = regex_module

# ------------------------------------------------------------------------
# NurdRage-Themed Placeholder Text
# ------------------------------------------------------------------------
nurdsem_text = """
Experimento acidus meltdown, quantum servo hackus impetus. 
Nulla pipettum solutionem, viva la exothermic reactionem. 
Curium subscriptus in volumetric beaker maxima, sed in 
errorum 404: reagent not found. Lorem scienca-lorem 
magnus pyro clavius, dat dataset crucial, 
ignite potentialum. Sed do circuitum transformare 
voluptate testum, con alchemicus debugga. 
Rageus Hackerorum unchained in manifestum, 
codeus snippet voluntarius replicate. 
Oscilloscope calibrat, magica chemica 
magnus ex reactio—NurdRage repletum semper excitare.
"""

# ------------------------------------------------------------------------
# Prepare a cyclic iterator for placeholder words.
# ------------------------------------------------------------------------
def get_nurdsem_words():
    try:
        words = regex.findall(r"[\p{L}\p{M}\p{N}_'\-]+", nurdsem_text)
        if not words:
            raise ValueError("No words found in placeholder text.")
        return words
    except Exception as e:
        sys.exit(f"Error processing placeholder text: {e}")

nurdsem_words = get_nurdsem_words()
nurdsem_cycle = cycle(nurdsem_words)

def replace_word(match):
    try:
        original_word = match.group()
        new_word = next(nurdsem_cycle)
        if original_word.isupper():
            new_word = new_word.upper()
        elif original_word[0].isupper():
            new_word = new_word.capitalize()
        else:
            new_word = new_word.lower()
        return new_word
    except Exception as e:
        print(f"Error in replace_word: {e}")
        return match.group()

# ------------------------------------------------------------------------
# File Selection Helpers (GUI Pickers)
# ------------------------------------------------------------------------
def get_input_file_path(cli_path=None):
    if cli_path:
        return cli_path
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        file_path = filedialog.askopenfilename(
            title="Select input file for Nurdsem",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        root.destroy()
        if not file_path:
            sys.exit("No input file selected. Exiting.")
        return file_path
    except Exception as e:
        sys.exit(f"Error in input file selection: {e}")

def get_output_file_path(cli_path=None):
    if cli_path:
        return cli_path
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        file_path = filedialog.asksaveasfilename(
            title="Select output file for Nurdsem",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        root.destroy()
        if not file_path:
            sys.exit("No output file selected. Exiting.")
        return file_path
    except Exception as e:
        sys.exit(f"Error in output file selection: {e}")

# ------------------------------------------------------------------------
# Main Function: Parse options and run the transformation
# ------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Nurdsem: A NurdRage-themed placeholder text generator."
    )
    parser.add_argument("-i", "--input", help="Path to the input file.")
    parser.add_argument("-o", "--output", help="Path for the output file.")
    args = parser.parse_args()

    input_file_path = get_input_file_path(args.input)
    output_file_path = get_output_file_path(args.output)

    if install_thread is not None:
        print("Waiting for 'regex' installation to complete...")
        install_thread.join(timeout=120)
        try:
            import regex
        except ImportError:
            sys.exit("Installation of 'regex' failed. Install it manually and re-run the script.")

    try:
        with open(input_file_path, "r", encoding="utf-8") as file_in:
            original_text = file_in.read()
    except Exception as e:
        sys.exit(f"Error reading input file '{input_file_path}': {e}")

    try:
        transformed_text = regex.sub(r"[\p{L}\p{M}\p{N}_'\-]+", replace_word, original_text)
    except Exception as e:
        sys.exit(f"Error during text transformation: {e}")

    try:
        with open(output_file_path, "w", encoding="utf-8") as file_out:
            file_out.write(transformed_text)
        print(f"Nurdsem complete! Transformed file saved to: {output_file_path}")
    except Exception as e:
        sys.exit(f"Error writing output file '{output_file_path}': {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nInterrupted by user. Exiting.")
    except Exception as e:
        sys.exit(f"Unexpected error: {e}")
EOF

# 8. Update Git: Stage all changes, commit, and push
git add .
git commit -m "Initial commit: MVP of Nurdsem with global CLI ('nurdsem'), input/output options, GUI pickers, and robust error handling. It's fucking awesome."
git push origin main

echo "All files updated and Git pushed."
