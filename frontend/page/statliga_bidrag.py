import taipy.gui.builder as tgb
from backend.data_processing import clean_columns
from backend.data_loader import load_funding_data
from backend.filter_data import filter_data_funding

selected_educational_area = ""
year = ""
year_students = "-"
schablon = "-"
government_funding = "-"

df = load_funding_data()

educational_area = list(df.index[:-2])
years = df.columns
df.columns = list(map(clean_columns, df.columns))

with tgb.Page() as government_grant_per_program:
    tgb.navbar()
    tgb.toggle(theme=True)
    with tgb.part(class_name="card text-center card-margin"):
        tgb.text("# Statliga bidrag per **Utbildningsområde** ", mode="md")

    with tgb.part(class_name="container government"):
        with tgb.part(class_name="card card-margin"):
            with tgb.layout(columns="3 1 2"):
                with tgb.part(class_name="testing"):
                    tgb.selector(
                        value="{selected_educational_area}",
                        lov=educational_area,
                        dropdown=True,
                        multiple=False,
                        label="Välj Utbildningsområde",
                        class_name="fullwidth")
                with tgb.part(class_name="text-center"):
                    tgb.selector(
                        value= "{year}",
                        lov= years,
                        label= "Välj År",
                        dropdown=True)
                with tgb.part(class_name="text-center"):
                    tgb.button(label="Filtrera",
                               class_name="plain filter-button government_button",
                               on_action=filter_data_funding)

    with tgb.part(class_name="container government"):
        with tgb.layout(columns="1 1 1"): 
            with tgb.part(class_name="card card-margin text-center"):
                tgb.text("### Statsbidrag", mode="md")
                tgb.text("**{government_funding:,.0f}** kr", mode="md", class_name="kpi-value")

            with tgb.part(class_name="card card-margin text-center"):
                tgb.text("### Antal årsplatser", mode="md")
                tgb.text("**{year_students:,.1f}**", mode="md", class_name="kpi-value")

            with tgb.part(class_name="card card-margin text-center"):
                tgb.text("### Schablonbelopp", mode="md")
                tgb.text("**{schablon:,.0f}** kr", mode="md", class_name="kpi-value")          