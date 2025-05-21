from taipy.gui import Gui
import taipy.gui.builder as tgb
import pandas as pd
from pathlib import Path


DATA_DIRECTORY = Path(__file__).parents[2] / "data"

# Data courses
df_2024_kurser = pd.read_excel(DATA_DIRECTORY / "anordnare_resultat_kurser_2020-2024/resultat-2024-for-kurser-inom-yh.xlsx")
df_2023_kurser = pd.read_excel(DATA_DIRECTORY / "anordnare_resultat_kurser_2020-2024/resultat-2023-for-kurser-inom-yh.xlsx")
df_2022_kurser = pd.read_excel(DATA_DIRECTORY / "anordnare_resultat_kurser_2020-2024/resultat-2022-for-kurser-inom-yh.xlsx")
df_2021_kurser_beviljade = pd.read_excel(DATA_DIRECTORY / "anordnare_resultat_kurser_2020-2024/resultat-juni-2021-for-korta-utbildningar-kurser-och-kurspaket.xlsx")
df_2021_kurser_inkomna = pd.read_excel(DATA_DIRECTORY / "anordnare_resultat_kurser_2020-2024/inkomna-ansokningar-juni-2021-for-korta-utbildningar-kurser-och-kurspaket.xlsx")
df_2020_kurser_april = pd.read_excel(DATA_DIRECTORY / "anordnare_resultat_kurser_2020-2024/Beviljade-korta-utb-kurser-kurspaket-YH-april-2020-1.xlsx")
df_2020_kurser_juli = pd.read_excel(DATA_DIRECTORY / "anordnare_resultat_kurser_2020-2024/Beviljade-korta-utb-kurser-kurspaket-YH-juli-2020-2.xlsx")



