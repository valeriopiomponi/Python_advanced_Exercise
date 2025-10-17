from typing import Dict, List, Any
import matplotlib.pyplot as plt

try:
    from PIL import Image
except ImportError as e:
    raise ImportError("Pillow (PIL) is required. Install with: pip install pillow") from e


class UIPresenter:
    """
    UI layer:
    - Shows the image
    - Displays a table (first 5 non-zero numeric params) UNDER the image, same figure
    """

    def __init__(self):
        pass

    def show_image_and_table(self, image_path: str, rows: List[Dict[str, Any]]) -> None:
        """
        Render image on top and a table underneath in a single figure.
        Assumes rows = [{key, value(float), unit(str)}, ...]
        """
        # Prepare table data (format float nicely)
        headers = ["Key", "Value", "Unit"]
        cell_data = [[r.get("key",""),
                      f"{float(r.get('value', 0.0)):.6g}",
                      r.get("unit","")] for r in rows]

        with Image.open(image_path) as img:
            width, height = img.size
            aspect = width / max(1, height)

            fig, (ax_img, ax_tbl) = plt.subplots(
                2, 1,
                gridspec_kw={"height_ratios": [max(3, aspect), 1]},
                figsize=(10, 8),
                constrained_layout=True
            )

            # Image on top
            ax_img.imshow(img, cmap="viridis")  # let Matplotlib decide default if grayscale
            ax_img.axis("off")
            ax_img.set_title(f"Preview: {image_path}")

        # Table underneath
        ax_tbl.axis("off")
        table = ax_tbl.table(cellText=cell_data, colLabels=headers, loc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.4)

        plt.show()
