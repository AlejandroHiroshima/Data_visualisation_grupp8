from taipy.gui import Gui



def filtrera_år(result, år):
    kolumnnamn = f"Antagna {år}"
    result_filtered = result.copy()
    result_filtered["log_antagna"] = np.log(result_filtered[kolumnnamn] + 1)
    result_filtered["antagna"] = result_filtered[kolumnnamn]
    return result_filtered


def skapa_karta(result, geojson, region_codes_map, år):
    data_för_år = filtrera_år(result, år)

    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=geojson,
            locations=region_codes_map,
            z=data_för_år["log_antagna"],
            featureidkey="properties.ref:se:länskod",
            colorscale="Blues",
            customdata=data_för_år["antagna"],
            marker_opacity=0.9,
            marker_line_width=0.1,
            text=data_för_år["Region"],
            hovertemplate="<b>%{text}</b><br>Antal antagna " + str(år) + ": %{customdata}<extra></extra>",
            showscale=False,
        )
    )

    fig.update_layout(
        mapbox=dict(style="white-bg", zoom=3.3, center=dict(lat=62.6952, lon=13.9149)),
        width=470,
        height=500,
        margin=dict(r=0, l=0, t=50, b=0),
        title=dict(
            text=f"ANTAGNA ELEVER ÅR {år}",
            x=0.06,
            y=0.75,
            font=dict(size=13),
        ),
    )
    return fig


# Delad variabel som användaren styr via dropdown
valår = 2024  # default

# Uppdaterad dynamisk figur
def get_figur():
    return skapa_karta(result, json_data, region_codes_map, valår)

# Taipy layout
page = """
# Antagna elever per län

<|{valår}|selector|lov=2020;2021;2022;2023;2024|label=Välj år|on_change=on_year_change|>

<|get_figur|chart|width=100%|height=600px|>
"""

# Callback-funktion när användaren byter år
def on_year_change(state):
    state.get_figur = get_figur()

Gui(page).run()