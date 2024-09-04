import sublime

from .core import log, ev_setting


## ----------------------------------------------------------------------------


# A simple object for caching the environment that's in use in any particular
# window.
#
# In the dict, the key is the ID value of a window, and the value is the
# list of environment variables.
#
# TODO: This should actually use as the key, the name of the config file that
#       is in use in the window as a complete path; then any window that has
#       the same folder open can use it, we can close and re-open a window and
#       have the same config available, and we don't need to track windows
#       closing so we can clean this up (which is currently not done).
_env_cache = { }


## ----------------------------------------------------------------------------


def store_env(window, new_env):
    """
    For the provided window, store the new environment dict provided as the
    environment to apply in that window.

    If this window already has an entry, this will replace it.
    """
    if ev_setting("debug"):
        log(f"storing new environment for window {window.id()}")
        log(f"variables: {list(new_env.keys())}")

    _env_cache[window.id()] = new_env


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
    if ev_setting("debug"):
        log(f"fetching environment for window {window.id()}")

    env = _env_cache.get(window.id(), None)
    if env is None and ev_setting("debug"):
        log(f"no environment set for window")
        env = {}

    return env


## ----------------------------------------------------------------------------
