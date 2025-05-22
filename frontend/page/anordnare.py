from taipy.gui import Gui
import taipy.gui.builder as tgb
import pandas as pd
from pathlib import Path


DATA_DIRECTORY = Path(__file__).parents[2] / "data"



def reading_file_course():
       
    
    dict_courses = {}
    
    
    df_kurser_2024 = pd.read_excel(DATA_DIRECTORY / "anordnare_resultat_kurser_2020-2024/resultat-2024-for-kurser-inom-yh.xlsx")
    df_kurser_2024.drop("Antal beviljade platser start och slut 2024", axis= 1, inplace=True)
    dict_courses[2024] = df_kurser_2024
    
    df_kurser_2023 = pd.read_excel(DATA_DIRECTORY / "anordnare_resultat_kurser_2020-2024/resultat-2023-for-kurser-inom-yh.xlsx")
    dict_courses[2023] = df_kurser_2023
            
    df_kurser_2022 = pd.read_excel(DATA_DIRECTORY / "anordnare_resultat_kurser_2020-2024/resultat-2022-for-kurser-inom-yh.xlsx")
    dict_courses[2022] = df_kurser_2022
    
    df_kurser_2021_lista = pd.read_excel(DATA_DIRECTORY / "anordnare_resultat_kurser_2020-2024/inkomna-ansokningar-juni-2021-for-korta-utbildningar-kurser-och-kurspaket.xlsx")
    df_kurser_2021_beviljade = pd.read_excel(DATA_DIRECTORY / "anordnare_resultat_kurser_2020-2024/resultat-juni-2021-for-korta-utbildningar-kurser-och-kurspaket.xlsx")
    df_kurser_2021 = pd.concat([df_kurser_2021_lista, df_kurser_2021_beviljade])
    
    if "Beslut" in df_kurser_2021:
                
        df_kurser_2021["Beslut"] = df_kurser_2021["Beslut"].fillna("Avslag")
        dict_courses[2021] = df_kurser_2021
    else:
        dict_courses[2021] = df_kurser_2021
    
            
    df_kurser_2020_april = pd.read_excel(DATA_DIRECTORY / "anordnare_resultat_kurser_2020-2024/Beviljade-korta-utb-kurser-kurspaket-YH-april-2020-1.xlsx")
    df_kurser_2020_juli = pd.read_excel(DATA_DIRECTORY / "anordnare_resultat_kurser_2020-2024/Beviljade-korta-utb-kurser-kurspaket-YH-juli-2020-2.xlsx")
    df_kurser_2020 = pd.concat([df_kurser_2020_april, df_kurser_2020_juli])
    dict_courses[2020] = df_kurser_2020
            
            
    return dict_courses
            


