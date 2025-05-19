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

def create_linechart(df, **options):
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

try:
    df = read_csv(sub_category="2024_kurser", file_name="studerande_examinerad_yrkeshogskola.csv")
except FileNotFoundError as e:
    print(f"Fel: {e}")
    df = pd.DataFrame() 
 
df_cleaned = clean_dataframe(df)
chart = create_linechart(df_cleaned, xlabel= "År", ylabel= "Antal Studerande")

with tgb.Page() as page: 
    with tgb.part(class_name="container card"):
        tgb.text("# Studenter på Yrkeshögskola", mode="md")
        tgb.text("### Utveckling över tid per utvecklingsområde", mode="md")
        with tgb.part(class_name="card"):
            tgb.text("Rådata:", mode="md")
            tgb.table("{df_cleaned}")
            tgb.chart(figure="{chart}")
if __name__ == "__main__":
    Gui(page).run(dark_mode=False, use_reloader=True, port=8080)