import os


def rename_folders_to_file_names(directory):
    """
    Käy läpi kaikki alikansiot annetussa kansiossa ja muuttaa kansion nimen vastaamaan
    tiedoston nimeä (ilman tiedostopäätettä), jos tiedosto löytyy.

    :param directory: Pääkansio, jonka alikansiot käydään läpi.
    """
    for root, dirs, _ in os.walk(directory):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)

            # Tarkista, että kansio ei ole tyhjä
            if not os.listdir(folder_path):
                print(f"Kansio '{dir_name}' on tyhjä. Ohitetaan.")
                continue

            # Etsi tiedostoja kansiosta
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            if not files:
                print(f"Kansiosta '{dir_name}' ei löytynyt tiedostoja. Ohitetaan.")
                continue

            # Käytä ensimmäisen tiedoston nimeä ilman tiedostopäätettä
            first_file = files[0]
            file_base_name, _ = os.path.splitext(first_file)

            # Uusi kansion nimi
            new_folder_path = os.path.join(root, file_base_name)

            # Tarkista, ettei samaa nimeä ole jo olemassa
            if os.path.exists(new_folder_path):
                print(f"Kansion '{file_base_name}' nimi on jo käytössä. Ohitetaan.")
                continue

            # Uudelleennimeä kansio
            os.rename(folder_path, new_folder_path)
            print(f"Kansio '{dir_name}' nimettiin uudelleen '{file_base_name}'.")


if __name__ == "__main__":
    # Kysy käyttäjältä kansion polku
    directory = input("Anna pääkansion polku: ").strip()
    if not os.path.isdir(directory):
        print(f"Virhe: Polku '{directory}' ei ole kelvollinen kansio.")
    else:
        rename_folders_to_file_names(directory)
