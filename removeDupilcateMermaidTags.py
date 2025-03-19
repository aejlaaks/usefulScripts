"""
Usage: removeDupilcateMermaidTags.py
------------------------------------
This script removes duplicate code fence markers (``` or ```mermaid) in Markdown files.
It's useful for fixing Markdown files where consecutive identical fence markers cause
rendering issues, especially with Mermaid diagrams.

Features:
- Recursively processes all Markdown (.md) files in a directory
- Removes consecutive duplicate code fence markers
- Preserves the content inside code blocks
- Reports which files were modified

To use:
1. Run the script: python removeDupilcateMermaidTags.py
2. When prompted, enter the path to the directory containing Markdown files
3. The script will process all Markdown files and report any changes
"""

import os
import re

def remove_duplicate_fence_lines(content):
    """
    Poistaa peräkkäin toistuvat koodilohkomerkit (esim. "```" tai "```mermaid")
    siten, että peräkkäiset samanlaiset merkkirivit säilytetään vain kerran.
    """
    lines = content.splitlines(keepends=True)
    new_lines = []
    prev_line = None
    for line in lines:
        # Tarkistetaan, onko kyseessä koodilohkomerkintä (aloitus tai lopetus)
        if line.strip().startswith("```"):
            # Jos edellinen rivi on sama kuin nykyinen, ohitetaan nykyinen rivi
            if prev_line is not None and line.strip() == prev_line.strip():
                continue
        new_lines.append(line)
        prev_line = line
    return "".join(new_lines)

def process_file(file_path):
    """
    Lukee Markdown-tiedoston, poistaa duplikaatit koodilohkomerkeistä
    ja tallentaa muutetun sisällön takaisin tiedostoon, jos muutoksia ilmenee.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()

    new_content = remove_duplicate_fence_lines(original_content)

    if new_content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Muokattu: {file_path}")
    else:
        print(f"Ei muutoksia: {file_path}")

def process_directory(root_dir):
    """
    Käy läpi annetun kansion ja sen alikansiot, ja käsittelee kaikki .md-tiedostot.
    """
    for dirpath, _, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith(".md"):
                file_path = os.path.join(dirpath, filename)
                process_file(file_path)

if __name__ == "__main__":
    directory = input("Anna kansion polku: ")  # Esim. C:\polku\kansioon
    if os.path.isdir(directory):
        process_directory(directory)
    else:
        print("Annettu polku ei ole kelvollinen kansio.")
