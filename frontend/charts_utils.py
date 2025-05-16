def horizontal_bar_options(ax, **options):
    ax.invert_yaxis()

    ax.set_title(
        label=options.get("title", ""),
        pad=options.get("title_pad", 10),
        loc="left",
    )
    ax.set_xlabel(options.get("xlabel", ""), loc="left")
    ax.set_ylabel(options.get("ylabel", ""), rotation=options.get("ylabel_rotation", 0))
    ax.yaxis.set_label_coords(
        options.get("ylabel_x_coord", -0.1), options.get("ylabel_y_coord", 1)
    )

    ax.legend().remove()

    return ax