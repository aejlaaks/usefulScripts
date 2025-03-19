"""
Usage: removeNonHtmlFiles.py
---------------------------
This script cleans up directories by removing all non-HTML files and duplicate HTML files.

Features:
- Recursively processes all files in a directory and its subdirectories
- Deletes any file that doesn't have a .html extension
- Identifies duplicate HTML files based on their relative path from the root directory
- Removes duplicates while keeping the first occurrence of each HTML file
- Reports all file deletions and any errors that occur during deletion

To use:
1. Run the script: python removeNonHtmlFiles.py
2. When prompted, enter the path to the directory you want to clean up
3. The script will remove all non-HTML files and duplicate HTML files

Warning: This operation is irreversible. Make sure to back up important files before using.
"""

import os

def remove_non_html_files_and_duplicates(folder_path):
    seen_files = set()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Tarkista, onko tiedoston pääte .html
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                # Tarkista, onko tiedosto jo nähty (sisältöperusteisesti)
                file_hash = os.path.relpath(file_path, folder_path)  # Käytetään suhteellista polkua tunnistamiseen
                if file_hash in seen_files:
                    try:
                        os.remove(file_path)
                        print(f"Poistettu duplikaatti: {file_path}")
                    except Exception as e:
                        print(f"Virhe poistettaessa tiedostoa {file_path}: {e}")
                else:
                    seen_files.add(file_hash)
            else:
                # Poistetaan ei-HTML-tiedostot
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Poistettu: {file_path}")
                except Exception as e:
                    print(f"Virhe poistettaessa tiedostoa {file_path}: {e}")

def main():
    folder_path = input("Anna kansion polku: ")

    if not os.path.isdir(folder_path):
        print("Annettu polku ei ole kelvollinen kansio.")
        return

    remove_non_html_files_and_duplicates(folder_path)
    print("Kaikki muut paitsi .html-tiedostot on poistettu, ja duplikaatit on poistettu.")

if __name__ == "__main__":
    main()
