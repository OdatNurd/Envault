from os.path import isdir, join, exists
from os import scandir

from .core import log
from ..yaml import safe_load
from ..yaml.scanner import ScannerError


## ----------------------------------------------------------------------------


# Top level folders in the window can have folders by this name to indicate
# that they have some number of configuration files present in them.
#
# Any yaml file that exists in this folder is treated as a config file.
CONFIG_FOLDER = "envault"


## ----------------------------------------------------------------------------


def validate_config(config_filename, config):
    """
    Given a dict object that has been loaded from a configuration file, ensure
    that it is a valid configuration; that is, that it has the keys that are
    expected to be there, and that those keys have the values expected.

    If the object checks out, a version of it containing only the keys from a
    config are returned back; otherwise an exception is raised.
    """
    apiKeyName = config.get("apiKeyName")
    url = config.get("url")
    variables = config.get("vars")

    if not isinstance(apiKeyName, str):
        raise ValueError("apiKeyName must exist and be a string")

    if not isinstance(url, str):
        raise ValueError("url must exist and be a string")

    if (not isinstance(variables, list) or
            not all([isinstance(v, str) for v in variables])):
        raise ValueError("vars must exist and be a list of key strings")

    return {
        "apiKeyName": apiKeyName,
        "url": url,
        "vars": variables
    }


## ----------------------------------------------------------------------------


def load_if_exists(config_filename):
    """
    Given a fully qualified path to a configuration file, attempt to load it.

    The return value is None if the file doesn't exist, fails to load or does
    not conform to the schema for configuration files. Otherwise the return is
    a dict that represents the contents of the configuration.

    In cases where the configuration file exists but is broken, an error is
    logged to ensure the user knows that their file is broken.
    """
    if exists(config_filename):
        try:
            with open(config_filename, "r") as config_file:
                return validate_config(config_filename, safe_load(config_file))

        except ScannerError as e:
            log(f"error loading: {config_filename}:")
            log(str(e))

        except Exception as e:
            log(f"error loading: {config_filename}:")
            log(str(e))

        return False


## ----------------------------------------------------------------------------


def scan_folder(path):
    """
    Scan the path that is provided for all files within it that appear to be
    YAML files based on their extension, and return a list of them back.
    """
    files = []
    with scandir(path) as scanner:
        for entry in scanner:
            if entry.is_file() and entry.name.upper().endswith('.YML'):
                files.append(join(path, entry.name))

    return files


## ----------------------------------------------------------------------------


def scan_project_configs(window):
    """
    Given a window, scan all of the top level folders that are open within that
    window for envault configuration files.

    The return value is a list of all of the located potential configuration
    files. This DOES NOT validate that the configuration in the file is
    correct, only that the file(s) seem to exist.
    """
    files = []

    paths = filter(isdir, [join(p, CONFIG_FOLDER) for p in window.folders()])
    for path in paths:
        files.extend(scan_folder(path))

    return files


## ----------------------------------------------------------------------------
