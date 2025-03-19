"""
Usage: replateDOT.py
-------------------
This script replaces all instances of ```dot with ```graphviz in Markdown files.
This is useful for converting DOT language code blocks to GraphViz format for 
better compatibility with Markdown renderers.

Features:
- Recursively processes all Markdown (.md) files in a directory and its subdirectories
- Case-insensitive matching to catch variations like ```DOT or ```Dot
- Reports each file processed and whether changes were made
- Preserves all other content in the files

To use:
1. Run the script: python replateDOT.py
2. When prompted, enter the path to the directory containing Markdown files
3. The script will process all files and report the changes made
"""

import os
import re

def replace_dot_with_graphviz(folder_path):
    """
    Replaces ```dot with ```graphviz in all Markdown files in a folder and its subfolders.
    Prints the name of each processed file.

    Parameters:
        folder_path (str): Path to the folder containing Markdown files.
    """
    try:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.md'):
                    input_file = os.path.join(root, file)
                    print(f"Processing file: {input_file}")

                    with open(input_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Replace ```dot with ```graphviz
                    updated_content = re.sub(r'```dot', '```graphviz', content, flags=re.IGNORECASE)

                    if content != updated_content:
                        with open(input_file, 'w', encoding='utf-8') as f:
                            f.write(updated_content)
                        print(f"  Updated: {input_file}")
                    else:
                        print(f"  No changes needed: {input_file}")

        print(f"\nFinished processing all Markdown files in {folder_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    folder_path = input("Enter the path to the folder containing Markdown files: ").strip()
    replace_dot_with_graphviz(folder_path)