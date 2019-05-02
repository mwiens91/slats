"""Contains the main function."""

import json
import sys
from colorama import Fore, Style
import jsonschema
from .config import parse_config_file
from .constants import ALBUMS_JSON_SCHEMA
from .exceptions import ConfigFileNotFound
from .runtime_args import parse_runtime_args
from .spotify import (
    get_album_uri,
    get_client,
    get_users_name,
    get_users_saved_albums,
    save_albums,
)


def main():
    """The main function."""
    # Get runtime arguments
    cli_args = parse_runtime_args()

    # Parse config file
    try:
        config_dict = parse_config_file(config_path=cli_args.config)
    except ConfigFileNotFound:
        print(Fore.RED + "Configuration not found" + Style.RESET_ALL)
        sys.exit(1)

    # Parse and validate passed in JSON file
    try:
        with open(cli_args.albums_json) as jsonfile:
            albums = json.load(jsonfile)
    except FileNotFoundError:
        print(
            Fore.RED + "%s not found" % cli_args.albums_json + Style.RESET_ALL
        )
        sys.exit(1)

    try:
        jsonschema.validate(instance=albums, schema=ALBUMS_JSON_SCHEMA)
    except jsonschema.ValidationError:
        print(
            Fore.RED
            + "%s failed to validate against schema" % cli_args.albums_json
            + Style.RESET_ALL
        )
        sys.exit(1)

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
        sys.exit(1)

    # Print a welcome message
    print(
        Fore.GREEN
        + "Successfully authenticated %s" % get_users_name(spotify)
        + Style.RESET_ALL
    )
    print()

    # Save albums
    saved_albums = get_users_saved_albums(spotify)

    try:
        for album in albums:
            print(
                "Attempting to find "
                + Style.BRIGHT
                + album["album"]
                + Style.RESET_ALL
                + " by "
                + Style.BRIGHT
                + album["album_artist"]
                + Style.RESET_ALL
            )

            album_result = get_album_uri(
                spotify, album["album_artist"], album["album"]
            )

            if album_result is None:
                print(
                    Fore.RED
                    + "Failed to find %s by %s"
                    % (album["album"], album["album_artist"])
                    + Style.RESET_ALL
                )
                print()
                continue

            print(
                "Found "
                + Style.BRIGHT
                + album_result["album_name"]
                + Style.RESET_ALL
                + " by "
                + Style.BRIGHT
                + album_result["artist_name"]
                + Style.RESET_ALL
            )

            if album_result["album_uri"] in saved_albums:
                print(
                    Fore.GREEN
                    + "%s by %s is already saved! skipping"
                    % (album_result["album_name"], album_result["artist_name"])
                    + Style.RESET_ALL
                )
            else:
                # We *could* build up a big list and save all the albums
                # at once, but if the list of albums is big then this
                # isn't a good idea. We could be more efficient and save
                # in chunks, but this is good enough for most purposes.
                save_albums(spotify, [album_result["album_uri"]])

            print()
    except KeyboardInterrupt:
        print(Fore.RED + "Aborting" + Style.RESET_ALL)
        sys.exit(1)
