import plotly.graph_objects as go
from difflib import get_close_matches
from backend.data_processing import df
from backend.data_processing import geojson

# ===== 3. Hjälpfunktioner =====
def create_region_maps(df):
    props = [f["properties"] for f in geojson["features"]]
    region_codes = {p["name"]: p["ref:se:länskod"] for p in props}
    return [
        region_codes.get(get_close_matches(region, region_codes, 1)[0])
        for region in df["Region"]
    ]

def create_map(df, year):
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
        mapbox=dict(style="carto-darkmatter", zoom=3.3, center=dict(lat=62.7, lon=13.9)),
        width=470,
        height=500,
        margin=dict(r=0, l=0, t=50, b=0),
        paper_bgcolor= "rgba(0,0,0,0)",
        plot_bgcolor= "rgba(0,0,0,0)"
)
    return fig

