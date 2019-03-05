"""Contains the main function."""

from .config import parse_config_file
from .runtime_args import parse_runtime_args
from .spotify import get_client


def main():
    """The main function."""
    # Get runtime arguments
    cli_args = parse_runtime_args()

    # Parse config file
    config_dict = parse_config_file(config_path=cli_args.config)

    # Initialize Spotify API client
    spotify = get_client(
        client_id=config_dict["spotify-client-id"],
        client_secret=config_dict["spotify-client-secret"],
    )

    # DEBUG
    artist_uri = "spotify:artist:2WX2uTcsvV5OnS0inACecP"

    results = spotify.artist_albums(artist_uri, album_type="album")
    albums = results["items"]
    while results["next"]:
        results = spotify.next(results)
        albums.extend(results["items"])

    for album in albums:
        print(album["name"])
