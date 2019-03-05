"""Contains functions for Spotify integration."""

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
