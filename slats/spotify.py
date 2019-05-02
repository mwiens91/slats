"""Contains functions for Spotify integration."""

import os
from typing import Dict, List, Optional
import webbrowser
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from .constants import (
    PROJECT_CONFIG_HOME,
    SPOTIFY_API_LIMIT,
    SPOTIFY_AUTH_SCOPES,
)


def get_client(
    username: str,
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    cache_path: Optional[str],
) -> Spotify:
    """Returns a spotipy.Spotify object.

    If there isn't already cached authentication tokens, this prompts
    the user for authentication by opening up a browser to a Spotify
    authentication page, requests the user to input the URL the Spotify
    authentication page redirects you to (the token is embedded in the
    URL), and saves a cache of the user-authenticated Spotify API
    tokens.

    The file path for the cached token can be explicitly set by passing
    it in as an argument; if no argument is passed in, the path is taken
    to be $XDG_CONFIG_HOME/slats/cache-username (XDG_CONFIG_HOME
    defaults to $HOME/.config).

    Args:
        username: A Spotify user identifier.
        client_id: A Spotify developer client ID.
        client_secret: A Spotify developer client secret.
        redirect_uri: A whitelisted URI to redirect to after authenticating.
        cache_path: An optional Spotify token cache file path.

    Returns:
        A spotify.Spotify client.
    """
    if cache_path is None:
        # Make sure the config directory exists
        os.makedirs(PROJECT_CONFIG_HOME, exist_ok=True)

        cache_path = os.path.join(
            PROJECT_CONFIG_HOME, "cache-%s.json" % username
        )

    # Get token OAuth
    token_oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=SPOTIFY_AUTH_SCOPES,
        cache_path=cache_path,
    )

    # See if we already have one cached
    token_dict = token_oauth.get_cached_token()

    if not token_dict:
        # We don't have a cached token OAuth info; open up auth page in
        # a browser and guide user on auth steps
        print("Please authenticate slats with your Spotify account.")
        print("A Spotify authentication page will now open in your browser.")
        print()
        webbrowser.open(token_oauth.get_authorize_url())

        redirected_url = input("Enter the URL you were redirected to: ")
        print()

        # Parse the response code
        response_code = token_oauth.parse_response_code(redirected_url)
        token_dict = token_oauth.get_access_token(response_code)

    return Spotify(auth=token_dict["access_token"])


def get_users_name(client: Spotify) -> str:
    """Get the authenticated users display name.

    Args:
        client: A spotipy Spotify client.

    Returns:
        Returns the users display name.
    """
    return client.me()["display_name"]


def get_users_saved_albums(client: Spotify) -> List[str]:
    """Get all of the authenticated users saved albums.

    Args:
        client: A spotipy Spotify client.

    Returns:
        A list of album URIs that the user already has saved to their
        account.
    """
    saved_albums = []
    offset = 0

    # Keep hitting the API until we've gone through all the saved albums
    while True:
        # API call
        response = client.current_user_saved_albums(
            limit=SPOTIFY_API_LIMIT, offset=offset
        )

        if not response["items"]:
            # No more saved albums
            break

        # Save all the album URIs
        for item in response["items"]:
            saved_albums += [item["album"]["uri"]]

        # Get the offset right for next API call
        offset += SPOTIFY_API_LIMIT

    return saved_albums


def get_album_uri(
    client: Spotify, album_artist: str, album: str
) -> Optional[Dict[str, str]]:
    """Retrieve the URI for an album.

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


def save_albums(client: Spotify, album_uris: List[str]):
    """Save a list of albums to the authenticated user's profile.

    Args:
        client: A spotipy Spotify client.
        album_uris: A list of album URIs to save.
    """
    client.current_user_saved_albums_add(album_uris)
