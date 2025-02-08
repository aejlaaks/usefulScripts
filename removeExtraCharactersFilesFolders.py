import os
import re

def sanitize_name(name):
    """
    Poistaa kaikki erikoismerkit ja Unicode-merkit tiedosto- ja kansioiden nimistä.
    """
    # Korvaa sallitut merkit ja poistaa Unicode-merkit
    name = re.sub(r'[<>:"/\\|?*\uf000-\uffff]', '_', name)  # Poistaa Unicode-erikoismerkit
    name = re.sub(r'[^\x00-\x7F]', '_', name)  # Poistaa ei-ASCII-merkit
    name = name.strip()  # Poistaa ylimääräiset välilyönnit
    return name[:100]  # Rajoittaa nimen pituuden 100 merkkiin

def shorten_path(path, max_length=255):
    """
    Lyhentää tiedostopolun, jos se ylittää Windowsin enimmäispituuden.
    """
    if len(path) <= max_length:
        return path
    directory, file_name = os.path.split(path)
    file_name = file_name[:max_length - len(directory) - 1]
    return os.path.join(directory, file_name)

def process_directory(directory):
    """
    Käy läpi annetun hakemiston ja muokkaa kansioiden ja tiedostojen nimiä.
    """
    for root, dirs, files in os.walk(directory, topdown=False):
        # Käsittele tiedostot
        for file in files:
            try:
                old_path = os.path.join(root, file)
                new_name = sanitize_name(file)
                new_path = os.path.join(root, new_name)

                # Lyhennetään tiedostopolku
                new_path = shorten_path(new_path)

                if old_path != new_path and not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f"Renamed file: {old_path} -> {new_path}")
            except Exception as e:
                print(f"Error processing file '{file}': {e}")

        # Käsittele kansiot
        for dir in dirs:
            try:
                old_path = os.path.join(root, dir)
                new_name = sanitize_name(dir)
                new_path = os.path.join(root, new_name)

                # Lyhennetään polku
                new_path = shorten_path(new_path)

                if old_path != new_path and not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f"Renamed directory: {old_path} -> {new_path}")
            except Exception as e:
                print(f"Error processing directory '{dir}': {e}")

if __name__ == "__main__":
    directory_to_process = input("Anna hakemiston polku: ")
    if os.path.isdir(directory_to_process):
        try:
            process_directory(directory_to_process)
            print("Käsittely valmis.")
        except Exception as e:
            print(f"Virhe käsittelyssä: {e}")
    else:
        print("Annettu polku ei ole kelvollinen hakemisto.")
