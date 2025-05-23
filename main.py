from taipy.gui import Gui
from frontend.page.karta_dashboard import map_page
from frontend.page.home import home_page
# from frontend.page.kurser_dashboard import page

pages = {"Hem": home_page,"Karta": map_page}

Gui(pages=pages).run(port=8080, dark_mode=False, use_reloader=True)