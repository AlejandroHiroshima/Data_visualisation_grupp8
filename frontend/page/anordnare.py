from taipy.gui import Gui
import taipy.gui.builder as tgb
import pandas as pd
from backend.data_processing import reading_file_course, reading_file_programs
from backend.update import change_data, update_year




# Dataframe global courses
global_dict_course = reading_file_course()


# Dataframe global programs
global_dict_programs = reading_file_programs()


# Initializ bindings variable
display_df_courses = pd.DataFrame()
display_df_programs = pd.DataFrame()
organizer_list = []
selected_organizer = None
year = None
amount_beviljade_courses = "-"
total_applied_courses = "-"
amount_beviljade_programs = "-"
total_applied_programs = "-"
percentage_courses = "-"
percentage_programs = "-"
sokta_platser = "-"
beviljade_platser = "-"
count_stats = "-"
course_applied_spots = "-"
course_approved_spots = "-"
stats_platser_kurs = "-"


with tgb.Page() as Organizer:
    tgb.navbar()
    tgb.toggle(theme=True)
    with tgb.part(class_name="card text-center card-margin"):
        tgb.text("# Kpi:er för **anordnare** på **yrkeshögskolor**", mode="md", raw=True)
        tgb.text("KPI:erna är baserad på offentliga excel-data över inkomna och beviljade platser för kurser och prgram åren mellan 2020 - 2024. \n Där data för 2020 för kurser så finns det bara beviljade.", mode= "md")

    with tgb.part(class_name="container"):
        with tgb.part(class_name=" card card-margin"):
            with tgb.layout(columns="1 2 1"):
                with tgb.part():
                    tgb.selector(
                        value="{year}",
                        label="Välj år",
                        lov=[2024, 2023, 2022, 2021, 2020],
                        dropdown=True,
                        on_change=update_year,
                        class_name="fullwidth",
                        bind="year",
                    )

                with tgb.part():
                    tgb.selector(
                        value="{selected_organizer}",
                        label="Välj anordnare",
                        lov="{organizer_list}",
                        dropdown=True,
                        filter=True,
                        class_name="fullwidth",
                        bind="selected_organizer",
                        disabled="year == None or year == ''",
                    )

                with tgb.part(class_name="text-center"):
                    tgb.button(
                        label="FILTRERA",
                        class_name="plain filter-button government_button",
                        on_action=change_data,
                        disabled="{selected_organizer} == None or {selected_organizer} == '' or {year} == None or {year} == ''",
                        bind=["year", "selected_organizer"],
                    )

    with tgb.part(class_name="container"):
        with tgb.part(class_name="card card-margin"):
            tgb.text(
                "### KPI:er kurser",
                mode="md",
            )
            # start kpi:er, applied courses
            with tgb.part():
                with tgb.layout(columns=("1 1 1 1")):

                    # applied course
                    with tgb.part(class_name="card card-margin text-center"):
                        tgb.text("### Antal ansökta", mode="md")
                        tgb.text(
                            "**{total_applied_courses}**",
                            mode="md",
                            class_name="kpi-value",
                        )

                    # approved course
                    with tgb.part(class_name="card card-margin text-center"):
                        tgb.text("### Antal beviljade", mode="md")
                        tgb.text(
                            "**{amount_beviljade_courses}**",
                            mode="md",
                            class_name="kpi-value",
                        )

                    # stats for courses, approved / applied
                    with tgb.part(class_name="card card-margin text-center"):
                        tgb.text("### Beviljandegrad", mode="md")
                        tgb.text(
                            "**{percentage_courses}**",
                            mode="md",
                            class_name="kpi-value",
                        )

                    # amount of spots for courses
                    with tgb.part(class_name="card card-margin text-center"):
                        tgb.text("### Beviljade platser", mode="md")
                        tgb.text(
                            "**{course_approved_spots}**",
                            mode="md",
                            class_name="kpi-value",
                        )

    # # data set for courses
    # with tgb.part(class_name= "card"):
    #     tgb.text("## DATA KURSER", mode="md")
    #     tgb.html("br")
    #     tgb.table(data="{display_df_courses}", rebuild=True)

    with tgb.part(class_name="container"):
        with tgb.part(class_name="card card-margin"):
            tgb.text("### KPI:er för program", mode= "md")

            # how many programs and approved
            with tgb.layout(columns=("1 1 1")):

                with tgb.part(class_name="card card-margin text-center"):
                    tgb.text("### Antal ansökta", mode="md")
                    tgb.text(
                        "**{total_applied_programs}**",
                        mode="md",
                        class_name="kpi-value",
                    )

                with tgb.part(class_name="card card-margin text-center"):
                    tgb.text("### Antal beviljande", mode="md")
                    tgb.text(
                        "**{amount_beviljade_programs}**",
                        mode="md",
                        class_name="kpi-value",
                    )

                with tgb.part(class_name="card card-margin text-center"):
                    tgb.text("### Beviljandegrad", mode="md")
                    tgb.text(
                        "**{percentage_programs}**", mode="md", class_name="kpi-value"
                    )

            # spots program
            with tgb.layout(columns=("1 1 1")):

                with tgb.part(class_name="card card-margin text-center"):
                    tgb.text("### Antal ansökta platser", mode="md")
                    tgb.text("**{sokta_platser}**", mode="md", class_name="kpi-value")

                with tgb.part(class_name="card card-margin text-center"):
                    tgb.text("### Antal beviljande platser", mode="md")
                    tgb.text(
                        "**{beviljade_platser}**", mode="md", class_name="kpi-value"
                    )

                with tgb.part(class_name="card card-margin text-center"):
                    tgb.text("### Beviljandegrad platser", mode="md")
                    tgb.text("**{count_stats}**", mode="md", class_name="kpi-value")

    # with tgb.part(class_name= "card"):
    #     with tgb.part(class_name="container"):
    #         tgb.text("## DATA PROGRAMS", mode="md")
    #         tgb.table(data="{display_df_programs}", rebuild=True)


if __name__ == "__main__":
    Gui(page, css_file="style.css").run(dark_mode=False, use_reloader=False, port=8080)
