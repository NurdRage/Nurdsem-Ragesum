# Nurdsem

**Nurdsem** is a NurdRage-themed placeholder text generator. It replaces each word in an input file with a cyclic token drawn from a custom placeholder text—while preserving the file's structure and capitalization.

## Features
- **GUI File Pickers:** Native dialogs for selecting input/output files when options are omitted.
- **Auto Dependency Helper:** Checks for and prompts installation of required dependencies.
- **Robust Error Handling:** Extensive error handling throughout the code.

## Installation

Clone the repository and install globally:
\`\`\`bash
git clone https://github.com/NurdRage/nurdsem.git nsem
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
