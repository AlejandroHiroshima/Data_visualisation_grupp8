from taipy.gui import Gui
from frontend.page.map_dashboard import map_page
from frontend.page.home import home_page
from frontend.page.organizer import Organizer
from frontend.page.students import number_students_educationalarea_year
from frontend.page.government_funding import government_grant_per_program


pages = {
    "Hem": home_page,
    "Karta": map_page,
    "Anordnare": Organizer,
    "Studenter": number_students_educationalarea_year,
    "Statsbidrag": government_grant_per_program,
}


if __name__ == "__main__":
    Gui(pages=pages, css_file="assets/style.css").run(
        port=8080,
        dark_mode=True,
        use_reloader=False,
        title="Elvins Dashboard",
        watermark="Elvins Dashboard",
    )