import taipy.gui.builder as tgb
from taipy.gui import navigate


current_page = "Hem"

image_map = "public/map.png"



def image_click(state):
    navigate(state, "Karta")

with tgb.Page() as home_page:
    # tgb.navbar()
    tgb.toggle(theme=True)
    with tgb.part(class_name= "card text-center card-margin"):
        tgb.text("# Välkommen till **The skool**", mode = "md")
        
    with tgb.part():
        with tgb.part(class_name= "card text-center card-margin"):
            tgb.image("{image_map}", on_action=image_click)
            
        
    
        
        
        
        
