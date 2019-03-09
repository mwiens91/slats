"""Contains constants for the program."""

import os


# Base of the repository/project
PROJECT_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Name of config file
CONFIG_FILE_NAME = "config.yaml"

# Base of XDG config files
try:
    PROJECT_CONFIG_HOME = os.path.join(os.environ["XDG_CONFIG_HOME"], "slats")
except KeyError:
    PROJECT_CONFIG_HOME = os.path.join(os.environ["HOME"], ".config/", "slats")

# Spotify authorization scopes
SPOTIFY_AUTH_SCOPES = "user-library-modify user-library-read"
