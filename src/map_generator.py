"""
Core map generation logic using Matplotlib and Cartopy.
"""
import io
import logging
from PIL import Image
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io import srtm

# Disable obnoxious UserWarnings from Pillow when saving large images
Image.MAX_IMAGE_PIXELS = None


def generate_map(
    width_px,
    height_px,
    dpi,
    add_borders=False,
    add_rivers=False,
    add_shaded_relief=False,
    add_land_cover=False,
):
    """
    Generates a map image in memory based on the specified features.

    Returns:
        bytes: The map image data in PNG format.
    """
    logging.info("Generating map with the following features:")
    logging.info(f"  - Borders: {add_borders}")
    logging.info(f"  - Rivers: {add_rivers}")
    logging.info(f"  - Shaded Relief: {add_shaded_relief}")
    logging.info(f"  - Land Cover: {add_land_cover}")

    # 1. Set up the plot and projection
    fig_width_in = width_px / dpi
    fig_height_in = height_px / dpi
    fig = plt.figure(figsize=(fig_width_in, fig_height_in), dpi=dpi)

    # Use Equirectangular projection (Plate Carree in Cartopy)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_global()  # Extent is the whole world

    # 2. Add map features based on configuration
    ax.add_feature(cfeature.OCEAN, zorder=0, facecolor="#a0d1f1")

    if add_land_cover:
        ax.stock_img()
    else:
        ax.add_feature(cfeature.LAND, zorder=0, facecolor="#94c27c")

    if add_shaded_relief:
        logging.info("Adding shaded relief (may download data on first run)...")
        shade = srtm.SRTM3Source(regrid_shape=(width_px // 4, height_px // 4))
        ax.add_raster(shade.shaded_relief, cmap="gray", zorder=2, alpha=0.3)

    if add_rivers:
        ax.add_feature(cfeature.RIVERS.with_scale("10m"), zorder=3, edgecolor="#6ab3f7")

    if add_borders:
        ax.add_feature(
            cfeature.BORDERS.with_scale("10m"), zorder=4, edgecolor="gray", linestyle="--"
        )

    ax.add_feature(cfeature.COASTLINE.with_scale("10m"), zorder=5, edgecolor="black", linewidth=0.5)

    # 3. Render the map to an in-memory buffer
    fig.patch.set_alpha(0)
    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0, dpi=dpi)
    plt.close(fig)
    buf.seek(0)

    logging.info("Map generation complete.")
    return buf.read()
