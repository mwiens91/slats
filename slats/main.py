"""Contains the main function."""

from .config import parse_config_file
from .runtime_args import parse_runtime_args
from .spotify import get_album_uri, get_client


def main():
    """The main function."""
    # Get runtime arguments
    cli_args = parse_runtime_args()

    # Parse config file
    config_dict = parse_config_file(config_path=cli_args.config)

    # Initialize Spotify API client
    spotify = get_client(
        username=config_dict["spotify-username"],
        client_id=config_dict["spotify-client-id"],
        client_secret=config_dict["spotify-client-secret"],
        redirect_uri=config_dict["spotify-redirect-uri"],
        cache_path=cli_args.cache,
    )

    # DEBUG
    album = get_album_uri(
        client=spotify, album_artist="Arcade Fire", album="Funeral"
    )
    print(album)
