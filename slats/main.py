"""Contains the main function."""

import json
import sys
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
        print("Configuration not found")
        sys.exit(1)

    # Parse and validate passed in JSON file
    try:
        with open(cli_args.albums_json) as jsonfile:
            albums = json.load(jsonfile)
    except FileNotFoundError:
        print("%s not found" % cli_args.albums_json)
        sys.exit(1)

    try:
        jsonschema.validate(instance=albums, schema=ALBUMS_JSON_SCHEMA)
    except jsonschema.ValidationError:
        print("%s failed to validate against schema" % cli_args.albums_json)
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
    print("Successfully authenticated %s" % get_users_name(spotify))
    print()

    # Build up a list of new albums to save
    new_albums = []
    saved_albums = get_users_saved_albums(spotify)

    for album in albums:
        print(
            "Attempting to find %s by %s"
            % (album["album"], album["album_artist"])
        )

        album_result = get_album_uri(
            spotify, album["album_artist"], album["album"]
        )

        if album_result is None:
            print(
                "Failed to find %s by %s"
                % (album["album"], album["album_artist"])
            )
            continue

        print(
            "Found %s by %s"
            % (album_result["album_name"], album_result["artist_name"])
        )

        if album_result["album_uri"] in saved_albums:
            print(
                "%s by %s is already saved! skipping"
                % (album_result["album_name"], album_result["artist_name"])
            )
        else:
            new_albums.append(album_result["album_uri"])

        print()

    # Save all albums
    if new_albums:
        save_albums(spotify, new_albums)
