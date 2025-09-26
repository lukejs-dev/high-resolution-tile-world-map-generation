"""
Handles slicing the high-resolution map into smaller tiles for Roblox.
"""
import os
import io
import logging
from PIL import Image


def slice_and_save_map(map_name, map_data, tile_size, root_dir):
    """
    Slices the generated map into tiles and saves them to a directory.

    Args:
        map_name (str): The name of the map style (e.g., "with_borders").
        map_data (bytes): The raw PNG data of the full map.
        tile_size (int): The width and height of each square tile.
        root_dir (str): The root directory to save the output folder in.
    """
    logging.info(f"Slicing and saving map '{map_name}'...")

    # Create the directory for this map version
    output_dir = os.path.join(root_dir, map_name)
    os.makedirs(output_dir, exist_ok=True)

    # Load the full map image from the byte data
    full_map = Image.open(io.BytesIO(map_data))

    # Save the full high-resolution map for reference
    full_map.save(os.path.join(output_dir, "full_map.png"))

    # Calculate the number of tiles
    num_tiles_x = full_map.width // tile_size
    num_tiles_y = full_map.height // tile_size

    # Slice the image and save each tile
    for y in range(num_tiles_y):
        for x in range(num_tiles_x):
            tile = full_map.crop((x * tile_size, y * tile_size, (x + 1) * tile_size, (y + 1) * tile_size))

            tile_name = f"{map_name}_{x}_{y}.png"
            tile.save(os.path.join(output_dir, tile_name))

    logging.info(f"Slicing complete. {num_tiles_x * num_tiles_y} tiles saved in '{output_dir}'.")
