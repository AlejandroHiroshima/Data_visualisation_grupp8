import taipy.gui.builder as tgb
from taipy.gui import Gui, notify
import pandas as pd
from utils.constant import SCHABLON_MOMS
from backend.data_processing import read_excel, clean_df, clean_columns


selected_educational_area = ""
year = ""
year_students = "-"
schablon = "-"
government_funding = "-"

try:
    df = read_excel(sub_category="statliga_bidrag", file_name="ek_4_utbet_arsplatser_utbomr.xlsx")
    df= clean_df(df)
except FileNotFoundError as e:
    print(f"Fel: {e}")
    df = pd.DataFrame() 

educational_area = list(df.index[:-2])
years = df.columns
df.columns = list(map(clean_columns, df.columns))

def filter_data(state):
    if not state.selected_educational_area:
        notify(state, "warning", "Välj ett Utbildningsområde")
        return
    if not state.year:
        notify(state, "warning", "Välj ett År")
    state.year_students = df.loc[state.selected_educational_area, int(state.year)]
    state.schablon = SCHABLON_MOMS[state.selected_educational_area]
    state.government_funding = state.year_students * state.schablon

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
        css_file="assets/style.css"
    ).run(
        dark_mode=False,
        use_reloader=True,
        port=8080,
        title="Elvins Dashboard",
        watermark="Elvins Dashboard"
    )