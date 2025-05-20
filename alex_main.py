import taipy.gui.builder as tgb
from taipy.gui import Gui
import pandas as pd
import chardet
from pathlib import Path
import plotly.express as px

DATA_DIRECTORY = Path(__file__).parents[0] / "data"

#funktioner:

def read_csv(sub_category, file_name, separator = ';'): # läser in csvfil, returnerar en df
    file_path = DATA_DIRECTORY / sub_category / file_name
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())

    return pd.read_csv(
        file_path,
        encoding=result['encoding'],
        sep=separator
    )

def clean_dataframe(df): # rensar df, använder kön och ålder == total, och tar sen bort de kolumnerna
    df = df.query("kön == 'totalt'")
    df = df.query("ålder == 'totalt'")
    df = df.drop(["ålder", "kön"], axis=1)
    for year in df.columns[3:]:
        df[year] = pd.to_numeric(df[year].str.replace('..', '0'), errors='coerce')
    return df.set_index("utbildningens inriktning")

def create_linechart(df, **options): # Skapar en linechart
    df_long = df.reset_index().melt(
        id_vars="utbildningens inriktning",
        var_name="År",
        value_name="Antal studerande"
    )
    fig = px.line(
        df_long,
        x="År",
        y="Antal studerande",
        color="utbildningens inriktning",
        markers=True,
        labels={"År": options.get("xlabel", "År"), "Antal studerande": options.get("ylabel", "Antal studerande")},
    )
    fig.update_layout(
        plot_bgcolor="white",
        margin=dict(t=0, l=40, r=30, b=50),
        legend_title="Utbildningsinriktning"
    )
    return fig

def update_end_year(state):
    state.end_year = max(state.start_year, state.end_year)

try:
    df = read_csv(sub_category="2024_kurser", file_name="studerande_examinerad_yrkeshogskola.csv")
except FileNotFoundError as e:
    print(f"Fel: {e}")
    df = pd.DataFrame() 
 
# start variabler:
df_cleaned = clean_dataframe(df)
years= df_cleaned.columns[3:]
start_year = int(years[0])
end_year = int(years[-1]) 
educational_area = []
chart = create_linechart(df_cleaned, xlabel= "År", ylabel= "Antal Studerande")

with tgb.Page() as number_students_educationalarea_year: #Taipy
    with tgb.part(class_name="container card"):
        with tgb.layout(columns="2 1"):
            with tgb.part(class_name="card"):
                tgb.text("# Studenter på Yrkeshögskola", mode="md")
                tgb.text("### Utveckling över tid per utvecklingsområde", mode="md")
                tgb.chart(figure="{chart}")
            with tgb.part(class_name="card"):
                tgb.text("**Filtrera data: År och Utbildnings Område**", mode="md")
                tgb.text("Välj utbildningsområde:")
                tgb.selector(value="{educational_area}", lov=df_cleaned.index, dropdown=True, multiple=True)
                tgb.text("Välj start år:")
                tgb.slider(value="{start_year}", min=start_year, max=end_year-1, step=1, show_value=True, label="Startår", on_change=update_end_year)
                tgb.text("Välj slut år:")
                tgb.slider(value="{end_year}", min="{start_year}", max=end_year, step=1, show_value=True, label="Slutår")
                




if __name__ == "__main__":
    Gui(number_students_educationalarea_year).run(dark_mode=False, use_reloader=True, port=8080)