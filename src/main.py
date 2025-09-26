"""
Main entry point for the Roblox Map Generator tool.

This script parses command-line arguments to generate specific map styles.
"""
import argparse
import logging

# Import project modules
from . import config
from . import map_generator
from . import slicer


def main():
    """Main execution function."""
    # Set up basic logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Generate and slice high-resolution world maps for Roblox.")
    parser.add_argument(
        "--style",
        type=str,
        choices=config.MAP_STYLES.keys(),
        help="The name of the map style to generate.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate all available map styles defined in config.py.",
    )
    args = parser.parse_args()

    if not args.style and not args.all:
        parser.error("No action requested. Please specify a --style or use --all.")
        return

    # --- Map Generation ---
    styles_to_generate = config.MAP_STYLES.keys() if args.all else [args.style]

    for style_name in styles_to_generate:
        logging.info(f"--- Starting generation for style '{style_name}' ---")
        style_config = config.MAP_STYLES[style_name]

        # 1. Generate the high-resolution map image in memory
        map_image_data = map_generator.generate_map(
            width_px=config.HIGH_RES_WIDTH,
            height_px=config.HIGH_RES_HEIGHT,
            dpi=config.DPI,
            **style_config,
        )

        # 2. Slice the image into tiles and save them
        slicer.slice_and_save_map(
            style_name, map_image_data, config.TILE_SIZE, config.EXPORT_ROOT_DIR
        )

    logging.info("\nAll map generation tasks are complete!")


if __name__ == "__main__":
    main()
