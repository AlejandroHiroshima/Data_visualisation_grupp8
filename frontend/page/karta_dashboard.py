import taipy.gui.builder as tgb
from frontend.frontend_map import create_map
from backend.data_processing import df 

# ===== Global variables =====
selected_year = 2020
years = [2024, 2023, 2022, 2021, 2020]
region_map = None

# ===== Initating KPI-variables =====
kpi_total_admitted_sweden = "N/A"
kpi_top_region = "N/A"
kpi_top_region_value = "N/A"
kpi_lowest_region = "N/A"
kpi_lowest_region_value = "N/A"

percentage_change = "N/A"
top_region_share = "N/A"
bottom_region_share = "N/A"

# ===== Callback when the years are changing =====
def on_year_change(state):
    year_df = df[f"Antagna {state.selected_year}"]
    region_df = df["Region"] 

    total = year_df.sum()
    top_row = year_df.iloc[year_df.idxmax()]
    bottom_row = year_df.iloc[year_df.idxmin()]
    top_region = region_df.iloc[year_df.idxmax()]
    bottom_region = region_df.iloc[year_df.idxmin()]
    
    base_year_total = df["Antagna 2020"].sum()
    if base_year_total != 0:
        percentage = ((total - base_year_total) / base_year_total) * 100
        state.percentage_change = f"{percentage:.2f}%"
    else:
        state.percentage_change = "N/A"

    if total != 0:
        top_share = (top_row/total) * 100
        bottom_share = (bottom_row/total) * 100
        state.top_region_share = f"{top_share:.2f}%"
        state.bottom_region_share = f"{bottom_share:.2f}%"
    else:
        state.top_region_share = "N/A"
        state.bottom_region_share = "N/A"


    state.kpi_total_admitted_sweden = int(total)
    state.kpi_top_region = top_region
    state.kpi_top_region_value = int(top_row)
    state.kpi_lowest_region = bottom_region
    state.kpi_lowest_region_value = int(bottom_row)

    state.region_map = create_map(df, state.selected_year)
    
    
# ===== Initiating the map =====
region_map = create_map(df, selected_year)

# ===== GUI-site =====
with tgb.Page() as map_page:
    tgb.navbar()
    with tgb.part(class_name="card text-center card-margin"):
        tgb.text("## ANTAGNA STUDENTER VID START", mode="md")

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
                tgb.text("**Elevantal: {kpi_total_admitted_sweden}**", mode="md")
                tgb.text("**Procentuell ökning från 2020:**", mode="md")
                tgb.text("**{percentage_change}**", mode="md")

            with tgb.part(class_name="card card-margin text-center"):
                tgb.text("### Regionen med flest studenter", mode="md")
                tgb.text("**Elevantal: {kpi_top_region_value}**", mode="md")
                tgb.text("**Region: {kpi_top_region}**", mode="md")
                tgb.text("**Andel av hela landet: {top_region_share}**", mode="md")


            with tgb.part(class_name="card card-margin text-center"):
                tgb.text("### Minst antagna region", mode="md")
                tgb.text("**Elevantal: {kpi_lowest_region_value}**",  mode="md")
                tgb.text("**Region: {kpi_lowest_region}**", mode="md")
                tgb.text("**Andel av hela landet: {bottom_region_share}**", mode="md")

                
                
    tgb.html("br")                             
    with tgb.part(class_name="container d-flex justify-content-center py-4"):
        with tgb.part(class_name="card d-flex justify-content-center align-items-center"):
            tgb.chart(figure="{region_map}")