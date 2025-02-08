import os

MAX_PATH_LENGTH = 350

def shorten_name(name, max_length):
    """Lyhentää nimen, jos se ylittää maksimi pituuden."""
    if len(name) > max_length:
        extension = ""
        if "." in name and not name.startswith("."):
            extension = name[name.rfind("."):]  # Säilytetään tiedostopääte
            name = name[:name.rfind(".")]
        return name[:max_length - len(extension)] + extension
    return name

def shorten_path(root, name):
    """Lyhentää nimen niin, että koko polku pysyy alle 350 merkin."""
    full_path = os.path.join(root, name)
    max_name_length = MAX_PATH_LENGTH - len(root) - 1  # Jätetään tilaa '/'
    return shorten_name(name, max_name_length)

def process_directory(directory):
    """Käy läpi hakemiston ja sen alihakemistot, lyhentäen nimiä tarvittaessa."""
    for root, dirs, files in os.walk(directory, topdown=False):
        # Käsitellään tiedostot
        for file in files:
            original_path = os.path.join(root, file)
            shortened_name = shorten_path(root, file)
            if shortened_name != file:
                shortened_path = os.path.join(root, shortened_name)
                os.rename(original_path, shortened_path)
                print(f"Renamed file: {original_path} -> {shortened_path}")

        # Käsitellään kansiot
        for dir in dirs:
            original_path = os.path.join(root, dir)
            shortened_name = shorten_path(root, dir)
            if shortened_name != dir:
                shortened_path = os.path.join(root, shortened_name)
                os.rename(original_path, shortened_path)
                print(f"Renamed directory: {original_path} -> {shortened_path}")

def main():
    base_directory = input("Anna kansion polku: ").strip()

    if not os.path.isdir(base_directory):
        print(f"Annettu polku ei ole kelvollinen hakemisto: {base_directory}")
        return

    print(f"Käsitellään kansio: {base_directory}")
    process_directory(base_directory)
    print("Valmis!")

if __name__ == "__main__":
    main()
