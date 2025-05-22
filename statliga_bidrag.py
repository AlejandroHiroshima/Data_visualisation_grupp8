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

def clean_df(df):
    index = df.columns[0]
    df = df.set_index(index)
    return df

def clean_columns(column):
    if isinstance(column, int):
        return column  
    new_column = column.replace(",", "")
    try: 
        return int(new_column)
    except ValueError:
        return column


try:
    df = read_excel(sub_category="statliga_bidrag", file_name="ek_4_utbet_arsplatser_utbomr.xlsx")
    df= clean_df(df)
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
year = ""
df.columns = [clean_columns(column) for column in df.columns]
years = df.columns
year_students = "-"
schablon = "-"
government_funding = "-"

# Filter funktion
def filter_data(state):
    if not state.selected_educational_area:
        notify(state, "warning", "Välj ett Utbildningsområde")
        return
    if not state.year:
        notify(state, "warning", "Välj ett År")
    area= state.selected_educational_area
    year = int(state.year)
    year_students = df.loc[area,year]
    schablon = schablon_moms[area]
    government_funding = year_students * schablon

    state.year_students= year_students
    state.schablon = schablon
    state.government_funding = government_funding


with tgb.Page() as government_grant_per_program:
    tgb.toggle(theme=True)
    with tgb.part(class_name="card text-center card-margin"):
        tgb.text("# Statliga bidrag per **Utbildningsområde** ", mode="md")

    with tgb.part(class_name="container government"):
        with tgb.part(class_name="card card-margin"):
            with tgb.layout(columns="3 1 2"):
                with tgb.part(class_name="testing"):
                    tgb.selector(
                        value="{selected_educational_area}",
                        lov=educational_area,
                        dropdown=True,
                        multiple=False,
                        label="Välj Utbildningsområde",
                        class_name="fullwidth")
                with tgb.part(class_name="text-center"):
                    tgb.selector(
                        value= "{year}",
                        lov= years,
                        label= "Välj År",
                        dropdown=True)
                with tgb.part(class_name="text-center"):
                    tgb.button(label="Filtrera",
                               class_name="plain filter-button government_button",
                               on_action=filter_data)

    with tgb.part(class_name="container government"):
        with tgb.layout(columns="1 1 1"): 
            with tgb.part(class_name="card card-margin text-center"):
                tgb.text("### Statsbidrag", mode="md")
                tgb.text("**{government_funding:,.0f}** kr", mode="md", class_name="kpi-value")

            with tgb.part(class_name="card card-margin text-center"):
                tgb.text("### Antal årsplatser", mode="md")
                tgb.text("**{year_students:,.1f}**", mode="md", class_name="kpi-value")

            with tgb.part(class_name="card card-margin text-center"):
                tgb.text("### Schablonbelopp", mode="md")
                tgb.text("**{schablon:,.0f}** kr", mode="md", class_name="kpi-value")                    

if __name__ == "__main__":
    Gui(
        government_grant_per_program,
        [
            df,
            educational_area,
            schablon_moms,
            selected_educational_area,
            year,
            years,
            year_students,
            schablon,
            government_funding
        ],
        css_file="assets/style.css"
    ).run(
        dark_mode=False,
        use_reloader=True,
        port=8080,
        title="Elvins Dashboard",
        watermark="Elvins Dashboard"
    )