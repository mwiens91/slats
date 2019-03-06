"""Contains functions for Spotify integration."""

from typing import Dict, Optional
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


def get_client(client_id: str, client_secret: str) -> Spotify:
    """Returns a spotipy.Spotify object.

    Args:
        client_id: A Spotify developer client ID.
        client_secret: A Spotify developer client secret.

    Returns:
        A spotify.Spotify client.
    """
    return Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )
    )


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
