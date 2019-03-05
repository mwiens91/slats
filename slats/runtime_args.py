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
        "-c", "--config", default=None, help="explicit path to config file"
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + VERSION
    )

    return parser.parse_args()
