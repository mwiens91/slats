"""Contains the main function."""

from .runtime_args import parse_runtime_args


def main():
    """The main function."""
    # Get runtime arguments
    cli_args = parse_runtime_args()
