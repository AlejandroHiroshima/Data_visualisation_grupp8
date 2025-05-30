from pathlib import Path
DATA_DIRECTORY = Path(__file__).parents[1] /"data"
EXPORTED_FILES_DIRECTORY = DATA_DIRECTORY / "save_data"
GEOJSON_REGIONS =  DATA_DIRECTORY / "geojson" / "swedish_regions.geojson"

SCHABLON_MOMS = {
    "Data/IT": 74100,
    "Ekonomi, administration och försäljning": 66600,
    "Friskvård och kroppsvård": 79200,
    "Hotell, restaurang och turism":68700,
    "Hälso- och sjukvård samt socialt arbete": 7100,
    "Journalistik och information": 70600,
    "Juridik": 64100,
    "Kultur, media och design": 89400,
    "Lantbruk, djurvård, trädgård, skog och fiske":116700,
    "Pedagogik och undervisning": 75500,
    "Samhällsbyggnad och byggteknik": 74600,
    "Säkerhetstjänster": 66800,
    "Teknik och tillverkning": 91000,
    "Transporttjänster": 85200
}

GRAY_1 = "#CCCCCC"
GRAY_2 = "#657072"
GRAY_3 = "#4A606C"
BLUE_1 = "#1E4E5C"

GOLDEN_YELLOW      = '#FFD700'
AMBER_YELLOW       = '#FFBF00'
MUSTARD_YELLOW     = '#E1AD01'
PASTEL_YELLOW      = '#FFFACD'
LIGHT_GOLD_YELLOW  = '#FAF3A0'
SUNFLOWER_YELLOW   = '#FFC512'
HONEY_GOLD         = "#E9CC7C"

EMERALD_GREEN = '#2CA02C'
LIME_GREEN    = '#32CD32'
FOREST_GREEN  = '#228B22'
MINT_GREEN    = '#98FF98'
SAGE_GREEN    = '#A8BCA1'
TEAL_GREEN    = '#008080'

FIRE_RED      = '#D62728'
CRIMSON_RED   = '#DC143C'
SCARLET_RED   = '#FF2400'
TOMATO_RED    = '#FF6347'
BRICK_RED     = '#B22222'
LIGHT_CORAL   = '#F08080'

ROYAL_PURPLE  = '#9467BD'
VIOLET        = '#8A2BE2'
INDIGO        = '#4B0082'
ORCHID        = '#DA70D6'
PLUM          = '#DDA0DD'
LAVENDER      = '#E6E6FA'

CHOCOLATE_BROWN = '#D2691E'
SADDLEBROWN     = '#8B4513'
SIENNA_BROWN    = '#A0522D'
ROSYBROWN       = '#BC8F8F'
PERU_BROWN      = '#CD853F'
WHEAT_BROWN     = '#F5DEB3'

# Orange färgpalett
ORANGE = "#FFA500"
LIGHT_ORANGE = "#FFB84D"
DARK_ORANGE = "#FF7F32"
PALE_ORANGE = "#FFD699"

# Komplementfärger till orange (blå)
BLUE = "#0000FF"
LIGHT_BLUE = "#66B3FF"
DARK_BLUE = "#003366"
PALE_BLUE = "#99CCFF"
X = "#EAEAEA"