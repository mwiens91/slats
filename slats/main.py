"""Contains the main function."""

from .config import parse_config_file
from .exceptions import ConfigFileNotFound
from .runtime_args import parse_runtime_args
from .spotify import (
    get_album_uri,
    get_client,
    get_users_name,
    get_users_saved_albums,
)


def main():
    """The main function."""
    # Get runtime arguments
    cli_args = parse_runtime_args()

    # Parse config file
    try:
        config_dict = parse_config_file(config_path=cli_args.config)
    except ConfigFileNotFound:
        print("Configuration not found")

    # Initialize Spotify API client
    try:
        spotify = get_client(
            username=config_dict["spotify-username"],
            client_id=config_dict["spotify-client-id"],
            client_secret=config_dict["spotify-client-secret"],
            redirect_uri=config_dict["spotify-redirect-uri"],
            cache_path=cli_args.cache,
        )
    except KeyboardInterrupt:
        return

    # Print a welcome message
    print("Successfully authenticated %s" % get_users_name(spotify))

    # DEBUG
    from pprint import pprint

    # saved_albums = get_users_saved_albums(client=spotify)
    # pprint(saved_albums)
