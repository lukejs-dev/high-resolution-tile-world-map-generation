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


def run_interactive_mode():
    """
    Guides the user through an interactive setup process to generate a map.
    Returns a tuple of (map_name, generation_config).
    """
    print("--- Interactive Map Generator ---")
    print("This wizard will guide you through creating a custom map.\n")

    # 1. Get map name
    map_name = ""
    while not map_name:
        map_name = input("▶ Enter a name for your map folder (e.g., 'my_first_map'): ").strip()
        if not map_name:
            print("  Error: Map name cannot be empty.")

    gen_config = {}

    # Helper for yes/no questions
    def ask_yes_no(prompt, default_yes=True):
        options = "(Y/n)" if default_yes else "(y/N)"
        while True:
            answer = input(f"▶ {prompt} {options} ").strip().lower()
            if answer in ["y", "yes"]:
                return True
            if answer in ["n", "no"]:
                return False
            if answer == "":
                return default_yes
            print(f"  Error: Please enter 'y' or 'n'.")

    # 2. Feature questions
    print("\n--- Features ---")
    gen_config["add_land_cover"] = ask_yes_no("Use satellite-style land cover?", default_yes=False)
    gen_config["add_borders"] = ask_yes_no("Add country borders?")
    gen_config["add_rivers"] = ask_yes_no("Add rivers?")
    gen_config["add_shaded_relief"] = ask_yes_no("Add elevation shading (topographic relief)?")

    # 3. Color questions
    print("\n--- Colors ---")
    if ask_yes_no("Customize map colors?", default_yes=False):
        def ask_color(prompt, default):
            color = input(f"  ▶ {prompt} (default: {default}): ").strip()
            return color if color else default

        if not gen_config.get("add_land_cover"):
             gen_config["land_color"] = ask_color("Land color", config.DEFAULT_LAND_COLOR)
        gen_config["ocean_color"] = ask_color("Ocean color", config.DEFAULT_OCEAN_COLOR)
        if gen_config.get("add_rivers"):
            gen_config["river_color"] = ask_color("River color", config.DEFAULT_RIVER_COLOR)
        if gen_config.get("add_borders"):
            gen_config["border_color"] = ask_color("Border color", config.DEFAULT_BORDER_COLOR)

    return map_name, gen_config

def main():
    """Main execution function."""
    # Set up basic logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(
        description="Generate and slice high-resolution world maps for Roblox.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Mode argument
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="Run the tool in an interactive, step-by-step mode."
    )

    # Core arguments
    parser.add_argument("-n", "--name", type=str, help="The output name for the map folder (required in non-interactive mode).")
    parser.add_argument(
        "-s", "--style", type=str, choices=config.MAP_STYLES.keys(), help="A preset style to use as a base."
    )

    # Feature flags
    features = parser.add_argument_group("features")
    features.add_argument("--borders", action="store_true", help="Render country borders.")
    features.add_argument("--rivers", action="store_true", help="Render major rivers.")
    features.add_argument("--shaded-relief", action="store_true", help="Add elevation shading.")
    features.add_argument("--land-cover", action="store_true", help="Use satellite/texture for land.")

    # Color overrides
    colors = parser.add_argument_group("colors")
    colors.add_argument("--ocean-color", type=str, help="Hex code for ocean color.")
    colors.add_argument("--land-color", type=str, help="Hex code for land color.")
    colors.add_argument("--river-color", type=str, help="Hex code for river color.")
    colors.add_argument("--border-color", type=str, help="Hex code for border color.")

    args = parser.parse_args()

    if args.interactive:
        map_name, gen_config = run_interactive_mode()
    else:
        # --- Build Configuration from CLI args ---
        if not args.name:
            parser.error("--name is required in non-interactive mode.")
        map_name = args.name
        gen_config = {}

        # Load a preset style if provided
        if args.style:
            logging.info(f"Loading preset style: '{args.style}'")
            gen_config.update(config.MAP_STYLES[args.style])

        # Override with any specified feature flags
        if args.borders: gen_config["add_borders"] = True
        if args.rivers: gen_config["add_rivers"] = True
        if args.shaded_relief: gen_config["add_shaded_relief"] = True
        if args.land_cover: gen_config["add_land_cover"] = True

        # Override with any specified colors
        if args.ocean_color: gen_config["ocean_color"] = args.ocean_color
        if args.land_color: gen_config["land_color"] = args.land_color
        if args.river_color: gen_config["river_color"] = args.river_color
        if args.border_color: gen_config["border_color"] = args.border_color

    # --- Map Generation ---
    logging.info(f"--- Starting generation for map '{map_name}' ---")

    # 1. Generate the high-resolution map image in memory
    map_image_data = map_generator.generate_map(
        width_px=config.HIGH_RES_WIDTH,
        height_px=config.HIGH_RES_HEIGHT,
        dpi=config.DPI,
        **gen_config,
    )

    # 2. Slice the image into tiles and save them
    slicer.slice_and_save_map(map_name, map_image_data, config.TILE_SIZE, config.EXPORT_ROOT_DIR)

    logging.info("\nAll map generation tasks are complete!")


if __name__ == "__main__":
    main()
