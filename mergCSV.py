import os
import pandas as pd

def merge_csv_files(input_folder, output_file):
    """
    Yhdistää kaikki CSV-tiedostot kansiossa yhdeksi tiedostoksi.

    Args:
        input_folder (str): Polku kansioon, jossa CSV-tiedostot sijaitsevat.
        output_file (str): Polku ja nimi yhdistetylle CSV-tiedostolle.
    """
    # Lista kaikista CSV-tiedostoista kansiossa
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

    if not csv_files:
        print("Ei CSV-tiedostoja annetussa kansiossa.")
        return

    # Lista datakehyksistä yhdistämistä varten
    dataframes = []

    for csv_file in csv_files:
        file_path = os.path.join(input_folder, csv_file)
        print(f"Luetaan tiedosto: {file_path}")
        df = pd.read_csv(file_path)
        dataframes.append(df)

    # Yhdistetään kaikki datakehykset
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Tallennetaan yhdistetty datakehys tiedostoon
    combined_df.to_csv(output_file, index=False)
    print(f"CSV-tiedostot yhdistetty ja tallennettu tiedostoon: {output_file}")

# Esimerkki käytöstä
if __name__ == "__main__":
    input_folder = input("Anna polku kansioon, jossa CSV-tiedostot ovat: ")
    output_file = "/home/antti/MetaGPT/data/cryptocurrency_historical_prices.csv"
    merge_csv_files(input_folder, output_file)
