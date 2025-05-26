from taipy.gui import Gui, notify
import taipy.gui.builder as tgb
import pandas as pd
from pathlib import Path



DATA_DIRECTORY = Path(__file__).parents[2] / "data"


def reading_file_course():
    
    dict_courses = {}

    df_kurser_2024 = pd.read_excel(
        DATA_DIRECTORY
        / "anordnare_resultat_kurser_2020-2024/resultat-2024-for-kurser-inom-yh.xlsx"
    )
    # df_kurser_2024.drop("Antal beviljade platser start och slut 2024", axis= 1, inplace=True)
    dict_courses[2024] = df_kurser_2024

    df_kurser_2023 = pd.read_excel(
        DATA_DIRECTORY
        / "anordnare_resultat_kurser_2020-2024/resultat-2023-for-kurser-inom-yh.xlsx"
    )
    dict_courses[2023] = df_kurser_2023

    df_kurser_2022 = pd.read_excel(
        DATA_DIRECTORY
        / "anordnare_resultat_kurser_2020-2024/resultat-2022-for-kurser-inom-yh.xlsx"
    )
    dict_courses[2022] = df_kurser_2022

    df_kurser_2021_lista = pd.read_excel(
        DATA_DIRECTORY
        / "anordnare_resultat_kurser_2020-2024/inkomna-ansokningar-juni-2021-for-korta-utbildningar-kurser-och-kurspaket.xlsx"
    )
    df_kurser_2021_beviljade = pd.read_excel(
        DATA_DIRECTORY
        / "anordnare_resultat_kurser_2020-2024/resultat-juni-2021-for-korta-utbildningar-kurser-och-kurspaket.xlsx"
    )
    df_kurser_2021 = pd.concat([df_kurser_2021_lista, df_kurser_2021_beviljade])

    if "Beslut" in df_kurser_2021.columns:

        df_kurser_2021["Beslut"] = df_kurser_2021["Beslut"].fillna("Avslag")
        
    else:
        df_kurser_2021["Beslut"] = "Avslag"
    
    dict_courses[2021] = df_kurser_2021

    df_kurser_2020_april = pd.read_excel(
        DATA_DIRECTORY
        / "anordnare_resultat_kurser_2020-2024/Beviljade-korta-utb-kurser-kurspaket-YH-april-2020-1.xlsx"
    )
    df_kurser_2020_juli = pd.read_excel(
        DATA_DIRECTORY
        / "anordnare_resultat_kurser_2020-2024/Beviljade-korta-utb-kurser-kurspaket-YH-juli-2020-2.xlsx"
    )
    df_kurser_2020 = pd.concat([df_kurser_2020_april, df_kurser_2020_juli])
    df_kurser_2020 = df_kurser_2020.rename(
        columns={
            "Anordnare": "Anordnare namn",
            "Platser med start 2020": "Antal beviljade platser 2020",
            "Platser med start 2021": "Antal beviljade platser 2021",
            "Platser med start och avslut 2020": "Antal beviljade platser start och slut 2020"
            
        },
    )
    df_kurser_2020["Beslut"] = "Beviljad"
    df_kurser_2020["Totalt antal beviljade platser"] = df_kurser_2020[
        [
            "Antal beviljade platser 2020",
            "Antal beviljade platser 2021",
            "Antal beviljade platser start och slut 2020",
        ]
    ].sum(axis=1)
    dict_courses[2020] = df_kurser_2020

    return dict_courses


def reading_file_programs():

    dict_programs = {}

    df_program_2024 = pd.read_excel(
        DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2024.xlsx",
        sheet_name="Tabell 3",
        skiprows=5,
    )
    df_program_2024.rename(
        columns={"Utbildningsanordnare administrativ enhet": "Anordnare namn"},
        inplace=True,
    )
    dict_programs[2024] = df_program_2024

    df_program_2023 = pd.read_excel(
        DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2023.xlsx",
        sheet_name="Tabell 3",
        skiprows=5,
    )
    df_program_2023.rename(
        columns={"Utbildningsanordnare administrativ enhet": "Anordnare namn"},
        inplace=True,
    )
    dict_programs[2023] = df_program_2023

    df_program_2022 = pd.read_excel(
        DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2022.xlsx",
        sheet_name="Tabell 4",
    )
    df_program_2022.rename(
        columns={"Utbildningsanordnare administrativ enhet": "Anordnare namn"},
        inplace=True,
    )
    dict_programs[2022] = df_program_2022

    df_program_2021 = pd.read_excel(
        DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2021.xlsx",
        sheet_name="Tabell 4",
    )
    df_program_2021.rename(
        columns={"Utbildningsanordnare administrativ enhet": "Anordnare namn"},
        inplace=True,
    )
    dict_programs[2021] = df_program_2021

    df_program_2020 = pd.read_excel(
        DATA_DIRECTORY / "program_2020-2024/resultat-ansokningsomgang-2020.xlsx",
        sheet_name="Tabell 4",
    )
    df_program_2020.rename(
        columns={"Utbildningsanordnare administrativ enhet": "Anordnare namn"},
        inplace=True,
    )
  
    dict_programs[2020] = df_program_2020

    return dict_programs


