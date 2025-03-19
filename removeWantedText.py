"""
Usage: removeWantedText.py
--------------------------
This script removes specified text patterns and numeric patterns (like x.x or x.xx) from file 
and directory names within a specified directory tree.

Features:
- Recursively processes all files and directories
- Removes custom text patterns defined in TEXTS_TO_REMOVE list
- Removes numeric patterns in the format x.x or x.xx (e.g., 2.5, 3.14)
- Safely handles naming conflicts

To use:
1. Edit the TEXTS_TO_REMOVE list at the top of the script to include the text patterns you want to remove
2. Run the script: python removeWantedText.py
3. When prompted, enter the path to the directory you want to process
4. The script will rename all files and directories, removing the specified patterns
"""

import os
import re

# Määritä poistettavat tekstit tähän listaan
TEXTS_TO_REMOVE = ['unwanted_text', 'another_text']

def remove_texts_from_name(name, remove_texts):
    """
    Poistaa nimestä annetut tekstit sekä numeromuotoiset osat, jotka ovat muotoa x.x tai x.xx.
    """
    new_name = name
    for text in remove_texts:
        new_name = new_name.replace(text, "")
    # Poistetaan numerot muodossa x.x tai x.xx (esim. 2.5 tai 2.51)
    new_name = re.sub(r'\b\d\.\d{1,2}\b', '', new_name)
    return new_name

def process_directory(input_dir, remove_texts):
    """
    Käy läpi kansion ja sen alikansiot sekä uudelleennimeää tiedostot ja kansiot
    poistamalla niiden nimistä annetut tekstit ja numeromuotoiset osat.
    """
    # Käydään hakemistorakenne läpi alhaalta ylöspäin, jotta kansioiden uudelleennimeäminen onnistuu oikein.
    for root, dirs, files in os.walk(input_dir, topdown=False):
        # Käsitellään ensin tiedostot
        for file_name in files:
            new_file_name = remove_texts_from_name(file_name, remove_texts)
            if new_file_name != file_name:
                old_file_path = os.path.join(root, file_name)
                new_file_path = os.path.join(root, new_file_name)
                if os.path.exists(new_file_path):
                    print(f"Varoitus: kohde {new_file_path} jo olemassa, tiedostoa {old_file_path} ei muuteta.")
                else:
                    os.rename(old_file_path, new_file_path)
                    print(f"Uudelleennimetty tiedosto: {old_file_path} -> {new_file_path}")
        # Käsitellään kansiot
        for dir_name in dirs:
            new_dir_name = remove_texts_from_name(dir_name, remove_texts)
            if new_dir_name != dir_name:
                old_dir_path = os.path.join(root, dir_name)
                new_dir_path = os.path.join(root, new_dir_name)
                if os.path.exists(new_dir_path):
                    print(f"Varoitus: kohde {new_dir_path} jo olemassa, kansiota {old_dir_path} ei muuteta.")
                else:
                    os.rename(old_dir_path, new_dir_path)
                    print(f"Uudelleennimetty kansio: {old_dir_path} -> {new_dir_path}")

def main():
    # Kysytään käyttäjältä käsiteltävän kansion polku
    input_dir = input("Anna käsiteltävän kansion polku: ").strip()
    if not os.path.isdir(input_dir):
        print(f"Virhe: {input_dir} ei ole olemassa oleva kansio.")
        return

    process_directory(input_dir, TEXTS_TO_REMOVE)

if __name__ == '__main__':
    main()
