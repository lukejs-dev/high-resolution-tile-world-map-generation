"""
Configuration file for the map generator.
"""
import os

# --- Image & Rendering Configuration ---
# High-resolution dimensions. Equirectangular is a 2:1 aspect ratio.
# 8192 = 8 * 1024, so this will give us an 8x4 grid of 1024x1024 tiles.
HIGH_RES_WIDTH = 8192
HIGH_RES_HEIGHT = 4096
DPI = 100  # Dots per inch for rendering

# Roblox's max image size
TILE_SIZE = 1024

# --- Path Configuration ---
EXPORT_ROOT_DIR = "exported_maps"

# --- Default Style Colors ---
DEFAULT_OCEAN_COLOR = "#a0d1f1"
DEFAULT_LAND_COLOR = "#94c27c"
DEFAULT_RIVER_COLOR = "#6ab3f7"
DEFAULT_BORDER_COLOR = "gray"

# --- Map Style Definitions ---
# Defines presets that can be loaded with the --style flag.
# These can be overridden by other command-line arguments.
MAP_STYLES = {
    "blank": {
        "land_color": "#d3d3d3",  # Light gray for blank
        "ocean_color": "#f0f0f0",  # Lighter gray for ocean
    },
    "simple": {
        "add_borders": True,
        "add_rivers": True,
    },
    "satellite": {
        "add_land_cover": True,
    },
    "topographic": {
        "add_shaded_relief": True,
        "add_rivers": True,
        "add_borders": True,
    },
    "full": {
        "add_borders": True,
        "add_rivers": True,
        "add_land_cover": True,
        "add_shaded_relief": True,
    },
}
