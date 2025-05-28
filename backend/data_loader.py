import pandas as pd
from backend.data_processing import read_excel, clean_df, clean_columns

def load_funding_data():
    try:
        df = read_excel(sub_category="statliga_bidrag", file_name="ek_4_utbet_arsplatser_utbomr.xlsx")
        df = clean_df(df)
        df.columns = list(map(clean_columns, df.columns))
        return df
    except FileNotFoundError as e:
        print(f"Fel: {e}") 
        return pd.DataFrame()