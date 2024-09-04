from os.path import join, exists

from .core import log
from ..yaml import safe_load
from ..yaml.scanner import ScannerError


## ----------------------------------------------------------------------------


# The name of the configuration files that we look for that control the
# variables returned by envault.
CONFIG_FILENAME = "envault-config.yml"


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


def scan_project_configs(window):
    """
    Given a window, scan all of the top level folders that are open within that
    window for envault configuration files.

    The return value is a list of all of the located potential configuration
    files. This DOES NOT validate that the configuration in the file is
    correct, only that the file seems to exist.
    """
    files = [join(path, CONFIG_FILENAME) for path in window.folders()]
    return [f for f in files if exists(f)]


## ----------------------------------------------------------------------------
