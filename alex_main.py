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
years= df_cleaned.columns[3:].tolist()
start_year = int(years[0])
end_year = int(years[-1]) 
educational_area = df_cleaned.index.tolist()
chart = create_linechart(df_cleaned, xlabel= "År", ylabel= "Antal Studerande")

with tgb.Page() as number_students_educationalarea_year:
    tgb.toggle(theme=True)
    with tgb.part(class_name="card text-center card-margin"):
        tgb.text("# Studenter på **Yrkeshögskola**", mode="md")
    

    with tgb.part(class_name="container"):
        with tgb.part(class_name="card card-margin"):
            with tgb.layout(columns="3 2 1"):
                with tgb.part(class_name= "education_area_filter"):
                    tgb.selector(
                        value="{educational_area}",
                        lov=educational_area[0],
                        dropdown=True,
                        multiple=True,
                        label="Välj utbildningsområde",
                        class_name="fullwidth"
                    )

                with tgb.part():
                    with tgb.layout(columns="1 1"):
                        tgb.selector(
                            value="{start_year}",
                            lov=years[:-1],
                            label="Välj startår",
                            dropdown=True,
                            on_change=update_end_year,
                            class_name="fullwidth"
                        )
                        tgb.selector(
                            value="{end_year}",
                            lov=years,
                            dropdown=True,
                            label="Välj slutår",
                            class_name="fullwidth"
                        )

                with tgb.part(class_name="text-center"):
                    tgb.button(label="Filtrera", class_name="plain filter-button fullwidth")

   
    with tgb.part(class_name="container"):
        with tgb.part(class_name="card"):
            tgb.text("### Utveckling över tid per utbildningsområde", mode="md")
            tgb.chart(figure="{chart}")
                




if __name__ == "__main__":
    Gui(number_students_educationalarea_year, css_file="assets/style.css").run(dark_mode=False, 
                                                use_reloader=True, 
                                                port=8080,
                                                title= "Elvins Dashboard",
                                                watermark="Elvins Dashboard",)