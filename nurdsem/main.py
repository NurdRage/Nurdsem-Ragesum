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
