"""
Usage: DPAssignmentGeneratoriLOGO.py
------------------------------------
This script generates educational tasks and examples on specified topics using the DeepSeek AI API,
with built-in rate limiting and error handling.

Features:
- Generates 2 tasks per topic with detailed explanations
- Implements token-based rate limiting to avoid API throttling
- Handles HTTP timeouts and connection errors
- Logs failed topic generation for later retry
- Saves output as Markdown files in a specified directory

Requirements:
- OpenAI Python package
- httpx package
- DeepSeek API key

To use:
1. Set your DeepSeek API key in the DEEPSEEK_API_KEY variable
2. Modify the 'topics' list in the main() function to include your desired topics
3. Update the 'base_directory' in main() to your preferred output location
4. Run the script: python DPAssignmentGeneratoriLOGO.py
"""

import os
import time
from datetime import datetime
from json import JSONDecodeError

import httpx
from openai import OpenAI

# Aseta DeepSeek API -yhteyden tiedot
DEEPSEEK_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
# DEEPSEEK_BASE_URL = "http://localhost:8000/v1"  # For local development

# Luo DeepSeek API -asiakas
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
    http_client=httpx.Client(timeout=1200)  # Aseta timeout 1200 sekuntiin (20 minuuttia)
)
# Add these global variables
TOKEN_LIMIT = 8000
TOKEN_RESET_INTERVAL = 60  # seconds
last_request_time = datetime.now()
tokens_used = 0


def wait_for_token_reset():
    global last_request_time, tokens_used
    current_time = datetime.now()
    time_since_last_request = (current_time - last_request_time).total_seconds()

    if time_since_last_request < TOKEN_RESET_INTERVAL:
        if tokens_used >= TOKEN_LIMIT:
            sleep_time = TOKEN_RESET_INTERVAL - time_since_last_request
            print(f"Rate limit reached. Waiting for {sleep_time:.2f} seconds.")
            time.sleep(sleep_time)
            tokens_used = 0
            last_request_time = datetime.now()
    else:
        tokens_used = 0
        last_request_time = current_time

