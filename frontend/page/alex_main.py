import taipy.gui.builder as tgb
from taipy.gui import Gui, notify
import pandas as pd
from frontend.charts_utils import create_linechart
from backend.data_processing import read_csv_alex, clean_dataframe
from backend.filter_data import filter_data
from backend.update import update_end_year

start_year = ""
end_year = ""
selected_educational_area = []
kpi_mean = "-"
kpi_peak_year = "-"
kpi_peak_year_value = "-"
kpi_top_area = "-"
kpi_top_area_value = "-"

try:
    df = read_csv_alex(sub_category="2024_kurser", file_name="studerande_examinerad_yrkeshogskola.csv")
except FileNotFoundError as e:
    print(f"Fel: {e}")
    df = pd.DataFrame() 

df_cleaned = clean_dataframe(df)
educational_area = df_cleaned.index.tolist()
years = df_cleaned.columns.tolist()
valid_end_years = years[1:]

chart = create_linechart(pd.DataFrame()) 

with tgb.Page() as number_students_educationalarea_year:
    tgb.toggle(theme=True)
    with tgb.part(class_name="card text-center card-margin"):
        tgb.text("# Studenter på **Yrkeshögskola**", mode="md")
    with tgb.part(class_name="container"): 
        with tgb.part(class_name="card card-margin"):
            with tgb.layout(columns="3 2 1"):
                with tgb.part(class_name="education_area_filter"):
                    tgb.selector(
                        value="{selected_educational_area}",
                        lov=educational_area,
                        dropdown=True,
                        multiple=True,
                        label="Välj Utbildningsområde",
                        class_name="fullwidth"
                    )
                with tgb.part():
                    with tgb.layout(columns="1 1"):
                        tgb.selector(
                            value="{start_year}",
                            lov=years[:-1],
                            label="Välj Startår",
                            dropdown=True,
                            on_change=update_end_year,
                            class_name="fullwidth"
                        )
                        tgb.selector(
                            value="{end_year}",
                            lov="{valid_end_years}",
                            dropdown=True,
                            label="Välj Slutår",
                            class_name="fullwidth"
                        )
                with tgb.part(class_name="text-center"):
                    tgb.button(label="Filtrera",
                               class_name="plain filter-button government_button",
                               on_action=filter_data)
    with tgb.part(class_name="container"):
            with tgb.layout(columns="1 1 1"):
                with tgb.part(class_name="card card-margin text-center"):
                    tgb.text("#### Genomsnitt/år:", mode="md")
                    tgb.text("**{kpi_mean:,}**", mode="md")

                with tgb.part(class_name="card card-margin text-center"):
                    tgb.text("#### Flest studenter år:", mode="md")
                    tgb.text("**{kpi_peak_year}**", mode="md")
                    tgb.text("**{kpi_peak_year_value:,}**  st studenter", mode ="md")

                with tgb.part(class_name="card card-margin text-center"):
                    tgb.text("#### Största område:", mode="md")
                    tgb.text("**{kpi_top_area}**", mode="md")
                    tgb.text("**{kpi_top_area_value:,}** st studenter totalt", mode= "md")
                                    
    with tgb.part(class_name="container"):
        with tgb.part(class_name="card"):
            tgb.text("### Utveckling över tid per **Utbildningsområde**", mode="md")
            tgb.chart(figure="{chart}")

if __name__ == "__main__":
    Gui(
        number_students_educationalarea_year,
        css_file="assets/style.css"
    ).run(
        dark_mode=False,
        use_reloader=True,
        port=8080,
        title="Elvins Dashboard",
        watermark="Elvins Dashboard"
    )