"""
Core map generation logic using Matplotlib and Cartopy.
"""
import io
import logging
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io import srtm
from . import config

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
    ocean_color=config.DEFAULT_OCEAN_COLOR,
    land_color=config.DEFAULT_LAND_COLOR,
    river_color=config.DEFAULT_RIVER_COLOR,
    border_color=config.DEFAULT_BORDER_COLOR,
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
    logging.info(f"  - Ocean Color: {ocean_color}")
    logging.info(f"  - Land Color: {land_color}")
    logging.info(f"  - River Color: {river_color}")
    logging.info(f"  - Border Color: {border_color}")

    # 1. Set up the plot and projection
    fig_width_in = width_px / dpi
    fig_height_in = height_px / dpi
    fig = plt.figure(figsize=(fig_width_in, fig_height_in), dpi=dpi)

    # Use Equirectangular projection (Plate Carree in Cartopy)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_global()  # Extent is the whole world

    # 2. Add map features based on configuration
    ax.add_feature(cfeature.OCEAN.with_scale('10m'), zorder=0, facecolor=ocean_color)

    if add_land_cover:
        ax.stock_img()
    else:
        ax.add_feature(cfeature.LAND.with_scale('10m'), zorder=0, facecolor=land_color)

    if add_shaded_relief:
        logging.info("Adding shaded relief (may download data on first run)...")
        # Create a source for the SRTM data and specify a resolution.
        # SRTM3 is 3 arc-second resolution (approx 90m).
        srtm_source = srtm.SRTM3Source()

        # Add the SRTM data as a shaded relief image.
        # The `1` specifies the resolution to use from the source.
        # The `cmap` and `alpha` are applied to the shaded relief.
        ax.add_raster(srtm_source, cmap='gray', alpha=0.5, zorder=2)

    if add_rivers:
        ax.add_feature(cfeature.RIVERS.with_scale("10m"), zorder=3, edgecolor=river_color)

    if add_borders:
        ax.add_feature(
            cfeature.BORDERS.with_scale("10m"), zorder=4, edgecolor=border_color, linestyle="--"
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
