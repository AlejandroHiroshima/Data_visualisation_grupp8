import pandas as pd
import json
from utils.constant import GEOJSON_REGIONS, EXPORTED_FILES_DIRECTORY, DATA_DIRECTORY
import chardet

# ===== 1. Ladda data =====
df = pd.read_csv(EXPORTED_FILES_DIRECTORY / "regions_2020_2024_log.csv")
with open(GEOJSON_REGIONS, "r") as file:
    geojson = json.load(file)




# === Reading file anordnare Marcus ===
def reading_file_programs():

    dict_programs = {}

    df_program_2024 = pd.read_excel(
        DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2024.xlsx",
        sheet_name="Tabell 3",
        skiprows=5,
    )
    df_program_2024.rename(
        columns={"Utbildningsanordnare administrativ enhet": "Anordnare namn"},
        inplace=True,
    )
    dict_programs[2024] = df_program_2024

    df_program_2023 = pd.read_excel(
        DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2023.xlsx",
        sheet_name="Tabell 3",
        skiprows=5,
    )
    df_program_2023.rename(
        columns={"Utbildningsanordnare administrativ enhet": "Anordnare namn"},
        inplace=True,
    )
    dict_programs[2023] = df_program_2023

    df_program_2022 = pd.read_excel(
        DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2022.xlsx",
        sheet_name="Tabell 4",
    )
    df_program_2022.rename(
        columns={"Utbildningsanordnare administrativ enhet": "Anordnare namn"},
        inplace=True,
    )
    dict_programs[2022] = df_program_2022

    df_program_2021 = pd.read_excel(
        DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2021.xlsx",
        sheet_name="Tabell 4",
    )
    df_program_2021.rename(
        columns={"Utbildningsanordnare administrativ enhet": "Anordnare namn"},
        inplace=True,
    )
    dict_programs[2021] = df_program_2021

    df_program_2020 = pd.read_excel(
        DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2020.xlsx",
        sheet_name="Tabell 4",
    )
    df_program_2020.rename(
        columns={"Utbildningsanordnare administrativ enhet": "Anordnare namn"},
        inplace=True,
    )

    dict_programs[2020] = df_program_2020

    return dict_programs







def reading_file_course():

    dict_courses = {}

    df_kurser_2024 = pd.read_excel(
        DATA_DIRECTORY
        / "anordnare_resultat_kurser_2020-2024/resultat-2024-for-kurser-inom-yh.xlsx"
    )
    # df_kurser_2024.drop("Antal beviljade platser start och slut 2024", axis= 1, inplace=True)
    dict_courses[2024] = df_kurser_2024

    df_kurser_2023 = pd.read_excel(
        DATA_DIRECTORY
        / "anordnare_resultat_kurser_2020-2024/resultat-2023-for-kurser-inom-yh.xlsx"
    )
    dict_courses[2023] = df_kurser_2023

    df_kurser_2022 = pd.read_excel(
        DATA_DIRECTORY
        / "anordnare_resultat_kurser_2020-2024/resultat-2022-for-kurser-inom-yh.xlsx"
    )
    dict_courses[2022] = df_kurser_2022

    df_kurser_2021_lista = pd.read_excel(
        DATA_DIRECTORY
        / "anordnare_resultat_kurser_2020-2024/inkomna-ansokningar-juni-2021-for-korta-utbildningar-kurser-och-kurspaket.xlsx"
    )
    df_kurser_2021_beviljade = pd.read_excel(
        DATA_DIRECTORY
        / "anordnare_resultat_kurser_2020-2024/resultat-juni-2021-for-korta-utbildningar-kurser-och-kurspaket.xlsx"
    )
    df_kurser_2021 = pd.concat([df_kurser_2021_lista, df_kurser_2021_beviljade])

    if "Beslut" in df_kurser_2021.columns:

        df_kurser_2021["Beslut"] = df_kurser_2021["Beslut"].fillna("Avslag")

    else:
        df_kurser_2021["Beslut"] = "Avslag"

    dict_courses[2021] = df_kurser_2021

    df_kurser_2020_april = pd.read_excel(
        DATA_DIRECTORY
        / "anordnare_resultat_kurser_2020-2024/Beviljade-korta-utb-kurser-kurspaket-YH-april-2020-1.xlsx"
    )
    df_kurser_2020_juli = pd.read_excel(
        DATA_DIRECTORY
        / "anordnare_resultat_kurser_2020-2024/Beviljade-korta-utb-kurser-kurspaket-YH-juli-2020-2.xlsx"
    )
    df_kurser_2020 = pd.concat([df_kurser_2020_april, df_kurser_2020_juli])
    df_kurser_2020 = df_kurser_2020.rename(
        columns={
            "Anordnare": "Anordnare namn",
            "Platser med start 2020": "Antal beviljade platser 2020",
            "Platser med start 2021": "Antal beviljade platser 2021",
            "Platser med start och avslut 2020": "Antal beviljade platser start och slut 2020",
        },
    )
    df_kurser_2020["Beslut"] = "Beviljad"
    df_kurser_2020["Totalt antal beviljade platser"] = df_kurser_2020[
        [
            "Antal beviljade platser 2020",
            "Antal beviljade platser 2021",
            "Antal beviljade platser start och slut 2020",
        ]
    ].sum(axis=1)
    dict_courses[2020] = df_kurser_2020

    return dict_courses

# === End ===

# === Alex start ===

def read_csv_alex(sub_category, file_name, separator = ';'): # 1
    file_path = DATA_DIRECTORY / sub_category / file_name
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return pd.read_csv(
        file_path,
        encoding=result['encoding'],
        sep=separator
    ) 

def clean_dataframe(df): # 2
    df = df.query("kön == 'totalt'")
    df = df.query("ålder == 'totalt'")
    df = df.drop(["ålder", "kön"], axis=1)
    df.rename(columns={'utbildningens inriktning': 'Utbildningens Inriktning'}, inplace = True)
    for year in df.columns[3:]:   
        df[year] = pd.to_numeric(df[year].str.replace('..', '0'), errors='coerce')
    return df.set_index("Utbildningens Inriktning")