# Data program
df_2024_program = pd.read_excel(DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2024.xlsx", sheet_name= "Tabell 3", skiprows= 5)
df_2023_program = pd.read_excel(DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2023.xlsx", sheet_name= "Tabell 3", skiprows= 5)
df_2022_program = pd.read_excel(DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2022.xlsx", sheet_name= "Tabell 3")
df_2021_program = pd.read_excel(DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2021.xlsx", sheet_name= "Tabell 3")
df_2020_program = pd.read_excel(DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2020.xlsx", sheet_name= "Tabell 3")

# Dataframe global programs
global_dict_programs = {
    2024: df_2024_program,
    2023: df_2023_program,
    2022: df_2022_program,
    2021: df_2021_program,
    2020: df_2020_program 
}

# Dataframe global courses
global_dict_course = {
    2024: df_2024_kurser,
    2023: df_2023_kurser,
    2022: df_2022_kurser   
    }

# Initializ bindings variable
display_df_courses = pd.DataFrame()
display_df_programs = pd.DataFrame()
organizer_list = list(df_2024_program["Utbildningsanordnare administrativ enhet"].unique())
year = 2024 
selected_organizer = organizer_list[0]
amount_beviljade_courses = ""
total_applied_courses = ""
amount_beviljade_programs = ""
total_applied_programs = ""

def change_data(state):
    
   
   
        
    print("==debug==")
    print("Valt år från ui: ", state.year)
    print("Anordnare namn:", state.selected_organizer)
    
    state.year = int(state.year)
    
    print(" global_dict keys:", list(global_dict_course.keys()))
    print(" Typ av state.year:", type(state.year))
    
    if state.year == 2020:
        
        april = df_2020_kurser_april
        juli = df_2020_kurser_juli
        programs = df_2020_program
        
        print(programs["Utbildningsanordnare administrativ enhet"].unique())
            
        
        filter_april = april.query("Anordnare == @state.selected_organizer")
        filter_juli = juli.query("Anordnare == @state.selected_organizer")
        filter_programs = programs.query("`Utbildningsanordnare administrativ enhet` == @state.selected_organizer")
            
        print("Filter_program:", filter_programs)
            
            
        state.amount_beviljade_courses = len(filter_april) + len(filter_juli)
        state.total_applied_courses = len(filter_april) + len(filter_juli)  
        state.display_df_courses = pd.concat([filter_april, filter_juli]) 
            
            
        state.amount_beviljade_programs= len(filter_programs.query("Beslut == 'Beviljad'"))
        state.total_applied_programs = len(filter_programs)
        state.display_df_programs = filter_programs
       
            

            
        
    
    elif state.year == 2021:
        
        inkomn = df_2021_kurser_inkomna.copy()
        resultat = df_2021_kurser_beviljade.copy()
        program_2021 = df_2021_program.copy()
        
        filter_inkomn = inkomn.query("`Anordnare namn` == @state.selected_organizer")
        filter_result = resultat.query("`Anordnare namn` == @state.selected_organizer")
        filter_program = program_2021.query("`Utbildningsanordnare administrativ enhet` == @state.selected_organizer")
        
        
        
        state.amount_beviljade_courses = len(filter_result)
        state.total_applied_courses = len(filter_inkomn)
        state.display_df_courses = filter_inkomn
    
        state.amount_beviljade_programs = len(filter_program.query("Beslut == 'Beviljad'"))
        state.total_appplied_programs = len(filter_program)
        state.display_df_programs = filter_program

    elif state.year in global_dict_course:
            

            #
            dff_programs = global_dict_programs.get(state.year).copy()
            
            # using get to pick out which dataframe to copy 
            dff = global_dict_course.get(state.year).copy()
        
            # Filter on selecte organinazer 
            filtered = dff.query("`Anordnare namn` == @state.selected_organizer")

            filtered_programs = dff_programs.query("`Utbildningsanordnare administrativ enhet` == @state.selected_organizer")
            
            # Uppdaera tabellens innehåll
            state.display_df_courses = filtered
            
            print("Programs:", filtered_programs )
            state.display_df_programs = filtered_programs
            
            
            # Count KPI:er
            state.total_applied_courses = len(filtered) 
            state.total_applied_programs = len(filtered_programs)
            
            state.amount_beviljade_courses = len(filtered.query("Beslut == 'Beviljad'"))
            state.amount_beviljade_programs = len(filtered_programs.query("Beslut == 'Beviljad'"))
              
            print("Kolumner i df_2020_program", df_2020_program.columns.tolist)
            print("Antal rade i filtered:", len(filtered_programs))
            print("Kollumner:", filtered_programs.columns.tolist)
            print(filtered_programs.head())
            
    else:
        # ÅR saknas helt - skydd mot krash
        print(f"⚠️ Ingen data definierad för år: {state.year}")
        state.display_df_courses = pd.DataFrame()
        state.display_df_programs = pd.DataFrame()
        state.total_applied_courses = ""
        state.amount_beviljade_courses = ""
        state.total_applied_programs = ""
        state.amount_beviljade_programs = ""
        
        
    print("Totalt ansökningar kurser:", state.total_applied_courses)
    print("Totalt beviljade platser kurser:", state.amount_beviljade_courses)
    print("Totalt beviljade platser program:", state.total_applied_programs)
    print("Totalt ansökningar programs:", state.amount_beviljade_programs)
    

with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        tgb.text("# <b>Anordnare</b> och KPI:er om beviljande och ansökningar", mode="md")
        with tgb.layout(columns="1 1"):
            with tgb.part():

                tgb.text("**YEAR**", mode="md")
                tgb.selector(
                    "{year}", lov=[2020, 2021, 2022, 2023, 2024], dropdown=True
                )
            with tgb.part():    
                tgb.text("**Anordnare**", mode="md")
                tgb.selector(value="{selected_organizer}", lov="{organizer_list}", dropdown=True, filter= True)

        with tgb.part():

            tgb.html("br")
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
                
                with tgb.part(class_name= "container"):
                    tgb.text("**Antal beviljande platser {selected_organizer} för kurser**", mode= "md")
                    tgb.text("{amount_beviljade_courses}")
                    tgb.html("br")
                    tgb.text("**Antal ansökta kurser {selected_organizer}**", mode= "md")
                    tgb.text("{total_applied_courses}")
                    
                with tgb.part(class_name= "container"):
                    tgb.text("**Beviljande program**", mode= "md")
                    tgb.text("{amount_beviljade_programs}")
                    tgb.text("**Ansökta program**", mode= "md")
                    tgb.text("{total_applied_programs}")
                    
                
                
                    
            
        tgb.html("br")
        with tgb.layout(columns= ("1 1")):
            with tgb.part(class_name="container"):
                tgb.text("## Kurser", mode= "md")
                tgb.html("br")
                tgb.table(data="{display_df_courses}", rebuild=True)
            
            with tgb.part(class_name= "container"):
                tgb.text("## Programs", mode= "md")
                tgb.html("br")
                tgb.table(data="{display_df_programs}", rebuild=True)
                


if __name__ == "__main__":
    Gui(page, css_file="../assets/main.css").run(
        dark_mode=False, use_reloader=False, port=8080
    )
