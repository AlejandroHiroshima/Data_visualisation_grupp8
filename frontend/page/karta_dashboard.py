import taipy.gui.builder as tgb
from frontend.frontend_map import create_map
from Backend.data_processing import df 

# ===== Globala variabler =====
selected_year = 2024
years = [2020, 2021, 2022, 2023, 2024]
region_map = None

# ===== Initiera KPI-variabler =====
kpi_total_admitted_sweden = "-"
kpi_top_region = "-"
kpi_top_region_value = "-"
kpi_lowest_region = "-"
kpi_lowest_region_value = "-"

# ===== Callback när året ändras =====
def on_year_change(state):
    year_df = df[df["år"] == state.selected_year]

    if year_df.empty:
        state.kpi_total_admitted_sweden = "-"
        state.kpi_top_region = "-"
        state.kpi_top_region_value = "-"
        state.kpi_lowest_region = "-"
        state.kpi_lowest_region_value = "-"
    else:
        total = year_df["antal_antagna"].sum()
        top_row = year_df.loc[year_df["antal_antagna"].idxmax()]
        bottom_row = year_df.loc[year_df["antal_antagna"].idxmin()]

        state.kpi_total_admitted_sweden = int(total)
        state.kpi_top_region = top_row["region"]
        state.kpi_top_region_value = int(top_row["antal_antagna"])
        state.kpi_lowest_region = bottom_row["region"]
        state.kpi_lowest_region_value = int(bottom_row["antal_antagna"])

    state.region_map = create_map(df, state.selected_year)

# ===== Callback när året ändras =====
def on_year_change(state):
    state.region_map = create_map(df, state.selected_year)

# ===== Initiera första kartan =====
region_map = create_map(df, selected_year)

# ===== GUI-sida =====
with tgb.Page() as map_page:
    tgb.navbar()
    with tgb.part(class_name="card text-center card-margin"):
        tgb.text("# ANTAGNA STUDENTER VID START", mode="md")

    tgb.html("br")
    with tgb.part(class_name="container"): 
        with tgb.part(class_name="card card-margin"):
            with tgb.layout(columns="3 2 1"):
                with tgb.part(class_name="education_area_filter"):
                    tgb.selector(
                        value="{selected_year}",
                        lov=years,
                        dropdown=True,
                        on_change=on_year_change,
                        label="Välj ett år",
                        class_name="fullwidth"
                    )

    tgb.html("br")
    with tgb.part(class_name="container"):
        with tgb.layout(columns="1 1 1"):
            with tgb.part(class_name="card card-margin text-center"):
                tgb.text("### Totalt antagna", mode="md")
                tgb.text("**{kpi_total_admitted_sweden:,}**", mode="md")

            with tgb.part(class_name="card card-margin text-center"):
                tgb.text("### Regionen med flest studenter", mode="md")
                tgb.text("**{kpi_top_region}**", mode="md")
                tgb.text("**{kpi_top_region_value:,}** studenter", mode="md")

            with tgb.part(class_name="card card-margin text-center"):
                tgb.text("### Minst antagna region", mode="md")
                tgb.text("**{kpi_lowest_region}**", mode="md")
                tgb.text("**{kpi_lowest_region_value:,}** studenter", mode="md")
                
    tgb.html("br")                             
    with tgb.part(class_name="container"):
        with tgb.part(class_name="card"):
            tgb.chart(figure="{region_map}",class_name="mx-auto")