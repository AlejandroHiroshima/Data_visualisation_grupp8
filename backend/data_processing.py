import pandas as pd
import json
from utils.constant import GEOJSON_REGIONS, EXPORTED_FILES_DIRECTORY

# ===== 1. Ladda data =====
df = pd.read_csv(EXPORTED_FILES_DIRECTORY / "regions_2020_2024_log.csv")
with open(GEOJSON_REGIONS, "r") as file:
    geojson = json.load(file)

