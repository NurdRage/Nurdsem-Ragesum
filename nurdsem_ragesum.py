#!/usr/bin/env python3
"""
Nurdsem Ragesum: A NurdRage-themed placeholder text generator that replaces each word
in an input file with a cyclic token from a custom placeholder text.
It preserves file structure and capitalization. Uses GUI file pickers if file paths are not provided.
"""

import sys
import argparse
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog
from itertools import cycle
import time

# ------------------------------------------------------------------------
# Helper: Ensure the 'regex' module is installed.
# ------------------------------------------------------------------------
def ensure_regex_installed():
    """
    Check if the 'regex' module is installed.
    If not, prompt the user to install it.
    Returns:
        A tuple (regex_module, install_thread)
          - regex_module: the imported module if already available; else None.
          - install_thread: a threading.Thread instance if installation was initiated; else None.
    """
    try:
        import regex
        return regex, None  # Already installed
    except ImportError:
        print("The 'regex' module is not installed.")
        try:
            choice = input("Would you like to install it now? [Y/n]: ").strip().lower()
        except Exception as e:
            sys.exit(f"Error reading input: {e}")

        if choice and choice[0] == "n":
            sys.exit("The 'regex' module is required. Exiting.")
        
        # Let the user choose a package manager.
        print("Select your package manager for installing 'regex':")
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

                print(f"Installing 'regex' using {package_manager} (command: {' '.join(cmd)}) ...")
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = proc.communicate()
                if proc.returncode == 0:
                    print("'regex' installed successfully.")
                else:
                    print(f"Installation failed with error:\n{stderr.decode('utf-8')}")
                return proc.returncode
            except Exception as e:
                print(f"An exception occurred during installation: {e}")
                return -1

        install_thread = threading.Thread(target=install_regex, daemon=True)
        install_thread.start()
        return None, install_thread

# ------------------------------------------------------------------------
# Global Dependency Check
# ------------------------------------------------------------------------
regex_module, install_thread = ensure_regex_installed()

# If regex was already installed, add it to globals.
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
# Prepare a cyclic iterator for our placeholder words.
# Using a Unicode-aware regex pattern (requires the regex module).
# ------------------------------------------------------------------------
def get_nurdsem_words():
    try:
        words = regex.findall(r"[\p{L}\p{M}\p{N}_'\-]+", nurdsem_text)
        if not words:
            raise ValueError("No words were found in the placeholder text.")
        return words
    except Exception as e:
        sys.exit(f"Error processing placeholder text: {e}")

try:
    nurdsem_words = get_nurdsem_words()
except Exception as e:
    sys.exit(e)

nurdsem_cycle = cycle(nurdsem_words)

def replace_word(match):
    """
    Replaces each detected word in the input with the next token from our NurdRage-themed text.
    Preserves the original word’s capitalization style:
      - ALL CAPS remains ALL CAPS.
      - Capitalized (first letter uppercase) is preserved.
      - Otherwise, the replacement is lowercase.
    """
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
        return match.group()  # Fallback: return original word

# ------------------------------------------------------------------------
# File Selection Logic: GUI pickers for Input and Output
# ------------------------------------------------------------------------
def get_input_file_path(cli_path=None):
    """
    Returns the input file path.
    If cli_path is provided and valid, returns it.
    Otherwise, opens a native file picker dialog.
    """
    if cli_path:
        return cli_path
    else:
        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            file_path = filedialog.askopenfilename(
                title="Select a file for Nurdsem Ragesum",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            root.destroy()
            if not file_path:
                sys.exit("No input file was selected. Exiting.")
            return file_path
        except Exception as e:
            sys.exit(f"Error in input file selection: {e}")

def get_output_file_path(cli_path=None):
    """
    Returns the output file path.
    If cli_path is provided, returns it.
    Otherwise, opens a native 'Save As' dialog.
    """
    if cli_path:
        return cli_path
    else:
        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            file_path = filedialog.asksaveasfilename(
                title="Select a destination for the transformed file",
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            root.destroy()
            if not file_path:
                sys.exit("No output file was selected. Exiting.")
            return file_path
        except Exception as e:
            sys.exit(f"Error in output file selection: {e}")

# ------------------------------------------------------------------------
# Main Execution Block
# ------------------------------------------------------------------------
def main():
    # --------------------------------------------------------------------
    # Parse Command-Line Arguments
    # --------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description="Nurdsem Ragesum: A NurdRage-themed placeholder text generator."
    )
    parser.add_argument("-i", "--input", help="Path to the input file.")
    parser.add_argument("-o", "--output", help="Path for the output file. If omitted, a 'Save As' dialog will open.")
    args = parser.parse_args()

    input_file_path = get_input_file_path(args.input)
    output_file_path = get_output_file_path(args.output)

    # --------------------------------------------------------------------
    # Wait for regex installation to finish if needed.
    # --------------------------------------------------------------------
    if install_thread is not None:
        print("Waiting for the 'regex' installation to finish...")
        install_thread.join(timeout=120)  # wait up to 2 minutes
        try:
            import regex
        except ImportError:
            sys.exit("Installation of 'regex' failed. Please install it manually and re-run the script.")

    # --------------------------------------------------------------------
    # Read the Original File Content
    # --------------------------------------------------------------------
    try:
        with open(input_file_path, "r", encoding="utf-8") as file_in:
            original_text = file_in.read()
    except Exception as e:
        sys.exit(f"Error reading file '{input_file_path}': {e}")

    # --------------------------------------------------------------------
    # Apply the Nurdsem Ragesum Transformation
    # --------------------------------------------------------------------
    try:
        transformed_text = regex.sub(r"[\p{L}\p{M}\p{N}_'\-]+", replace_word, original_text)
    except Exception as e:
        sys.exit(f"Error during text transformation: {e}")

    # --------------------------------------------------------------------
    # Write the Transformed Text to the Output File
    # --------------------------------------------------------------------
    try:
        with open(output_file_path, "w", encoding="utf-8") as file_out:
            file_out.write(transformed_text)
        print(f"Nurdsem Ragesum complete!\nTransformed file saved to: {output_file_path}")
    except Exception as e:
        sys.exit(f"Error writing to file '{output_file_path}': {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nProcess interrupted by user. Exiting.")
    except Exception as e:
        sys.exit(f"An unexpected error occurred: {e}")
