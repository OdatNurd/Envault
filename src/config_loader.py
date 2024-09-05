from os.path import isdir, join, exists
from os import scandir

from .logging import log

from ..yaml import safe_load
from ..yaml.scanner import ScannerError

from .env_cache import store_env, clear_env
from .envault_request import EnvaultRequestThread


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

    The return value is None if the file doesn't exist, False if it fails to
    load or does not conform to the schema for configuration files, or  is a
    dict that represents the contents of the configuration.

    In cases where the configuration file exists but is broken, an error is
    logged to ensure the user knows that their file is broken.
    """
    if not exists(config_filename):
        return log(f"file '{config_filename}' does not exist")

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


def _accept_loaded_config(var_list, window):
    """
    Invoked after a call to load_and_fetch_config() to accept the loaded config
    data, if any.

    This will update the environment cache associated with the result, either
    storing in a new config or clobbering one that might have already existed
    from a previous call, depending on whether or not it worked.
    """
    if var_list is None:
        log("no variables to set; request failed")
        clear_env(window)
    else:
        store_env(window, var_list)


## ----------------------------------------------------------------------------


def load_and_fetch_config(config_filename, window):
    """
    Given a filename that we presume exists and the window that it is
    associated with, load it from disk and then invoke a request to actually
    fetch the variables that go with the config.

    If there is an error loading the config file, an error dialog is displayed
    and nothing else happens.

    Otherwise, once the fetch is complete the environment cache is updated with
    the result; either updating the environment cache to add new values, or to
    remove previous results if the request failed.
    """
    config = load_if_exists(config_filename)
    if not config:
        return log("""
            Error loading the Envault config file; see the
            console for error details.
            """, error=True)

    # Kick off a background request to fetch the actual environment keys
    # that are being requested by this config.
    EnvaultRequestThread(**config, callback=
                         lambda r: _accept_loaded_config(r, window)).start()


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
