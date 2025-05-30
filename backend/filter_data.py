import pandas as pd
from taipy.gui import notify
from frontend.charts_utils import create_linechart
from utils.constant import SCHABLON_MOMS


# == filter desicion anordnare Marcus ===
def filter_desicion(filtered):
    filtered = filtered.query("Beslut == 'Beviljad'")

    return filtered

# == End ===

def filter_data_marcus(df, state):
    
    filtered = df.query("`Anordnare namn` == @state.selected_organizer")

    return filtered

def filter_data(state): 
    if not state.start_year or not state.end_year:
        notify(state, "warning", "Välj både start och slutår")
        state.chart = create_linechart(pd.DataFrame())
        state.kpi_mean = "-"
        state.kpi_peak_year = "-"
        state.kpi_peak_year_value = "-"
        state.kpi_top_area = "-" 
        state.kpi_top_area_value = "-"
        return
    if not state.selected_educational_area_students:
        notify(state, "warning", "Välj minst ett utbildningsområde")
        state.chart = create_linechart(pd.DataFrame())
        state.kpi_mean = "-"
        state.kpi_peak_year = "-"
        state.kpi_peak_year_value = "-"
        state.kpi_top_area = "-"
        state.kpi_top_area_value = "-"
        return
    filtered_df = state.df_cleaned.loc[state.selected_educational_area_students]
    selected_years = [year for year in state.years if int(year) >= int(state.start_year) and int(year) <= int(state.end_year)]
    filtered_df = filtered_df[selected_years]
    dynamix_xlabel = f"År ({state.start_year} - {state.end_year})"
    state.chart = create_linechart(filtered_df, xlabel=dynamix_xlabel, ylabel="Antal Studerande")
    filtered_df = filtered_df.apply(pd.to_numeric, errors= 'coerce') # added this one marcus
    state.kpi_mean = int(filtered_df.mean().mean())
    year_sums = filtered_df.sum(axis=0)
    state.kpi_peak_year = int(year_sums.idxmax())
    state.kpi_peak_year_value = int(year_sums.max())
    area_sums = filtered_df.sum(axis=1)
    state.kpi_top_area = str(area_sums.idxmax())
    state.kpi_top_area_value = int(area_sums.max())
    

def filter_data_funding(state):
    if not state.selected_educational_area:
        notify(state, "warning", "Välj ett Utbildningsområde")
        return
    if not state.year:
        notify(state, "warning", "Välj ett År")
    try:
        state.year_students = state.df.loc[state.selected_educational_area, int(state.year)]
        state.schablon = SCHABLON_MOMS[state.selected_educational_area]
        state.government_funding = state.year_students * state.schablon
    except Exception as e:
        notify(state, "error", f"Ett fel uppstod: {str(e)}")
       

