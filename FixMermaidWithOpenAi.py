"""
Usage: FixMermaidWithOpenAi.py
------------------------------
This script uses the OpenAI API to automatically fix syntax errors in Mermaid diagrams 
found in Markdown files.

Features:
- Recursively processes all Markdown (.md) files in a directory
- Identifies Mermaid code blocks (between ```mermaid and ```)
- Sends Mermaid code to OpenAI for syntax correction
- Updates files only if corrections are made
- Reports which files were modified

Requirements:
- OpenAI Python package
- OpenAI API key

To use:
1. Set your OpenAI API key in the openai.api_key variable
2. Run the script: python FixMermaidWithOpenAi.py
3. When prompted, enter the path to the directory containing Markdown files
4. The script will find and fix Mermaid syntax errors in all Markdown files
"""

import os
import re
import openai

# Aseta OpenAI API -avain
openai.api_key = "YOUR_API_KEY_HERE"  # Replace with your actual API key


def read_md(file_path):
    """Lukee Markdown-tiedoston sisällön."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_md(file_path, content):
    """Kirjoittaa sisällön Markdown-tiedostoon."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def correct_mermaid_code_with_openai(code):
    """
    Lähettää mermaid-koodilohkon sisällön OpenAI:lle,
    jotta mahdolliset syntaksivirheet korjattaisiin.
    Palauttaa ainoastaan korjatun koodin ilman lisäselityksiä.
    """
    prompt = (
            "Korjaa seuraava mermaid-koodilohko mahdollisista syntaksivirheistä. "
            "Palauta ainoastaan korjattu koodi, älä lisää mitään selityksiä:\n\n" +
            code
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Voit halutessasi käyttää myös GPT-4:ää, jos se on käytettävissä
            messages=[
                {"role": "system", "content": "Olet asiantuntija, joka korjaa mermaid-koodilohkojen syntaksia."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=2048
        )
        corrected_code = response["choices"][0]["message"]["content"].strip()
        return corrected_code
    except Exception as e:
        print(f"Virhe OpenAI-kutsussa: {e}")
        return code  # Palautetaan alkuperäinen koodi virheen sattuessa


def process_file(file_path):
    """
    Lukee Markdown-tiedoston, etsii siitä kaikki mermaid-koodilohkot,
    lähettää niiden sisällön OpenAI:lle korjattavaksi ja tallentaa muutokset.
    """
    content = read_md(file_path)

    # Regex etsii lohkot, jotka alkavat "```mermaid" ja päättyvät "```"
    pattern = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL)

    def replacer(match):
        original_code = match.group(1)
        print("Löydetty mermaid-koodilohko, lähetetään korjattavaksi...")
        corrected_code = correct_mermaid_code_with_openai(original_code)
        if corrected_code and corrected_code != original_code:
            print("Mermaid-koodilohko korjattu.")
            return f"```mermaid\n{corrected_code}\n```"
        else:
            return match.group(0)

    new_content = pattern.sub(replacer, content)

    if new_content != content:
        write_md(file_path, new_content)
        print(f"Korjattu tiedosto: {file_path}")
    else:
        print(f"Ei muutoksia tiedostossa: {file_path}")


def process_directory(root_directory):
    """
    Käy läpi annetun kansion ja sen alikansiot, ja prosessoi kaikki Markdown-tiedostot.
    """
    for subdir, _, files in os.walk(root_directory):
        for filename in files:
            if filename.endswith(".md"):
                file_path = os.path.join(subdir, filename)
                print(f"Käsitellään tiedostoa: {file_path}")
                process_file(file_path)


if __name__ == "__main__":
    directory = input("Anna kansion polku, jossa Markdown-tiedostot sijaitsevat: ")
    if os.path.isdir(directory):
        process_directory(directory)
    else:
        print("Annettu polku ei ole kelvollinen kansio.")
