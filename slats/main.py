"""Contains the main function."""

from .config import parse_config_file
from .runtime_args import parse_runtime_args


def main():
    """The main function."""
    # Get runtime arguments
    cli_args = parse_runtime_args()

    # Parse config file
    config_dict = parse_config_file(config_path=cli_args.config)
