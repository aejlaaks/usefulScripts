"""
Usage: DPAssignmentGeneratori.py
---------------------------------
This script generates educational tasks and examples on specified topics using the DeepSeek AI API.
The generated content includes task descriptions, explanations, and examples with GraphViz diagrams.

Features:
- Generates 20 tasks per topic with detailed explanations
- Creates examples with Graphviz/DOT diagrams
- Saves output as Markdown files in a specified directory

Requirements:
- OpenAI Python package
- DeepSeek API key

To use:
1. Set your DeepSeek API key in the DEEPSEEK_API_KEY variable
2. Modify the 'topics' list in the main() function to include your desired topics
3. Update the 'base_directory' in main() to your preferred output location
4. Run the script: python DPAssignmentGeneratori.py
"""

import os
from openai import OpenAI

# Aseta DeepSeek API -yhteyden tiedot
DEEPSEEK_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# Luo DeepSeek API -asiakas
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)


def generate_tasks_and_examples(topic):
    prompt = (
         f"Olet tehtävä- ja esimerkkiluoja. Generoi tarkalleen 20 tehtävää ja esimerkkejä liittyen aiheeseen '{topic}'. "
        "Tehtävien tulisi kattaa aiheen peruskäsitteet ja edistyneemmät näkökohdat. Korosta erityisesti esimerkkien laajuutta ja laatua siten, että "
        "ne auttavat opiskelijaa ymmärtämään aihetta syvällisesti ja eri näkökulmista. "
        "Jokaiseen tehtävään tulee sisältyä:\n"
        "1. Laajempi selitys tehtävän tarkoituksesta: Miksi tehtävää tehdään ja miten se liittyy oppimiseen.\n"
        "2. Tehtävänanto: Selkeästi ja kattavasti selvitetty ohjeistus, mitä opiskelijan tulee tehdä.\n"
        "3. Esimerkki mahdollisesta vastauksesta:\n"
        "   - Sisällytä logiikkakaavio Graphviz-muodossa (DOT-kieli) tehtävän ratkaisuun. Haluan kaavioon gates kuin AND, OR, etc.\n"
        "   - Näytä, kuinka logiikka ohjelmoidaan vaihe vaiheelta :\n"
        "     1. Lisää lohkot, kuten ajastimet, portit tai kytkimet.\n"
        "     2. Määritä parametrien arvot, kuten viiveet tai kytkentälogiikka.\n"
        "     3. Yhdistä lohkot ja testaa logiikka ohjelmiston simulaattorilla.\n"
        "   - Käytä Graphviz/DOT-kieltä havainnollistamaan logiikkakaavio:\n"
        "Muista, että sisältösi on tarkoitettu pedagogiseen käyttöön, joten käytä selkeää, tarkkaa ja ystävällistä kieltä. "
        "Pyri antamaan opiskelijalle kaikki tarvittavat tiedot, jotta hän voi ymmärtää tehtävän ja oppia aiheen perusteellisesti."
    )

    try:
        # Tee API-kutsu
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": (
                         "Olet asiantuntija ja pedagogi, jonka tehtävänä on luoda tehtäviä ja esimerkkejä opiskelijoille. "
                         "Keskity varmistamaan, että luomasi tehtävät ovat pedagogisesti merkityksellisiä, tarjoavat monipuolisia näkökulmia, "
                         "ja sisältävät tarvittaessa visuaalisia elementtejä, kuten mermaid kaavioita. Huomioi myös eritasoisten opiskelijoiden tarpeet."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            stream=False,
            max_tokens=8000
        )

        # Tarkista ja tulosta raakadata
        print("Raakavastaus:", response)

        # Tarkista, onko 'choices'-avain vastauksessa ja sisältääkö se sisältöä
        if not response or not hasattr(response, "choices") or not response.choices:
            raise ValueError("API-vastaus ei sisällä 'choices'-osaa tai se on tyhjä.")

        # Hae ensimmäinen valinta
        tasks_and_examples = response.choices[0].message.content.strip()
        if not tasks_and_examples:
            raise ValueError("API-vastaus on tyhjä tai puutteellinen.")

        return tasks_and_examples

    except Exception as e:
        print(f"Virhe API-kutsussa aiheelle '{topic}': {e}")
        return None


def sanitize_file_name(name):
    """Poistaa epäkelvot merkit tiedostonimestä."""
    return "".join(c for c in name if c.isalnum() or c in "._- ").rstrip()


def save_tasks_to_file(directory, topic, content):
    # Luo hakemisto, jos sitä ei ole
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Luo tiedoston nimi ja tallennuspolku
    file_name = sanitize_file_name(topic[:150].strip().replace(" ", "_")) + ".md"
    file_path = os.path.join(directory, file_name)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Tehtävät tallennettu tiedostoon: {file_path}")
    except Exception as e:
        print(f"Virhe tallentaessa tiedostoa: {e}")


def main():
    topics = [
       "Ohm's law",
        "Resistance in electiricity",
        "Resistor in electiricity",
        "Capasitor in electiricity",
        "Diode"
        "series and parallel connection in circuits"
        "coil in electricity"
        "series and parallel connection with resistors and capacitors"

    ]

    base_directory = "C:\\Users\\Antti\\tehtavat"
    for topic in topics:
        print(f"Generoi tehtäviä ja esimerkkejä aiheesta: {topic}...")
        try:
            tasks_and_examples = generate_tasks_and_examples(topic)

            if tasks_and_examples:
                # Lisää otsikko ja sisältö Markdown-muotoon
                content = f"# Aihe: {topic}\n\n{tasks_and_examples}\n"
                save_tasks_to_file(base_directory, topic, content)
            else:
                print(f"Tehtävien luominen epäonnistui aiheelle: {topic}")

        except Exception as e:
            print(f"Virhe aiheen '{topic}' käsittelyssä: {e}")

    print(f"Tehtävät ja esimerkit tallennettu kansioon: {base_directory}")


if __name__ == "__main__":
    main()