def generate_tasks_and_examples(topic):
    global tokens_used

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
        wait_for_token_reset()

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

        # Update tokens used
        tokens_used += response.usage.total_tokens
        print(f"Tokens used in this request: {response.usage.total_tokens}")
        print(f"Total tokens used: {tokens_used}")

        # Tarkista ja tulosta raakadata
        print("Raakavastaus:", response)

        # Tarkista, onko 'choices'-avain vastauksessa ja sisältääkö se sisältöä
        if not response or not response.choices:
            raise ValueError("Empty or invalid API response")

        tasks_and_examples = response.choices[0].message.content.strip()
        if not tasks_and_examples:
            raise ValueError("Empty content in API response")

        return tasks_and_examples


    except JSONDecodeError as e:

        print(f"JSON decoding error for topic '{topic}': {e}")

    except ValueError as e:

        print(f"Value error for topic '{topic}': {e}")

    except Exception as e:

        print(f"Unexpected error for topic '{topic}': {e}")

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
        "Automated Pump Control with Siemens LOGO!: Implementing logic for water level management and pressure regulation.",
        "Siemens LOGO! in Industrial Fan and Ventilation Systems: Controlling airflow, temperature, and exhaust management.",
        "Traffic Light and Signal Control in Industrial Facilities Using Siemens LOGO!: Programming sequential logic for safety.",
        "Using Siemens LOGO! for Packaging and Sorting Systems: Automating weight, size sorting, and packaging operations.",
        "Siemens LOGO! in Warehouse Automation: Controlling conveyors, palletizers, and automated guided vehicles (AGVs).",
        "Temperature and Humidity Control with Siemens LOGO!: Implementing environmental monitoring and climate control in storage areas.",
        "Industrial Alarm Systems with Siemens LOGO!: Configuring alert notifications for equipment failures and emergency shutdowns.",
        "Siemens LOGO! for Energy Management: Optimizing power consumption and peak load monitoring in industrial setups.",
        "Automated Gate and Barrier Control with Siemens LOGO!: Controlling access systems for warehouses and production sites.",
        "Liquid Level Monitoring and Tank Control Using Siemens LOGO!: Implementing automatic refilling and emptying sequences.",
        "Industrial Batch Processing with Siemens LOGO!: Automating multi-step production processes and tracking cycles.",
        "Siemens LOGO! in Food Processing Industry: Automating mixing, weighing, and packaging systems.",
        "Industrial Boiler and Heating System Automation with Siemens LOGO!: Implementing temperature control and safety mechanisms.",
        "Siemens LOGO! for Material Handling Systems: Controlling robotic arms, hoists, and cranes in production environments.",
        "Predictive Maintenance Systems Using Siemens LOGO!: Monitoring motor loads and vibration levels for preventive maintenance.",
        "SCADA Integration with Siemens LOGO! in Industrial Monitoring: Connecting LOGO! to centralized supervisory control systems.",
        "Remote Control and Cloud Integration with Siemens LOGO!: Enabling industrial IoT connectivity for real-time monitoring and analytics."
        # Introduction
        "Siemens LOGO! in Industrial Automation: Overview of LOGO! capabilities, applications, and its role in industrial automation.",

        # Basic Programming
        "Siemens LOGO! Programming Basics: Understanding function blocks, ladder logic, and parameter settings.",
        "Siemens LOGO! vs. Other PLCs: Differences, use cases, and benefits of using LOGO! over traditional PLCs.",
        "Siemens LOGO! Software and Interfaces: Introduction to LOGO! Soft Comfort, web-based control, and remote access.",

        # Etching and Cleaning Systems
        "Siemens LOGO! in Etching and Cleaning Systems: Process automation for syövytys- ja puhdistuslaitteistot (etching and cleaning equipment).",
        "Siemens LOGO! for Chemical Dosage Control: Automating acid/base mixing processes.",
        "Siemens LOGO! Safety Measures in Cleaning Systems: Ensuring chemical spill detection and ventilation control.",

        # Silo Automation
        "Siemens LOGO! in Silo Automation: Monitoring and controlling siilot (silos) for bulk material management.",
        "Siemens LOGO! Level Sensors in Silos: Capacitive, ultrasonic, and load cell integration.",
        "Siemens LOGO! Automated Silo Refilling: Using sensors to detect low levels and trigger refilling mechanisms.",

        # Fill Level Detection
        "Siemens LOGO! for Fill Level Detection: Täyttöasteen tunnistus (fill level monitoring) for industrial processes.",
        "Siemens LOGO! Liquid vs. Solid Level Measurement: Handling different material types in automation.",
        "Siemens LOGO! Overfill Protection: Configuring alarms and emergency shutoffs for safety.",

        # Conveyor System Control
        "Siemens LOGO! in Conveyor System Control: Kuljettimien ohjaus (conveyor control) in industrial applications.",
        "Siemens LOGO! Conveyor Speed Control: Implementing variable speed drives and logic programming.",
        "Siemens LOGO! Fault Detection in Conveyor Systems: Monitoring jams, slippages, and system failures.",

        # Pump and Valve Control
        "Siemens LOGO! for Pump and Valve Control: Automating pump sequences and venttiilien ohjaus (valve automation).",
        "Siemens LOGO! Multi-Pump Systems: Managing parallel or alternating pump operation.",
        "Siemens LOGO! Pressure Regulation with Sensors: Integrating pressure sensors for real-time adjustments.",

        # Industrial Lighting Control
        "Siemens LOGO! in Industrial Lighting Control: Automating valaistusten ohjaus (lighting control) for factories and warehouses.",
        "Siemens LOGO! Timer-Based Lighting Control: Scheduling lights based on shift hours and daylight sensors.",
        "Siemens LOGO! Motion-Activated Lighting: Using PIR sensors for energy efficiency in large facilities.",

        # Greenhouse Automation
        "Siemens LOGO! in Greenhouse Automation: Automating kasvihuoneautomatiikka (greenhouse processes).",
        "Siemens LOGO! Temperature and Humidity Control: Implementing sensors for climate regulation.",
        "Siemens LOGO! Irrigation System Automation: Managing water cycles based on soil moisture levels.",

        # Access Control and Gates
        "Siemens LOGO! for Access Control and Gates: Automating kulkuporttien ohjaus (entry and exit points).",
        "Siemens LOGO! RFID-Based Access Control: Integrating card readers for secure entry.",
        "Siemens LOGO! Time-Based Gate Automation: Restricting access based on schedules and shift changes.",

        # Packaging Machines
        "Siemens LOGO! in Packaging Machines: Automating pakkauskoneet (packaging line operations).",
        "Siemens LOGO! Product Counting and Sorting: Configuring optical sensors and logic counters.",
        "Siemens LOGO! Labeling and Barcode Integration: Automating package tracking and quality control.",

        # ASi Bus Control Systems
        "Siemens LOGO! in ASi Bus Control Systems: Implementing ASi-väyläohjauksissa (AS-Interface bus systems).",
        "Siemens LOGO! Decentralized Control with ASi: Reducing wiring complexity in industrial setups.",
        "Siemens LOGO! Safety Applications in ASi Networks: Implementing emergency stop and safety relays.",

        # HVAC and Ventilation Control
        "Siemens LOGO! for HVAC and Ventilation Control: Automating ilmastointilaitteet (HVAC systems).",
        "Siemens LOGO! Temperature Regulation in Factories: Configuring heating and cooling systems.",
        "Siemens LOGO! CO2 and Air Quality Monitoring: Using sensors for real-time adjustments.",

        # Remote Monitoring and Control
        "Siemens LOGO! Remote Monitoring and Control: Using LOGO! Web Editor and cloud-based systems.",
        "Siemens LOGO! SMS and Email Notifications: Configuring event-based alerts for maintenance personnel.",
        "Siemens LOGO! Remote Troubleshooting and Diagnostics: Accessing fault logs and adjusting settings remotely.",

        # Safety and Compliance
        "Siemens LOGO! Safety Considerations in Industrial Automation: Implementing emergency stop mechanisms.",
        "Siemens LOGO! Compliance with Industrial Standards: Meeting ISO, IEC, and EU safety regulations.",
        "Siemens LOGO! Redundancy and Fail-Safe Mechanisms: Ensuring uninterrupted automation operations."
    ]

    base_directory = "C:\\Users\\Antti\\tehtavat"
    delay_between_tasks = 30  # 6 minuuttia

    while topics:
        current_topic = topics[0]
        print(f"Generoi tehtäviä ja esimerkkejä aiheesta: {current_topic}...")
        try:
            tasks_and_examples = generate_tasks_and_examples(current_topic)

            if tasks_and_examples:
                content = f"# Aihe: {current_topic}\n\n{tasks_and_examples}\n"
                save_tasks_to_file(base_directory, current_topic, content)
                topics.pop(0)  # Poista onnistuneesti käsitelty aihe listasta
                print(f"Aihe '{current_topic}' käsitelty onnistuneesti.")
            else:
                print(f"Tehtävien luominen epäonnistui aiheelle: {current_topic}")
                # Siirrä epäonnistunut aihe listan loppuun
                topics.append(topics.pop(0))

        except Exception as e:
            print(f"Virhe aiheen '{current_topic}' käsittelyssä: {e}")
            # Siirrä epäonnistunut aihe listan loppuun
            topics.append(topics.pop(0))

        # Lisää viive ennen seuraavaa yritystä
        if topics:
            print(f"Odotetaan {delay_between_tasks} sekuntia ennen seuraavaa yritystä...")
            time.sleep(delay_between_tasks)

    print("Kaikki aiheet käsitelty onnistuneesti!")
    print(f"Tehtävät ja esimerkit tallennettu kansioon: {base_directory}")


if __name__ == "__main__":
    main()

def log_failed_topics(failed_topics, log_file_path):
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        log_file.write("Aiheet, joita ei saatu käsiteltyä API-virheiden vuoksi:\n\n")
        for topic in failed_topics:
            log_file.write(f"- {topic}\n")
    print(f"Lista epäonnistuneista aiheista tallennettu tiedostoon: {log_file_path}")
