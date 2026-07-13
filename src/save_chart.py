import os

CHARTS_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "Charts"
)


def save_chart(fig, filename):
    if not os.path.exists(CHARTS_FOLDER):
        os.mkdir(CHARTS_FOLDER)

    save_path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return save_path
