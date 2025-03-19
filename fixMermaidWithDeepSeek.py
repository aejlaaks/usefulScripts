"""
Usage: fixMermaidWithDeepSeek.py
--------------------------------
This script uses the DeepSeek AI API to automatically fix syntax errors in Mermaid diagrams 
found in Markdown files.

Features:
- Recursively processes folders looking for .md files with the same name as their folder
- Identifies Mermaid code blocks (between ```mermaid and ```)
- Sends Mermaid code to DeepSeek AI for syntax correction
- Updates the file only if corrections are made
- Reports which files were modified

Requirements:
- OpenAI Python package
- DeepSeek API key

To use:
1. Set your DeepSeek API key in the DEEPSEEK_API_KEY variable
2. Run the script: python fixMermaidWithDeepSeek.py
3. When prompted, enter the path to the root directory to process
4. The script will find and fix Mermaid syntax errors in matching Markdown files
"""

import os
import re
from openai import OpenAI

# Aseta DeepSeek API -yhteyden tiedot
DEEPSEEK_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# Luo DeepSeek API -asiakas
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

def strip_code_fence(code):
    """
    Jos koodi alkaa '```mermaid' ja päättyy '```', poistetaan nämä merkit.
    Palauttaa puhtaan koodin ilman koodilohkomerkintöjä.
    """
    pattern = re.compile(r"^```mermaid\s*\n(.*?)\n```$", re.DOTALL)
    match = pattern.match(code.strip())
    if match:
        return match.group(1).strip()
    return code.strip()

def correct_mermaid_code_with_ai(code):
    """
    Lähettää vain mermaid-koodilohkon sisällön tekoälylle,
    jotta se korjaisi mahdolliset syntaksivirheet.
    """
    prompt = (
        "Korjaa seuraava mermaid-koodi mahdollisista syntaksivirheistä. "
        "Vastaa ainoastaan korjatulla koodilla, älä muuta muuta sisältöä:\n\n"
        f"{code}"
    )

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Olet asiantuntija, joka korjaa mermaid-koodilohkojen syntaksia. "
                        "Käytä selkeää ja ytimekästä kieltä."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            stream=False,
            max_tokens=8000
        )

        print("Raakavastaus:", response)

        if not response or not hasattr(response, "choices") or not response.choices:
            raise ValueError("API-vastaus ei sisällä 'choices'-osaa tai se on tyhjä.")

        corrected_code = response.choices[0].message.content.strip()
        if not corrected_code:
            raise ValueError("API-vastaus on tyhjä tai puutteellinen.")

        # Poistetaan mahdolliset ylimääräiset koodilohkomerkit
        corrected_code = strip_code_fence(corrected_code)
        return corrected_code
    except Exception as e:
        print(f"Virhe API-kutsussa: {e}")
        return code  # Palautetaan alkuperäinen koodi virheen sattuessa

def process_file(file_path):
    """
    Lukee tiedoston, etsii mermaid-koodilohkot, lähettää niiden sisällön tekoälylle
    korjattavaksi ja tallentaa mahdolliset muutokset takaisin tiedostoon.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex etsii mermaid-koodilohkot: alkava "```mermaid", jonka jälkeen koodia, ja päättyy "```"
    pattern = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL)

    def replacer(match):
        original_code = match.group(1)
        corrected_code = correct_mermaid_code_with_ai(original_code)
        # Jos korjattu koodi eroaa alkuperäisestä, palautetaan uusi lohko
        if corrected_code and corrected_code != original_code:
            print("Mermaid-koodilohko korjattu.")
            return f"```mermaid\n{corrected_code}\n```"
        else:
            return match.group(0)

    new_content = pattern.sub(replacer, content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Muokattu: {file_path}")
    else:
        print(f"Ei muutoksia: {file_path}")

def process_directory(root_dir):
    """
    Käy läpi annetun kansion ja sen alikansiot.
    Jokaisessa kansiossa etsitään .md-tiedosto, jonka nimi vastaa kansion nimeä.
    """
    for dirpath, dirs, files in os.walk(root_dir):
        current_folder_name = os.path.basename(dirpath)
        expected_file_name = current_folder_name + ".md"

        if expected_file_name in files:
            file_path = os.path.join(dirpath, expected_file_name)
            print(f"Käsitellään tiedostoa: {file_path}")
            process_file(file_path)
        else:
            print(f"Tiedostoa '{expected_file_name}' ei löytynyt kansiosta: {dirpath}")

if __name__ == "__main__":
    directory = input("Anna kansion polku: ")  # Esim. /polku/kansioon
    process_directory(directory)
