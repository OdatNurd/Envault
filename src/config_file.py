import sublime

from os.path import isdir, join, exists, split
from os import scandir, makedirs

from textwrap import dedent

from .logging import log

from ..yaml import safe_load
from ..yaml.scanner import ScannerError

from .env_cache import store_env, clear_env
from .envault_request import EnvaultRequestThread

from .settings import ev_setting


## ----------------------------------------------------------------------------


# Top level folders in the window can have folders by this name to indicate
# that they have some number of configuration files present in them.
#
# Any yaml file that exists in this folder is treated as a config file.
CONFIG_FOLDER = "envault"

# All Envault configuration files must, in addition to being in the above
# mentioned folder, have an extension that matches this one.
CONFIG_EXTENSION = ".yml"

# When creating a new configuration
CONFIG_TEMPLATE = dedent("""
# Envault to request keys from, and the API key to use to authenticate the
# request. The API key provided here specifies the name of an environment
# variable whose value is the actual API key to use.
apiKeyName: {apiKeyName}
url: {url}

# The list of variable specifications to request from the server; each spec
# will produce some number of environment variables and values. See the
# Envault server documentation for more information.
vars: []
#  - spec1
#  - spec2
""").lstrip()


## ----------------------------------------------------------------------------


def validate_config(config_file, config):
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
        raise ValueError(f"{config_file}: apiKeyName must exist and be a string")

    if not isinstance(url, str):
        raise ValueError(f"{config_file}: url must exist and be a string")

    if (not isinstance(variables, list) or
            not all([isinstance(v, str) for v in variables])):
        raise ValueError(f"{config_file}: vars must exist and be a list of key strings")

    return {
        "apiKeyName": apiKeyName,
        "url": url,
        "vars": variables
    }


## ----------------------------------------------------------------------------


def load_if_exists(config_file):
    """
    Given a fully qualified path to a configuration file, attempt to load it.

    The return value is None if the file doesn't exist, False if it fails to
    load or does not conform to the schema for configuration files, or  is a
    dict that represents the contents of the configuration.

    In cases where the configuration file exists but is broken, an error is
    logged to ensure the user knows that their file is broken.
    """
    if not exists(config_file):
        return log(f"file '{config_file}' does not exist")

    try:
        with open(config_file, "r") as file:
            return validate_config(config_file, safe_load(file))

    except ScannerError as e:
        log(f"error loading: {config_file}:")
        log(str(e))

    except Exception as e:
        log(f"error loading: {config_file}:")
        log(str(e))

    return False


## ----------------------------------------------------------------------------


def _accept_loaded_config(var_list, config_file):
    """
    Invoked after a call to load_and_fetch_config() to accept the loaded config
    data, if any.

    This will update the environment cache associated with the result, either
    storing in a new config or clobbering one that might have already existed
    from a previous call, depending on whether or not it worked.
    """
    if var_list is None:
        log("no variables to set; request failed")
        # If a request failed, update the cache to not have any values, but
        # keep a record of this config still being active. This allows the
        # post-save event listener to tell that this config is still active,
        # so that fixing it if you break it will allow it to reload.
        store_env(config_file, {})
        return

    log(f"loaded envault config from {split(config_file)[1]}", status=True)
    if ev_setting("debug"):
        log(f"variables: {list(var_list.keys())}")

    store_env(config_file, var_list)


## ----------------------------------------------------------------------------


def load_and_fetch_config(config_file):
    """
    Given an envault configuration filenam that we presume exists, load the
    config and then invoke a request to the server to fetch the variables that
    the config defines.

    Any config load or validation error will result in error logs and a message
    dialog indicating the problem.

    Sucessful loads from the server will update the cache; request failures
    will get logged as well.
    """
    config = load_if_exists(config_file)
    if not config:
        return log("""
            Error loading the Envault config file; see the
            console for error details.
            """, error=True)

    # Kick off a background request to fetch the actual environment keys
    # that are being requested by this config.
    EnvaultRequestThread(**config, config_file=config_file, callback=
                         lambda r: _accept_loaded_config(r, config_file)).start()


## ----------------------------------------------------------------------------


def scan_folder(path):
    """
    Scan the path that is provided for all files within it that appear to be
    YAML files based on their extension, and return a list of them back.
    """
    files = []
    with scandir(path) as scanner:
        for entry in scanner:
            if entry.is_file() and entry.name.lower().endswith(CONFIG_EXTENSION):
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


def create_config(config_name, apiKeyName, url, window=None):
    """
    Given the name of a configuration file to create, create one using the
    template, filling out the API key name and URL from the values provided
    in the call.

    The created file will be opened for editing in the window provided; if no
    window is provided, the current window will be opened instead.

    This will ensure that the folder that should contain the file exists, if it
    does not yet. It will also clobber over any existing file that might exist.
    """
    path, _ = split(config_name)
    makedirs(path, exist_ok=True)

    with open(config_name, "w") as file:
        file.write(CONFIG_TEMPLATE.format(
            apiKeyName=apiKeyName,
            url=url))

    window = window or sublime.active_window()
    window.open_file(config_name)


## ----------------------------------------------------------------------------