# Dataframe global courses
global_dict_course = reading_file_course()


# Dataframe global programs
global_dict_programs = reading_file_programs()


# Initializ bindings variable
display_df_courses = pd.DataFrame()
display_df_programs = pd.DataFrame()
organizer_list = []
selected_organizer = None
year = None 
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


def filter_beslut(filtered):
    filtered = filtered.query("Beslut == 'Beviljad'")

    return filtered


def filter_data(df, state):

    filtered = df.query("`Anordnare namn` == @state.selected_organizer")

    return filtered


# counting platser for selected organizer
def count_beviljande_platser(filtered):

    filtered = filter_beslut(filtered)

    try:
        totala = float(filtered["Totalt antal beviljade platser"].sum())
        
        return max(totala, 0)
    
    except Exception as e:
        print("Fel i beräkning:", e)
        return 0
   

def check_zero(a):
    
    # notna to find out if value is nan, return false if it is nan
    # return zero if it's empty string or 0
    return str(int(a)) if pd.notna(a) else "0"
     

# count KPI:er for percentage
def count_percentage(part, hole):

    try:
        # Percentage for applied courses
        
        if not part and not hole or str(part).strip() == "" or str(hole).strip() == "":
            
            return "0%"
        
        a = int(part)
        b = int(hole)
       
        if a and b > 0:
           return  f"{a/b * 100:.1f}%"
           
        else:
           return  "0%"
           
       

    except Exception as e:
        print("Fel count_percentage", e)
        print(f"Fel uträkning")
        print(f"fel Ingen uträkning")


def update_year(state):
    
    try:
        state.year = int(state.year)
        
    except:
        print(f"⚠ Ogiltigt årval: {state.year}")
        return
    
    
    
    print(f"Uppdaterad anordnare för år: {state.year}")

    # Update selector for anordnare based on year
    if state.year in global_dict_programs:
        
        df_program = global_dict_programs[state.year]
        
        print(f"Dataframe kolumn: {df_program.columns.tolist()}")
        print(f"Antal rader: {len(df_program)}")
        
        if "Anordnare namn" in df_program.columns:
            
            new_list = sorted(df_program["Anordnare namn"].dropna().unique())
            print(f"Ny lista:", new_list[:5])
        
            state.organizer_list = []
            state.organizer_list = list(new_list)

            if state.selected_organizer and state.selected_organizer not in new_list:
                state.selected_organizer= None
                
        else:
            print("❌ kolumnen 'Anordnare namn' finns inte i dataframe")
            
    else:
        print("❌ ÅR {state.year} finns inte i globala_dict_programs")

      


def change_data(state):

    print(f"\nkör change_data med year= {state.year}, \nselected_organizer= {state.selected_organizer}" )
    
    if not state.year or not state.selected_organizer:
        
        print("⚠️ Abryter - år eller anordnare inte valt")
        notify(state, "⚠️Warning", "Vänligen välj år och anorndare")
        
        return
    
    try:
        
        update_year(state)
        
        state.year = int(state.year)

        # Pandas get to bring selected year
        # selected year is to get dataframe based on which year is selected
        dff_programs = global_dict_programs.get(state.year).copy()

        # using get to pick out which dataframe to copy
        dff = global_dict_course.get(state.year).copy()  
        
    except Exception as e:
        print("Fel change_data:", e)

    # Filter on selecte organinazer courses
    filtered = filter_data(dff, state)
    # Filter on selectro organizer programs
    filtered_programs = filter_data(dff_programs, state)

    # Uppdaera tabellens innehåll
    state.display_df_courses = filtered
    state.display_df_programs = filtered_programs

  
    # Count KPI:er
    # len to get a number how many row filtered and filtered_programs has.
    # Filtered is a variable with value of choosing organizer
    state.total_applied_courses = check_zero(len(filtered))    
    state.total_applied_programs = check_zero(len(filtered_programs))

    
    state.amount_beviljade_courses = check_zero(len(filter_beslut(filtered)))
    state.amount_beviljade_programs = check_zero(len(filter_beslut(filtered_programs)))

   
    state.course_approved_spots = check_zero(count_beviljande_platser(filtered))

    # filtered_programs is the new data
    # sum all in column sökta platser totalt
    # notna to find out if value is nan, return false if it is nan
    state.sokta_platser =  check_zero(filtered_programs["Sökta platser totalt"].sum())
    state.beviljade_platser = check_zero(filtered_programs["Beviljade platser totalt"].sum())

   

    # For courses, counting percentage
    state.percentage_courses = count_percentage(state.amount_beviljade_courses, state.total_applied_courses)
    
    # For programs, counting percentage
    state.percentage_programs = count_percentage(state.amount_beviljade_programs, state.total_applied_programs)
    state.count_stats = count_percentage(state.beviljade_platser, state.sokta_platser)


