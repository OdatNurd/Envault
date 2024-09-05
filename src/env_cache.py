import sublime

from os.path import split

from .core import ev_setting, get_envault_data
from .logging import log


## ----------------------------------------------------------------------------


# A simple object for caching the environment that was loaded for any
# particular configuration file loaded this session.
#
# In the dict, the key is the fully qualified and absolute filename of an
# Envault config, and the value is the result of making a query for the
# variables associated with that file.
_env_cache = { }


## ----------------------------------------------------------------------------


def store_env(window, new_env):
    """
    For the provided window, store the new environment dict provided as the
    environment to apply in that window.

    If this window already has an entry, this will replace it.
    """
    current_config = get_envault_data(window).get("current", None)
    if current_config is None:
        return log(f"unable to cache env; window {window.id()} has no config")

    log(f"loaded envault config from {split(current_config)[1]}", status=True)

    if ev_setting("debug"):
        log(f"variables: {list(new_env.keys())}")

    _env_cache[current_config] = new_env


def clear_env(window):
    """
    For the provided window, remove the stored environment for that window, if
    any. This will cause all fetches to return the default empty dict.
    """
    if ev_setting("debug"):
        log(f"deleting environment for window {window.id()}")

    if window.id() in _env_cache:
        del _env_cache[window.id()]


def fetch_env(window):
    """
    Fetch the appropriate environment to use for the given window; the return
    is a dict of all of the variables and the values therein to be used within
    this window.

    If there is no stored env, an empty dict will be returned.
    """
    current_config = get_envault_data(window).get("current", None)
    if ev_setting("debug"):
        log(f"fetching environment for window {window.id()}")
        if current_config:
            log(f"config file name is {current_config}")

    env = _env_cache.get(current_config, None)
    if env is None:
        env = {}
        if ev_setting("debug"):
            log(f"no environment set for window")

    return env


## ----------------------------------------------------------------------------
