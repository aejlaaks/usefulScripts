#!/usr/bin/env python3
"""
Usage: removeSameSentencesByThreshold.py
----------------------------------------
This script removes duplicate sentences from Markdown files based on a similarity threshold.

Features:
- Recursively processes all Markdown (.md) files in a directory
- Uses similarity threshold to identify and remove duplicate sentences
- Preserves code blocks (content between ``` marks)
- Ignores Markdown headers, list markers, and formatting
- Keeps sentences shorter than 15 characters regardless of similarity
- Reports removed sentences during processing

Special cases that are always preserved:
- Markdown headers (starting with # or *)
- Numbered items (like "1." or "2)")
- List items with instructions (starting with - and containing :)
- Text with bold formatting (**)
- Short sentences (less than 15 characters)

To use:
1. Run the script: python removeSameSentencesByThreshold.py
2. When prompted, enter the path to the directory containing Markdown files
3. Enter a similarity threshold (0.0-1.0) - higher values are more strict, 
   only removing sentences that are very similar
"""

import os
import re
import difflib


def remove_duplicate_sentences(text, threshold):
    """
    Jakaa tekstin osiin siten, että koodilohkot (kolmoisbacktickit) ohitetaan.
    Tekstiosuuksissa lauseet jaetaan ja duplicate-tarkistus suoritetaan seuraavin ehdoin:
      - Markdown-otsikoita (alkavat "#" tai "*") ei käsitellä.
      - Lauseita, jotka ovat pelkkiä järjestysnumeroita (esim. "1." tai "2)") ei käsitellä.
      - Listarivejä, joissa on ohjeellista sisältöä (esim. rivit, jotka alkavat '-' ja sisältävät kaksoispisteen) ei käsitellä.
      - Rivejä, joissa esiintyy bold-merkintöjä eli "**" ei käsitellä.
      - Lisäksi, jos lauseen pituus on alle 50 merkkiä, duplicate-tarkistusta ei sovelleta, vaan lause säilytetään aina.

    Duplicate-tarkistuksessa säilytetään aina ensimmäinen esiintymä,
    ja vastaavat myöhemmät esiintymät poistetaan, paitsi yllä mainituissa ohitustapauksissa.

    Palauttaa muunnetun tekstin sekä listan poistetuista lauseista.
    """
    # Jaetaan koodilohkoihin ja muu teksti
    parts = re.split(r'(```[\s\S]*?```)', text)
    processed_parts = []
    removed_sentences = []

    for part in parts:
        # Koodilohkot jätetään muuttumattomiksi
        if part.startswith("```"):
            processed_parts.append(part)
            continue

        # Muussa tekstissä jaetaan lauseisiin
        sentences = re.split(r'(?<=[.!?])\s+', part)
        unique_sentences = []
        for sentence in sentences:
            stripped = sentence.strip()
            if not stripped:
                continue

            # Ohitetaan duplicate-tarkistus seuraaville:
            if stripped.startswith('#') or stripped.startswith('*'):
                unique_sentences.append(sentence)
                continue
            if re.match(r'^\d+[\.\)]\s*$', stripped):
                unique_sentences.append(sentence)
                continue
            if stripped.startswith('-') and ':' in stripped:
                unique_sentences.append(sentence)
                continue
            if '**' in stripped:
                unique_sentences.append(sentence)
                continue

            # Jos lause on alle 50 merkkiä pitkä, sitä ei poisteta duplicate-tarkistuksessa
            if len(stripped) < 15:
                unique_sentences.append(sentence)
                continue

            duplicate_found = False
            # Käydään läpi jo hyväksytyt lauseet; ensimmäinen esiintymä pysyy, myöhemmät verrataan siihen
            for accepted in unique_sentences:
                acc_stripped = accepted.strip()
                # Ohitetaan vertailu, jos hyväksytty lause täyttää jokin ohitusehto
                if (acc_stripped.startswith('#') or acc_stripped.startswith('*') or
                        re.match(r'^\d+[\.\)]\s*$', acc_stripped) or
                        (acc_stripped.startswith('-') and ':' in acc_stripped) or
                        ('**' in acc_stripped) or
                        len(acc_stripped) < 50):
                    continue
                similarity = difflib.SequenceMatcher(None, stripped, acc_stripped).ratio()
                if similarity > threshold:
                    duplicate_found = True
                    removed_sentences.append(sentence)
                    break
            if not duplicate_found:
                unique_sentences.append(sentence)
        processed_parts.append(" ".join(unique_sentences))
    new_content = "".join(processed_parts)
    return new_content, removed_sentences


def process_file(filepath, threshold):
    """Lukee, käsittelee ja kirjoittaa Markdown-tiedoston uudelleen."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Virhe luettaessa tiedostoa {filepath}: {e}")
        return

    new_content, removed_sentences = remove_duplicate_sentences(content, threshold)
    if new_content != content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Muokattu tiedosto: {filepath}")
            if removed_sentences:
                print("Poistettu seuraavat toistuvat lauseet:")
                for sentence in removed_sentences:
                    print(f"- {sentence.strip()}")
        except Exception as e:
            print(f"Virhe kirjoitettaessa tiedostoon {filepath}: {e}")


def process_directory(directory, threshold):
    """Käy läpi kaikki alikansiot ja käsittelee Markdown-tiedostot."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.md'):
                filepath = os.path.join(root, file)
                process_file(filepath, threshold)


if __name__ == '__main__':
    directory = input("Anna kansion polku: ")
    try:
        threshold_input = input("Anna threshold-arvo (0.0 - 1.0): ")
        threshold = float(threshold_input)
        if not 0 <= threshold <= 1:
            raise ValueError("Threshold-arvon tulee olla välillä 0.0 ja 1.0")
    except ValueError as e:
        print(f"Virheellinen threshold-arvo: {e}. Käytetään oletusarvoa 0.8.")
        threshold = 0.8

    process_directory(directory, threshold)
