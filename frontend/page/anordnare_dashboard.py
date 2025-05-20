from taipy.gui import Gui
import taipy.gui.builder as tgb
import pandas as pd
from pathlib import Path


DATA_DIRECTORY = Path(__file__).parents[2] / "data/anordnare_resultat_kurser_2020-2024"

df_2024_kurser = pd.read_excel(DATA_DIRECTORY / "resultat-2024-for-kurser-inom-yh.xlsx")

   


anordnare = list(df_2024_kurser["Anordnare namn"].unique())

year = 2020


selected_orginazer = anordnare[0]

amount_beviljade = ""
total_applied = ""


def change_data(state):

    dff = df_2024_kurser.copy()
    
    
    dff = df_2024_kurser.query("`Anordnare namn` == @state.selected_orginazer")
    print(dff)
    state.df_2024_kurser = dff[f"Antal beviljade platser start {state.year}"]
    
    state.total_applied = len(state.df_2024_kurser)
   
    
    state.amount_beviljade = len(dff.query("Beslut == 'Beviljad'"))  
  
    

with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        tgb.text("# Rubrik", mode="md")
        with tgb.layout(columns="1 1"):
            with tgb.part():

                tgb.text("**YEAR**", mode="md")
                tgb.selector(
                    "{year}", lov=[2020, 2021, 2022, 2023, 2024], dropdown=True
                )
            with tgb.part():    
                tgb.text("**Anordnare**", mode="md")
                tgb.selector(value="{selected_orginazer}", lov=anordnare, dropdown=True, filter= True)

            
        with tgb.part(class_name="text-center"):

            tgb.button(
                label="APPLY",
                class_name="plain apply_buttom",
                on_action=change_data,
            )

        with tgb.part():
            tgb.html("br")
            
        with tgb.part():
            tgb.text("**TEXT OM KPI:er**", mode="md")
            
        
            with tgb.layout(columns= ("1 1")):
                
                with tgb.part(class_name= "card"):
                    tgb.text("**Beviljade plaser kurs**", mode= "md")
                    tgb.text("{amount_beviljade}")
                    tgb.text("**Ansökta kurser**", mode= "md")
                    tgb.text("{total_applied}")
                    
                with tgb.part(class_name= "card"):
                    tgb.text("**Beviljande program**", mode= "md")
                    tgb.text("**Ansökta program**", mode= "md")
                    
                
                
                    
            
        tgb.html("br")
        with tgb.part(class_name="container card"):

            tgb.html("br")
            tgb.table(data="{df_2024_kurser}", rebuild=True)


if __name__ == "__main__":
    Gui(page, css_file="../assets/main.css").run(
        dark_mode=False, use_reloader=False, port=8080
    )
