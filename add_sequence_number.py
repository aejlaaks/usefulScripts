"""
Usage: add_sequence_number.py
----------------------------
This script organizes directories by renaming them with sequential numbers based on 
their creation date, and renames files to match their parent directory names.

Features:
- Renames directories with format "NNN. DirectoryName" (where NNN is sequential number)
- Removes any existing numeric prefixes from directory names
- Sorts directories by creation date before numbering
- Renames all files in each directory to match their parent directory name
- Preserves file extensions

To use:
1. Run the script: python add_sequence_number.py
2. When prompted, enter the path to the base directory to process
3. The script will rename all directories and files according to the rules

Note: If multiple files exist in the same directory, they will all get the same name,
which may cause conflicts. Manual intervention may be needed in such cases.
"""

import os
import re


def remove_prefix(name):
    """
    Poistaa nimen alusta kaikki numeroprefiksit, jotka ovat muodossa
      "<numero>.<välilyönnit>"

    Esimerkiksi:
      "005. 5 .Johdanto laserpaikannukseen"
    muuttuu muotoon:
      "Johdanto laserpaikannukseen"
    """
    pattern = r'^(?:\d+\s*\.\s*)+'
    return re.sub(pattern, '', name)


def rename_directories(base_directory):
    """
    Käy läpi kaikki hakemistot (topdown) ja nimeää kansion uudelleen
    Windowsin luomispäivämäärän (getctime) mukaisesti. Uusi nimi on
      "NNN. <perusnimi>"
    jossa perusnimenä on alkuperäinen nimi, josta mahdolliset
    numeroprefiksit on poistettu.
    """
    for root, dirs, files in os.walk(base_directory, topdown=True):
        # Järjestetään kansiot luomispäivän mukaan
        dirs.sort(key=lambda d: os.path.getctime(os.path.join(root, d)))
        seq = 1
        for i, d in enumerate(dirs):
            new_name = f"{seq:03d}. {remove_prefix(d)}"
            old_path = os.path.join(root, d)
            new_path = os.path.join(root, new_name)
            os.rename(old_path, new_path)
            # Päivitetään dirs-lista, jotta os.walk löytää alihakemistot oikein
            dirs[i] = new_name
            seq += 1


def rename_files_to_match_parent(base_directory):
    """
    Käy läpi kaikki hakemistot ja nimeää kunkin kansion tiedostot uudelleen niin,
    että niiden nimi on täsmälleen sama kuin kansion nimi (lisäten alkuperäinen tiedostopääte).
    Jos tiedostoja on useampi samassa kansiossa, kaikista tiedostojen nimi tulee täsmälleen sama,
    mikä ei ole sallittua – tällöin joudut erottelemaan tiedostot erillisillä lisänumeroilla.
    """
    for root, dirs, files in os.walk(base_directory, topdown=True):
        # Jos kyseessä on base_directory itsessään, ohitetaan
        if root == base_directory:
            continue
        parent_dir_name = os.path.basename(root)
        for f in files:
            ext = os.path.splitext(f)[1]
            new_name = f"{parent_dir_name}{ext}"
            old_path = os.path.join(root, f)
            new_path = os.path.join(root, new_name)
            os.rename(old_path, new_path)


if __name__ == "__main__":
    base_directory = input("Anna kansion polku: ").strip()
    if os.path.isdir(base_directory):
        rename_directories(base_directory)
        rename_files_to_match_parent(base_directory)
        print("Kansiot on nimetty uudelleen ja tiedostojen nimet päivitetty vastaamaan kansion nimeä.")
    else:
        print("Annettu polku ei ole kelvollinen hakemisto.")