def reading_file_programs():
    
    dict_programs = {}
    
    df_program_2024 = pd.read_excel(DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2024.xlsx", sheet_name= "Tabell 3", skiprows=5)
    df_program_2024.rename(columns= {"Utbildningsanordnare administrativ enhet": "Anordnare namn"}, inplace=True)
    dict_programs[2024] = df_program_2024 
    
    df_program_2023 = pd.read_excel(DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2023.xlsx", sheet_name= "Tabell 3", skiprows=5)
    df_program_2023.rename(columns= {"Utbildningsanordnare administrativ enhet": "Anordnare namn"}, inplace= True)
    dict_programs[2023] = df_program_2023
    
    df_program_2022 = pd.read_excel(DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2022.xlsx", sheet_name= "Tabell 4")
    df_program_2022.rename(columns= {"Utbildningsanordnare administrativ enhet": "Anordnare namn"}, inplace= True)
    dict_programs[2022] = df_program_2022
    
    df_program_2021 = pd.read_excel(DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2021.xlsx", sheet_name= "Tabell 4")
    df_program_2021.rename(columns= {"Utbildningsanordnare administrativ enhet": "Anordnare namn"}, inplace= True)
    dict_programs[2021] = df_program_2021
    
    df_program_2020 = pd.read_excel(DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2020.xlsx", sheet_name= "Tabell 4")
    df_program_2020.rename(columns= {"Utbildningsanordnare administrativ enhet": "Anordnare namn"}, inplace= True)
    dict_programs[2020] = df_program_2020
    
    return dict_programs
            



# Dataframe global courses
global_dict_course = reading_file_course()


# Dataframe global programs
global_dict_programs = reading_file_programs()
  

# Initializ bindings variable
display_df_courses = pd.DataFrame()
display_df_programs = pd.DataFrame()
organizer_list = sorted(global_dict_programs[2024]["Anordnare namn"].dropna().unique())
selected_organizer_temp = ""
selected_organizer = ""
year = 2024
amount_beviljade_courses = ""
total_applied_courses = ""
amount_beviljade_programs = ""
total_applied_programs = ""
percentage_courses = ""
percentage_programs = ""
sokta_platser = ""
beviljade_platser = ""
count_stats = ""
course_applied_spots = ""
course_approved_spots = ""
stats_platser_kurs = ""

def kpi_filter(filtered):
    filtered = filtered.query("Beslut == 'Beviljad'")
    
    return filtered


def filter_data(df, state):
    
    filtered = df.query("`Anordnare namn` == @state.selected_organizer")
    
    return filtered


# count KPI:er for percentage        
def count_percentag(state):
    
    try:
        # Percentage for applied courses
        if (
            state.amount_beviljade_courses
            and state.total_applied_courses > 0
        ):
            percentage_c = (
                state.amount_beviljade_courses / state.total_applied_courses * 100
            )
            state.percentage_courses = f"{percentage_c:.1f}%"
        
        else:
            state.percentage_courses = f"Fel {percentage_c}"
            
        # percentage for applied programs 
        if state.amount_beviljade_programs and state.total_applied_programs > 0:
                percentage_p = state.amount_beviljade_programs / state.total_applied_programs * 100
                state.percentage_programs = f"{percentage_p:.1f}%"

        else:
            state.percentage_programs = f"Fel {percentage_p}"
            
        # Percentage for platser programs
        if state.beviljade_platser and state.sokta_platser > 0:
            count_stats = state.beviljade_platser / state.sokta_platser * 100
            state.count_stats = f"{count_stats:.1f}%"
            
            
        else:
            state.count_stats = f"Fel {count_stats}"
            
            
        # Percentage for platser i courses  
        if state.course_applied_spots and state.course_approved_spots > 0:
            
            percent_p = state.course_applied_spots / state.course_approves_spots * 100
            
            state.percent_p = f"{percent_p}%"
            
        else:
            state.percent_p = f"Fel {percent_p}"
            
        

    except Exception as e:
        state.percentage_courses = f"Fel {e}"
        state.percentage_programs = f"fel {e}"


def update_year(state):
    
    # Update selector for anordnare based on year
    if state.year in global_dict_programs:
        df_program = global_dict_programs[state.year]
        new_list = sorted(
            df_program["Anordnare namn"].dropna().unique()
        )
        state.organizer_list = new_list

        print("Ny anordnar lista:", new_list)
        print("Nuvarande organizer lista:", {state.selected_organizer})
        print("update selected_organizer:", state.selected_organizer)

        if new_list:
            state.selected_organizer_temp = new_list

        else:
            state.selected_organizer_temp = state.selected_organizer


def change_data(state):
    
    update_year(state)

    print("==debug==")
    print("Valt år från ui: ", state.year)
    print("Anordnare namn:", state.selected_organizer)

    state.year = int(state.year)

    print(" global_dict keys:", list(global_dict_course.keys()))
    print(" Typ av state.year:", type(state.year))

   
   

        
    dff_programs = global_dict_programs.get(state.year).copy()

    # using get to pick out which dataframe to copy
    dff = global_dict_course.get(state.year).copy()

    # Filter on selecte organinazer courses
    filtered = filter_data(dff, state)

    # Filter on selectro organizer programs
    filtered_programs = filter_data(dff_programs, state)
    # Uppdaera tabellens innehåll
    state.display_df_courses = filtered

    print("Programs:", filtered_programs)
    state.display_df_programs = filtered_programs
    

    print(f"Vad visar filtered här: {filtered}")
    # Count KPI:er
    # len to get a number how many row filtered and filtered_programs has.
    # Filtered is a variable with value of choosing organizer
    state.total_applied_courses = len(filtered)
    state.total_applied_programs = len(filtered_programs)
    
    # len finding number of row kpi_filter function filter Beslut is Beviljad
    state.amount_beviljade_courses = len(kpi_filter(filtered))
    state.amount_beviljade_programs = len(kpi_filter(filtered_programs))

    # filtered_programs is the new data
    # sum all in column sökta platser totalt
    state.sokta_platser = filtered_programs["Sökta platser totalt"].sum()
    state.beviljade_platser = filtered_programs["Beviljade platser totalt"].sum()
    #courses 
    state.course_applied_spots = filtered[["Antal beviljade platser start 2024", "Antal beviljade platser start 2025"]].sum().sum()
    state.course_approved_spots = filtered.query("Beslut == 'Beviljad'")["Totalt antal beviljade platser"].sum()
    
    print("Antal rade i filtered:", len(filtered_programs))
    print("Kollumner:", filtered_programs.columns.tolist)
    print(filtered_programs.head())



    print("Totalt ansökningar kurser:", state.total_applied_courses)
    print("Totalt beviljade platser kurser:", state.amount_beviljade_courses)
    print("Totalt beviljade platser program:", state.total_applied_programs)
    print("Totalt ansökningar programs:", state.amount_beviljade_programs)
    
    count_percentag(state)
   

with tgb.Page() as page:
    tgb.toggle(theme=True)
    with tgb.part(class_name="container card"):
        tgb.text(
            "# Anordnare och KPI:er om beviljande och ansökningar", mode="md", raw=True
        )
        with tgb.layout(columns="1 1"):

            with tgb.part():
                tgb.text("**SELECT YEAR**", mode="md")
                tgb.selector(
                    "{year}",
                    lov=[2024, 2023, 2022, 2021, 2020],
                    dropdown=True,
                    on_change=update_year,
                )
            with tgb.part():
                tgb.text("**SELECT ANORDNARE**", mode="md")
                tgb.selector(
                    value="{selected_organizer}",
                    lov="{organizer_list}",
                    dropdown=True,
                    filter=True,
                )

        with tgb.part():

            tgb.button(
                label="APPLY",
                class_name="plain apply_buttom",
                on_action=change_data,
            )

        with tgb.part():
            tgb.text("**TEXT OM KPI:er**", mode="md")
            with tgb.part(class_name= "container"):
                tgb.text("KPI.er för hur det har gått för anordnaren för året {year}")

            # start kpi:er, applied courses
            tgb.html("br")
            with tgb.layout(columns=("1 1 1")):
        
                with tgb.part(class_name="container"):
                    tgb.text("Antal ansökta kurser", class_name= "container",
                        mode="md")
                    with tgb.part(class_name= "card"):
                        tgb.text("{total_applied_courses}")
                    
                    
                
                with tgb.part(class_name= "container"):
                    tgb.text(
                        "Antal beviljande kurser",
                        mode="md", class_name= "container")
                    with tgb.part(class_name= "card"):
                        tgb.text("{amount_beviljade_courses}")
                
                    
                
                with tgb.part(class_name="container"):
                    tgb.text("Beviljandegrad kurser", mode="md", class_name= "container")
                    with tgb.part(class_name= "card"):
                        tgb.text("{percentage_courses}")


            tgb.html("br")
            with tgb.layout(columns= ("1 1 1")):
                
                
                with tgb.part(class_name= "container"):
                    tgb.text("Antal ansökta platser kurser", class_name= "container")
                    with tgb.part(class_name= "card"):
                        tgb.text("{course_applied_spots}")
                    
                    
                
                with tgb.part(class_name="container"):
                    tgb.text("Antal beviljande platser kurser", class_name= "container")
                    with tgb.part(class_name= "card"):
                        tgb.text("{program_approved_spots}")
                    
                
                with tgb.part(class_name="container"):
                    tgb.text("Beviljandegrad platser för kurser", class_name= "container")
                    with tgb.part(class_name= "card"):
                        tgb.text("{stats_platser_kurs}")
                   
                   
            tgb.html("br")   
            with tgb.part(class_name="container"):
                tgb.text("## DATA KURSER", mode="md")
                tgb.html("br")
                tgb.table(data="{display_df_courses}", rebuild=True)
                    
             
            with tgb.part(class_name= "container"):
                tgb.text("KPI:er för program för valt anordnare")  
                
                
            tgb.html("br")
            with tgb.layout(columns= ("1 1 1")):
                
                    
                with tgb.part(class_name= "container"):
                    tgb.text("Antal ansökta program", class_name= "container")
                    with tgb.part(class_name= "card"):
                        tgb.text("{total_applied_programs}")
                    
                with tgb.part(class_name= "container"):                    
                    tgb.text("Antal beviljande program", class_name= "container")
                    with tgb.part(class_name= "card"):
                        tgb.text("{amount_beviljade_programs}")
                    
                with tgb.part(class_name= "container"):                    
                    tgb.text("Beviljandegrad för program", class_name= "container")
                    with tgb.part(class_name= "card"):
                        tgb.text("{percentage_programs}")
            
            tgb.html("br")    
            with tgb.layout(columns= ("1 1 1")):
                
                
                with tgb.part(class_name= "container"):                    
                    tgb.text("Antal ansökta platser program", class_name= "container")
                    with tgb.part(class_name= "card"):
                        tgb.text("{sokta_platser}")
                    
                with tgb.part(class_name= "container"):                    
                    tgb.text("Antal beviljande platser program", class_name= "container")
                    with tgb.part(class_name= "card"):
                        tgb.text("{beviljade_platser}")
                    
                with tgb.part(class_name= "container"):                    
                    tgb.text("Beviljandegrad platser program")
                    with tgb.part(class_name= "card"):
                        tgb.text("{count_stats}")

        
            tgb.html("br")
            with tgb.part(class_name="container"):
                tgb.text("## DATA PROGRAMS", mode="md")
                tgb.table(data="{display_df_programs}", rebuild=True)


if __name__ == "__main__":
    Gui(page, css_file="style.css").run(
        dark_mode=False, use_reloader=False, port=8080
    )
