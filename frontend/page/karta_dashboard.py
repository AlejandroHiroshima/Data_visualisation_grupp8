import taipy.gui.builder as tgb
from frontend.map import skapa_karta
from Backend.data_processing import df 

# ===== Globala variabler =====
selected_year = 2024
years = [2020, 2021, 2022, 2023, 2024]
region_map = None

# ===== Callback när året ändras =====
def on_year_change(state):
    state.region_map = skapa_karta(df, state.selected_year)

# ===== Initiera första kartan =====
region_map = skapa_karta(df, selected_year)

# ===== GUI-sida =====
with tgb.Page() as map_page:
    tgb.navbar()
    tgb.text("## Välj år för antagna elever", mode="md")
    tgb.selector(
        label="År",
        value="{selected_year}",
        lov=years,
        dropdown=True,
        on_change=on_year_change
    )
    tgb.chart(figure="{region_map}")


# ===== 7. Starta GUI =====
# Gui(page).run(port=8080, dark_mode=False)
