import argparse
import ujson
import logging

from .items_parser import ItemsParser

options = ["all", "skins", "stickers", "patches", "graffities", "musickits", "agents", "containers", "container_keys", "pins", "passes", "keychains"]

def save_to_file(data, output, pretty=False):
    with open(output, "w") as f:
        if pretty:
            f.write(ujson.dumps(data, indent=4))
        else:
            f.write(ujson.dumps(data))

    logging.info(f"Data saved to {output}")

def main():
    parser = argparse.ArgumentParser(description="CS Items Parser CLI")

    parser.add_argument(
        "-t", "--type",
        choices=options,
        required=True,
        default="all",
        help="Type of items to parse"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default="output.json",
        help="Output file path"
    )

    parser.add_argument(
        "--pretty",
        action="store_true",
        default=False,
        help="Add indentation to the output JSON file"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose output"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    items_parser = ItemsParser()
    items_parser.update_files()

    if args.type == "all":
        save_to_file({
            "skins": items_parser.get_skins(),
            "stickers": items_parser.get_stickers(),
            "patches": items_parser.get_patches(),
            "graffities": items_parser.get_graffities(),
            "musickits": items_parser.get_musickits(),
            "agents": items_parser.get_agents(),
            "containers": items_parser.get_containers(),
            "container_keys": items_parser.get_container_keys(),
            "pins": items_parser.get_pins(),
            "passes": items_parser.get_passes(),
            "keychains": items_parser.get_keychains()
        }, args.output)

    if args.type == "skins":
        save_to_file({
            "skins": items_parser.get_skins()
        }, args.output)

    if args.type == "stickers":
        save_to_file({
            "stickers": items_parser.get_stickers()
        }, args.output)

    if args.type == "patches":
        save_to_file({
            "patches": items_parser.get_patches()
        }, args.output)

    if args.type == "graffities":
        save_to_file({
            "graffities": items_parser.get_graffities()
        }, args.output)

    if args.type == "musickits":
        save_to_file({
            "musickits": items_parser.get_musickits()
        }, args.output)

    if args.type == "agents":
        save_to_file({
            "agents": items_parser.get_agents()
        }, args.output)

    if args.type == "containers":
        save_to_file({
            "containers": items_parser.get_containers()
        }, args.output)

    if args.type == "container_keys":
        save_to_file({
            "container_keys": items_parser.get_container_keys()
        }, args.output)

    if args.type == "pins":
        save_to_file({
            "pins": items_parser.get_pins()
        }, args.output)

    if args.type == "passes":
        save_to_file({
            "passes": items_parser.get_passes()
        }, args.output)

    if args.type == "keychains":
        save_to_file({
            "keychains": items_parser.get_keychains()
        }, args.output)

if __name__ == "__main__":
    main()
