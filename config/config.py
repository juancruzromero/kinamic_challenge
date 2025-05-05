# -*- coding: utf-8 -*-
"""
This is the configuration module.
Loads the YAML configuration file.
"""

import yaml

def load_config() -> dict:
    """Load data from a YAML configuration file.

    Returns:
        dict: Dictionary containing the configuration data.
    """

    path = 'config.yaml'
    with open(path, 'r') as file:
        return yaml.safe_load(file)