from .settings import ev_setting
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


def store_env(config_file, new_env):
    """
    Given the full path to a configuration file and the environment result of
    loading it, cache the environment variables into the cache, so that they
    can be retreived later.

    If this configuration file already has an entry in the cache, this will
    replace it.
    """
    if not config_file:
        return log(f"unable to cache env; no config provided")

    if ev_setting("debug"):
        log(f"storing environment for {config_file}")

    _env_cache[config_file] = new_env


def clear_env(config_file):
    """
    For the given configuration file, remove the stored environment, if any.
    This will cause all future cache fetches for this config to return an empty
    dict until the cache is updated with new results.
    """
    if ev_setting("debug"):
        log(f"deleting environment for {config_file}")

    if config_file in _env_cache:
        del _env_cache[config_file]


def fetch_env(config_file):
    """
    Fetch the appropriate environment to use for the given window; the return
    is a dict of all of the variables and the values therein to be used within
    this window.

    If there is no stored env, an empty dict will be returned.
    """
    if ev_setting("debug"):
        log(f"using environment for {config_file}")

    env = _env_cache.get(config_file, None)
    if env is None:
        env = {}
        if ev_setting("debug"):
            log(f"no environment available; using empty default")

    return env


def has_env(config_file):
    """
    Test to see if the given configuration file has previously been loaded
    and the variables fetched.
    """
    return config_file in _env_cache


## ----------------------------------------------------------------------------
