import taipy.gui.builder as tgb
from taipy.gui import Gui, notify
import pandas as pd
from pathlib import Path

DATA_DIRECTORY = Path(__file__).parents[0] / "data"


#funktioner:

def read_excel(sub_category, file_name, skiprows=5, skipfooter=4): # 1
    file_path = DATA_DIRECTORY / sub_category / file_name
    return pd.read_excel(
        file_path,
        skiprows=skiprows,
        skipfooter=skipfooter
    )
def clean_df1(df):
    index = df.columns[0]
    df = df.set_index(index)
    return df

try:
    df = read_excel(sub_category="statliga_bidrag", file_name="ek_4_utbet_arsplatser_utbomr.xlsx")
    df= clean_df1(df)
except FileNotFoundError as e:
    print(f"Fel: {e}")
    df = pd.DataFrame()

#initiera variabler:
educational_area = list(df.index)
schablon_moms = {
    "Data/IT": 74100,
    "Ekonomi, administration och försäljning": 66600,
    "Friskvård och kroppsvård": 79200,
    "Hotell, restaurang och turism":68700,
    "Hälso- och sjukvård samt socialt arbete": 7100,
    "Journalistik och information": 70600,
    "Juridik": 64100,
    "Kultur, media och design": 89400,
    "Lantbruk, djurvård, trädgård, skog och fiske":116700,
    "Pedagogik och undervisning": 75500,
    "Samhällsbyggnad och byggteknik": 74600,
    "Säkerhetstjänster": 66800,
    "Teknik och tillverkning": 91000,
    "Transporttjänster": 85200
}
selected_educational_area = ""

with tgb.Page() as government_grant_per_program:
    tgb.toggle(theme=True)
    with tgb.part(class_name="card text-center card-margin"):
        tgb.text("# Statliga bidrag på Utbildningsområde", mode="md")
    with tgb.part(class_name="container"): 
        with tgb.part(class_name="card card-margin"):
            with tgb.layout(columns="1 1 1"):
                with tgb.part(class_name="testing"):
                    tgb.selector(
                        value="{selected_educational_area}",
                        lov=educational_area,
                        dropdown=True,
                        multiple=False,
                        label="Välj Utbildningsområde",
                        class_name="fullwidth")

if __name__ == "__main__":
    Gui(
            government_grant_per_program,
        # [
        #     df_cleaned,
        #     years,
        #     start_year,
        #     end_year,
        #     educational_area,
        #     selected_educational_area,
        #     valid_end_years,
        #     chart,
        #     filter_data,
        #     update_end_year
        # ],
        css_file="assets/style.css"
    ).run(
        dark_mode=False,
        use_reloader=True,
        port=8080,
        title="Elvins Dashboard",
        watermark="Elvins Dashboard"
    )