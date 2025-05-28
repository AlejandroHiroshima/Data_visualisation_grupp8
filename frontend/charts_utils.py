import plotly.express as px
import pandas as pd

def horizontal_bar_options(ax, **options):
    ax.invert_yaxis()

    ax.set_title(
        label=options.get("title", ""),
        pad=options.get("title_pad", 10),
        loc="left",
    )
    ax.set_xlabel(options.get("xlabel", ""), loc="left")
    ax.set_ylabel(options.get("ylabel", ""), rotation=options.get("ylabel_rotation", 0))
    ax.yaxis.set_label_coords(
        options.get("ylabel_x_coord", -0.1), options.get("ylabel_y_coord", 1)
    )

    ax.legend().remove()

    return ax


# === Alex line chart func ===
def create_linechart(df, **options): # 5
    if df.empty:
        df_long = pd.DataFrame(columns=["Utbildningens Inriktning", "År", "Antal studerande"])
    else:
        df_long = df.reset_index().melt(
            id_vars="Utbildningens Inriktning",
            var_name="År",
            value_name="Antal studerande" 
        )
    fig = px.line(
        df_long,
        x="År",
        y="Antal studerande",
        color="Utbildningens Inriktning", 
        markers=True,
        labels={"År": options.get("xlabel", "År"), "Antal studerande": options.get("ylabel", "Antal studerande")},
    )
    fig.update_layout( 
        plot_bgcolor="white",
        margin=dict(t=0, l=40, r=30, b=50),
        legend_title="Utbildningsinriktning"
    )
    return fig