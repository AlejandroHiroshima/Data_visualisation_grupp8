from taipy.gui import Gui
import taipy.gui.builder as tgb
import numpy as np 
import plotly.graph_objects as go 
import duckdb as db
from utils.constant import GEOJSON_REGIONS, EXPORTED_FILES_DIRECTORY
import json
import pandas as pd 
from difflib import get_close_matches

df = pd.read_csv(EXPORTED_FILES_DIRECTORY / "regions_2020_2024_log.csv")

with open(GEOJSON_REGIONS, "r") as file:
    geojson = json.load(file)

def create_region_maps(df):
    properties = [feature.get("properties") for feature in geojson.get("features")]
    regions_codes = {
        property.get("name"): property.get("ref:se:länskod") for property in properties
    }

    region_codes_map = []

    for region in df["Region"]:
        region_name = get_close_matches(region, regions_codes.keys(), n=1)[0]
        code = regions_codes[region_name]
        region_codes_map.append(code)

    return region_codes_map



def skapa_karta(df, year = 2020):

    region_codes_map = create_region_maps(df)


    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=geojson,
            locations=region_codes_map,
            z=df[f"log_Antagna {year}"],
            featureidkey="properties.ref:se:länskod",
            colorscale="Blues",
            customdata=df[f"Antagna {year}"],
            marker_opacity=0.9,
            marker_line_width=0.1,
            text=df.index,
            hovertemplate="<b>%{text}</b><br>Antal antagna " + str(year) + ": %{customdata}<extra></extra>",
            showscale=False,
        )
    )

    fig.update_layout(
        mapbox=dict(style="white-bg", zoom=3.3, center=dict(lat=62.6952, lon=13.9149)),
        width=470,
        height=500,
        margin=dict(r=0, l=0, t=50, b=0),
        title=dict(
            text=f"ANTAGNA ELEVER ÅR {year}",
            x=0.06,
            y=0.75,
            font=dict(size=13),
        ),
    )
    return fig


region_map = skapa_karta(df, year = 2024) 

with tgb.Page() as page:
    tgb.text("Välj utbildningsområde", mode="md")
    tgb.selector(
        value="{df}",
        dropdown=True
    )
    tgb.chart(figure="{region_map}")

Gui(page).run(use_reloader=True, port= 8080, dark_mode=False)
