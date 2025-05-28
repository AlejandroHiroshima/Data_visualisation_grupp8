import taipy.gui.builder as tgb
from taipy.gui import Gui


with tgb.Page() as home_page:
    tgb.navbar()
    tgb.toggle(theme=True)
    with tgb.part(class_name= "card text-center card-margin"):
        tgb.text("# Välkommen till **The skool**", mode = "md")
        
        
        
        
        
# if __name__=="__main__":
#     Gui(home_page, css_file="style.css").run(dark_mode=False, use_reloader=False, port=8080)