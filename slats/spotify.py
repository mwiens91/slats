"""Contains functions for Spotify integration."""

from typing import Dict, Optional
from spotipy import Spotify
from spotipy.util import prompt_for_user_token


def get_client(
    username: str, client_id: str, client_secret: str, redirect_uri: str
) -> Spotify:
    """Returns a spotipy.Spotify object.

    In authenticating a Spotify client, this prompts user for
    authentication and as a side effect saves a cache in the CWD.

    TODO: save the cache in a sensible location.

    Args:
        username: A Spotify user identifier.
        client_id: A Spotify developer client ID.
        client_secret: A Spotify developer client secret.
        redirect_uri: A whitelisted URI to redirect to after authenticating.

    Returns:
        A spotify.Spotify client.
    """
    token = prompt_for_user_token(
        username=username,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-library-modify",
    )
    return Spotify(auth=token)


def get_album_uri(
    client: Spotify, album_artist: str, album: str
) -> Optional[Dict[str, str]]:
    """Retrieve the URI for an album

    Args:
        client: A spotipy Spotify client.
        album_artist: The artist who released the album.
        album: The album name.

    Returns:
        A dictionary containing the artist name, album name, and album
        URI, if an could be found; otherwise, None.
    """
    # Search
    response = client.search(q="%s %s" % (album_artist, album), type="album")

    # Return None if no albums found
    if not response["albums"]["items"]:
        return None

    # Return the top search hit
    top_hit = response["albums"]["items"][0]

    album_dict = dict(
        artist_name=top_hit["artists"][0]["name"],
        album_name=top_hit["name"],
        album_uri=top_hit["uri"],
    )

    return album_dict
