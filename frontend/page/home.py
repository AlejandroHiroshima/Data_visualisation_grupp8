import taipy.gui.builder as tgb

with tgb.Page() as home_page:
    tgb.navbar()
    
    tgb.text("# Hem", mode = "md")

