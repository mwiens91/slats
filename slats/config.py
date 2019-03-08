"""Contains functions relating to the configuration file."""

import os
from typing import Dict, Optional
import yaml
from .constants import CONFIG_FILE_NAME, PROJECT_BASE_DIR, PROJECT_CONFIG_HOME
from .exceptions import ConfigFileNotFound


def find_config_file() -> str:
    """Find and return the path of a config file.

    The config file looked for is "config.yaml" and it is looked for at
    the base of the respository first (if you're running from source),
    and then in $XDG_CONFIG_HOME/slats/ (XDG_CONFIG_HOME defaults to
    $HOME/.config).

    Returns:
        A string containing the absolute path to the config file.

    Raises:
        ConfigFileNotFound: A config file couldn't be found.
    """
    # Check the base of the project
    config_path = os.path.join(PROJECT_BASE_DIR, CONFIG_FILE_NAME)

    if os.path.exists(config_path):
        return config_path

    # Check XDG_CONFIG_HOME
    config_path = os.path.join(PROJECT_CONFIG_HOME, CONFIG_FILE_NAME)

    if os.path.exists(config_path):
        return config_path

    # Couldn't find anything :thinking:
    raise ConfigFileNotFound


def parse_config_file(config_path: Optional[str] = None) -> Dict[str, str]:
    """Find and parse a config file.

    Args:
        config_path: An optional path to the config file. If not passed
            in, looks for the config file as documented in the
            find_config_file function.

    Returns:
        A dictionary containing the variables specified in the config
        file.

    Raises:
        ConfigFileNotFound: A config file couldn't be found.
    """
    if config_path is None:
        # Find the config file
        config_path = find_config_file()

    # Now parse and return it
    try:
        with open(config_path, "r") as config_file:
            return yaml.safe_load(config_file)
    except IOError:
        # Be consistent with types of exceptions thrown
        raise ConfigFileNotFound
