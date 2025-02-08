import os
import re

# Funktio lukemaan Markdown-tiedosto
def read_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# Funktio kirjoittamaan korjattu sisältö tiedostoon
def write_md(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Funktio korjaamaan Mermaid-kaavioiden syntaksin
def fix_mermaid_syntax(content):
    # Korjaa escapetut kaarisulut
    content = re.sub(r"\\\(", r"(", content)
    content = re.sub(r"\\\)", r")", content)

    # Korjaa mahdollisesti virheelliset Mermaid-yhteydet (esim. "|>" -> "|")
    content = re.sub(r"\|>", r"|", content)

    # Poistaa ylimääräiset välilyönnit Mermaid-avaus- ja sulkemistageista
    content = re.sub(r"```mermaid\s+", "```mermaid\n", content)
    content = re.sub(r"\s+```", "\n```", content)

    return content

# Funktio käsittelemään Markdown-tiedostot ja korjaamaan Mermaid-kaaviot
def process_markdown_files(directory):
    for root, _, files in os.walk(directory):  # Käy läpi myös alikansiot
        for filename in files:
            if filename.endswith(".md"):  # Etsi Markdown-tiedostoja
                file_path = os.path.join(root, filename)
                print(f"Tutkitaan tiedostoa: {file_path}")

                # Lue tiedosto
                content = read_md(file_path)

                # Korjaa Mermaid-kaavioiden syntaksin
                updated_content = fix_mermaid_syntax(content)

                # Tallenna korjattu tiedosto
                write_md(file_path, updated_content)
                print(f"Korjattu tiedosto tallennettu: {file_path}")

# Suorita skripti määritetyssä kansiossa
if __name__ == "__main__":
    directory = input("Anna kansion polku, jossa Markdown-tiedostot sijaitsevat: ")
    if os.path.isdir(directory):
        process_markdown_files(directory)
    else:
        print("Annettu polku ei ole kelvollinen kansio.")
