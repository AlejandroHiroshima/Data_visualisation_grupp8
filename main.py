from taipy.gui import Gui
from frontend.page.karta_dashboard import map_page
from frontend.page.home import home_page
from frontend.page.anordnare import Organizer
from frontend.page.alex_main import number_students_educationalarea_year
from frontend.page.statliga_bidrag import government_grant_per_program




pages = {"Hem": home_page, "Anordnare": Organizer, "Karta": map_page, "Studenter_per_utbildningsområde": number_students_educationalarea_year, "Statsbidrag": government_grant_per_program}

if __name__=="__main__":
    Gui(pages=pages).run(port=8080, dark_mode=False, use_reloader=True)