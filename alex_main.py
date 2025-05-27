import taipy.gui.builder as tgb
from taipy.gui import Gui, notify
import pandas as pd
import chardet
from pathlib import Path
import plotly.express as px

DATA_DIRECTORY = Path(__file__).parents[0] / "data"

#initiera variabler
start_year = ""
end_year = ""
selected_educational_area = []
kpi_mean = "-"
kpi_peak_year = "-"
kpi_peak_year_value = "-"
kpi_top_area = "-"
kpi_top_area_value = "-"

#funktioner
def read_csv(sub_category, file_name, separator = ';'): # 1
    file_path = DATA_DIRECTORY / sub_category / file_name
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return pd.read_csv(
        file_path,
        encoding=result['encoding'],
        sep=separator
    ) 

try:
    df = read_csv(sub_category="2024_kurser", file_name="studerande_examinerad_yrkeshogskola.csv")
except FileNotFoundError as e:
    print(f"Fel: {e}")
    df = pd.DataFrame()

def clean_dataframe(df): # 2
    df = df.query("kön == 'totalt'")
    df = df.query("ålder == 'totalt'")
    df = df.drop(["ålder", "kön"], axis=1)
    df.rename(columns={'utbildningens inriktning': 'Utbildningens Inriktning'}, inplace = True)
    for year in df.columns[3:]:   
        df[year] = pd.to_numeric(df[year].str.replace('..', '0'), errors='coerce')
    return df.set_index("Utbildningens Inriktning")

df_cleaned = clean_dataframe(df)
educational_area = df_cleaned.index.tolist()
years = df_cleaned.columns.tolist()
valid_end_years = years[1:]

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
chart = create_linechart(pd.DataFrame()) 

#filter funktioner
def update_end_year(state): # 3
    if not state.start_year:
        notify(state, "warning", "Välj ett startår först")
        return
    state.valid_end_years = [year for year in state.years if int(year) > int(state.start_year)]
    if not state.end_year or int(state.end_year) < int(state.start_year):
        state.end_year = state.valid_end_years[0] 

def filter_data(state): # 4
    if not state.start_year or not state.end_year:
        notify(state, "warning", "Välj både start och slutår")
        state.chart = create_linechart(pd.DataFrame())
        state.kpi_mean = "-"
        state.kpi_peak_year = "-"
        state.kpi_peak_year_value = "-"
        state.kpi_top_area = "-" 
        state.kpi_top_area_value = "-"
        return
    if not state.selected_educational_area:
        notify(state, "warning", "Välj minst ett utbildningsområde")
        state.chart = create_linechart(pd.DataFrame())
        state.kpi_mean = "-"
        state.kpi_peak_year = "-"
        state.kpi_peak_year_value = "-"
        state.kpi_top_area = "-"
        state.kpi_top_area_value = "-"
        return
    filtered_df = state.df_cleaned.loc[state.selected_educational_area]
    selected_years = [year for year in state.years if int(year) >= int(state.start_year) and int(year) <= int(state.end_year)]
    filtered_df = filtered_df[selected_years]
    dynamix_xlabel = f"År ({state.start_year} - {state.end_year})"
    state.chart = create_linechart(filtered_df, xlabel=dynamix_xlabel, ylabel="Antal Studerande")
    state.kpi_mean = int(filtered_df.mean().mean())
    year_sums = filtered_df.sum(axis=0)
    state.kpi_peak_year = int(year_sums.idxmax())
    state.kpi_peak_year_value = int(year_sums.max())
    area_sums = filtered_df.sum(axis=1)
    state.kpi_top_area = str(area_sums.idxmax())
    state.kpi_top_area_value = int(area_sums.max())

# Taipy
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