

def horizontal_bar(ax, **option):
    
    ax.invert_yaxis()

    # clutter
    ax.tick_params("y", length=0, pad=option.get("y_tick_params", 10))
    

    # Describle title and label -> call to action
    ax.set_title(
        option.get("title", ""),
        loc="left",
        pad=option.get("pad", 15),
    )
    # contrast
    ax.set_ylabel(option.get("y_title", ""), loc="top", rotation=option.get("rotation", 0), fontsize=option.get("y_font", 12))
    ax.yaxis.set_label_coords(option.get("ylabel_xcoords", 0), option.get("ylabel_ycoords", 0))
    ax.set_xlabel(option.get("x_title", ""), loc="left", fontsize=option.get("x_font", 12))
    ax.set_facecolor(option.get("facecolor", "#E0E0DA"))
    
    # ax.legend().remove()
    return ax



def save_fig_from_ax(ax, fig_path, **option):
    
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(fig_path, dpi= option.get("dpi", 300))