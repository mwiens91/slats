"""Contains functions to parse runtime arguments."""

import argparse
from .version import DESCRIPTION, NAME, VERSION


def parse_runtime_args() -> argparse.Namespace:
    """Parse runtime args using argparse.

    Returns:
        An argparse.Namespace containing the runtime arguments as
        attributes.
    """
    # Main runtime options
    parser = argparse.ArgumentParser(
        prog=NAME, description="%(prog)s - " + DESCRIPTION
    )
    parser.add_argument(
        "--albums-json",
        required=True,
        help="path to albums JSON file (see readme for details)",
    )
    parser.add_argument(
        "--cache",
        default=None,
        help="explicit path to save user-authenticated Spotify API token info to",
    )
    parser.add_argument(
        "--config", default=None, help="explicit path to config file"
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + VERSION
    )

    return parser.parse_args()
