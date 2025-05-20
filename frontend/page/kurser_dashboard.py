from taipy.gui import Gui
import taipy.gui.builder as tgb
from Backend.data_processing import df


anordnare = df["Anordnare namn"].unique()
utbildningsområde = df["Utbildningsområde"].unique()



with tgb.Page() as page:
    tgb.navbar()
    with tgb.part(class_name= "container card"):
        tgb.text("# Rubrik", mode= "md")
        with tgb.layout(columns= "2 1"):
            with tgb.part(class_name= "card"):
                
                tgb.text("## YEAR", mode="md")
                tgb.selector("year", lov= [2020, 2021, 2022, 2023, 2024],dropdown=True)
                
                tgb.text("## Anordnare", mode= "md")
                tgb.selector("ANORDNARE", lov= anordnare, dropdown=True)
                
                tgb.text("## UTBILDNINGSOMRÅDE", mode="md")
                tgb.selector("OMRÅDE", lov= utbildningsområde, dropdown=True)
            
            with tgb.part(class_name= "card text-center"):
                tgb.button(label="APPLY", class_name= "plain")
            





if __name__=="__main__":
    Gui(page).run(dark_mode=False, use_reloader= False, port= 8080)