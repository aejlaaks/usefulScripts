"""
Usage: FixMermaidAzureAi.py
---------------------------
This script uses Azure OpenAI Service to automatically fix syntax errors in Mermaid diagrams
found in Markdown files.

Features:
- Recursively processes all Markdown (.md) files in a directory
- Identifies Mermaid code blocks (between ```mermaid and ```)
- Sends Mermaid code to Azure OpenAI for syntax correction
- Updates files only if corrections are made
- Reports which files were modified

Requirements:
- OpenAI Python package (with Azure support)
- tiktoken package
- Azure OpenAI Service API key and endpoint

To use:
1. Set your Azure OpenAI endpoint and API key in the variables
2. Run the script: python FixMermaidAzureAi.py
3. When prompted, enter the path to the directory containing Markdown files
4. The script will find and fix Mermaid syntax errors in all Markdown files
"""

import os
import re
from openai import AzureOpenAI
from tiktoken import get_encoding

# Aseta Azure OpenAI Service -yhteyden tiedot
AZURE_OPENAI_ENDPOINT = "YOUR_AZURE_ENDPOINT_HERE"  # Replace with your Azure OpenAI endpoint
AZURE_OPENAI_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key
TOKEN_LIMIT = 128000  # Token-raja (esim. 128000 GPT-4:ssa)

# Luodaan Azure OpenAI -client
client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2024-02-01"
)

def read_md(file_path):
    """Lukee Markdown-tiedoston sisällön."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_md(file_path, content):
    """Kirjoittaa sisällön Markdown-tiedostoon."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def correct_mermaid_code_with_ai(code):
    """
    Lähettää vain mermaid-koodilohkon sisällön Azure OpenAI:lle,
    jotta mahdolliset syntaksivirheet korjattaisiin.
    Palauttaa ainoastaan korjatun koodin ilman selityksiä.
    """
    prompt = (
        "Korjaa seuraava mermaid-koodi mahdollisista syntaksivirheistä. "
        "Palauta ainoastaan korjattu koodi, älä lisää mitään selityksiä:\n\n"
        f"{code}"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Olet asiantuntija, joka korjaa mermaid-koodilohkojen syntaksivirheet. "
                        "Palauta vain korjattu koodi ilman lisäselvityksiä."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            stream=False,
            max_tokens=8000
        )
        print("Raakavastaus:", response)
        corrected_code = response.choices[0].message.content.strip()
        if not corrected_code:
            raise ValueError("API-vastaus on tyhjä tai puutteellinen.")
        return corrected_code
    except Exception as e:
        print(f"Virhe API-kutsussa: {e}")
        return code  # Palautetaan alkuperäinen koodi virheen sattuessa

def process_file(file_path):
    """
    Lukee tiedoston, etsii mermaid-koodilohkot, lähettää niiden sisällön
    korjattavaksi Azure OpenAI:lle ja tallentaa mahdolliset muutokset.
    """
    content = read_md(file_path)
    # Etsitään lohkot, jotka alkavat "```mermaid" ja päättyvät "```"
    pattern = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL)

    def replacer(match):
        original_code = match.group(1)
        print("Löydetty mermaid-koodilohko, lähetetään korjattavaksi...")
        corrected_code = correct_mermaid_code_with_ai(original_code)
        if corrected_code and corrected_code != original_code:
            print("Mermaid-koodilohko korjattu.")
            return f"```mermaid\n{corrected_code}\n```"
        else:
            return match.group(0)

    new_content = pattern.sub(replacer, content)
    if new_content != content:
        write_md(file_path, new_content)
        print(f"Muokattu: {file_path}")
    else:
        print(f"Ei muutoksia: {file_path}")

def process_directory(root_directory):
    """
    Käy läpi kaikki pääkansion ja alikansioiden Markdown-tiedostot.
    """
    for subdir, _, files in os.walk(root_directory):
        for filename in files:
            if filename.endswith(".md"):
                file_path = os.path.join(subdir, filename)
                print(f"Käsitellään tiedostoa: {file_path}")
                process_file(file_path)

if __name__ == "__main__":
    root_directory = input("Anna pääkansion polku, jossa Markdown-tiedostot sijaitsevat: ")
    if os.path.isdir(root_directory):
        process_directory(root_directory)
    else:
        print("Annettu polku ei ole kelvollinen kansio.")
