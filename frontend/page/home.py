import taipy.gui.builder as tgb
from taipy.gui import navigate




image_map = "picture/karta.PNG"
image_students = "picture/studenter.PNG"
image_government = "picture/statsbidrag.PNG"
image_organizer = "picture/anordnare.PNG"


def image_karta(state):
    navigate(state, "Karta")


def image_anordnare(state):
    navigate(state, "Anordnare")


def image_student(state):
    navigate(state, "Studenter")


def image_statsbidrag(state):
    navigate(state, "Statsbidrag")


with tgb.Page() as home_page:
    # tgb.navbar()
    tgb.toggle(theme=True)
    with tgb.part(class_name="card text-center card-margin"):
        tgb.text("# Välkommen till **The skool**", mode="md")

    with tgb.part():
        with tgb.part(class_name="text-center card-margin"):
            with tgb.part(class_name="card card-margin"):
                with tgb.layout(columns=("1 1 1 1")):
                    with tgb.part():
                        tgb.image(
                            "{image_map}",
                            label= "Karta",
                            on_action=image_karta,
                            class_name="hover_color picture_style",
                        )
                    with tgb.part():
                        tgb.image(
                            "{image_organizer}",
                            label= "Anordnare",
                            on_action=image_anordnare,
                            class_name="hover_color picture_style",
                        )
                    with tgb.part():
                        tgb.image(
                            "{image_students}",
                            label="Studenter",
                            on_action=image_student,
                            class_name="hover_color picture_style",
                            mode= "md"
                        )
                    with tgb.part():
                        tgb.image(
                            "{image_government}",
                            label="Statsbidrag",
                            on_action=image_statsbidrag,
                            class_name="hover_color picture_style",
                            mode= "md"
                        )
