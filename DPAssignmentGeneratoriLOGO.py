import os
from openai import OpenAI

# Aseta DeepSeek API -yhteyden tiedot
DEEPSEEK_API_KEY = "sk-7c25c5c668724e2db72ecaff22201665"  # Vaihda tämä oikeaan API-avainarvoon
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# Luo DeepSeek API -asiakas
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)


def generate_tasks_and_examples(topic):
    prompt = (
        f"Olet tehtävä- ja esimerkkiluoja. Generoi tarkalleen 2 tehtävää ja esimerkkejä liittyen aiheeseen '{topic}'. "
        "Tehtävien tulisi kattaa aiheen peruskäsitteet ja edistyneemmät näkökohdat. Korosta erityisesti esimerkkien laajuutta ja laatua siten, että "
        "ne auttavat opiskelijaa ymmärtämään aihetta syvällisesti ja eri näkökulmista. "
        "Jokaiseen tehtävään tulee sisältyä:\n"
        "1. Laajempi selitys tehtävän tarkoituksesta: Miksi tehtävää tehdään ja miten se liittyy oppimiseen.\n"
        "2. Tehtävänanto: Selkeästi ja kattavasti selvitetty ohjeistus, mitä opiskelijan tulee tehdä.\n"
        "3. Esimerkki mahdollisesta vastauksesta:\n"
        "   - Käytä Siemens LOGO! -ohjelmaesimerkkejä aina, kun se on mahdollista.\n"
        "   - Sisällytä logiikkakaavio Graphviz-muodossa (DOT-kieli) tehtävän ratkaisuun.\n"
        "   - Näytä, kuinka logiikka ohjelmoidaan vaihe vaiheelta LOGO! Soft Comfort -ohjelmistossa:\n"
        "     1. Lisää lohkot, kuten ajastimet, portit tai kytkimet.\n"
        "     2. Määritä parametrien arvot, kuten viiveet tai kytkentälogiikka.\n"
        "     3. Yhdistä lohkot ja testaa logiikka ohjelmiston simulaattorilla.\n"
        "   - Käytä Graphviz/DOT-kieltä havainnollistamaan logiikkakaavio:\n"
        "Muista, että sisältösi on tarkoitettu pedagogiseen käyttöön, joten käytä selkeää, tarkkaa ja ystävällistä kieltä. "
        "Pyri antamaan opiskelijalle kaikki tarvittavat tiedot, jotta hän voi ymmärtää tehtävän ja oppia aiheen perusteellisesti."
    )

    try:
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Olet asiantuntija ja pedagogi, jonka tehtävänä on luoda tehtäviä ja esimerkkejä opiskelijoille. "
                        "Keskity varmistamaan, että luomasi tehtävät ovat pedagogisesti merkityksellisiä, tarjoavat monipuolisia näkökulmia, "
                        "ja sisältävät Siemens LOGO! -ohjelmaesimerkkejä sekä logiikkakaavioita Graphviz-muodossa (DOT-kieli). "
                        "Näytä vaiheittaiset ohjeet, joilla logiikkakaavio muunnetaan ohjelmaksi LOGO! Soft Comfort -ohjelmistossa. "
                        "Huomioi myös eritasoisten opiskelijoiden tarpeet ja käytä selkeitä selityksiä."
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
    file_name = sanitize_file_name(topic[:50].strip().replace(" ", "_")) + ".md"
    file_path = os.path.join(directory, file_name)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Tehtävät tallennettu tiedostoon: {file_path}")
    except Exception as e:
        print(f"Virhe tallentaessa tiedostoa: {e}")


def main():
    topics = [
      "Write logic and instruction for four-way intersection trafficlights control. We also need sensor for traffic "

    

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
