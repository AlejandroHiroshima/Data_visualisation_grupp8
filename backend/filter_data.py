import pandas as pd

# == filter desicion anordnare Marcus ===
def filter_desicion(filtered):
    filtered = filtered.query("Beslut == 'Beviljad'")

    return filtered

# == End ===

# == 
def filter_data_marcus(df, state):
    
    filtered = df.query("`Anordnare namn` == @state.selected_organizer")

    return filtered





