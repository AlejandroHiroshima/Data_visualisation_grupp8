from backend.data_processing import reading_file_programs, reading_file_course
from backend.filter_data import filter_data_marcus, filter_desicion
from taipy.gui import notify
from backend.calculation import check_zero, count_approved_spots, count_percentage
from frontend.charts_utils import create_linechart
import pandas as pd

#  === Dataframe global programs anordnare Marcus === 
global_dict_programs = reading_file_programs()
# Dataframe global courses
global_dict_course = reading_file_course()

def update_year(state):

    try:
        state.year_organizer = int(state.year_organizer)

    except:
        print(f"⚠ Ogiltigt årval: {state.year_organizer}")
        return

    

    # Update selector for anordnare based on year
    if state.year_organizer in global_dict_programs:

        df_program = global_dict_programs[state.year_organizer]

       

        if "Anordnare namn" in df_program.columns:

            new_list = sorted(df_program["Anordnare namn"].dropna().unique())
            

            state.organizer_list = []
            state.organizer_list = list(new_list)

            if state.selected_organizer and state.selected_organizer not in new_list:
                state.selected_organizer = None

        else:
            print("❌ kolumnen 'Anordnare namn' finns inte i dataframe")

    else:
        print("❌ ÅR {state.year_organizer} finns inte i globala_dict_programs")
        



def change_data(state):
    

    if not state.year_organizer or not state.selected_organizer:

        # print("⚠️ Abryter - år eller anordnare inte valt")
        notify(state, "warning", "Vänligen välj år och anorndare")

        return

    try:

        update_year(state)

        state.year_organizer = int(state.year_organizer)

        # Pandas get to bring selected year_organizer
        # selected year_organizer is to get dataframe based on which year_organizer is selected
        dff_programs = global_dict_programs.get(state.year_organizer).copy()

        # using get to pick out which dataframe to copy
        dff = global_dict_course.get(state.year_organizer).copy()

    except Exception as e:
        print("Fel change_data:", e)

    # Filter on selecte organinazer courses
    filtered = filter_data_marcus(dff, state)      
    # Filter on selectro organizer programs
    filtered_programs = filter_data_marcus(dff_programs, state) 

    # Uppdaera tabellens innehåll
    # state.display_df_courses = filtered
    # state.display_df_programs = filtered_programs

    # Count KPI:er
    # len to get a number how many row filtered and filtered_programs has.
    # Filtered is a variable with value of choosing organizer
    state.total_applied_courses = check_zero(len(filtered))
    state.total_applied_programs = check_zero(len(filtered_programs))

    state.amount_beviljade_courses = check_zero(len(filter_desicion(filtered)))
    state.amount_beviljade_programs = check_zero(len(filter_desicion(filtered_programs)))

    state.course_approved_spots = check_zero(count_approved_spots(filtered))

    # filtered_programs is the new data
    # sum all in column sökta platser totalt
    # notna to find out if value is nan, return false if it is nan
    state.sokta_platser = check_zero(filtered_programs["Sökta platser totalt"].sum())
    state.beviljade_platser = check_zero(
        filtered_programs["Beviljade platser totalt"].sum()
    )

    # For courses, counting percentage
    state.percentage_courses = count_percentage(
        state.amount_beviljade_courses, state.total_applied_courses
    )

    # For programs, counting percentage
    state.percentage_programs = count_percentage(
        state.amount_beviljade_programs, state.total_applied_programs
    )
    state.count_stats = count_percentage(state.beviljade_platser, state.sokta_platser)
    
    # === End ===

    # === Alex start ===

def update_end_year(state): # 3
    if not state.start_year:
        notify(state, "warning", "Välj ett startår först")
        return
    state.valid_end_years = [year for year in state.years if int(year) > int(state.start_year)]
    if not state.end_year or int(state.end_year) < int(state.start_year):
        state.end_year = state.valid_end_years[0] 

