import os

def delete_files_and_dirs_with_keyword(base_path, keyword):
    """
    Poistaa kaikki tiedostot ja kansiot annetusta kansiosta ja sen alikansioista,
    joiden nimissä on tietty avainsana.

    :param base_path: Polku kansioon, josta tiedostoja ja kansioita etsitään.
    :param keyword: Avainsana, jota etsitään tiedostonimistä ja kansioiden nimistä.
    """
    for root, dirs, files in os.walk(base_path, topdown=False):
        # Poista tiedostot, joiden nimessä on avainsana
        for file in files:
            if keyword.lower() in file.lower():
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Poistettu tiedosto: {file_path}")
                except Exception as e:
                    print(f"Virhe poistettaessa tiedostoa {file_path}: {e}")

        # Poista kansiot, joiden nimessä on avainsana
        for dir in dirs:
            if keyword.lower() in dir.lower():
                dir_path = os.path.join(root, dir)
                try:
                    os.rmdir(dir_path)  # Poistaa vain tyhjät kansiot
                    print(f"Poistettu kansio: {dir_path}")
                except Exception as e:
                    print(f"Virhe poistettaessa kansiota {dir_path}: {e}")

if __name__ == "__main__":
    # Korvaa tämä haluamallasi kansion polulla
    base_path = input("Anna polku kansioon: ").strip()

    # Avainsana, jonka esiintyminen johtaa tiedoston tai kansion poistoon
    keyword = "korjattu"

    # Varmista, että annettu polku on olemassa
    if os.path.exists(base_path) and os.path.isdir(base_path):
        delete_files_and_dirs_with_keyword(base_path, keyword)
    else:
        print("Annettu polku ei ole kelvollinen hakemisto.")