with tgb.Page() as page:
    tgb.toggle(theme=True)
    with tgb.part(class_name="card text-center card-margin"):
        tgb.text(
            "# Anordnare och KPI:er om beviljande och ansökningar", mode="md", raw=True
        )
       

    with tgb.part(class_name= "container"):
        with tgb.part(class_name= " card card-margin"):
            with tgb.layout(columns="1 2 1"):
                with tgb.part():
                    tgb.selector(
                        value="{year}",
                        label= "Välj år",
                        lov=[2024, 2023, 2022, 2021, 2020],
                        dropdown=True,
                        on_change=update_year,
                        class_name= "fullwidth",
                        bind = "year"
                    )
                    
                with tgb.part():
                    tgb.selector(
                        value="{selected_organizer}",
                        label= "Välj anordnare",
                        lov="{organizer_list}",
                        dropdown=True,
                        filter=True,
                        class_name= "fullwidth",
                        bind= "selected_organizer",
                        disabled = "year == None or year == ''"
                    )

                with tgb.part(class_name= "text-center"):
                    tgb.button(
                        label="FILTRERA",
                        class_name="plain filter-button government_button",
                        on_action=change_data,
                        disabled = "{selected_organizer} == None or {selected_organizer} == '' or {year} == None or {year} == ''",
                        bind = ["year",  "selected_organizer"] 
                    )
                    
    with tgb.part(class_name= "container"):
        with tgb.part(class_name= "card card-margin"):
            tgb.text("**TEXT OM KPI:er**", mode="md")
            tgb.html("br")
            tgb.text("KPI.er för hur det har gått för anordnaren för året {year}")

        # start kpi:er, applied courses
            tgb.html("br")     
            with tgb.part():
                with tgb.layout(columns=("1 1 1 1")):

                    # applied course
                    with tgb.part():
                        tgb.text("Antal ansökta kurser")
                        with tgb.part(class_name="card"):
                            tgb.text("{total_applied_courses}")

                    # approved course
                    with tgb.part():
                        tgb.text(
                            "Antal beviljande kurser"
                        )
                        with tgb.part(class_name="card"):
                            tgb.text("{amount_beviljade_courses}")
                
                    # stats for courses, approved / applied
                    with tgb.part():
                        tgb.text("Beviljandegrad kurser")
                        with tgb.part(class_name="card"):
                            tgb.text("{percentage_courses}")
                        
                    # amount of spots for courses             
                    with tgb.part(class_name="container"):
                        tgb.text("Antal beviljande platser kurser")
                        with tgb.part(class_name="card"):
                            tgb.text("{course_approved_spots}")

    # data set for courses
    with tgb.part(class_name= "card"):
        tgb.text("## DATA KURSER", mode="md")
        tgb.html("br")
        tgb.table(data="{display_df_courses}", rebuild=True)

    tgb.html("br")
    with tgb.part(class_name= "container"):
        with tgb.part(class_name="card card-margin"):
            tgb.text("KPI:er för program för valt anordnare")

            # how many programs and approved 
            tgb.html("br")
            with tgb.layout(columns=("1 1 1")):
                
                with tgb.part(class_name="container"):
                    tgb.text("Antal ansökta program")
                    with tgb.part(class_name="card"):
                        tgb.text("{total_applied_programs}")

                with tgb.part(class_name="container"):
                    tgb.text("Antal beviljande program")
                    with tgb.part(class_name="card"):
                        tgb.text("{amount_beviljade_programs}")

                with tgb.part(class_name="container"):
                    tgb.text("Beviljandegrad för program")
                    with tgb.part(class_name="card"):
                        tgb.text("{percentage_programs}")

            # spots program
            tgb.html("br")
            with tgb.layout(columns=("1 1 1")):

                with tgb.part(class_name="container"):
                    tgb.text("Antal ansökta platser program")
                    with tgb.part(class_name="card"):
                        tgb.text("{sokta_platser}")

                with tgb.part(class_name="container"):
                    tgb.text("Antal beviljande platser program")
                    with tgb.part(class_name="card"):
                        tgb.text("{beviljade_platser}")

                with tgb.part(class_name="container"):
                    tgb.text("Beviljandegrad platser program")
                    with tgb.part(class_name="card"):
                        tgb.text("{count_stats}")
    
                  
    with tgb.part(class_name= "card"):
        with tgb.part(class_name="container"):
            tgb.text("## DATA PROGRAMS", mode="md")
            tgb.table(data="{display_df_programs}", rebuild=True)


if __name__ == "__main__":
    Gui(page, css_file="style.css").run(dark_mode=False, use_reloader=False, port=8080)
