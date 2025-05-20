from taipy.gui import Gui
import taipy.gui.builder as tgb
import pandas as pd
import plotly.graph_objects as go
import json
from difflib import get_close_matches
from utils.constant import GEOJSON_REGIONS, EXPORTED_FILES_DIRECTORY

# ===== 1. Ladda data =====
df = pd.read_csv(EXPORTED_FILES_DIRECTORY / "regions_2020_2024_log.csv")
with open(GEOJSON_REGIONS, "r") as file:
    geojson = json.load(file)

# ===== 2. Globala variabler =====
selected_year = 2024
years = [2020, 2021, 2022, 2023, 2024]
region_map = None

# ===== 3. Hjälpfunktioner =====
def create_region_maps(df):
    props = [f["properties"] for f in geojson["features"]]
    region_codes = {p["name"]: p["ref:se:länskod"] for p in props}
    return [
        region_codes.get(get_close_matches(region, region_codes, 1)[0])
        for region in df["Region"]
    ]

def skapa_karta(df, year):
    codes = create_region_maps(df)
    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson,
        locations=codes,
        z=df[f"log_Antagna {year}"],
        featureidkey="properties.ref:se:länskod",
        colorscale="Blues",
        customdata=df[f"Antagna {year}"],
        marker_opacity=0.9,
        marker_line_width=0.1,
        text=df["Region"],
        hovertemplate="<b>%{text}</b><br>Antal antagna " + str(year) + ": %{customdata}<extra></extra>",
        showscale=False,
    ))
    fig.update_layout(
        mapbox=dict(style="white-bg", zoom=3.3, center=dict(lat=62.7, lon=13.9)),
        width=470,
        height=500,
        margin=dict(r=0, l=0, t=50, b=0),
        title=dict(text=f"ANTAGNA ELEVER ÅR {year}", x=0.06, y=0.75, font=dict(size=13)),
    )
    return fig

# ===== 4. Callback när året ändras =====
def on_year_change(state):
    state.region_map = skapa_karta(df, state.selected_year)

# ===== 5. Initiera första kartan =====
region_map = skapa_karta(df, selected_year)

# ===== 6. GUI-sida =====
with tgb.Page() as page:
    tgb.text("## Välj år för antagna elever")
    tgb.selector(
        label="År",
        value="{selected_year}",
        lov=years,
        dropdown=True,
        on_change=on_year_change
    )
    tgb.chart(figure="{region_map}")


# ===== 7. Starta GUI =====
Gui(page).run(port=8080, dark_mode=False)
