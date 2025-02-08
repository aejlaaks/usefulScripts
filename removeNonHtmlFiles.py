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
