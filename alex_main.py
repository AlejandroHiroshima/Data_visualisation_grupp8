import taipy.gui.builder as tgb
from taipy.gui import Gui
import pandas as pd
import chardet
from pathlib import Path

DATA_DIRECTORY = Path(__file__).parents[0] / "data"

def read_csv(sub_category, file_name, separator = ';'):
    file_path = DATA_DIRECTORY / sub_category / file_name
    print(f"file_path: {file_path}") 
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())

    return pd.read_csv(
        file_path,
        encoding=result['encoding'],
        sep=separator
    )

try:
    df = read_csv(sub_category="2024_kurser", file_name="studerande_examinerad_yrkeshogskola.csv")
except FileNotFoundError as e:
    print(f"Fel: {e}")
    df = pd.DataFrame()  # Skapa en tom DataFrame om filen inte hittas

with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        tgb.text("# Studenter på Yrkeshögskola", mode="md")
        tgb.text("### Utveckling över tid per utvecklingsområde", mode="md")
        with tgb.part(class_name="card"):
            tgb.text("Rådata:", mode="md")
            tgb.table("{df}")

if __name__ == "__main__":
    Gui(page).run(dark_mode=False, use_reloader=True, port=8080)