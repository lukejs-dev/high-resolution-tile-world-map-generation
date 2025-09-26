"""
Configuration file for the map generator.
"""
import os

# --- Image & Rendering Configuration ---
# High-resolution dimensions. Equirectangular is a 2:1 aspect ratio.
# 8192 = 8 * 1024, so this will give us an 8x4 grid of 1024x1024 tiles.
HIGH_RES_WIDTH = 8192*2
HIGH_RES_HEIGHT = 4096*2
DPI = 100  # Dots per inch for rendering

# Roblox's max image size
TILE_SIZE = 1024

# --- Path Configuration ---
EXPORT_ROOT_DIR = "exported_maps"

# --- Map Style Definitions ---
# Defines the different map configurations you can generate.
# The keys (e.g., "blank", "with_borders") will be used as command-line arguments.
MAP_STYLES = {
    "blank": {},
    "with_borders": {"add_borders": True},
    "with_rivers": {"add_rivers": True},
    "with_land_cover": {"add_land_cover": True},
    "with_shaded_relief": {"add_shaded_relief": True},
    "full_no_labels": {
        "add_borders": True,
        "add_rivers": True,
        "add_land_cover": True,
        "add_shaded_relief": True,
    },
}
